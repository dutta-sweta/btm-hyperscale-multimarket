"""
fig_repdays.py  ->  Figure_repdays (OPTIONAL — not in the submitted set)
Illustrates the temporal-reduction step (Section 4.4): a site's 365 daily
24-hour capacity-factor shapes are clustered by k-means (k=12, fixed seed)
into weighted representative days. Uses the SAME clustering call as the
optimization model, so the figure is a faithful picture of what the model
sees. Requires a local profiles CSV (site,hour,cf,tamb_c).
"""
import numpy as np, pandas as pd
from scipy.cluster.vq import kmeans2
from mdpi_energies_style import set_style, new_fig, save_fig, OKABE_ITO, city_names

def main(profiles="data/pv_profiles_default.csv",
         site="PHX_Phoenix_AZ", k=12, seed=42, outdir="figures"):
    set_style()
    df = pd.read_csv(profiles)
    cf = df[df.site == site].sort_values("hour").cf.to_numpy()
    days = cf.reshape(365, 24)

    cent, lab = kmeans2(days, k, seed=seed, minit="++", missing="warn")
    w = np.array([(lab == i).sum() for i in range(len(cent))], float)
    keep = w > 0
    cent, w = np.clip(cent[keep], 0, None), w[keep]

    fig, ax = new_fig(width="medium", height_ratio=0.60)
    hrs = np.arange(24)
    for d in days:
        ax.plot(hrs, d, color=OKABE_ITO["skyblue"], lw=0.25, alpha=0.15, zorder=1)
    wmax = w.max()
    for c, wi in sorted(zip(cent, w), key=lambda t: -t[1]):
        ax.plot(hrs, c, color=OKABE_ITO["vermillion"],
                lw=0.8 + 2.2 * (wi / wmax), alpha=0.9, zorder=3)

    ax.plot([], [], color=OKABE_ITO["skyblue"], lw=1.0, alpha=0.6,
            label="365 daily profiles")
    ax.plot([], [], color=OKABE_ITO["vermillion"], lw=2.0,
            label=f"{len(w)} representative days (width scales with weight)")

    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Solar capacity factor")
    ax.set_xlim(0, 23)
    ax.set_ylim(0, None)
    ax.set_xticks(range(0, 24, 4))
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    save_fig(fig, "Figure_repdays", outdir=outdir)
    print(f"  {city_names([site])[0]}: {len(w)} non-empty clusters, "
          f"weights sum to {w.sum():.0f}")

if __name__ == "__main__":
    main()
