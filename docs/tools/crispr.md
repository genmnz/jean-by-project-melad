# ✂️ CRISPR & genome editing

_Guide design and scoring, off-targets, screens, and editing outcomes measured from traces._

20 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`crispr_analyze_screen`](#crispr_analyze_screen) | Which genes are hits in a pooled CRISPR screen, by gene-level Bayes factor? |
| [`crispr_design_guides`](#crispr_design_guides) | Which CRISPR guides can be made against this target, and how good is each one on-target and off-target? |
| [`crispr_design_library`](#crispr_design_library) | Which oligos should be ordered for an sgRNA pool against these targets, with the vector's overhangs and optional barcodes? |
| [`crispr_quantify_edits`](#crispr_quantify_edits) | How much of the edited population carries which indels, from a control and an edited trace (ICE)? |
| [`crispr_score_deephf`](#crispr_score_deephf) | What knockout efficiency does DeepHF predict for each guide under this nuclease and promoter? |
| [`crispr_score_deepspcas9`](#crispr_score_deepspcas9) | What indel frequency does DeepSpCas9 predict for each 30-nt context? |
| [`design_indel_primers`](#design_indel_primers) | Which back-to-back primers delete, insert or replace these residues, and what product do they make? |
| [`detect_trace_indel`](#detect_trace_indel) | Does this trace split into two reads of different length, as a heterozygous indel does? |
| [`fold_guide`](#fold_guide) | Does a spacer base-pair into its sgRNA scaffold, and what does the whole guide RNA fold into? |
| [`list_sgrna_scaffolds`](#list_sgrna_scaffolds) | Which sgRNA scaffolds has this workbench sourced, for which nucleases, from which publication? |
| [`peptide_mass`](#peptide_mass) | What is this peptide's monoisotopic and average mass, and its m/z at each charge? |
| [`protein_signal_peptide`](#protein_signal_peptide) | Where would signal peptidase cut this protein, by von Heijne's weight matrix? |
| [`quantify_base_editing`](#quantify_base_editing) | What fraction of each base in the guide window was edited, from one trace (EditR)? |
| [`screen_contamination`](#screen_contamination) | Does this sequence carry vector, adapter, linker or primer contamination from UniVec, and how strong is each match? |
| [`screen_guides`](#screen_guides) | Which guide spacers fail the pre-acceptance screens: GC, self-complementary hairpins, and hairpins against the sgRNA backbone? |
| [`screen_molecule_library`](#screen_molecule_library) | How does each structure of this library fare against these rules and alerts? |
| [`screen_oligo_structure`](#screen_oligo_structure) | Which oligos in a set form hairpins, self-dimers or cross-dimers, at any position and at the 3' end? |
| [`search_off_targets`](#search_off_targets) | Which sites in this sequence could a guide also cut, and how specific is the guide within it? |
| [`survey_off_targets`](#survey_off_targets) | How many off-target sites, by mismatch class, does each of these spacers have in this sequence? |
| [`tide_quantify_indels`](#tide_quantify_indels) | How abundant is each indel size in the edited population (TIDE)? |

---

### crispr_analyze_screen

**CRISPR analyze screen**: _Which genes are hits in a pooled CRISPR screen, by gene-level Bayes factor?_

Call HITS from a pooled CRISPR screen: per-guide read counts in, a gene-level Bayes factor and a precision/recall curve out. This is the other end of a screen from the pool designer — it reads what came back rather than deciding what to order. The estimator is BAGEL2 (Kim & Hart 2021), reproduced byte-for-byte against upstream, so a gene's Bayes factor here is the number BAGEL2 prints for the same counts. It is a COMPARISON against two reference gene sets, not an absolute fitness measure, and it reports how many of those reference genes the library actually carries, because a screen whose gene symbols do not match the reference sets trains on almost nothing and still returns a ranking. MAGeCK's alpha-RRA and drugZ are different statistics that disagree with this one on the same counts; neither is computed here, and a hit list must say which statistic produced it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- BAGEL2's model: guide counts come from one screen with the stated controls.
- The essential and non-essential training sets are appropriate for the cell type.

**Does not:**
- A Bayes factor ranks genes; the precision and recall curve is what sets a cutoff, and the cutoff is yours.
- Low-representation guides weaken a gene's call rather than being dropped silently.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `read_counts` | string | **yes** |  |  | the count table: a header line, then one row per reagent — identifier, gene, then one column per sequenced sample. Tab- or comma-separated. Counts may be written as decimals, as upstream's own files are. |
| `essential_genes` | string | **yes** |  |  | reference ESSENTIAL gene symbols, one per line (extra columns ignored). BAGEL2's CEGv2 is the usual choice; the editor panel ships it and the mouse set beside it. |
| `non_essential_genes` | string | **yes** |  |  | reference NON-ESSENTIAL gene symbols, one per line. BAGEL2's NEGv1 is the usual choice. |
| `control_columns` | string[] | **yes** |  |  | the T0 / plasmid column NAMES, exactly as the header spells them. Summed before the fold change, so a two-replicate T0 is one control and not two. |
| `sample_columns` | string[] |  |  |  | which sample column names to score. Leave empty to score every column that is not a control. |
| `min_reads` | number |  | `0` | ≥ 0 | drop a reagent whose SUMMED control count is below this (upstream's -m). Applied after the pseudocount, exactly as upstream applies it. |
| `pseudo_count` | number |  | `5` | ≥ 0 | added to every count before normalising to 10,000,000 reads per column. Advanced. |
| `equalise_replicates` | number |  | `0` | 0–20 | scale every Bayes factor as if the screen had this many replicates (upstream's -p), 0 to leave it off. A BF is a SUM over replicates, so two screens of different replicate counts are not comparable until this is set. Advanced. |
| `fdr_cut` | number |  | `0.05` | 0–1 | the false-discovery rate the hit list is cut at. A DISPLAY threshold read off the computed curve, not a parameter of the estimator. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `genes` | any |  | every gene with its Bayes factor, standard deviation and observation count, ranked |
| `hits` | number |  | genes at or above the Bayes factor the FDR cut lands on |
| `hitBf` | number |  | the Bayes factor the cut lands on (0 when nothing clears the FDR) |
| `training` | any |  | reference essential and non-essential genes FOUND in this library, against the number supplied — the check that the symbols match |
| `fit` | any |  | the fitted line the Bayes factor is scored against: slope, intercept and the fold-change window |
| `curve` | any |  | the precision/recall curve, one row per gene |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "crispr_analyze_screen",
  "arguments": {
    "read_counts": "<string>",
    "essential_genes": "<string>",
    "non_essential_genes": "<string>",
    "control_columns": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### crispr_design_guides

**CRISPR design guides**: _Which CRISPR guides can be made against this target, and how good is each one on-target and off-target?_

Design and score CRISPR guides on the subject — on/off-target scores, QC flags, and cloning-enzyme conflicts. Nuclease list comes from the real nuclease registry.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The nuclease's PAM and spacer length are the registry's.
- On-target scores are the published models' (Rule Set 3, DeepHF, DeepSpCas9) within their trained scope.

**Does not:**
- Off-target specificity here is against the sequence searched, not a genome; it says so rather than inventing a genome-wide number.
- A score is a prediction from screens of other guides, not a measurement of this one.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `nuclease` | `"SpCas9"` · `"SpCas9-NG"` · `"SpG"` · `"SpRY"` · `"xCas9"` · `"SaCas9"` · `"SaCas9-KKH"` · `"AsCas12a"` · `"LbCas12a"` · `"enAsCas12a"` |  | `"SpCas9"` |  | the nuclease (PAM + spacer length) to scan for. Values: SpCas9 (SpCas9: NGG (3')), SpCas9-NG (SpCas9-NG: NG (3')), SpG (SpG: NGN (3')), SpRY (SpRY: NRN (3')), xCas9 (xCas9: NG (3')), SaCas9 (SaCas9: NNGRRT (3')), SaCas9-KKH (SaCas9-KKH: NNNRRT (3')), AsCas12a (AsCas12a: TTTV (5')), LbCas12a (LbCas12a: TTTV (5')), enAsCas12a (enAsCas12a: TTTV (5')). |
| `region_start` | number |  |  | ≥ 0 | restrict results to guides starting at/after this position (0-based). In bp. Advanced. |
| `region_end` | number |  |  | ≥ 0 | restrict results to guides ending at/before this position. In bp. Advanced. |
| `restriction_enzymes` | string[] |  |  |  | cloning enzymes whose recognition site must NOT appear in the spacer. Advanced. |
| `min_stem` | number |  | `4` | 2–12 | minimum self-complementary stem to report. In nt. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `guides` | any |  | the designed guides, scored |
| `count` | number |  | guides passing the region filter |
| `totalCandidates` | number |  | candidates found before filtering |
| `topSpacer` | string |  | spacer of the highest-ranked guide |
| `region` | any |  | the window the guides were filtered to, resolved: start, end, and whether it is the whole molecule. Reported because `region_start`/`region_end` are optional and their default is the molecule's length, which a caller holding only this result does not have — without it, `count` of `totalCandidates` cannot be read |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "crispr_design_guides",
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

### crispr_design_library

**CRISPR design library**: _Which oligos should be ordered for an sgRNA pool against these targets, with the vector's overhangs and optional barcodes?_

Turn the open record's annotated targets into an ORDERABLE sgRNA oligo pool: the best N guides per target, filtered at order time (Pol-III terminator, Graf inactive motif, cloning-enzyme site, minimum on-target score), each composed into the oligo a synthesiser makes — the vector's cloning overhangs around the spacer plus, optionally, one of CRISPOR's eleven subpool barcodes. A spacer that serves two overlapping targets takes ONE well, and every candidate a filter held back is counted by reason, so a short pool says which rule shortened it. It designs a library; it does not analyse one. No recommended representation, MOI or read depth is embedded — the screen-scale arithmetic is in the editor panel, where the numbers are the user's.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The order-time filters (terminator, inactive motif, cloning site, minimum score) are the ones named.
- The vector's cloning overhangs are as given.

**Does not:**
- Composes the oligos to order; synthesis success and pool representation are not predicted.

**Not read from this result:** The oligos to order with their per-target accounting; the Oligo pool section shows them as a table, and the guide ranking's reading is on crispr_design_guides.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `nuclease` | `"SpCas9"` · `"SpCas9-NG"` · `"SpG"` · `"SpRY"` · `"xCas9"` · `"SaCas9"` · `"SaCas9-KKH"` · `"AsCas12a"` · `"LbCas12a"` · `"enAsCas12a"` |  | `"SpCas9"` |  | the nuclease (PAM + spacer length) to scan for. Values: SpCas9 (SpCas9: NGG (3')), SpCas9-NG (SpCas9-NG: NG (3')), SpG (SpG: NGN (3')), SpRY (SpRY: NRN (3')), xCas9 (xCas9: NG (3')), SaCas9 (SaCas9: NNGRRT (3')), SaCas9-KKH (SaCas9-KKH: NNNRRT (3')), AsCas12a (AsCas12a: TTTV (5')), LbCas12a (LbCas12a: TTTV (5')), enAsCas12a (enAsCas12a: TTTV (5')). |
| `target_type` | string |  |  |  | annotation type to take as the targets, one pool entry per feature of that type (`CDS`, `gene`, …). Leave unset to treat the whole record as a single target — which is what a saturating-mutagenesis pool over one locus wants. |
| `guides_per_target` | number |  | `4` | 1–50 | how many guides to take per target, best-ranked first. |
| `rank` | `"ruleSet1"` · `"crisprScan"` · `"crisprRater"` |  | `"ruleSet1"` |  | which on-target score orders the candidates. A guide the chosen model cannot score is left unranked, never dropped. Rule Set 3 is deliberately not offered here: its weights are a 9.8 MB download the editor fetches on demand, and this engine is headless and cannot fetch — offering it would return an unranked pool that looked ranked. |
| `exclude_poly_t` | boolean |  | `false` |  | drop guides whose spacer carries a Pol-III (TTTT) terminator. |
| `exclude_graf` | boolean |  | `false` |  | drop guides matching a Graf 2019 inactive motif (the TT/GCC classes). |
| `restriction_enzymes` | string[] |  |  |  | cloning enzymes whose recognition site must NOT appear in the spacer — a hit drops the guide from the pool. Advanced. |
| `barcode_id` | number |  | `0` | 0–10 | CRISPOR subpool barcode id, 0 for none — lets several sub-libraries share one synthesis array and amplify apart. Advanced. |
| `custom_prefix` | string |  |  |  | your vector's 5' cloning overhang. BOTH sides must be given, or the pool stays on pLentiGuide — that is upstream's rule, reproduced. Advanced. |
| `custom_suffix` | string |  |  |  | your vector's 3' cloning overhang. Advanced. |
| `representation` | number |  | `1` | ≥ 1 | cells you intend to keep carrying EACH guide. Joung et al. 2017 recommends >500; the default here is the neutral 1, not that recommendation, so the plan is the identity until you choose a scale. Advanced. |
| `transduction_efficiency` | number |  | `1` | 0.001–1 | fraction of cells that take up a construct, 0-1 — sizes the transduction back up from the cells you need to keep. Advanced. |
| `reads_per_oligo` | number |  | `1` | ≥ 1 | sequencing reads per guide in the readout. Joung et al. 2017 recommends >500 for a screen (>100 to QC the cloned library); the default here is the neutral 1. Advanced. |
| `moi` | number |  | `0` | 0–10 | multiplicity of infection, 0 to leave it unplanned. Joung et al. 2017 recommends <0.3 so most cells take at most one perturbation; reported, never applied. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `oligos` | any |  | one row per selected guide: target, spacer, coordinates, rank score, Graf class and the oligo to order |
| `count` | number |  | oligos in the pool |
| `distinctSpacers` | number |  | distinct spacers — the number the screen's complexity is set by |
| `perTarget` | any |  | per target: candidates, selected, shortfall, and what each filter held back |
| `oligoLength` | number |  | length of every oligo, for a synthesis quote (null when the pool is mixed) |
| `coverage` | any |  | the screen's scale at the numbers given: cells to keep, cells to transduce, reads to buy, guides the depth expects to miss, and `belowGuidance` naming which of Joung et al. 2017's figures the plan falls short of |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "crispr_design_library",
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

### crispr_quantify_edits

**CRISPR quantify edits**: _How much of the edited population carries which indels, from a control and an edited trace (ICE)?_

Quantify a CRISPR edit from a pair of Sanger traces — how much of the population was edited, what the indel spectrum looks like, and how well the model fits. Synthego ICE: the CONTROL trace gives the unedited sequence, the EDITED trace is decomposed into a mixture of proposed indels around each guide's cut, and the abundances are fitted. Answers the question a screen cannot: not whether a guide is good, but what it actually did to these cells.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Synthego ICE's decomposition and the guides given.

**Does not:**
- Sanger-scale sensitivity; a minor allele below a few percent is not resolved.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `control` | string | **yes** |  |  | the UNEDITED trace, by file name or id — it supplies the reference the edited read is decomposed against. |
| `edited` | string | **yes** |  |  | the EDITED trace, by file name or id. |
| `guides` | string[] | **yes** |  |  | the guide spacers, RNA accepted. Each is located in the CONTROL on either strand, so the cut sites come from the data rather than from a coordinate you supply. |
| `donor` | string |  |  |  | optional HDR donor / ssODN. Given one, ICE also proposes the recombination outcome and reports an HDR percentage; left empty there is no HDR arm rather than a zero. |
| `indel_max_size` | number |  | `20` | 5–60 | largest single-cut indel modeled either side of the cut — ICE's own CLI default is 20. In bp. Advanced. |
| `base_editing` | boolean |  | `false` |  | also fit every single-base change on the PAM-distal side of each cut, for a base editor. Left false, the scores stay comparable with published ICE numbers, which the extra proposals would move. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `iceScore` | number |  | the headline ICE score: the edited fraction of the population, 0-100 |
| `knockoutScore` | number |  | the fraction carrying a frameshift or a 21+ bp indel — the number a knockout experiment is actually asking for, which is NOT the same as the edit fraction |
| `rSquared` | number |  | how well the fitted mixture explains the edited trace. A high ICE score with a poor fit is not a result, and this is the number that says so |
| `hdrPct` | number | % | the HDR percentage, when a `donor` was given |
| `iceD` | number |  | ICE-D, an independent discordance-based read on the same trace — a second opinion rather than a restatement |
| `spectrum` | any |  | the indel-size histogram ICE publishes, every size from -2x to +1x `indel_max_size` INCLUDING the zeros, so the spectrum's shape is visible and not only its peaks |
| `contributions` | any |  | each proposed edit with its relative abundance, most abundant first |
| `perGuide` | any |  | each guide's own answer: its cut (control base, from 1), the share edited there, its indel spectrum at that cut alone, and the alleles edited at it and another cut |
| `inseparable` | any |  | groups of reported alleles this trace cannot tell apart (their expected traces correlate above a variance inflation factor of 5), each with its summed share and 95% interval; the split inside a group is not measured |
| `baseEdits` | any |  | with `base_editing`, each fitted substitution (protospacer position, control base, change, share, refit interval), the range of the pool carrying any, and the notes on phasing and near-cut calls; null otherwise |
| `checks` | any |  | TIDE once per guide and tracy's breakpoint call on the same pair, reported beside ICE and never averaged into it; tracy's `status` says whether it agrees with ICE's top sizes |
| `report` | any |  | the whole result, including ICE's own notes and warnings |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "crispr_quantify_edits",
  "arguments": {
    "control": "<string>",
    "edited": "<string>",
    "guides": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### crispr_score_deephf

**CRISPR score DeepHF**: _What knockout efficiency does DeepHF predict for each guide under this nuclease and promoter?_

Score CRISPR guides with DeepHF: a predicted knockout EFFICIENCY between 0 and 1 for wild-type SpCas9 (U6 or T7 promoter), eSpCas9(1.1) or SpCas9-HF1. It is not a z-score and not comparable with Rule Set 3 — the two answer different questions and must never be averaged or ranked together. Takes 23-nt protospacers (20-nt spacer + NGG PAM), which is what `crispr_design_guides` produces; a guide whose PAM is not canonical NGG comes back null rather than extrapolated, because the model was trained on NGG only. THE WEIGHTS DOWNLOAD ON FIRST USE, 3-5 MB per model, and scoring is slow by construction: each guide is folded twice, once with the 79-nt tracrRNA scaffold, before the network sees it.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The DeepHF model named, as its authors trained it.

**Does not:**
- A prediction; trained on human cell lines.

**Not read from this result:** One predicted efficiency per protospacer. The score belongs to the guide table, whose reading is on crispr_design_guides; a sentence here would describe a column rather than a run.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protospacers` | string[] | **yes** |  |  | the 23-nt protospacers to score — 20-nt spacer plus the 3-nt PAM, exactly as DeepHF takes them. Anything that is not 23 nt of unambiguous A/C/G/T ending in GG scores null rather than being silently trimmed or extrapolated. |
| `model` | `"wt_u6"` · `"wt_t7"` · `"wt"` · `"esp"` · `"hf"` |  | `"wt_u6"` |  | which published model to score under. This is a scientific choice about YOUR experiment — which Cas9 variant, and which promoter the sgRNA is expressed from — not a quality setting, and scores from two models are not comparable. Values: wt_u6 (WT SpCas9 · U6 promoter), wt_t7 (WT SpCas9 · T7 promoter), wt (WT SpCas9 · both promoters), esp (eSpCas9(1.1)), hf (SpCas9-HF1). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `scores` | any |  | every protospacer with its efficiency, IN THE ORDER GIVEN — null where DeepHF is not defined, with the reason beside it |
| `efficiencies` | any |  | just the numbers, same order — null-preserving, so it lines up with the input |
| `best` | string |  | the highest-scoring protospacer, or empty when none could be scored |
| `scored` | number |  | how many of the inputs DeepHF is defined on — the accounting, not an assumption |
| `model` | string |  | which model produced these numbers. Scores from two models are not comparable |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "crispr_score_deephf",
  "arguments": {
    "protospacers": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### crispr_score_deepspcas9

**CRISPR score DeepSpCas9**: _What indel frequency does DeepSpCas9 predict for each 30-nt context?_

Score CRISPR guides with DeepSpCas9 (Kim et al. 2019, Sci Adv 5:eaax9249): a predicted INDEL FREQUENCY IN PERCENT for wild-type SpCas9. It is a third quantity, not a second opinion: Rule Set 3 is a z-score across a screen and DeepHF is an efficiency in [0, 1], so none of the three may be averaged or ranked together. Takes the 30-nt CONTEXT the model reads whole (4 nt + 20-nt spacer + 3-nt PAM + 3 nt), which is what `crispr_design_guides` reports as `context30`; a 23-nt protospacer is not enough and comes back null rather than padded. Unlike DeepHF it does NOT require a canonical NGG PAM, because its training library was not NGG-only. The output is the network's own linear value and is left unclipped, so a context it scores below zero reads below zero. THE WEIGHTS DOWNLOAD ON FIRST USE, about 0.93 MB, once.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- DeepSpCas9 (Kim et al. 2019) as published.

**Does not:**
- A prediction for wild-type SpCas9 only.

**Not read from this result:** One predicted activity per protospacer. The score belongs to the guide table, whose reading is on crispr_design_guides.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `contexts` | string[] | **yes** |  |  | the 30-nt contexts to score, exactly as DeepSpCas9 takes them: 4 nt upstream, the 20-nt spacer, the 3-nt PAM and 3 nt downstream. Anything that is not 30 nt of unambiguous A/C/G/T scores null, with the reason beside it, rather than being trimmed or padded. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `scores` | any |  | every context with its predicted indel percentage, IN THE ORDER GIVEN — null where the model is not defined, with the reason beside it |
| `indelPercents` | any |  | just the numbers, same order — null-preserving, so it lines up with the input |
| `best` | string |  | the highest-scoring context, or empty when none could be scored |
| `scored` | number |  | how many of the inputs DeepSpCas9 is defined on — the accounting, not an assumption |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "crispr_score_deepspcas9",
  "arguments": {
    "contexts": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_indel_primers

**Design indel primers**: _Which back-to-back primers delete, insert or replace these residues, and what product do they make?_

Round-the-horn (NEB Q5-style) primers that DELETE, INSERT or REPLACE whole residues of a CDS: the two back-to-back primers, the edited product they make after KLD re-circularisation, and the span they edit on the template. design_mutagenesis_primers covers substitutions; this covers the other three. Residue positions are 1-based on the protein.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- NEB's published Q5 geometry: non-overlapping primers pointing away from each other, the insert as a 5' tail.
- The annealing arms are pydna's `_design_primer` at the target Tm.

**Does not:**
- An insert must be a whole number of codons; anything else would frameshift everything downstream and is refused.
- No reference implementation to grade against exists (NEBaseChanger and SnapGene are closed), so the product is proved by re-simulating the PCR rather than by a golden copy.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds_feature` | string |  |  |  | the annotated CDS the residue numbers count in, by NAME. Left empty the selection scopes it, and `cds_offset` is taken from the region. |
| `edit` | `"delete"` · `"insert"` · `"replace"` |  | `"delete"` |  | which edit this is. Values: delete (Delete residues), insert (Insert residues), replace (Replace residues). |
| `first_residue` | number |  |  | ≥ 1 | 1-based first residue to remove (delete and replace). Only applies when edit is delete or replace. |
| `last_residue` | number |  |  | ≥ 1 | 1-based last residue to remove, inclusive. Only applies when edit is delete or replace. |
| `after_residue` | number |  |  | ≥ 0 | insert after this residue; 0 inserts before the first. Only applies when edit is insert. |
| `insert_codons` | string |  |  |  | the residues to introduce, as DNA codons in frame. A length that is not a multiple of 3 is refused rather than frameshifting the rest of the protein. Only applies when edit is insert or replace. |
| `template` | string |  |  |  | the whole plasmid to amplify. Left empty the open record is used, which is the usual case. Advanced. |
| `cds_offset` | number |  |  | ≥ 0 | 0-based offset of the CDS start within the template, when `template` is given literally. Resolved from the record otherwise. Advanced. |
| `circular` | boolean |  | `true` |  | the template is circular, which round-the-horn assumes. Taken from the record when one is open. |
| `target_tm` | number |  | `60` |  | annealing Tm each arm is designed to. NEB's Q5 protocol targets ~60 °C. In °C. |
| `tm_model` | `"santalucia"` · `"wallace"` · `"gc:Chester_1993"` · `"gc:QuickChange"` · `"gc:Schildkraut_1965"` · `"gc:Wetmur_Melting_1991"` · `"gc:Wetmur_RNA_1991"` · `"gc:Wetmur_DNA_RNA_1991"` · `"gc:Primer3"` · `"gc:Ahsen_2001"` |  | `"santalucia"` |  | Tm scale the arms are grown against. Values: santalucia (SantaLucia nearest-neighbor (Biopython Tm_NN defaults)), wallace (Wallace rule (4 °C per G·C, 2 °C per A·T)), gc:Chester_1993 (GC formula: Marmur-Doty (Chester & Marshak 1993)), gc:QuickChange (GC formula: QuikChange (the kit manufacturer’s own formula)), gc:Schildkraut_1965 (GC formula: Schildkraut & Lifson 1965 (Marmur-Doty + log[Na⁺])), gc:Wetmur_Melting_1991 (GC formula: Wetmur 1991, DNA (MELTING 4.3 approximate mode)), gc:Wetmur_RNA_1991 (GC formula: Wetmur 1991, RNA), gc:Wetmur_DNA_RNA_1991 (GC formula: Wetmur 1991, RNA/DNA hybrid), gc:Primer3 (GC formula: Primer3Plus product Tm (Biopython’s default set)), gc:Ahsen_2001 (GC formula: von Ahsen 2001 (accuracy against ease of use)). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `forward` | any |  | the forward primer: `seq` as ordered (5' tail + arm), `anneal` (the template-complementary part), its Tm, GC and binding span |
| `reverse` | any |  | the reverse primer, same shape |
| `product` | string |  | the edited molecule these primers produce after amplification and KLD re-circularisation — wire it into a digest, a gel or a map |
| `kind` | string |  | what the engine classified this as: deletion, insertion or replacement |
| `deletedLength` | number | bp | bases removed |
| `insertedLength` | number | bp | bases added |
| `editSpan` | any |  | the span edited on the ORIGINAL template, 0-based half-open. Empty for a pure insertion, which removes nothing |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_indel_primers",
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

### detect_trace_indel

**Detect trace indel**: _Does this trace split into two reads of different length, as a heterozygous indel does?_

Ask whether a Sanger trace splits into TWO READS OF DIFFERENT LENGTH, which is what a heterozygous insertion or deletion does: clean up to the indel, then a superposition of two sequences offset by its length. This is not mixed-base calling — that asks whether two BASES sit at one position and is blind to a length difference. Emits where the split starts, how long it is, and the two allele sequences the trace deconvolves into, so a pipeline can gate on the answer or carry either allele onward.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- TraceTuner's indel detection on its calibration table.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace file to read: its name (`read_F.ab1`) or its project file id. LEAVE IT EMPTY to run on the chromatogram tab that is open, in which case the answer also appears in the rail. A file id is project-specific, so a template ships this unset. |
| `table` | `"3700pop5"` · `"3700pop6"` · `"3100pop6"` · `"3730pop7"` |  | `"3730pop7"` |  | the instrument and polymer the quality scale was calibrated on. There is no universal default: a base scores differently under a different table, and the detector gates on a quality JUMP. |
| `quality_value_reading` | `"corrected"` · `"upstream"` |  | `"corrected"` |  | corrected = read the quality values as TraceTuner's own header declares them, which is the only reading that can detect anything; upstream = reproduce the program as shipped, whose detector never fires. |
| `breakpoint_scan` | number |  | `-1` | ≥ -1 | skip the search and measure the indel at this scan position on the x axis. -1 searches for it. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `found` | boolean |  | whether a heterozygous indel was detected. Wire it into a gate |
| `startsAtBase` | number |  | the 1-based base the split starts at, or 0 when none was found |
| `sizeInBases` | number |  | how many bases the longer allele carries that the shorter one does not |
| `longAllele` | string |  | the allele with the extra bases, from the breakpoint on. N marks a position the deconvolution would not commit to, not a low-quality base |
| `shortAllele` | string |  | the allele without them, from the breakpoint on |
| `qualityJump` | number |  | the drop in quality values across the breakpoint. It must exceed 7 for a position to be considered at all, so this is what a negative answer is checkable against |
| `report` | any |  | the whole finding, including the size in scans and the stutter verdict |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "detect_trace_indel",
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

### fold_guide

**Fold guide**: _Does a spacer base-pair into its sgRNA scaffold, and what does the whole guide RNA fold into?_

Fold a guide RNA — the spacer alone, and the whole sgRNA on a real published scaffold — and report which bases of the spacer pair with the scaffold. A spacer that base-pairs into the scaffold disrupts the structure Cas9 binds, which is a physical cause of a dead guide rather than a score. Every free energy is a minimum-free-energy fold under the Turner 2004 nearest-neighbour parameters, in kcal/mol, cross-checked against ViennaRNA 2.7.2.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Turner 2004 nearest-neighbour parameters; the scaffold is one of the published ones we ship.

**Does not:**
- A minimum-free-energy fold, not an ensemble; co-transcriptional folding is not modelled.
- Without a sourced scaffold for the nuclease it folds the spacer alone and says so.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `spacer` | string | **yes** |  |  | the protospacer to fold. |
| `nuclease` | `"SpCas9"` · `"SpCas9-NG"` · `"SpG"` · `"SpRY"` · `"xCas9"` · `"SaCas9"` · `"SaCas9-KKH"` · `"AsCas12a"` · `"LbCas12a"` · `"enAsCas12a"` |  | `"SpCas9"` |  | picks the scaffold published for that nuclease. Values: SpCas9 (SpCas9: NGG (3')), SpCas9-NG (SpCas9-NG: NG (3')), SpG (SpG: NGN (3')), SpRY (SpRY: NRN (3')), xCas9 (xCas9: NG (3')), SaCas9 (SaCas9: NNGRRT (3')), SaCas9-KKH (SaCas9-KKH: NNNRRT (3')), AsCas12a (AsCas12a: TTTV (5')), LbCas12a (LbCas12a: TTTV (5')), enAsCas12a (enAsCas12a: TTTV (5')). |
| `sg_rna` | boolean |  | `true` |  | also fold the full spacer+scaffold sgRNA, not just the spacer. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `spacer` | any |  | the spacer's own fold: sequence, dot-bracket structure and free energy |
| `sgRna` | any |  | the full sgRNA fold, when a scaffold is published for this nuclease |
| `spacerScaffoldPairs` | number or null |  | how many spacer bases pair INTO the scaffold — every one of them disrupts the structure Cas9 binds. Null when no scaffold is published for this nuclease |
| `scaffoldIntact` | boolean or null |  | whether the scaffold still folds as published once the spacer is attached. Null when no scaffold is published for this nuclease: false would read as a disrupted scaffold |
| `scaffoldName` | string or null |  | which published scaffold was used. Null when no scaffold is published for this nuclease |
| `unavailable` | string or null |  | why nothing was folded, when no scaffold is published for this nuclease; null when the fold ran |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fold_guide",
  "arguments": {
    "spacer": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### list_sgrna_scaffolds

**List sgRNA scaffolds**: _Which sgRNA scaffolds has this workbench sourced, for which nucleases, from which publication?_

Every sgRNA scaffold this workbench has sourced, with the nucleases each covers and the publication it comes from. A scaffold not listed here is one we do not have — the list is what we ship, not what exists.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- The list is what we ship, not what exists; a scaffold absent here is one we have not sourced.

**No scientific claim:** Lists the scaffolds we have sourced with their citations; it computes nothing.

**Arguments**

_No arguments beyond the shared `_subject` and `_files`._

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `scaffolds` | any |  | each scaffold: id, name, sequence, length, which side of the spacer it sits, the nucleases it covers, its citation and accessions |
| `count` | number |  | how many scaffolds are shipped |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_sgrna_scaffolds",
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

### peptide_mass

**Peptide mass**: _What is this peptide's monoisotopic and average mass, and its m/z at each charge?_

Monoisotopic and average mass of a peptide, and its m/z at each charge state (validated against pyteomics). Plain one-letter sequences also take an ion type (b, y, c, z, a, x and their neutral-loss forms); a ProForma peptidoform with modification tags, as masses or Unimod names and accessions (e.g. [TMT6plex]-PEPTM[Oxidation]IDE, M[UNIMOD:35], M[+15.994915]), is weighed monoisotopically with its modifications.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Element masses are the standard tables'; ProForma tags resolve to the modification masses named.

**Does not:**
- A calculated mass, not a measured one; isotope distribution is isotope_envelope's question.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string | **yes** |  |  | peptide: one-letter residues, optionally ProForma tags on residues and termini (a signed mass, a Unimod name, or UNIMOD:accession). |
| `ionType` | `"M"` · `"M-H2O"` · `"M-NH3"` · `"a"` · `"a+1"` · `"a-H2O"` · `"a-NH3"` · `"b"` · `"b-H2O"` · `"b-NH3"` · `"c"` · `"c-1"` · `"c-dot"` · `"c+1"` · `"c+2"` · `"c-H2O"` · `"c-NH3"` · `"x"` · `"x+1"` · `"x-H2O"` · `"x-NH3"` · `"y"` · `"y-H2O"` · `"y-NH3"` · `"z-1"` · `"z"` · `"z-dot"` · `"z+1"` · `"z+2"` · `"z+3"` · `"z-H2O"` · `"z-NH3"` |  | `"M"` |  | weigh the peptide as this ion; M is the intact molecule. Plain sequences only. |
| `charges` | number[] |  | `[1, 2, 3]` |  | charge states to report m/z for (positive integers). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `monoisotopic` | number or null | Da | neutral monoisotopic mass (Da) |
| `average` | number or null | Da | neutral average mass (Da); null for a peptidoform with modification tags |
| `mz` | any |  | per charge: monoisotopic and average m/z |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "peptide_mass",
  "arguments": {
    "sequence": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### protein_signal_peptide

**Protein signal peptide**: _Where would signal peptidase cut this protein, by von Heijne's weight matrix?_

Signal-peptidase cleavage sites in a protein, by von Heijne's (1986) weight matrix as implemented by EMBOSS sigcleave. Scores a 15-residue window at every position (the 13 residues before the cut plus the first two after) against either the eukaryotic or the prokaryotic training set. Predicts WHERE the cut would fall, not WHETHER the protein is secreted — a high score away from the N-terminus is a look-alike, not a secretion call.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The training set chosen (eukaryotic or prokaryotic) matches the protein's origin.

**Does not:**
- Predicts WHERE a cut would fall, not WHETHER the protein is secreted.
- A 1986 matrix, not a trained modern predictor.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (unambiguous one-letter codes); wire it from translate_sequence. |
| `kingdom` | `"eukaryote"` · `"prokaryote"` |  | `"eukaryote"` |  | which of von Heijne's training sets to score against: 161 aligned eukaryotic or 36 prokaryotic signal peptides. Pick the one matching the EXPRESSION HOST — the two disagree by several points on the same sequence. |
| `minWeight` | number |  | `3.5` |  | report sites scoring strictly above this. EMBOSS's default of 3.5 finds ~95% of real signal peptides and rejects ~95% of non-signal sequences. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sites` | any |  | every site above the threshold, best first: { cleavageAfter, score, start, end, window, maturePeptide } |
| `cleavageAfter` | number |  | 1-based residue the best site cuts after; the mature chain starts at the next one. 0 when nothing cleared the threshold |
| `score` | number |  | the best site's score — a sum of 15 log-odds, NOT a probability |
| `signalPeptide` | string |  | residues 1..cleavageAfter, the predicted signal peptide |
| `maturePeptide` | string |  | the predicted mature chain, from the cleavage site to the end |
| `siteCount` | number |  | how many sites cleared the threshold |
| `scores` | any |  | the score at every position, thresholded or not — the series a plot draws |
| `matrix` | string |  | which training set was used, and how many peptides it was built from |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_signal_peptide",
  "arguments": {
    "protein": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### quantify_base_editing

**Quantify base editing**: _What fraction of each base in the guide window was edited, from one trace (EditR)?_

Quantify BASE EDITING from a single Sanger trace, with no control read — the EditR method (Kluesner et al. 2018), graded against the authors' own R. A base editor makes no double-strand break and no indel, so it is invisible to ICE and TIDE: the edit is a C→T or A→G inside the protospacer that shows up only as a second peak under the called base. This models the trace's OWN background from the positions outside the guide, then p-values every base of the guide against it. Emits the significant calls, so a pipeline can gate on whether editing happened and at which position.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- EditR's (Kluesner et al. 2018) zero-adjusted gamma model of background noise.

**Does not:**
- One trace, no control; edits outside the guide window are not scored.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace file to read: its name (`read_F.ab1`) or its project file id. LEAVE IT EMPTY to run on the chromatogram tab that is open. A file id is project-specific, so a template ships this unset. |
| `guide` | string | **yes** |  |  | the protospacer, 5'→3', without the PAM. Matched exactly against the read's own base calls; the coordinates it lands on come back in the result. |
| `guide_is_reverse_complement` | boolean |  | `false` |  | search for the guide's reverse complement. A C→T edit on the guide strand then reads as G→A in the result. |
| `p_value_cutoff` | number |  | `0.01` | 1e-07–0.5 | a base is called as edited when its share of the position's signal clears this trace's own noise model at this probability. EditR's own default is 0.01. |
| `trim5` | number |  |  | ≥ 1 | first base of the read the background model may be fitted on, 1-based inclusive. GIVE BOTH BOUNDS OR NEITHER — upstream errors on a lone one rather than filling the other in. Left unset, upstream's automatic rule runs: drop the first 20 bases, then drop every base whose total peak height is under a tenth of the mean of what is left. The window is an INPUT to the answer, not a view: it is what the noise is estimated from, so tightening it lowers the cut-off. |
| `trim3` | number |  |  | ≥ 1 | last base of the read the background model may be fitted on, 1-based inclusive. Pair it with `trim5`. |
| `guide_start` | number |  |  | ≥ 1 | place the guide yourself, 1-based inclusive in the read's own base calls, instead of matching it exactly. GIVE BOTH BOUNDS OR NEITHER. This is what a read carrying a sequencing error inside the protospacer needs: the analysis tests the bases you point at rather than refusing the read. |
| `guide_end` | number |  |  | ≥ 1 | the other end of an explicit placement, 1-based inclusive. Pair it with `guide_start`. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `edited` | boolean |  | whether ANY base of the guide carries a non-reference signal above this trace's own noise. Wire it into a gate |
| `topPosition` | number |  | the guide position (1-based) of the biggest call, or 0 when there is none |
| `topChange` | string |  | the biggest call as `reference→edited`, e.g. `C→T`. Empty when there is none |
| `topPercent` | number |  | its share of that position's total peak height, 0–100 |
| `guideStart` | number |  | 1-based position in the read's own base calls where the guide was found — what a canvas needs to draw it |
| `calls` | any |  | every significant call: { guidePosition, index, guideBase, base, percent, pValue }, biggest first |
| `report` | any |  | the whole run: every guide position with all four base percentages and p-values, the four fitted noise models and their cut-off lines. This is what makes a negative checkable — 'no editing' and 'the model could never have fired' look identical without it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "quantify_base_editing",
  "arguments": {
    "guide": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### screen_contamination

**Screen contamination**: _Does this sequence carry vector, adapter, linker or primer contamination from UniVec, and how strong is each match?_

Screen a nucleotide sequence for vector, adapter, linker and primer contamination against NCBI's UniVec, using VecScreen's own BLASTn parameters and category rules. Reports every match graded Strong/Moderate/Weak plus the short 'suspect origin' stretches NCBI asks to be removed with the vector, and emits both the N-masked sequence and the longest clean region so a pipeline can gate on the result or carry the clean part onward.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- VecScreen's own blastn parameters and Strong/Moderate/Weak category rules.
- The UniVec build named (core or full).

**Does not:**
- Finds only what UniVec holds; a contaminant missing from it reads as clean.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the nucleotide sequence to screen; leave empty to screen the open record. A protein sequence is refused — this is a nucleotide search. |
| `build` | `"core"` · `"full"` |  | `"core"` |  | which UniVec build to search: 'core' is NCBI's curated 3,155-segment subset and is what routine screening should use; 'full' is the complete 6,111-segment set — more sensitive, and more redundant hits. |
| `reward` | number |  | `1` | 1–10 | score for a matching base (`-reward`). Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `penalty` | number |  | `-5` | -20–-1 | score for a mismatching base, NEGATIVE (`-penalty`). With reward 1 and penalty −5 only a near-exact stretch can score above the reporting floor, which is what makes VecScreen specific. Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `gap_open` | number |  | `3` | 0–20 | cost to open a gap (`-gapopen`); a gap of length k costs `gapopen + k * gapextend`. Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `gap_extend` | number |  | `3` | 0–20 | cost per gapped base (`-gapextend`). Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `word_size` | number |  | `11` | 4–32 | exact-match seed length (`-word_size`). A sequence shorter than this cannot be screened at all, and the engine says so. Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `x_drop_ungapped` | number |  | `11` | 5–100 | X-drop for ungapped extension, in score units. It bounds extension; it does not change which alignment is optimal. Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `x_drop_gapped` | number |  | `14` | 5–150 | X-drop for the preliminary gapped pass, in score units (`-xdrop_gap`, converted); capped at each seed’s own ungapped score. Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `x_drop_gapped_final` | number |  | `49` | 5–300 | X-drop for the traceback that produces the reported alignment, in score units (`-xdrop_gap_final`, converted). Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `ungapped_cutoff` | number |  | `13` | 1–100 | lowest ungapped score that sends a seed to gapped extension — blastn’s gap trigger, converted from 27 bits. Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `min_score` | number |  | `16` | 5–100 | lowest raw score worth reporting — VecScreen's weakest reportable match. Lowering it reports more and specifies less. Default is NCBI's published VecScreen setting; changing it means the result is no longer VecScreen's. Advanced. |
| `dust` | boolean |  | `true` |  | mask low-complexity sequence for SEEDING only (`-dust yes -soft_masking true`): a seed may not START in masked sequence, but an extension may run through it, so a genuine match spanning a repeat is not truncated. Advanced. |
| `terminal_strong` | number |  | `24` | 1–200 | raw score at or above which a terminal match is graded Strong. A terminal match — one reaching within `terminal_distance` of an end of the query or of another reported region — is believed on less evidence than an internal one, which is why the two ladders differ. Each ladder must stay in order (strong >= moderate >= weak) or the lower rungs become unreachable, and the run is refused rather than graded. Advanced. |
| `terminal_moderate` | number |  | `19` | 1–200 | raw score at or above which a terminal match is graded Moderate. Each ladder must stay in order (strong >= moderate >= weak) or the lower rungs become unreachable, and the run is refused rather than graded. Advanced. |
| `terminal_weak` | number |  | `16` | 1–200 | raw score at or above which a terminal match is reported at all, as Weak. Below this a terminal match is not reported. Each ladder must stay in order (strong >= moderate >= weak) or the lower rungs become unreachable, and the run is refused rather than graded. Advanced. |
| `internal_strong` | number |  | `30` | 1–200 | raw score at or above which an internal match — one that is not terminal — is graded Strong. Each ladder must stay in order (strong >= moderate >= weak) or the lower rungs become unreachable, and the run is refused rather than graded. Advanced. |
| `internal_moderate` | number |  | `25` | 1–200 | raw score at or above which an internal match is graded Moderate. Each ladder must stay in order (strong >= moderate >= weak) or the lower rungs become unreachable, and the run is refused rather than graded. Advanced. |
| `internal_weak` | number |  | `23` | 1–200 | raw score at or above which an internal match is reported at all, as Weak. NCBI leaves a deliberate gap here: an internal match scoring 16-22 is not reportable, because an internal match needs more evidence than a terminal one. Each ladder must stay in order (strong >= moderate >= weak) or the lower rungs become unreachable, and the run is refused rather than graded. Advanced. |
| `terminal_distance` | number |  | `25` | 0–500 | how close to an end of the query — or to another reported region — a match must reach to count as terminal and be graded on the lower of the two ladders. NCBI's published value is 25 bases. Advanced. |
| `suspect_origin_max` | number |  | `50` | 0–500 | length under which a stretch of non-vector sequence stranded between two matches (or between a match and an end) is reported as 'suspect origin' — too short to have come from anywhere trustworthy, so NCBI asks for it to be removed with the vector. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `worst` | string |  | the highest category present — strong \| moderate \| weak \| suspect — or 'clean' when nothing was found. The slot to branch a pipeline on |
| `contaminatedPct` | number | % | percentage of the query covered by at least one reported match — the slot to gate on numerically |
| `segments` | any |  | the merged contaminated regions, each with its coordinates and category — what the map draws |
| `matches` | any |  | every raw match, one per database record: coordinates, strand, score and the UniVec entry hit |
| `maskedSequence` | string |  | the query with every match and suspect-origin stretch replaced by N — the form NCBI asks a submitter to upload |
| `cleanSequence` | string |  | the longest stretch carrying no match at all — wire it onward when the screen is a trimming step rather than a gate. Empty when nothing clean is left |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "screen_contamination",
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

### screen_guides

**Screen guides**: _Which guide spacers fail the pre-acceptance screens: GC, self-complementary hairpins, and hairpins against the sgRNA backbone?_

Screen guide spacers the way CHOPCHOP does before it accepts them: GC gate, self-complementary hairpins inside the spacer, and hairpins against the sgRNA backbone. A guide that folds onto its own scaffold is loaded into Cas9 poorly however good its on-target score is, so this is the check that explains a guide with a good score and no activity.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The screens are CHOPCHOP's, with the Thyme 2016 thresholds and backbones.

**Does not:**
- A screen explains a dead guide; passing it does not predict activity.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `spacers` | string[] | **yes** |  |  | the protospacers to screen (20 nt for SpCas9) — wire `topSpacer` or the spacers out of a design run, or list them. |
| `backbone` | `"original"` · `"extended"` |  | `"original"` |  | which sgRNA backbone the spacer will be cloned into — the hairpin test is against this. Values: original (original gRNA backbone), extended (extended backbone (Cas9-GFP tracking)). |
| `gg` | boolean |  | `false` |  | the construct starts the transcript GG — upstream's `-gg` REPLACES the spacer's first two bases with G (T7 preference), it does not lengthen it. Advanced. |
| `pre_g` | boolean |  | `false` |  | the construct prepends a single 5' G (upstream's `-preG`) — this one lengthens the scanned string, and upstream's fixed 17-window loop then never reaches its last bases. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `screened` | any |  | per spacer: GC, whether it was dropped by the GC gate, the two hairpin verdicts, and every flagged 4-mer with its position |
| `clean` | any |  | the spacers that passed the GC gate and flagged no hairpin — the ones to take forward |
| `counts` | any |  | upstream's own four summary counts: total, after the GC screen, with a self hairpin, with a backbone hairpin |
| `backboneLabel` | string |  | which backbone the run screened against |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "screen_guides",
  "arguments": {
    "spacers": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### screen_molecule_library

**Screen molecule library**: _How does each structure of this library fare against these rules and alerts?_

Screen every structure of a library at once against drug-likeness rules and structural-alert catalogs, as the library grid does, and bin one rule property across it, split at the bound of a chosen rule. Returns, per 0-based structure, the rules it breaks and the alerts it trips, and the binned distribution with how many structures fall within the bound.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's descriptors and medchem's rule and alert definitions.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the library: one SMILES or molfile per entry. |
| `rules` | (`"rule_of_five"` · `"rule_of_five_beyond"` · `"rule_of_four"` · `"rule_of_three"` · `"rule_of_three_extended"` · `"rule_of_two"` · `"rule_of_ghose"` · `"rule_of_veber"` · `"rule_of_reos"` · `"rule_of_chemaxon_druglikeness"` · `"rule_of_egan"` · `"rule_of_pfizer_3_75"` · `"rule_of_gsk_4_400"` · `"rule_of_oprea"` · `"rule_of_xu"` · `"rule_of_cns"` · `"rule_of_respiratory"` · `"rule_of_five_paper"` · `"rule_of_ghose_paper"` · `"rule_of_reos_paper"`)[] |  | `["rule_of_five", "rule_of_five_beyond", "rule_of_four", "rule_of_three", "rule_of_three_extended", "rule_of_two", "rule_of_ghose", "rule_of_veber", "rule_of_reos", "rule_of_chemaxon_druglikeness", "rule_of_egan", "rule_of_pfizer_3_75", "rule_of_gsk_4_400", "rule_of_oprea", "rule_of_xu", "rule_of_cns", "rule_of_respiratory", "rule_of_five_paper", "rule_of_ghose_paper", "rule_of_reos_paper"]` |  | which drug-likeness rules to screen, by id. Every rule by default. |
| `alert_sets` | (`"PAINS_A"` · `"PAINS_B"` · `"PAINS_C"` · `"BRENK"` · `"NIH"` · `"ZINC"` · `"CHEMBL_Glaxo"` · `"CHEMBL_Dundee"` · `"CHEMBL_BMS"` · `"CHEMBL_MLSMR"` · `"CHEMBL_Inpharmatica"` · `"CHEMBL_LINT"` · `"CHEMBL_SureChEMBL"`)[] |  | `["PAINS_A", "PAINS_B", "PAINS_C", "BRENK", "NIH", "ZINC", "CHEMBL_Glaxo", "CHEMBL_Dundee", "CHEMBL_BMS", "CHEMBL_MLSMR", "CHEMBL_Inpharmatica", "CHEMBL_LINT", "CHEMBL_SureChEMBL"]` |  | which structural-alert catalogs to screen against. Empty screens nothing. |
| `property` | `"mw"` · `"clogp"` · `"hbd"` · `"hba"` · `"lipinskiHbd"` · `"lipinskiHba"` · `"hbonds"` · `"tpsa"` · `"rotatableBonds"` · `"rings"` · `"heavyAtoms"` · `"numAtoms"` · `"molarRefractivity"` · `"averageMw"` · `"totalAtoms"` · `"formalCharge"` |  | `"mw"` |  | the rule property to bin, at the value the rules judged. Values: mw (Monoisotopic mass), clogp (cLogP (Crippen)), hbd (H-bond donors), hba (H-bond acceptors), lipinskiHbd (Lipinski donors (NH + OH)), lipinskiHba (Lipinski acceptors (N + O)), hbonds (Donors + acceptors), tpsa (TPSA (N and O only)), rotatableBonds (Rotatable bonds), rings (Rings), heavyAtoms (Heavy atoms), numAtoms (Atoms in the graph), molarRefractivity (Molar refractivity (Crippen)), averageMw (Molecular weight (average)), totalAtoms (Atoms, hydrogens included), formalCharge (Net formal charge). |
| `split_rule` | `"rule_of_five"` · `"rule_of_five_beyond"` · `"rule_of_four"` · `"rule_of_three"` · `"rule_of_three_extended"` · `"rule_of_two"` · `"rule_of_ghose"` · `"rule_of_veber"` · `"rule_of_reos"` · `"rule_of_chemaxon_druglikeness"` · `"rule_of_egan"` · `"rule_of_pfizer_3_75"` · `"rule_of_gsk_4_400"` · `"rule_of_oprea"` · `"rule_of_xu"` · `"rule_of_cns"` · `"rule_of_respiratory"` · `"rule_of_five_paper"` · `"rule_of_ghose_paper"` · `"rule_of_reos_paper"` |  |  |  | the rule whose bound on that property splits each bar; the first screened rule bounding it by default. Values: rule_of_five (Lipinski rule of five), rule_of_five_beyond (Beyond rule of five), rule_of_four (Rule of four (PPI inhibitors)), rule_of_three (Rule of three (fragments)), rule_of_three_extended (Rule of three, extended), rule_of_two (Rule of two (building blocks)), rule_of_ghose (Ghose filter), rule_of_veber (Veber filter), rule_of_reos (REOS), rule_of_chemaxon_druglikeness (ChemAxon drug-likeness), rule_of_egan (Egan filter), rule_of_pfizer_3_75 (Pfizer 3/75), rule_of_gsk_4_400 (GSK 4/400), rule_of_oprea (Oprea lead-likeness), rule_of_xu (Xu drug-like index), rule_of_cns (CNS penetration), rule_of_respiratory (Respiratory (inhaled/nasal)), rule_of_five_paper (Lipinski rule of five (paper: average MW)), rule_of_ghose_paper (Ghose filter (paper: all atoms, average MW)), rule_of_reos_paper (REOS (paper: net charge bounded, average MW)). |
| `bins` | number |  | `8` | ≥ 1 | how many bins. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many structures pass clean, and how many fall within the split bound |
| `rows` | any |  | per structure: 0-based index, canonical SMILES, rules broken, alerts tripped |
| `distribution` | any |  | the bins (lo, hi, within, outside), the bounds on the property and the split |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "screen_molecule_library",
  "arguments": {
    "molecules": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### screen_oligo_structure

**Screen oligo structure**: _Which oligos in a set form hairpins, self-dimers or cross-dimers, at any position and at the 3' end?_

Fold a set of oligos and check them against each other: every oligo's hairpin, its self-dimer anywhere and its self-dimer at the 3' end, plus the cross-dimer with every other oligo in the set, at any position and at a 3' end. This is primer3's `thal` — the same engine the Tm columns elsewhere use — so a pool can be screened before it is ordered rather than explained after a gel. The 3'-end measures are the ones that matter for a primer-dimer BAND, because only a paired 3' end extends. Works on any oligo: primers, probes, ssODN donors, guides, adapters.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Free energies and melting temperatures are primer3 thal's at the stated conditions.

**Does not:**
- A dimer's free energy is a thermodynamic score, not a measured yield of primer-dimer.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `oligos` | string[] | **yes** |  |  | the oligos to screen, 5'→3'. One is a valid pool: it still gets its hairpin and self-dimer. Wire the primers out of a design run, or list them. |
| `names` | string[] |  |  |  | optional labels, in the same order as `oligos` — what the pair table calls each one. Missing or short, the rest are numbered. Advanced. |
| `mv_conc` | number |  | `50` | 0–1000 | monovalent cations (Na⁺ + K⁺ + Tris⁺), mM. In mM. |
| `dv_conc` | number |  | `1.5` | 0–200 | divalent cations (Mg²⁺), mM. In mM. |
| `dntp_conc` | number |  | `0.6` | 0–100 | total dNTPs, mM — subtracted from the divalent term, because dNTPs chelate Mg²⁺. In mM. |
| `dna_conc` | number |  | `50` | 0.01–10000 | oligo strand concentration, nM — it moves a DIMER's Tm and leaves a hairpin's alone, because a hairpin is unimolecular. In nM. |
| `temperature` | number |  | `37` | -20–100 | the temperature ΔG is evaluated at. It does NOT move any Tm — Tm is the structure's own melting point — so change it to read ΔG at your annealing temperature. In °C. Advanced. |
| `max_loop` | number |  | `30` | 0–30 | largest internal loop the alignment will span (primer3's MAX_LOOP). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `perOligo` | any |  | per oligo: its hairpin, its self-dimer anywhere and its 3'-end self-dimer, each with ΔG, ΔH, ΔS, Tm, the limit it was graded against and whether it exceeds it — plus primer3's own drawing of the pairing, so a number can be checked rather than trusted |
| `pairs` | any |  | every unordered pair INCLUDING the self diagonal, with the any-position and 3'-end cross-dimer and which oligo's 3' end the reported end measure belongs to |
| `flagged` | any |  | only the oligos and pairs that broke a limit, with which limit — the list to act on. Empty is a real result and means every measure sat under primer3's cutoffs |
| `clean` | any |  | the oligos that broke no limit of their own AND appear in no flagged pair — the ones to order. An oligo is dropped from here for a partner's sake, which is the point of screening a POOL |
| `worstEndTmC` | number | °C | the highest 3'-end dimer melting temperature in the set — the single number that predicts a primer-dimer band. Self-dimers count, because an oligo dimerising with itself makes a band too. 0 means no 3'-anchored alignment was found at all, not that the set is safe |
| `worstAnyTmC` | number | °C | the highest any-position dimer melting temperature in the set, self-dimers included |
| `worstHairpinTmC` | number | °C | the highest hairpin melting temperature across the oligos — a hairpin melting above the annealing temperature competes with the template |
| `incompatibleCount` | number |  | how many DISTINCT pairs broke a limit — the self diagonal excluded, because a single oligo's self-dimer is not a pair problem and counting it makes a one-oligo run report an incompatibility. Branch a workflow on this rather than re-deriving it from `pairs`; read `flagged` for the self-structures |
| `limits` | any |  | the five primer3 cutoffs every verdict here was made against, and the settings file they come from — a verdict whose threshold is not stated is not checkable (§10a) |
| `conditions` | any |  | the buffer every number here was computed in, including the values left at their default — so a result carries its own reaction rather than an unstated one |
| `provenance` | any |  | which primer3 this engine IS, and which one a user comparing against primer3web or bioconda `ntthal` is holding. The two generations disagree on about 3% of primer-length oligos |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "screen_oligo_structure",
  "arguments": {
    "oligos": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### search_off_targets

**Search off targets**: _Which sites in this sequence could a guide also cut, and how specific is the guide within it?_

Search a sequence for sites a guide could also cut, allowing mismatches, and score each one (MIT and CFD) plus the aggregate specificity of the guide WITHIN that sequence. This is specificity against what you searched — it is not a genome-wide score, and it says so rather than inventing one.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Mismatches are allowed up to the limit given; bulges only when asked.
- MIT and CFD are the published scoring schemes.

**Does not:**
- Specificity is against the sequence searched: it is not a genome-wide score, and it states that.
- A site found is a possible cut, not a measured one.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `spacer` | string | **yes** |  |  | the protospacer to search for (20 nt for SpCas9). |
| `subject` | string |  |  |  | the sequence to search — wire a record or name a library document; leave unset to search the open record. |
| `nuclease` | `"SpCas9"` · `"SpCas9-NG"` · `"SpG"` · `"SpRY"` · `"xCas9"` · `"SaCas9"` · `"SaCas9-KKH"` · `"AsCas12a"` · `"LbCas12a"` · `"enAsCas12a"` |  | `"SpCas9"` |  | which nuclease's PAM and geometry to use. Values: SpCas9 (SpCas9: NGG (3')), SpCas9-NG (SpCas9-NG: NG (3')), SpG (SpG: NGN (3')), SpRY (SpRY: NRN (3')), xCas9 (xCas9: NG (3')), SaCas9 (SaCas9: NNGRRT (3')), SaCas9-KKH (SaCas9-KKH: NNNRRT (3')), AsCas12a (AsCas12a: TTTV (5')), LbCas12a (LbCas12a: TTTV (5')), enAsCas12a (enAsCas12a: TTTV (5')). |
| `max_mismatches` | number |  | `3` | 0–6 | how many mismatches a site may carry and still be reported. |
| `limit` | number |  | `200` | 0–5000 | cap the rows returned (hits come back worst-first: fewest mismatches). 0 = all. Advanced. |
| `dna_bulge` | number |  | `0` | 0–2 | extra bases in the DNA a site may carry (a gap opened in the guide). 0 searches mismatches only. The ceiling is the width a golden oracle covers, and a bulged hit outside that envelope reports `validated: false` for itself. In nt. Advanced. |
| `rna_bulge` | number |  | `0` | 0–1 | extra bases in the guide a site may carry (a gap opened in the DNA). Same envelope as `dna_bulge`. In nt. Advanced. |
| `circular` | boolean |  | `false` |  | search across the origin as well. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | each candidate site: position, strand, mismatches, the PAM found, and its MIT/CFD scores |
| `total` | number |  | sites found before `limit` was applied |
| `byMismatch` | any |  | how many sites carry 0, 1, 2 … mismatches — the census a specificity read needs |
| `mitSpecificity` | number or null |  | aggregate MIT specificity within the searched sequence, 0-100 (null when the nuclease geometry is unscored) |
| `cfdSpecificity` | number or null |  | aggregate CFD specificity within the searched sequence, 0-100: the same Hsu-form aggregate over each site's CFD score (null when the nuclease geometry is unscored) |
| `scored` | boolean |  | false when this nuclease has no published MIT/CFD model — the hits are still real, the scores are absent |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "search_off_targets",
  "arguments": {
    "spacer": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### survey_off_targets

**Survey off targets**: _How many off-target sites, by mismatch class, does each of these spacers have in this sequence?_

Count every guide's off-target sites by mismatch class across one sequence, in one pass — the question that comes BEFORE opening any single guide's site table: which of these spacers is worth looking at. Returns counts and the aggregate specificity per spacer, never the sites themselves, so a few hundred spacers cost a few hundred rows rather than a few hundred thousand.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The same search rule as search_off_targets, run once per spacer.

**Does not:**
- Counts and the aggregate specificity only, never the sites; and within the sequence searched, not a genome.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `spacers` | string[] | **yes** |  |  | the protospacers to count — wire the spacers out of a design run, or list them. |
| `subject` | string |  |  |  | the sequence to search — wire a record or name a library document; leave unset to search the open record. |
| `nuclease` | `"SpCas9"` · `"SpCas9-NG"` · `"SpG"` · `"SpRY"` · `"xCas9"` · `"SaCas9"` · `"SaCas9-KKH"` · `"AsCas12a"` · `"LbCas12a"` · `"enAsCas12a"` |  | `"SpCas9"` |  | which nuclease's PAM and geometry to use. Values: SpCas9 (SpCas9: NGG (3')), SpCas9-NG (SpCas9-NG: NG (3')), SpG (SpG: NGN (3')), SpRY (SpRY: NRN (3')), xCas9 (xCas9: NG (3')), SaCas9 (SaCas9: NNGRRT (3')), SaCas9-KKH (SaCas9-KKH: NNNRRT (3')), AsCas12a (AsCas12a: TTTV (5')), LbCas12a (LbCas12a: TTTV (5')), enAsCas12a (enAsCas12a: TTTV (5')). |
| `max_mismatches` | number |  | `3` | 0–6 | how many mismatches a site may carry and still be counted. Every row is this many classes wide plus the exact one, so the rows line up. |
| `dna_bulge` | number |  | `0` | 0–2 | extra bases in the DNA a site may carry. 0 counts mismatches only. In nt. Advanced. |
| `rna_bulge` | number |  | `0` | 0–1 | extra bases in the guide a site may carry. Same envelope as `dna_bulge`. In nt. Advanced. |
| `circular` | boolean |  | `false` |  | count across the origin as well. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `spacers` | any |  | one row per spacer: its counts by mismatch class, its total, its off-target count and its aggregate MIT/CFD specificity within the searched sequence |
| `cleanest` | string |  | the spacer with the fewest off-target sites (ties broken by the higher CFD specificity) — empty when nothing could be counted |
| `counted` | number |  | how many distinct spacers were counted |
| `skipped` | any |  | spacers that could not be counted, each with the reason — never dropped in silence |
| `searched` | string |  | the sequence the counts are against, which is what makes them readable later |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "survey_off_targets",
  "arguments": {
    "spacers": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### tide_quantify_indels

**TIDE quantify indels**: _How abundant is each indel size in the edited population (TIDE)?_

Quantify a CRISPR edit from a pair of Sanger traces by TIDE (Brinkman et al.) — the abundance of each indel SIZE in the sequenced population, with a p-value per size class, the total editing efficiency, the goodness of fit, and the base composition of the +1 insertion. This is a different question from crispr_quantify_edits, not a cheaper version of it: ICE fits a mixture of whole proposed alleles and names them, TIDE fits the control trace shifted by n bases and so reports how much of the population shifted by n, whatever allele carried it. Run both on the same pair when the two disagree about how much was edited — that disagreement is information about the read.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- TIDE's (Brinkman et al.) decomposition window and p-value threshold given.

**Does not:**
- Indel sizes, not sequences.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `control` | string | **yes** |  |  | the UNEDITED trace, by file name or id — every indel class is the control trace shifted, so this read IS the model. |
| `edited` | string | **yes** |  |  | the EDITED trace, by file name or id. |
| `guide` | string | **yes** |  |  | the guide spacer, RNA accepted. TIDE decomposes around ONE break, so this is a single guide rather than a list — it is located in the control on either strand and the break is placed three bases 5-prime of the PAM. |
| `seq_start` | number |  | `100` | 1–1000 | first base of the READ to use. The start of a Sanger read is poor quality; upstream's own web app starts at 100. In bp. |
| `seq_end` | number |  | `700` | 10–2000 | last base of the READ to use, clamped down to the shorter of the two reads if it overruns. In bp. |
| `max_shift` | number |  | `10` | 2–50 | largest indel size modeled, in both directions. One basis function is fitted per size from -max_shift to +max_shift, so this bounds what can be reported at all. In bp. |
| `p_threshold` | number |  | `0.001` | 0–1 | an indel class is called PRESENT below this p-value. A 0% class and a non-significant class are different answers, which is why this is a knob rather than a constant. Advanced. |
| `window_start` | number |  | `115` | 0–2000 | first base of the decomposed region. 0 asks the engine to place the window after the break itself, which is what upstream does when given no boundaries. In bp. Advanced. |
| `window_end` | number |  | `685` | 0–2000 | last base of the decomposed region. 0 = as far as the shorter read allows. In bp. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `efficiency` | number |  | total editing efficiency: the R-squared-scaled signal in every non-zero indel class, 0-100. Not the same quantity as an ICE score — wire them into a comparison rather than treating either as the number |
| `rSquared` | number |  | goodness of fit of the whole decomposition. Every percentage below is already scaled by it, so a low fit shrinks the classes rather than flagging them |
| `breaksite` | number |  | the base the break was placed at, three bases 5-prime of the PAM. Every window in the result is positioned against it |
| `indels` | any |  | every modeled size from -max_shift to +max_shift with its percentage, p-value and whether it cleared the threshold — INCLUDING the classes that did not, so the spectrum has a shape and not only peaks |
| `significantIndels` | any |  | the classes that cleared p_threshold, excluding the unmodified class — what a gate should read |
| `insertionBases` | any |  | base composition of the +1 insertion as percentages in A, C, G, T order — the readout ICE cannot produce. Null when there is no significant +1 class, which is the common case and not an error; `insertionNote` then says why in upstream’s own words |
| `aberrantSignal` | any |  | the four means TIDE's own quality checklist is read from: control and sample, before and after the break. A sample already aberrant BEFORE the break is a sequencing problem rather than an edit, and this is the pair of numbers that says so |
| `report` | any |  | the whole result, including the window corrections upstream raises as warnings |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "tide_quantify_indels",
  "arguments": {
    "control": "<string>",
    "edited": "<string>",
    "guide": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
