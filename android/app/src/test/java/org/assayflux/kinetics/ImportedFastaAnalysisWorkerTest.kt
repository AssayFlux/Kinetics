package org.assayflux.kinetics

import androidx.work.ListenableWorker
import androidx.work.testing.TestListenableWorkerBuilder
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35])
class ImportedFastaAnalysisWorkerTest {
    private val context = RuntimeEnvironment.getApplication()

    @Test
    fun missingJobIdFailsClosed() {
        val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context).build()

        assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun malformedJobIdFailsClosedBeforeStoreAccess() {
        val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
            .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "../escape"))
            .build()

        assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun unknownJobFailsWithoutStartingScientificRuntime() {
        val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
            .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "missing-job"))
            .build()

        assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
    }

    @Test
    fun oversizedCommittedInputIsRejectedBeforePlaintextMaterialization() {
        val store = ResearchStore(context)
        try {
            store.createJob("oversized-1", "large.fa", "content://large")
            store.updateJob(
                "oversized-1",
                "succeeded",
                hash = "a".repeat(64),
                bytes = 1_000_001L,
            )
            val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
                .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "oversized-1"))
                .build()

            assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
            val saved = store.recentJobs().single { it.id == "oversized-1" }
            assertTrue(saved.state == "succeeded")
            assertTrue(saved.message.orEmpty().contains("1,000,000-byte analysis limit"))
        } finally {
            store.close()
            context.deleteDatabase("kinetics-research.db")
        }
    }

    @Test
    fun fastqIsRejectedUntilPhredOffsetIsExplicit() {
        val store = ResearchStore(context)
        try {
            store.createJob("fastq-1", "reads.fastq", "content://reads")
            store.updateJob(
                "fastq-1",
                "succeeded",
                hash = "b".repeat(64),
                bytes = 128L,
            )
            val worker = TestListenableWorkerBuilder<ImportedFastaAnalysisWorker>(context)
                .setInputData(androidx.work.workDataOf(ImportedFastaAnalysisWorker.KEY_JOB_ID to "fastq-1"))
                .build()

            assertTrue(worker.doWork() is ListenableWorker.Result.Failure)
            val saved = store.recentJobs().single { it.id == "fastq-1" }
            assertTrue(saved.message.orEmpty().contains("FASTQ requires an explicit Phred offset"))
        } finally {
            store.close()
            context.deleteDatabase("kinetics-research.db")
        }
    }
}
