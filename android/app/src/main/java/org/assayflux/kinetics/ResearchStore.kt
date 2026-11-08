package org.assayflux.kinetics

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

data class ResearchJob(
    val id: String,
    val inputName: String,
    val state: String,
    val sha256: String?,
    val message: String?,
)

class ResearchStore(context: Context) :
    SQLiteOpenHelper(context, "kinetics-research.db", null, DATABASE_VERSION) {

    override fun onConfigure(db: SQLiteDatabase) {
        super.onConfigure(db)
        db.setForeignKeyConstraintsEnabled(true)
    }

    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(
            """CREATE TABLE jobs (
                id TEXT PRIMARY KEY NOT NULL, input_name TEXT NOT NULL, input_uri TEXT NOT NULL,
                state TEXT NOT NULL, sha256 TEXT, byte_count INTEGER, message TEXT,
                storage_path TEXT, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL
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

    /** Atomically records encrypted storage location, successful state and provenance. */
    fun completeImport(id: String, hash: String, bytes: Long, encryptedPath: String) {
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
                put("tool_version", "2")
                put("input_sha256", hash)
                put("parameters_json", """{"encryption":"AES-256-GCM","storage":"app-private-no-backup"}""")
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
        private const val DATABASE_VERSION = 2
    }
}
