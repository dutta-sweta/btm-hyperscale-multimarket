"""
fig_montecarlo.py  ->  Figure_3
Monte Carlo screening: distribution of NGCC LCOE under gas-price
uncertainty at three carbon prices ($0/$50/$100), vs the fixed PV LCOE
benchmark ($63/MWh). Reproduces the statistics in manuscript Table 3
directly from the Section 4.3 equations (fixed seed 42).

This is a *screening* device (levelized cost per MWh); it does not set
the optimal portfolio, which is governed by the capacity-expansion model.
"""
import numpy as np
from mdpi_energies_style import set_style, new_fig, save_fig, OKABE_ITO

# --- NGCC parameters (manuscript Table 1 + Section 4) --------------------
R, LIFE = 0.067, 30
CAPEX, FOM, VOM, HR = 921_000, 15_510, 3.33, 6226   # $/MW, $/MW-yr, $/MWh, Btu/kWh
NGCC_CF = 0.90                                       # firm dispatchable duty
EF_CO2 = 53.06                                       # kg CO2 / MMBtu
PV_BENCH = 63.0                                      # $/MWh (single-axis, ~25% CF)
CARBON = [0, 50, 100]
N, SEED = 10_000, 42


def crf(r, n): return r * (1 + r) ** n / ((1 + r) ** n - 1)


def main(outdir="figures"):
    set_style()
    fixed_per_mwh = (CAPEX * crf(R, LIFE) + FOM) / (8760 * NGCC_CF)
    # Gas price: normal(4, 1.5) CLIPPED to [1, 10] $/MMBtu.
    # NOTE: clipping (not true truncation) is what reproduces manuscript
    # Table 3 exactly (mean 39.3/55.8/72.4, sd 9.2, P(>PV) 0.6/21.6/83.6%).
    # Manuscript Section 4.5 wording matches ("clipped").
    rng = np.random.default_rng(SEED)
    gas = np.clip(rng.normal(4.0, 1.5, N), 1.0, 10.0)

    fig, ax = new_fig(width="medium", height_ratio=0.60)
    colors = [OKABE_ITO["blue"], OKABE_ITO["orange"], OKABE_ITO["vermillion"]]
    for cp, col in zip(CARBON, colors):
        adder = (HR / 1000) * (EF_CO2 / 1000) * cp
        lcoe = fixed_per_mwh + VOM + (HR / 1000) * gas + adder
        p_exceed = np.mean(lcoe > PV_BENCH) * 100
        ax.hist(lcoe, bins=60, density=True, histtype="stepfilled",
                alpha=0.35, color=col)
        ax.hist(lcoe, bins=60, density=True, histtype="step",
                lw=1.3, color=col,
                label=f"${cp}/t  (mean ${lcoe.mean():.1f}, "
                      f"P>PV {p_exceed:.0f}%)")

    ax.axvline(PV_BENCH, ls="--", lw=1.2, color="#444444")
    ax.text(PV_BENCH + 0.6, ax.get_ylim()[1] * 0.92,
            "PV benchmark\n$63/MWh", fontsize=6.8, color="#444444", va="top")
    ax.set_xlabel("NGCC levelized cost of electricity ($/MWh)")
    ax.set_ylabel("Probability density")
    ax.legend(title="Carbon price", loc="upper right", frameon=False,
              title_fontsize=7)
    fig.tight_layout()
    save_fig(fig, "Figure_3", outdir=outdir)


if __name__ == "__main__":
    main()
