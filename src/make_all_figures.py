"""make_all_figures.py — regenerate every manuscript figure (600-dpi PNG + PDF).
Run from anywhere: outputs always land in <repo_root>/figures."""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
os.chdir(_ROOT)

import fig_workflow, fig_leadtimes, fig_montecarlo, fig_crossover, fig_sensitivity

STEPS = [
    ("Figure 1  methodology workflow", fig_workflow.main),
    ("Figure 2  lead-time ranges",     fig_leadtimes.main),
    ("Figure 3  Monte Carlo LCOE",     fig_montecarlo.main),
    ("Figure 4  crossover vs CF",      fig_crossover.main),
    ("Figure 5  sensitivity scenarios", fig_sensitivity.main),
]

if __name__ == "__main__":
    for name, fn in STEPS:
        print(f"{name} ...")
        fn()
    print("\nAll figures written to figures/ (600-dpi PNG + vector PDF).")
