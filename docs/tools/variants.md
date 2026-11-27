# 🧫 Genomics, variants & copy number

_Variant calls, copy-number segmentation, LOH and mosaicism, genome regions._

23 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`apply_variant_call`](#apply_variant_call) | What sequence results from substituting this called ALT allele? |
| [`browse_region`](#browse_region) | What does this window of the genome hold: bands, transcripts and nuclease sites? |
| [`check_invariants`](#check_invariants) | Is this designed sequence admissible: protein unchanged, forbidden sites absent, frame intact, length, GC and CAI within bounds? |
| [`compare_flow_cytometry_populations`](#compare_flow_cytometry_populations) | Does this channel differ between these two populations, and by which test? |
| [`copy_number_allele_split`](#copy_number_allele_split) | What major and minor allele copy number does each segment carry? |
| [`copy_number_compare`](#copy_number_compare) | Which copy-number events do two samples share, and which only one carries? |
| [`copy_number_findings`](#copy_number_findings) | Which gains, losses and runs of homozygosity did the file's producer call? |
| [`copy_number_loh`](#copy_number_loh) | Where is heterozygosity lost, recomputed from the array's own genotype calls? |
| [`copy_number_mosaicism`](#copy_number_mosaicism) | Which mosaic fraction class is each region of this chromosome closest to? |
| [`copy_number_read`](#copy_number_read) | What does this Affymetrix copy-number file hold: algorithm, array, data sets and per-marker values? |
| [`copy_number_regions`](#copy_number_regions) | Which of the sample's own calls fall in each ClinGen curated region? |
| [`copy_number_segment`](#copy_number_segment) | Where are the breakpoints in this chromosome's copy-number signal, by each method named? |
| [`copy_number_somatic`](#copy_number_somatic) | What somatic-mutation calls does this array result carry? |
| [`design_expression_variants`](#design_expression_variants) | Which codon-optimised variants of this CDS does an expression trial need, and how do they differ? |
| [`export_flow_cytometry_population`](#export_flow_cytometry_population) | Give me this population's events as a file another tool can open. |
| [`lookup_variant`](#lookup_variant) | What does the authority named return for this variant? |
| [`population_ancestry`](#population_ancestry) | What mixture of K ancestral populations does each sample look like, and which K does cross-entropy prefer? |
| [`population_fst`](#population_fst) | How differentiated are these populations, per site and averaged, with a jackknife standard error? |
| [`population_site_stats`](#population_site_stats) | What are this call set's per-site and per-sample genotype statistics, including heterozygosity, F and the exact Hardy-Weinberg test? |
| [`read_variant_calls`](#read_variant_calls) | Which records of this VCF or BCF match this query? |
| [`score_variant_effect`](#score_variant_effect) | How much less (or more) likely does ESM-2 find each substitution than the wild-type residue? |
| [`variant_call_summary`](#variant_call_summary) | What does bcftools stats say about this call set? |
| [`variant_consequences`](#variant_consequences) | What does each call in this VCF do to the transcripts of its reference? |

---

### apply_variant_call

**Apply variant call**: _What sequence results from substituting this called ALT allele?_

Substitute one called ALT allele into a sequence and return the edited bases, the range the edit occupies and the length change. The REF allele is checked against the sequence first and a mismatch REFUSES naming both: applying a call from a different assembly would produce a construct that looks fine and is wrong. Symbolic and breakend alleles are refused for what they are: they name a rearrangement rather than replacement bases.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The REF allele must match the sequence at that position, and is checked.

**Does not:**
- One allele at a time.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string | **yes** |  |  | the sequence to edit. |
| `file` | string |  |  |  | which call set the variant comes from, by name. Unset, it is the project's only one. |
| `contig` | string | **yes** |  |  | the contig of the record to apply, as the file names it. |
| `pos` | number | **yes** |  | ≥ 1 | the POS of the record to apply, 1-based as VCF writes it. |
| `alt_index` | number |  | `1` | ≥ 1 | which ALT of a multiallelic record to apply, counting from 1 as the file lists them. Default the first. |
| `offset` | number |  | `1` | ≥ 1 | the coordinate this sequence's FIRST base has in the call set's contig. Default 1, meaning the sequence starts at the contig's start. A plasmid extracted from a genome sets this to where it was cut from, which is what lets a genomic call be applied to it at all. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the edit in one sentence, generated from this run |
| `sequence` | string |  | the sequence with this ALT substituted for the REF, ready to wire into a next step. Every base outside the edited range is unchanged, and the length differs from the input by `delta`, so any coordinate downstream of `edited_start` has moved by that much |
| `edited_start` | number |  | 0-based inclusive start of the range the edit occupies in the NEW sequence, for selecting it |
| `edited_end` | number |  | 0-based INCLUSIVE end of the edited range in the new sequence. Inclusive, not half-open, because it is the end of a selection a reader is meant to see highlighted rather than a slice bound |
| `delta` | number |  | signed length change, which is what any annotation downstream of the edit must shift by |
| `applied` | any |  | the record as applied: chrom, pos, ref, the ALT chosen and its index, so a run record says which allele of a multiallelic site was taken |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "apply_variant_call",
  "arguments": {
    "sequence": "<string>",
    "contig": "<string>",
    "pos": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### browse_region

**Browse region**: _What does this window of the genome hold: bands, transcripts and nuclease sites?_

Read one window of a genome the way a genome browser shows it: the cytogenetic bands it spans, the transcripts in the chosen RefSeq set, which residues of each protein the window encodes (translated from the assembly’s own bases), how many dbSNP 155 variants fall in it and how many ClinVar calls pathogenic, and every CRISPR site for the chosen nuclease (SpCas9 unless told otherwise) with its strand, cut position and on-target scores. Give a gene symbol (resolved through MANE Select, then HGNC) or a locus, 1-based and inclusive. Each lane refuses a window wider than it will read, and says so.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Assumes:**
- The cytobands and RefSeq set for the assembly named.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `assembly` | string | **yes** |  |  | the UCSC assembly name (hg38, hg19, mm39…). |
| `gene` | string |  |  |  | a gene symbol; the window is its MANE Select (or HGNC) transcript with a 2% margin either side. Takes precedence over `locus`. |
| `locus` | string |  |  |  | the window, 1-based and inclusive, when no `gene` is given. |
| `gene_track` | `"ncbiRefSeqSelect"` · `"ncbiRefSeqCurated"` · `"ncbiRefSeq"` · `"ncbiRefSeqPredicted"` |  | `"ncbiRefSeqSelect"` |  | which RefSeq set the transcripts and protein residues come from. Values: ncbiRefSeqSelect (RefSeq Select and MANE), ncbiRefSeqCurated (RefSeq Curated), ncbiRefSeq (RefSeq All), ncbiRefSeqPredicted (RefSeq Predicted). |
| `nuclease` | `"SpCas9"` · `"SpCas9-NG"` · `"SpG"` · `"SpRY"` · `"xCas9"` · `"SaCas9"` · `"SaCas9-KKH"` · `"AsCas12a"` · `"LbCas12a"` · `"enAsCas12a"` |  | `"SpCas9"` |  | which nuclease the CRISPR sites are enumerated for (its PAM and cut rule). On-target scores are SpCas9-trained and come back null for any other. Values: SpCas9 (SpCas9 · NGG), SpCas9-NG (SpCas9-NG · NG), SpG (SpG · NGN), SpRY (SpRY · NRN), xCas9 (xCas9 · NG), SaCas9 (SaCas9 · NNGRRT), SaCas9-KKH (SaCas9-KKH · NNNRRT), AsCas12a (AsCas12a · TTTV), LbCas12a (LbCas12a · TTTV), enAsCas12a (enAsCas12a · TTTV). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | what each lane found in the window, generated from the run |
| `window` | string |  | the window read, 1-based inclusive, and how it was reached |
| `protein` | any |  | per transcript: accession, strand, the first and last residue numbers in the window and the residues themselves |
| `sites` | any |  | CRISPR sites: spacer, PAM, strand, 1-based protospacer bounds, cut position and Rule Set 1 / CRISPRscan scores |
| `refusals` | any |  | each lane that did not run for this window, and why |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "browse_region",
  "arguments": {
    "assembly": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### check_invariants

**Check invariants**: _Is this designed sequence admissible: protein unchanged, forbidden sites absent, frame intact, length, GC and CAI within bounds?_

Decide whether a sequence is scientifically admissible: protein unchanged, forbidden restriction sites absent, reading frame intact, length/GC/CAI inside stated bounds. Every verdict names what broke, where, and the remedy. Run this after any design or optimisation step, and stop the chain when `admissible` is false — never report a designed sequence without it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The bounds and forbidden sites given are the design's real requirements.

**Does not:**
- A composition: validated parts do not add up to a validated whole, so it is graded against an independent oracle rather than the engines it calls.
- Says what broke and where; it does not repair it.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the sequence to judge — defaults to the open record. |
| `preserve_protein_of` | string |  |  |  | the ORIGINAL coding sequence (or its protein): the result must still translate to it. |
| `forbid_sites` | string[] |  |  |  | enzyme names that must not cut, e.g. BsaI, BsmBI. |
| `require_frame` | boolean |  | `false` |  | length divisible by 3 and no premature stop. |
| `require_start` | boolean |  | `false` |  | with require_frame: the first codon must be a start codon. Only applies when require_frame is true. Advanced. |
| `require_stop` | boolean |  | `false` |  | with require_frame: the last codon must be a stop. Only applies when require_frame is true. Advanced. |
| `min_length` | number |  |  | ≥ 0 | minimum length [bp]. In bp. Advanced. |
| `max_length` | number |  |  | ≥ 0 | maximum length [bp]. In bp. Advanced. |
| `min_gc` | number |  |  | 0–1 | minimum GC fraction (0-1). |
| `max_gc` | number |  |  | 0–1 | maximum GC fraction (0-1). |
| `gc_window` | number |  |  | 10–500 | judge every window of this many bases instead of the whole sequence — a synthesis is rejected on a local GC peak, not on the mean. In bp. Advanced. |
| `cai_organism` | string |  |  |  | host for the codon-adaptation check, e.g. sce. Advanced. |
| `min_cai` | number |  |  | 0–1 | minimum CAI (needs cai_organism). Advanced. |
| `table` | number |  | `1` | 1–33 | NCBI translation table. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `admissible` | boolean |  | every invariant was decided and held |
| `failed` | number |  | how many invariants did not hold |
| `checked` | number |  | how many invariants were asked |
| `summary` | string |  | one line per failure: value, requirement, remedy |
| `verdicts` | any |  | per-invariant verdicts, with breach coordinates |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_invariants",
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

### compare_flow_cytometry_populations

**Compare flow cytometry populations**: _Does this channel differ between these two populations, and by which test?_

One channel of an FCS file between two populations of the run (FlowJo's and FCS Express's population comparison): Welch's two-sample t-test, the Wilcoxon rank-sum test, the two-sample Kolmogorov–Smirnov test and Pearson's χ² on the two histograms over shared equal-width bins, each R's test on the populations' linear values.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The two populations are gated in the same run (the same file, compensation and gating).

**Does not:**
- The Overton-like subtraction is flowStats' overton_like, a density difference; histogram subtraction is CellEngine's subtractHistograms (Overton's cumulative, channel-by-channel, enhanced normalized and one-sided KS), with population A as the control. FlowJo normalises each histogram by its mode where CellEngine scales the control by the event counts.
- With thousands of events every test reports tiny p-values for differences too small to matter.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `scale` | `"logicle"` · `"fasinh"` · `"arcsinh"` · `"hyperlog"` · `"flowcore-logicle"` · `"wsp-biex"` · `"flin"` · `"flowcore-arcsinh"` · `"boxcox"` · `"linlog"` · `"flowcore-biex"` |  | `"logicle"` |  | as analyze_flow_cytometry. |
| `T` | number |  |  | ≥ 1 | as analyze_flow_cytometry. |
| `W` | number |  | `0.5` | 0–5 | as analyze_flow_cytometry. |
| `M` | number |  | `4.5` | 0.5–10 | as analyze_flow_cytometry. |
| `A` | number |  | `0` | -5–5 | as analyze_flow_cytometry. |
| `cofactor` | number |  | `150` | ≥ 0.001 | the c in asinh(x / c). |
| `biex_width` | number |  | `-10` | ≤ -1 | as analyze_flow_cytometry. |
| `biex_negative` | number |  | `0` | ≥ 0 | as analyze_flow_cytometry. |
| `asinh_a` | number |  | `1` |  | the a in asinh(a + b·x) + c. |
| `asinh_b` | number |  | `1` |  | the b in asinh(a + b·x) + c. |
| `asinh_c` | number |  | `0` |  | the c in asinh(a + b·x) + c. |
| `lambda` | number |  | `1` |  | λ of Box-Cox or linlog. |
| `biexp_a` | number |  | `0.5` |  | flowCore biexponential a. |
| `biexp_b` | number |  | `1` |  | flowCore biexponential b. |
| `biexp_c` | number |  | `0.5` |  | flowCore biexponential c. |
| `biexp_d` | number |  | `1` |  | flowCore biexponential d. |
| `biexp_w` | number |  | `0` |  | flowCore biexponential w. |
| `compare_channel` | string |  |  |  | the channel compared (PnN, PnS or a derived name); empty for the first fluorescence channel. |
| `population_a` | string |  |  |  | population A; empty for all events. |
| `population_b` | string |  |  |  | population B; empty for all events. |
| `compare_bins` | number |  | `20` | 2–256 | equal-width histogram bins over both populations’ range, for the χ² test. |
| `pb_levels` | number |  | `0` | 0–20 | probability-binning levels (2^levels bins cut from population A); 0 for flowFP's own rule, floor(log2 n(A)) − 3. |
| `subtraction_bins` | number |  | `256` | 2–4096 | histogram subtraction's equal bins over both populations' range (CellEngine's bins). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `welch_p` | number or null |  | Welch's t-test p-value |
| `rank_sum_p` | number or null |  | Wilcoxon rank-sum p-value |
| `ks_d` | number or null |  | Kolmogorov–Smirnov D |
| `pb_t` | number or null |  | probability-binning T(χ) of B against A, unitless; above 4 the distributions differ at p < 0.01 |
| `overton_positive` | number or null |  | flowStats' Overton-like subtraction, one-sided: the share (0–1) of B's density above A's past A's mean |
| `subtraction_positive` | any |  | histogram subtraction: the % of B above A by Overton's cumulative, channel-by-channel, enhanced normalized (ens) and one-sided KS estimators, and the bins |
| `tests` | any |  | every test: method, statistic, parameter, p-value; the χ² histograms; the probability-binning counts |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "compare_flow_cytometry_populations",
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

### copy_number_allele_split

**Copy number allele split**: _What major and minor allele copy number does each segment carry?_

Read an Affymetrix array result's own allele-specific copy number: for each segment the major and minor allele counts (1+1, 2+0, 0+0), what they mean (balanced, allelic imbalance, loss of heterozygosity placed against the sample's own ploidy, homozygous deletion), and ASCAT's whole-genome summary over them (LOH fraction, homozygous deletions, modal allele state, whole-genome doubling, genomic instability). OncoScan results state a split when the aberrant-cell fraction was determined; the tool says why when a file states none.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- The producer's estimates, read.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one, and it refuses rather than guessing when there are several. |
| `estimated_only` | boolean |  | `false` |  | report only the segments the producer split. Default false: an unestimated segment is listed as such, which is a different answer from its absence. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many segments carry a split, how many are LOH (and copy-neutral), homozygous deletions, imbalanced and balanced, and the autosomal LOH fraction |
| `segments` | any |  | one entry per segment: chromosome (the file's own name, X not 24), start and end (the file's coordinates), markers, estimated, major and minor (null where not estimated), raw_a and raw_b (the producer's raw nA/nB, null where empty), total_cn (the producer's total, fractional where it made no integer call), state (not-estimated, homozygous-deletion, loh, balanced, imbalanced) and relative_to_ploidy (below, equal, above, for LOH only, null when no ploidy is stated) |
| `metrics` | any |  | ASCAT 3.2.0's ascat.metrics() profile columns over the estimated segments, unrounded: n_segs, segs_size, size_odd_segments, size_intermediate_segments, homdel_segs, homdel_largest, homdel_size, homdel_fraction, LOH (autosomal fraction), mode_minA, mode_majA, WGD (0, 1, '1+' or null) and GI (null when WGD is). Null when nothing is estimated |
| `provenance` | any |  | which file answered, the data set the split was read from, how many segments it holds and how many are estimated, and the producer's own fit: ploidy and aberrant-cell fraction as the chip summary states them |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_allele_split",
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

### copy_number_compare

**Copy number compare**: _Which copy-number events do two samples share, and which only one carries?_

Join two Affymetrix copy-number samples' own calls and report which events they share and which only one of them carries: for every pair, the chromosome both files resolved to, the kind, the bases they overlap and their reciprocal overlap; and separately each sample's unshared calls. Kind is part of the match, so a gain in one sample and a loss in the other at one locus are reported as two unshared calls rather than as agreement. Chromosomes only one file indexes are listed apart and are NOT reported as differences: nothing about them was compared. NO OVERLAP THRESHOLD IS APPLIED — every pair comes back with its numbers, and which agreement counts as agreement is a laboratory's judgement.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- Compares the samples' own calls.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project is the first sample, by name. Unset, it is the project's only one — and it refuses rather than guessing when there is more than one. |
| `data_set` | string |  |  |  | which data set of the first file to scan, by name. Unset is the file's FIRST, which is what the panel opens on. |
| `compare` | string | **yes** |  |  | which copy-number file in this project is the second sample, by name — the same parameter copy_number_read.compare takes. Required: there is no default second sample, and a file compared with itself answers one question twice. |
| `compare_data_set` | string |  |  |  | which data set of the second file to scan. Unset is that file's FIRST. |
| `min_markers` | number |  | `1` | ≥ 1 | ignore any call shorter than this many markers, on BOTH sides. The default counts everything either file called, because a reporting floor belongs to the laboratory and not to this tool — and it is the same floor copy_number_findings applies. |
| `min_bases` | number |  | `0` | ≥ 0 | ignore any call spanning fewer bases than this, on BOTH sides. Default 0, for the same reason as min_markers. Note a single-marker call spans 0 bases. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many of each sample's own calls are shared and in how many overlapping pairs (a call can overlap several on the other side, so the two differ), how many each carries alone, over how many chromosomes both files index, and which floors were applied |
| `shared` | any |  | one entry per PAIR of overlapping calls of the same kind: chrom (the name BOTH files resolved to, never either file's raw chromosome number), kind, a and b (the two calls, each with its own start, end, marker count and value), overlapBases, and reciprocalOverlap — the SMALLER of the two containment fractions, so a focal call inside a whole-arm one scores low rather than 100%. A call that overlaps several on the other side appears once per pair, which is how the reference application's own overlap table behaves |
| `only_in_file` | any |  | the first sample’s calls that no call of the same kind in the second sample overlaps, on a chromosome BOTH files index — each with the chromosome name and the call itself. This is the half a reader cannot get by reading two result sets one after the other |
| `only_in_compare` | any |  | the second sample’s calls that no call of the same kind in the first sample overlaps, on a chromosome both files index |
| `unmatched_chromosomes` | any |  | chromosomes only one of the two files indexes, each with which side carries it. Their calls were NOT compared and are NOT in only_in_file or only_in_compare: a targeted array that does not carry Y says nothing about Y in the other sample |
| `compared` | any |  | the chromosome names both files index — what this comparison actually covers, so a caller can tell a clean result from a narrow one |
| `provenance` | any |  | which two files and data sets answered, how each side’s calls were read (the producer’s own segment calls, or the per-marker state columns), how many calls each side contributed, and the floors applied to both |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_compare",
  "arguments": {
    "compare": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### copy_number_findings

**Copy number findings**: _Which gains, losses and runs of homozygosity did the file's producer call?_

Scan every indexed chromosome of an Affymetrix copy-number container and report what the file itself called: gains, losses and stretches of homozygosity, with their positions, marker counts and spans, plus a per-chromosome summary. Reads the file's own CNState and LOH columns and infers nothing — for a second opinion computed from the log2 ratios, use copy_number_segment. A chromosome that was read and carries nothing is reported as clean, which is a different answer from one that could not be read. NO GENOME BUILD IS ASSUMED: positions are the file's own.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- The producer's calls, read; nothing is re-called.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one — and it refuses rather than guessing when there is more than one. |
| `data_set` | string |  |  |  | which data set to scan, by name. Unset is the file's FIRST, which is what the panel opens on. |
| `min_markers` | number |  | `1` | ≥ 1 | ignore any run shorter than this many markers. The default counts everything the file called, including single markers, because a reporting floor belongs to the laboratory and not to this tool. |
| `min_bases` | number |  | `0` | ≥ 0 | ignore any run spanning fewer bases than this. Default 0, for the same reason as min_markers. Note a single-marker run spans 0 bases. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | what was found, across how many chromosomes and markers |
| `findings` | any |  | every gain, loss and stretch of homozygosity, as the file called them: kind, chromosome, startPosition, endPosition, markerCount, bases, and — where the file states them — state and stateLabel (the copy-number state; absent on an LOH finding, which is not a copy-number call), confidence (the producer's own, 0..1) and mixture (mosaic fraction, signed as the file signs it, so a mosaic loss and a mosaic gain stay distinguishable). No cytoband: naming a band needs a genome build, and this node is given none |
| `chromosomes` | any |  | per chromosome: markers read, and the counts and spans of gains, losses and LOH runs |
| `source` | string |  | which route answered: `segments` means the producer's own segment calls, which is what a CYCHP written by ChAS carries; `markers` means the per-marker state columns, which is what a CNCHP carries. Different provenance for the same question, so a pipeline comparing two files can tell which it got |
| `bed` | string |  | the same calls as a UCSC BED track, ready for IGV, the UCSC browser or bedtools: 0-based half-open, one row per finding, colored by kind through itemRgb, with the producer's confidence in the score column (0 where the file states none) and the genome build on the `track db=` line when the container names one. The JSON `findings` above carry the file's own inclusive marker positions; this output is the same calls converted once, by the same writer the Export panel uses |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_findings",
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

### copy_number_loh

**Copy number loh**: _Where is heterozygosity lost, recomputed from the array's own genotype calls?_

Recompute loss of heterozygosity from an Affymetrix array's own per-marker genotype calls, rather than reading the runs the producer wrote: APT's window method, with the false-positive rate and the assumed genotyping error rate as parameters. Answers where a sample has lost one parental haplotype, including where copy number is normal. Needs a container that states genotype calls — an OncoScan OSCHP does; a CytoScan CYCHP states the set with no rows, and this says so rather than answering empty.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- APT's windowed LOH model at the alpha and error rate given.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one — and it refuses rather than guessing when there are several. |
| `alpha` | number |  | `0.01` | 1e-07–0.5 | APT's `lohCN_alpha`: the false-positive rate the heterozygote cutoff is set against. Raising it makes the window narrower and the method readier to call a run, which is the knob to move when comparing against another caller. |
| `error_rate` | number |  | `0.05` | 1e-07–0.5 | APT's `lohCN_errorrate`: the assumed genotyping error rate, which is what makes a heterozygote inside a homozygous stretch explicable. It is RE-ESTIMATED from the sample's own no-call rate when the genotype confidences reach the no-call threshold, and the output says which value was actually used. |
| `min_genomic_span` | number |  | `1000000` | ≥ 0 | APT's `lohCN_minGenomicSpan`: a called run narrower than this many base pairs is dropped. The default is the vendor's 1,000,000. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many runs of loss of heterozygosity were called, over how many chromosomes and how many megabases, and how many markers the method could read |
| `runs` | any |  | one entry per called run: chromosome (the file's own label), start, end, markers (how many genotyped markers it spans). Coordinates are the marker positions the container states, on whatever assembly it names |
| `window` | any |  | what the parameters solved to for THIS sample: markerCount (the window width), hetCutoff (heterozygotes at or above which the window is not LOH), and errorRate (the value used, which differs from the parameter when it was re-estimated from the no-call rate) |
| `accounting` | any |  | markers (genotype calls read), noCalls (dropped before anything else), evaluated, inSegmentsTooShort (markers in a stretch shorter than the window, left UNCALLED rather than called clear), beyondLastChromosome, segments. The five ways a marker can be spent sum to markers |
| `provenance` | any |  | which data set the genotype calls came from, which one the coordinates came from, how many were paired, and the parameters in force. The pairing is checked against the marker each call names, never trusted |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_loh",
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

### copy_number_mosaicism

**Copy number mosaicism**: _Which mosaic fraction class is each region of this chromosome closest to?_

Estimate which mosaic fraction class each region of one chromosome is closest to, as Affymetrix Power Tools computes it. A mosaic event is present in only some of the sample's cells, so its log2 ratio sits between the levels a clonal change would produce. Every segment comes back with the class it was assigned (±0.3, ±0.5, ±0.7, ±1.0), the fraction that class is NAMED for, its confidence, and whether the method CALLED it as mosaic — a whole-copy change of exactly ±1.0 is clonal and is reported with call 0, which is the vendor's own test. The mixture values are class labels, not measured cell fractions: there is no published method for this estimate and no independent implementation to grade it against, so it is reported as APT computes it and the provenance output carries that sentence. A chromosome with fewer than 4,330 markers is refused by name rather than answered empty, because the method's own boundary adjustments would delete every call.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Affymetrix Power Tools' mosaicism model with the bandwidth and window given.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one — and it refuses rather than guessing when there is more than one. |
| `data_set` | string |  |  |  | which data set to read, by name. Unset is the file's FIRST, which is what the panel opens on. |
| `chromosome` | number |  |  | 1–25 | which chromosome, as the file numbers them (1-22, then 23=X, 24=Y, 25=MT — the file's own convention). Unset is the first the index carries. A chromosome too short for the method is refused with the count it has and the ones that would run. |
| `graph` | string |  |  |  | which graph column to read. Unset is the first log2-ratio column, the same rule copy_number_segment applies. A column that is not a log2 ratio is refused rather than smoothed: a copy-number STATE column is already someone's answer. |
| `mosaic_bandwidth` | number |  | `6000` | ≥ 1 | the smoothing window in markers — APT's own `marker-bandwidth`. A mosaic event is a shallow wide elevation, so this is what decides how wide 'wide' is. The default is the vendor's shipped value. |
| `mosaic_confidence_window` | number |  | `251` | ≥ 1 | the running-median window used to score a segment, in markers — APT's own `confidence-window`. The default is the vendor's shipped value. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many segments the method produced, how many of them it CALLED as mosaic, which classes they fall in, and which chromosome and column answered |
| `segments` | any |  | every segment: startPosition and endPosition in bases, startIndex and endIndex in markers, mixture (the class as APT numbers it), mixtureValue (the fraction that class is NAMED for — a label, not a measurement), confidence, and call, which is 1 only for a segment the method calls mosaic. A reader looking for mosaic events wants call === 1 |
| `called` | any |  | the subset of segments with call === 1 — the mosaic events themselves, separated out so a pipeline does not have to know the vendor’s clonal test to find them |
| `provenance` | any |  | which file, data set, chromosome and column answered, how many markers were read, the windows and the eight class boundaries the run used, and the sentence this estimate must be presented with — verbatim from the engine, never paraphrased |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_mosaicism",
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

### copy_number_read

**Copy number read**: _What does this Affymetrix copy-number file hold: algorithm, array, data sets and per-marker values?_

Read an Affymetrix copy-number container (CNCHP/CYCHP/OSCHP/CHP) in this project and say what is in it: the algorithm and array that produced it, its data sets and their graphs, the per-chromosome marker index the file carries, and — for one chromosome — each graph decimated to a summary with its real range. Values the analysis left undefined are counted and reported, never plotted as zero. NO GENOME BUILD IS ASSUMED: positions are the file's own, because these files name an annotation release and not an assembly.

<sub>read-only · runs locally on the engine · long-running</sub>

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one — and it refuses rather than guessing when there is more than one. |
| `data_set` | string |  |  |  | which data set to read, by name. Unset is the file's FIRST, which is what the panel opens on. |
| `chromosome` | number |  |  | 1–25 | which chromosome's markers to summarize, as THE FILE numbers them. The autosomes are 1-22; which numbers are X and Y is stated by the file's own header (`xChromosome`/`yChromosome`, which both bundled arrays give as 24 and 25) and read from it rather than assumed. Unset is the first the index carries, which is what the panel selects. |
| `bins` | number |  | `60` | 10–400 | how many buckets to decimate each graph into. The panel uses one per pixel column of its plot; a smaller number here is a coarser summary of the same data. |
| `compare` | string |  |  |  | a SECOND copy-number file in this project, by name, to read over the SAME chromosome, the same window and the same buckets — the overlay the canvas draws, as numbers. Its chromosome is matched by LABEL and not by number, because each file states its own numbering, and its graphs are matched by COLUMN NAME, so a file carrying a different set of them reports which it has rather than answering from whatever sits at that position. Unset, nothing of a second file is read. |
| `start` | number |  |  | ≥ 0 | first base of the region to summarize, on the selected chromosome. Unset is the chromosome's first marker. Clamped to what the file's markers actually cover, because a locus is a position in the assembly and an array's coverage stops where it stops. |
| `end` | number |  |  | ≥ 0 | last base of the region to summarize. Unset is the chromosome's last marker. Given with `start`, the graphs are decimated over that window instead of the whole chromosome: the same thing the panel's Region field does. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the file in one sentence, generated from this run — the panel's own facts |
| `provenance` | any |  | the header chain the file states about itself: algorithm, version, array, and the annotation release it was analyzed against |
| `data_sets` | any |  | every data set, with its row count, its columns and which of them are graphs |
| `compared` | any |  | null unless `compare` named a second file. Otherwise: file, dataSet, chromosomeLabel and chromosomeInThatFile (matched by LABEL, so the number may differ), markersOnChromosome and markersInWindow (ITS markers — a different array covers a chromosome at a different density), bins and binnedOver (the SAME buckets and the same extent as `tracks`, which is what makes the two comparable at a coordinate), and tracks: one entry per graph of the PRIMARY file, each with that graph's buckets in the compared sample, or `absent` naming the column the compared file does not carry. A `refused` field instead of the rest means the comparison could not be made and says why — never an empty list, which would read as the two samples agreeing |
| `chromosomes` | any |  | the file's OWN per-chromosome index — start row, marker count and display flag each. This is what makes a chromosome one ranged read rather than a whole-file scan. A CNCHP states it in the data set's parameters and a CYCHP as rows in Chromosomes/Summary; both are read, and `index_source` says which one answered |
| `index_source` | string |  | where the per-chromosome index above came from, because the two container shapes keep it in different places and a reader comparing two files should not have to guess which |
| `tracks` | any |  | the selected chromosome decimated: per graph, its fitted range, the bucket minima/maxima/means, and how many markers carried no value |
| `lanes` | string or null |  | the tracks above drawn as the canvas draws them: one lane per graph over the same window, the bucket min-max envelope with its mean over it, the compared sample's envelope behind it where `compare` named a second file, and the marker lane underneath, because a gap in the probes is not a deletion. Null when no graph was decimated — no chromosome was selected, or none of its markers carried a value |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_read",
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

### copy_number_regions

**Copy number regions**: _Which of the sample's own calls fall in each ClinGen curated region?_

Place an Affymetrix copy-number sample's own calls in ClinGen's curated regions: for each region, which gains, losses or stretches of homozygosity fall in it, at what reciprocal overlap, and how much of the region they cover between them. Regions come from ClinGen's dosage-sensitivity curation, cached with its retrieval date — a loss is reported against the region's haploinsufficiency score and a gain against its triplosensitivity score, and no score is claimed for LOH or mosaic events, which change no copy number. NO THRESHOLD IS APPLIED: every overlap is reported with its numbers and which calls are worth reporting is a laboratory's judgement. Regions ClinGen has not placed on this build are listed separately and are NOT reported as clean.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- ClinGen's curated regions for the build named.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one — and it refuses rather than guessing when there is more than one. |
| `data_set` | string |  |  |  | which data set to scan, by name. Unset is the file's FIRST, which is what the panel opens on. |
| `build` | `"hg19"` · `"hg38"` |  |  |  | which assembly's curated region list to place the calls on. Unset is the build THIS FILE states about itself, and the node refuses rather than guessing when it states none — a region is a pair of coordinates, and placing a call on the wrong assembly moves every boundary by hundreds of kilobases with nothing to show it. Values: hg19 (hg19 / GRCh37), hg38 (hg38 / GRCh38). |
| `regions` | string |  |  |  | a BED region file in this project, by name, to check against INSTEAD of ClinGen's curated list — the laboratory's own panel, which is what ChAS calls the CytoRegion file. Unset is ClinGen. A BED line states no dosage score, so with this set every hit comes back with dosage null: the list says where to look and claims nothing about what a change there means. If the file states an assembly on its track line (`track ... db=hg19`) and it is not the build being read, the node refuses rather than moving every boundary by hundreds of kilobases. |
| `min_markers` | number |  | `1` | ≥ 1 | ignore any call shorter than this many markers. The default counts everything the file called, because a reporting floor belongs to the laboratory and not to this tool — and it is the same floor copy_number_findings applies, so both doors place the same calls. |
| `min_bases` | number |  | `0` | ≥ 0 | ignore any call spanning fewer bases than this. Default 0, for the same reason as min_markers. Note a single-marker call spans 0 bases. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many curated regions contain a call, out of how many were checked, on which build |
| `regions` | any |  | one entry per curated region containing at least one call: id (the ISCA identifier a report cites), name, cytoband, chrom, start, end (0-based half-open), covered (fraction of the region the calls cover between them, each base counted once, so it never exceeds 1), counts by finding kind, and hits — each with the finding itself, overlapBases, reciprocalOverlap (the SMALLER of the two containment fractions, so a focal call inside a whole-arm region scores low rather than 100%), regionCovered, and dosage/dosageAxis: ClinGen's score and description for the axis that speaks to that call's direction, or null for LOH and mosaic events, which change no copy number |
| `unplaced` | any |  | curated regions ClinGen has NOT placed on this build — it states their location as 'tbd'. They carry id, name, cytoband and their dosage scores but no coordinates, so nothing could be checked against them. They are NOT clean: they are unchecked. Empty on hg19, which places all of them |
| `provenance` | any |  | which region list answered: its authority, source URL, the curation date the file states, the assembly, and how many regions were placed and unplaced. A cached copy of an authority's table is only interpretable with its version beside it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_regions",
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

### copy_number_segment

**Copy number segment**: _Where are the breakpoints in this chromosome's copy-number signal, by each method named?_

Segment one chromosome of an Affymetrix copy-number container by up to four independent methods and report where they agree. The HMM lays a copy-number model over the log2 ratios and calls a state per segment; circular binary segmentation finds where the mean changes with no model of what a gain looks like, by permutation test; piecewise constant fitting picks the piecewise-constant curve minimizing squared error plus a penalty per jump, with no test and no seed; PELT minimizes the same shape of objective exactly and prices a boundary with an information criterion rather than a tuned constant, so its segment count follows from a model-selection rule (`pelt_method` swaps in changepoint's binary segmentation, segment neighborhood or at-most-one-change scan over the same costs and penalties, and `pelt_penalty` CROPS returns every segmentation optimal over a range of penalties). Every parameter and every default is the canvas's own. NO GENOME BUILD IS ASSUMED and no method is on unless asked for.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- CBS, PCF, PELT and the HMM as their reference implementations define them, with the parameters given.

**Does not:**
- Segments the signal; calling gains and losses is copy_number_findings'.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one — and it refuses rather than guessing when there is more than one. |
| `data_set` | string |  |  |  | which data set to segment, by name. Unset is the file's FIRST, which is what the panel opens on. |
| `chromosome` | number |  |  | 1–25 | which chromosome to segment, as the file numbers them (1-22, then 23=X, 24=Y, 25=MT — the file's own convention). Unset is the first the index carries, which is what the panel selects. |
| `graph` | string |  |  |  | which graph column to segment. Unset is the first log2-ratio column, which is what the panel segments. A column that is not a log2 ratio is refused rather than segmented: a copy-number STATE column is already someone's answer. |
| `methods` | string |  |  |  | which methods to run, comma-separated: `hmm`, `cbs`, `pcf`, `pelt`. Unset runs all four, because the point of this node is where they agree. The panel has each of them off until asked, so running one here is not a different default — it is the same control, pressed. |
| `hmm_model` | `"file"` · `"apt-cn-state"` · `"apt-cn-cyto2"` |  |  |  | which copy-number state model the HMM calls against. `file` is the model the container's own header states, and is used when unset if the file states one; otherwise the first preset. `apt-cn-state` is APT's generic method with its GC-corrected means, `apt-cn-cyto2` the six-state method written for CytoScan arrays. The panel lists the same models in the same order. Values: file (This file’s own parameters), apt-cn-state (APT cn-state (GC-corrected)), apt-cn-cyto2 (APT cn-cyto2 (CytoScan)). |
| `cbs_seed` | number |  | `1` | ≥ 1 | CBS accepts a boundary by permutation test, so the run is seeded and about 1 borderline dataset in 40 segments differently under a different seed. Same default as the panel. |
| `cbs_undo_splits` | `"none"` · `"sdundo"` · `"prune"` |  | `"none"` |  | DNAcopy's `undo.splits`, the post-hoc merge over what CBS found: `none` keeps every significant split, `sdundo` merges adjacent segments whose medians are within `cbs_undo_sd` trimmed SDs (is this boundary bigger than the noise?), `prune` keeps the fewest change points whose cost stays within `cbs_undo_prune` (how few boundaries explain this almost as well?). Same default as the panel. Values: none (Keep every split), sdundo (Merge within SDs), prune (Prune by cost). |
| `cbs_undo_sd` | number |  | `3` | ≥ 0 | DNAcopy's `undo.SD`: the merge threshold in trimmed noise SDs. Read only when `cbs_undo_splits` is sdundo. Same default as the panel. Only applies when cbs_undo_splits is sdundo. |
| `cbs_trim` | number |  | `0.025` | 0–0.5 | DNAcopy's `trim`: the fraction cut from each tail before sdundo measures the noise SD. Read only when `cbs_undo_splits` is sdundo. Same default as the panel. Only applies when cbs_undo_splits is sdundo. |
| `cbs_undo_prune` | number |  | `0.05` | ≥ 0 | DNAcopy's `undo.prune`: the fractional increase in residual cost pruning may accept. Read only when `cbs_undo_splits` is prune. Same default as the panel. Only applies when cbs_undo_splits is prune. |
| `cbs_eta` | number |  | `0.05` | 0.0001–0.5 | DNAcopy's `eta`: the error budget for stopping each permutation test early once its outcome is settled. Not the significance level; any value but 0.05 recomputes the stopping boundary. Same default as the panel. |
| `pcf_gamma` | number |  | `40` | ≥ 0 | PCF's penalty per jump — how much evidence a level change must carry. Scaled by the squared MAD noise estimate unless `pcf_normalize` is off, which is what makes 40 mean the same thing on a quiet array and a noisy one. Same default as the panel. |
| `pcf_kmin` | number |  | `5` | ≥ 1 | PCF's shortest allowed segment, in markers — the finest change the fit may claim. Same default as the panel. |
| `pcf_method` | `"auto"` · `"exact"` · `"fast"` |  | `"auto"` |  | which piecewise-constant fit: `auto` (copynumber's own rule — the exact dynamic program under 400 markers, its selectFastPcf approximation above), `exact`, or `fast`. Both are graded against R, so this is a real choice. `exact` is refused above 25,000 markers rather than silently downgraded: it is quadratic there (21 s at 100,000), where the approximation fits a whole 142,000-marker chromosome in about 0.3 s. Same default as the panel. Values: auto (Automatic), exact (Exact), fast (Approximate). |
| `pcf_normalize` | boolean |  | `true` |  | scale the PCF penalty by the squared MAD noise estimate (the vendor’s `normalize`). Off makes gamma an absolute penalty in squared log2 units, which is a different parameter wearing the same name. Same default as the panel. |
| `pelt_method` | `"PELT"` · `"BinSeg"` · `"SegNeigh"` · `"AMOC"` |  | `"PELT"` |  | which of changepoint's three multiple-change searches the `pelt` method runs over the same costs and penalties: `PELT` prunes to the exact optimum in linear time (changepoint's default); `BinSeg` splits greedily, at most `pelt_q` times, keeping each split while it pays for its penalty; `AMOC` scans for at most one change and keeps it only if it pays for the penalty, reporting Chen & Gupta's confidence; `SegNeigh` finds the exact optimum for every segment count up to `pelt_q` and lets the penalty pick one, at quadratic cost, so it declines past a Q·n² work budget (5,000 markers at Q = 5) and refuses MBIC and a shortest segment above 1, as changepoint does. Same default as the panel. Values: PELT (Pruned exact linear time), BinSeg (Binary segmentation), SegNeigh (Segment neighborhood), AMOC (At most one change). |
| `pelt_q` | number |  | `5` | ≥ 1 | changepoint's `Q`: BinSeg's most change points, SegNeigh's most segments. Read only by those two. Same default as the panel. Only applies when pelt_method is BinSeg or SegNeigh. |
| `pelt_penalty` | `"MBIC"` · `"BIC"` · `"SIC0"` · `"AIC"` · `"Hannan-Quinn"` · `"Manual"` · `"None"` · `"CROPS"` |  | `"MBIC"` |  | PELT's penalty, and the reason its knob is a different KIND of knob from PCF's gamma: it is an information criterion, so the number of segments follows from a model-selection rule rather than from a constant calibrated against this array's noise. MBIC is changepoint's own default and adds log(segment length) to each segment's cost as well as its (parameters + 2)·log(n) penalty. `Manual` is the only one that reads `pelt_penalty_value`; `CROPS` is a RANGE (Haynes, Eckley & Fearnhead 2017), read from `pelt_crops_*`, and needs `pelt_method` PELT. Same default as the panel. Values: MBIC (MBIC), BIC (BIC), SIC0 (BIC without the location term), AIC (AIC), Hannan-Quinn (Hannan-Quinn), Manual (Manual), None (None), CROPS (A range (CROPS)). |
| `pelt_penalty_value` | number |  | `0` | ≥ 0 | the cost a boundary must save to be worth buying, in the cost function's own units. Read ONLY when `pelt_penalty` is Manual; the named criteria derive their own from the marker count. Same default as the panel. Only applies when pelt_penalty is Manual. |
| `pelt_crops_from` | number |  | `1` | ≥ 0 | the smallest penalty of the CROPS range, in multiples of log(n). changepoint's own range is 1 to 10. Read only when `pelt_penalty` is CROPS. Same default as the panel. Only applies when pelt_penalty is CROPS. |
| `pelt_crops_to` | number |  | `10` | ≥ 0 | the largest penalty of the CROPS range, in multiples of log(n). Read only when `pelt_penalty` is CROPS. Same default as the panel. Only applies when pelt_penalty is CROPS. |
| `pelt_crops_draw_at` | number |  | `2` | ≥ 0 | which CROPS segmentation becomes `segments.pelt`: the one optimal at this penalty, in multiples of log(n) (2 is BIC for a change in mean). Every segmentation in the range is in the derivation either way. Same default as the panel. Only applies when pelt_penalty is CROPS. |
| `pelt_minseglen` | number |  | `1` | ≥ 1 | PELT's shortest allowed segment, in markers (changepoint's `minseglen`) — the finest change the fit may claim. Same default as the panel. |
| `pelt_standardize` | boolean |  | `true` |  | divide by the robust MAD before fitting. ON by default, and this is the one PELT default that is ours rather than the vendor's, because the vendor documents the assumption and does not enforce it: a change-in-mean cost is a raw residual sum of squares while the penalty is on a log(n) scale, so the two are only commensurate at unit variance. Off, a noisy array buys boundaries it should not and a quiet one buys none, and both look like plausible answers. Same default as the panel. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | what each method answered on this chromosome, generated from the run — never a fixed sentence over a variable outcome |
| `segments` | any |  | per method, its segments with their marker range, genomic span and level — and for the HMM, the state it called |
| `agreement` | any |  | where the methods that ran put their boundaries, and which boundaries more than one of them found. This is the reading no single method can produce |
| `derivation` | any |  | per method, what it actually used: the model and its means for the HMM, the seed for CBS, kmin and the raw and scaled gamma for PCF — plus each method's published provenance, and the reason where one declined to run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_segment",
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

### copy_number_somatic

**Copy number somatic**: _What somatic-mutation calls does this array result carry?_

Read an Affymetrix array result's own somatic-mutation calls: one row per mutation probe set with the producer's call, the score behind it and the two thresholds that call was graded against. OncoScan CNV Plus states this table; CytoScan and SNP 6.0 results do not, and the tool says so rather than answering empty.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- The producer's calls, read.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which copy-number file in this project, by name. Unset, it is the project's only one — and it refuses rather than guessing when there are several. |
| `detected_only` | boolean |  | `false` |  | report only the calls the producer detected. Default false: the undetected rows are what say the probe set was READ and came back wild type, which is a different answer from the probe set being absent. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many mutation probe sets this file states, how many the producer detected, and which array wrote them |
| `calls` | any |  | one entry per mutation probe set: probe_set (the producer's own identifier), call (its word — `Detected`, `Undetected`, or a third this reader passes through unchanged), detected (that word tested against the undetected one), score (MutScore, the statistic the call was made on), signal (QNSignal, the quantile-normalized signal behind the score), threshold_high and threshold_low (MutThreshHigh/MutThreshLow — the bars THIS probe set was graded at, which differ row to row), and from the array's annotation database for the genome the file states: gene, mutation (protein and cDNA change), cosmic (COSMIC id), chromosome, and position (1-based, the variant's first base); all five are null for a probe set that database does not list or when the file states no genome it is cached for. |
| `detected` | any |  | the subset of `calls` whose word is not the undetected one — the mutations this sample actually carries, in the same shape |
| `provenance` | any |  | which file answered, the container kind it was read from, the name of the data set the somatic table was found in, how many rows it holds, placement (which annotation database, genome and retrieval date placed the calls and how many it placed, or why none were placed), and the vocabulary note: the call words are the producer's own and are not normalized here |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "copy_number_somatic",
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

### design_expression_variants

**Design expression variants**: _Which codon-optimised variants of this CDS does an expression trial need, and how do they differ?_

The expression-design deliverable: several coding sequences for one protein, each variant following a different published strategy (maximise codon adaptation, match the host's codon usage, harmonise with the native host, or preserve the initiation region), each scored by an engine — CAI, GC, the folding energy of the Kudla -4..+37 initiation window, and rare codons. It returns the comparison rather than one answer, because the strategies disagree about what limits expression and the researcher picks. Refuses a frame-shifted CDS, an internal stop or a missing host table rather than optimising nonsense.

<sub>returns new records · runs locally on the engine · randomised, reproducible with its seed · deliverable: expression</sub>

**Assumes:**
- The organism's codon usage table is the one named.
- Each strategy (maximise CAI, match usage, harmonise) is DnaChisel's.

**Does not:**
- Variants to try, not a prediction of which expresses best.
- Codon choice only: promoter, RBS and plasmid copy number are elsewhere.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds` | string |  |  |  | the coding sequence to redesign, in frame and start-codon first. Unset falls back to THE SELECTION, on the strand the selection or its matching annotation states, then to the whole open record. |
| `feature` | string |  |  |  | redesign this annotated CDS or gene by NAME instead of the selection, exactly as `codon_usage_analysis` takes one. Its own strand is used. Takes precedence over the selection; `cds` still wins over both. |
| `host_table` | string |  |  |  | the TARGET host's codon-usage table, BY NAME, as the Codon Usage panel lists it. This is the way to pass a table: it resolves against the tables loaded in this project, so the numbers come from a table someone built or fetched. Leave unset and the active table is used. |
| `host_table_tsv` | string |  |  |  | ONLY for a table you are pasting yourself, measured elsewhere — prefer `host_table`, which names one this project already has. Do NOT write a table out from memory: codon frequencies are measured data, and a typed one is indistinguishable from a real one in the result. TSV: codon<TAB>count. Advanced. |
| `host_table_name` | string |  |  |  | how to name that table on every score it produced (e.g. "E. coli K-12, Kazusa"), so a reported CAI is attributable. |
| `postures` | (`"max_cai"` · `"match_usage"` · `"harmonize"` · `"native_initiation"`)[] | **yes** |  |  | which strategies to design, in order. max_cai = every amino acid takes the target host's single most-used codon; match_usage = reproduce the target host's synonymous-codon distribution rather than its single best codon, so rare codons stay at their natural rate; harmonize = put each codon at the same relative adaptiveness it had in the gene's native host, so the elongation rhythm (and any pause the protein folds around) survives the transfer; native_initiation = leave nt +1…+37 of the coding sequence exactly as they are and match the host's codon usage only downstream, so the redesign cannot add secondary structure to the window Kudla found dominant. The set IS the deliverable — asking for one gets one, and there is no hidden default of three. |
| `native_table` | string |  |  |  | the gene's NATIVE host codon table, BY NAME from this project's loaded tables — required only for the `harmonize` posture, which matches relative adaptiveness BETWEEN two hosts. It must be a DIFFERENT table from `host_table`: harmonising a host against itself is a difference of zero. |
| `native_table_tsv` | string |  |  |  | ONLY for a native table you are pasting yourself — prefer `native_table`. Do not write one out from memory (see `host_table_tsv`). TSV: codon<TAB>count. Advanced. |
| `upstream` | string |  |  |  | the bases immediately 5' of the CDS (the 5'UTR/RBS region). Kudla's window starts 4 nt BEFORE the start codon, so without this the folding energy is reported over a truncated window and says so. |
| `rare_below` | number |  |  | 0.01–0.99 | within-family frequency below which a codon counts as RARE, for the report only — it adds no constraint. Omit and no rare-codon count is reported, which is the honest answer: "rare" has no host-independent definition. |
| `genetic_table` | string |  | `"Standard"` |  | genetic code for the translation constraint (default Standard). Advanced. |
| `avoid_patterns` | string[] |  |  |  | literal patterns (restriction sites, homopolymers) every variant must not contain. |
| `gc_min` | number |  |  | 0–1 | minimum GC fraction (0-1); set with gc_max. Advanced. |
| `gc_max` | number |  |  | 0–1 | maximum GC fraction (0-1); set with gc_min. Advanced. |
| `gc_window` | number |  |  | ≥ 10 | window in bp the GC bounds apply over (whole sequence when unset). Advanced. |
| `seed` | number |  |  | ≥ 0 | seed for the solver's random draws, so a listed variant can be regenerated exactly. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `variants` | any |  | one entry per posture: its sequence, what it was optimising for, what it trades away, and every score with the engine that produced it |
| `records` | any |  | the variants as sequence RECORDS, so the run leaves the user holding the designs it describes |
| `protein` | string |  | the protein every variant encodes — asserted per variant, not assumed |
| `region` | string |  | what was actually redesigned — the selection when there is one, otherwise the whole open record, naming the STRAND and where it came from. Empty when the caller passed `cds` outright, because then there is no region, only a sequence they named |
| `distinct` | number |  | how many of the variants are DIFFERENT sequences |
| `skipped` | any |  | postures that were asked for and could not run, each with the reason |
| `best_cai` | string |  | the posture reaching the highest CAI — a ranking on ONE axis, never a recommendation |
| `least_structured` | string |  | the posture whose initiation window folds least tightly (the highest, least-negative dG) |
| `report` | string |  | the whole comparison as Markdown — table, what each design trades, the provenance of every number, and the sequences — so it survives outside the transcript |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_expression_variants",
  "arguments": {
    "postures": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### export_flow_cytometry_population

**Export flow cytometry population**: _Give me this population's events as a file another tool can open._

One population's events as a file: FCS 3.1 (FlowIO create_fcs, returned as base64) or CSV (returned as text). `raw` writes the linearized acquired values with the file's own $SPILLOVER, so the export can be compensated and gated again; `compensated` writes the run's compensated values and no spillover keyword. The population's path is recorded in a POPULATION keyword.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The population is one the strategy (or a saved cluster) defines on this file.

**Does not:**
- FCS is written as float32 list mode, as FlowIO writes it.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `population` | string |  |  |  | the population to write, by its gate id; empty for every event. |
| `values` | `"raw"` · `"compensated"` |  | `"raw"` |  | acquired values with the spillover keyword, or the compensated values. Values: raw (as acquired), compensated (compensated). |
| `format` | `"fcs"` · `"csv"` |  | `"fcs"` |  | the file format. Values: fcs (FCS 3.1), csv (CSV). |
| `computed` | boolean |  | `false` |  | also write the run's derived and unmixed channels. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `file` | any |  | the file: its name, MIME type, event count, and the CSV text or the FCS bytes as base64 |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "export_flow_cytometry_population",
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

### lookup_variant

**Lookup variant**: _What does the authority named return for this variant?_

Look up a variant: ClinVar clinical interpretation, dbSNP records, gnomAD population frequency and gene constraint, CADD deleteriousness, or GWAS/eQTL associations.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"clinvar"` · `"dbsnp"` · `"gnomad"` · `"cadd"` · `"gwascatalog"` · `"eqtlcatalogue"` · `"variation"` · `"pheweb"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | an rsID, HGVS or chrom-pos-ref-alt id, or a command such as "get_variant:variant_id=19-44908822-C-T" or "gene_constraint:gene_symbol=BRCA2". The eQTL Catalogue is the exception and needs a LOCUS, because its summary statistics are indexed by position and its REST API is retired: "eqtl_list_datasets tissue_label=macrophage" to pick a dataset, then "eqtl_associations dataset_id=QTD000021 region=1:109274570-109279000 gene_id=ENSG00000134243". |
| `limit` | number |  |  |  | maximum records (1–20). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `records` | any |  | the records the authority returned, in its own field names — wire them into a tool that takes ids, or read them in the transcript |
| `count` | number or null |  | how many records came back, which is a result even when it is zero |
| `provenance` | any |  | the authority, the exact endpoints called and when — what makes an answer re-checkable without re-running it |
| `envelope` | any |  | the authority's whole answer: paging, totals and the query it actually ran |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "lookup_variant",
  "arguments": {
    "source": "clinvar",
    "query": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### population_ancestry

**Population ancestry**: _What mixture of K ancestral populations does each sample look like, and which K does cross-entropy prefer?_

Individual ancestry coefficients, the ADMIXTURE-style picture: each sample as a mixture of K ancestral populations, fitted by sparse non-negative matrix factorisation for every K in a range, with K scored by the cross-entropy of predicting genotypes held out at random (LEA snmf, Frichot et al. 2014). Single-base records only, as LEA's vcf2geno keeps them. Validated against LEA 3.19.8 on every record and sample of 1000 Genomes phase 3 APOL1.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- LEA's sparse non-negative matrix factorisation; single-base records only, as its converter keeps them.

**Does not:**
- Ancestral components are statistical, not historical populations, and change with K and with which populations were sampled.
- Cross-entropy ranks the K values tried; it does not say the best one is right.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `vcf` | string | **yes** |  |  | the call set as VCF text (a .vcf, or a .vcf.gz already decompressed); every record's GT is read, ploidy 2. |
| `populations` | string |  |  |  | a sample table: a header row with a `sample` column and one or more grouping columns (tab-separated, as 1000 Genomes' .panel). Samples it does not list belong to no group. |
| `groupBy` | string |  | `""` |  | which column of the sample table groups the samples; empty is its first grouping column. |
| `kFrom` | number |  | `1` | 1–20 | smallest number of ancestral populations to fit. |
| `kTo` | number |  | `5` | 1–20 | largest number of ancestral populations to fit; every K from kFrom up is fitted, on one random stream. |
| `holdOut` | boolean |  | `true` |  | hold out a share of genotypes and score each K by the cross-entropy of predicting them; the K with the lowest is the one the data support best. |
| `holdOutShare` | number |  | `0.05` | 0.01–0.5 | share of genotypes held out for the cross-entropy. Only applies when holdOut is true. |
| `alpha` | number |  | `10` | ≥ 0 | regularisation added to every cell of FᵀF in the Q step: larger values push each sample toward fewer ancestries. Advanced. |
| `tolerance` | number |  | `1e-05` | ≥ 0 | stop when the relative change in the least-squares criterion falls below this (after 16 passes). Advanced. |
| `iterations` | number |  | `200` | ≥ 1 | most alternating passes per K. Advanced. |
| `ploidy` | number |  | `2` | 1–2 | 2 for diploid ALT counts 0/1/2, 1 for haploid 0/1. Advanced. |
| `seed` | number |  | `1` | ≥ 1 | R's set.seed value: it fixes the held-out genotypes and every K's random start, so a run is reproducible and citable. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `runs` | any |  | one row per K: K, the masked cross-entropy (null without holding out), and the passes the fit took |
| `bestK` | number or null |  | the K with the lowest cross-entropy, or the largest fitted K when nothing was held out |
| `ancestry` | any |  | one row per sample at the best K: sample, its group, and its share of each ancestral population |
| `ancestralGenotypeFrequencies` | any |  | one row per site at the best K: chrom, pos, ref, alt, and each ancestral population's frequency of each genotype (0, 1, 2 ALT copies) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "population_ancestry",
  "arguments": {
    "vcf": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### population_fst

**Population Fst**: _How differentiated are these populations, per site and averaged, with a jackknife standard error?_

Differentiation between populations of a call set: Weir and Cockerham's θ over two or more populations, or Hudson's or Patterson's Fst between pairs, per site and averaged with a block-jackknife standard error (scikit-allel). Every pair when more than two populations are compared. Validated on every site of 1000 Genomes phase 3 APOL1 for the 5 super-populations and 26 populations.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The populations given are the units of interest; the estimator chosen (Weir and Cockerham, Hudson or Patterson) suits the sample sizes.

**Does not:**
- Estimators differ systematically, especially at small sample sizes, so the estimator is named with the number.
- A block jackknife standard error assumes the blocks are independent.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `vcf` | string | **yes** |  |  | the call set as VCF text (a .vcf, or a .vcf.gz already decompressed); every record's GT is read, ploidy 2. |
| `populations` | string | **yes** |  |  | a sample table: a header row with a `sample` column and one or more grouping columns (tab-separated, as 1000 Genomes' .panel). Samples it does not list belong to no group. |
| `groupBy` | string |  | `""` |  | which column of the sample table groups the samples; empty is its first grouping column. |
| `estimator` | `"weirCockerham"` · `"hudson"` · `"patterson"` |  | `"hudson"` |  | weirCockerham: θ from the variance components over every compared population at once. hudson: 1 − within / between pairwise differences (Bhatia 2013). patterson: F2-based, biallelic sites only. Values: weirCockerham (Weir–Cockerham θ), hudson (Hudson Fst), patterson (Patterson Fst). |
| `compare` | string |  | `""` |  | the populations to compare, comma-separated; empty is every group of the column. |
| `blockLength` | number |  | `20` | ≥ 1 | sites per jackknife block for the average's standard error; a trailing partial block is dropped, as scikit-allel does. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `average` | any |  | per comparison: the populations, Fst over all sites, its jackknife standard error, blocks |
| `sites` | any |  | per site: pos, and per comparison the site's Fst (numerator / denominator), null where undefined |
| `matrix` | any |  | pairwise average Fst between every compared population (Hudson and Patterson) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "population_fst",
  "arguments": {
    "vcf": "<string>",
    "populations": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### population_site_stats

**Population site stats**: _What are this call set's per-site and per-sample genotype statistics, including heterozygosity, F and the exact Hardy-Weinberg test?_

Per-site and per-sample genotype statistics of a call set, for all samples or one population: allele counts and frequencies, called and missing calls, heterozygous and homozygous counts, observed and expected heterozygosity and the inbreeding coefficient F (scikit-allel), and the exact Hardy–Weinberg test with its excess-heterozygosity tail (bcftools +fill-tags). Validated on every site and sample of 1000 Genomes phase 3 APOL1 in 32 groups.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Genotypes are called correctly and samples are unrelated for F and HWE to mean what they say.
- The population given is the one the statistics should describe.

**Does not:**
- Missing calls are reported rather than imputed.
- HWE departure has many causes (structure, selection, genotyping error) and the test names none of them.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `vcf` | string | **yes** |  |  | the call set as VCF text (a .vcf, or a .vcf.gz already decompressed); every record's GT is read, ploidy 2. |
| `populations` | string |  |  |  | a sample table: a header row with a `sample` column and one or more grouping columns (tab-separated, as 1000 Genomes' .panel). Samples it does not list belong to no group. |
| `groupBy` | string |  | `""` |  | which column of the sample table groups the samples; empty is its first grouping column. |
| `group` | string |  | `""` |  | compute over this group's samples only; empty is every sample. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sites` | any |  | one row per record: chrom, pos, ref, alts, allele counts and frequencies, AN, called, missing, het, homRef, homAlt, ho, he, f, hwe and excHet per ALT |
| `samples` | any |  | one row per sample: its group, called, missing, het, homAlt and the missing and het rates |
| `summary` | any |  | sites, samples, segregating, biallelic and multiallelic sites, mean Ho and He, and the sites with the smallest HWE p-values |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "population_site_stats",
  "arguments": {
    "vcf": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### read_variant_calls

**Read variant calls**: _Which records of this VCF or BCF match this query?_

Read a variant call set (VCF, bgzipped VCF or BCF) in this project and return the records matching a query: a locus, a variant class, a QUAL floor, PASS-only, a sample that is not hom-ref, or an INFO key. Every answer says what it read over and what it filtered on, so a count can never be mistaken for the file's total. A call set too large to read whole opens at its header, and a locus is then the way in rather than an option.

<sub>read-only · runs locally on the engine · long-running</sub>

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which call set in this project, by name. Unset, it is the project's only one, and it refuses rather than guessing when there is more than one. |
| `contig` | string |  |  |  | restrict to one contig, named as the FILE names it: `20` and `chr20` are different names and neither is normalized into the other. With `start`/`end` this is a locus read; alone it is the whole contig. |
| `start` | number |  |  | ≥ 1 | first base of the region, 1-based and inclusive, as VCF itself counts. Needs `contig`. Unset is the contig's first record. |
| `end` | number |  |  | ≥ 1 | last base of the region, 1-based and inclusive. Needs `contig`. Unset is the contig's last record. |
| `types` | (`"snp"` · `"mnp"` · `"indel"` · `"other"` · `"bnd"` · `"overlap"`)[] |  |  |  | keep only these variant classes. The classes are htslib's own, assigned by the validated `setVariantType` and identical to the ones the panel's type filter offers. Unset keeps every class. |
| `min_qual` | number |  |  | ≥ 0 | keep only records whose QUAL is at least this. A record stating no QUAL (`.`) is DROPPED unless `include_missing_qual` is on, because a missing score is not a passing one. |
| `include_missing_qual` | boolean |  | `false` |  | keep records that state no QUAL when `min_qual` is set. Off by default: a caller asking for a quality floor is asking about scores, and a record with none has not met it. |
| `pass_only` | boolean |  | `false` |  | keep only records whose FILTER is PASS or unset (`.`): the usual first question of a call set, and the one filter that changes what most downstream steps should see. |
| `sample` | string |  |  |  | keep only records where this sample's genotype is neither hom-ref nor missing, which is that sample's own variants out of a cohort. Named as the file's header names it. |
| `info_key` | string |  |  |  | keep only records carrying this INFO key; with `info_value`, only those where it equals that value. |
| `info_value` | string |  |  |  | with `info_key`, the value that key must equal. |
| `limit` | number |  | `100` | 1–5000 | how many matching records to return. The COUNT is always the full number of matches: this caps the rows, never the accounting. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | what was read and what matched, in one sentence generated from this run |
| `variants` | any |  | the matching records, up to `limit`: chrom, pos (1-based), ids, ref, alts, qual, filters, end and the record's own htslib class label. Genotypes are not included: `sample` filters on them and `variant_call_summary` counts them, and a cohort record would otherwise carry thousands of columns per row |
| `matched` | number |  | how many records matched: the full count, not the number of rows returned |
| `read` | number |  | how many records were read before filtering. For a locus read this is the records in that window, NOT the file (`scope` says which) |
| `scope` | string |  | whether the numbers describe the whole file or one region, and (when the file was too large to read whole) that its header alone was opened. A count read from a window must never be readable as the file's |
| `filters_applied` | any |  | every filter this run actually applied, with its value. A caller comparing two runs needs to know which asked the narrower question |
| `samples` | any |  | the call set's sample names in header order, empty for a sites-only VCF, which is a fact about the file rather than a failure |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_variant_calls",
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

### score_variant_effect

**Score variant effect**: _How much less (or more) likely does ESM-2 find each substitution than the wild-type residue?_

Score protein substitutions with ESM-2, the zero-shot way `facebookresearch/esm`'s own `predict.py` does: how much less (or more) likely the mutant residue is than the wild type at that site, under a protein language model. It ranks a saturation library without an assay — and it is a RANKING IN NATS, not a stability measurement: it carries no kcal/mol and is calibrated against nothing. THE MODEL IS DOWNLOADED ON FIRST RUN, 30 MB for the 8M export and 2.6 GB for the 650M one, then cached; a run in a browser with no network to Hugging Face will refuse rather than hang.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The ESM-2 model and scoring strategy named, as facebookresearch/esm's predict.py computes it.

**Does not:**
- A zero-shot likelihood, not a measured effect.

**Not read from this result:** The answer is the model's per-variant score, which the outputs carry; no panel shows this tool, so there is no panel reading to carry.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein the positions are numbered against, one letter per residue. Wire a translation, or the CDS protein the library was designed on — the positions mean nothing without it. |
| `variants` | string[] | **yes** |  |  | the substitutions, in `A24D` form: wild-type residue, position, mutant residue. Every one is checked against `protein` first, because a scored substitution whose wild type does not match is a confident number about a protein nobody has. |
| `model` | `"esm2_t6_8M"` · `"esm2_t12_35M"` · `"esm2_t33_650M"` |  | `"esm2_t6_8M"` |  | which published ESM-2 ONNX export to score under. The three sizes are a download decision as much as an accuracy one, and the label says which. Values: esm2_t6_8M (ESM-2 8M · 30.3 MB), esm2_t12_35M (ESM-2 35M · 134.5 MB), esm2_t33_650M (ESM-2 650M · 2.61 GB). |
| `strategy` | `"wt-marginals"` · `"masked-marginals"` · `"pseudo-ppl"` |  | `"masked-marginals"` |  | how the score is computed. `masked-marginals` is ESM-1v's recommendation — one forward pass per residue, each with that site masked. `wt-marginals` is one pass over the wild type and the paper reports it as weaker. `pseudo-ppl` scores the whole mutant sequence and costs one pass per residue PER VARIANT, which is two orders of magnitude more; its number is a log-likelihood, not a ratio, and is comparable only against other variants of the same protein. Values: wt-marginals (Wild-type marginals), masked-marginals (Masked marginals), pseudo-ppl (Pseudo-perplexity). |
| `offset_idx` | number |  | `1` | 0–100000 | the number `position` counts from. 1 is ordinary protein numbering; set it when your variants are numbered against a mature chain or a construct that starts partway in. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `scores` | any |  | every variant with its score in nats, the strategy that produced it and the forward passes it cost — MOST DAMAGING FIRST, which is the reason to rank a library at all |
| `ranked` | any |  | just the substitution notations, in the same order — the list to take forward into an order or a filter |
| `mostDamaging` | string |  | the lowest-scoring substitution. It is the model's opinion about likelihood, not a measured loss of function, and `caption` is the sentence that says so |
| `leastDamaging` | string |  | the highest-scoring substitution — the one the model finds most ordinary |
| `caption` | string |  | the one sentence a score may never be shown without, generated from THIS run rather than fixed: what the number means under the strategy that produced it, and what it is not |
| `model` | string |  | which ESM-2 export produced these scores. Scores from two models are not comparable |
| `strategy` | string |  | which of the three strategies ran. Scores from two strategies are not comparable either, and pseudo-perplexity is not even the same quantity |
| `passes` | number |  | forward passes the run cost — the price of the strategy, after the fact |
| `variantCount` | number |  | how many substitutions were scored |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "score_variant_effect",
  "arguments": {
    "protein": "<string>",
    "variants": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### variant_call_summary

**Variant call summary**: _What does bcftools stats say about this call set?_

Summarize a variant call set the way bcftools stats does: records by class, transitions and transversions with their ratio, the twelve directed substitutions, indel lengths, per-contig counts, the FILTER tally, the QUAL range, and per-sample genotype counts. Reports what could NOT be counted rather than leaving a zero standing in for it, meaning a file whose genotypes were not parsed, and any genotype naming an allele its record never declares.

<sub>read-only · runs locally on the engine · long-running</sub>

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which call set in this project, by name. Unset, it is the project's only one, and it refuses rather than guessing when there is more than one. |
| `contig` | string |  |  |  | summarize ONE contig instead of the whole file, named as the file names it. The per-contig table is always over everything read; this narrows what everything else counts. |
| `pass_only` | boolean |  | `false` |  | count only records whose FILTER is PASS or unset. A Ts/Tv computed over unfiltered calls and one computed over passing calls are different measurements, and this is which one you asked for. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the call set in one sentence, generated from this run |
| `counts` | any |  | records, samples, and the class tallies: snps, mnps, indels, others, noAlts, multiallelicSites and multiallelicSnpSites. A site counts in every class its alleles carry, which is how bcftools counts them |
| `tstv` | any |  | ts, tv and ratio over every ALT, and tsFirstAlt/tvFirstAlt/ratioFirstAlt over each site’s first ALT only. Both, because bcftools reports both and a multiallelic call set makes them differ |
| `substitutions` | any |  | the twelve directed substitution types with their counts |
| `indel_lengths` | any |  | indel length (ALT minus REF) to the number of sites, sorted by length: bcftools' IDD section. Negative is a deletion |
| `substitutionMap` | object or null |  | the twelve directed substitutions as a REF by ALT grid, the Summary tab’s bars as one picture; the diagonal is empty, since a base does not substitute for itself |
| `substitutionMap.rows` | string[] |  |  |
| `substitutionMap.cols` | string[] |  |  |
| `substitutionMap.values` | ((number or null)[])[] |  |  |
| `substitutionMap.label` | string |  |  |
| `substitutionMap.title` | string |  |  |
| `indelPlot` | object or null |  | sites per indel length (ALT minus REF), deletions left of zero and insertions right of it |
| `indelPlot.x` | number[] |  |  |
| `indelPlot.series` | object[] |  |  |
| `indelPlot.series[].name` | string |  |  |
| `indelPlot.series[].y` | (number or null)[] |  |  |
| `indelPlot.xLabel` | string |  |  |
| `indelPlot.yLabel` | string |  |  |
| `indelPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `indelPlot.title` | string |  |  |
| `indelPlot.rules` | object[] |  |  |
| `indelPlot.rules[].y` | number |  |  |
| `indelPlot.rules[].label` | string |  |  |
| `per_contig` | any |  | records, snps and indels per contig, over everything read |
| `filters` | any |  | every FILTER value seen with its count, including PASS and the unfiltered (`.`) tally: the two are different states and are counted apart |
| `qual` | any |  | min, max, median and the number of records stating no QUAL. Null when nothing stated one, which is not the same as a range of zero |
| `per_sample` | any |  | bcftools' PSC section per sample: refHom, nonRefHom, hets, transitions, transversions, indels, averageDepth, singletons, hapRef, hapAlt and missing |
| `not_counted` | any |  | what this run could NOT count and why: `genotypesUnavailable` when the file's genotypes were not parsed (so per_sample is empty for a reason), and `badAlleleCalls` listing genotypes naming an allele their record never declares. Real bcftools stats exits on such a file rather than reporting per-sample numbers, so a non-empty list means per_sample has no bcftools counterpart to be compared against |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "variant_call_summary",
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

### variant_consequences

**Variant consequences**: _What does each call in this VCF do to the transcripts of its reference?_

Annotate every call in a VCF or BCF in this project against the transcripts of a GenBank reference: the Sequence Ontology term per transcript, Ensembl's IMPACT, HGVS c. and p., the CDS and protein positions, and the distance for an upstream, downstream or intronic call. Each call's most severe consequence is picked by Ensembl's own ranking. A symbolic allele, or a REF the reference does not carry at that position, is reported as not annotated rather than read against the wrong sequence. A CDS naming no /transl_table is read on the standard code, as INSDC specifies.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The VCF was called against this reference: every REF is checked against it.
- The coding annotation is the GenBank record’s own CDS and mat_peptide features.

**Does not:**
- No UTR or splice-site model: a reference carrying no mRNA or exon features has none to report.
- Symbolic alleles (<DEL>, *, <*>) and breakends are not annotated.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | which call set in this project, by name. Unset, it is the project's only one, and it refuses rather than guessing when there is more than one. |
| `reference` | string |  |  |  | the GenBank file the calls were made against, by name. Unset, every GenBank file in the project is a candidate: one is used for every call, several are matched to each call by its CHROM (accession or LOCUS). |
| `offset` | number |  | `1` | ≥ 1 | the coordinate the reference's FIRST base has in the call set's contig. Default 1, the reference is the whole contig; a region cut out of a genome sets where it was cut from. |
| `up_down_stream_bp` | number |  | `5000` | 0–100000 | how far from a transcript a call still counts as upstream or downstream of it. SnpEff’s own default is 5,000; the window decides how many annotations each call gets. In bp. |
| `min_impact` | `"HIGH"` · `"MODERATE"` · `"LOW"` · `"MODIFIER"` |  |  |  | keep only calls whose most severe consequence is rated at least this. Unset keeps every call. |
| `limit` | number |  | `200` | 1–10000 | how many calls to return in `calls`; the counts are always of all of them. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | what the set holds, generated from the annotation |
| `calls` | any |  | one row per ALT allele: chrom, pos, ref, alt, the most severe term, its IMPACT, gene, transcript, HGVS c. and p., and why it was not annotated when it was not |
| `annotations` | any |  | every consequence of every returned call, one per transcript it reaches |
| `by_term` | any |  | how many calls have each most-severe term, over all of them |
| `annotated` | number |  | alleles annotated |
| `not_annotated` | number |  | alleles skipped, each with its reason in `calls` |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "variant_consequences",
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
