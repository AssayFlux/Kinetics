package org.assayflux.kinetics

import android.content.Context
import android.net.Uri
import androidx.work.Worker
import androidx.work.WorkerParameters
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.security.MessageDigest

/**
 * Streams a user-selected document into app-private, no-backup storage.
 * A resumed import verifies that the source prefix still matches the retained
 * partial file before appending, preventing a mixed-version input hash.
 */
class ImportWorker(context: Context, parameters: WorkerParameters) : Worker(context, parameters) {
    override fun doWork(): Result {
        val jobId = inputData.getString(KEY_JOB_ID) ?: return Result.failure()
        if (!jobId.matches(Regex("[A-Za-z0-9_-]{1,80}"))) return Result.failure()
        val uri = Uri.parse(inputData.getString(KEY_URI) ?: return Result.failure())
        val store = ResearchStore(applicationContext)
        val importDirectory = File(applicationContext.noBackupFilesDir, "research-imports")
            .apply { mkdirs() }
        val partial = File(importDirectory, "$jobId.part")
        store.updateJob(jobId, "running")

        var byteCount = 0L
        return try {
            val digest = MessageDigest.getInstance("SHA-256")
            val partialPrefixDigest = MessageDigest.getInstance("SHA-256")

            if (partial.exists()) {
                FileInputStream(partial).use { input ->
                    val buffer = ByteArray(DEFAULT_BUFFER_SIZE)
                    while (true) {
                        if (isStopped) return markCancelled(store, jobId, partial, byteCount)
                        val count = input.read(buffer)
                        if (count < 0) break
                        byteCount += count
                        if (byteCount > MAX_IMPORT_BYTES) {
                            throw IllegalArgumentException("Partial input exceeds the 512 MiB import limit")
                        }
                        digest.update(buffer, 0, count)
                        partialPrefixDigest.update(buffer, 0, count)
                    }
                }
            }

            val source = applicationContext.contentResolver.openInputStream(uri)
                ?: throw IllegalStateException("Selected document could not be opened")
            source.use { input ->
                val sourcePrefixDigest = MessageDigest.getInstance("SHA-256")
                var verifiedBytes = 0L
                val buffer = ByteArray(DEFAULT_BUFFER_SIZE)

                // Re-read and hash the source prefix rather than trusting skip(), so a
                // changed document cannot silently be appended to an old partial file.
                while (verifiedBytes < byteCount) {
                    if (isStopped) return markCancelled(store, jobId, partial, byteCount)
                    val wanted = minOf(buffer.size.toLong(), byteCount - verifiedBytes).toInt()
                    val count = input.read(buffer, 0, wanted)
                    if (count < 0) {
                        throw IllegalStateException("Source became shorter during resume")
                    }
                    sourcePrefixDigest.update(buffer, 0, count)
                    verifiedBytes += count
                }

                if (!MessageDigest.isEqual(partialPrefixDigest.digest(), sourcePrefixDigest.digest())) {
                    throw IllegalStateException("Source content changed since the partial import; restart required")
                }

                FileOutputStream(partial, true).use { output ->
                    var sinceSync = 0L
                    while (true) {
                        if (isStopped) {
                            output.flush()
                            output.fd.sync()
                            return markCancelled(store, jobId, partial, byteCount)
                        }
                        val count = input.read(buffer)
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
            store.updateJob(
                jobId, "succeeded", hash, byteCount,
                "Imported and hashed; no scientific analysis performed",
            )
            store.recordProvenance(jobId, hash)
            check(partial.delete()) { "Imported file could not be finalized/removed from staging" }
            Result.success()
        } catch (error: Exception) {
            store.updateJob(
                jobId, "failed", bytes = partial.length().coerceAtLeast(byteCount),
                message = error.message ?: error.javaClass.simpleName,
            )
            Result.failure()
        }
    }

    private fun markCancelled(
        store: ResearchStore,
        jobId: String,
        partial: File,
        byteCount: Long,
    ): Result {
        store.updateProgress(jobId, partial.length().coerceAtLeast(byteCount))
        store.updateJob(
            jobId, "cancelled", bytes = partial.length().coerceAtLeast(byteCount),
            message = "Partial import retained in app-private no-backup storage; resume is available",
        )
        return Result.failure()
    }

    companion object {
        const val KEY_JOB_ID = "job_id"
        const val KEY_URI = "input_uri"
        const val MAX_IMPORT_BYTES = 512L * 1024L * 1024L
        const val CHECKPOINT_BYTES = 4L * 1024L * 1024L
    }
}
