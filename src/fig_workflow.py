"""
fig_workflow.py  ->  Figure_1
Explanatory flowchart of the coupled framework (Section 4): public data
-> LCOE/LCOS screening + Monte Carlo -> representative-day reduction ->
capacity-expansion & dispatch LP with storage -> carbon-price sweep ->
per-market solar-entry thresholds. Pure matplotlib so it exports as a
clean 600-dpi PNG + vector PDF (fully reproducible, no external tool).

Per the MDPI GenAI policy this is an explanatory diagram built from the
manuscript's own method description; it contains no observed data.
"""
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from mdpi_energies_style import set_style, save_fig, OKABE_ITO, COLS
import matplotlib.pyplot as plt


def box(ax, xy, w, h, text, fc, ec, fs=7.2, tc="#111111"):
    x, y = xy
    p = mpatches.FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.006,rounding_size=0.012",
                                linewidth=0.8, edgecolor=ec, facecolor=fc)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, zorder=5)
    return (x + w / 2, y)


def arrow(ax, p0, p1, color="#555555"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=9,
                                 lw=0.9, color=color, shrinkA=1, shrinkB=1,
                                 zorder=1))


def main(outdir="figures"):
    set_style()
    W = COLS["medium"]
    fig, ax = plt.subplots(figsize=(W, W * 0.95))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    blue, org, verm, grn = (OKABE_ITO["blue"], OKABE_ITO["orange"],
                            OKABE_ITO["vermillion"], OKABE_ITO["green"])

    def tint(hexc, a=0.14):
        import matplotlib.colors as mc
        r, g, b = mc.to_rgb(hexc)
        return (1 - a + a * r, 1 - a + a * g, 1 - a + a * b)

    bw, bh = 0.62, 0.085
    cx = 0.5 - bw / 2

    box(ax, (cx, 0.86), bw, bh,
        "Public data: EIA / NREL costs · EPA emissions ·\n"
        "NREL PVWatts V8 hourly solar (11 markets)",
        tint(blue), blue)
    box(ax, (0.06, 0.70), 0.40, bh,
        "LCOE / LCOS screening\n+ Monte Carlo gas price (n=10,000)",
        tint(org), org)
    box(ax, (0.54, 0.70), 0.40, bh,
        "Representative-day reduction\nk-means (k=12, weighted)",
        tint(grn), grn)
    box(ax, (cx, 0.52), bw, bh + 0.02,
        "Capacity-expansion + hourly dispatch LP\n"
        "grid · NGCC · PV · 4-h battery  (PuLP/CBC)",
        tint(verm), verm, fs=7.4)
    box(ax, (cx, 0.36), bw, bh,
        "Carbon-price sweep  $0–250/ton",
        tint(blue), blue)
    box(ax, (0.06, 0.19), 0.40, bh,
        "Per-market solar-entry\nthreshold vs. capacity factor",
        tint(grn), grn)
    box(ax, (0.54, 0.19), 0.40, bh,
        "Robustness: PV & load\nsensitivities · relaxed grid",
        tint(org), org)

    tc = 0.5
    arrow(ax, (tc, 0.86), (0.26, 0.70 + bh))
    arrow(ax, (tc, 0.86), (0.74, 0.70 + bh))
    arrow(ax, (0.26, 0.70), (tc, 0.52 + bh + 0.02))
    arrow(ax, (0.74, 0.70), (tc, 0.52 + bh + 0.02))
    arrow(ax, (tc, 0.52), (tc, 0.36 + bh))
    arrow(ax, (tc, 0.36), (0.26, 0.19 + bh))
    arrow(ax, (tc, 0.36), (0.74, 0.19 + bh))

    save_fig(fig, "Figure_1", outdir=outdir)


if __name__ == "__main__":
    main()
