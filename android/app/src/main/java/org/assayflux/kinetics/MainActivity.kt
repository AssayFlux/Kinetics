package org.assayflux.kinetics

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import java.util.UUID
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { KineticsResearchHome(this) }
    }
}

@androidx.compose.runtime.Composable
private fun KineticsResearchHome(activity: ComponentActivity) {
    val store = remember { ResearchStore(activity) }
    var jobs by remember { mutableStateOf(store.recentJobs()) }
    var notice by remember { mutableStateOf("Research Mode. Local files stay on this device.") }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            runCatching {
                activity.contentResolver.takePersistableUriPermission(
                    uri, android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            val id = UUID.randomUUID().toString()
            val name = uri.lastPathSegment ?: "Imported document"
            store.createJob(id, name, uri.toString())
            val request = OneTimeWorkRequestBuilder<ImportWorker>()
                .setInputData(workDataOf(ImportWorker.KEY_JOB_ID to id, ImportWorker.KEY_URI to uri.toString()))
                .addTag("kinetics-import").build()
            WorkManager.getInstance(activity).enqueueUniqueWork(
                "import-$id", ExistingWorkPolicy.KEEP, request)
            notice = "Import queued. The file will be streamed and hashed in the background."
            jobs = store.recentJobs()
        }
    }
    LaunchedEffect(Unit) {
        while (true) {
            delay(1000)
            jobs = store.recentJobs()
        }
    }
    MaterialTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
            Column(modifier = Modifier.fillMaxSize().padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text("Kinetics Research Workbench", style = MaterialTheme.typography.headlineSmall)
                Text("Research Mode only • Offline-first • No clinical use")
                Text(notice)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { picker.launch(arrayOf("*/*")) }) { Text("Import research file") }
                    Button(onClick = { jobs = store.recentJobs() }) { Text("Refresh") }
                }
                Text("Recent jobs", style = MaterialTheme.typography.titleMedium)
                LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(jobs, key = { it.id }) { job ->
                        Column {
                            Text(job.inputName, style = MaterialTheme.typography.bodyLarge)
                            Text("State: ${job.state}")
                            job.sha256?.let { Text("SHA-256: $it") }
                            job.message?.let { Text(it) }
                        }
                    }
                }
            }
        }
    }
}
