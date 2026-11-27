# 🔬 Expression & hypothesis testing

_Differential expression, gene-set enrichment and falsification-tested discovery programmes._

14 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`describe_discovery_corpus`](#describe_discovery_corpus) | What does a discovery corpus hold, before any test is run on it? |
| [`differential_abundance_flow_cytometry`](#differential_abundance_flow_cytometry) | Which cell populations change in abundance between two groups of samples? |
| [`differential_expression`](#differential_expression) | Differential expression from raw RNA-seq read counts, by one of the three standard count models. |
| [`discover_flag_rates`](#discover_flag_rates) | How often does a corpus of maps carry a cryptic promoter, splice site or synthesis-breaking repeat more extreme than chance? |
| [`discover_reference_concordance`](#discover_reference_concordance) | Does a reference-gene stability ranking hold across conditions, and which candidates rank well everywhere? |
| [`discover_reference_stability`](#discover_reference_stability) | Are candidate reference genes more or less variable across human tissues than genes of the same abundance? |
| [`discover_site_avoidance`](#discover_site_avoidance) | Which exact restriction sites does each sequence carry far less, or far more, often than a stated null predicts? |
| [`discover_target_validation`](#discover_target_validation) | Does the evidence in a set of gene-level tables support a hypothesis that one gene drives a phenotype, by sequential falsification? |
| [`gene_set_camera`](#gene_set_camera) | Competitive gene set test that accounts for inter-gene correlation (camera; Wu & Smyth 2012), as limma 3.68.5 runs it: is a set more differentially expressed than the genes outside it, with the variance of its mean st… |
| [`gene_set_enrichment`](#gene_set_enrichment) | Preranked gene set enrichment analysis (GSEA; Subramanian et al. |
| [`gene_set_overrepresentation`](#gene_set_overrepresentation) | Over-representation analysis (ORA): which gene sets hold more of a gene list than chance, by the one-sided hypergeometric test against a background, as clusterProfiler's enricher() runs it (enrichit 0.2.6). |
| [`resolve_gene_sets`](#resolve_gene_sets) | Which gene sets do GO or Reactome define for this organism right now? |
| [`run_discovery_programme`](#run_discovery_programme) | Which pre-registered hypotheses does a program of falsification tests support, with the false discovery rate controlled across all of them? |
| [`validate_gene_trait`](#validate_gene_trait) | Does public expression and GWAS evidence support a hypothesis that a gene is involved in a trait, by sequential falsification? |

---

### describe_discovery_corpus

**Describe discovery corpus**: _What does a discovery corpus hold, before any test is run on it?_

The design step's view of a discovery corpus: each record's name, file, length and GC fraction, and how many records each file holds. Runs no test and returns no statistic, so hypotheses proposed from it are proposed before any result is seen (POPPER's metadata-only design step). Use it before run_discovery_programme.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Runs no test and returns no statistic, by design.

**No scientific claim:** Lists names, lengths and GC fractions; a design step, not a measurement.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] |  |  |  | the corpus: library document or file names, or wired records. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `records` | any |  | every record: name, file, length, GC fraction |
| `files` | any |  | every file with its record count and total length |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "describe_discovery_corpus",
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

### differential_abundance_flow_cytometry

**Differential abundance flow cytometry**: _Which cell populations change in abundance between two groups of samples?_

diffcyt differential abundance over project FCS files and a sample sheet: every sample's events (optionally one gated population) clustered together by FlowSOM on asinh-transformed channels, counted per sample, and each cluster's abundance compared between two levels of a sample-sheet column by edgeR (negative binomial GLM, Cox-Reid common and shrunk tagwise dispersions, likelihood-ratio test, Benjamini-Hochberg), optionally adjusting for a second column; with state channels, also each cluster's median of each state channel compared between the levels by limma (diffcyt testDS_limma: medians weighted by event count, empirical Bayes, moderated t, Benjamini-Hochberg).

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Each sample is one observation; a subject sampled twice belongs in the adjusting column.
- Every sample is clustered on the same channels and transform, so a cluster is the same cells in each.

**Does not:**
- edgeR's dispersion trend is not fitted (diffcyt's default, trend none); limma-voom's blocking factor needs at least int(11 b / 6) residual degrees of freedom per cluster for b blocks (the one dgesdd path ported) and is refused below that; the GLMM takes only the per-sample random intercept diffcyt adds, not a random effect on another column (cols_random).

**Validated:** against the reference implementation by 5 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `samples` | string |  | `""` |  | the FCS files to compare, by name or id, comma-separated; empty for every FCS file in the project. |
| `sample_sheet` | string | **yes** |  |  | a CSV in the project whose first column, headed sample, names each FCS file. |
| `condition` | string | **yes** |  |  | the sample sheet's column whose two levels are compared. |
| `reference` | string |  | `""` |  | the condition's baseline level; empty for the first in the sheet. |
| `compared` | string |  | `""` |  | the level compared with the baseline; empty for the first other one. |
| `covariate` | string |  | `""` |  | a second sample-sheet column the model adjusts for (donor, batch, time); empty for none. |
| `covariate_as` | `"factor"` · `"number"` |  | `"factor"` |  | the adjusting column as groups (a factor) or as a number. Values: factor (groups), number (a number). |
| `channels` | string |  | `""` |  | the channels to cluster on (diffcyt's type markers), comma-separated PnN or PnS; empty for every fluorescence channel. |
| `population` | string |  | `""` |  | a population of the strategy, gated in every file before clustering; empty for every event. |
| `cluster_cofactor` | number |  | `5` | ≥ 0.001 | asinh(x / cofactor) before clustering: diffcyt's default 5 is the CyTOF one, 150 common for fluorescence. |
| `xdim` | number |  | `10` | ≥ 2 | FlowSOM map width. |
| `ydim` | number |  | `10` | ≥ 2 | FlowSOM map height. |
| `meta_clustering` | boolean |  | `false` |  | group the map nodes into metaclusters by ConsensusClusterPlus (otherwise every node is a cluster). |
| `meta_k` | number |  | `40` | ≥ 2 | the number of metaclusters. Only applies when meta_clustering is true. |
| `cluster_seed` | number |  | `123` |  | R's set.seed before the map is trained (diffcyt seed_clustering). |
| `min_cells` | number |  | `3` | ≥ 0 | a cluster is tested when at least min_samples samples hold this many of its events. |
| `min_samples` | number |  |  | ≥ 1 | see min_cells; empty for half the samples. |
| `normalize` | boolean |  | `false` |  | TMM normalization factors on the cluster counts. |
| `state_channels` | string |  | `""` |  | channels whose per-cluster medians are compared too (diffcyt's state markers, testDS_limma), comma-separated PnN or PnS, none of them clustered on; empty for none. |
| `state_trend` | boolean |  | `true` |  | testDS_limma's trend: the prior variance follows each row's average median (limma eBayes trend = TRUE). |
| `voom` | boolean |  | `false` |  | also test every cluster's abundance by limma-voom (diffcyt testDA_voom: precision-weighted log-CPM, moderated t), beside edgeR. |
| `voom_block` | string |  | `""` |  | a sample-sheet column whose groups share a random effect in the voom test (diffcyt block_id: limma duplicateCorrelation, then lmFit with that correlation); empty for none. Only applies when voom is true. |
| `glmm` | boolean |  | `false` |  | also test every cluster's abundance by diffcyt's binomial GLMM (testDA_GLMM: lme4 glmer with a random intercept per sample, multcomp glht), beside edgeR. |
| `sam` | `"none"` · `"SAM"` · `"SAMseq"` |  | `"none"` |  | also test every cluster by samr (Tusher 2001, as CITRUS feeds it): SAM on each cluster's share of its sample's events, or SAMseq on the raw counts; permutation FDR over the reference and compared samples only. |
| `sam_pair` | string |  | `""` |  | a sample-sheet column pairing each reference sample with one compared sample (samr "Two class paired", permutations within pairs); empty for unpaired. Only applies when sam is SAM or SAMseq. |
| `sam_test` | `"standard"` · `"wilcoxon"` |  | `"standard"` |  | SAM's testStatistic for unpaired shares: standard (t with s0) or wilcoxon (rank sum). Only applies when sam is SAM. |
| `sam_nperms` | number |  | `100` | ≥ 1 | permutations (samr nperms); every distinct labelling instead when there are fewer. Only applies when sam is SAM or SAMseq. |
| `sam_seed` | number |  | `123` |  | samr random.seed: R's set.seed before the permutations are drawn. Only applies when sam is SAM or SAMseq. |
| `sam_fdr` | number |  | `0.2` | 0–1 | samr fdr.output: SAM() reports from the largest Δ whose median FDR is still at or above it (samr's own rule), so the reported FDR can exceed it. Only applies when sam is SAM or SAMseq. |
| `sam_nresamp` | number |  | `20` | ≥ 1 | SAMseq's nresamp: Poisson resamplings of the counts the ranks are averaged over. Only applies when sam is SAMseq. |
| `citrus` | boolean |  | `false` |  | also run CITRUS (Bruggner 2014, citrus.full with the SAM endpoint): its own Ward clustering of events sampled from every file, each merge holding enough events a candidate population, each file described by those populations' abundances or medians, tested by SAM against the endpoint. |
| `citrus_feature` | `"abundances"` · `"medians"` |  | `"abundances"` |  | CITRUS featureType: each population's share of the file's sampled events, or its median on every clustered channel. Only applies when citrus is true. |
| `citrus_sample_size` | number |  | `1000` | ≥ 0 | CITRUS fileSampleSize: events sampled from each file (every event when a file has fewer); 0 for every event. Only applies when citrus is true. |
| `citrus_min_size` | number |  | `0.05` | 0–1 | CITRUS minimumClusterSizePercent: a merge is a candidate population when it holds at least this fraction of the pooled events. Only applies when citrus is true. |
| `citrus_endpoint` | string |  | `""` |  | a numeric sample-sheet column as the endpoint (CITRUS continuous family, SAM quantitative); empty to classify by the condition column (two levels: two-class, more: multiclass). Only applies when citrus is true. |
| `citrus_seed` | number |  | `123` |  | R's set.seed before CITRUS samples the files; SAM's permutations continue the same stream, as citrus calls SAM without a seed. Only applies when citrus is true. |
| `citrus_nperms` | number |  | `10000` | ≥ 1 | SAM's permutations inside CITRUS (citrus passes 10000). Only applies when citrus is true. |
| `mem` | boolean |  | `false` |  | also type every cluster by marker enrichment modeling on the clustered channels (cytoMEM MEM, on asinh(x / cofactor)). |
| `mem_iqr_thresh` | string |  | `"0.5"` |  | cytoMEM IQR.thresh: the floor on both IQRs, a number or 'auto' (cytoMEM forces 0.5 below four clusters). Only applies when mem is true. |
| `mem_zero_ref` | boolean |  | `false` |  | cytoMEM zero.ref: compare each cluster with zero expression instead of the other cells. Only applies when mem is true. |
| `mem_scale` | `"linear"` · `"log"` · `"arcsinh"` |  | `"linear"` |  | cytoMEM scale.matrix: how the scores are rescaled. Only applies when mem is true. |
| `mem_scale_factor` | number |  | `0` |  | cytoMEM scale.factor: log base e^f, or asinh(x / f). Only applies when mem_scale is log or arcsinh. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `clusters` | any |  | per cluster: logFC, logCPM, LR, p and adjusted p (NaN, with the reason, where the filter left it out) |
| `counts` | any |  | the cluster × sample event counts, the samples and the clustered channels |
| `differential_state` | any |  | when state channels were given: per cluster and state marker, the median difference (asinh scale), average median, moderated t, p and adjusted p, and the prior df |
| `voom` | any |  | when voom was asked for: per cluster the log2 fold change, average log-CPM, moderated t, p and adjusted p (NaN where the filter left it out) |
| `voom_block` | any |  | when voom_block was given: the consensus intra-block correlation lmFit used, the number of blocks, and each tested cluster's own correlation (duplicateCorrelation) |
| `glmm` | any |  | when glmm was asked for: per cluster the contrast's log odds ratio, its standard error, z, p, BH-adjusted p, the fitted between-sample SD, and glmer's error or warnings (NaN where the filter left it out or the fit failed) |
| `sam` | any |  | when sam was asked for: per cluster samr's score d, numerator, s + s0, fold change, permutation p, q-value (%) and whether it is called up or down at the chosen Δ; with s0, π0, the permutations run and SAM's delta table |
| `citrus` | any |  | when citrus was asked for: the kept populations and their sizes, the file x feature matrix, SAM's score, numerator, s + s0, fold change and q-value (%) per feature, s0, π0, Δ, and the populations called at FDR 10%, 5% and 1% |
| `mem` | any |  | when mem was asked for: per cluster and clustered channel the MEM score, the medians (MAG) and IQRs of the cluster and its reference, and the IQR floor used |
| `dispersion` | any |  | edgeR's common dispersion, the tested clusters' tagwise dispersions and the prior degrees of freedom |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "differential_abundance_flow_cytometry",
  "arguments": {
    "sample_sheet": "<string>",
    "condition": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### differential_expression

**Differential expression**

Differential expression from raw RNA-seq read counts, by one of the three standard count models. DESeq2 (Love, Huber & Anders 2014): median-of-ratios size factors, negative-binomial GLM with empirical-Bayes shrunken dispersions, Wald or likelihood-ratio test, Cook's-distance outlier handling, independent filtering, optional LFC shrinkage. edgeR quasi-likelihood (Chen et al. 2025): filterByExpr, TMM normalization, a negative-binomial GLM with bias-adjusted QL dispersions squeezed toward an abundance trend, QL F-test. limma-voom (Law et al. 2014): filterByExpr, TMM, log-CPM with mean-variance precision weights, weighted linear models, moderated t. Takes a gene-by-sample count table and a sample table with the design's variables. Every gene of every validated fit is bit-identical to DESeq2 1.52.0, edgeR 4.10.6 and limma 3.68.5 running in R. Hands its significant genes, tested genes and ranked list on for gene-set enrichment.

<sub>read-only · runs locally on the engine · randomness: unknown</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `counts` | string | **yes** |  |  | raw read counts (never normalized values or TPM): genes in rows with the gene ID first, samples in columns, tab- or comma-separated, a header row naming the samples. |
| `samples` | string | **yes** |  |  | the sample table: a header row, then one row per sample with its name (as in the count table's header) first and the design's variables after; the run uses this table's sample order. |
| `method` | `"DESeq2"` · `"edgeR-QL"` · `"limma-voom"` |  | `"DESeq2"` |  | the count model: DESeq2 (negative binomial, Wald or LRT), edgeR-QL (negative binomial with quasi-likelihood F-test) or limma-voom (precision-weighted linear model on log-CPM, moderated t). |
| `design` | string |  | `"~ condition"` |  | the design formula over the sample table's columns, the variable of interest last (e.g. '~ batch + condition'). |
| `reference` | string |  | `""` |  | reference level per factor, 'variable=level' separated by commas; a factor not named takes its alphabetically first level, as R does. |
| `test` | `"Wald"` · `"LRT"` |  | `"Wald"` |  | Wald: one coefficient or contrast. LRT: the full design against `reduced`, testing every removed term at once. Only applies when method is DESeq2. |
| `reduced` | string |  | `""` |  | the reduced design for the likelihood-ratio test. Only applies when method is DESeq2. |
| `contrast` | string |  | `""` |  | 'factor, numerator, denominator': the log2 fold change of numerator over denominator. Empty is the design's last coefficient. Under edgeR and voom the denominator must be the factor's reference level. |
| `name` | string |  | `""` |  | one fitted coefficient to report, by its DESeq2 name (e.g. 'condition_treated_vs_untreated') or its model-matrix column ('conditiontreated'); empty is the last. |
| `fitType` | `"parametric"` · `"local"` · `"mean"` · `"glmGamPoi"` |  | `"parametric"` |  | the dispersion trend: parametric (asymptDisp + extraPois / mean, DESeq2's default, which falls back to local when it does not fit), local (locfit regression of log dispersion on log mean), the mean of gene-wise estimates, or glmGamPoi (gene-wise maximum likelihood by glmGamPoi, a local-median trend and quasi-likelihood shrinkage; with test LRT the p-values are glmGamPoi's quasi-likelihood F test; no outlier replacement, minmu 1e-6, no observation weights). Only applies when method is DESeq2. |
| `sfType` | `"ratio"` · `"poscounts"` · `"iterate"` |  | `"ratio"` |  | size factors: median of ratios over genes with no zero (ratio), with zeros allowed (poscounts, for sparse data), or iterated to maximise the NB likelihood of all but the worst-fitting 5% of genes (iterate, when every gene has a zero). Only applies when method is DESeq2. |
| `avgTxLength` | string |  | `""` |  | optional: tximport's average transcript lengths (txi$length), the same genes and samples as `counts`. DESeq2 then normalizes by gene-by-sample factors (each gene's lengths over their geometric mean, times median-of-ratios size factors), correcting for changes in transcript usage between samples. Only applies when method is DESeq2. |
| `weights` | string |  | `""` |  | optional: observation weights (assays(dds)[["weights"]]), the same genes and samples as `counts`, e.g. zinbwave's posterior probability that a single-cell count is not a dropout. DESeq2 divides each gene's weights by their largest and uses them in the base means, the dispersion likelihoods (samples at or below 0.01 leave the Cox-Reid term), the GLM and its tests. Only applies when method is DESeq2. |
| `useT` | boolean |  | `false` |  | Wald p-values from a Student t on each gene's summed weights (or the sample count) minus the coefficients, instead of the normal: zinbwave's recommendation for weighted single-cell data. Wald test only. Only applies when method is DESeq2. |
| `minmu` | number |  |  | ≥ 0 | the floor on fitted means in the GLM and the dispersion fit; empty is DESeq2's default, 0.5, or 1e-6 with fitType glmGamPoi. Single-cell counts, often below 1, want a small value such as 1e-6 (zinbwave's vignette). Only applies when method is DESeq2. |
| `betaPrior` | boolean |  | `false` |  | DESeq2's pre-1.16 default: a zero-mean Normal prior on every level's log2 fold change, so the reported fold changes, SEs and Wald test are the shrunken (MAP) ones. Wald only, no interactions; use instead of `shrink`. Only applies when method is DESeq2. |
| `alpha` | number |  | `0.1` | 0–1 | the target FDR: the summary counts genes below this adjusted p, and DESeq2's independent filtering maximizes rejections at it. |
| `filterByExpr` | boolean |  | `true` |  | keep only genes edgeR's filterByExpr finds expressed (the edgeR and limma workflows' first step); off fits every gene. Only applies when method is edgeR-QL or limma-voom. |
| `minCount` | number |  | `10` | ≥ 0 | filterByExpr: the count, at the median library size, a gene needs in the smallest group's worth of samples (taken as CPM). Only applies when method is edgeR-QL or limma-voom. |
| `minTotalCount` | number |  | `15` | ≥ 0 | filterByExpr: the total count a gene needs across all samples. Only applies when method is edgeR-QL or limma-voom. |
| `lfcThreshold` | number |  | `0` | ≥ 0 | test \|log2 fold change\| against this threshold instead of 0. Only applies when method is DESeq2. |
| `altHypothesis` | `"greaterAbs"` · `"greaterAbsUPSHOT"` · `"lessAbs"` · `"greater"` · `"less"` · `"greaterAbs2014"` |  | `"greaterAbs"` |  | which side of the threshold is the alternative. Only applies when method is DESeq2. |
| `pAdjustMethod` | `"holm"` · `"hochberg"` · `"hommel"` · `"bonferroni"` · `"BH"` · `"BY"` · `"fdr"` · `"none"` |  | `"BH"` |  | multiple-testing adjustment across genes (R `p.adjust`). |
| `independentFiltering` | boolean |  | `true` |  | drop low-mean genes from the adjustment when that gains rejections at `alpha`. Only applies when method is DESeq2. |
| `cooksFilter` | boolean |  | `true` |  | set the p-value of genes with a Cook's-distance outlier to NA. Only applies when method is DESeq2. |
| `cooksCutoff` | number |  |  | ≥ 0 | the Cook's distance cutoff; empty is DESeq2's F(0.99; p, m - p). Only applies when method is DESeq2. |
| `minReplicatesForReplace` | number |  | `7` | ≥ 3 | samples per group from which outlier counts are replaced and the gene refitted, instead of flagged. Only applies when method is DESeq2. |
| `shrink` | `"none"` · `"normal"` · `"apeglm"` · `"ashr"` |  | `"none"` |  | shrink the reported coefficient's or contrast's log2 fold changes toward zero where the counts cannot support them (DESeq2 lfcShrink), for ranking and plotting by effect size; p-values stay the unshrunken test's. apeglm: adaptive Cauchy prior, posterior mode (a coefficient only). ashr: mixture-of-normals prior, posterior mean. normal: DESeq2's original zero-centred Normal prior (Wald only), a contrast on the expanded model matrix. With lfcThreshold, apeglm and ashr give s-values of a false sign or a fold change inside the threshold, and normal re-tests the shrunken fit. Only applies when method is DESeq2. |
| `transform` | `"vst"` · `"VST"` · `"rlog"` · `"normTransform"` · `"none"` |  | `"vst"` |  | the count transformation the sample-level checks (PCA, sample distances) run on: vst (DESeq2's variance stabilizing transformation, the trend fitted on 1,000 genes; with fewer than 1,000 genes above a mean of 5 use VST), VST (varianceStabilizingTransformation, every gene), rlog (regularized log, a per-gene ridge fit, slow above ~30 samples) or normTransform (log2 of normalized count + 1, no stabilization). none skips the checks. Only applies when method is DESeq2. |
| `blind` | boolean |  | `true` |  | fit the transformation's dispersion trend under ~ 1, blind to the design (DESeq2's default, for quality assessment); off reuses the fitted design and trend, for downstream use when large differences between groups are expected. Only applies when method is DESeq2. |
| `pcaTop` | number |  | `500` | ≥ 2 | plotPCA's ntop: the PCA uses this many genes with the largest variance of the transformed values. Only applies when method is DESeq2. |
| `pcaGroup` | string |  | `""` |  | plotPCA's intgroup: the sample-table variables, separated by commas, that colour the samples (joined with ':' when more than one); empty is the factor of the reported comparison. Only applies when method is DESeq2. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `genes` | any |  | one row per gene: log2FoldChange, stat (DESeq2 Wald or LRT, edgeR F, voom moderated t), pvalue, padj, why padj is NA, the normalized counts per sample; DESeq2 adds baseMean, lfcSE, the gene-wise, fitted and final dispersions, whether it was refitted and with `shrink` the shrunken fold change, its SE and s-value (normal with lfcThreshold: the shrunken fit's p-value and padj); edgeR and voom add logCPM, the raw, prior and posterior variance (edgeR's QL dispersion) and the total df, and voom the B-statistic |
| `summary` | any |  | genes up and down at alpha and tested, with the method's own fit: DESeq2's outliers, low counts, filter threshold, size factors, dispersion trend and shrinkage prior; edgeR's common and average QL dispersion and prior df; voom's span and prior variance; the filterByExpr cutoffs and library sizes |
| `significantGenes` | string |  | genes with padj below alpha, one per line: the gene list for over-representation analysis |
| `upGenes` | string |  | significant genes with positive log2 fold change, one per line |
| `downGenes` | string |  | significant genes with negative log2 fold change, one per line |
| `testedGenes` | string |  | every gene with an adjusted p-value, one per line: the background (universe) for over-representation analysis |
| `rankedList` | string |  | tested genes by their test statistic, decreasing: DESeq2's Wald statistic, voom's moderated t, or edgeR's signed square root of F (a t with the same df): the ranked list for GSEA |
| `meanCounts` | string |  | DESeq2 runs only (empty under edgeR and voom): every tested gene with its mean normalized count (baseMean), 'gene value' per line: the gene weights for a Wallenius-weighted over-representation test, which corrects for the extra power to call well-counted genes |
| `maPlot` | object or null |  | log2 fold change (shrunken, with `shrink`) against mean normalized count (DESeq2) or average log2 CPM (edgeR, voom), significant genes apart |
| `maPlot.x` | number[] |  |  |
| `maPlot.series` | object[] |  |  |
| `maPlot.series[].name` | string |  |  |
| `maPlot.series[].y` | (number or null)[] |  |  |
| `maPlot.xLabel` | string |  |  |
| `maPlot.yLabel` | string |  |  |
| `maPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `maPlot.title` | string |  |  |
| `maPlot.rules` | object[] |  |  |
| `maPlot.rules[].y` | number |  |  |
| `maPlot.rules[].label` | string |  |  |
| `volcano` | object or null |  | -log10 p against log2 fold change, significant genes apart |
| `volcano.x` | number[] |  |  |
| `volcano.series` | object[] |  |  |
| `volcano.series[].name` | string |  |  |
| `volcano.series[].y` | (number or null)[] |  |  |
| `volcano.xLabel` | string |  |  |
| `volcano.yLabel` | string |  |  |
| `volcano.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `volcano.title` | string |  |  |
| `volcano.rules` | object[] |  |  |
| `volcano.rules[].y` | number |  |  |
| `volcano.rules[].label` | string |  |  |
| `dispersionPlot` | object or null |  | DESeq2: gene-wise, fitted and final dispersions against mean count. edgeR: quarter-root raw, squeezed and trend QL dispersions against average log2 CPM (plotQLDisp). voom: sqrt standard deviation against log2 count size, with the lowess trend that sets the weights |
| `dispersionPlot.x` | number[] |  |  |
| `dispersionPlot.series` | object[] |  |  |
| `dispersionPlot.series[].name` | string |  |  |
| `dispersionPlot.series[].y` | (number or null)[] |  |  |
| `dispersionPlot.xLabel` | string |  |  |
| `dispersionPlot.yLabel` | string |  |  |
| `dispersionPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `dispersionPlot.title` | string |  |  |
| `dispersionPlot.rules` | object[] |  |  |
| `dispersionPlot.rules[].y` | number |  |  |
| `dispersionPlot.rules[].label` | string |  |  |
| `samplePca` | object or null |  | DESeq2 runs only (null under edgeR and voom): plotPCA on the transformed counts (`transform`, `blind`): PC2 against PC1 per sample, one series per `pcaGroup` level, each axis labelled with its share of the variance |
| `samplePca.x` | number[] |  |  |
| `samplePca.series` | object[] |  |  |
| `samplePca.series[].name` | string |  |  |
| `samplePca.series[].y` | (number or null)[] |  |  |
| `samplePca.xLabel` | string |  |  |
| `samplePca.yLabel` | string |  |  |
| `samplePca.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `samplePca.title` | string |  |  |
| `samplePca.rules` | object[] |  |  |
| `samplePca.rules[].y` | number |  |  |
| `samplePca.rules[].label` | string |  |  |
| `sampleDistances` | any |  | DESeq2 runs only (null under edgeR and voom): the sample checks as data: the transformation and its trend, the PCA genes, percentVar, PC1 and PC2 per sample, the sample-to-sample Euclidean distance matrix over every gene and its complete-linkage clustering (leaf order, merges, heights), as the vignette's heatmap draws it; or why the checks could not run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "differential_expression",
  "arguments": {
    "counts": "<string>",
    "samples": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### discover_flag_rates

**Discover flag rates**: _How often does a corpus of maps carry a cryptic promoter, splice site or synthesis-breaking repeat more extreme than chance?_

Measure how often a corpus of maps carries a cryptic σ70 promoter, a cryptic splice site or a synthesis-breaking repeat MORE EXTREME THAN CHANCE, rather than how many it carries. Every map of a few kilobases spells promoters, splice donors and repeats, so a raw hit count measures length and composition; here each map's own extreme (its most negative promoter ΔG, its highest MaxEntScan donor and acceptor score, its longest homopolymer, tandem repeat, repeated stretch and hairpin arm) is scored against k-let-preserving shuffles of that same map, and the false discovery rate is controlled across the corpus within each statistic. No statistic uses a threshold: none of the three models publishes one, and a vendor's repeat limit is a product's capability, which `check_manufacturability` answers instead. The result is a per-statistic rate with an exact binomial interval, plus every map's own test. Cost is dominated by the σ70 scan at roughly a third of a second per map per shuffle, so a corpus of maps at the default 99 shuffles is minutes of work; drop `flags` to the statistics you need to make it cheaper.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- k-let-preserving shuffles of each map are the null for that map's own extremes.
- The promoter, splice and repeat models are the ones named, at their published scoring.

**Does not:**
- A rate against chance is not a manufacturability verdict; a vendor's limits are check_manufacturability's question.
- Cost is about a third of a second per map per shuffle for the promoter scan.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] |  |  |  | the corpus: wire upstream records here, or list library document names. Each is one record of the sweep. |
| `include_subject` | boolean |  | `true` |  | also test the node's subject (the open or wired record). |
| `flags` | (`"sigma70-strongest"` · `"splice-donor"` · `"splice-acceptor"` · `"homopolymer"` · `"tandem-repeat"` · `"long-repeat"` · `"inverted-repeat"`)[] |  |  |  | which statistics to run. Empty runs all seven. |
| `alpha` | number |  | `0.05` | 0.0001–0.5 | false discovery rate at which a record counts towards a flag's rate. |
| `correction` | `"BH"` · `"BY"` |  | `"BH"` |  | Benjamini–Hochberg (independent or positively dependent tests) or Benjamini–Yekutieli (any dependence; less power). Values: BH (Benjamini–Hochberg), BY (Benjamini–Yekutieli). |
| `shuffle_k` | number |  | `2` | 1–6 | k-let size the shuffles preserve. 2 holds every dinucleotide count, which is what all three statistics read. |
| `shuffles` | number |  | `99` | 9–999 | shuffles per record. The smallest p the null can give is 1 / (shuffles + 1), which is what bounds how small a corrected q can get. |
| `seed` | number |  | `1` | ≥ 0 | seed for the shuffles. Each record draws from seed + its own index, so a record's answer does not depend on the rest of the corpus. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rates` | any |  | per statistic: records tested, records above chance, the rate and its exact 95% interval |
| `hits` | any |  | every record whose statistic beat chance, smallest p first |
| `hitCount` | number |  | how many (record, statistic) tests were called |
| `tests` | any |  | every (record, statistic) test: the observed statistic, the shuffles' mean, p, q and the Monte Carlo interval |
| `nullModel` | string |  | the null the p-values stand on, stated with every run |
| `sweep` | any |  | the full result, including the records tested |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_flag_rates",
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

### discover_reference_concordance

**Discover reference concordance**: _Does a reference-gene stability ranking hold across conditions, and which candidates rank well everywhere?_

Ask whether a reference-gene stability ranking holds across conditions, and which candidate genes rank well everywhere rather than in one tissue or treatment. Each condition (the Group column of a long-format Cq table) is ranked by geNorm on its own samples; the conditions are then the blocks of a Friedman test and Kendall's W says how far they agree (0 independent orders, 1 the same order everywhere), with an asymptotic χ² p and a Monte Carlo p from shuffling each condition's ranks. Returns every gene's rank in every condition, its mean rank (the meta-ranking) and its best and worst. geNorm cannot order its two most stable genes, so they share rank 1.5 in every condition. Use `rank_reference_genes` for one condition's ranking by all four algorithms.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- Each Group in the Cq table is one condition with enough samples for geNorm to rank on its own.
- Cq values are on a common scale across conditions.

**Does not:**
- geNorm cannot order its two most stable genes, so they share a rank.
- Agreement between conditions is not stability within any one of them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cq_table` | string | **yes** |  |  | the long-format table `Target,Sample,Group,Cq`, one row per measurement; Group is the condition each sample was measured in, and every gene must be measured in every sample. |
| `permutations` | number |  | `999` | 9–99999 | shuffles of the ranks within each condition. The smallest p is 1 / (permutations + 1). |
| `seed` | number |  | `1` | ≥ 0 | seed for the shuffles. Each permutation draws from its own stream, so one can be re-run alone. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `genes` | any |  | every gene, most stable on average first: its rank in each condition, mean rank, best and worst |
| `w` | number or null |  | Kendall's coefficient of concordance across conditions |
| `p` | number or null |  | Monte Carlo p of W against within-condition shuffles |
| `conditions` | any |  | each condition's geNorm order with M |
| `nullModel` | string |  | the null, stated with every run |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_reference_concordance",
  "arguments": {
    "cq_table": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### discover_reference_stability

**Discover reference stability**: _Are candidate reference genes more or less variable across human tissues than genes of the same abundance?_

Ask whether the genes used to normalize expression (reference or housekeeping genes, such as GAPDH, ACTB or B2M) are more or less variable across human tissues than genes of the same abundance, on GTEx v8 median expression. Each candidate's standard deviation of log2(TPM + pseudocount) across the chosen tissues is ranked among the genes nearest it in mean expression (1,000 by default, from the 19,107 protein-coding genes GTEx measures), giving one p for 'more variable than its peers' and one for 'steadier', each corrected across the candidates. The four rankers the field runs (geNorm M, NormFinder, BestKeeper, comparative ΔCt, and RefFinder's consensus) also order the candidates against each other, reading the tissues as samples. A ranker always finds a most stable gene; the null says whether any candidate is stable at all. Tissue medians hide the variation between people within a tissue, so this answers 'across tissues', not 'across samples of one tissue'.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- GTEx v8 tissue medians stand for each tissue's expression.
- Genes nearest in mean expression are the right peers.

**Does not:**
- Answers 'across tissues', not 'across samples of one tissue'.
- A stability ranker always finds a most stable gene; only the peer null says whether any is stable at all.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** gtex-v8-median-tpm.json

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `genes` | string[] | **yes** |  |  | the candidate reference genes, as current HGNC symbols (GAPD is GAPDH). |
| `tissues` | string[] |  |  |  | GTEx tissue names to compare across, three or more; empty means all 54. |
| `neighbours` | number |  | `1000` | 20–19106 | how many genes nearest in mean expression each candidate is ranked among. The smallest p it can give is 1 / (neighbours + 1). |
| `alpha` | number |  | `0.05` | 0.0001–0.5 | false discovery rate at which a candidate is called more variable, or steadier, than its peers. |
| `correction` | `"BH"` · `"BY"` |  | `"BH"` |  | Benjamini–Hochberg (independent or positively dependent tests) or Benjamini–Yekutieli (any dependence; less power). Values: BH (Benjamini–Hochberg), BY (Benjamini–Yekutieli). |
| `pseudocount` | number |  | `1` | 0.01–10 | added to TPM before the logarithm, so a tissue with no expression has one. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `unstable` | any |  | the candidates more variable across tissues than their expression peers at the chosen false discovery rate |
| `stable` | any |  | the candidates steadier than their expression peers at the chosen false discovery rate |
| `candidates` | any |  | every candidate's mean and SD of log2 expression, the expression band of its peers, its percentile among them and both p and q |
| `rankers` | any |  | geNorm M, NormFinder, BestKeeper, comparative ΔCt and the RefFinder consensus over the candidates |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_reference_stability",
  "arguments": {
    "genes": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### discover_site_avoidance

**Discover site avoidance**: _Which exact restriction sites does each sequence carry far less, or far more, often than a stated null predicts?_

Sweep a set of sequences against every exact recognition site in the NEB catalog and report the sites each one carries far less (avoided) or far more (enriched) often than a stated null predicts, with the false discovery rate controlled across every (sequence, site) test. Avoidance is evidence of the restriction–modification systems a lineage has lived with, and a site a design can rely on being rare. Three nulls: base composition (order-0, Poisson); k-let-preserving shuffles (uShuffle), which holds dinucleotide skews such as CpG depletion in the null rather than reporting them as findings; and R'MES's maximal-order Markov model, the standard in published avoidance analyses, which judges a site of length k against the record's own (k−1)-mers so only what those cannot explain is reported.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The null named (base composition, k-let shuffles, or R'MES's maximal-order Markov model) is what 'expected' means; a finding is relative to it.
- Sites are NEB's exact recognition sequences; degenerate sites are not swept.

**Does not:**
- Avoidance is evidence of a lineage's restriction-modification history, not proof of it.
- Short sequences give little power for long sites.

**Validated:** against the reference implementation by 4 golden suites.

**Reads bundled data:** neb

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] |  |  |  | the corpus: wire upstream records here, or list library document names. Each is one record of the sweep. |
| `include_subject` | boolean |  | `true` |  | also sweep the node's subject (the open or wired record). |
| `enzymes` | string[] |  |  |  | restrict the sweep to these enzymes' sites (NEB names). Empty sweeps every exact site in the catalog; degenerate (IUPAC) sites are never swept and are listed in the result. Advanced. |
| `min_site_length` | number |  | `4` | 4–8 | shortest recognition site swept. In bp. |
| `alpha` | number |  | `0.05` | 0.0001–0.5 | false discovery rate at which a site is reported avoided or enriched. |
| `correction` | `"BH"` · `"BY"` |  | `"BH"` |  | Benjamini–Hochberg (independent or positively dependent tests) or Benjamini–Yekutieli (any dependence, including overlapping sites on one sequence; less power). Values: BH (Benjamini–Hochberg), BY (Benjamini–Yekutieli). |
| `null_model` | `"order0"` · `"shuffle"` · `"maximal"` |  | `"order0"` |  | what a site is rare relative to: base composition, shuffles that keep the record's own k-let counts, or the record's own (k−1)-mers for a site of length k (R'MES maximal order, Gaussian score). Values: order0 (Base composition (order-0)), shuffle (k-let shuffles (uShuffle)), maximal (Maximal-order Markov (R'MES)). |
| `shuffle_k` | number |  | `2` | 1–6 | k-let size the shuffles preserve. 2 holds every dinucleotide count, so CpG depletion is in the null. Only applies when null_model is shuffle. |
| `shuffles` | number |  | `99` | 9–9999 | shuffles per record. The smallest p the null can give is 1 / (shuffles + 1). Only applies when null_model is shuffle. |
| `seed` | number |  | `1` | ≥ 0 | seed for the shuffles, so a run reproduces. Only applies when null_model is shuffle. Advanced. |
| `positions` | boolean |  | `false` |  | also return every occurrence's coordinate and strand, for drawing on a map. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `avoided` | any |  | tests whose low-tail q is at or below alpha, most extreme ratio first |
| `enriched` | any |  | tests whose high-tail q is at or below alpha, most extreme ratio first |
| `avoidedCount` | number |  | how many (record, site) tests were called avoided |
| `enrichedCount` | number |  | how many (record, site) tests were called enriched |
| `tests` | any |  | every (record, site) test: observed, expected, ratio, both tails and both q-values; under the maximal-order null also the R'MES score z and its variance |
| `nullModel` | string |  | the null the p-values stand on, stated with every run |
| `correction` | string |  | the multiple-testing correction that ran, and why it is valid |
| `sweep` | any |  | the full result, including the records swept and the degenerate sites skipped |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_site_avoidance",
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

### discover_target_validation

**Discover target validation**: _Does the evidence in a set of gene-level tables support a hypothesis that one gene drives a phenotype, by sequential falsification?_

Test a hypothesis that a gene drives a phenotype ("gene G regulates IL-2 production") the way POPPER does: each evidence table is one falsification test, an implication of the hypothesis that a gene-level score could contradict (expression in the relevant tissue, association with related disease, interaction with genes annotated to the process). Under the null that G is exchangeable with any gene the tables score, G's p in each table is the share of genes scoring at or beyond it; each p is calibrated to the e-value κ·p^(κ−1), the e-values are multiplied in the order given, and the hypothesis passes when the product exceeds 1/α. The product is a valid e-value only when the tests are independent under the null, so the run also reports the joint p: the product's own share among every gene's product, valid whatever the tables' dependence. Returns every test's score, rank, p, e and running product, the test after which the product first crossed 1/α, and the joint p. Each table is `gene<TAB>score` with one header line; the gene must be in every table.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Under the null the gene is exchangeable with every other gene the tables score.
- The tables are fixed before the gene's scores are seen.

**Does not:**
- The product of e-values is valid only when the tests are independent under the null; the joint p is the answer whatever their dependence.
- Two or three tables answer fewer questions than a program of tests designed for the hypothesis.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `gene` | string | **yes** |  |  | the gene under test, as the tables spell it (HGNC symbol for the bundled corpus). |
| `tables` | object[] | **yes** |  |  | the falsification tests in the order to apply them: each `{ name, text, direction }`, where `text` is `gene<TAB>score` with a header line and `direction` is the end of the score the hypothesis predicts, `greater` (default) or `less`. |
| `alpha` | number |  | `0.1` | 0.001–0.5 | the hypothesis passes when the product of e-values exceeds 1/α. |
| `kappa` | number |  | `0.5` | 0.01–0.99 | κ of the p-to-e calibrator κ·p^(κ−1); POPPER's default is 0.5. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rejected` | boolean |  | whether the product of e-values exceeded 1/α |
| `combined` | number or null |  | the product of the calibrated e-values |
| `jointP` | number or null |  | the product's share among every gene's product |
| `tests` | any |  | each test: score, genes at or beyond, p, e and running product |
| `nullModel` | string |  | the null, stated with every run |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_target_validation",
  "arguments": {
    "gene": "<string>",
    "tables": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### gene_set_camera

**Gene set camera**

Competitive gene set test that accounts for inter-gene correlation (camera; Wu & Smyth 2012), as limma 3.68.5 runs it: is a set more differentially expressed than the genes outside it, with the variance of its mean statistic inflated by the correlation between its genes instead of treating them as independent. From a count table it fits voom (filterByExpr, TMM, precision weights) and tests the design's coefficient per set (camera); from a ranked statistic it tests that statistic directly (cameraPR). Parametric or rank-based, fixed or per-set estimated correlation, directional or not. Every set is bit-identical to limma in R on filtered pasilla voom and on DESeq2's Wald statistics against every fly GO term.

<sub>read-only · runs locally on the engine · randomness: unknown</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `statistic` | `"ranked"` · `"voom"` |  | `"ranked"` |  | ranked: cameraPR on a supplied gene-wise statistic (`ranked`). voom: camera on a voom fit of `counts` and `samples`, each gene's own residuals and weights. Given only `counts`, voom is assumed. |
| `ranked` | string |  | `""` |  | a gene-wise statistic, 'gene statistic' per line (e.g. a DE run's Wald or moderated t). Only applies when statistic is ranked. |
| `counts` | string |  | `""` |  | a gene-by-sample table of raw read counts, gene IDs in the first column: camera then runs on its voom fit (filterByExpr, TMM, voom weights). Give this or `ranked`. Only applies when statistic is voom. |
| `samples` | string |  | `""` |  | with `counts`: one row per sample, its name first, then the design's variables. Only applies when statistic is voom. |
| `design` | string |  | `"~ condition"` |  | with `counts`: the design formula, the variable of interest last. Only applies when statistic is voom. |
| `reference` | string |  | `""` |  | reference level per factor, 'variable=level' separated by commas; a factor not named takes its alphabetically first level. Only applies when statistic is voom. |
| `name` | string |  | `""` |  | the tested coefficient by name; empty is the design's last. Only applies when statistic is voom. |
| `contrast` | string |  | `""` |  | 'factor, numerator, denominator', the denominator being the factor's reference level. Only applies when statistic is voom. |
| `filterByExpr` | boolean |  | `true` |  | drop genes too lowly expressed to test (edgeR's filterByExpr) before voom. Only applies when statistic is voom. |
| `minCount` | number |  | `10` | ≥ 0 | filterByExpr: minimum count in the smallest group's worth of samples. Only applies when statistic is voom. |
| `minTotalCount` | number |  | `15` | ≥ 0 | filterByExpr: minimum total count. Only applies when statistic is voom. |
| `geneSets` | string | **yes** |  |  | the gene sets, as GMT text (MSigDB, GO or WikiPathways exports): one set per line, tab-separated ID, description, then member gene IDs. IDs must be the same kind as the genes'. |
| `useRanks` | boolean |  | `false` |  | a correlation-adjusted Wilcoxon rank-sum test instead of the parametric t on z-scores; robust to a few extreme genes. |
| `interGeneCor` | number |  | `0.01` | -0.99–0.99 | the fixed inter-gene correlation, limma's default 0.01 (a value most real sets exceed slightly). |
| `estimateCorrelation` | boolean |  | `false` |  | with `counts`: estimate each set's correlation from the residuals instead of fixing it; the test then uses min(residual df, genes - 2) degrees of freedom. Only applies when statistic is voom. |
| `allowNegCor` | boolean |  | `false` |  | with an estimated correlation: let a negative estimate deflate the variance (limma floors it at 0). Only applies when statistic is voom. |
| `directional` | boolean |  | `true` |  | test up or down against the rest (true), or only whether the set's genes change more in either direction (false, a rank test on \|statistic\|). |
| `fdrCutoff` | number |  | `0.05` | 0–1 | a set is called when its BH FDR (its p-value when one set is tested) is at most this. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `terms` | any |  | every set with a member among the tested genes, by p: genes in the set, correlation, direction, p and BH FDR |
| `enriched` | any |  | the sets at or under the FDR cutoff |
| `summary` | any |  | the mode (voom camera or cameraPR), genes tested, sets supplied and tested, the degrees of freedom, the prior df of the variance squeeze, the settings limma changed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "gene_set_camera",
  "arguments": {
    "geneSets": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### gene_set_enrichment

**Gene set enrichment**

Preranked gene set enrichment analysis (GSEA; Subramanian et al. 2005) with fgsea's multilevel p-values (Korotkevich et al.), either as clusterProfiler's GSEA() runs it (enrichit 0.2.6, with q-values; or its fixed-count or adaptive sample and permute tests) or as fgsea 1.38 itself runs it (fgseaMultilevel, or fgseaSimple with a permutation count): weighted running-sum enrichment score, normalized ES against size-matched permutations, multilevel Monte Carlo p-values down to eps, adjusted p, log2err, rank at maximum, leading-edge genes. Seeded: a seed reproduces the chosen package's p-values exactly, and every set is bit-identical to that package in R on pasilla's DESeq2 Wald statistics against every fly GO term.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `ranked` | string | **yes** |  |  | the ranked list: 'gene statistic' per line (tab, comma or space), e.g. a DE run's Wald statistic; sorted decreasing here if it is not. |
| `geneSets` | string | **yes** |  |  | the gene sets, as GMT text (MSigDB, GO or WikiPathways exports): one set per line, tab-separated ID, description, then member gene IDs. IDs must be the same kind as the genes'. |
| `minGSSize` | number |  | `10` | ≥ 1 | smallest set tested, counted among the ranked genes. |
| `maxGSSize` | number |  | `500` | ≥ 1 | largest set tested, counted among the ranked genes. |
| `exponent` | number |  | `1` | ≥ 0 | weight of each gene's statistic in the running sum: 0 is the unweighted Kolmogorov-Smirnov form, 1 classic GSEA. |
| `scoreType` | `"std"` · `"pos"` · `"neg"` |  | `"std"` |  | std: both tails; pos or neg: one-tailed, for a statistic with one meaningful sign (the multilevel estimate only). Only applies when method is multilevel. |
| `eps` | number |  | `1e-10` | ≥ 0 | floor for multilevel p-values; 0 estimates them however small. Only applies when method is multilevel. |
| `sampleSize` | number |  | `101` | ≥ 3 | multilevel samples per level (made odd). Only applies when method is multilevel. |
| `nPermSimple` | number |  | `1000` | ≥ 1 | multilevel: permutations for the first, simple p-value estimate and the NES. Only applies when method is multilevel. |
| `seed` | number |  | `12345` |  | seeds the permutations; the same seed gives the same p-values as the chosen engine in R (fgsea: set.seed(seed) before the call). |
| `engine` | `"clusterProfiler"` · `"fgsea"` |  | `"clusterProfiler"` |  | clusterProfiler: enrichit 0.2.6's GSEA, what clusterProfiler 4.20's GSEA() runs, with q-values. fgsea: fgsea 1.38's own, a different random stream and arithmetic, so the same seed gives fgsea's p-values; BH only, no q-value. |
| `nperm` | number |  | `0` | ≥ 0 | fgsea: run fgseaSimple with this many permutations (p-values no smaller than 1/(nperm + 1)); 0 keeps the multilevel estimate. Only applies when engine is fgsea. |
| `method` | `"multilevel"` · `"sample"` · `"permute"` |  | `"multilevel"` |  | clusterProfiler's p-value: multilevel Monte Carlo (fgsea-derived, down to eps); sample: a fixed count of random gene samples of each set's size; permute: that count of relabellings of the whole ranked list (slower: every set is re-scored along every permuted list). The permutation methods score both tails whatever the score type. Only applies when engine is clusterProfiler. |
| `permutations` | number |  | `1000` | ≥ 1 | sample or permute: null draws per set (p-values no smaller than 1/(same-side draws + 1)). Only applies when method is sample or permute. |
| `adaptive` | boolean |  | `false` |  | sample or permute: draw per set in batches from minPerm, doubling while its p-value is at most pvalThreshold, up to maxPerm, instead of a fixed count. Only applies when method is sample or permute. |
| `minPerm` | number |  | `101` | ≥ 1 | adaptive: the first batch for every set. Only applies when adaptive is true. |
| `maxPerm` | number |  | `100000` | ≥ 1 | adaptive: the most draws any set gets. Only applies when adaptive is true. |
| `pvalThreshold` | number |  | `0.1` | 0–1 | adaptive: a set whose p-value rises above this stops drawing. Only applies when adaptive is true. |
| `pAdjustMethod` | `"holm"` · `"hochberg"` · `"hommel"` · `"bonferroni"` · `"BH"` · `"BY"` · `"fdr"` · `"none"` |  | `"BH"` |  | multiple-testing adjustment across the tested sets (R `p.adjust`). |
| `pvalueCutoff` | number |  | `0.05` | 0–1 | a set is significant when p and adjusted p are at most this. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `terms` | any |  | every set in the size range, by \|NES\|: ES, NES, p, adjusted p, q-value, log2err, rank at maximum, leading-edge statistics and genes, and the ranks of the set's members |
| `enriched` | any |  | the sets passing the p and adjusted-p cutoff |
| `summary` | any |  | ranked genes, ties, whether the list was re-sorted, sets supplied and in range, significant sets, q-value route |
| `runningScore` | object or null |  | the running enrichment score along the ranked list for the top set, with its hits |
| `runningScore.x` | number[] |  |  |
| `runningScore.series` | object[] |  |  |
| `runningScore.series[].name` | string |  |  |
| `runningScore.series[].y` | (number or null)[] |  |  |
| `runningScore.xLabel` | string |  |  |
| `runningScore.yLabel` | string |  |  |
| `runningScore.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `runningScore.title` | string |  |  |
| `runningScore.rules` | object[] |  |  |
| `runningScore.rules[].y` | number |  |  |
| `runningScore.rules[].label` | string |  |  |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "gene_set_enrichment",
  "arguments": {
    "ranked": "<string>",
    "geneSets": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### gene_set_overrepresentation

**Gene set overrepresentation**

Over-representation analysis (ORA): which gene sets hold more of a gene list than chance, by the one-sided hypergeometric test against a background, as clusterProfiler's enricher() runs it (enrichit 0.2.6). Reports gene and background ratios, fold enrichment, odds ratio, z-score, p, adjusted p and Storey q-value per set, and which sets pass both cutoffs. Every tested set is bit-identical to enrichit in R on pasilla's DE genes against every fly GO term.

<sub>read-only · runs locally on the engine · randomness: unknown</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `genes` | string | **yes** |  |  | the gene list (e.g. the significant genes of a DE run), one ID per line or separated by commas or spaces. |
| `geneSets` | string | **yes** |  |  | the gene sets, as GMT text (MSigDB, GO or WikiPathways exports): one set per line, tab-separated ID, description, then member gene IDs. IDs must be the same kind as the genes'. |
| `universe` | string |  | `""` |  | the background: every gene the experiment could have called (e.g. a DE run's tested genes). Empty is every gene any set annotates, clusterProfiler's default. |
| `forceUniverse` | boolean |  | `false` |  | use `universe` as given instead of intersecting it with the annotated genes. |
| `weights` | string |  | `""` |  | per-gene sampling weights, 'gene weight' per line (e.g. a DESeq2 run's mean normalized counts, `meanCounts`, or gene lengths): replaces the hypergeometric test with Wallenius' noncentral one (BiasedUrn), each set's odds being its members' mean weight over the rest of the background's, so a set of well-counted or long genes is not called for being easy to detect. Background genes without a weight take the median; weights at or below 0 are lifted to the smallest positive one. Empty is the unweighted test. |
| `minGSSize` | number |  | `10` | ≥ 1 | smallest set tested, counted within the background. |
| `maxGSSize` | number |  | `500` | ≥ 1 | largest set tested, counted within the background. |
| `pAdjustMethod` | `"holm"` · `"hochberg"` · `"hommel"` · `"bonferroni"` · `"BH"` · `"BY"` · `"fdr"` · `"none"` |  | `"BH"` |  | multiple-testing adjustment across the tested sets (R `p.adjust`). |
| `pvalueCutoff` | number |  | `0.05` | 0–1 | a set is enriched when p and adjusted p are at most this. |
| `qvalueCutoff` | number |  | `0.2` | 0–1 | and its q-value at most this. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `terms` | any |  | every tested set, by p: count, set size, gene and background ratios, fold enrichment, odds ratio, z-score, p, adjusted p, q-value, the hit genes |
| `enriched` | any |  | the sets passing the p, adjusted-p and q cutoffs |
| `summary` | any |  | input genes, how many are in the background, the background size, sets supplied, in the size range and tested, and the q-value route |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "gene_set_overrepresentation",
  "arguments": {
    "genes": "<string>",
    "geneSets": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### resolve_gene_sets

**Resolve gene sets**: _Which gene sets do GO or Reactome define for this organism right now?_

Gene sets for an organism, fetched from the authority at run time instead of a bundled list: Gene Ontology terms from the GO Consortium's own annotation file for the organism (each term's direct annotations, NOT annotations dropped, term names from QuickGO), or Reactome pathways from Reactome's AnalysisService (each pathway's members among the genes you submit, in the species Reactome resolves). Returns GMT text for gene_set_overrepresentation, gene_set_enrichment and gene_set_camera, with the source, release and retrieval date.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Assumes:**
- GO: a set is a term's direct annotations in the GO Consortium file whose metadata names the organism's NCBI taxon; annotations are not propagated to ancestor terms.
- Reactome: a set is the submitted genes Reactome maps into one pathway, inferred pathways included.

**Does not:**
- Needs the network.
- GO covers the organisms the GO Consortium publishes an annotation file for; others are annotated by UniProt accession in QuickGO.
- Reactome's sets hold only the submitted genes, so an over-representation background of every annotated gene becomes the annotated genes among those submitted.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `authority` | `"go"` · `"reactome"` |  | `"go"` |  | go: every GO term with a direct annotation in the organism. reactome: Reactome's pathways, restricted to the genes in `genes`. Values: go (GO · GO Consortium), reactome (Reactome · AnalysisService). |
| `organism` | string | **yes** |  |  | the organism: an NCBI taxon ID (7227) or a name (Drosophila melanogaster, human); GO resolves it through NCBI Taxonomy, Reactome resolves it itself. |
| `genes` | string |  | `""` |  | reactome: the genes to map, one per line (a 'gene value' line keeps its first field), e.g. a DE run's tested genes, in an ID system Reactome reads (Ensembl, UniProt, NCBI Gene, a model organism's own). Only applies when authority is reactome. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `geneSets` | string |  | the sets as GMT text: ID, name, member genes |
| `provenance` | any |  | the authority, the organism it resolved, its release, the retrieval date, every URL read and what the sets are restricted to |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "resolve_gene_sets",
  "arguments": {
    "organism": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### run_discovery_programme

**Run discovery programme**: _Which pre-registered hypotheses does a program of falsification tests support, with the false discovery rate controlled across all of them?_

Run a discovery program end to end under pre-registration: every hypothesis names its test (discover_site_avoidance: a site, optionally a record, and its null; discover_codon_outliers: a gene and its genetic code; validate_gene_trait: a human gene, the trait's own gene or tissues, and GWAS Catalog categories; discover_flag_rates: a cryptic-element flag, optionally a record, against k-let shuffles; discover_tree_incongruence: a locus of a multi-locus alignment, by the ILD test; discover_gene_tree_discordance: a gene alignment against a species tree, by the SH test; discover_reference_stability: a candidate reference gene against its GTEx abundance peers; discover_annotation_contradictions: a UniProt signal peptide or transmembrane segment against the experimentally confirmed ones; discover_reference_concordance: a Cq table whose conditions should rank its reference genes alike; differential_expression: a gene of a DESeq2 fit, up or down in the contrast; gene_set_overrepresentation: a gene set holding more of a gene list than chance; gene_set_enrichment: a gene set toward the top or bottom of a ranked list by GSEA) and direction, and all are registered in a hypothesis ledger before any test runs. Each registered test then runs once over the corpus, every answering result is attached as a κ-calibrated e-value (evidence from another test, a changed parameter or the same data twice is refused and reported), and e-BH decides over all hypotheses, those without evidence included. Returns the verdicts, the whole ledger as a file that imports into Discovery Expert, every run's input, the refusals, and the literature query each supported hypothesis needs before it may be called new. Pass a previous ledger with posterior beliefs to get the follow-up order by Bayesian surprise, which ranks what to test next and never changes a verdict. Also returns the whole program as a sealed run file (every corpus input pinned by SHA-256, the last attempt at each hypothesis); pass it back as `run` to add hypotheses and retry the ones whose test failed, or to research_run_status and resume_research_run. Evidence that read one source (one table, or one sequence under two names) is averaged, not multiplied, and each verdict names the rule.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Every hypothesis names its test and direction before any test runs.
- e-values from tests that read different sources are independent; evidence that read one source is averaged, not multiplied.

**Does not:**
- A supported hypothesis still needs the literature query it carries before it may be called new.
- Bayesian surprise orders follow-ups and never changes a verdict.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] |  |  |  | the corpus every registered test runs over: library document or file names, or wired records. |
| `hypotheses` | object[] |  |  |  | each {statement, test, params, direction, prior_belief?}. test: discover_site_avoidance (params site, record?, null_model, shuffle_k/shuffles/seed under the shuffle null; direction less, greater or two-sided) or discover_codon_outliers (params gene as its library name, genetic_code, alt_init?, min_codons?; direction two-sided) or validate_gene_trait (params gene as its HGNC symbol, expression_test coexpression with trait_genes or tissue with tissues, categories as GWAS Catalog parent categories, alpha?; direction greater; needs no corpus) or discover_flag_rates (params flag as one of sigma70-strongest, splice-donor, splice-acceptor, homopolymer, tandem-repeat, long-repeat, inverted-repeat, record?, shuffle_k/shuffles/seed; direction greater, meaning beyond chance in the flag's own tail) or discover_tree_incongruence (params locus as its alignment file's name, permutations/seed; direction greater; the corpus is one aligned FASTA per locus) or discover_gene_tree_discordance (params gene as its alignment file's name, species_tree in Newick, replicates/sh_form/gamma_categories/seed; direction greater, meaning the gene fits another tree better; the corpus is one aligned FASTA per gene) or discover_reference_stability (params gene as its HGNC symbol, tissues?, neighbours?, pseudocount?; direction greater for more variable than its abundance peers, less for steadier, or two-sided; needs no corpus) or discover_annotation_contradictions (params annotation as a UniProt accession, or accession:start-end where the protein has several, feature signal or transmembrane, predictor for signal, decoding for transmembrane; direction less, meaning it scores below the experimentally confirmed features; needs no corpus) or discover_reference_concordance (params cq_table as the long-format Target,Sample,Group,Cq table itself, permutations/seed; direction greater, meaning the conditions rank the genes more alike than independent orders; needs no corpus) or differential_expression (params gene as its count-table ID, symbol? as papers name it for the literature query, counts and samples as the tables themselves, and design/reference/test/reduced/contrast/name/fitType/sfType/lfcThreshold/altHypothesis/cooksFilter/cooksCutoff/minReplicatesForReplace as the tool takes them; direction greater for higher in the contrast's numerator, less for lower, or two-sided; one-sided needs the Wald test at lfcThreshold 0; needs no corpus) or gene_set_overrepresentation (params set as its GMT ID, genes, geneSets as GMT text, universe?, forceUniverse?, minGSSize?, maxGSSize?; direction greater; needs no corpus) or gene_set_enrichment (params set as its GMT ID, ranked as 'gene statistic' lines, geneSets as GMT text, minGSSize/maxGSSize/exponent/scoreType/eps/sampleSize/nPermSimple/seed; direction greater for toward the top of the list, less for the bottom, or two-sided; needs no corpus). prior_belief: the proposer's belief before any result, one sample or a list of them (true, false, definitely true, maybe true, uncertain, maybe false, definitely false, cannot comment). |
| `ledger` | object |  |  |  | a ledger file from an earlier run, to continue: its hypotheses keep their evidence and new ones are added beside them. |
| `run` | object |  |  |  | a run file from an earlier call, to continue it: its seal and its pinned inputs are checked, hypotheses whose test failed or was deferred are retried, new ones are added, and nothing answered is run again. |
| `budget_seconds` | number |  |  | ≥ 0 | seconds this call may spend running tests: whole tests run until the budget is spent and the rest are deferred, so a long program returns before a client's timeout and resume_research_run continues it. A test is never cut short and at least one runs per call. Unset: every test runs in this call. In s. Advanced. |
| `posterior_beliefs` | object[] |  |  |  | each {id, samples}: the proposer's belief in a hypothesis after reading its evidence. With prior beliefs these give the follow-up order by Bayesian surprise. |
| `alpha` | number |  | `0.1` | 0.001–0.5 | e-BH level the verdicts are decided at, across every hypothesis in the ledger. |
| `kappa` | number |  | `0.5` | 0.01–0.99 | κ of the p-to-e calibrator e = κ·p^(κ−1); fixed for a ledger once it holds evidence. Advanced. |
| `organism` | string |  |  |  | the organism the corpus is from, for the literature query each supported hypothesis needs. Advanced. |
| `check_literature` | boolean |  | `false` |  | run each supported hypothesis's literature query against Europe PMC and record what came back in the ledger: papers to read (candidates) or none (not found). Never records a hypothesis as known; confirm_literature_hit does that for a paper someone read. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `decisions` | any |  | every hypothesis: verdict (supported, not-supported, no-evidence), product e-value and tests |
| `supportedCount` | number |  | how many hypotheses e-BH supports |
| `ledger` | any |  | the whole ledger as a jane.discovery-ledger file, every hypothesis and its evidence with traces |
| `followUp` | any |  | hypotheses with prior and posterior beliefs, most surprising first: what to test next, never a verdict |
| `report` | any |  | the program as text lines: registrations, runs, refusals, verdicts, literature queries |
| `run` | any |  | the whole program as a sealed jane.research-run file: the ledger, every corpus input pinned by SHA-256, the last attempt at each hypothesis. Pass it back to continue |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "run_discovery_programme",
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

### validate_gene_trait

**Validate gene trait**: _Does public expression and GWAS evidence support a hypothesis that a gene is involved in a trait, by sequential falsification?_

Put a hypothesis of the form "gene G is involved in trait T" through POPPER-style sequential falsification on two public tables, each test fixed in advance and run in a fixed order. (1) GTEx v8 expression: either G's co-expression across the 54 tissues with the trait's own gene(s), such as IL2 for IL-2 production, or G's expression in named tissues against its own elsewhere. (2) The GWAS Catalog: how many studies place an association inside G for traits in the named GWAS Catalog categories. Each p is G's rank among the 19,107 protein-coding genes GTEx measures, so it is exact under the null that G is just another gene, with no model of how expression or GWAS hits are distributed. Each p becomes an e-value (κ calibrator), the running product is the evidence, and testing stops at the first product above 1/α, which is POPPER's own sequential stop. Benchmarked on POPPER's TargetVal (Schmidt et al. 2022 CRISPR screens): it holds Type-I below α and has far less power than an agent writing its own tests, because two tables answer fewer questions; the result says which tests were run and what each could and could not show.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Under the null the gene is exchangeable with any of the protein-coding genes GTEx v8 measures.
- GTEx tissue medians and GWAS Catalog categories are the evidence the hypothesis implies.

**Does not:**
- Two public tables answer fewer questions than tests written for the hypothesis; power is low.
- Tissue medians hide variation between people within a tissue.

**Not read from this result:** The per-test e-values, the stopped product and this setting's own Type-I rate. The Hypothesis ledger reads a LEDGER of pre-registered tests rather than one test, so its reading has no single-test form.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** gtex-v8-median-tpm.json, gwas-catalog-gene-categories.json

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `gene` | string | **yes** |  |  | the hypothesis gene, as its current HGNC symbol (protein-coding). |
| `expression_test` | `"coexpression"` · `"tissue"` |  | `"coexpression"` |  | which GTEx test: co-expression with the trait's own gene(s), or expression in named tissues against the gene's own elsewhere. One only, because both read GTEx and one table is one piece of evidence. Values: coexpression (Co-expression with the trait's gene), tissue (Expression in named tissues). |
| `trait_genes` | string[] |  |  |  | co-expression: the trait's own gene(s) as HGNC symbols, such as IL2 for IL-2 production. |
| `tissues` | string[] |  |  |  | tissue test: GTEx tissue names where involvement implies higher expression, such as Whole Blood or Spleen. |
| `categories` | string[] | **yes** |  |  | GWAS Catalog parent categories an involved gene's associations should fall in, such as Immune system disorder. |
| `alpha` | number |  | `0.1` | 0.001–0.5 | the level the sequential test stops and decides at: supported when the product of e-values exceeds 1/α. |
| `kappa` | number |  | `0.5` | 0.01–0.99 | κ of the p-to-e calibrator e = κ·p^(κ−1). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `supported` | boolean |  | whether the stopped product of e-values exceeds 1/α |
| `e` | number |  | the stopped product of e-values: the evidence against "G is just another gene" |
| `nullRate` | any |  | these settings' own Type-I rate: how many of the universe's genes, each taken as the hypothesis, the same test would support |
| `tests` | any |  | every falsification test in its registered order: what it reads, its statistic, G's value, its rank among the genes and its p, and whether it was run before the stop |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "validate_gene_trait",
  "arguments": {
    "gene": "<string>",
    "categories": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
