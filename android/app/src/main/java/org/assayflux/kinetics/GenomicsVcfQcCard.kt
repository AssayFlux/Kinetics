package org.assayflux.kinetics

import android.content.Context
import android.net.Uri
import android.provider.OpenableColumns
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Checkbox
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.nio.charset.CodingErrorAction

private data class VcfQcDocument(val name: String, val text: String)

private fun readVcfQcDocument(context: Context, uri: Uri): VcfQcDocument {
    val name = context.contentResolver.query(
        uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
    )?.use { cursor ->
        if (cursor.moveToFirst()) cursor.getString(0) else null
    } ?: uri.lastPathSegment ?: "variants.vcf"
    require(name.endsWith(".vcf", ignoreCase = true)) {
        "Select an uncompressed .vcf file. VCF.GZ is not supported by this screen."
    }
    val input = context.contentResolver.openInputStream(uri)
        ?: error("The selected VCF document could not be opened.")
    val bytes = input.use { stream ->
        val output = ByteArrayOutputStream()
        val buffer = ByteArray(16 * 1024)
        var total = 0
        while (true) {
            val count = stream.read(buffer)
            if (count < 0) break
            total += count
            require(total <= GenomicsVcfQcRunner.MAX_INPUT_BYTES) {
                "VCF input exceeds the 5 MiB limit."
            }
            output.write(buffer, 0, count)
        }
        output.toByteArray()
    }
    val text = Charsets.UTF_8.newDecoder()
        .onMalformedInput(CodingErrorAction.REPORT)
        .onUnmappableCharacter(CodingErrorAction.REPORT)
        .decode(ByteBuffer.wrap(bytes)).toString()
    require(!text.contains('\u0000')) { "VCF input contains a NUL byte." }
    return VcfQcDocument(name, text)
}

/** P1 aggregate-only VCF syntax/QC surface; no sample-level result is exposed. */
@Composable
internal fun GenomicsVcfQcCard() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var consentConfirmed by rememberSaveable { mutableStateOf(false) }
    var selectedUri by remember { mutableStateOf<Uri?>(null) }
    var selectedName by remember { mutableStateOf<String?>(null) }
    var report by remember { mutableStateOf<JSONObject?>(null) }
    var status by remember { mutableStateOf("Choose a synthetic or authorized public non-patient VCF file.") }
    var error by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }

    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        selectedUri = uri
        selectedName = uri?.let {
            runCatching {
                context.contentResolver.query(
                    it, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null,
                )?.use { cursor -> if (cursor.moveToFirst()) cursor.getString(0) else null }
            }.getOrNull()
        }
        consentConfirmed = false
        report = null
        error = null
        status = if (uri == null) "No file selected." else "File selected. Confirm the data boundary before running aggregate QC."
    }

    Card(Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("P1 · VCF aggregate research QC", style = MaterialTheme.typography.titleMedium)
            Text(
                "Bounded local VCF syntax and record summary. Only aggregate counts are returned; sample identifiers and genotype strings are not displayed or persisted.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(
                onClick = { picker.launch(arrayOf("text/vcf", "text/plain", "*/*")) },
                enabled = !busy,
                modifier = Modifier.fillMaxWidth(),
            ) { Text("Choose VCF file") }
            selectedName?.let { Text("File: $it", style = MaterialTheme.typography.labelMedium) }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = consentConfirmed, onCheckedChange = {
                    consentConfirmed = it
                    report = null
                })
                Text(
                    "I confirm this file contains only synthetic or authorized public non-patient data.",
                    style = MaterialTheme.typography.bodySmall,
                )
            }
            Text(
                "This declaration is an operator attestation, not automated verification of data origin. Do not select patient, clinical, identifiable or human-subject data.",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(
                onClick = {
                    val uri = selectedUri ?: return@Button
                    busy = true
                    error = null
                    report = null
                    status = "Checking the selected VCF locally…"
                    scope.launch {
                        val outcome = withContext(Dispatchers.IO) {
                            runCatching {
                                val document = readVcfQcDocument(context, uri)
                                document.name to GenomicsVcfQcRunner.analyze(context, document.text)
                            }
                        }
                        outcome.onSuccess {
                            selectedName = it.first
                            report = it.second
                            status = "Aggregate QC completed in memory. Input text was not saved by this screen."
                        }.onFailure {
                            error = it.message ?: "VCF QC failed."
                            status = "No result was produced."
                        }
                        busy = false
                    }
                },
                enabled = !busy && selectedUri != null && consentConfirmed,
                modifier = Modifier.fillMaxWidth(),
            ) { Text(if (busy) "Checking…" else "Run aggregate QC") }
            Text(status, style = MaterialTheme.typography.bodySmall)
            error?.let { Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
            report?.let { result ->
                HorizontalDivider()
                Text(
                    "${result.optInt("record_count")} variant records · ${result.optInt("contig_count")} contigs · ${result.optInt("sample_count")} sample columns",
                    fontWeight = androidx.compose.ui.text.font.FontWeight.SemiBold,
                )
                Text(
                    "SNV records ${result.optInt("snv_record_count")} · multiallelic ${result.optInt("multiallelic_record_count")} · missing QUAL ${result.optInt("missing_quality_record_count")}",
                    style = MaterialTheme.typography.bodySmall,
                )
                Text("FILTER counts", style = MaterialTheme.typography.labelLarge)
                result.optJSONObject("filter_counts")?.let { counts ->
                    counts.keys().asSequence().sorted().forEach { key ->
                        Text("$key · ${counts.optInt(key)}", style = MaterialTheme.typography.bodySmall)
                    }
                }
                Text("Contig counts", style = MaterialTheme.typography.labelLarge)
                result.optJSONObject("contig_record_counts")?.let { counts ->
                    counts.keys().asSequence().sorted().forEach { key ->
                        Text("$key · ${counts.optInt(key)}", style = MaterialTheme.typography.bodySmall)
                    }
                }
                Text("Input SHA-256 · ${result.optString("source_sha256")}", style = MaterialTheme.typography.labelSmall)
                val limitations = result.optJSONArray("limitations")
                if (limitations != null) {
                    for (index in 0 until limitations.length()) {
                        Text("• ${limitations.optString(index)}", style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}
