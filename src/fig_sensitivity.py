"""
fig_sensitivity.py  ->  Figure_5
Solar-entry threshold vs. capacity factor across the three manuscript
scenarios. Every point traces to model output:
  S1 default, flat load (headline)   : results_multisite.csv thr_s1_default
  S2 PV sensitivity (DC/AC 1.3, 11%) : results_pv_sens.csv xover (model run)
  S3 temperature-responsive load     : results_multisite.csv thr_s3_temp
                                       (identical to S1 - verified max
                                       difference $0/ton)
Markets labelled by city name, collision-free (adjustText leader lines).
"""
import pandas as pd
from mdpi_energies_style import (set_style, new_fig, save_fig, OKABE_ITO,
                                 label_points_repel, city_names)


def main(curated="data/results_multisite.csv",
         pv_sens="data/results_pv_sens.csv", outdir="figures"):
    set_style()
    cur = pd.read_csv(curated).sort_values("cf")
    sens = pd.read_csv(pv_sens).sort_values("cf")

    fig, ax = new_fig(width="full", height_ratio=0.58)
    ax.plot(cur["cf"], cur["thr_s1_default"], ls="-", marker="o", ms=4.5,
            color=OKABE_ITO["blue"],
            label="S1 · default config, flat load (headline)")
    ax.plot(sens["cf"], sens["xover"], ls="--", marker="s", ms=4.5,
            color=OKABE_ITO["vermillion"],
            label="S2 · PV sensitivity (DC/AC 1.3, 11% losses), flat load")
    ax.plot(cur["cf"], cur["thr_s3_temp"], ls=":", marker="^", ms=4.5,
            color=OKABE_ITO["green"],
            label="S3 · temperature-responsive load (coincides with S1)")

    ax.axhline(100, ls=":", lw=1.0, color=OKABE_ITO["grey"])
    ax.text(cur["cf"].min(), 101.5, "$100/t reference",
            ha="left", va="bottom", fontsize=6.5, color=OKABE_ITO["grey"])

    label_points_repel(ax, cur["cf"], cur["thr_s1_default"],
                       city_names(cur["market"]), fontsize=6.4)

    ax.set_xlabel("Solar capacity factor (real NREL PVWatts)")
    ax.set_ylabel("Carbon-price threshold for on-site solar\n(\$/ton CO$_2$)")
    ax.set_ylim(95, 245)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    save_fig(fig, "Figure_5", outdir=outdir)


if __name__ == "__main__":
    main()
