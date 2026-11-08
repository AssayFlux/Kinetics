package org.assayflux.kinetics

import java.time.Instant
import java.time.format.DateTimeFormatter

/**
 * Human-readable, portable summary of the import record.
 * Intentionally contains no source URI, private storage path, or input contents.
 */
data class ImportProvenanceSummary(
    val jobId: String,
    val inputName: String,
    val state: String,
    val inputSha256: String?,
    val byteCount: Long?,
    val jobCreatedAtEpochMs: Long,
    val jobUpdatedAtEpochMs: Long,
    val toolId: String,
    val toolVersion: String,
    val parametersJson: String,
    val recordedAtEpochMs: Long,
)

object ImportProvenanceSummaryFormatter {
    fun render(record: ImportProvenanceSummary): String = buildString {
        appendLine("KINETICS — IMPORT PROVENANCE SUMMARY")
        appendLine("Schema: org.assayflux.kinetics.provenance-summary")
        appendLine("Schema version: 1")
        appendLine()
        appendLine("JOB")
        appendLine("ID: ${record.jobId}")
        appendLine("Input name: ${singleLine(record.inputName)}")
        appendLine("State: ${record.state}")
        appendLine("Input bytes: ${record.byteCount?.toString() ?: "not recorded"}")
        appendLine("Input SHA-256: ${record.inputSha256 ?: "not recorded"}")
        appendLine("Created (UTC): ${timestamp(record.jobCreatedAtEpochMs)}")
        appendLine("Updated (UTC): ${timestamp(record.jobUpdatedAtEpochMs)}")
        appendLine()
        appendLine("IMPORT TOOL")
        appendLine("Tool ID: ${record.toolId}")
        appendLine("Tool version: ${record.toolVersion}")
        appendLine("Recorded (UTC): ${timestamp(record.recordedAtEpochMs)}")
        appendLine("Parameters (JSON):")
        appendLine(record.parametersJson)
        appendLine()
        appendLine("SCOPE AND LIMITATIONS")
        appendLine("This document describes file import, encryption-at-rest and input hashing only.")
        appendLine("It is not a scientific analysis result, validation report or clinical interpretation.")
        appendLine("Source document URI, private storage path and input contents are intentionally excluded.")
    }

    private fun timestamp(epochMillis: Long): String =
        DateTimeFormatter.ISO_INSTANT.format(Instant.ofEpochMilli(epochMillis))

    private fun singleLine(value: String): String =
        value.replace(Regex("[\\r\\n\\t\\u0000-\\u001F\\u007F]"), " ")
}
