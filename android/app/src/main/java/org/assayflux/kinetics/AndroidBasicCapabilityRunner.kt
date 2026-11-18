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
        "genome.orf_candidate_scan",
        "kinetics.michaelis_menten",
        "phylo.newick",
        "sequence.global_alignment",
        "genome.contig_assembly_qc",
        "structure.sasa",
        "structure.interaction_candidates",
        "microbiome.diversity",
        "omics.logistic_growth",
        "sequence.explicit_genetic_code_translation",
        "kinetics.inhibition_rate",
        "phylo.upgma",
        "omics.normalisation",
        "omics.cross_correlation",
        "phylo.jukes_cantor_nj",
        "genome.gff3_annotation_import",
        "genome.gff3_transcript_cds_reconstruction",
    )

    fun analyze(context: Context, capabilityId: String, sequenceText: String): String {
        require(capabilityId in supported) { "Unsupported Android capability: $capabilityId" }
        require(sequenceText.isNotBlank()) { "Sequence input must not be blank" }
        require(sequenceText.length <= MAX_INPUT_CHARS) {
            "Sequence input exceeds the 1,000,000-character mobile limit"
        }
        if (!Python.isStarted()) Python.start(AndroidPlatform(context.applicationContext))
        return Python.getInstance().getModule("kinetics_probe")
            .callAttr("run_android_basic_capability", capabilityId, sequenceText)
            .toString()
    }
}
