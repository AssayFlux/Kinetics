package org.assayflux.kinetics

import android.content.Context
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

/** Explicitly allow-listed local bridges for simple sequence/protein research tools. */
internal object AndroidBasicCapabilityRunner {
    const val MAX_INPUT_CHARS = 1_000_000

    private val supported = setOf(
        "protein.descriptors",
        "molecular.primer_screen",
        "molecular.crispr_pam",
    )

    fun analyze(context: Context, capabilityId: String, sequenceText: String): String {
        require(capabilityId in supported) { "Unsupported Android capability: $capabilityId" }
        require(sequenceText.isNotBlank()) { "Sequence input must not be blank" }
        require(sequenceText.length <= MAX_INPUT_CHARS) {
            "Sequence input exceeds the 1,000,000-character mobile limit"
        }
        if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
        return Python.getInstance().getModule("kinetics_probe")
            .callAttr("run_basic_sequence_capability", capabilityId, sequenceText)
            .toString()
    }
}
