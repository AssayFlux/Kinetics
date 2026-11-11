from __future__ import annotations
import hashlib
import pytest
from kinetics.pharmvar import match_pharmvar_haplotype, parse_pharmvar_tsv
TSV=("Haplotype Identifier\tGene Symbol\tdbSNP rsID\tReference Sequence\tVariant Start\tVariant Stop\tReference Allele\tVariant Allele\tVariant Type\n"
"*1\tSYN1\t.\tNG_SYNTHETIC.1\t0\t0\tREFERENCE\t.\treference\n"
"*2\tSYN1\trsSynthetic1\tNG_SYNTHETIC.1\t2\t2\tA\tG\tsnv\n")
def defs():
 return parse_pharmvar_tsv(TSV,source_release="fixture-1",source_url="https://example.invalid/source",
  source_sha256=hashlib.sha256(TSV.encode()).hexdigest(),license_id="CC0 synthetic test only",expected_release="fixture-1")
def test_pharmvar_exact_byte_digest_and_accession_preservation():
 d=defs(); assert len(d)==2 and d[0].is_reference
 assert next(iter(d[1].variants)).reference_accession=="NG_SYNTHETIC.1"
def test_pharmvar_exact_haplotype_match_and_unphased_abstention():
 d=defs(); v=next(iter(d[1].variants))
 m=match_pharmvar_haplotype("SYN1","NG_SYNTHETIC.1",[v],d,phase_confirmed=True,call_complete=True)
 assert m.status=="matched" and m.haplotype=="*2"
 u=match_pharmvar_haplotype("SYN1","NG_SYNTHETIC.1",[v],d,phase_confirmed=False,call_complete=True)
 assert u.status=="no_call_unphased" and u.haplotype is None
def test_pharmvar_rejects_digest_release_and_accession_mismatch():
 digest=hashlib.sha256(TSV.encode()).hexdigest()
 with pytest.raises(ValueError,match="checksum"):
  parse_pharmvar_tsv(TSV,source_release="fixture-1",source_url="https://example.invalid/source",
   source_sha256="0"*64,license_id="test",expected_release="fixture-1")
 with pytest.raises(ValueError,match="release"):
  parse_pharmvar_tsv(TSV,source_release="fixture-1",source_url="https://example.invalid/source",
   source_sha256=digest,license_id="test",expected_release="fixture-2")
 with pytest.raises(ValueError,match="different reference accession"):
  match_pharmvar_haplotype("SYN1","OTHER",[next(iter(defs()[1].variants))],defs(),
   phase_confirmed=True,call_complete=True)
