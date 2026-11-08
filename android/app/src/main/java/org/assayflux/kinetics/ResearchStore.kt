package org.assayflux.kinetics

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.io.File
import java.util.UUID

data class ResearchJob(
    val id: String,
    val inputName: String,
    val state: String,
    val sha256: String?,
    val message: String?,
)

data class RecoverableImport(val id: String, val uri: String)


class ResearchStore(context: Context) :
    SQLiteOpenHelper(context, "kinetics-research.db", null, DATABASE_VERSION) {

    private val appContext = context.applicationContext

    init {
        cleanupStalePlaintextCache()
    }

    /**
     * Recover plaintext analysis temporaries left by abrupt process death.
     * Only this app's uniquely-prefixed cache files older than 24 hours are eligible.
     */
    private fun cleanupStalePlaintextCache() {
        val cutoff = System.currentTimeMillis() - PLAINTEXT_CACHE_MAX_AGE_MS
        appContext.cacheDir.listFiles()
            ?.filter { file ->
                file.isFile && file.name.startsWith(PLAINTEXT_CACHE_PREFIX) &&
                    file.lastModified() > 0L && file.lastModified() < cutoff
            }
            ?.forEach { it.delete() }
    }

    override fun onConfigure(db: SQLiteDatabase) {
        super.onConfigure(db)
        db.setForeignKeyConstraintsEnabled(true)
    }

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """CREATE TABLE jobs (
                id TEXT PRIMARY KEY NOT NULL, input_name TEXT NOT NULL, input_uri TEXT NOT NULL,
                state TEXT NOT NULL, sha256 TEXT, byte_count INTEGER, message TEXT,
                storage_path TEXT, exported_at INTEGER, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        db.execSQL(
            """CREATE TABLE provenance (
                job_id TEXT PRIMARY KEY NOT NULL REFERENCES jobs(id), tool_id TEXT NOT NULL,
                tool_version TEXT NOT NULL, input_sha256 TEXT NOT NULL,
                parameters_json TEXT NOT NULL, created_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        db.execSQL("CREATE INDEX jobs_created_at_idx ON jobs(created_at DESC)")
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        if (oldVersion < 2) {
            db.execSQL("ALTER TABLE jobs ADD COLUMN storage_path TEXT")
        }
        if (oldVersion < 3) {
            db.execSQL("ALTER TABLE jobs ADD COLUMN exported_at INTEGER")
            db.execSQL("CREATE INDEX IF NOT EXISTS provenance_created_at_idx ON provenance(created_at DESC)")
        }
    }

    fun createJob(id: String, name: String, uri: String) {
        val now = System.currentTimeMillis()
        val values = ContentValues().apply {
            put("id", id)
            put("input_name", name)
            put("input_uri", uri)
            put("state", "queued")
            put("created_at", now)
            put("updated_at", now)
        }
        writableDatabase.insertOrThrow("jobs", null, values)
    }

    fun updateJob(
        id: String, state: String, hash: String? = null,
        bytes: Long? = null, message: String? = null,
    ) {
        val values = ContentValues().apply {
            put("state", state)
            put("updated_at", System.currentTimeMillis())
            if (hash != null) put("sha256", hash)
            if (bytes != null) put("byte_count", bytes)
            if (message != null) put("message", message)
        }
        writableDatabase.update("jobs", values, "id=?", arrayOf(id))
    }

    /** Resolve only canonical finalized KDAT files inside the dedicated no-backup directory. */
    private fun resolveEncryptedInput(path: String): File {
        val root = File(appContext.noBackupFilesDir, "research-inputs").canonicalFile
        val candidate = File(path).canonicalFile
        require(candidate.parentFile == root && candidate.extension == "kdat") {
            "Encrypted input path is outside the dedicated app-private storage directory"
        }
        return candidate
    }

    /** Atomically records encrypted storage location, successful state and provenance. */
    fun completeImport(id: String, hash: String, bytes: Long, encryptedPath: String) {
        val verifiedPath = resolveEncryptedInput(encryptedPath)
        require(verifiedPath.isFile && verifiedPath.length() > LocalCrypto.HEADER_BYTES) {
            "Final encrypted input file is missing or empty"
        }
        val db = writableDatabase
        db.beginTransaction()
        try {
            val values = ContentValues().apply {
                put("state", "succeeded")
                put("sha256", hash)
                put("byte_count", bytes)
                put("storage_path", encryptedPath)
                put("message", "Imported, encrypted at rest and SHA-256 recorded")
                put("updated_at", System.currentTimeMillis())
            }
            check(db.update("jobs", values, "id=?", arrayOf(id)) == 1) {
                "Import job disappeared before finalization"
            }
            val provenance = ContentValues().apply {
                put("job_id", id)
                put("tool_id", "file-import-encrypt-sha256")
                put("tool_version", "3")
                put("input_sha256", hash)
                put("parameters_json", """{"encryption":"AES-256-GCM","format":"chunked-v2","aad":"job-id+chunk-index","storage":"app-private-no-backup"}""")
                put("created_at", System.currentTimeMillis())
            }
            db.insertWithOnConflict(
                "provenance", null, provenance, SQLiteDatabase.CONFLICT_REPLACE,
            )
            db.setTransactionSuccessful()
        } finally {
            db.endTransaction()
        }
    }

    fun storedInputPath(id: String): String? {
        readableDatabase.rawQuery(
            "SELECT storage_path FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            return if (cursor.moveToFirst() && !cursor.isNull(0)) cursor.getString(0) else null
        }
    }

    /** Materialize an authenticated temporary plaintext copy for a caller-controlled analysis/export. */
    fun materializeStoredInput(id: String, destination: File): Boolean {
        val safeRoot = appContext.cacheDir.canonicalFile.toPath()
        val safeDestination = destination.canonicalFile.toPath()
        require(safeDestination.startsWith(safeRoot) && safeDestination != safeRoot) {
            "Decrypted research inputs may only be materialized inside the app-private cache"
        }
        val stored = readableDatabase.rawQuery(
            "SELECT storage_path,sha256 FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst() || cursor.isNull(0) || cursor.isNull(1)) null
            else Pair(cursor.getString(0), cursor.getString(1))
        } ?: return false
        LocalCrypto.decryptChunkedFile(
            resolveEncryptedInput(stored.first), destination, "kinetics-import:$id", stored.second,
        )
        return true
    }

    /** Stream an authenticated, hash-verified input to a caller-selected SAF output stream. */
    fun exportStoredInput(id: String, destination: java.io.OutputStream): Boolean {
        val stored = readableDatabase.rawQuery(
            "SELECT storage_path,sha256 FROM jobs WHERE id=? AND state='succeeded'",
            arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst() || cursor.isNull(0) || cursor.isNull(1)) null
            else Pair(cursor.getString(0), cursor.getString(1))
        } ?: return false
        LocalCrypto.decryptChunkedFileToStream(
            resolveEncryptedInput(stored.first), destination, "kinetics-import:$id", stored.second,
        )
        val exported = ContentValues().apply {
            put("exported_at", System.currentTimeMillis())
            put("updated_at", System.currentTimeMillis())
        }
        check(writableDatabase.update("jobs", exported, "id=?", arrayOf(id)) == 1) {
            "Exported job metadata disappeared"
        }
        return true
    }

    /** Run a local analysis callback and always remove its plaintext cache file. */
    fun <T> withStoredInput(id: String, action: (File) -> T): T? {
        val temporary = File(appContext.cacheDir, "kinetics-analysis-" + UUID.randomUUID() + ".tmp")
        if (!materializeStoredInput(id, temporary)) return null
        return try {
            action(temporary)
        } finally {
            temporary.delete()
        }
    }

    fun updateProgress(id: String, bytes: Long) {
        val values = ContentValues().apply {
            put("byte_count", bytes)
            put("updated_at", System.currentTimeMillis())
        }
        writableDatabase.update("jobs", values, "id=?", arrayOf(id))
    }

    fun progress(id: String): Long {
        readableDatabase.rawQuery(
            "SELECT byte_count FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            return if (cursor.moveToFirst() && !cursor.isNull(0)) cursor.getLong(0) else 0L
        }
    }

    fun inputUri(id: String): String? {
        readableDatabase.rawQuery(
            "SELECT input_uri FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            return if (cursor.moveToFirst()) cursor.getString(0) else null
        }
    }

    /** Imports left queued/running by process death; unique WorkManager names make re-enqueue idempotent. */
    fun recoverableImports(): List<RecoverableImport> {
        val result = mutableListOf<RecoverableImport>()
        readableDatabase.rawQuery(
            "SELECT id,input_uri FROM jobs WHERE state IN ('queued','running') ORDER BY created_at",
            emptyArray(),
        ).use { cursor ->
            while (cursor.moveToNext()) {
                result += RecoverableImport(cursor.getString(0), cursor.getString(1))
            }
        }
        return result
    }

    /** Delete local encrypted input, partial staging and associated SQLite metadata (not secure erase). */
    fun deleteStoredJob(id: String): Boolean {
        require(id.matches(Regex("[A-Za-z0-9_-]{1,80}"))) { "Invalid research job identifier" }
        val storedPath = readableDatabase.rawQuery(
            "SELECT storage_path FROM jobs WHERE id=?", arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst()) return false
            if (cursor.isNull(0)) null else cursor.getString(0)
        }
        val encrypted = storedPath?.let(::resolveEncryptedInput)
        val stagingRoot = File(appContext.noBackupFilesDir, "research-imports").canonicalFile
        val partial = File(stagingRoot, "$id.encpart").canonicalFile
        require(partial.parentFile == stagingRoot) { "Invalid encrypted staging path" }
        if (encrypted != null && encrypted.exists() && !encrypted.delete()) {
            throw IllegalStateException("Encrypted input could not be deleted")
        }
        if (partial.exists() && !partial.delete()) {
            throw IllegalStateException("Encrypted partial input could not be deleted")
        }
        val db = writableDatabase
        db.beginTransaction()
        try {
            db.delete("provenance", "job_id=?", arrayOf(id))
            check(db.delete("jobs", "id=?", arrayOf(id)) == 1) {
                "Research job metadata disappeared during deletion"
            }
            db.setTransactionSuccessful()
        } finally {
            db.endTransaction()
        }
        return true
    }

    fun recentJobs(limit: Int = 30): List<ResearchJob> {
        val result = mutableListOf<ResearchJob>()
        readableDatabase.rawQuery(
            "SELECT id,input_name,state,sha256,message FROM jobs ORDER BY created_at DESC LIMIT ?",
            arrayOf(limit.coerceIn(1, 100).toString()),
        ).use { cursor ->
            while (cursor.moveToNext()) {
                result += ResearchJob(
                    cursor.getString(0), cursor.getString(1), cursor.getString(2),
                    if (cursor.isNull(3)) null else cursor.getString(3),
                    if (cursor.isNull(4)) null else cursor.getString(4),
                )
            }
        }
        return result
    }

    companion object {
        private const val DATABASE_VERSION = 3
        private const val PLAINTEXT_CACHE_PREFIX = "kinetics-analysis-"
        private const val PLAINTEXT_CACHE_MAX_AGE_MS = 24L * 60L * 60L * 1000L
    }
}
