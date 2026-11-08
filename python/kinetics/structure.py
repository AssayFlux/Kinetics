"""Conservative PDB ATOM/HETATM parsing and geometric descriptors."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from typing import Iterable

@dataclass(frozen=True)
class Atom:
    serial:int; name:str; residue:str; chain:str; residue_number:int
    x:float; y:float; z:float; element:str

def parse_pdb(text: str, *, include_hetero: bool=False) -> list[Atom]:
    atoms=[]
    for line_no,line in enumerate(text.splitlines(),1):
        if not (line.startswith("ATOM  ") or (include_hetero and line.startswith("HETATM"))): continue
        if len(line)<54: raise ValueError(f"PDB line {line_no}: truncated coordinate record")
        if line[16:17] not in (" ","A"): continue
        try:
            atoms.append(Atom(int(line[6:11]),line[12:16].strip(),line[17:20].strip(),
                line[21:22].strip(),int(line[22:26]),float(line[30:38]),float(line[38:46]),
                float(line[46:54]),line[76:78].strip().upper() if len(line)>=78 else ""))
        except ValueError as exc: raise ValueError(f"PDB line {line_no}: invalid atom field") from exc
    if not atoms: raise ValueError("No supported PDB coordinate records")
    return atoms

def rmsd(reference: Iterable[Atom], mobile: Iterable[Atom], *, superpose: bool=False) -> float:
    a,b=list(reference),list(mobile)
    if len(a)!=len(b) or not a: raise ValueError("Coordinate sets must have equal non-zero length")
    if superpose: raise NotImplementedError("Rigid-body superposition is not implemented; align coordinates first")
    return sqrt(sum((p.x-q.x)**2+(p.y-q.y)**2+(p.z-q.z)**2 for p,q in zip(a,b))/len(a))

def contact_pairs(atoms: Iterable[Atom], cutoff_angstrom: float=8.0) -> list[tuple[int,int,float]]:
    points=list(atoms)
    if cutoff_angstrom<=0: raise ValueError("cutoff must be positive")
    result=[]
    for i,a in enumerate(points):
        for j in range(i+1,len(points)):
            b=points[j]
            if a.chain==b.chain and a.residue_number==b.residue_number: continue
            d=sqrt((a.x-b.x)**2+(a.y-b.y)**2+(a.z-b.z)**2)
            if d<=cutoff_angstrom: result.append((i,j,d))
    return result
