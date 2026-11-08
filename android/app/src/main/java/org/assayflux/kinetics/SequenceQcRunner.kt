package org.assayflux.kinetics

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import org.json.JSONObject

internal data class SequenceQcRecord(
    val identifier: String,
    val length: Int,
    val gcPercent: Double,
    val ambiguousCount: Int,
)

internal data class SequenceQcResult(
    val recordCount: Int,
    val totalBases: Int,
    val records: List<SequenceQcRecord>,
)

internal object SequenceQcRunner {
    const val MAX_INPUT_CHARS = 1_000_000

    fun analyze(context: Context, fastaText: String): SequenceQcResult {
        require(fastaText.isNotBlank()) { "Enter FASTA records before analysis." }
        require(fastaText.length <= MAX_INPUT_CHARS) {
            "FASTA input exceeds the 1,000,000-character limit."
        }
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(context.applicationContext))
        }
        val json = Python.getInstance()
            .getModule("kinetics_probe")
            .callAttr("analyze_fasta", fastaText)
            .toString()
        val root = JSONObject(json)
        val recordsJson = root.getJSONArray("records")
        val records = (0 until recordsJson.length()).map { index ->
            val item = recordsJson.getJSONObject(index)
            SequenceQcRecord(
                identifier = item.getString("identifier"),
                length = item.getInt("length"),
                gcPercent = item.getDouble("gc_percent"),
                ambiguousCount = item.getInt("ambiguous_count"),
            )
        }
        return SequenceQcResult(
            recordCount = root.getInt("record_count"),
            totalBases = root.getInt("total_bases"),
            records = records,
        )
    }
}
