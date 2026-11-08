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
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkInfo
import androidx.work.WorkManager
import androidx.work.workDataOf
import java.util.UUID
import java.io.File
import java.security.MessageDigest
import androidx.lifecycle.Observer
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

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
    var runtimeReport by remember { mutableStateOf<String?>(null) }
    var deleteTarget by remember { mutableStateOf<ResearchJob?>(null) }
    val scope = rememberCoroutineScope()
    var pendingExportJob by remember { mutableStateOf<String?>(null) }
    val exportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/octet-stream"),
    ) { uri ->
        val jobId = pendingExportJob
        pendingExportJob = null
        if (uri != null && jobId != null) {
            scope.launch {
                notice = "Exporting verified research input..."
                val result = withContext(Dispatchers.IO) {
                    runCatching {
                        val output = activity.contentResolver.openOutputStream(uri, "w")
                            ?: error("Selected export destination could not be opened")
                        output.use { stream ->
                            check(store.exportStoredInput(jobId, stream)) {
                                "No completed encrypted input exists for this job"
                            }
                        }
                    }
                }
                notice = result.fold(
                    { "Verified research input exported successfully." },
                    { "Export failed: ${it.message ?: it.javaClass.simpleName}" },
                )
            }
        }
    }
    val picker = rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if (uri != null) {
            val persistentReadGrant = runCatching {
                activity.contentResolver.takePersistableUriPermission(
                    uri, android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }.isSuccess
            if (!persistentReadGrant) {
                notice = "This document provider did not grant persistent read access. Choose a file from a provider that supports resumable access."
                return@rememberLauncherForActivityResult
            }
            val id = UUID.randomUUID().toString()
            val name = uri.lastPathSegment ?: "Imported document"
            store.createJob(id, name, uri.toString())
            val request = OneTimeWorkRequestBuilder<ImportWorker>()
                .setInputData(workDataOf(ImportWorker.KEY_JOB_ID to id, ImportWorker.KEY_URI to uri.toString()))
                .addTag("kinetics-import").build()
            WorkManager.getInstance(activity).enqueueUniqueWork(
                "import-$id", ExistingWorkPolicy.KEEP, request)
            notice = "Import queued. The file will be streamed, encrypted at rest and hashed in the background."
            jobs = store.recentJobs()
        }
    }
    DisposableEffect(activity) {
        val manager = WorkManager.getInstance(activity)
        // Recover imports interrupted by process death. KEEP prevents duplicate workers
        // when WorkManager already has an unfinished unique job.
        store.recoverableImports().forEach { pending ->
            val uri = android.net.Uri.parse(pending.uri)
            val hasReadGrant = activity.contentResolver.persistedUriPermissions.any {
                it.uri == uri && it.isReadPermission
            }
            if (!hasReadGrant) {
                store.updateJob(
                    pending.id, "failed",
                    message = "Recovery blocked: persistent document read permission was revoked",
                )
            } else {
                val request = OneTimeWorkRequestBuilder<ImportWorker>()
                    .setInputData(workDataOf(
                        ImportWorker.KEY_JOB_ID to pending.id,
                        ImportWorker.KEY_URI to pending.uri,
                    ))
                    .addTag("kinetics-import")
                    .build()
                manager.enqueueUniqueWork(
                    "import-${pending.id}", ExistingWorkPolicy.KEEP, request,
                )
            }
        }
        val workInfos = manager.getWorkInfosByTagLiveData("kinetics-import")
        val observer = Observer<List<WorkInfo>> { jobs = store.recentJobs() }
        workInfos.observe(activity, observer)
        jobs = store.recentJobs()
        onDispose { workInfos.removeObserver(observer) }
    }
    MaterialTheme {
        Surface(modifier = Modifier.fillMaxSize()) {
            Column(modifier = Modifier.fillMaxSize().padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text(
                    "Kinetics Research Workbench",
                    modifier = Modifier.semantics {
                        contentDescription = "Kinetics Research Workbench home"
                    },
                    style = MaterialTheme.typography.headlineSmall,
                )
                Text(
                    "Research Mode only • Offline-first • No clinical use",
                    modifier = Modifier.semantics {
                        contentDescription = "Research Mode only. Offline first. Not for clinical use."
                    },
                )
                Text(notice)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = { picker.launch(arrayOf("*/*")) }) { Text("Import research file") }
                    Button(onClick = { jobs = store.recentJobs() }) { Text("Refresh") }
                }
                Button(onClick = {
                    scope.launch {
                        runtimeReport = "Running local Python and native runtime probes..."
                        runtimeReport = withContext(Dispatchers.IO) {
                            val python = runCatching { PythonProbe.report(activity) }
                                .getOrElse { "FAILED: ${it.message ?: it.javaClass.simpleName}" }
                            val native = runCatching {
                                val probe = NativeProbe()
                                val cpp = probe.cppSumSquares(3.0, 4.0)
                                val rust = probe.rustSumSquares(3.0, 4.0)
                                check(kotlin.math.abs(cpp - 25.0) < 1e-9) { "C++ JNI result mismatch" }
                                check(kotlin.math.abs(rust - 25.0) < 1e-9) { "Rust FFI result mismatch" }
                                val aad = LocalCrypto.associatedData("runtime-probe", 0)
                                val plaintext = "kinetics-keystore-probe".toByteArray()
                                val encrypted = LocalCrypto.encrypt(plaintext, aad)
                                check(LocalCrypto.decrypt(encrypted, aad).contentEquals(plaintext)) {
                                    "Android Keystore AES-GCM roundtrip mismatch"
                                }
                                val wrongAadRejected = runCatching {
                                    LocalCrypto.decrypt(encrypted, LocalCrypto.associatedData("wrong-job", 0))
                                }.isFailure
                                check(wrongAadRejected) { "AES-GCM did not reject mismatched authenticated metadata" }
                                val cryptoDir = File(activity.cacheDir, "kinetics-crypto-probe").apply { mkdirs() }
                                val encryptedFile = File(cryptoDir, "probe.kdat")
                                val plaintextFile = File(cryptoDir, "probe.txt")
                                try {
                                    LocalCrypto.ensureChunkedFileHeader(encryptedFile)
                                    LocalCrypto.appendEncryptedChunk(encryptedFile, plaintext, aad)
                                    val hash = MessageDigest.getInstance("SHA-256").digest(plaintext)
                                        .joinToString("") { "%02x".format(it) }
                                    LocalCrypto.decryptChunkedFile(
                                        encryptedFile, plaintextFile, "runtime-probe", hash,
                                    )
                                    check(plaintextFile.readBytes().contentEquals(plaintext)) {
                                        "Versioned encrypted-file roundtrip mismatch"
                                    }
                                } finally {
                                    encryptedFile.delete()
                                    plaintextFile.delete()
                                    cryptoDir.delete()
                                }
                                "C++ JNI: $cpp; Rust FFI: $rust; Keystore AES-GCM + versioned file roundtrip: passed"
                            }.getOrElse { "FAILED: ${it.message ?: it.javaClass.simpleName}" }
                            "Python probe:\n$python\nNative probe: $native"
                        }
                    }
                }) { Text("Run local runtime probes") }
                runtimeReport?.let { Text(it, style = MaterialTheme.typography.bodySmall) }
                Text("Recent jobs", style = MaterialTheme.typography.titleMedium)
                LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(jobs, key = { it.id }) { job ->
                        Column(
                            modifier = Modifier.semantics(mergeDescendants = true) {
                                contentDescription = "Research import: " + job.inputName +
                                    ". State: " + job.state + "."
                            },
                        ) {
                            Text(job.inputName, style = MaterialTheme.typography.bodyLarge)
                            Text("State: ${job.state}")
                            job.sha256?.let { Text("SHA-256: $it") }
                            job.message?.let { Text(it) }
                            if (job.state == "succeeded" || job.state == "failed" || job.state == "cancelled") {
                                TextButton(onClick = { deleteTarget = job }) { Text("Delete local data") }
                            }
                            if (job.state == "succeeded" && job.sha256 != null) {
                                Button(onClick = {
                                    pendingExportJob = job.id
                                    exportPicker.launch(job.inputName.substringAfterLast('/').take(120).ifBlank { "kinetics-research-export.bin" })
                                }) { Text("Export original file") }
                            }
                            if (job.state == "queued" || job.state == "running" || job.state == "cancel_requested") {
                                Button(onClick = {
                                    store.updateJob(job.id, "cancel_requested")
                                    WorkManager.getInstance(activity).cancelUniqueWork("import-" + job.id)
                                    jobs = store.recentJobs()
                                }) { Text("Cancel") }
                            } else if (job.state == "cancelled" || job.state == "failed") {
                                Button(onClick = {
                                    val savedUri = store.inputUri(job.id)
                                    if (savedUri != null) {
                                        val request = OneTimeWorkRequestBuilder<ImportWorker>()
                                            .setInputData(workDataOf(
                                                ImportWorker.KEY_JOB_ID to job.id,
                                                ImportWorker.KEY_URI to savedUri,
                                            )).addTag("kinetics-import").build()
                                        WorkManager.getInstance(activity).enqueueUniqueWork(
                                            "import-" + job.id, ExistingWorkPolicy.REPLACE, request)
                                        store.updateJob(job.id, "queued", message = "Resume queued")
                                        jobs = store.recentJobs()
                                    }
                                }) { Text("Resume") }
                            }
                        }
                    }
                }
            }
        }
        deleteTarget?.let { target ->
            AlertDialog(
                onDismissRequest = { deleteTarget = null },
                title = { Text("Delete local research data?") },
                text = {
                    Text(
                        "This removes the encrypted local input, any retained encrypted partial, " +
                            "and job/provenance metadata. It cannot delete copies you previously exported. " +
                            "Flash storage secure erasure is not guaranteed."
                    )
                },
                confirmButton = {
                    TextButton(onClick = {
                        deleteTarget = null
                        WorkManager.getInstance(activity).cancelUniqueWork("import-" + target.id)
                        scope.launch {
                            val result = withContext(Dispatchers.IO) {
                                runCatching { store.deleteStoredJob(target.id) }
                            }
                            notice = result.fold(
                                { "Local research data deleted." },
                                { "Deletion failed: ${it.message ?: it.javaClass.simpleName}" },
                            )
                            jobs = store.recentJobs()
                        }
                    }) { Text("Delete") }
                },
                dismissButton = {
                    TextButton(onClick = { deleteTarget = null }) { Text("Keep data") }
                },
            )
        }
    }
}
