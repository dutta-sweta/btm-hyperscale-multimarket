**Supplementary Material S2**

**Data Source Inventory, Peer-Reviewed References, PVWatts Request Parameters, and Data Dictionary**

Supplementary material for: Behind-the-Meter Power for Hyperscale Campuses: A Multi-Market Techno-Economic Framework for Grid-Constrained Energy Supply Under Carbon Pricing and Equipment Lead-Time Uncertainty (Dutta). Submitted to *Energies*.

# Purpose

This document lists every publicly available data source used in the manuscript, the exact NREL PVWatts V8 request parameters behind the hourly solar profiles, the peer-reviewed open-access references that ground the method, and a data dictionary mapping each model input to its source, units, and point of entry into the code (Supplementary Material S1). All sources were accessed and verified on 30 June 2026 unless otherwise noted. Every source listed here is cited in the manuscript's reference list.

# Data Source Inventory

| Ref. (manuscript) | Document | Organization | Used for | Accessed | URL |
|---|---|---|---|---|---|
| [13] EIA (2024a) | Capital Cost and Performance Characteristics for Utility-Scale Electric Power Generating Technologies | U.S. Energy Information Administration | CAPEX, FOM, VOM, heat rates (Table 1; §4–5) | 2026-06-30 | https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2025.pdf |
| [14] Cole & Karmakar (2025) | Cost Projections for Utility-Scale Battery Storage: 2025 Update | National Renewable Energy Laboratory | 4-h Li-ion BESS power/energy capex, ~85% RTE, 15-yr life (Table 1; §4.1, §4.4) | 2026-06-30 | https://doi.org/10.2172/2503498 |
| [15] NREL (2024) | 2024 Annual Technology Baseline: Utility-Scale PV | National Renewable Energy Laboratory | PV CAPEX/O&M and capacity-factor benchmark; BESS cross-check (Table 1; §4.1) | 2026-06-30 | https://atb.nrel.gov/electricity/2024/utility-scale_pv |
| [16] Lazard (2025) | 2025 Levelized Cost of Energy+ Report | Lazard | Cross-check ranges for LCOE across technologies (§5.3) | 2026-06-30 | https://www.lazard.com/media/uounhon4/lazards-lcoeplus-june-2025.pdf |
| [28] EIA (2024b) | Assumptions to the Annual Energy Outlook 2025: Electricity Market Module | U.S. Energy Information Administration | Financing baseline (~6.7% discount rate; CRF 0.0782) (§4.2) | 2026-06-30 | https://www.eia.gov/outlooks/aeo/assumptions/pdf/EMM_Assumptions.pdf |
| [27] EPA (2025) | Emission Factors for Greenhouse Gas Inventories (Jan. 2025 update) | U.S. Environmental Protection Agency | Natural-gas combustion CO₂ factor (53.06 kg CO₂/MMBtu) (§4.2; Eq. 4) | 2026-06-30 | https://www.epa.gov/system/files/documents/2025-01/ghg-emission-factors-hub-2025.pdf |
| [7] DOE (2024b) | Transmission Interconnection Roadmap (i2X) | U.S. Department of Energy | Queue-volume growth (~2,600 GW), time-to-interconnect (§1–2, §5.2) | 2026-06-30 | https://www.energy.gov/sites/default/files/2024-04/i2X%20Transmission%20Interconnection%20Roadmap.pdf |
| [29] ERCOT (2024) | ERCOT Interconnection Process: Generation Entity Winter Weather Preparedness | Electric Reliability Council of Texas | ERCOT interconnection timeline (18–30 months) (§5.2) | 2026-06-30 | https://www.ercot.com/files/docs/2024/10/30/0940-AM-ERCOT-Interconnection-Process-Generation-Entity-Winter-Weather-Preparedness-Fernandes.pdf |
| [30] NYISO (2023) | 2023 NYISO Interconnection Process Report | New York Independent System Operator | ISO interconnection process timelines (§5.2) | 2026-06-30 | https://www.nyiso.com/documents/20142/35688159/2023-NYISO-Interconnection-Process-Report.pdf |
| [9] DOE (2022) | DOE and Industry Team to Keep the Lights On in America | U.S. DOE, Office of Electricity | Distribution-transformer lead-time escalation (Table 2; §1–2) | 2026-06-30 | https://www.energy.gov/oe/articles/doe-and-industry-team-keep-lights-america |
| [11] DOE (2024c) | Large Power Transformer Resilience Report | U.S. Department of Energy | Large-power-transformer lead times (~36–60 months) (Table 2; §1–2, §6.3) | 2026-06-30 | https://www.energy.gov/sites/default/files/2024-10/EXEC-2022-001242%20-%20Large%20Power%20Transformer%20Resilience%20Report%20signed%20by%20Secretary%20Granholm%20on%207-10-24.pdf |
| [10] NIAC (2024) | Addressing the Critical Shortage of Power Transformers to Ensure Reliability of the U.S. Grid | National Infrastructure Advisory Council (via CISA) | Large-transformer lead times (80–210 weeks) (Table 2; §1–2, §6.3) | 2026-06-30 | https://www.cisa.gov/sites/default/files/2024-09/NIAC_Addressing%20the%20Critical%20Shortage%20of%20Power%20Transformers%20to%20Ensure%20Reliability%20of%20the%20U.S.%20Grid_Report_06112024_508c_pdf_0.pdf |
| [12] Reuters (2025) | Grid Equipment Makers Invest in U.S. to Ease Supply Shortage | Reuters | Wood Mackenzie Q2 2025: GSUs ~143 wk, power transformers ~128 wk (Table 2; §2.2) | 2026-06-30 | https://www.reuters.com/business/energy/grid-equipment-makers-invest-us-ease-supply-shortage--reeii-2025-12-02/ |
| [1] IEA (2025) | Energy and AI | International Energy Agency | Global data-center electricity consumption (~415 TWh 2024; ~945 TWh 2030) (§1) | 2026-06-30 | https://www.iea.org/reports/energy-and-ai |
| [4] DOE (2024a) | DOE Releases New Report Evaluating Increase in Electricity Demand from Data Centers | U.S. Department of Energy | U.S. data-center load-growth projections (§1) | 2026-06-30 | https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers |

*Note.* An earlier draft of this inventory also listed Bloom Energy (2024, 2025), Rand et al. (2024), and DOE (2024d, long-duration storage). Those sources are not cited in the submitted manuscript and have been removed from this inventory, consistent with the *Energies* rule that citations in supplementary files must also appear in the main text and reference list.

# NREL PVWatts V8 Request Parameters (Hourly Solar Profiles)

Hourly PV capacity-factor and ambient-temperature profiles for the eleven market archetypes were obtained from the NREL PVWatts V8 API (NSRDB PSM V3 typical-meteorological-year data; host `developer.nlr.gov`; NREL's developer domain transitioned from nrel.gov to nlr.gov on 29 May 2026, and existing API keys remained valid). PVWatts TMY output is deterministic: any valid key with identical parameters returns identical data. The pull script is provided in Supplementary Material S1 (`pull_pvwatts_profiles.py`); the API key is supplied via environment variable and is not part of the scientific record.

**Fixed system parameters (identical across all sites, so only climate varies):** system capacity 1,000 kW DC (normalizer); standard modules; single-axis tracking (array_type 2); tilt 0°; azimuth 180°; inverter efficiency 96%; ground coverage ratio 0.4; hourly timeframe; NSRDB dataset.

**Two documented configurations:**

| Configuration | DC/AC ratio | System losses | Role in manuscript |
|---|---|---|---|
| default | 1.2 | 14% | Headline (Table 4; realized CFs 0.147–0.238) |
| pv_sens | 1.3 | 11% | PV-assumption sensitivity (§4.6, §5.5; realized CFs 0.153–0.246) |

**Market archetype coordinates (public metro city centers — no facility location is identified):**

| Market | Latitude | Longitude | Grid region |
|---|---|---|---|
| Atlanta, GA | 33.749 | −84.388 | Southeast |
| Charlotte, NC | 35.227 | −80.843 | Southeast |
| Columbus, OH | 39.961 | −82.999 | PJM |
| Ashburn, VA | 39.045 | −77.487 | PJM |
| Jackson, MS | 32.299 | −90.185 | MISO-South |
| Portland, OR | 45.512 | −122.658 | Pacific NW |
| Philadelphia, PA | 39.953 | −75.165 | PJM |
| Phoenix, AZ | 33.448 | −112.074 | WECC |
| South Bend, IN | 41.683 | −86.250 | MISO |
| Houston, TX | 29.760 | −95.369 | ERCOT |
| Reno, NV | 39.530 | −119.814 | WECC |

# Peer-Reviewed Open-Access References

The following peer-reviewed, open-access references ground the method and findings in the scholarly literature on data-center energy demand, levelized-cost methodology, firming and storage economics, hourly carbon accounting, and interconnection. All are cited in the manuscript and appear in its consolidated reference list ([manuscript reference number] shown).

- [19] Arbabzadeh, M., Sioshansi, R., Johnson, J. X., & Keoleian, G. A. (2019). The role of energy storage in deep decarbonization of electricity production. *Nature Communications, 10,* 3413. https://doi.org/10.1038/s41467-019-11161-5
- [26] Brown, T., Hörsch, J., & Schlachtberger, D. (2018). PyPSA: Python for Power System Analysis. *Journal of Open Research Software, 6*(1), 4. https://doi.org/10.5334/jors.188
- [20] Comello, S., & Reichelstein, S. (2019). The emergence of cost effective battery storage. *Nature Communications, 10,* 2038. https://doi.org/10.1038/s41467-019-09988-z
- [8] Gorman, W., Mulvaney Kemp, J., Rand, J., Seel, J., Wiser, R., Manderlink, N., Kahrl, F., Porter, K., & Cotton, W. (2024). Grid connection barriers to renewable energy deployment in the United States. *Joule, 8*(12), 101791. https://doi.org/10.1016/j.joule.2024.11.008
- [2] Koomey, J. G. (2008). Worldwide electricity used in data centers. *Environmental Research Letters, 3*(3), 034008. https://doi.org/10.1088/1748-9326/3/3/034008
- [23] Miller, G. J., Novan, K., & Jenn, A. (2022). Hourly accounting of carbon emissions from electricity consumption. *Environmental Research Letters, 17*(4), 044073. https://doi.org/10.1088/1748-9326/ac6147
- [21] Petrollese, M. (2025). Levelized Cost of Storage (LCOS) of Battery Energy Storage Systems Deployed for Photovoltaic Curtailment Mitigation. *Energies, 18*(14), 3602. https://doi.org/10.3390/en18143602
- [22] Riepin, I., & Brown, T. (2024). On the means, costs, and system-level impacts of 24/7 carbon-free energy procurement. *Energy Strategy Reviews, 54,* 101488. https://doi.org/10.1016/j.esr.2024.101488
- [6] Siddik, M. A. B., Shehabi, A., & Marston, L. (2021). The environmental footprint of data centers in the United States. *Environmental Research Letters, 16*(6), 064017. https://doi.org/10.1088/1748-9326/abfba1
- [18] Tong, D., Farnham, D. J., Duan, L., Zhang, Q., Lewis, N. S., Caldeira, K., & Davis, S. J. (2021). Geophysical constraints on the reliability of solar and wind power worldwide. *Nature Communications, 12,* 6146. https://doi.org/10.1038/s41467-021-26355-z

The manuscript's remaining references (Hirth 2013 [17]; Masanet et al. 2020 [3]) are peer-reviewed but not open access; they are used for context, not as data inputs.

# Data Dictionary

Each model input, its source, units, base-case value, and its entry point in the Supplementary Material S1 code (`model_multisite.py`).

| Parameter | Source | Units | Base value | Code entry point (S1) |
|---|---|---|---|---|
| NGCC overnight capital cost | EIA (2024a) [13] | $/kW | 921 | TECH["ngcc"]["capex"] |
| NGCC fixed O&M | EIA (2024a) [13] | $/kW-yr | 15.51 | TECH["ngcc"]["fom"] |
| NGCC variable O&M | EIA (2024a) [13] | $/MWh | 3.33 | TECH["ngcc"]["vom"] |
| NGCC heat rate | EIA (2024a) [13] | Btu/kWh | 6,226 | TECH["ngcc"]["hr"] |
| NGCC economic life | EIA (2024b) [28] | years | 30 | TECH["ngcc"]["life"] |
| PV overnight capital cost | EIA (2024a) [13] / NREL (2024) [15] | $/kW | 1,502 | TECH["pv"]["capex"] |
| PV fixed O&M | EIA (2024a) [13] | $/kW-yr | 20.23 | TECH["pv"]["fom"] |
| Hourly PV capacity factor (per market) | NREL PVWatts V8 pull (this document) | fraction | 0.147–0.238 annual (default) | profiles CSV → solve_site(cf) |
| Hourly ambient temperature (per market) | NREL PVWatts V8 pull (this document) | °C | market-specific | profiles CSV → pue_load(tamb) |
| BESS power capital cost | Cole & Karmakar (2025) [14] | $/kW | 150 | TECH["bess"]["power_capex"] |
| BESS energy capital cost | Cole & Karmakar (2025) [14] | $/kWh | 280 | TECH["bess"]["energy_capex"] |
| BESS round-trip efficiency | Cole & Karmakar (2025) [14] | fraction | 0.85 | TECH["bess"]["eff_rt"] |
| BESS life | Cole & Karmakar (2025) [14] | years | 15 | TECH["bess"]["life"] |
| Discount rate (WACC) | EIA (2024b) [28] | fraction | 0.067 | R |
| Capital recovery factor | Derived (Eq. 2) | fraction | 0.0782 (30 yr) / 0.108 (15 yr) | crf() |
| Natural-gas CO₂ factor | EPA (2025) [27] | kg CO₂/MMBtu | 53.06 | CO2_KG_PER_MMBTU |
| Natural-gas price (base) | EIA (2024b) [28] | $/MMBtu | 4.00 | gas_price |
| Grid import price | Planning assumption | $/MWh | 35 | GRID_PRICE |
| Grid import cap | Scenario input | MW | 100 (base); swept in §5.6 | grid_max |
| Reserve margin | Planning assumption | fraction | 0.15 | RESERVE |
| PV firm-capacity credit | Planning assumption | fraction | 0.05 | PV_CREDIT |
| Storage firm-credit duration rule | Modeling convention | hours | 4 | BE == 4.0*BP |
| Value of lost load | Planning assumption | $/MWh | 5,000 | VOLL |
| Campus load (headline) | Planning assumption | MW | flat 200 | LOAD_MW |
| Campus load (sensitivity) | IT×PUE(T), IT=160 MW | MW | 193–198 mean | pue_load() |
| Temporal reduction | Modeling convention | rep. days | k-means k=12, seed 42, weights sum 365 | solve_site() |

# Notes on Data Access and Archiving

**Source-version pins (verified 5 August 2026).** Two cited sources are living documents whose URLs now serve newer editions than the ones used. (1) EIA EMM assumptions [27]: the value used (6.7% WACC, 60/40 debt/equity) is from the AEO2025 edition, verified verbatim ("the resulting discount rate with a 60/40 debt/equity split is 6.7% from 2024 through 2050"); the live URL now hosts the AEO2026 edition, which states 7.1%. The citation is to the AEO2025 edition as titled. (2) The model's BESS power/energy split (\$150/kW + \$280/kWh; 2.5% FOM) is a rounded modeling decomposition benchmarked to Cole & Karmakar [14], whose 2024 four-hour point is \$334/kWh total (\$372/kW power + \$241/kWh energy; 4% FOM; 85% RTE; 15-yr life). The model's implied four-hour total (\$1,270/kW) is about 5% below the report's, i.e., storage is priced slightly favorably, making the solar-entry thresholds conservative with respect to storage cost.

**Archival stability.** Government and laboratory reports (EIA, DOE, NREL, EPA) are periodically revised or relocated. The author recommends downloading and archiving a dated PDF of every source at submission and depositing the archive alongside the code so links remain verifiable through review and after publication. The `atb.nrel.gov` URL was re-verified as resolving on 31 July 2026.

**Code and data archive.** The model code, the hourly PVWatts profiles, the model output files, the verification harness, and the figure-generation scripts are deposited at Zenodo under the concept DOI https://doi.org/10.5281/zenodo.21803457, which always resolves to the most recent version. The release used to produce the results reported in the manuscript is version 1.0.0, https://doi.org/10.5281/zenodo.21803458. The development repository is at https://github.com/dutta-sweta/btm-hyperscale-multimarket (accessed on 5 August 2026). Code is released under the MIT license and the accompanying data under CC BY 4.0.

**Currency basis.** All monetary values are 2023 U.S. dollars unless otherwise noted, consistent with the EIA Annual Energy Outlook 2025 cost basis. Where sources report in a different vintage, values were not deflated; this simplification is noted in the manuscript limitations.

**ISO queue and interconnection data.** Interconnection timelines (ERCOT, NYISO) and queue statistics (DOE i2X; Gorman et al. 2024) reflect the most recent editions available as of the access date and are used for schedule context, not as model optimization inputs.

**Equipment lead-time data.** Transformer and GSU lead-time figures are drawn from agency reports and trade reporting (Wood Mackenzie via Reuters) and are first-order schedule constraints, not precise procurement quotes.

**Solar data vintage.** Profiles are typical-meteorological-year (TMY) composites — a screening choice appropriate for market-level comparison, not a specific calendar year; this is disclosed in the manuscript limitations (§6.5).
