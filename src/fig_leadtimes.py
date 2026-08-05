"""
fig_leadtimes.py  ->  Figure_2
Equipment and interconnection lead-time evidence (manuscript Table 2)
shown as horizontal range bars, in months, with the typical 18-36 month
campus construction window overlaid for context.
Sources: DOE 2022/2024c, NIAC 2024, Reuters 2025, ERCOT 2024
(manuscript refs [8-11,26]). NIAC weeks converted: 80 wk = 18.4 mo,
210 wk = 48.3 mo; Reuters ~128-143 wk = 29.5-33 mo.
"""
import numpy as np
from mdpi_energies_style import set_style, new_fig, save_fig, OKABE_ITO

ITEMS = [
    ("Distribution transformer (2019)",        3,    6,    "equip"),
    ("Distribution transformer (2023)",       12,   30,    "equip"),
    ("Generator interconnection (ERCOT)",     18,   30,    "proc"),
    ("Large power transformer (Reuters '25)", 29.5, 33,    "equip"),
    ("Large transformer (NIAC)",              18.4, 48.3,  "equip"),
    ("Large power transformer (DOE)",         36,   60,    "equip"),
    ("Combined critical path (both)",         48,   72,    "crit"),
]
COLOR = {"equip": OKABE_ITO["blue"], "proc": OKABE_ITO["orange"],
         "crit": OKABE_ITO["vermillion"]}
LABEL = {"equip": "Equipment lead time", "proc": "Interconnection process",
         "crit": "Combined critical path"}


def main(outdir="figures"):
    set_style()
    fig, ax = new_fig(width="medium", height_ratio=0.68)
    y = np.arange(len(ITEMS))[::-1]
    seen = set()
    for yi, (lab, lo, hi, kind) in zip(y, ITEMS):
        ax.barh(yi, hi - lo, left=lo, height=0.55, color=COLOR[kind],
                edgecolor="white", linewidth=0.5,
                label=LABEL[kind] if kind not in seen else None)
        seen.add(kind)
        ax.text(hi + 1.2, yi, f"{lo:g}–{hi:g}", va="center",
                fontsize=6.6, color="#333333")

    ax.axvspan(18, 36, color="#000000", alpha=0.05, zorder=0)
    ax.text(27, len(ITEMS) - 0.3, "typical campus\nconstruction 18–36 mo",
            ha="center", va="top", fontsize=6.2, color="#666666")

    ax.set_yticks(y)
    ax.set_yticklabels([it[0] for it in ITEMS], fontsize=6.8)
    ax.set_xlabel("Lead time / duration (months)")
    ax.set_xlim(0, 80)
    ax.legend(loc="upper right", frameon=False, fontsize=6.6)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save_fig(fig, "Figure_2", outdir=outdir)


if __name__ == "__main__":
    main()
