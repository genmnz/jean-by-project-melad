# 🧪 qPCR & digital PCR

_Amplification and melt curves, RDML runs, droplet gating, uncertainty and relative quantification._

13 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`analyze_melt_curves`](#analyze_melt_curves) | What is each reaction's melting temperature, and does its melt show the product, an artifact, or no amplification? |
| [`bootstrap_cq`](#bootstrap_cq) | How tightly do one reaction's observations pin down its Cq, efficiency and fitted coefficients? |
| [`call_cq`](#call_cq) | What is each reaction's Cq and amplification efficiency, read off a fitted sigmoid under a named Cq definition? |
| [`check_qpcr_multiplex`](#check_qpcr_multiplex) | Which of these qPCR assays can be pooled in one reaction, and which pair clashes? |
| [`classify_droplets`](#classify_droplets) | Which population (NN, NP, PN, PP) does each two-channel ddPCR droplet belong to, under a fixed grid, k-means or a k-nearest-neighbour vote? |
| [`design_qpcr_assay`](#design_qpcr_assay) | Which primer pair and hydrolysis probe make a qPCR assay on this target, ranked by penalty? |
| [`gate_droplets`](#gate_droplets) | What is the template concentration in each ddPCR well, from the raw droplet amplitudes rather than the instrument's count? |
| [`melt_profile`](#melt_profile) | How does this molecule melt: the helicity curve, its Tm50, and the domains that melt together behind each HRM peak? |
| [`melting_temperature`](#melting_temperature) | What is this oligo's melting temperature in this buffer under this model, step by step? |
| [`propagate_uncertainty`](#propagate_uncertainty) | How uncertain is a reported qPCR quantity, given the uncertainty of each measurement in it, and which measurement contributes most? |
| [`quantify_dpcr`](#quantify_dpcr) | What is the absolute concentration of a target from digital PCR partition counts, with a confidence interval? |
| [`read_rdml_run`](#read_rdml_run) | What does an RDML export hold, and what are one run's curves, Cq values, melts and partition counts as tables? |
| [`simulate_taqman_curve`](#simulate_taqman_curve) | What amplification curve and Cq will a singleplex hydrolysis-probe qPCR assay draw, from its sequences and thermocycling programme? |

---

### analyze_melt_curves

**Analyze melt curves**: _What is each reaction's melting temperature, and does its melt show the product, an artifact, or no amplification?_

Melt curves to melting temperature, under any of THREE engines that answer different questions and none of which is a fallback for another. `plate` (RDML-Python) normalises, derives twice, calls the peaks of -dF/dT and CLASSIFIES them against the target's expected Tm into per-reaction verdicts — one peak in the window is the product, an extra peak is an artifact or a primer dimer, no peak at all is a reaction that did not amplify; it is the only engine that produces a verdict. `vertex` (MBmca diffQ) fits a quadratic near the extremum and reports its vertex, so the Tm is NOT one of the sampled temperatures — the only sub-grid answer. `curve` (qpcR) does no plate normalisation and gives no verdicts, but reports every melting peak with the AREA under it. Replicate spread travels with all three, because it describes the readings rather than the method.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The fluorescence falls as the duplex melts, so peaks of -dF/dT are melting transitions.
- The expected Tm is the target product's, when the plate engine is to give verdicts.

**Does not:**
- Only the plate engine gives verdicts; the vertex and curve engines report temperatures and areas.
- Two products melting within a degree read as one peak.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `melt_table` | string | **yes** |  |  | the melt table: a header row, first column the temperature and every other column one reaction's fluorescence. The same table the Melt tab takes. |
| `engine` | `"plate"` · `"vertex"` · `"curve"` |  | `"plate"` |  | which of the three engines runs. They answer DIFFERENT questions: `plate` is the only one that produces a verdict, `vertex` the only one whose Tm is not a sampled temperature, `curve` the only one that reports peak areas. Values: plate (Plate (RDML-Python) - normalise, classify, verdicts), vertex (Vertex (MBmca diffQ) - sub-grid Tm), curve (Per curve (qpcR) - peak areas). |
| `expected_tm` | number |  |  | 40–100 | the product's expected melting temperature, which is what turns a peak list into a verdict. Left unset, every peak is reported and none is classified - an honest absence rather than a guess. Read by the `plate` engine only, because it is the only one that classifies. In C. Only applies when engine is plate. |
| `extremum` | `"auto"` · `"min"` · `"max"` |  | `"auto"` |  | `vertex` only: which extremum the melt sits at. `auto` reads each curve's direction, because upstream assumes a signal that RISES with temperature and a solution-phase melt FALLS — on which the default walks to the far end of the curve and returns a plausible-looking wrong Tm. Only applies when engine is vertex. |
| `window_ceiling` | number |  | `8` | 2–20 | `vertex` only: the largest neighbourhood half-width the quadratic is tried at. Every width from 2 up to this is fitted and the one with the best adjusted R-squared wins, so the Tm arrives with the fit quality that chose it. Only applies when engine is vertex. |
| `second_derivative` | boolean |  | `false` |  | `vertex` only: locate the inflection points of the melt (diffQ2) rather than the peak of the first derivative. Only applies when engine is vertex. Advanced. |
| `all_peaks` | boolean |  | `false` |  | `vertex` only: report every peak the curve carries, not the dominant one alone. Only applies when engine is vertex. Advanced. |
| `resample` | boolean |  | `false` |  | `vertex` only: resample the curve onto an even temperature grid before differentiating. Only applies when engine is vertex. Advanced. |
| `span_smooth` | number |  | `0.05` | 0.005–0.5 | `curve` only: the smoothing span of the cubic spline fitted before the analytic derivative. Only applies when engine is curve. Advanced. |
| `span_peaks` | number |  | `51` | 3–201 | `curve` only: the span Friedman's super smoother uses when the peaks are called. Only applies when engine is curve. Advanced. |
| `cut_area` | number |  | `0` | 0–1 | `curve` only: drop peaks whose area is under this fraction of the largest. 0 keeps every peak, which is upstream's own default. Only applies when engine is curve. Advanced. |
| `replicate_percent` | boolean |  | `true` |  | report replicate spread as a PERCENTAGE of the mean rather than in degrees. Advanced. |
| `replicate_robust` | boolean |  | `false` |  | replicate spread as median and MAD rather than mean and SD. Engine-independent: it describes the readings, so every run carries it. Advanced. |
| `true_peak_width` | number |  | `1` | 0.1–10 | `plate` only: half-width of the window around `expected_tm` a peak must fall in to count as the product. In C. Only applies when engine is plate. Advanced. |
| `expo_low_temp` | number |  | `65` | 40–100 | `plate` only: low end of the window the EXPONENTIAL background is fitted over. In C. Only applies when norm_method is exponential or combined. Advanced. |
| `expo_high_temp` | number |  | `92` | 40–100 | `plate` only: high end of the exponential fit window. In C. Only applies when norm_method is exponential or combined. Advanced. |
| `bilin_low_start_temp` | number |  | `65` | 40–100 | `plate` only: start of the LOW seed window the bilinear background is fitted from. In C. Only applies when norm_method is bilinear or combined. Advanced. |
| `bilin_low_stop_temp` | number |  | `67` | 40–100 | `plate` only: end of the low seed window. In C. Only applies when norm_method is bilinear or combined. Advanced. |
| `bilin_high_start_temp` | number |  | `93` | 40–100 | `plate` only: start of the high seed window. NARROWER THAN IT LOOKS, and upstream's own quirk reproduced: the high baseline scan walks a hard-coded 90-91 C seed, so this knob feeds ONLY the first exponential-free fit and moves the result far less than the low window does. The windows actually chosen come back in the result. In C. Only applies when norm_method is bilinear or combined. Advanced. |
| `bilin_high_stop_temp` | number |  | `94` | 40–100 | `plate` only: end of the high seed window — same narrow effect as its start, for the same reproduced reason. In C. Only applies when norm_method is bilinear or combined. Advanced. |
| `norm_method` | `"exponential"` · `"bilinear"` · `"combined"` |  | `"exponential"` |  | `plate` only: how each curve is normalised before it is derived. Only applies when engine is plate. Advanced. |
| `fluor_source` | `"normalised"` · `"smooth"` |  | `"normalised"` |  | `plate` only: which matrix a peak's fluorescence drop is read from — the normalised curve or the smoothed raw one. Only applies when engine is plate. Advanced. |
| `artifact_peak_width` | number |  | `1` | 0.1–10 | `plate` only: half-width used when an extra peak is measured as an artifact. In C. Only applies when engine is plate. Advanced. |
| `peak_low_temp` | number |  | `60` | 40–100 | `plate` only: lowest temperature a peak is looked for at. In C. Only applies when engine is plate. Advanced. |
| `peak_high_temp` | number |  | `98` | 40–100 | `plate` only: highest temperature a peak is looked for at. In C. Only applies when engine is plate. Advanced. |
| `peak_max_width` | number |  | `5` | 0.5–30 | `plate` only: widest a peak may be before it is not read as one product. In C. Only applies when engine is plate. Advanced. |
| `peak_cutoff` | number |  | `5` | 0–100 | `plate` only: the height a candidate must reach, as a percentage of the largest peak. In %. Only applies when engine is plate. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `reactions` | any |  | one row per reaction, in the shape the CHOSEN engine reports: `plate` gives peaks plus a verdict, `vertex` gives the sub-grid Tm with the adjusted R-squared that chose its window, `curve` gives every peak with its area |
| `count` | number |  | how many reactions were analysed |
| `meanTm` | number | °C | mean dominant Tm over the reactions that produced a peak |
| `noPeak` | number |  | reactions with no melting peak at all: a reaction that did not amplify, reported rather than dropped |
| `classified` | string |  | whether the peaks were classified, and why not when they were not — including 'this engine does not classify', which is a property of the choice and not a failure |
| `engine` | string |  | which engine produced these rows, named: the three answer different questions and a Tm without its engine is not comparable |
| `replicateSpread` | any |  | location and deviation per temperature per target, from the plate's own replicates. Engine-independent: it describes the readings, not the method, so every run carries it |
| `targets` | any |  | `plate` only: per target, the reactions that contributed a product peak and their averaged Tm against the expected one. Empty for `vertex` and `curve` |
| `meltPlot` | object or null |  | the melt curves as read from the table, one line per reaction, fluorescence against temperature. Every engine reads this same input |
| `meltPlot.x` | number[] |  |  |
| `meltPlot.series` | object[] |  |  |
| `meltPlot.series[].name` | string |  |  |
| `meltPlot.series[].y` | (number or null)[] |  |  |
| `meltPlot.xLabel` | string |  |  |
| `meltPlot.yLabel` | string |  |  |
| `meltPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `meltPlot.title` | string |  |  |
| `meltPlot.rules` | object[] |  |  |
| `meltPlot.rules[].y` | number |  |  |
| `meltPlot.rules[].label` | string |  |  |
| `derivativePlot` | object or null |  | `plate` only: −dF/dT of each reaction after normalisation and smoothing, the curve its peaks are called on, one line per reaction. Null for `vertex` and `curve`, which fit near the extremum and report no whole derivative |
| `derivativePlot.x` | number[] |  |  |
| `derivativePlot.series` | object[] |  |  |
| `derivativePlot.series[].name` | string |  |  |
| `derivativePlot.series[].y` | (number or null)[] |  |  |
| `derivativePlot.xLabel` | string |  |  |
| `derivativePlot.yLabel` | string |  |  |
| `derivativePlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `derivativePlot.title` | string |  |  |
| `derivativePlot.rules` | object[] |  |  |
| `derivativePlot.rules[].y` | number |  |  |
| `derivativePlot.rules[].label` | string |  |  |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "analyze_melt_curves",
  "arguments": {
    "melt_table": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### bootstrap_cq

**Bootstrap Cq**: _How tightly do one reaction's observations pin down its Cq, efficiency and fitted coefficients?_

Resampling error bars on ONE reaction's Cq. A Cq is read off a fitted model, so its uncertainty is how tightly the observations pin that model down - which propagating a measured spread cannot answer. This refits the curve a few hundred times, either by resampling its residuals or by leaving observations out, and reports the spread of everything the fit produces: every model coefficient, the Cq under each definition, the efficiency and the initial fluorescence, each with the quantiles of the iterations rather than a normal approximation, so an asymmetric interval means the estimate genuinely is asymmetric. Reproduces qpcR 1.4.2's `pcrboot`.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- Residuals are exchangeable (residual resampling) or observations can be left out without changing the curve's shape.

**Does not:**
- Measures fitting uncertainty in one reaction, not variation between replicate reactions.

**Not read from this result:** The Curve tab's bootstrap section shows the resampled intervals as a table with no sentence over them; the quantiles are the answer, and a reading composed here would be one nobody reviewed.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `curves` | string | **yes** |  |  | the amplification table: a header row, first column the cycle number and every other column one reaction's fluorescence. The same parser `call_cq` and the Curve->Cq tab use. |
| `reaction` | string |  | `""` |  | which reaction to resample, by its column name. Blank takes the first column — this is a per-reaction run by design, because at the default 200 iterations a 47-reaction plate would be 9,400 refits nobody asked for. |
| `model` | `"l4"` · `"l5"` · `"l6"` · `"l7"` · `"b4"` · `"b5"` · `"b6"` · `"b7"` |  | `"l4"` |  | the sigmoid fitted once and REFITTED on every iteration. It is not re-chosen per resample: Cqs fitted under different models are not comparable, so a mixture over models would make the quantiles mean nothing. Values: l4 (l4 · 4-param log-logistic), l5 (l5 · + asymmetry), l6 (l6 · + linear baseline drift), l7 (l7 · + quadratic baseline), b4 (b4 · 4-param logistic (raw scale)), b5 (b5 · + asymmetry), b6 (b6 · + linear baseline drift), b7 (b7 · + quadratic baseline). |
| `cq_method` | `"cpD2"` · `"cpD1"` · `"maxE"` · `"expR"` · `"Cy0"` · `"CQ"` · `"maxRatio"` |  | `"cpD2"` |  | which Cq definition the resampled efficiency readouts report. Values: cpD2 (cpD2 · second-derivative max), cpD1 (cpD1 · first-derivative max), maxE (maxE · cycle of maximum efficiency), expR (expR · exponential region), Cy0 (Cy0 · tangent x-intercept (Guescini)), CQ (CQ · 20 % of the Cq fluorescence), maxRatio (maxRatio · spline, model-free (Shain)). |
| `scheme` | `"boot"` · `"jack"` |  | `"boot"` |  | `boot` resamples the fit's residuals (upstream's default); `jack` leaves observations out. The bootstrap answers "how would this Cq move under the same noise?", the jackknife "how much does any single cycle carry it?". |
| `iterations` | number |  | `200` | 20–2000 | each iteration is a full nonlinear refit, so this is the run's whole cost. 100 is upstream's default and puts a 95 % bound on a single order statistic, which is why both doors open on 200. |
| `drop` | number |  | `1` | 1–10 | jackknife only: observations left out of each refit. 1 is the delete-one jackknife; more is a delete-d jackknife, which is less sensitive to a single influential cycle. Only applies when scheme is jack. |
| `conf_level` | number |  | `0.95` | 0.5–0.999 | the level the reported bounds are read at — 0.95 puts them at the 2.5 % and 97.5 % quantiles of the iterations. |
| `include_readouts` | boolean |  | `true` |  | also resample every efficiency readout — the Cq definitions, the efficiency, the initial fluorescence — not just the model coefficients. On, because an interval on the Cq is the point; off is faster and returns coefficients alone. Advanced. |
| `seed` | number |  | `1` | ≥ 1 | R's `set.seed` value, so the interval is reproducible and citable. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `reaction` | string |  | the reaction actually resampled, named — "the first column" is not a citation |
| `model` | string |  | the model refitted on every iteration |
| `readouts` | any |  | one row per resampled readout — Cq under each definition, efficiency, initial fluorescence — with mean, SD, median and the interval quantiles. Empty when `include_readouts` is off |
| `coefficients` | any |  | one row per model coefficient, in the model's own parameter order, same fields |
| `converged` | number |  | iterations whose refit converged — the ONLY ones any number here is computed from. Well below `iterations` is a finding about the curve, not a warning to swallow |
| `iterations` | number |  | iterations requested |
| `confLevel` | number |  | the level the bounds above are read at |
| `rmse` | any |  | residual standard error across the iterations |
| `rss` | any |  | residual sum of squares across the iterations |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "bootstrap_cq",
  "arguments": {
    "curves": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### call_cq

**Call Cq**: _What is each reaction's Cq and amplification efficiency, read off a fitted sigmoid under a named Cq definition?_

Amplification curves to Cq, one row per reaction. Fits each raw fluorescence curve to a sigmoid (l4-l7, b4-b7), reads the Cq off it under any of the seven definitions (cpD1, cpD2, maxE, expR, Cy0, CQ, maxRatio) or at a fluorescence threshold you set (the classic Ct), and returns the per-reaction efficiency and the fit-quality block beside it, so a bad fit is visible next to the Cq it produced rather than hidden behind it. Also reports the two exponential-phase locators (Tichopad take-off, model midpoint), which come back null rather than 0 when a curve has no exponential phase at all.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The sigmoid model chosen (or selected by the criterion) fits the curve; the fit-quality block says how well.
- The baseline window holds no amplification.

**Does not:**
- Different Cq definitions give different numbers; compare Cqs only under one definition.
- A curve with no exponential phase gives null locators, not a Cq of zero.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `curves` | string | **yes** |  |  | the amplification table: a header row, first column the cycle number and every other column one reaction's fluorescence. Tab- or comma-separated, and read by the same parser the Curve->Cq tab uses. |
| `model` | `"l4"` · `"l5"` · `"l6"` · `"l7"` · `"b4"` · `"b5"` · `"b6"` · `"b7"` |  | `"l4"` |  | which sigmoid is fitted before a Cq is read off it. Ignored when `auto_model` is on, except as the starting point mselect ranks from. Values: l4 (l4 · 4-param log-logistic), l5 (l5 · + asymmetry), l6 (l6 · + linear baseline drift), l7 (l7 · + quadratic baseline), b4 (b4 · 4-param logistic (raw scale)), b5 (b5 · + asymmetry), b6 (b6 · + linear baseline drift), b7 (b7 · + quadratic baseline). |
| `cq_method` | `"cpD2"` · `"cpD1"` · `"maxE"` · `"expR"` · `"Cy0"` · `"CQ"` · `"maxRatio"` |  | `"cpD2"` |  | which Cq definition. These are genuinely different quantities, not one number under several names. Values: cpD2 (cpD2 · second-derivative max), cpD1 (cpD1 · first-derivative max), maxE (maxE · cycle of maximum efficiency), expR (expR · exponential region), Cy0 (Cy0 · tangent x-intercept (Guescini)), CQ (CQ · 20 % of the Cq fluorescence), maxRatio (maxRatio · spline, model-free (Shain)). |
| `auto_model` | boolean |  | `false` |  | let the plate choose its own model. mselect runs on the FIRST reaction and its winner is applied to every reaction, because Cqs fitted under different models are not comparable — the result reports which model won and the full ranking table. |
| `criterion` | `"ftest"` · `"ratio"` · `"weights"` · `"chisq"` |  | `"ftest"` |  | how auto_model ranks. The nested tests are only meaningful inside one family (l4-l7 or b4-b7); AICc weights is the one that can rank all eight. The reduced chi-square needs a measurement error per cycle and the only honest source is the plate's own replicates, so it REFUSES a plate with none. Values: ftest (Nested F-test (within family)), ratio (Likelihood ratio (within family)), weights (AICc weights (all eight models)), chisq (Reduced chi-square (needs replicates)). Only applies when auto_model is true. |
| `outlier_method` | `"uni1"` · `"uni2"` · `"multi1"` · `"multi2"` · `"multi3"` |  | `"uni2"` |  | which kinetic-outlier test judges the reaction shapes. Two are univariate and three judge a curve's whole shape against a robust MCD covariance of the plate, so a plate can look clean under one and dirty under another. Values: uni1 (Efficiency Z-score (Bar)), uni2 (Shape: cpD1 − cpD2 (Tichopad)), multi1 (Multivariate: cpD1 vs cpD2 residual (Tichopad MOD1)), multi2 (Multivariate: slope, Fmax (Tichopad MOD2)), multi3 (Multivariate: slope, F at cpD1, Fmax (Sisti)). Advanced. |
| `baseline_from` | number |  | `1` | 1–40 | first cycle of the window the sliwin and LRE estimators scan a baseline over. Affects the all-methods table only: the sigmoidal fit and its Cq do not use a baseline scan. In cycle. Advanced. |
| `baseline_to` | number |  | `8` | 1–40 | last cycle of that window. In cycle. Advanced. |
| `baseline_scan` | number |  | `1` | 0–10 | how many SDs of offset the baseline scan searches; 0 subtracts nothing, which is upstream's own default and is WRONG on real instrument data. Measured against the real LinRegPCR over the 47 reactions of the bundled Own Mix B plate: scanning gives a median efficiency disagreement of 0.038, not scanning gives 0.460. The result reports what the other setting would have returned, so the choice is never hidden. In SD. Advanced. |
| `shift` | number |  | `0` | -10–10 | cycles added to every reported Cq, for aligning against an instrument's own numbering. Advanced. |
| `threshold` | number |  |  |  | a fluorescence threshold, on the plate's own fluorescence scale. Set, every Cq is the cycle where the fitted curve crosses it (the classic threshold cycle, Ct) and `cq_method` is overridden. Blank reads the Cq under `cq_method`. A reaction that never reaches it has no Cq and says so. |
| `amounts` | string |  |  |  | the known template amount of each reaction, in column order (comma- or space-separated, `-` for a reaction with none). Each reaction given one reports its calibration factor `cf`, the amount over `init1`, the fit's fluorescence at cycle 0, which is what an absolute quantification scales an unknown's `init1` by. Advanced. |
| `max_ratio_baseshift` | number |  | `0` |  | fluorescence added to every cycle before the maxRatio spline is drawn. qpcR's own remedy when a baseline near zero makes the cycle-to-cycle ratio explode; it moves only the `maxRatio` Cq. Only applies when cq_method is maxRatio. Advanced. |
| `max_ratio_smooth` | boolean |  | `false` |  | smooth the raw curve before the maxRatio spline is drawn, as qpcR's `eff(smooth = TRUE)` does. Moves only the `maxRatio` Cq. Only applies when cq_method is maxRatio. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rows` | any |  | one row per reaction: Cq, cpD1, cpD2, efficiency, the fit-quality block, take-off and midpoint, the initial fluorescence two ways (`init1` the fit at cycle 0, `init2` the fluorescence at the Cq over E^Cq), and `cf`, the known amount over `init1` for a reaction given one (NaN otherwise) |
| `count` | number |  | how many reactions were fitted |
| `failed` | number |  | reactions whose fit did not converge. A non-zero count is a finding about the plate, not a warning to swallow |
| `meanEfficiency` | number | % | mean per-reaction efficiency over the reactions that fitted, as a percentage |
| `model` | string |  | the model that produced these Cqs, named: a Cq without its model is not comparable, and under `auto_model` this is the one that WON rather than the one you asked for |
| `cqMethod` | string |  | the Cq definition used: `cpT` when a `threshold` was set, since a threshold overrides `cq_method` |
| `modelTable` | any |  | the full model ranking when `auto_model` chose one — logLik, AIC, AICc, residual variance, F test, likelihood ratio, AICc weight and reduced chi-square per model. Null when the model was given rather than chosen |
| `methods` | any |  | the all-methods table: the same reactions measured four independent ways (sigmoidal fit, sliwin, expfit, LRE) with each failure NAMED, plus what sliwin returns under the other baseline setting. Agreement between them is the evidence a well is clean |
| `outliers` | any |  | the kinetic-outlier verdicts, including the reactions the test could not MEASURE — reported as not judged with the reason, never as passing |
| `outlierStat` | string |  | which statistic judged them, or the refusal when the plate could not support the test |
| `zeroCrossing` | any |  | reactions whose fluorescence crosses zero after `max_ratio_baseshift` is added, where the spline estimators put a pole in the series and would return a confident 1e16. Named rather than printed |
| `threshold` | number or null |  | the fluorescence threshold every Cq was read at; null when the Cq came from `cq_method` instead |
| `modelChosen` | string or null |  | the curve model the ranking chose when the model was not given; null when it was given |
| `errorNote` | string or null |  | a plate-level note from the fit (for example a reaction the model could not fit); null when there is none |
| `amplificationPlot` | object or null |  | the raw amplification curves as read from the plate, one line per reaction, fluorescence against cycle |
| `amplificationPlot.x` | number[] |  |  |
| `amplificationPlot.series` | object[] |  |  |
| `amplificationPlot.series[].name` | string |  |  |
| `amplificationPlot.series[].y` | (number or null)[] |  |  |
| `amplificationPlot.xLabel` | string |  |  |
| `amplificationPlot.yLabel` | string |  |  |
| `amplificationPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `amplificationPlot.title` | string |  |  |
| `amplificationPlot.rules` | object[] |  |  |
| `amplificationPlot.rules[].y` | number |  |  |
| `amplificationPlot.rules[].label` | string |  |  |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "call_cq",
  "arguments": {
    "curves": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### check_qpcr_multiplex

**Check qPCR multiplex**: _Which of these qPCR assays can be pooled in one reaction, and which pair clashes?_

Can these qPCR assays share a tube? Every unordered pair is scored on MultiPLX's five primer-primer and primer-product interactions and, beyond MultiPLX, on each assay's hydrolysis PROBE against the other assay's oligos (primer3 thal) — a probe consumed by a neighbour's primer loses signal while the PCR works perfectly, which reads as poor efficiency and is blamed on the primers. Returns the pairs that clash with the cutoffs they break, and the assays that clash with nothing.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- MultiPLX's interaction model: the tube holds both assays' primers and their products.
- Probe interactions are primer3's thal under the same conditions, which is an addition to MultiPLX rather than its output.

**Does not:**
- Pairwise: an assay compatible with two others and not the third cannot be pooled, and the pair is named.
- A missing amplicon leaves the two primer-product scores unmeasurable, and that is reported rather than passed.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `assays` | object[] | **yes** |  |  | the assays to pool: one object per assay with `name`, `forward`, `reverse`, `probe` and `amplicon`. Wire `design_qpcr_assay` outputs here, or list them yourself. Without `amplicon` the two primer-product scores cannot be measured and say so. |
| `stringency` | `"primer3"` · `"high"` · `"normal"` · `"low"` |  | `"primer3"` |  | whose cutoffs decide. `primer3` judges on the Tm limits calibrated for the engine that computes them, which is what the panel opens on; the other three are MultiPLX's own presets, verbatim from cmultiplx 1.4. Values: primer3 (primer3 limits (the engine's own)), high (MultiPLX high stringency), normal (MultiPLX normal), low (MultiPLX low). |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method every interaction is measured in. Left unset it is filled from your reaction-conditions settings, and falls back to primer3's defaults when there are none. Advanced. |
| `conditions.Na` | number |  |  | ≥ 0 | Na⁺ [mM]. In mM. |
| `conditions.K` | number |  |  | ≥ 0 | K⁺ [mM]. In mM. |
| `conditions.Tris` | number |  |  | ≥ 0 | Tris buffer [mM]. In mM. |
| `conditions.Mg` | number |  |  | ≥ 0 | Mg²⁺ [mM]. In mM. |
| `conditions.dNTPs` | number |  |  | ≥ 0 | total dNTPs [mM]. In mM. |
| `conditions.dnac1` | number |  |  | ≥ 0 | primer / higher-concentration strand [nM]. In nM. |
| `conditions.dnac2` | number |  |  | ≥ 0 | template / other strand [nM]. In nM. |
| `conditions.saltcorr` | number |  |  | 0–7 | Biopython salt-correction method 0–7 (0 = none). It moves the answer more than any other knob here: on a 24-mer at the Taq buffer the eight span 79.302 °C (method 0) to 66.009 °C (method 2). |
| `conditions.selfcomp` | boolean |  |  |  | both strands are one self-complementary oligo (the concentration term becomes dnac1 rather than dnac1 − dnac2/2). |
| `conditions.method` | `"santaLucia"` · `"dbd"` |  |  |  | which validated nearest-neighbour model and default buffer — santaLucia (pydna `tm_default`, Taq) or dbd (pydna `tm_dbd`, Phusion / Pfu-Sso7d). Values: santaLucia (SantaLucia (pydna tm_default, Taq)), dbd (DNA-binding domain (pydna tm_dbd, Phusion)). |
| `conditions.nnTable` | string |  |  |  | override the method's nearest-neighbour table; the buffer convention is unchanged. |
| `conditions.additives` | object |  |  |  | DMSO and formamide, applied AFTER the nearest-neighbour Tm. |
| `conditions.additives.DMSO` | number |  |  | 0–100 | DMSO [% v/v]. In %. |
| `conditions.additives.fmd` | number |  |  | ≥ 0 | formamide — percent when `fmdmethod` is 1, molar when it is 2. |
| `conditions.additives.dmsoMethod` | `"ahs01"` · `"mus81"` · `"cul76"` · `"esc80"` |  |  |  | which published DMSO depression sets the coefficient. Values: ahs01 (Ahsen et al. (2001) (0.75 °C per %)), mus81 (Musielski et al. (1981) (0.6 °C per %)), cul76 (Cullen and Bick (1976) (0.5 °C per %)), esc80 (Escara and Hutton (1980) (0.675 °C per %)). |
| `conditions.additives.DMSOfactor` | number |  |  | ≥ 0 | °C of Tm lost per % DMSO, as an explicit override. Supplying it WINS over `dmsoMethod`, and detaches the number from its citation. |
| `conditions.additives.fmdfactor` | number |  |  | ≥ 0 | °C lost per % formamide (method 1). Papers report 0.6 to 0.72. |
| `conditions.additives.fmdmethod` | `1` · `2` |  |  |  | 1 = linear % formamide (McConaughy 1969) · 2 = GC-dependent, molar (Blake & Delcourt 1996). Values: 1 (Linear %, McConaughy 1969), 2 (GC-dependent molar, Blake & Delcourt 1996). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `pairs` | any |  | every unordered pair: its five MultiPLX scores, its probe interactions, the cutoffs it breaks, whether it is compatible, and why not in words |
| `compatible` | any |  | assay names that clashed with nothing — the ones that can be pooled |
| `conflicting` | any |  | assay names involved in at least one clash |
| `poolable` | boolean |  | true when NO pair clashes, so the whole set can go in one tube. Branch a workflow on this rather than counting the rows |
| `cutoffs` | any |  | the cutoff set the verdicts were judged against, so a report says what it means by compatible |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_qpcr_multiplex",
  "arguments": {
    "assays": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### classify_droplets

**Classify droplets**: _Which population (NN, NP, PN, PP) does each two-channel ddPCR droplet belong to, under a fixed grid, k-means or a k-nearest-neighbour vote?_

ddPCR droplet amplitudes to populations. For TWO targets, a four-way classification — NN, NP, PN, PP — under any of THREE published methods that answer different questions and none of which is a fallback for another. `grid` applies eight fixed thresholds: reproducible and auditable, the only one that does not move when the data does, and the only one that needs someone to have chosen the numbers. `kmeans` clusters both channels at once and names the clusters by where they sit, so it adapts to the well, and it CANNOT abstain because k-means partitions everything. `knn` classifies against a well you have already labelled and abstains into `Rain` when the neighbour vote is weaker than a floor you set, so it is the only one that can decline per droplet. They disagree on the droplets between the populations, and that disagreement is the honest measure of how much an answer rests on the method rather than on the data. Distinct from `gate_droplets`, which asks whether a droplet is EMPTY per channel and ends in a concentration; this asks which of four populations it belongs to. For ONE to FOUR targets multiplexed by amplitude, ddPCRclust names up to sixteen populations from the primary clusters and reports each target's copies per droplet, by any of three first clusterings or their consensus: `density` places the primaries from density gates, `samspectral` from spectral clustering of a faithful sample, `flowpeaks` from the density peaks k-means clusters climb to, and `ensemble` (ddPCRclust's own default) runs all three and keeps the partition that agrees most with the others, with their mean corrected Rand index as the confidence. A plate of exports with ddPCRclust's run template is classified well by well and can be normalised to a constant control.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The four populations sit where the method expects them: at the grid's thresholds, as k-means clusters, or near a labelled training well's.

**Does not:**
- The methods disagree on droplets between populations; that disagreement measures how much the answer rests on the method.
- Only k-nearest-neighbours can abstain (Rain); k-means partitions everything.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `droplets` | string | **yes** |  |  | the well to classify: two amplitude columns, `Ch1` then `Ch2`, one row per droplet. A header line is optional. This is the whole well, not a summary. For the ddPCRclust methods it may instead be a PLATE: each export as `# <file name>` then its CSV, separated by a line of `---`, the well id read from the file name (`..._B01_Amplitude.csv`). |
| `method` | `"grid"` · `"kmeans"` · `"knn"` · `"density"` · `"samspectral"` · `"flowpeaks"` · `"ensemble"` |  | `"kmeans"` |  | which classifier. `grid` needs its eight thresholds to suit your assay; `kmeans` needs nothing and cannot abstain; `knn` needs `training` and is the only one that can leave a droplet unassigned; `density`, `samspectral`, `flowpeaks` and `ensemble` (ddPCRclust) are for one to four targets and name populations by marker number (`1`, `1+2`, ...); `ensemble` runs the other three and is the slowest. |
| `markers` | string |  | `"M1,M2,M3,M4"` |  | for `density`: the well's four marker slots, comma-separated, as in ddPCRclust's run template. A name is a target the reaction carries; an EMPTY slot is one it does not, so `a,,c,d` is a three-target well whose cluster 2 is missing. The number of names is the number of targets. Only applies when method is density or samspectral or flowpeaks or ensemble. |
| `sensitivity` | number |  | `1` | 0.1–2 | for `density`: how finely the initial cluster search resolves density peaks (its step is 0.02 / sensitivity³). Higher divides the data into more clusters, lower merges more. Only applies when method is density or samspectral or flowpeaks or ensemble. |
| `distance_param` | number |  | `0.2` | 0–1 | for `density`: the share of the path between two clusters within which rain goes to the LOWER one; the rest goes to the higher one. Only applies when method is density or samspectral or flowpeaks or ensemble. |
| `sam_seed` | number |  | `1` | 1–2147483647 | for `samspectral` and `ensemble`: R's `set.seed` before the run. SamSPECTRAL keeps the best of 1000 k-means starts drawn from it, and on a plate one stream runs through the wells in order, as `ddPCRclust()` does. Only applies when method is samspectral or ensemble. |
| `template` | string |  |  |  | for a PLATE under the ddPCRclust methods: ddPCRclust's run template (a `>name, channel1=..., channel2=..., description` line, then `Well,Sample type,# of markers,Marker 1..Marker 4`). Each well then takes its own row's markers instead of `markers`. Only applies when method is density or samspectral or flowpeaks or ensemble. |
| `constant_control` | string |  | `""` |  | for a PLATE under the ddPCRclust methods: the marker that should read the same in every well. Every well's copies per droplet are multiplied by the control's highest value on the plate over its own, as `calculateCPDs(constantControl =)` does. Empty: no normalisation. Only applies when method is density or samspectral or flowpeaks or ensemble. |
| `training` | string |  |  |  | for `knn` only: an already-labelled well, as `Ch1,Ch2,class` with class one of NN, NP, PN, PP or Rain. Rain IS a class here and not a rejection — a droplet can be assigned to it on the strength of its neighbours, separately from the probability floor below. Only applies when method is knn. |
| `k` | number |  | `5` | 1–999 | for `knn`: how many nearest labelled neighbours vote. Only applies when method is knn. |
| `prob` | number |  | `0` | 0–1 | for `knn`: the smallest winning share of the vote that counts as a call. Below it the droplet is `Rain`. 0 disables the floor. At k = 5 a bare 3-2 majority is 0.6, so any floor at or below 0.5 accepts every droplet the vote decided at all. Only applies when method is knn. |
| `ch1_nn` | number |  | `6500` | 0–100000 | grid: Ch1 below this and Ch2 below `ch2_nn` is NN. Only applies when method is grid. |
| `ch2_nn` | number |  | `1900` | 0–100000 | grid: the Ch2 half of the NN box. Only applies when method is grid. |
| `ch1_np` | number |  | `6500` | 0–100000 | grid: Ch1 below this and Ch2 above `ch2_np` is NP. Only applies when method is grid. |
| `ch2_np` | number |  | `5000` | 0–100000 | grid: the Ch2 half of the NP box. Only applies when method is grid. |
| `ch1_pn` | number |  | `10000` | 0–100000 | grid: Ch1 above this and Ch2 below `ch2_pn` is PN. Only applies when method is grid. |
| `ch2_pn` | number |  | `2900` | 0–100000 | grid: the Ch2 half of the PN box. Only applies when method is grid. |
| `ch1_pp` | number |  | `7500` | 0–100000 | grid: Ch1 above this and Ch2 above `ch2_pp` is PP. Only applies when method is grid. |
| `ch2_pp` | number |  | `5000` | 0–100000 | grid: the Ch2 half of the PP box. Only applies when method is grid. |
| `random_seed` | number |  | `8` | 1–2147483647 | for `knn`: ties among equidistant neighbours, and among tied winning classes, are broken from this stream. On a well-separated plate it changes nothing; where droplets sit exactly between populations it does, and a deterministic tie-break would be stable and wrong. Only applies when method is knn. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `classes` | any |  | one label per droplet, in the order given: NN, NP, PN, PP, or Rain where the method abstained |
| `counts` | any |  | droplets per class, which is what a copy-number read consumes next. Rain is reported separately and is never folded into a population |
| `total` | number |  | droplets classified — the denominator the counts sum to |
| `method` | string |  | which classifier produced this. A classification without its method is not comparable with another, because the three disagree on the droplets between populations |
| `centres` | any |  | for `kmeans`: the final cluster centres with the name geometry gave each one; for `density`: the primary cluster centres, named by marker. Empty for the other methods, which have no centres |
| `params` | any |  | every parameter the run used, defaults included: the thresholds, k and the floor each move the answer |
| `copies_per_droplet` | any |  | for the ddPCRclust methods on one well: each named marker's positive droplets (every population carrying it) and its copies per droplet, -ln(1 - positives / total). Empty for the two-target methods |
| `members` | any |  | for the ddPCRclust methods: each first clustering that ran, with its population counts or the error that left it out of the consensus. `ensemble` is only as good as the members that agreed |
| `confidence` | number |  | for the ddPCRclust methods: the mean corrected Rand index between the member partitions (1 when one member answered). Low means the three first clusterings disagree about this well |
| `wells` | any |  | for a PLATE: every well's counts, copies per droplet, confidence and members, or the reason no member could partition it. `classes`, `counts` and `total` are empty for a plate |
| `normalised` | any |  | for a PLATE with `constant_control`: every well's copies per droplet after scaling to the control's highest value on the plate, with each well's factor. Null without a control |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "classify_droplets",
  "arguments": {
    "droplets": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_qpcr_assay

**Design qPCR assay**: _Which primer pair and hydrolysis probe make a qPCR assay on this target, ranked by penalty?_

Design qPCR assays over the subject — primer pair plus hydrolysis probe, ranked by penalty, with amplicon size/GC, per-oligo Tm and whether both primers bind a single site.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- primer3's and TaqMan's published constraints define an acceptable assay.
- Melting temperatures are the nearest-neighbour model's at the stated conditions.

**Does not:**
- No upstream designs this triple, so every cited primer3 and TaqMan constraint is asserted on the designed assays instead.
- Specificity is whether both primers bind a single site in the sequence given, not in a genome.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to design in. Unset = the whole sequence; pass the selection's start to scope to it. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end. Unset = the whole sequence. Advanced. |
| `max_results` | number |  | `5` | 1–25 | how many assays to return, best penalty first. |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method and any DMSO or formamide that every Tm in this design is measured in. Left unset it is filled from your reaction-conditions settings, and falls back to the nearest-neighbour defaults when there are none. Advanced. |
| `conditions.Na` | number |  |  | ≥ 0 | Na⁺ [mM]. In mM. |
| `conditions.K` | number |  |  | ≥ 0 | K⁺ [mM]. In mM. |
| `conditions.Tris` | number |  |  | ≥ 0 | Tris buffer [mM]. In mM. |
| `conditions.Mg` | number |  |  | ≥ 0 | Mg²⁺ [mM]. In mM. |
| `conditions.dNTPs` | number |  |  | ≥ 0 | total dNTPs [mM]. In mM. |
| `conditions.dnac1` | number |  |  | ≥ 0 | primer / higher-concentration strand [nM]. In nM. |
| `conditions.dnac2` | number |  |  | ≥ 0 | template / other strand [nM]. In nM. |
| `conditions.saltcorr` | number |  |  | 0–7 | Biopython salt-correction method 0–7 (0 = none). It moves the answer more than any other knob here: on a 24-mer at the Taq buffer the eight span 79.302 °C (method 0) to 66.009 °C (method 2). |
| `conditions.selfcomp` | boolean |  |  |  | both strands are one self-complementary oligo (the concentration term becomes dnac1 rather than dnac1 − dnac2/2). |
| `conditions.method` | `"santaLucia"` · `"dbd"` |  |  |  | which validated nearest-neighbour model and default buffer — santaLucia (pydna `tm_default`, Taq) or dbd (pydna `tm_dbd`, Phusion / Pfu-Sso7d). Values: santaLucia (SantaLucia (pydna tm_default, Taq)), dbd (DNA-binding domain (pydna tm_dbd, Phusion)). |
| `conditions.nnTable` | string |  |  |  | override the method's nearest-neighbour table; the buffer convention is unchanged. |
| `conditions.additives` | object |  |  |  | DMSO and formamide, applied AFTER the nearest-neighbour Tm. |
| `conditions.additives.DMSO` | number |  |  | 0–100 | DMSO [% v/v]. In %. |
| `conditions.additives.fmd` | number |  |  | ≥ 0 | formamide — percent when `fmdmethod` is 1, molar when it is 2. |
| `conditions.additives.dmsoMethod` | `"ahs01"` · `"mus81"` · `"cul76"` · `"esc80"` |  |  |  | which published DMSO depression sets the coefficient. Values: ahs01 (Ahsen et al. (2001) (0.75 °C per %)), mus81 (Musielski et al. (1981) (0.6 °C per %)), cul76 (Cullen and Bick (1976) (0.5 °C per %)), esc80 (Escara and Hutton (1980) (0.675 °C per %)). |
| `conditions.additives.DMSOfactor` | number |  |  | ≥ 0 | °C of Tm lost per % DMSO, as an explicit override. Supplying it WINS over `dmsoMethod`, and detaches the number from its citation. |
| `conditions.additives.fmdfactor` | number |  |  | ≥ 0 | °C lost per % formamide (method 1). Papers report 0.6 to 0.72. |
| `conditions.additives.fmdmethod` | `1` · `2` |  |  |  | 1 = linear % formamide (McConaughy 1969) · 2 = GC-dependent, molar (Blake & Delcourt 1996). Values: 1 (Linear %, McConaughy 1969), 2 (GC-dependent molar, Blake & Delcourt 1996). |
| `structure_check` | boolean |  | `true` |  | run the `thal` secondary-structure check on the RETURNED assays: hairpin and cross-dimer melting temperatures for all three oligos and every pairing between them. On by default, because a qPCR assay that dimerises is the commonest design failure and penalty ranking alone will happily put one first. Off returns null structures and is measurably faster - the check is a dynamic-programming alignment per oligo pair. Advanced. |
| `probe_chemistry` | `"dna"` · `"lna"` |  | `"dna"` |  | what the hydrolysis probe is made of. `dna` is unmodified DNA; `lna` locks the bases named by `probe_locked_positions`, which raises the probe Tm and is how a short probe reaches the TaqMan offset over its primers. MGB and Scorpion chemistries are not offered: neither has a published nearest-neighbour parameter set to compute a Tm from. |
| `probe_locked_positions` | string |  | `""` |  | which bases to lock, 1-based from the probe's 5′ end, e.g. `3, 6, 9`. Read only when `probe_chemistry` is `lna`. Positions must be interior to the SHORTEST probe the search will try and never adjacent, because McTigue et al. (2004) measured one locked base per nearest neighbour and none at a duplex end - a position that breaks either rule is refused by name rather than silently dropped. Only applies when probe_chemistry is lna. |
| `amplicon_min` | number |  | `70` | 40–500 | shortest acceptable amplicon. In bp. |
| `amplicon_max` | number |  | `150` | 50–1000 | longest acceptable amplicon - qPCR amplicons are short on purpose, because a short product amplifies efficiently enough for the exponential phase to be clean. In bp. |
| `primer_tm_opt` | number |  | `59` | 50–72 | target primer Tm; the penalty ranks candidates by their distance from it. In °C. |
| `probe_tm_opt` | number |  | `68` | 55–80 | target probe Tm - conventionally ~10 °C above the primers, so the probe is bound before extension reaches it. In °C. |
| `probe_tm_offset_min` | number |  | `6` | 0–20 | how many °C the probe Tm must exceed the MEAN primer Tm. TaqMan guidance is 8-10; below that the probe can melt off before it is cleaved. In °C. |
| `primer_min_length` | number |  | `18` | 10–36 | shortest primer considered. In nt. Advanced. |
| `primer_opt_length` | number |  | `20` | 10–36 | primer length the penalty prefers. In nt. Advanced. |
| `primer_max_length` | number |  | `23` | 10–36 | longest primer considered; primer3's own ceiling is 36. In nt. Advanced. |
| `primer_min_tm` | number |  | `57` | 40–80 | primers below this Tm are rejected outright, not merely penalised. In °C. Advanced. |
| `primer_max_tm` | number |  | `63` | 40–90 | primers above this Tm are rejected outright. In °C. Advanced. |
| `primer_min_gc` | number |  | `30` | 0–100 | lowest acceptable primer GC content. In %. Advanced. |
| `primer_max_gc` | number |  | `80` | 0–100 | highest acceptable primer GC content. In %. Advanced. |
| `probe_min_length` | number |  | `18` | 10–36 | shortest probe considered. In nt. Advanced. |
| `probe_opt_length` | number |  | `20` | 10–36 | probe length the penalty prefers. In nt. Advanced. |
| `probe_max_length` | number |  | `27` | 10–36 | longest probe considered. In nt. Advanced. |
| `probe_min_tm` | number |  | `65` | 40–90 | probes below this Tm are rejected outright. In °C. Advanced. |
| `probe_max_tm` | number |  | `72` | 40–95 | probes above this Tm are rejected outright. In °C. Advanced. |
| `probe_min_gc` | number |  | `30` | 0–100 | lowest acceptable probe GC content. In %. Advanced. |
| `probe_max_gc` | number |  | `80` | 0–100 | highest acceptable probe GC content. In %. Advanced. |
| `max_poly_x` | number |  | `5` | 2–10 | longest run of one base allowed in any oligo (primer3's POLY_X). A long run mispairs by slipping, and for a TaqMan probe a run of four or more Gs quenches the reporter. In nt. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `assays` | any |  | the ranked assays |
| `conditions` | any |  | the buffer every Tm in this design was measured in - salt, magnesium, dNTPs, oligo concentration, the salt-correction method and any additives - or a note saying none were supplied |
| `count` | number |  | how many assays were found |
| `best` | any |  | the best-penalty assay |
| `forward` | string |  | the best assay's forward primer |
| `reverse` | string |  | the best assay's reverse primer |
| `probe` | string |  | the best assay's probe |
| `probe_ordered` | string |  | the best assay's probe as it must be ORDERED: plain DNA, or the locked-base notation (`GTCGLAAC`) when the probe was designed as LNA |
| `offset` | number |  | where the designed-in stretch starts in the record: add it to every position above for record coordinates. 0 unless a region was given |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_qpcr_assay",
  "arguments": {
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### gate_droplets

**Gate droplets**: _What is the template concentration in each ddPCR well, from the raw droplet amplitudes rather than the instrument's count?_

Two-channel ddPCR droplet-amplitude exports to a template concentration, by CLASSIFYING the raw droplets rather than trusting a count the instrument already made. Four steps in a fixed order, each of which needs the previous one's output: a k-means quality check marks wells whose two droplet clusters are not separable, a plate-wide 1%-slice IQR cutoff marks outlier droplets, a two-component Gaussian mixture per well per channel sets the empty-droplet cutoff on the droplets that survive, and the empty fraction inverts through the Poisson zero term to copies/uL. Reports the cluster the droplets landed in and the reason any well was rejected, so a failed well reads as rejected rather than as a concentration. This is the counterpart of `quantify_dpcr`, not a duplicate: that one starts from per-well positive COUNTS an instrument already classified, this one starts from the amplitudes and does the classifying.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- Empty and positive droplets form two separable clusters per channel, each well checked by k-means first.
- Copies are Poisson-distributed across droplets of the stated volume.

**Does not:**
- A well whose clusters do not separate is rejected with its reason, not quantified.
- Rain between the clusters is assigned by the mixture's cutoff, which moves with the data.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `files` | string | **yes** |  |  | the droplet exports, as `<filename>` and its CSV body. QuantaSoft writes one `<name>_<well>_Amplitude.csv` per well with columns `Assay1 Amplitude, Assay2 Amplitude, Cluster`; the well id is read from the FILE NAME because the body does not carry it. Separate files with a line containing only `---`, and start each with `# <filename>`. |
| `random_seed` | number |  | `8` | 1–2147483647 | re-seeded before EVERY k-means and EVERY mixture fit, not once per run. Neither has a deterministic start, so this value IS part of the answer: a different seed lands the mixture on a different local optimum and moves the empty cutoff. Upstream's default is 8. |
| `droplet_volume_ul` | number |  | `0.00085` | 1e-06–1 | mean volume of ONE droplet, in µL. A per-platform constant: 0.85e-3 µL (0.85 nL) for the Bio-Rad QX200, which is what the QuantaSoft export comes from. |
| `total_drops_t` | number |  | `5000` | 0–100000 | fewer accepted droplets than this and the well is rejected before it is clustered at all. |
| `empty_lambda_low` | number |  | `0.3` | 0–1 | smallest empty-droplet fraction a well may have. Below it the smaller k-means cluster is too small to be the empty population, which means the run did not separate. |
| `empty_lambda_high` | number |  | `0.99` | 0–1 | largest empty-droplet fraction a well may have. Above it almost every droplet is empty, so there is no positive population to quantify and a concentration would be an extrapolation. |
| `top_percent` | number |  | `1` | 0.1–100 | the top slice of droplets, pooled across the SUCCESSFUL wells, that the outlier cutoff is computed on. One cutoff per axis for the whole plate, not one per well. |
| `cutoff_iqr` | number |  | `5` | 0–50 | how many interquartile ranges above the third quartile of that slice a droplet must sit to be an outlier. |
| `cutoff_sd` | number |  | `7` | 0–30 | how many standard deviations above the LOWER mixture component's mean the empty cutoff sits. This is the knob that decides which droplets are empty, and therefore the concentration. |
| `x_var` | string |  | `"HEX"` |  | name for the X channel, which is the file's SECOND amplitude column. Bio-Rad's Ch2 is usually HEX or VIC. |
| `y_var` | string |  | `"FAM"` |  | name for the Y channel, which is the file's FIRST amplitude column. Bio-Rad's Ch1 is usually FAM. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `wells` | any |  | one row per well: droplet counts by cluster, the empty fraction, the per-well cutoffs, and the concentration in copies/uL — null for a rejected well, never a number |
| `count` | number |  | how many wells were read |
| `rejected` | number |  | how many wells were rejected by the quality check and so carry no concentration |
| `verdicts` | any |  | why each well passed or was rejected, with the k-means the verdict was taken from: both cluster centres, their sizes, their distances to the origin and the gap between them |
| `outlierCutoff` | any |  | the two plate-wide outlier cutoffs, echoed because they were computed from the successful wells only and so depend on which wells passed |
| `totalDroplets` | number |  | every droplet read, across every well — the denominator the cluster counts account for |
| `params` | any |  | every parameter the run used, including the ones left at their defaults: the seed and the two cutoff multipliers change the concentration, so a reading without them is not comparable |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "gate_droplets",
  "arguments": {
    "files": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### melt_profile

**Melt profile**: _How does this molecule melt: the helicity curve, its Tm50, and the domains that melt together behind each HRM peak?_

DNA melting behaviour of the subject by the Poland–Scheraga model (DECIPHER): the melt curve (mean helicity vs temperature), its Tm50, and the cooperatively-melting domains behind each HRM peak.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The Poland-Scheraga recursion as DECIPHER implements it, at the stated salt and strand conditions.

**Does not:**
- An equilibrium model: ramp rate and dye chemistry are not in it.
- Domains are the model's cooperative units, not measured peaks.

**Not read from this result:** The answer is the helicity curve itself, which the outputs carry; the Melting temperature panel draws it and writes no reading over it.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `min_temp` | number |  | `60` | 0–120 | lowest temperature to evaluate. In °C. |
| `max_temp` | number |  | `95` | 0–120 | highest temperature to evaluate. In °C. |
| `step` | number |  | `0.5` | 0.1–5 | grid spacing; finer costs proportionally more. In °C. |
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to melt. Unset = the whole sequence; pass the selection's start to scope to it. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end. Unset = the whole sequence. Advanced. |
| `ions` | number |  | `0.2` | 0.01–1 | molar sodium-equivalent concentration. Defaults to DECIPHER's own 0.2 M; the editor substitutes the project's shared Na⁺ instead. In M. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `tm50` | number or null | °C | temperature where mean helicity crosses 0.5 (null if the range never crosses it) |
| `curve` | any |  | mean helicity per temperature |
| `derivative` | any |  | −dθ/dT, the HRM trace |
| `meltPlot` | object or null |  | the melt curve as a plot: mean helicity against temperature |
| `meltPlot.x` | number[] |  |  |
| `meltPlot.series` | object[] |  |  |
| `meltPlot.series[].name` | string |  |  |
| `meltPlot.series[].y` | (number or null)[] |  |  |
| `meltPlot.xLabel` | string |  |  |
| `meltPlot.yLabel` | string |  |  |
| `meltPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `meltPlot.title` | string |  |  |
| `meltPlot.rules` | object[] |  |  |
| `meltPlot.rules[].y` | number |  |  |
| `meltPlot.rules[].label` | string |  |  |
| `hrmPlot` | object or null |  | the HRM trace as a plot: −dθ/dT against temperature, one peak per melting domain |
| `hrmPlot.x` | number[] |  |  |
| `hrmPlot.series` | object[] |  |  |
| `hrmPlot.series[].name` | string |  |  |
| `hrmPlot.series[].y` | (number or null)[] |  |  |
| `hrmPlot.xLabel` | string |  |  |
| `hrmPlot.yLabel` | string |  |  |
| `hrmPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `hrmPlot.title` | string |  |  |
| `hrmPlot.rules` | object[] |  |  |
| `hrmPlot.rules[].y` | number |  |  |
| `hrmPlot.rules[].label` | string |  |  |
| `transitions` | any |  | melting domains (one peak each) |
| `domainCount` | number |  | number of cooperatively-melting domains |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "melt_profile",
  "arguments": {
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### melting_temperature

**Melting temperature**: _What is this oligo's melting temperature in this buffer under this model, step by step?_

The melting temperature of an oligo IN A BUFFER, UNDER A MODEL — and the working, not just the number. Nearest-neighbor (SantaLucia & Hicks 2004 · Allawi & SantaLucia 1997 · Sugimoto 1996 · Breslauer 1986), pydna's dsDNA-binding-domain model, the GC formula, the Wallace rule or NEB, over the salt correction you name, then DMSO and formamide depression under the published model you name. LOCKED NUCLEIC ACID is understood: write the probe as it is ordered, with an L after each locked base (GTCGLAACAGC), and McTigue, Peterson & Kahn's (2004) per-neighbor increments are added to the nearest-neighbor sum. Returns the per-step breakdown the panel shows, so a pipeline can read WHICH coefficient produced a ΔTm rather than a bare temperature.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The nearest-neighbor table, salt correction and additive model named in the request.
- Two-state melting at the stated strand concentration.

**Does not:**
- A model's prediction, not a measurement; modified bases other than LNA are not modeled.

**Not read from this result:** A melting temperature under the stated model and buffer is the whole answer, which the outputs carry; the Melting temperature panel shows it as a readout and writes no reading over it.

**Validated:** against the reference implementation by 5 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `oligo` | string | **yes** |  |  | the oligo to melt, 5'→3'. IUPAC ambiguity codes and whitespace are tolerated; at least 2 bases. An L after a base marks it LOCKED (LNA), e.g. GTCGLAACAGC — the marker is not a base and does not count toward the length. |
| `model` | string |  | `"nn_unified"` |  | which melting model — nn_santalucia (Nearest-neighbor, SantaLucia 1997) · nn_unified (Nearest-neighbor, unified 2004) · nn_sugimoto (Nearest-neighbor, Sugimoto 1996) · nn_breslauer (Nearest-neighbor, Breslauer 1986) · nn_rna_xia (RNA/RNA, Xia 1998) · nn_rna_chen (RNA/RNA, Chen 2012 (GU wobble)) · nn_rna_freier (RNA/RNA, Freier 1986) · nn_hybrid_sugimoto (RNA/DNA hybrid, Sugimoto 1995) · bresluc_dbd (Breslauer (dsDNA-binding polymerase)) · gc (GC-based (Tm_GC)) · wallace (Wallace rule (2·AT + 4·GC)) · neb (NEB). Advanced. |
| `dmso_method` | string |  | `"ahs01"` |  | which published DMSO depression — ahs01 (Ahsen et al. (2001), 0.75 °C per %) · mus81 (Musielski et al. (1981), 0.6 °C per %) · cul76 (Cullen and Bick (1976), 0.5 °C per %) · esc80 (Escara and Hutton (1980), 0.675 °C per %). Only read when the conditions carry DMSO. Only applies when dmso is set. Advanced. |
| `conditions` | object |  |  |  | the buffer this temperature is measured in: Na⁺/K⁺/Tris/Mg²⁺/dNTP under `salt`, the strand concentrations under `oligo`, and any DMSO or formamide under `additives`. Left unset it is filled from your reaction-conditions settings, which is what the Melting Temperature panel is showing, so the two doors cannot quote different temperatures for one oligo. Advanced. |
| `conditions.model` | string |  |  |  | which melting model this buffer is read under. Named here as well as at the top level because a conditions object is a complete description of one measurement. |
| `conditions.gcValueSet` | string |  |  |  | which published GC-formula parameter set, for the GC model. |
| `conditions.salt` | object |  |  |  | buffer composition [mM], plus the salt-correction method. |
| `conditions.salt.Na` | number |  |  | ≥ 0 | Na⁺ [mM]. In mM. |
| `conditions.salt.K` | number |  |  | ≥ 0 | K⁺ [mM]. In mM. |
| `conditions.salt.Tris` | number |  |  | ≥ 0 | Tris buffer [mM]. In mM. |
| `conditions.salt.Mg` | number |  |  | ≥ 0 | Mg²⁺ [mM]. In mM. |
| `conditions.salt.dNTPs` | number |  |  | ≥ 0 | total dNTPs [mM]. In mM. |
| `conditions.salt.method` | number |  |  | 0–7 | Biopython salt-correction method 0–7 (0 = none). |
| `conditions.oligo` | object |  |  |  | strand concentrations. |
| `conditions.oligo.dnac1` | number |  |  | ≥ 0 | higher-concentration strand [nM]. In nM. |
| `conditions.oligo.dnac2` | number |  |  | ≥ 0 | lower-concentration strand [nM]. In nM. |
| `conditions.oligo.selfcomp` | boolean |  |  |  | self-complementary oligo (halves the effective concentration term). |
| `conditions.additives` | object |  |  |  | DMSO and formamide, applied after the base model. |
| `conditions.additives.dmso` | number |  |  | 0–100 | DMSO [% v/v]. In %. |
| `conditions.additives.dmsoMethod` | `"ahs01"` · `"mus81"` · `"cul76"` · `"esc80"` |  |  |  | which published DMSO depression sets the coefficient. Values: ahs01 (Ahsen et al. (2001) (0.75 °C per %)), mus81 (Musielski et al. (1981) (0.6 °C per %)), cul76 (Cullen and Bick (1976) (0.5 °C per %)), esc80 (Escara and Hutton (1980) (0.675 °C per %)). |
| `conditions.additives.dmsoFactor` | number |  |  | ≥ 0 | °C lost per % DMSO. Setting it directly detaches the number from its citation. |
| `conditions.additives.formamide` | number |  |  | ≥ 0 | formamide — % (v/v) for method 1, mol/L for method 2. |
| `conditions.additives.formamideMethod` | `1` · `2` |  |  |  | 1 = linear % (McConaughy 1969) · 2 = GC-dependent, molar (Blake & Delcourt 1996). Values: 1 (Linear %, McConaughy 1969), 2 (GC-dependent molar, Blake & Delcourt 1996). |
| `conditions.additives.formamideFactor` | number |  |  | ≥ 0 | °C lost per % formamide (method 1). Papers report 0.6 to 0.72. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `tm` | number | °C | melting temperature [°C] after every correction the conditions asked for |
| `steps` | any |  | the derivation, one row per correction: the base model with its table and salt method, then each additive with the degrees it removed AND the published model that set the coefficient — the same rows the panel prints, from the same generator |
| `baseTm` | number | °C | the temperature BEFORE any additive, so a pipeline can see what DMSO or formamide cost rather than inferring it |
| `model` | string |  | the model that produced it, named — never the id alone |
| `gc` | number | % | GC content [%] of the oligo, weighted for ambiguity codes |
| `thermodynamics` | any |  | ΔH, ΔS and ΔG(37 °C) from the SAME table as the temperature, so a row never mixes two models. Absent for models that carry no nearest-neighbor table (GC formula, Wallace, NEB) |
| `lockedBases` | number |  | how many bases of this oligo were read as LOCKED (LNA). 0 for ordinary DNA, so a pipeline can tell whether McTigue's increments were in play without parsing the steps |
| `caveat` | string |  | why this model's number should not be read for an oligo of this length, or empty when it can be — Wallace above its published 14–20 nt domain is the case this exists for |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "melting_temperature",
  "arguments": {
    "oligo": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### propagate_uncertainty

**Propagate uncertainty**: _How uncertain is a reported qPCR quantity, given the uncertainty of each measurement in it, and which measurement contributes most?_

Uncertainty through any qPCR quantity, three independent ways at once. Give it the expression you actually report - a ratio, a normalised expression, an efficiency-corrected quantity - and a mean and standard deviation for each variable in it (or the replicate observations themselves), and it returns the analytic Taylor propagation, a Monte-Carlo simulation and a permutation resampling side by side, because they disagree in informative ways: the Taylor arm is exact only for a linear expression, and a ratio is not linear. Also reports the derivative per variable and how much of the total variance each one contributes, which is the answer to "which measurement should I make more precisely?". Reproduces qpcR 1.4.2's `propagate`.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- Each variable's mean and SD (or its replicates) describe its uncertainty; covariances are used only when asked.

**Does not:**
- The Taylor arm is exact only for a linear expression; a ratio is not linear, so compare it with the simulation.
- Systematic error (a wrong efficiency, a biased calibrator) is not in the spread.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `expression` | string | **yes** |  |  | the quantity whose uncertainty is wanted, in R's syntax over the variable names below: `x/y`, `2^-(a - b)`, `(Etar^-Cttar)/(Eref^-Ctref)`. Every name in it must appear in `variables`. |
| `input` | `"stat"` · `"raw"` |  | `"stat"` |  | what `variables` holds. `stat` = a summary per variable; `raw` = the replicate observations. `raw` is the stronger input: it carries the measured covariance between variables and it is the only one the permutation arm can resample, because permutation resamples observed ROWS and a mean with an SD beside it has none. |
| `variables` | string | **yes** |  |  | the numbers. In `stat` mode: a header row `variable, mean, sd` and one row per variable. In `raw` mode: a header row of variable names and one row per replicate, blank cells left blank (they are dropped pairwise, never read as zero). Tab- or comma-separated. |
| `second_order` | boolean |  | `true` |  | include the second-order Taylor terms. On is upstream's default and is what makes the analytic arm usable on a ratio; off gives the classic first-order propagation of error. |
| `use_cov` | boolean |  | `false` |  | `raw` only: propagate the measured covariance between the variables, not just their variances. Two Ct values read off the same plate are not independent, and treating them as independent understates the error of their ratio. Only applies when input is raw. |
| `do_sim` | boolean |  | `true` |  | run the Monte-Carlo arm — draw from the joint normal and push every draw through the expression. Correct for any nonlinearity, at the cost of being a sample. |
| `nsim` | number |  | `10000` | 5000–1000000 | Monte-Carlo draws. Only applies when do_sim is true. |
| `dist_sim` | `"norm"` · `"tnorm"` |  | `"norm"` |  | the distribution drawn from: `norm`, or `tnorm` truncated at zero — the one to use when a variable is a concentration or a fluorescence and a negative draw is not a possible measurement. Only applies when do_sim is true. |
| `do_perm` | boolean |  | `false` |  | `raw` only: run the permutation arm, which resamples the observed rows and so assumes no distribution at all. It also returns p-values for the three hypotheses upstream tests. Only applies when input is raw. |
| `nperm` | number |  | `2000` | 100–200000 | permutations. Only applies when do_perm is true. |
| `ties` | string |  | `""` |  | `raw` only: which columns are resampled together, as one whole number per column — `1,1,2` permutes the first two as a block. Blank permutes every column on its own. Use it when two columns are readings of the same tube. Only applies when do_perm is true. |
| `conf_level` | number |  | `0.95` | 0.5–0.999 | the level the reported bounds are read at. |
| `seed` | number |  | `1` | ≥ 1 | R's `set.seed` value, so a simulated or permuted run is reproducible and citable. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `propagatedMean` | number or null |  | the expression evaluated at the input means, with the second-order correction when it is on |
| `firstOrderMean` | number or null |  | the expression evaluated at the input means, before the second-order correction |
| `secondOrderMean` | number or null |  | the mean with the second-order Taylor correction applied, whether or not the reported mean uses it |
| `propagatedSd` | number or null |  | the analytic (Taylor) standard error — the number to report when the expression is close to linear |
| `confLower` | number or null |  | lower analytic bound at `conf_level` |
| `confUpper` | number or null |  | upper analytic bound |
| `simulated` | any |  | the Monte-Carlo arm: mean, sd, median, mad and its own interval. Every field null when it was not run — a nonlinear expression whose two arms disagree is the finding, not a display detail |
| `permuted` | any |  | the permutation arm, same fields. Null in `stat` mode, which has no rows to resample |
| `permPValues` | any |  | permutation p-values for the three hypotheses upstream tests, in `perm > init` / `perm == init` / `perm < init` order |
| `contributions` | any |  | how much of the propagated variance each variable contributes, in %, first-order — which measurement to make more precisely |
| `gradient` | any |  | the printed partial derivative per variable, and its value at the means |
| `variables` | any |  | the variable names the run used, in expression order — every other array here is in this order |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "propagate_uncertainty",
  "arguments": {
    "expression": "<string>",
    "variables": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### quantify_dpcr

**Quantify dPCR**: _What is the absolute concentration of a target from digital PCR partition counts, with a confidence interval?_

Digital PCR (dPCR) partition counts to absolute concentration, with no standard curve. Positives and accepted partitions become lambda = -ln(1 - k/n), lambda becomes copies per uL through the partition volume and the dilution chain, and the confidence interval is carried on the lambda scale under any of eleven published binomial interval methods. Returns the dMIQE-2020 occupancy QC beside every reading, so a well with no positives, or one saturated past 95% occupancy, is reported as such rather than as a number.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Template copies are Poisson-distributed across partitions of the stated volume.
- Partitions are classified correctly by the instrument.

**Does not:**
- A well with no positives or past 95% occupancy is reported as such, not as a number.
- The answer is only as good as the partition volume; a published nominal volume can be off by several percent.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `wells` | string | **yes** |  |  | the well table: `Well,Sample,Target,Positives,Partitions`. Instrument column names are accepted as they are printed (Bio-Rad's `AcceptedDroplets`, QIAcuity's `Valid partitions`), so a real export needs no renaming. |
| `partition_volume_nl` | number |  | `0.85` | 0.01–10 | mean volume of ONE partition. A per-platform constant, not a universal one (Bio-Rad QX200 approx 0.85 nL, QIAcuity 26k approx 0.34 nL, QuantStudio 3D approx 0.755 nL), and dMIQE 2020 requires it to be reported with the result. In nL. |
| `reaction_volume_ul` | number |  | `20` | 1–200 | total reaction volume, for copies per reaction. In uL. |
| `template_volume_ul` | number |  | `0` | 0–200 | volume of template added to the reaction. Left at 0 the sample-concentration row is omitted rather than guessed. In uL. Advanced. |
| `dilution_factor` | number |  | `1` | 1–100000 | fold dilution applied to the sample before the reaction (2 = diluted 1:2). Advanced. |
| `ci_method` | `"agresti-coull"` · `"asymptotic"` · `"bayes"` · `"cloglog"` · `"exact"` · `"logit"` · `"lrt"` · `"probit"` · `"prop.test"` · `"profile"` · `"wilson"` |  | `"wilson"` |  | which binomial confidence interval is carried onto the lambda scale. Values: agresti-coull (Agresti–Coull), asymptotic (Asymptotic (normal approximation)), bayes (Bayes (Jeffreys prior, highest-density)), cloglog (Complementary log-log), exact (Exact (Clopper–Pearson)), logit (Logit), lrt (Likelihood ratio), probit (Probit), prop.test (Score test inverted, continuity-corrected), profile (Profile likelihood), wilson (Wilson score). Advanced. |
| `conf_level` | number |  | `0.95` | 0.5–0.999 | confidence level for the interval. Advanced. |
| `merge_replicates` | boolean |  | `true` |  | pool wells that share a sample and target before quantifying. Replicates of one measurement are one measurement, and pooling the COUNTS is the correct way to combine them, never averaging concentrations. |
| `ratio_target` | string |  |  |  | the assay whose COPY NUMBER you want, named as it appears in the table's Target column. Leave it and `ratio_reference` unset and no copy number is reported at all — a guessed pair is a fabricated comparison. |
| `ratio_reference` | string |  |  |  | the assay it is measured against: the single-copy or known-ploidy reference, again by its Target name. |
| `reference_copies` | number |  | `2` | 1–100 | copies of the REFERENCE target per genome. 2 is a diploid autosome, 1 a haploid or single-copy locus. Advanced. |
| `volume_model` | `"poisson"` · `"normal"` · `"truncated"` |  | `"poisson"` |  | how partition-volume SPREAD is handled (QP-5c). `poisson` is the standard estimator and assumes every partition holds the same volume. The two Poisson-Plus arms (Majumdar 2017) integrate the Poisson negative probability over a normal volume distribution and invert it: `normal` is the closed-form Eq (9), `truncated` the exact Eq (13) over a normal cut off at zero, which is the honest density because a partition cannot hold a negative volume. The spread biases the standard estimate DOWNWARD, hard at high occupancy and not at all at low. Values: poisson (Standard Poisson (no correction)), normal (Poisson-Plus, normal (Eq 9)), truncated (Poisson-Plus, truncated normal (Eq 13)). |
| `volume_cv` | number |  | `0` | 0–100 | coefficient of variation of the partition volume, as a percentage. Ignored under the `poisson` model. There is no universal value and inventing one would fabricate the exact quantity the correction consumes - the one figure this repo has a published source for is QuantStudio 3D chip (Majumdar 2017) at 3.03 %, and that paper says the vendor re-estimates it per chip rather than treating it as a platform constant. In %. Only applies when volume_model is normal or truncated. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rows` | any |  | one reading per well, or per pooled replicate group: occupancy, lambda with its interval, and every concentration the supplied volumes support |
| `count` | number |  | how many readings were produced |
| `flagged` | number |  | readings carrying at least one dMIQE occupancy flag |
| `ciMethod` | string |  | the interval method that produced the bounds: a CI without its method is not comparable |
| `partitionVolumeNl` | number |  | the partition volume the concentrations were computed at, echoed because dMIQE requires it to travel with the number |
| `ratios` | any |  | target-vs-reference copy number per sample, with the exact Poisson rate ratio and its interval rescaled onto the concentration scale the number is on. Empty when no assay pair was named — never a guessed pair |
| `volumeModel` | string |  | how partition-volume spread was handled. `poisson` means it was not — a concentration without this is not comparable with one that was corrected |
| `volumeCvPercent` | number |  | the volume spread the correction used, echoed for the same reason as the partition volume: it changed the number |
| `confLevel` | number or null |  | the confidence level every interval in `rows` was computed at |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "quantify_dpcr",
  "arguments": {
    "wells": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### read_rdml_run

**Read RDML run**: _What does an RDML export hold, and what are one run's curves, Cq values, melts and partition counts as tables?_

Read an instrument's RDML export - the open qPCR exchange standard, v1.0 to v1.4 - and hand back one run's contents as the same tables every other qPCR tool here takes. This is the step every qPCR analysis starts from. Lists what each run actually holds (amplification curves, melting curves, instrument Cq values, digital-PCR partition counts with the partition volume the file declares) before anything is imported, so a run is chosen on what is in it rather than on its name. Takes the UNCOMPRESSED XML: a `.rdml` archive is a zip, and the tool vocabulary here has no file input.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The XML is RDML v1.0 to v1.4, uncompressed.

**Does not:**
- Reads what the instrument wrote; it does not judge it.

**Not read from this result:** A file reader: the runs and the table come back as the RDML file states them, and the analyses that read them (call_cq, relative_expression, analyze_melt_curves) carry the reading.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `rdml_xml` | string | **yes** |  |  | the RDML document as XML text - the `rdml_data.xml` member of a `.rdml` archive, or a bare `.xml` export. Not base64 and not a file path. |
| `run` | number |  | `0` | 0–9999 | which run to read, 0-based across every experiment in the file in document order. A file routinely holds several; `summary` lists them all whatever this is set to. |
| `table` | `"summary"` · `"curves"` · `"cq"` · `"genorm"` · `"melt"` · `"partitions"` |  | `"summary"` |  | which table to return for the chosen run. `summary` reads the file without importing anything. The other four are exactly what the panel's four `Send to ...` buttons produce, so a value imported here and one imported there cannot differ. Values: summary (Summary - what every run in the file holds), curves (Amplification curves - Cycle,<reaction>,...), cq (Instrument Cq values - the wide Ct table plus its group column), genorm (Instrument Cq values - long Target,Sample,Cq), melt (Melting curves - Temperature,<reaction>,...), partitions (Digital PCR partition counts - Well,Sample,Target,Positives,Partitions). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `version` | string |  | the RDML version the file declares (1.0-1.4). The reader's behaviour differs by version and a table without it is not reproducible |
| `runs` | any |  | every run in the file and what it holds - reactions, curves, melt curves, instrument Cq values, partition counts, the declared partition volumes, targets and samples |
| `table` | string |  | the chosen run's table, as the text the matching tool's own parser takes. Empty when the run has nothing of that kind - which is a fact about the run, not a failure |
| `rows` | number |  | data rows in `table`, excluding its header |
| `groups` | string |  | for `cq`: one sample name per row of the Ct table, already aligned to it. The group column relative quantification needs |
| `omitted` | any |  | what the import deliberately left out and why - wells whose Cq is RDML's -1 `not available`, and samples whose replicates do not square up across targets. Never padded and never zero-filled (a Ct of 0 is a fabricated measurement) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_rdml_run",
  "arguments": {
    "rdml_xml": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### simulate_taqman_curve

**Simulate TaqMan curve**: _What amplification curve and Cq will a singleplex hydrolysis-probe qPCR assay draw, from its sequences and thermocycling programme?_

Predict the amplification curve a hydrolysis-probe (TaqMan) qPCR assay will draw, and the Cq read off it, from the assay's own sequences and its thermocycling programme - a forward simulation, not a fit to data. Ports DYNAMIC (Kreitmann et al., Anal. Chem. 2026, 98(12):9089-9101): thirteen species, four phases per cycle, mass-action annealing integrated as a stiff ODE, with primer-dimer formation and amplicon re-annealing competing for the primers. It is SINGLEPLEX, which is the paper's own stated limit and not an omission here - one target per run, no interassay competition. Two things it needs said about their provenance every time they are quoted: the primer-dimer free energy is upstream's NUPACK quantity and primer3's `thal` is explicitly NOT a substitute for it, and the association rate constants are one assay's FITTED values reused, not physical constants.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- DYNAMIC's thirteen-species mass-action model describes the reaction.
- The primer-dimer free energy is NUPACK's quantity, and the association rate constants are one assay's fitted values reused.

**Does not:**
- Singleplex only: one target per run, no competition between assays.
- A forward simulation, not a fit: it predicts, it does not explain a measured curve.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `amplicon` | string | **yes** |  |  | the amplicon, forward strand, 5'->3'. The whole product, not the region between the primers: the amplicon's own re-annealing is a species in the model and it competes with the primers for template late in the run, which is what bends the plateau. |
| `forward_primer` | string | **yes** |  |  | forward primer, 5'->3'. |
| `reverse_primer` | string | **yes** |  |  | reverse primer, 5'->3'. |
| `probe` | string | **yes** |  |  | the hydrolysis probe, 5'->3'. Fluorescence in this model IS probe cleavage, so without a probe there is no curve to predict - this is a TaqMan simulator and not a SYBR one. |
| `primer_dimer_dg` | number |  | `-8.88` | -30–0 | free energy of the forward-reverse primer dimer, kcal/mol, negative. NOT computed for you, and that is deliberate: the paper computes it with NUPACK and says why nothing simpler does - 'the nonspecific binding of P_for and P_rev into PD is not in perfect match', so nearest-neighbour formulas are the wrong class of tool. primer3's `thal`, which this repo does ship, is that class: on upstream's own C22 assay it returns -4.40 against upstream's -8.880. Pass the `thal` figure if it is the best you have and treat the answer as carrying that estimator's name, or pass a NUPACK value to reproduce the paper. In kcal/mol. |
| `template_copies` | number |  | `10000000` | 1–1000000000000 | template copies in the reaction at cycle 0. This is the quantity Cq is a readout OF, so sweeping it is how you get a standard curve out of this node. In copies. |
| `forward_primer_molar` | number |  | `4.5e-07` | 0–1e-05 | forward primer concentration, mol/L (450 nM in upstream's assay). In M. Advanced. |
| `reverse_primer_molar` | number |  | `4.6e-07` | 0–1e-05 | reverse primer concentration, mol/L (460 nM in upstream's assay). In M. Advanced. |
| `probe_molar` | number |  | `1.5e-07` | 0–1e-05 | probe concentration, mol/L (150 nM in upstream's assay). It caps the plateau: fluorescence cannot exceed the probe you put in. In M. Advanced. |
| `cycles` | number |  | `60` | 5–120 | how many cycles to run. In cycles. |
| `annealing_temperature` | number |  | `60` | 30–80 | annealing temperature, °C. Every binding constant in the model is evaluated here, so this is the single knob that moves the whole curve rather than scaling it. In °C. |
| `annealing_time` | number |  | `15` | 1–600 | seconds at the annealing temperature. A real parameter of the answer, not a formality: the system is NOT at equilibrium when a 15 s anneal ends, so a longer hold binds measurably more. In s. |
| `denaturation_time` | number |  | `15` | 1–600 | seconds at the denaturation temperature. It reaches the answer only through polymerase decay, so with `k_deg` at 0 it changes nothing. In s. Advanced. |
| `k_deg` | number |  | `0` | 0–0.01 | polymerase thermal-decay rate constant. Upstream SHIPS this at 0 - no decay, efficiency identically 1 at every cycle - with its own code commenting 'original value: 1.9e-4'. Left at 0 you are running the model upstream ships; raise it and the plateau bends down. Advanced. |
| `beta` | number |  | `1` | 0.1–3 | stretching exponent of the decay, exp(-(k_deg*t)^beta). Upstream ships 1, which makes the decay a plain exponential. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `cq` | number or null |  | the predicted Cq, as a whole cycle number - upstream reads it as the cycle maximising the curve's SECOND derivative, so it is not interpolated and never fractional |
| `fluorescence` | any |  | the predicted curve: one reading per cycle, in mol/L of cleaved probe |
| `curvePlot` | object or null |  | the predicted amplification curve as a plot, one point per cycle |
| `curvePlot.x` | number[] |  |  |
| `curvePlot.series` | object[] |  |  |
| `curvePlot.series[].name` | string |  |  |
| `curvePlot.series[].y` | (number or null)[] |  |  |
| `curvePlot.xLabel` | string |  |  |
| `curvePlot.yLabel` | string |  |  |
| `curvePlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `curvePlot.title` | string |  |  |
| `curvePlot.rules` | object[] |  |  |
| `curvePlot.rules[].y` | number |  |  |
| `curvePlot.rules[].label` | string |  |  |
| `plateau` | number or null |  | the final cycle's reading - what the curve levels off at, capped by the probe you put in |
| `probeConsumed` | number or null |  | fraction of the probe cleaved by the last cycle. Near 1 the plateau is probe-limited and the Cq is still trustworthy; well under it something else stopped the reaction |
| `estimators` | any |  | which model produced each quoted quantity, so nothing here is read as upstream's when it is ours (§10 r11) |
| `notes` | any |  | what the run wants said about itself, in the panel's own words |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "simulate_taqman_curve",
  "arguments": {
    "amplicon": "<string>",
    "forward_primer": "<string>",
    "reverse_primer": "<string>",
    "probe": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
