package org.assayflux.kinetics

import android.content.ContentValues
import android.database.sqlite.SQLiteDatabase
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35])
class ResearchStoreMigrationTest {
    private val context = RuntimeEnvironment.getApplication()

    @After
    fun cleanDatabase() {
        context.deleteDatabase("kinetics-research.db")
    }

    @Test
    fun freshInstallCreatesVersionFourSchemaAndCascadeForeignKey() {
        val store = ResearchStore(context)
        val db = store.writableDatabase

        assertEquals(4, db.version)
        assertTrue(tableExists(db, "analysis_results"))
        assertTrue(columnExists(db, "analysis_results", "input_sha256"))
        assertTrue(columnExists(db, "analysis_results", "result_json"))
        assertEquals("CASCADE", foreignKeyDeleteAction(db, "analysis_results", "jobs"))
        store.close()
    }

    @Test
    fun versionThreeDatabaseMigratesToVersionFourWithoutLosingJobs() {
        val legacy = context.openOrCreateDatabase("kinetics-research.db", 0, null)
        legacy.execSQL(
            """CREATE TABLE jobs (
                id TEXT PRIMARY KEY NOT NULL, input_name TEXT NOT NULL, input_uri TEXT NOT NULL,
                state TEXT NOT NULL, sha256 TEXT, byte_count INTEGER, message TEXT,
                storage_path TEXT, exported_at INTEGER, created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        legacy.execSQL(
            """CREATE TABLE provenance (
                job_id TEXT PRIMARY KEY NOT NULL REFERENCES jobs(id), tool_id TEXT NOT NULL,
                tool_version TEXT NOT NULL, input_sha256 TEXT NOT NULL,
                parameters_json TEXT NOT NULL, created_at INTEGER NOT NULL
            )""".trimIndent(),
        )
        legacy.execSQL("CREATE INDEX jobs_created_at_idx ON jobs(created_at DESC)")
        legacy.execSQL("CREATE INDEX provenance_created_at_idx ON provenance(created_at DESC)")
        legacy.execSQL(
            "INSERT INTO jobs(id,input_name,input_uri,state,created_at,updated_at) VALUES('legacy-1','x.fa','content://legacy','succeeded',1,1)",
        )
        legacy.version = 3
        legacy.close()

        val store = ResearchStore(context)
        val db = store.writableDatabase

        assertEquals(4, db.version)
        assertTrue(tableExists(db, "analysis_results"))
        db.rawQuery("SELECT input_name FROM jobs WHERE id='legacy-1'", null).use { cursor ->
            assertTrue(cursor.moveToFirst())
            assertEquals("x.fa", cursor.getString(0))
        }
        store.close()
    }

    @Test
    fun analysisResultIsDigestBoundAndExportStopsWhenJobDigestChanges() {
        val store = ResearchStore(context)
        store.createJob("job-1", "sample.fa", "content://sample")
        val digest = "a".repeat(64)
        store.updateJob("job-1", "succeeded", hash = digest, bytes = 12)
        store.saveAnalysisResult(
            id = "job-1",
            toolId = "sequence.fasta.qc",
            toolVersion = "1",
            parametersJson = """{"max_bytes":1048576}""",
            resultJson = """{"record_count":1,"records":[{"length":12}]}""",
        )

        assertNotNull(store.analysisResultJson("job-1"))
        assertNotNull(store.analysisExportJson("job-1"))

        store.updateJob("job-1", "succeeded", hash = "b".repeat(64))
        assertNull(store.analysisExportJson("job-1"))
        store.close()
    }

    @Test
    fun analysisCannotBeSavedForIncompleteOrMalformedImportDigest() {
        val store = ResearchStore(context)
        store.createJob("job-2", "sample.fa", "content://sample")
        store.updateJob("job-2", "queued", hash = "a".repeat(64))
        val notSucceeded = runCatching {
            store.saveAnalysisResult("job-2", "tool", "1", "{}", """{"ok":true}""")
        }.exceptionOrNull()
        assertNotNull(notSucceeded)

        store.updateJob("job-2", "succeeded", hash = "not-a-sha256")
        val malformed = runCatching {
            store.saveAnalysisResult("job-2", "tool", "1", "{}", """{"ok":true}""")
        }.exceptionOrNull()
        assertNotNull(malformed)
        store.close()
    }

    @Test
    fun deletingJobRemovesItsAnalysisResult() {
        val store = ResearchStore(context)
        store.createJob("job-3", "sample.fa", "content://sample")
        store.updateJob("job-3", "succeeded", hash = "c".repeat(64), bytes = 1)
        store.saveAnalysisResult("job-3", "tool", "1", "{}", """{"ok":true}""")

        assertTrue(store.deleteStoredJob("job-3"))
        assertNull(store.analysisResultJson("job-3"))
        assertFalse(store.deleteStoredJob("job-3"))
        store.close()
    }

    private fun tableExists(db: SQLiteDatabase, name: String): Boolean =
        db.rawQuery(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
            arrayOf(name),
        ).use { it.moveToFirst() }

    private fun columnExists(db: SQLiteDatabase, table: String, column: String): Boolean =
        db.rawQuery("PRAGMA table_info($table)", null).use { cursor ->
            val nameIndex = cursor.getColumnIndexOrThrow("name")
            generateSequence { if (cursor.moveToNext()) cursor.getString(nameIndex) else null }
                .any { it == column }
        }

    private fun foreignKeyDeleteAction(db: SQLiteDatabase, table: String, parent: String): String? =
        db.rawQuery("PRAGMA foreign_key_list($table)", null).use { cursor ->
            val tableIndex = cursor.getColumnIndexOrThrow("table")
            val actionIndex = cursor.getColumnIndexOrThrow("on_delete")
            while (cursor.moveToNext()) {
                if (cursor.getString(tableIndex) == parent) return@use cursor.getString(actionIndex)
            }
            null
        }
}
