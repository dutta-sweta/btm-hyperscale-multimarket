"""
model_multisite.py: multi-market run on real NREL PVWatts V8 (NSRDB PSM V3 TMY) profiles.
Reads a profiles CSV (site, hour, cf, tamb_c) and, for each public market
archetype, co-optimizes investment + hourly dispatch with 4-hour storage.

Temporal reduction: each site's 365 days are clustered (k-means, k=12) on their 24-hour
capacity-factor shape; cluster centroids are the representative days, weighted by cluster
size (weights sum to 365). This preserves the real distribution of sunny/cloudy/seasonal
days, unlike monthly averaging.
"""
import numpy as np, pandas as pd, pulp
from scipy.cluster.vq import kmeans2

R = 0.067; CO2_KG_PER_MMBTU = 53.06
TECH = {
    "ngcc": dict(capex=921, fom=15.51, vom=3.33, hr=6226, life=30, avail=0.95),
    "pv":   dict(capex=1502, fom=20.23, life=30),
    "bess": dict(power_capex=150, energy_capex=280, fom_frac=0.025, eff_rt=0.85, life=15),
}
GRID_PRICE = 35.0; RESERVE = 0.15; PV_CREDIT = 0.05; VOLL = 5000.0; LOAD_MW = 200.0

def crf(r, n): return r*(1+r)**n/((1+r)**n-1)
def ngcc_var(gas, cp):
    hr = TECH["ngcc"]["hr"]
    return TECH["ngcc"]["vom"] + (hr/1000)*gas + (hr/1000)*(CO2_KG_PER_MMBTU/1000)*cp

def representative_days(cf, k=12, seed=42):
    days = np.asarray(cf, float).reshape(365, 24)
    cent, lab = kmeans2(days, k, seed=seed, minit="++", missing="warn")
    w = np.array([(lab == i).sum() for i in range(len(cent))], float)
    keep = w > 0
    return np.clip(cent[keep], 0, None), w[keep]

def pue_load(tamb, it_mw=160.0, pue_min=1.2, t_ref=20.0, slope=0.006, pue_cap=1.5):
    """Temperature-responsive facility load (MW): IT load x PUE(T), PUE rising with ambient temp."""
    t = np.asarray(tamb, float)
    pue = np.clip(pue_min + slope * np.clip(t - t_ref, 0, None), pue_min, pue_cap)
    return it_mw * pue

def solve_site(cf, carbon_price, grid_max=100.0, gas_price=4.0, allow_storage=True, load8760=None):
    days = np.asarray(cf, float).reshape(365, 24)
    cent, lab = kmeans2(days, 12, seed=42, minit="++", missing="warn")
    w = np.array([(lab == i).sum() for i in range(len(cent))], float)
    keep = w > 0; rep = np.clip(cent[keep], 0, None); w = w[keep]; K = len(w)
    # representative load per cluster (mean of member days); flat if no load profile
    if load8760 is None:
        rep_ld = np.full((K, 24), LOAD_MW); peak = LOAD_MW
    else:
        ld_days = np.asarray(load8760, float).reshape(365, 24)
        rep_ld = np.array([ld_days[lab == i].mean(axis=0) for i in range(len(cent))])[keep]
        peak = float(np.max(load8760))
    a_ng = (crf(R,30)*TECH["ngcc"]["capex"]+TECH["ngcc"]["fom"])*1000
    a_pv = (crf(R,30)*TECH["pv"]["capex"]+TECH["pv"]["fom"])*1000
    b = TECH["bess"]
    a_bp = (crf(R,b["life"])*b["power_capex"]+b["fom_frac"]*b["power_capex"])*1000
    a_be = (crf(R,b["life"])*b["energy_capex"]+b["fom_frac"]*b["energy_capex"])*1000
    ngv = ngcc_var(gas_price, carbon_price); eff = np.sqrt(b["eff_rt"])

    p = pulp.LpProblem("site", pulp.LpMinimize)
    GRID = pulp.LpVariable("grid",0,grid_max); NG = pulp.LpVariable("ng",0)
    PV = pulp.LpVariable("pv",0); BP = pulp.LpVariable("bp",0); BE = pulp.LpVariable("be",0)
    if not allow_storage: BP.upBound=0; BE.upBound=0
    g={ };n={};pv={};ch={};di={};soc={};us={}
    for k in range(K):
        for h in range(24):
            g[k,h]=pulp.LpVariable(f"g{k}_{h}",0); n[k,h]=pulp.LpVariable(f"n{k}_{h}",0)
            pv[k,h]=pulp.LpVariable(f"p{k}_{h}",0); ch[k,h]=pulp.LpVariable(f"c{k}_{h}",0)
            di[k,h]=pulp.LpVariable(f"d{k}_{h}",0); soc[k,h]=pulp.LpVariable(f"s{k}_{h}",0)
            us[k,h]=pulp.LpVariable(f"u{k}_{h}",0)
    fixed = a_ng*NG + a_pv*PV + a_bp*BP + a_be*BE
    var = pulp.lpSum(w[k]*(g[k,h]*GRID_PRICE + n[k,h]*ngv + us[k,h]*VOLL)
                     for k in range(K) for h in range(24))
    p += fixed + var
    for k in range(K):
        for h in range(24):
            p += g[k,h]+n[k,h]+pv[k,h]+di[k,h]+us[k,h] == rep_ld[k,h] + ch[k,h]
            p += g[k,h] <= GRID
            p += n[k,h] <= NG*TECH["ngcc"]["avail"]
            p += pv[k,h] <= PV*float(rep[k,h])
            p += ch[k,h] <= BP; p += di[k,h] <= BP; p += soc[k,h] <= BE
            prev = soc[k,h-1] if h>0 else soc[k,23]
            p += soc[k,h] == prev + eff*ch[k,h] - di[k,h]/eff
    p += BE == 4.0*BP
    p += GRID + NG*TECH["ngcc"]["avail"] + BP + PV*PV_CREDIT >= peak*(1+RESERVE)
    p.solve(pulp.PULP_CBC_CMD(msg=0))

    def E(v): return sum(w[k]*v[k,h].value() for k in range(K) for h in range(24))/1000.0
    pv_used=E(pv); tot=E(g)+E(n)+pv_used+1e-9
    return dict(grid=round(GRID.value()), ngcc=round(NG.value()), pv=round(PV.value()),
                bess_mw=round(BP.value()), bess_mwh=round(BE.value()),
                pv_share=round(100*pv_used/tot), cost_M=round(pulp.value(p.objective)/1e6,1),
                unserved=round(E(us),1))

if __name__ == "__main__":
    # --- portable paths + config/load selection -------------------------
    #     --profiles picks the PV configuration (default vs pv_sens);
    #     --load {flat,temp} picks the load model. Output is auto-named from
    #     both unless --out is given.
    import os, argparse
    _ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description="Multi-market BTM optimization")
    ap.add_argument("--profiles",
                    default=os.path.join(_ROOT, "data", "pv_profiles_default.csv"),
                    help="hourly profiles CSV (site,hour,cf,tamb_c)")
    ap.add_argument("--load", choices=["flat", "temp"], default="flat",
                    help="flat 200 MW (headline) or temperature-responsive PUE load")
    ap.add_argument("--out", default=None,
                    help="output results CSV (default: results_<config>[_temp].csv)")
    args = ap.parse_args()
    _IN = args.profiles
    if args.out:
        _OUT = args.out
    else:
        _stem = os.path.splitext(os.path.basename(_IN))[0].replace("pv_profiles_", "")
        _suffix = "_temp" if args.load == "temp" else ""
        _OUT = os.path.join(_ROOT, "data", f"results_{_stem}{_suffix}.csv")
    df = pd.read_csv(_IN)
    order = df.groupby("site").cf.mean().sort_values().index.tolist()
    rows=[]
    print(f"profiles={os.path.basename(_IN)}  load={args.load}")
    print(f"{'site':22s}{'CF':>6}{'  |  $0/t':>18}{'  $50/t':>16}{'  $100/t':>26}{'crossover':>11}")
    for s in order:
        sub = df[df.site==s].sort_values("hour")
        cf = sub.cf.values
        acf = cf.mean()
        load8760 = pue_load(sub.tamb_c.values) if args.load == "temp" else None
        r100=solve_site(cf,100,load8760=load8760); r150=solve_site(cf,150,load8760=load8760)
        xover=None
        for cp in range(0,251,5):
            if solve_site(cf,cp,load8760=load8760)["pv"]>1: xover=cp; break
        rows.append(dict(site=s, cf=round(acf,3),
                         ng100=r100["ngcc"], pv100=r100["pv"], pvsh100=r100["pv_share"],
                         ng150=r150["ngcc"], pv150=r150["pv"], bess150=r150["bess_mw"],
                         pvsh150=r150["pv_share"], cost150=r150["cost_M"], xover=xover))
        print(f"{s:22s}{acf:6.3f}   @100: NG{r100['ngcc']:>3}/PV{r100['pv']:<3}({r100['pv_share']:>2}%E)   "
              f"@150: NG{r150['ngcc']:>3}/PV{r150['pv']:<3}/B{r150['bess_mw']:<3}({r150['pv_share']:>2}%E)   "
              f"crossover ${'>250' if xover is None else xover:>4}/t")
    out=pd.DataFrame(rows)
    out.to_csv(_OUT, index=False)
    print(f"\nWrote {_OUT}")
    print(f"\nPV energy share @ $100/t: min {out.pvsh100.min()}% ({out.loc[out.pvsh100.idxmin(),'site']}), "
          f"max {out.pvsh100.max()}% ({out.loc[out.pvsh100.idxmax(),'site']})")
    print(f"Crossover carbon price: ${out.xover.min()}/t (sunniest) to ${out.xover.max()}/t (cloudiest)")
