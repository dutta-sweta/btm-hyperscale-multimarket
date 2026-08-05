"""
pull_pvwatts_profiles.py
Pull hourly PV capacity-factor + ambient-temperature profiles for public
data-center market archetypes from NREL PVWatts V8 (NSRDB PSM V3 TMY).

Reproducibility notes
---------------------
* NEVER hard-code your API key. This script reads it from the environment:
      export NREL_API_KEY="your_key_here"     # macOS / Linux
  Get a free key at https://developer.nlr.gov/signup/
* Coordinates are public metro city-centers, NOT any facility location.
* All system parameters are identical across sites so only climate varies.
* Record the API version and access date in Supplementary Material S2 at
  submission.

Usage
-----
    export NREL_API_KEY="..."
    python src/pull_pvwatts_profiles.py --config default   # DC/AC 1.2, 14% loss
    python src/pull_pvwatts_profiles.py --config pv_sens   # DC/AC 1.3, 11% loss
"""
import argparse
import csv
import os
import sys
import time
import requests

# NREL retired developer.nrel.gov on 2026-05-29; the current host is
# developer.nlr.gov. If you are running this before that cutover on an old
# environment, the legacy host was https://developer.nrel.gov/api/pvwatts/v8.json
BASE = "https://developer.nlr.gov/api/pvwatts/v8.json"

# Two documented configurations matching the manuscript.
CONFIGS = {
    # Headline / default (manuscript Section 4.1): DC/AC 1.2, 14% system losses
    "default": dict(dc_ac_ratio=1.2, losses=14),
    # PV-assumption sensitivity (Section 4.6): DC/AC 1.3, 11% system losses
    "pv_sens": dict(dc_ac_ratio=1.3, losses=11),
}

FIXED = dict(
    system_capacity=1000,   # kW DC (normalizer -> per-MW capacity factor)
    module_type=0,          # standard
    array_type=2,           # 1-axis tracking
    tilt=0,                 # horizontal axis for tracker
    azimuth=180,            # due south
    inv_eff=96,
    gcr=0.4,
    timeframe="hourly",
    dataset="nsrdb",
)

# Public representative metro coordinates (city centers), NOT facility sites.
SITES = {
    "ATL_Atlanta_GA":      (33.749,  -84.388),
    "CLT_Charlotte_NC":    (35.227,  -80.843),
    "CMH_Columbus_OH":     (39.961,  -82.999),
    "IAD_Ashburn_VA":      (39.045,  -77.487),
    "JAN_Jackson_MS":      (32.299,  -90.185),
    "PDX_Portland_OR":     (45.512, -122.658),
    "PHL_Philadelphia_PA": (39.953,  -75.165),
    "PHX_Phoenix_AZ":      (33.448, -112.074),
    "SBN_SouthBend_IN":    (41.683,  -86.250),
    "IAH_Houston_TX":      (29.760,  -95.369),
    "RNO_Reno_NV":         (39.530, -119.814),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", choices=CONFIGS, default="default")
    ap.add_argument("--out", default=None,
                    help="output CSV path (default: data/pv_profiles_<config>.csv)")
    args = ap.parse_args()

    api_key = os.environ.get("NREL_API_KEY")
    if not api_key:
        sys.exit("ERROR: set NREL_API_KEY in your environment "
                 "(export NREL_API_KEY='...'). Get one free at "
                 "https://developer.nlr.gov/signup/")

    cfg = {**FIXED, **CONFIGS[args.config]}
    out = args.out or f"data/pv_profiles_{args.config}.csv"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    rows = []
    print(f"config={args.config}  {CONFIGS[args.config]}")
    print(f"{'site':22s} {'annual CF':>9s}   weather source")
    for name, (lat, lon) in SITES.items():
        params = dict(api_key=api_key, lat=lat, lon=lon, **cfg)
        resp = requests.get(BASE, params=params, timeout=90)
        data = resp.json()
        if data.get("errors"):
            print(f"{name:22s}  ERROR: {data['errors']}")
            continue
        out_d = data["outputs"]
        ac = out_d["ac"]                                  # hourly AC power (W)
        tamb = out_d.get("tamb", [None] * len(ac))        # hourly ambient (C)
        cap_w = cfg["system_capacity"] * 1000.0
        cf = [a / cap_w for a in ac]                      # per-MW-DC capacity factor
        ann = sum(cf) / len(cf)
        src = data.get("station_info", {}).get("weather_data_source", "n/a")
        print(f"{name:22s} {ann:9.3f}   {src}")
        for h in range(len(ac)):
            rows.append([name, h, round(cf[h], 5),
                         round(tamb[h], 1) if tamb[h] is not None else ""])
        time.sleep(1)                                     # be courteous to the API

    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["site", "hour", "cf", "tamb_c"])
        w.writerows(rows)
    print(f"\nWrote {out}  ({len(rows)} rows).")


if __name__ == "__main__":
    main()
