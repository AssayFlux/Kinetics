"""R1-only on-device scientific dependency probe; not a production capability."""

from io import StringIO


def runtime_report():
    import platform
    import sys

    import Bio
    import numpy
    import scipy
    from Bio import SeqIO

    fasta = StringIO(">kinetics-r1-smoke\nACGTACGT\n")
    record = next(SeqIO.parse(fasta, "fasta"))
    assert str(record.seq) == "ACGTACGT"

    vector = numpy.asarray([3.0, 4.0], dtype=numpy.float64)
    norm = float(scipy.linalg.norm(vector))
    assert abs(norm - 5.0) < 1e-12

    return {
        "python": sys.version,
        "platform": platform.platform(),
        "biopython": Bio.__version__,
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "seqio_fasta_smoke": str(record.seq),
        "scipy_linalg_norm": norm,
    }
