"""SDF V2000 atom/bond parsing and transparent 2D graph descriptors."""
from __future__ import annotations
from collections import Counter
from math import sqrt

ATOMIC_MASS={"H":1.008,"C":12.011,"N":14.007,"O":15.999,"F":18.998,"P":30.974,
"S":32.06,"CL":35.45,"BR":79.904,"I":126.90,"B":10.81,"SI":28.085}

def parse_sdf_record(text: str) -> dict[str, object]:
    lines=text.splitlines()
    if len(lines)<4 or "V2000" not in lines[3]: raise ValueError("Only molfile V2000 is supported")
    try: na,nb=int(lines[3][0:3]),int(lines[3][3:6])
    except ValueError as exc: raise ValueError("Invalid V2000 counts line") from exc
    if na<1 or len(lines)<4+na+nb: raise ValueError("Truncated SDF record")
    atoms=[]; elements=Counter()
    for line in lines[4:4+na]:
        symbol=line[31:34].strip().upper()
        if symbol not in ATOMIC_MASS: raise ValueError(f"Unsupported element: {symbol}")
        atoms.append({"x":float(line[0:10]),"y":float(line[10:20]),"z":float(line[20:30]),"element":symbol})
        elements[symbol]+=1
    bonds=[]
    for line in lines[4+na:4+na+nb]:
        a,b,order=int(line[0:3]),int(line[3:6]),int(line[6:9])
        if not (1<=a<=na and 1<=b<=na and a!=b and order in (1,2,3,4)): raise ValueError("Invalid bond record")
        bonds.append((a-1,b-1,order))
    return {"atoms":atoms,"bonds":bonds,"atom_count":na,"bond_count":nb,
            "formula":formula(elements),"molecular_weight":sum(ATOMIC_MASS[k]*v for k,v in elements.items()),
            "limitations":["V2000 only","No stereochemical interpretation","No protonation/tautomer normalization"]}

def formula(elements: Counter[str]) -> str:
    keys=[]
    if "C" in elements: keys.append("C")
    if "H" in elements: keys.append("H")
    keys.extend(sorted(k for k in elements if k not in ("C","H")))
    return "".join(k+(str(elements[k]) if elements[k]!=1 else "") for k in keys)
