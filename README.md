# The Slow Decay of Democracy

**Live:** https://vaibhavgit9210.github.io/decay-democracy/

Can democratic backsliding be detected in data — and does India show it? This project
calibrates a quantitative "decay detector" on three countries with a documented history
of slow democratic decay (**Hungary**, **Turkey**, **Venezuela**), checks that it stays
quiet on a healthy control (**Switzerland**), and then applies it to **India**.

## The verdict

**The hypothesis is supported.** The detector fires for India:

| Country | Peak → 2025 | Drop | Onset | Years below threshold | Fires? |
|---|---|---|---|---|---|
| Hungary | 0.766 (2009) → 0.315 | −0.451 | 2009 | 16 | 🔴 yes |
| Turkey | 0.502 (2004) → 0.110 | −0.392 | 2007 | 18 | 🔴 yes |
| Venezuela | 0.618 (1991) → 0.042 | −0.576 | 1997 | 27 | 🔴 yes |
| **India** | **0.593 (1998) → 0.260** | **−0.333** | **2013** | **17** | 🔴 **yes** |
| Switzerland (control) | 0.862 (2012) → 0.843 | −0.019 | — | 0 | 🟢 no |

India also matches the backslider *sequence*: freedom of expression & media fall first
(2014, −0.44 since), civil liberties and association next (2014–15), judicial
constraints last and least (2019, −0.16). Aligned at onset year, India's trajectory
closely shadows Hungary's.

Caveats (spelled out on the page): one expert-coded source family (though corroborated
by Freedom House and EIU downgrades), decay is reversible (Poland 2023–, Brazil), and
India's judiciary and elections remain far healthier than end-state autocracies.

## Method

- **Data:** [V-Dem v15 (2025)](https://v-dem.net) via
  [Our World in Data](https://ourworldindata.org/democracy) — six indices
  (liberal democracy, electoral democracy, freedom of expression, judicial constraints
  on the executive, civil liberties, freedom of association), best point estimates.
- **Detector** (thresholds borrowed from V-Dem's *Episodes of Regime Transformation*
  research): from the post-1990 peak of the liberal-democracy index, fire when
  (1) total decline ≥ 0.10 and (2) the index stays below `peak − 0.05` for ≥ 5
  consecutive years. Onset = start of the steepest 10-year fall.
- **Calibration discipline:** the detector must fire on all three reference cases and
  stay quiet on the control before it is allowed to score India.

## Reproduce

```bash
python3 analyze.py   # reads data/*.csv, writes analysis.json
```

`index.html` is a single self-contained file (no build step, no CDN, works offline);
the analysis JSON is embedded in it. Charts are hand-rolled inline SVG with hover
tooltips, a light/dark theme toggle (`?theme=light|dark` to force), and a table view.

## Files

- `index.html` — the data story (everything inline)
- `analyze.py` — detector + sequencing analysis
- `data/*.csv` — V-Dem index series for the five countries (via OWID, CC BY)

Built as a data-analysis exercise, not a political statement: the detector was frozen
on the reference cases before India's data was scored.
