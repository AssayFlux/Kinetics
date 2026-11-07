"""R1-only Python runtime probe; not a production scientific capability."""

def runtime_report():
    import platform
    import sys
    import Bio
    import numpy
    import scipy

    return {
        "python": sys.version,
        "platform": platform.platform(),
        "biopython": Bio.__version__,
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
    }
