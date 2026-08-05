"""
verify_manuscript.py
Reconcile the manuscript's numbers against the model's actual output.

Usage
-----
    # headline (default config) — after you pull it and run the model:
    python src/verify_manuscript.py --config default \
        --results data/results_default.csv

    # sensitivity config (the existing profiles reproduce this):
    python src/verify_manuscript.py --config pv_sens \
        --results data/results_pv_sens.csv

What it checks
--------------
* default : every cell of manuscript Table 4 (capacity factor, solar-entry
            threshold, PV energy share at $150/ton) against the model.
* pv_sens : the three quantitative claims the manuscript makes about the
            PV-assumption sensitivity (Section 5.5):
              (a) Phoenix threshold = $105/ton,
              (b) no market's threshold reaches $100/ton,
              (c) thresholds fall ~$9/ton on average vs the default.

Exit code is non-zero if any check fails, so this can gate a submission.
"""
import argparse
import sys
import pandas as pd

# --- Manuscript Table 4 (DEFAULT config, 1.2/14%) as printed -------------
#   code : (capacity_factor, solar_entry_threshold, pv_share_%_at_150)
TABLE4_DEFAULT = {
    "PDX": (0.147, 230, 0), "CMH": (0.168, 190, 0), "SBN": (0.171, 185, 0),
    "IAD": (0.174, 180, 0), "PHL": (0.175, 180, 0), "CLT": (0.186, 165, 0),
    "JAN": (0.188, 160, 0), "ATL": (0.189, 160, 0), "IAH": (0.191, 160, 0),
    "RNO": (0.224, 125, 16), "PHX": (0.238, 110, 18),
}
DEFAULT_MEAN_THR = sum(v[1] for v in TABLE4_DEFAULT.values()) / len(TABLE4_DEFAULT)

CITY = {
    "PDX": "Portland", "CMH": "Columbus", "SBN": "South Bend",
    "IAD": "Ashburn", "PHL": "Philadelphia", "CLT": "Charlotte",
    "JAN": "Jackson", "ATL": "Atlanta", "IAH": "Houston",
    "RNO": "Reno", "PHX": "Phoenix",
}

CF_TOL, THR_TOL, SHARE_TOL = 0.003, 6, 2   # tolerances (thr sweep step is $5)


def load(results):
    m = pd.read_csv(results)
    m["code"] = m["site"].str[:3]
    return m.set_index("code")


def check_default(m):
    print(f"{'market':14} {'CF model/paper':>16} {'thr model/paper':>16} "
          f"{'PV%@150 model/paper':>20}  verdict")
    ok = True
    for code, (cf_p, thr_p, sh_p) in TABLE4_DEFAULT.items():
        r = m.loc[code]
        cf_ok = abs(r.cf - cf_p) <= CF_TOL
        thr_ok = abs(r.xover - thr_p) <= THR_TOL
        sh_ok = abs(r.pvsh150 - sh_p) <= SHARE_TOL
        row_ok = cf_ok and thr_ok and sh_ok
        ok &= row_ok
        print(f"{CITY[code]:14} {r.cf:7.3f}/{cf_p:<7.3f} {int(r.xover):7d}/{thr_p:<7d} "
              f"{int(r.pvsh150):9d}/{sh_p:<9d}  {'PASS' if row_ok else 'FAIL'}")
    return ok


def check_pv_sens(m):
    phx = m.loc["PHX", "xover"]
    mn = m["xover"].min()
    mean_drop = DEFAULT_MEAN_THR - m["xover"].mean()
    checks = [
        ("Phoenix threshold = $105/ton", abs(phx - 105) <= THR_TOL, f"${int(phx)}/ton"),
        ("No market reaches $100/ton",   mn > 100,                  f"min ${int(mn)}/ton"),
        ("~$9/ton lower on average",     abs(mean_drop - 9) <= 3,   f"${mean_drop:.1f}/ton"),
    ]
    ok = True
    for label, passed, got in checks:
        ok &= passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {label:34s} -> model: {got}")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", choices=["default", "pv_sens"], required=True)
    ap.add_argument("--results", required=True, help="model results CSV")
    args = ap.parse_args()

    m = load(args.results)
    print(f"\nVerifying '{args.config}' against manuscript using {args.results}\n")
    ok = check_default(m) if args.config == "default" else check_pv_sens(m)
    print("\n" + ("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
