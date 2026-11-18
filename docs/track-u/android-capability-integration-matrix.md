# Android capability integration matrix

**Baseline commit:** `520d3b5777294871645a88f1566341ac8b1d1747`  
**Branch:** `main`  
**Purpose:** Separate Python source registration from an actual Android-executable workflow.  
**Evidence boundary:** A connected route means the Android UI invokes a bounded Chaquopy bridge. It does not mean the scientific method has been independently validated, clinically approved, or device-accepted.

## Summary

- Catalogue entries: **68**
- Catalogue entries connected to Android workflows: **26**
- Catalogue entries not yet connected to Android: **42**
- Additional Android service outside the JSON catalogue: `public.reference_databases` (NCBI/UniProt/RCSB retrieval).

The Android UI must never display catalogue `status: implemented` as proof of Android integration. The service page separately reports whether an Android workflow is connected.

## Connected Android workflows

| Capability ID | Android entry |
|---|---|
| `public.reference_databases` | Public database retrieval card; NCBI Gene/sequence, UniProt FASTA, RCSB mmCIF |
| `sequence.fasta` | FASTA QC card |
| `sequence.fastq` | FASTQ QC card |
| `sequence.genetic_code_candidate_inference` | Genetic-code candidate inference card |
| `protein.descriptors` | Protein descriptors form |
| `molecular.primer_screen` | Primer property screen form |
| `molecular.crispr_pam` | SpCas9 NGG PAM scan form |
| `genome.orf_candidate_scan` | Six-frame ORF candidate scan form |
| `kinetics.michaelis_menten` | Michaelis–Menten rate calculator |
| `phylo.newick` | Newick parser |
| `structure.ligand_site_candidates` | Ligand-site candidate analysis |
| `structure.apo_pocket_candidates` | Apo-pocket candidate analysis |
| `chemistry.sdf_graph` | SDF graph preview |
| `genomics.sam_vcf` | Aggregate-only VCF QC and research gate |

| `sequence.global_alignment` | Global pairwise alignment form (two sequences, bounded Needleman–Wunsch) |
| `genome.contig_assembly_qc` | Contig assembly statistics from FASTA |
| `structure.sasa` | PDB-based approximate Shrake–Rupley SASA |
| `structure.interaction_candidates` | PDB distance-only interaction candidate screen |
| `microbiome.diversity` | Shannon and Gini–Simpson count-vector calculator |
| `omics.logistic_growth` | JSON-parameterized logistic growth model |

| `sequence.explicit_genetic_code_translation` | Explicit NCBI genetic-code translation with caller-supplied table/frame/CDS mode |
| `kinetics.inhibition_rate` | Competitive, uncompetitive, noncompetitive and mixed inhibition equation calculator |
| `phylo.upgma` | Rooted UPGMA construction from supplied distance matrix |

| `omics.normalisation` | CPM or CLR transformation for bounded feature-by-sample matrices |
| `omics.cross_correlation` | Pairwise Pearson correlation between matched multi-omics matrices |
| `phylo.jukes_cantor_nj` | Neighbour joining from supplied aligned sequences using Jukes–Cantor distances |

| `genome.gff3_annotation_import` | GFF3 structural validation and feature/parent graph checks |
| `genome.gff3_transcript_cds_reconstruction` | CDS reconstruction from validated GFF3 and caller-supplied contigs |

All local forms use an explicit bridge allow-list and bounded input/work limits. Their method-specific limitations are returned or displayed with results.

## Complete catalogue mapping

| Capability ID | Python source | Android integration |
|---|---|---|
| `sequence.fasta` | `python/kinetics/sequence.py` | Connected — local Android form + Python bridge |
| `sequence.exact_reference_search` | `python/kinetics/sequence_reference.py` | Not connected — Python source only |
| `sequence.local_reference_pack_loader` | `python/kinetics/sequence_pack.py` | Not connected — Python source only |
| `sequence.local_fasta_exact_search` | `python/kinetics/sequence_pack.py` | Not connected — Python source only |
| `sequence.explicit_genetic_code_translation` | `python/kinetics/genetic_code.py` | Connected — local Android form + Python bridge |
| `sequence.genetic_code_candidate_inference` | `python/kinetics/genetic_code_inference.py` | Connected — local Android form + Python bridge |
| `genome.orf_candidate_scan` | `python/kinetics/orf.py` | Connected — local Android form + Python bridge |
| `genome.prokaryotic_orf_candidate_scan` | `python/kinetics/genome_orf.py` | Not connected — Python source only |
| `sequence.local_blastp` | `python/kinetics/blastp.py` | Not connected — Python source only |
| `sequence.local_hmmpress` | `python/kinetics/hmmer_runner.py` | Not connected — Python source only |
| `sequence.local_hmmscan` | `python/kinetics/hmmer_runner.py` | Not connected — Python source only |
| `protein.hmmscan_domain_evidence` | `python/kinetics/hmmer.py` | Not connected — Python source only |
| `sequence.fastq` | `python/kinetics/sequence.py` | Connected — local Android form + Python bridge |
| `sequence.global_alignment` | `python/kinetics/sequence.py` | Connected — local Android form + Python bridge |
| `genomics.sam_vcf` | `python/kinetics/genomics.py` | Connected — local Android form + Python bridge |
| `variant.reference_checked_normalization` | `python/kinetics/variant_reference.py` | Not connected — Python source only |
| `protein.descriptors` | `python/kinetics/protein.py` | Connected — local Android form + Python bridge |
| `kinetics.michaelis_menten` | `python/kinetics/kinetics.py` | Connected — local Android form + Python bridge |
| `structure.pdb_geometry` | `python/kinetics/structure.py` | Not connected — Python source only |
| `chemistry.sdf_graph` | `python/kinetics/chemistry.py` | Connected — local Android form + Python bridge |
| `phylo.newick` | `python/kinetics/phylo.py` | Connected — local Android form + Python bridge |
| `omics.normalisation` | `python/kinetics/omics.py` | Connected — local Android form + Python bridge |
| `microbiome.diversity` | `python/kinetics/omics.py` | Connected — local Android form + Python bridge |
| `genes.ncbi_catalogue` | `python/kinetics/catalog.py` | Not connected — Python source only |
| `molecular.primer_screen` | `python/kinetics/molecular.py` | Connected — local Android form + Python bridge |
| `molecular.crispr_pam` | `python/kinetics/molecular.py` | Connected — local Android form + Python bridge |
| `phylo.upgma` | `python/kinetics/phylo.py` | Connected — local Android form + Python bridge |
| `omics.logistic_growth` | `python/kinetics/omics.py` | Connected — local Android form + Python bridge |
| `omics.cross_correlation` | `python/kinetics/omics.py` | Connected — local Android form + Python bridge |
| `genomics.variant_normalization` | `python/kinetics/genomics.py` | Not connected — Python source only |
| `kinetics.bootstrap_intervals` | `python/kinetics/kinetics.py` | Not connected — Python source only |
| `structure.sasa` | `python/kinetics/structure.py` | Connected — local Android form + Python bridge |
| `phylo.newick_export` | `python/kinetics/phylo.py` | Not connected — Python source only |
| `omics.nb2_glm` | `python/kinetics/omics.py` | Not connected — Python source only |
| `genomics.bam_core` | `python/kinetics/genomics.py` | Not connected — Python source only |
| `pgx.star_allele_definitions` | `python/kinetics/pgx.py` | Not connected — Python source only |
| `phylo.jukes_cantor_nj` | `python/kinetics/phylo.py` | Connected — local Android form + Python bridge |
| `structure.interaction_candidates` | `python/kinetics/structure.py` | Connected — local Android form + Python bridge |
| `chemistry.rdkit_adapter` | `python/kinetics/chemistry_rdkit.py` | Not connected — Python source only |
| `genomics.htslib_bam_cram` | `python/kinetics/genomics_htslib.py` | Not connected — Python source only |
| `pgx.pharmvar_tsv` | `python/kinetics/pharmvar.py` | Not connected — Python source only |
| `phylo.nj_site_bootstrap` | `python/kinetics/phylo.py` | Not connected — Python source only |
| `structure.viewer_payload` | `python/kinetics/structure_view.py` | Not connected — Python source only |
| `structure.session_export` | `python/kinetics/structure_view.py` | Not connected — Python source only |
| `structure.exact_sequence_mapping` | `python/kinetics/sequence_structure.py` | Not connected — Python source only |
| `structure.geometry_screen_metrics` | `python/kinetics/structure_quality.py` | Not connected — Python source only |
| `structure.variant_coordinate_mapping` | `python/kinetics/sequence_structure.py` | Not connected — Python source only |
| `structure.chain_interface_contacts` | `python/kinetics/sequence_structure.py` | Not connected — Python source only |
| `structure.ligand_site_candidates` | `python/kinetics/structure_pockets.py` | Connected — local Android form + Python bridge |
| `structure.apo_pocket_candidates` | `python/kinetics/apo_pockets.py` | Connected — local Android form + Python bridge |
| `genes.catalogue_coverage_report` | `python/kinetics/catalog.py` | Not connected — Python source only |
| `structure.prediction_envelope_validation` | `python/kinetics/structure_prediction.py` | Not connected — Python source only |
| `structure.experimental_ca_comparison` | `python/kinetics/structure_prediction.py` | Not connected — Python source only |
| `genome.contig_assembly_qc` | `python/kinetics/genome_qc.py` | Connected — local Android form + Python bridge |
| `protein.fixed_width_motif_scan` | `python/kinetics/protein_motifs.py` | Not connected — Python source only |
| `protein.design_brief_validation` | `python/kinetics/protein_design.py` | Not connected — Python source only |
| `structure.alignment_coordinate_mapping` | `python/kinetics/structure_alignment.py` | Not connected — Python source only |
| `sequence.local_alignment_reference_search` | `python/kinetics/sequence_reference.py` | Not connected — Python source only |
| `genome.gff3_annotation_import` | `python/kinetics/gff3.py` | Connected — local Android form + Python bridge |
| `sequence.local_fasta_alignment_search` | `python/kinetics/sequence_pack.py` | Not connected — Python source only |
| `genome.gff3_transcript_cds_reconstruction` | `python/kinetics/gff3_transcripts.py` | Connected — local Android form + Python bridge |
| `protein.hmmer_domain_candidate_ranking` | `python/kinetics/hmmer_rank.py` | Not connected — Python source only |
| `protein.hmmscan_domtblout_evidence` | `python/kinetics/hmmer.py` | Not connected — Python source only |
| `structure.pinned_local_prediction_process` | `python/kinetics/s4_process.py` | Not connected — Python source only |
| `genome.augustus_local_gene_candidates` | `python/kinetics/augustus.py` | Not connected — Python source only |
| `genome.prodigal_local_gene_candidates` | `python/kinetics/prodigal.py` | Not connected — Python source only |
| `genome.pinned_local_gff3_annotator` | `python/kinetics/genome_annotation.py` | Not connected — Python source only |
| `structure.local_prediction_engine_adapter` | `python/kinetics/s4_engine.py` | Not connected — Python source only |

## Remaining engineering work

1. Add typed Android forms and bridge methods for the remaining catalogue entries, grouping related tools into coherent service workspaces without hiding individual capability IDs.
2. Integrate optional dependencies (RDKit, HTSlib/pysam, HMMER, BLAST, Vina, OpenMM and structure-prediction adapters) only where Android-compatible packaging, ABI, licences, model provenance, storage and runtime limits are demonstrated. Host-only availability is not Android availability.
3. Add workflow-level cancellation, progress, lifecycle-safe execution, result persistence, provenance export and recovery for long-running workflows.
4. Add Android tests for every exposed capability: valid inputs, malformed inputs, upper bounds, cancellation, result schema and privacy boundaries.
5. Complete public-database retrieval lifecycle: retries/backoff, cancellation, cache quotas/eviction, provider terms/licence metadata, source release capture and background execution.
6. Decide and implement remote account authentication only after an identity provider/backend is selected. Current profile and biometric unlock remain device-local; no fake password reset or remote account ID.
7. Re-run exact-head CI after the final engineering changes. Physical-device, accessibility, scientific benchmark, independent review and clinical/ethics acceptance remain separate later gates.

## Change log

- `92824712238e7dd54ddcab5e5ab8e8552e1d0014`: added Android forms and Python bridge for protein descriptors, primer screening and SpCas9 NGG PAM scan.
- `520d3b5777294871645a88f1566341ac8b1d1747`: added Android forms and bounded bridge for ORF candidate scan, Michaelis–Menten rate calculation and Newick parsing.
