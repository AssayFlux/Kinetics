-- Kinetics migration 002: domain-specific normalized scientific records.
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS entity_subtypes(
 entity_id INTEGER PRIMARY KEY REFERENCES entities(entity_id) ON DELETE CASCADE,
 domain TEXT NOT NULL,
 subtype TEXT NOT NULL,
 canonical_accession TEXT,
 source_id TEXT REFERENCES data_sources(source_id),
 UNIQUE(domain,subtype,canonical_accession)
);
CREATE INDEX IF NOT EXISTS idx_entity_subtypes_domain ON entity_subtypes(domain,subtype);

CREATE TABLE IF NOT EXISTS sequence_features(
 feature_id INTEGER PRIMARY KEY,
 sequence_entity_id INTEGER NOT NULL REFERENCES sequences(entity_id) ON DELETE CASCADE,
 feature_type TEXT NOT NULL,
 start_pos INTEGER NOT NULL CHECK(start_pos>=1),
 end_pos INTEGER NOT NULL CHECK(end_pos>=start_pos),
 strand INTEGER CHECK(strand IN(-1,1)),
 label TEXT,
 evidence_code TEXT,
 source_record_id INTEGER REFERENCES source_records(record_id)
);
CREATE INDEX IF NOT EXISTS idx_sequence_features_span ON sequence_features(sequence_entity_id,start_pos,end_pos);

CREATE TABLE IF NOT EXISTS genetic_variants(
 entity_id INTEGER PRIMARY KEY REFERENCES entities(entity_id) ON DELETE CASCADE,
 assembly TEXT,
 chromosome TEXT,
 start_pos INTEGER,
 end_pos INTEGER,
 reference_allele TEXT,
 alternate_allele TEXT,
 variant_class TEXT,
 clinical_significance TEXT,
 review_status TEXT,
 source_record_id INTEGER REFERENCES source_records(record_id)
);
CREATE INDEX IF NOT EXISTS idx_variants_locus ON genetic_variants(assembly,chromosome,start_pos);

CREATE TABLE IF NOT EXISTS expression_measurements(
 expression_id INTEGER PRIMARY KEY,
 gene_entity_id INTEGER REFERENCES entities(entity_id),
 transcript_entity_id INTEGER REFERENCES entities(entity_id),
 sample_entity_id INTEGER REFERENCES entities(entity_id),
 assay TEXT NOT NULL,
 value REAL,
 unit TEXT,
 normalized_value REAL,
 organism_entity_id INTEGER REFERENCES entities(entity_id),
 tissue_entity_id INTEGER REFERENCES entities(entity_id),
 condition TEXT,
 source_record_id INTEGER REFERENCES source_records(record_id)
);
CREATE INDEX IF NOT EXISTS idx_expression_gene ON expression_measurements(gene_entity_id);
CREATE INDEX IF NOT EXISTS idx_expression_sample ON expression_measurements(sample_entity_id);

CREATE TABLE IF NOT EXISTS omics_samples(
 entity_id INTEGER PRIMARY KEY REFERENCES entities(entity_id) ON DELETE CASCADE,
 sample_accession TEXT,
 study_accession TEXT,
 assay_type TEXT NOT NULL,
 organism_entity_id INTEGER REFERENCES entities(entity_id),
 tissue_entity_id INTEGER REFERENCES entities(entity_id),
 cell_type TEXT,
 disease_entity_id INTEGER REFERENCES entities(entity_id),
 metadata_json TEXT NOT NULL DEFAULT '{}',
 source_record_id INTEGER REFERENCES source_records(record_id)
);
CREATE INDEX IF NOT EXISTS idx_omics_study ON omics_samples(study_accession,assay_type);

CREATE TABLE IF NOT EXISTS interaction_evidence(
 evidence_id INTEGER PRIMARY KEY,
 subject_entity_id INTEGER NOT NULL REFERENCES entities(entity_id),
 object_entity_id INTEGER NOT NULL REFERENCES entities(entity_id),
 interaction_type TEXT NOT NULL,
 detection_method TEXT,
 confidence REAL CHECK(confidence IS NULL OR(confidence>=0 AND confidence<=1)),
 biological_role TEXT,
 source_record_id INTEGER REFERENCES source_records(record_id)
);
CREATE INDEX IF NOT EXISTS idx_interaction_subject ON interaction_evidence(subject_entity_id);
CREATE INDEX IF NOT EXISTS idx_interaction_object ON interaction_evidence(object_entity_id);

CREATE TABLE IF NOT EXISTS pathway_memberships(
 pathway_entity_id INTEGER NOT NULL REFERENCES entities(entity_id),
 member_entity_id INTEGER NOT NULL REFERENCES entities(entity_id),
 role TEXT,
 evidence_code TEXT,
 source_record_id INTEGER REFERENCES source_records(record_id),
 PRIMARY KEY(pathway_entity_id,member_entity_id,role)
) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS idx_pathway_member ON pathway_memberships(member_entity_id);

CREATE TABLE IF NOT EXISTS ontology_terms(
 entity_id INTEGER PRIMARY KEY REFERENCES entities(entity_id) ON DELETE CASCADE,
 ontology_id TEXT NOT NULL,
 term_id TEXT NOT NULL,
 term_name TEXT NOT NULL,
 definition TEXT,
 obsolete INTEGER NOT NULL DEFAULT 0 CHECK(obsolete IN(0,1)),
 replaced_by TEXT,
 UNIQUE(ontology_id,term_id)
);
CREATE INDEX IF NOT EXISTS idx_ontology_name ON ontology_terms(term_name);

CREATE TABLE IF NOT EXISTS ontology_edges(
 ontology_id TEXT NOT NULL,
 parent_term_id TEXT NOT NULL,
 predicate TEXT NOT NULL,
 child_term_id TEXT NOT NULL,
 source_record_id INTEGER REFERENCES source_records(record_id),
 PRIMARY KEY(ontology_id,parent_term_id,predicate,child_term_id)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS publications(
 entity_id INTEGER PRIMARY KEY REFERENCES entities(entity_id) ON DELETE CASCADE,
 doi TEXT,
 pmid TEXT,
 pmcid TEXT,
 title TEXT,
 journal TEXT,
 publication_year INTEGER,
 abstract TEXT,
 license_id TEXT,
 full_text_available INTEGER NOT NULL DEFAULT 0 CHECK(full_text_available IN(0,1)),
 UNIQUE(doi)
);
CREATE INDEX IF NOT EXISTS idx_publications_pmid ON publications(pmid);

CREATE TABLE IF NOT EXISTS dataset_files(
 file_id INTEGER PRIMARY KEY,
 release_id INTEGER NOT NULL REFERENCES dataset_releases(release_id),
 relative_path TEXT NOT NULL,
 format TEXT NOT NULL,
 compression TEXT,
 checksum_sha256 TEXT,
 byte_size INTEGER,
 license_id TEXT,
 access_class TEXT NOT NULL DEFAULT 'open' CHECK(access_class IN('open','registered','controlled','restricted')),
 UNIQUE(release_id,relative_path)
);

CREATE TABLE IF NOT EXISTS import_checkpoints(
 source_id TEXT NOT NULL REFERENCES data_sources(source_id),
 dataset_key TEXT NOT NULL,
 cursor TEXT,
 last_record_key TEXT,
 records_imported INTEGER NOT NULL DEFAULT 0,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY(source_id,dataset_key)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS token_index_metadata(
 index_id INTEGER PRIMARY KEY,
 entity_id INTEGER REFERENCES entities(entity_id) ON DELETE CASCADE,
 tokenizer TEXT NOT NULL,
 tokenizer_version TEXT NOT NULL,
 token_kind TEXT NOT NULL CHECK(token_kind IN('metadata','protein_kmer','dna_kmer','rna_kmer','chemical_fingerprint','ontology_synonym')),
 parameters_json TEXT NOT NULL DEFAULT '{}',
 payload_path TEXT,
 checksum_sha256 TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO schema_migrations(version,description)
VALUES(2,'Add normalized genomics, variants, omics, interactions, ontology and provenance tables');
