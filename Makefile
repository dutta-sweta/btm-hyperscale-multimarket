# Convenience targets. Requires a Python env with requirements installed.
.PHONY: setup data model results figures verify all clean

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

data:            ## re-pull PVWatts profiles (needs NREL_API_KEY); writes both configs
	python src/pull_pvwatts_profiles.py --config default
	python src/pull_pvwatts_profiles.py --config pv_sens

results:         ## run the optimization for all four scenario combinations
	python src/model_multisite.py --profiles data/pv_profiles_default.csv  --load flat
	python src/model_multisite.py --profiles data/pv_profiles_default.csv  --load temp
	python src/model_multisite.py --profiles data/pv_profiles_pv_sens.csv  --load flat
	python src/model_multisite.py --profiles data/pv_profiles_pv_sens.csv  --load temp

verify:          ## check model output against the manuscript tables/claims
	python src/verify_manuscript.py --config default --results data/results_default.csv
	python src/verify_manuscript.py --config pv_sens --results data/results_pv_sens.csv

figures:         ## regenerate all manuscript figures (600-dpi PNG + PDF) into figures/
	python src/make_all_figures.py

all: results figures verify

clean:
	rm -f figures/*.pdf figures/*.png
