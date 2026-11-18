package org.assayflux.kinetics

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@Composable
internal fun PublicDatabaseCard() {
    var query by rememberSaveable { mutableStateOf("") }
    var hits by remember { mutableStateOf(emptyList<PublicDatabaseHit>()) }
    var record by remember { mutableStateOf<PublicScientificRecord?>(null) }
    var busy by remember { mutableStateOf(false) }
    var message by remember { mutableStateOf("Search public reference records. Internet is used only when you choose an action.") }
    val scope = rememberCoroutineScope()
    val client = remember { PublicDatabaseClient() }

    Card(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text("Public scientific databases", style = MaterialTheme.typography.titleMedium)
            Text(
                "Search NCBI Gene and UniProtKB, retrieve protein sequences, or open an RCSB structure by PDB ID. Records are fetched inside Kinetics.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            OutlinedTextField(
                value = query,
                onValueChange = { query = it; message = "Search by gene/protein name or accession. For structures, enter a four-character PDB ID." },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("Gene, protein or PDB ID") },
                singleLine = true,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    enabled = !busy && query.trim().length >= 2,
                    onClick = {
                        busy = true
                        record = null
                        scope.launch {
                            val result = runCatching {
                                withContext(Dispatchers.IO) { client.searchNcbiGene(query) }
                            }
                            hits = result.getOrDefault(emptyList())
                            message = result.fold(
                                { "NCBI Gene: ${it.size} results" },
                                { "NCBI search failed: ${it.message ?: "request error"}" },
                            )
                            busy = false
                        }
                    },
                ) { Text("Search genes") }
                Button(
                    enabled = !busy && query.trim().length >= 2,
                    onClick = {
                        busy = true
                        record = null
                        scope.launch {
                            val result = runCatching {
                                withContext(Dispatchers.IO) { client.searchUniProt(query) }
                            }
                            hits = result.getOrDefault(emptyList())
                            message = result.fold(
                                { "UniProtKB: ${it.size} results" },
                                { "UniProtKB search failed: ${it.message ?: "request error"}" },
                            )
                            busy = false
                        }
                    },
                ) { Text("Search proteins") }
            }
            Button(
                enabled = !busy && query.trim().matches(Regex("[0-9][A-Za-z0-9]{3}")),
                onClick = {
                    busy = true
                    hits = emptyList()
                    scope.launch {
                        val result = runCatching {
                            withContext(Dispatchers.IO) { client.fetchRcsbMmcif(query) }
                        }
                        record = result.getOrNull()
                        message = result.fold(
                            { "RCSB mmCIF fetched. It is shown as a source record, not yet parsed into the 3D viewer." },
                            { "RCSB retrieval failed: ${it.message ?: "request error"}" },
                        )
                        busy = false
                    }
                },
            ) { Text("Fetch PDB structure") }
            if (busy) CircularProgressIndicator()
            Text(message, style = MaterialTheme.typography.bodySmall)
            hits.take(6).forEach { hit ->
                Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                    Text(hit.title, style = MaterialTheme.typography.bodyMedium)
                    Text(
                        listOfNotNull(hit.source, hit.accession, hit.organism).joinToString(" · "),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    hit.description?.let {
                        Text(it, style = MaterialTheme.typography.bodySmall, maxLines = 2, overflow = TextOverflow.Ellipsis)
                    }
                    if (hit.source == "UniProtKB") {
                        TextButton(
                            enabled = !busy,
                            onClick = {
                                busy = true
                                scope.launch {
                                    val result = runCatching {
                                        withContext(Dispatchers.IO) { client.fetchUniProtFasta(hit.accession) }
                                    }
                                    record = result.getOrNull()
                                    message = result.fold(
                                        { "Protein FASTA retrieved from UniProtKB. Choose a later analysis/import action to process it." },
                                        { "FASTA retrieval failed: ${it.message ?: "request error"}" },
                                    )
                                    busy = false
                                }
                            },
                        ) { Text("Fetch FASTA") }
                    }
                }
            }
            record?.let { fetched ->
                Text(
                    "${fetched.source} · ${fetched.accession} · ${fetched.format}\nSHA-256: ${fetched.sha256}\nRetrieved: ${fetched.retrievedAt}",
                    style = MaterialTheme.typography.labelSmall,
                )
                Text(
                    fetched.content.take(1800),
                    modifier = Modifier.fillMaxWidth().heightIn(max = 180.dp).verticalScroll(rememberScrollState()),
                    style = MaterialTheme.typography.bodySmall,
                )
                Text(
                    "This retrieval is currently session-only. It is not saved to the research store or dispatched to an analysis engine yet.",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}
