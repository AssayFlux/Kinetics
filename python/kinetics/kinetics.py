"""Enzyme kinetics models and transparent, dependency-free parameter estimation."""
from __future__ import annotations
from math import log, sqrt

def michaelis_menten(substrate: float, vmax: float, km: float) -> float:
    if substrate < 0 or vmax < 0 or km <= 0: raise ValueError("Require S>=0, Vmax>=0 and Km>0")
    return vmax*substrate/(km+substrate)

def inhibition_rate(substrate: float, inhibitor: float, vmax: float, km: float,
                    ki: float, mode: str, ki_uncompetitive: float | None = None) -> float:
    if inhibitor < 0 or ki <= 0: raise ValueError("Require inhibitor>=0 and Ki>0")
    alpha=1+inhibitor/ki
    if mode=="competitive": return vmax*substrate/(alpha*km+substrate)
    if mode=="uncompetitive": return vmax*substrate/(km+alpha*substrate)
    if mode=="noncompetitive": return (vmax/alpha)*substrate/(km+substrate)
    if mode=="mixed":
        if ki_uncompetitive is None or ki_uncompetitive <= 0:
            raise ValueError("mixed inhibition requires ki_uncompetitive>0")
        alpha_prime=1+inhibitor/ki_uncompetitive
        return vmax*substrate/(alpha*km+alpha_prime*substrate)
    raise ValueError("mode must be competitive, uncompetitive, noncompetitive or mixed")

def fit_michaelis_menten(substrates: list[float], rates: list[float], *,
                         vmax_bounds: tuple[float,float] | None = None,
                         km_bounds: tuple[float,float] | None = None,
                         grid_size: int = 100) -> dict[str, object]:
    """Log-grid least-squares fit; exploratory estimator, not a substitute for validation."""
    if len(substrates)!=len(rates) or len(rates)<3: raise ValueError("Need >=3 paired observations")
    if grid_size<10: raise ValueError("grid_size must be >=10")
    if any(s<0 for s in substrates) or any(v<0 for v in rates): raise ValueError("Inputs must be non-negative")
    if max(substrates)==0 or max(rates)==0: raise ValueError("Non-informative data")
    smax, rmax=max(substrates), max(rates)
    vlo,vhi=vmax_bounds or (rmax*0.5,rmax*5)
    klo,khi=km_bounds or (max(smax/1000,1e-12),smax*100)
    if not (0<vlo<vhi and 0<klo<khi): raise ValueError("Bounds must be positive and increasing")
    best=None
    for i in range(grid_size):
        vmax=vlo*(vhi/vlo)**(i/(grid_size-1))
        for j in range(grid_size):
            km=klo*(khi/klo)**(j/(grid_size-1))
            residuals=[v-michaelis_menten(s,vmax,km) for s,v in zip(substrates,rates)]
            sse=sum(x*x for x in residuals)
            if best is None or sse<best[0]: best=(sse,vmax,km,residuals)
    assert best is not None
    sse,vmax,km,residuals=best
    return {"vmax":vmax,"km":km,"sse":sse,"rmse":sqrt(sse/len(rates)),
            "n":len(rates),"estimator":"log-grid least squares",
            "confidence_intervals":None,
            "warnings":["No confidence intervals calculated","Grid search is approximate",
                        "Inspect residuals and identifiability before interpretation"],
            "residuals":residuals}
