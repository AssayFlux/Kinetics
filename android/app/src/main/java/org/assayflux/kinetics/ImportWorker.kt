package org.assayflux.kinetics

import android.content.Context
import android.net.Uri
import androidx.work.Worker
import androidx.work.WorkerParameters
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.security.MessageDigest

class ImportWorker(context: Context, parameters: WorkerParameters) : Worker(context, parameters) {
    override fun doWork(): Result {
        val jobId = inputData.getString(KEY_JOB_ID) ?: return Result.failure()
        val uri = Uri.parse(inputData.getString(KEY_URI) ?: return Result.failure())
        val store = ResearchStore(applicationContext)
        val partial = File(applicationContext.cacheDir, "kinetics-import-$jobId.part")
        store.updateJob(jobId, "running")
        return try {
            val digest = MessageDigest.getInstance("SHA-256")
            var byteCount = 0L
            if (partial.exists()) {
                FileInputStream(partial).use { input ->
                    val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                    while (true) {
                        val count = input.read(buffer)
                        if (count < 0) break
                        byteCount += count
                        digest.update(buffer, 0, count)
                    }
                }
            }
            if (byteCount > MAX_IMPORT_BYTES) {
                throw IllegalArgumentException("Partial input exceeds the 512 MiB import limit")
            }
            val input = applicationContext.contentResolver.openInputStream(uri)
                ?: throw IllegalStateException("Selected document could not be opened")
            input.use { source ->
                var skipped = 0L
                while (skipped < byteCount) {
                    val count = source.skip(byteCount - skipped)
                    if (count <= 0) {
                        if (source.read() < 0) throw IllegalStateException("Source changed or became shorter during resume")
                        skipped++
                    } else {
                        skipped += count
                    }
                }
                FileOutputStream(partial, true).use { output ->
                    val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                    var sinceSync = 0L
                    while (true) {
                        if (isStopped) {
                            output.flush()
                            output.fd.sync()
                            store.updateProgress(jobId, byteCount)
                            store.updateJob(jobId, "cancelled", bytes = byteCount,
                                message = "Partial import retained; resume is available")
                            return Result.failure()
                        }
                        val count = source.read(buffer)
                        if (count < 0) break
                        byteCount += count
                        if (byteCount > MAX_IMPORT_BYTES) {
                            throw IllegalArgumentException("Input exceeds the 512 MiB import limit")
                        }
                        output.write(buffer, 0, count)
                        digest.update(buffer, 0, count)
                        sinceSync += count
                        if (sinceSync >= CHECKPOINT_BYTES) {
                            output.flush()
                            output.fd.sync()
                            store.updateProgress(jobId, byteCount)
                            setProgressAsync(androidx.work.workDataOf("bytes" to byteCount))
                            sinceSync = 0
                        }
                    }
                    output.flush()
                    output.fd.sync()
                }
            }
            val hash = digest.digest().joinToString("") { "%02x".format(it) }
            store.updateJob(jobId, "succeeded", hash, byteCount,
                "Imported, resumed if needed, and hashed; no scientific analysis performed")
            store.recordProvenance(jobId, hash)
            partial.delete()
            Result.success()
        } catch (error: Exception) {
            store.updateJob(jobId, "failed", bytes = byteCountOrZero(partial),
                message = error.message ?: error.javaClass.simpleName)
            Result.failure()
        }
    }

    private fun byteCountOrZero(file: File): Long = if (file.exists()) file.length() else 0L

    companion object {
        const val KEY_JOB_ID = "job_id"
        const val KEY_URI = "input_uri"
        const val MAX_IMPORT_BYTES = 512L * 1024L * 1024L
        const val CHECKPOINT_BYTES = 4L * 1024L * 1024L
    }
}
