package org.assayflux.kinetics

import android.content.Context
import android.net.Uri
import androidx.work.Worker
import androidx.work.WorkerParameters
import java.security.MessageDigest

class ImportWorker(context: Context, parameters: WorkerParameters) : Worker(context, parameters) {
    override fun doWork(): Result {
        val jobId = inputData.getString(KEY_JOB_ID) ?: return Result.failure()
        val uri = Uri.parse(inputData.getString(KEY_URI) ?: return Result.failure())
        val store = ResearchStore(applicationContext)
        store.updateJob(jobId, "running")
        return try {
            val digest = MessageDigest.getInstance("SHA-256")
            var byteCount = 0L
            val input = applicationContext.contentResolver.openInputStream(uri)
                ?: throw IllegalStateException("Selected document could not be opened")
            input.use { stream ->
                val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                while (true) {
                    if (isStopped) {
                        store.updateJob(jobId, "cancelled", message = "Cancellation requested")
                        return Result.failure()
                    }
                    val count = stream.read(buffer)
                    if (count < 0) break
                    byteCount += count
                    if (byteCount > MAX_IMPORT_BYTES) {
                        throw IllegalArgumentException("Input exceeds the 512 MiB import limit")
                    }
                    digest.update(buffer, 0, count)
                }
            }
            val hash = digest.digest().joinToString("") { "%02x".format(it) }
            store.updateJob(jobId, "succeeded", hash, byteCount,
                "Imported and hashed; no scientific analysis performed")
            store.recordProvenance(jobId, hash)
            Result.success()
        } catch (error: Exception) {
            store.updateJob(jobId, "failed", message = error.message ?: error.javaClass.simpleName)
            Result.failure()
        }
    }
    companion object {
        const val KEY_JOB_ID = "job_id"
        const val KEY_URI = "input_uri"
        const val MAX_IMPORT_BYTES = 512L * 1024L * 1024L
    }
}
