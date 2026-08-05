"""
fig_crossover.py  ->  Figure_4
Carbon-price threshold at which on-site solar enters the cost-optimal
portfolio vs. real solar capacity factor, across 11 U.S. markets
(manuscript Table 4, default configuration). Reproduces the headline
R^2=0.97 relationship. Markets are labelled by CITY NAME with
collision-free placement (adjustText leader lines).
"""
import numpy as np
import pandas as pd
from mdpi_energies_style import (set_style, new_fig, save_fig, OKABE_ITO,
                                 label_points_repel, city_names)


def main(results="data/results_multisite.csv", outdir="figures"):
    set_style()
    df = pd.read_csv(results).sort_values("cf")
    x = df["cf"].to_numpy()
    y = df["thr_s1_default"].to_numpy()

    m, b = np.polyfit(x, y, 1)
    yhat = m * x + b
    r2 = 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)

    fig, ax = new_fig(width="full", height_ratio=0.58)
    xs = np.linspace(x.min() - 0.004, x.max() + 0.004, 100)
    ax.plot(xs, m * xs + b, ls="--", lw=1.2, color=OKABE_ITO["vermillion"],
            label=f"linear fit (R$^2$={r2:.2f})", zorder=1)
    ax.scatter(x, y, s=45, color=OKABE_ITO["blue"], edgecolor="white",
               linewidth=0.5, zorder=3)
    ax.axhline(100, ls=":", lw=1.0, color=OKABE_ITO["green"])
    ax.text(x.max(), 101.5, "$100/t reference", ha="right", va="bottom",
            fontsize=6.5, color=OKABE_ITO["green"])

    label_points_repel(ax, x, y, city_names(df["market"]), fontsize=6.6)

    ax.set_xlabel("Solar capacity factor (real NREL PVWatts, single-axis)")
    ax.set_ylabel("Carbon price where on-site solar enters\n(\$/ton CO$_2$)")
    ax.set_xlim(x.min() - 0.006, x.max() + 0.010)
    ax.set_ylim(90, 245)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    save_fig(fig, "Figure_4", outdir=outdir)


if __name__ == "__main__":
    main()
