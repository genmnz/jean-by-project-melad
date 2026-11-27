# 📊 Sequence analysis

_Everything else a bench scientist asks of a sequence._

67 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`analyze_flow_cytometry`](#analyze_flow_cytometry) | How many events fall in each gated population of this FCS file, and what are their per-channel intensities? |
| [`analyze_flow_cytometry_ploidy`](#analyze_flow_cytometry_ploidy) | What are the cell-cycle phases and DNA content in this DNA-stained sample? |
| [`analyze_rt_pcr`](#analyze_rt_pcr) | Does this primer pair span an exon junction, and would genomic DNA amplify too? |
| [`auto_gate_flow_cytometry`](#auto_gate_flow_cytometry) | Where would openCyto place its automated gates on these two channels, and how many events fall on each side? |
| [`batch_flow_cytometry`](#batch_flow_cytometry) | How does each population change across samples, and between groups of samples? |
| [`blast_project_sequences`](#blast_project_sequences) | Which of this project's own records carry this span, with what E-values? |
| [`blast_search`](#blast_search) | Which public sequences resemble this one, with what E-values? |
| [`calibrate_flow_cytometry_beads`](#calibrate_flow_cytometry_beads) | Which bead population is each event, and how does each channel map to MEF? |
| [`check_assay_decay`](#check_assay_decay) | How often do a published assay's oligos mismatch the genomes circulating now, and where in each oligo do the mismatches sit? |
| [`check_flow_cytometry_quality`](#check_flow_cytometry_quality) | Which stretches of this acquisition were unstable, and which events should be removed? |
| [`check_primer_specificity`](#check_primer_specificity) | Do these primer pairs make products off their template, and which pair ranks best by it? |
| [`check_rows`](#check_rows) | Does every row of this table satisfy the rule, and which rows broke it? |
| [`classify_flow_cytometry_events`](#classify_flow_cytometry_events) | Which population would a model trained on the gated ones assign each event to, or where does the density put a 2-D gate? |
| [`cluster_flow_cytometry_events`](#cluster_flow_cytometry_events) | Which clusters do the events of this population form, and how large is each? |
| [`cluster_flow_cytometry_flowsom`](#cluster_flow_cytometry_flowsom) | Which cell populations does FlowSOM find in this file, and how large is each? |
| [`compare_antibodies`](#compare_antibodies) | How do these antibodies' heavy (or light) variable domains differ position by position, and how do their lengths, pI, charge, hydropathy, extinction and CDR charge compare? |
| [`correct_flow_cytometry_batches_cycombine`](#correct_flow_cytometry_batches_cycombine) | Where must each cell move so that the batches agree within every group of similar cells, without a control sample? |
| [`enzyme_cut_counts`](#enzyme_cut_counts) | How many times does each enzyme cut this molecule? |
| [`estimate_cytof_spillover`](#estimate_cytof_spillover) | How much does each metal channel of this mass cytometry panel spill into the others? |
| [`estimate_flow_cytometry_scale`](#estimate_flow_cytometry_scale) | Which transform parameters does this data itself support? |
| [`estimate_spectra_from_controls`](#estimate_spectra_from_controls) | What spectral signatures do these single-stain controls imply? |
| [`estimate_spillover_from_controls`](#estimate_spillover_from_controls) | What spillover matrix do these compensation controls imply? |
| [`filter_items`](#filter_items) | Which rows of this table meet the condition, and how many were dropped? |
| [`find_common_substructure`](#find_common_substructure) | What is the largest substructure all of these molecules share? |
| [`find_orfs`](#find_orfs) | Which open reading frames does this molecule carry, on both strands? |
| [`find_primer_snps`](#find_primer_snps) | Which known dbSNP variants sit under these primers, and how far is each from the 3' end? |
| [`fit_flow_cytometry_cell_cycle`](#fit_flow_cytometry_cell_cycle) | What share of these DNA-stained cells is in G1, S and G2/M? |
| [`fit_flow_cytometry_compass`](#fit_flow_cytometry_compass) | Which cytokine combinations respond to stimulation in each subject, and how polyfunctional is the response? |
| [`fit_flow_cytometry_proliferation`](#fit_flow_cytometry_proliferation) | How many divisions have these dye-labeled cells gone through, and what share sits in each generation? |
| [`fit_flow_cytometry_trajectory`](#fit_flow_cytometry_trajectory) | Which developmental paths run through these clusters, and how far along each path is every event? |
| [`flow_cytometry_kinetics`](#flow_cytometry_kinetics) | How does this channel change over the acquisition, and what are its peak, slope and area in each time range? |
| [`fold_rna`](#fold_rna) | What is the minimum-free-energy secondary structure of this sequence, and its free energy? |
| [`fragment_ions`](#fragment_ions) | Which theoretical fragment ions does this peptide give, at each charge? |
| [`gc_content`](#gc_content) | What is this sequence's GC fraction, overall or along a sliding window? |
| [`genotype_pca`](#genotype_pca) | What population structure do these genotypes show in their principal components? |
| [`hmm_build`](#hmm_build) | What profile HMM does hmmbuild make of this alignment, and with what E-value statistics? |
| [`hmm_search`](#hmm_search) | How well does each sequence score against this profile HMM, where does the model match, and does it clear the family’s own gathering cutoff? |
| [`hmmscan`](#hmmscan) | Which of these profile HMMs does the protein carry, in which domains, with what E-values? |
| [`impute_flow_cytometry_infinity`](#impute_flow_cytometry_infinity) | What would every Infinity marker of the screen read on each cell, from the backbone alone? |
| [`isotope_envelope`](#isotope_envelope) | What coarse isotope pattern does this peptide or formula show: the heights and masses of M, M+1, M+2 and beyond? |
| [`isotopic_composition`](#isotopic_composition) | Which isotopic composition is this peptide most likely to carry, and how abundant is it? |
| [`linkage_disequilibrium`](#linkage_disequilibrium) | How much linkage disequilibrium is there between each pair of biallelic sites, and which sites survive pruning? |
| [`load_trace`](#load_trace) | What bases, qualities and trim bounds does this Sanger trace carry? |
| [`mask_sequence`](#mask_sequence) | Which stretches of this sequence should a similarity search not seed on? |
| [`match_part_by_sequence`](#match_part_by_sequence) | Which published iGEM part carries exactly these bases? |
| [`miqe_checklist`](#miqe_checklist) | Which MIQE 2.0 items does a qPCR paper provide, and where, or why are they omitted? |
| [`normalize_cytof_beads`](#normalize_cytof_beads) | How much did the instrument's sensitivity drift over these acquisitions, and what are the counts with that drift taken out? |
| [`normalize_flow_cytometry_batch`](#normalize_flow_cytometry_batch) | Do the same populations sit at the same place on each channel across these samples, and if not, by how much must each be moved? |
| [`normalize_flow_cytometry_cytonorm`](#normalize_flow_cytometry_cytonorm) | How must each batch be moved so that its control sample matches the others, and what does that do to the samples of that batch? |
| [`rank_reference_genes`](#rank_reference_genes) | Which candidate reference genes are most stable on this plate, by geNorm, NormFinder, BestKeeper, comparative delta-Ct and their consensus? |
| [`read_eds_run`](#read_eds_run) | What run, plate, dyes and amplification curves does this QuantStudio .eds hold? |
| [`read_mgf`](#read_mgf) | What spectra does this MGF file hold? |
| [`read_mzml`](#read_mzml) | What spectra, precursors and acquisition metadata does this mzML run hold? |
| [`read_structure`](#read_structure) | What is in this structure file: chains, sequences, ligands, solvent, disulfides, modified residues, B-factors, cell, resolution and experiment? |
| [`record_composition`](#record_composition) | What is this record made of: molecular weight under its own topology, GC and AT, and the per-symbol census? |
| [`relative_expression`](#relative_expression) | How much does a gene's expression change between groups, by delta-delta-Ct, delta-Ct or the standard-curve model, with a significance test on request? |
| [`reverse_complement`](#reverse_complement) | What is the reverse complement of this sequence, with its annotations carried over? |
| [`scan_intrinsic_terminators`](#scan_intrinsic_terminators) | Which rho-independent terminators does this bacterial sequence carry, and how good is each hairpin and tail? |
| [`scan_sigma70_promoters`](#scan_sigma70_promoters) | Which sigma70 promoters does this bacterial sequence carry, and how strong is each by the La Fleur-Hossain-Salis biophysical model? |
| [`scan_splice_sites`](#scan_splice_sites) | Which splice donors and acceptors does this sequence spell, by maximum-entropy strength and by typicality against measured Arabidopsis sites? |
| [`score_spectrum`](#score_spectrum) | How well does this MS/MS spectrum match this peptide, by X!Tandem HyperScore? |
| [`size_fragments`](#size_fragments) | What size in bases is each peak of this fragment run, against its own size standard? |
| [`summarize_rows`](#summarize_rows) | What is this table column's summary: its largest, smallest, median, mean or spread, overall or per group? |
| [`synthesize_flow_cytometry`](#synthesize_flow_cytometry) | What does this file support, read before any question is asked? |
| [`target_decoy_qvalues`](#target_decoy_qvalues) | What q-value does each peptide-spectrum match get by target-decoy competition, and how many pass a threshold? |
| [`test_cytometry_spatial_interactions`](#test_cytometry_spatial_interactions) | Which cell types sit next to each other more, or less, often than a random arrangement of the same cells? |
| [`translate_sequence`](#translate_sequence) | What protein does this DNA encode, under the genetic code chosen? |

---

### analyze_flow_cytometry

**Analyze flow cytometry**: _How many events fall in each gated population of this FCS file, and what are their per-channel intensities?_

An FCS 2.0/3.0/3.1 file from the project, end to end: read and linearize every event, compensate with the file's spillover, apply a Gating-ML 2.0 strategy from the project; every population's count, % of parent and % of all events, per-channel mean, median, SD and CV, a two-channel density for a plot, and a flowDensity deGate threshold on any channel, on the chosen display scale.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- The file's $SPILLOVER describes how each dye spills into the other detectors on THIS acquisition.
- A gate's coordinates are in the transform its Gating-ML dimension names.

**Does not:**
- One file per call; batches, FlowJo workspaces (.wsp), spectral unmixing and clustering are not read.
- A strategy written for other channel names refuses by name rather than gating the wrong channel.

**Validated:** against the reference implementation by 5 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file, by name or id; may be left empty when the project holds exactly one. |
| `gating` | string |  | `""` |  | a Gating-ML 2.0 document or a FlowJo 10 workspace (.wsp) in the project, by name or id (from a workspace, the sample that is this file, matched by its $TOT, $BTIM, $ETIM and $DATE); empty for no gating (every statistic is then of all events). |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | `auto`: the file's own $SPILLOVER/$SPILL when it has one, else none; `file`: that, refusing a file without one; `none`: leave the values as acquired; `custom`: the matrix in `spillover`. Values: auto (automatic), file (file's own matrix), none (none), custom (custom matrix). |
| `spectral_matrix` | string |  |  |  | A spectral matrix in this project (CSV: a detector header, then one row per fluorochrome), by file name or id: every fluorochrome is unmixed from the raw detectors (by unmixing_method) and added as a channel of its own name, which plots, gates and statistics can then name. |
| `unmixing_method` | `"ols"` · `"wls"` · `"poisson"` |  | `"ols"` |  | `ols`: ordinary least squares (flowSpecs specUnmix); `wls`: detectors weighted 1 / max(\|mean\|, 125) (AutoSpectral unmix.wls); `poisson`: a per-cell identity-link Poisson fit started from WLS (AutoSpectral unmix.poisson). Values: ols (ordinary least squares), wls (weighted least squares), poisson (Poisson). |
| `spillover` | string |  |  |  | The `custom` compensation, a spillover matrix: an FCS $SPILLOVER value (n, the detectors, then the values row by row) or CSV/TSV with a detector header row. It must name exactly the file’s fluorescence detectors. Gates of the strategy keep the file’s own matrix. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | which published algorithm: FlowKit's solve(Sᵀ, Xᵀ) or flowCore's X · S⁻¹. They agree to ~1e-15 of full scale. Values: flowkit (solve(Sᵀ, Xᵀ) (FlowKit)), flowcore (X · S⁻¹ (flowCore)). Only applies when compensation is auto or file. |
| `scale` | `"logicle"` · `"fasinh"` · `"arcsinh"` · `"hyperlog"` · `"flowcore-logicle"` · `"wsp-biex"` · `"flin"` · `"flowcore-arcsinh"` · `"boxcox"` · `"linlog"` · `"flowcore-biex"` |  | `"logicle"` |  | the display scale of the fluorescence channels (scatter and time stay linear): used for the plot, the threshold and, with `stats_on: scaled`, the statistics. Values: logicle (Logicle (Gating-ML 2.0, Moore & Parks)), fasinh (ArcSinh (Gating-ML 2.0 fasinh)), arcsinh (ArcSinh with a cofactor (asinh(x / c), Cytobank and CyTOF)), hyperlog (Hyperlog (Gating-ML 2.0, Bagwell)), flowcore-logicle (Logicle on a 0–M axis (flowCore)), wsp-biex (Biex (FlowJo 10, channels 0–4096)), flin (Linear (Gating-ML flin)), flowcore-arcsinh (ArcSinh, asinh(a + b·x) + c (flowCore, flowTrans)), boxcox (Box-Cox (flowClust, flowTrans)), linlog (Linlog (flowTrans)), flowcore-biex (Biexponential (flowCore, flowTrans)). |
| `T` | number |  |  | ≥ 1 | top of scale; empty means the file's largest fluorescence $PnR. |
| `W` | number |  | `0.5` | 0–5 | linear width in decades. Only applies when scale is logicle or hyperlog or flowcore-logicle. |
| `M` | number |  | `4.5` | 0.5–10 | decades of the full scale. Only applies when scale is logicle or hyperlog or flowcore-logicle or fasinh. |
| `A` | number |  | `0` | -5–5 | additional negative decades. Only applies when scale is logicle or hyperlog or flowcore-logicle or fasinh. |
| `cofactor` | number |  | `150` | ≥ 0.001 | the c in asinh(x / c): 5 is the CyTOF convention, 150 a common one for fluorescence. Only applies when scale is arcsinh. |
| `biex_width` | number |  | `-10` | ≤ -1 | FlowJo biex width basis (negative; FlowJo's default -10). Only applies when scale is wsp-biex. |
| `biex_negative` | number |  | `0` | ≥ 0 | FlowJo biex extra negative decades. Only applies when scale is wsp-biex. |
| `asinh_a` | number |  | `1` |  | the a in asinh(a + b·x) + c (flowCore arcsinhTransform; flowTrans fits a and b). Only applies when scale is flowcore-arcsinh. |
| `asinh_b` | number |  | `1` |  | the b in asinh(a + b·x) + c; 1/b is a cofactor. Only applies when scale is flowcore-arcsinh. |
| `asinh_c` | number |  | `0` |  | the c in asinh(a + b·x) + c (flowTrans fixes it at 0). Only applies when scale is flowcore-arcsinh. |
| `lambda` | number |  | `1` |  | λ of Box-Cox ((sign(x)·\|x\|^λ − 1)/λ, flowClust box) or of linlog (log above λ, the tangent line below); estimate_flow_cytometry_scale's flowTrans fit gives it. Only applies when scale is boxcox or linlog. |
| `biexp_a` | number |  | `0.5` |  | the a of flowCore biexponentialTransform: y solves a·e^(b(y − w)) − c·e^(−d(y − w)) = x. Only applies when scale is flowcore-biex. |
| `biexp_b` | number |  | `1` |  | the b of flowCore biexponentialTransform. Only applies when scale is flowcore-biex. |
| `biexp_c` | number |  | `0.5` |  | the c of flowCore biexponentialTransform. Only applies when scale is flowcore-biex. |
| `biexp_d` | number |  | `1` |  | the d of flowCore biexponentialTransform. Only applies when scale is flowcore-biex. |
| `biexp_w` | number |  | `0` |  | the w of flowCore biexponentialTransform. Only applies when scale is flowcore-biex. |
| `stats_on` | `"linear"` · `"scaled"` |  | `"linear"` |  | statistics on linear compensated values (MFI) or on the display scale. Values: linear (linear values (MFI)), scaled (display scale). |
| `plot_x` | string |  |  |  | channel (PnN or PnS) on the density plot's x axis; empty for no plot. |
| `plot_y` | string |  |  |  | channel on the plot's y axis. |
| `plot_population` | string |  |  |  | the population plotted; empty for all events. |
| `bins` | number |  | `128` | 8–256 | bins per axis of the density. |
| `threshold_channel` | string |  |  |  | channel to find a density-valley threshold on (flowDensity deGate on the display scale); empty for none. |
| `threshold_population` | string |  |  |  | the population thresholded; empty for all events. |
| `derived` | string |  | `""` |  | derived parameters, `name = expression` separated by `;` (FlowJo's vocabulary: channels by name or [name], + − * / % ^, abs ceil floor neg round max min pow exp ln log sqrt and the trig functions); each becomes a channel of the run. |
| `clusters` | string |  | `""` |  | populations made of FlowSOM nodes, as a JSON array of {name, parent, seed, channels, xdim, ydim, rlen, nClus, scale, outlierMAD, nodes}: the map is rebuilt from those settings and the population holds the parent's events in those nodes (1-based). |
| `metrics` | string |  | `""` |  | population metrics separated by `;`: `name = A / B` for the ratio of two populations' event counts (CD4/CD8), `name = A % B` for A as a percentage of B; A and B are population names, `All events` included. |
| `embedding_method` | `""` · `"tsne"` · `"fitsne"` · `"umap"` · `"optsne"` · `"embedsom"` |  | `""` |  | embed one population in two dimensions and join the coordinates to the run as two channels (tSNE-1/tSNE-2, optSNE-1/optSNE-2, UMAP-1/UMAP-2 or EmbedSOM-1/EmbedSOM-2) that plots, gates and statistics can name; empty for none. Values:  (none), tsne (t-SNE (Barnes–Hut)), fitsne (t-SNE (FFT interpolation, FIt-SNE)), umap (UMAP), optsne (opt-SNE), embedsom (EmbedSOM). |
| `embedding_population` | string |  |  |  | the population embedded; empty for all events. Only applies when embedding_method is tsne or fitsne or umap or optsne or embedsom. |
| `embedding_channels` | string |  |  |  | channels the embedding reads, separated by `;` (fluorescence on the display scale, scatter linear); empty for the file's fluorescence channels. Only applies when embedding_method is tsne or fitsne or umap or optsne or embedsom. |
| `embedding_events` | number |  | `2000` | ≥ 0 | at most this many of the population's events, drawn without replacement by the seed (numpy choice); 0 for every event. Only applies when embedding_method is tsne or fitsne or umap or optsne or embedsom. |
| `embedding_seed` | number |  | `42` |  | the numpy seed of the sample, the initialisation's jitter and the layout. Only applies when embedding_method is tsne or fitsne or umap or optsne or embedsom. |
| `perplexity` | number |  | `30` | ≥ 1 | t-SNE perplexity: the effective neighbours each event's affinities spread over (⌊3 × perplexity⌋ exact neighbours). Only applies when embedding_method is tsne or fitsne or optsne. |
| `early_exaggeration_iter` | number |  | `250` | ≥ 0 | t-SNE iterations with the affinities multiplied by 12. Only applies when embedding_method is tsne or fitsne. |
| `n_iter` | number |  | `500` | ≥ 1 | t-SNE iterations after early exaggeration. Only applies when embedding_method is tsne or fitsne. |
| `theta` | number |  | `0.5` | 0–1 | Barnes–Hut angle: larger is faster and coarser. Only applies when embedding_method is tsne or optsne. |
| `n_neighbors` | number |  | `15` | ≥ 2 | UMAP n_neighbors: larger keeps more global structure. Only applies when embedding_method is umap. |
| `min_dist` | number |  | `0.1` | ≥ 0 | UMAP min_dist: how tightly neighbours may pack (a and b are fitted to it and the spread). Only applies when embedding_method is umap. |
| `spread` | number |  | `1` | ≥ 0.01 | UMAP spread. Only applies when embedding_method is umap. |
| `n_epochs` | number |  | `0` | ≥ 0 | UMAP epochs; 0 for umap-learn's rule (500 up to 10,000 events, 200 above). Only applies when embedding_method is umap. |
| `optsne_max_iter` | number |  | `1000` | ≥ 1 | opt-SNE: the most iterations it may run (it usually stops well before). Only applies when embedding_method is optsne. |
| `optsne_end` | number |  | `5000` | ≥ 1 | opt-SNE stop: end once the KL divergence changes by less than KL / this per iteration (auto_iter_end). Only applies when embedding_method is optsne. |
| `som_xdim` | number |  | `10` | ≥ 1 | EmbedSOM: width of the self-organising map's grid (FlowSOM SOM() xdim). Only applies when embedding_method is embedsom. |
| `som_ydim` | number |  | `10` | ≥ 1 | EmbedSOM: height of the map's grid (ydim); the grid needs at least xdim × ydim events. Only applies when embedding_method is embedsom. |
| `som_rlen` | number |  | `10` | ≥ 1 | EmbedSOM: the map's training passes over the events (rlen). Only applies when embedding_method is embedsom. |
| `embedsom_smooth` | number |  | `0` | ≥ -3 | EmbedSOM smooth: positive smoother, negative rougher (at least -3). Only applies when embedding_method is embedsom. |
| `embedsom_k` | number |  | `0` | ≥ 0 | EmbedSOM: neighbouring codes per event; 0 for EmbedSOM's rule 1 + ⌊√codes⌋. Only applies when embedding_method is embedsom. |
| `embedsom_adjust` | number |  | `1` | ≥ 0 | EmbedSOM adjust: how much non-local pull between codes far apart on the grid is removed. Only applies when embedding_method is embedsom. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `populations` | any |  | every population: id, parent, event count, percent of parent and of all events |
| `stats` | any |  | per population and channel: count, mean, median, SD (n − 1), CV, min, max |
| `density` | object or null |  | the two-channel density, events per bin, rows from the top of the plot |
| `density.rows` | string[] |  |  |
| `density.cols` | string[] |  |  |
| `density.values` | ((number or null)[])[] |  |  |
| `density.label` | string |  |  |
| `density.title` | string |  |  |
| `threshold` | any |  | every density-valley cut on the display scale and as scale values, and how many events lie at or above |
| `metrics` | any |  | every asked-for metric: its two populations and their events, the value, and the arithmetic in words |
| `compensation` | any |  | the spillover matrix used, its detectors and the algorithm, or null when the file has none |
| `file` | any |  | version, event count, every channel with its role, range, gain and decades |
| `embedding` | any |  | the embedding, when asked for: method, population, channels, the two axis channels, events embedded of the population, seed, every parameter it ran with, KL divergence (t-SNE) and time |
| `events` | number |  | events in the file |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "analyze_flow_cytometry",
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

### analyze_flow_cytometry_ploidy

**Analyze flow cytometry ploidy**: _What are the cell-cycle phases and DNA content in this DNA-stained sample?_

flowPloidy's DNA-content (cell cycle, genome size) fit on one channel of a project FCS file, optionally one population: G1/G2 Gaussians per sample, broadened-rectangle S phase, debris and aggregates by bounded nlsLM; nuclei counts, G1 CVs, G2/G1 linearity, reduced chi-square; with a standard, the ratio and pg; without G2, the endoreduplication index. Or flowPloidy's refusal.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The channel is linear DNA content (area); nuclei of one sample sit in a G1 peak, a G2 peak near twice it, and S phase between.
- With a standard, the standard and the sample were stained and run together in one tube.

**Does not:**
- Up to six samples per histogram; peaks below the debris limit are not used to start the fit.
- The reduced chi-square is flowPloidy's goodness-of-fit guide (0.7–4 acceptable), not a test.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `channel` | string |  | `""` |  | the DNA-content channel (PnN or PnS). |
| `population` | string |  | `""` |  | a population of the strategy to analyze (flowPloidy gate); empty for every event. |
| `histogram_bins` | number |  | `256` | ≥ 16 | histogram bins. |
| `samples_in_tube` | number |  | `2` | 1–6 | how many samples (sets of G1/G2/S peaks) the model may hold. |
| `debris` | `"SC"` · `"MC"` |  | `"SC"` |  | the debris model. Values: SC (single cut), MC (multiple cut). |
| `linearity` | `"variable"` · `"fixed"` |  | `"variable"` |  | the G2/G1 ratio: fitted between 1.5 and 2.5, or held at 2. Values: variable (fitted), fixed (fixed at 2). |
| `g2` | boolean |  | `true` |  | model G2 peaks; off for endopolyploid tissue (then the endoreduplication index is reported). |
| `debris_limit` | number |  | `40` | ≥ 0 | peaks below this bin are not used as starting peaks. |
| `trim_raw` | number |  | `0` | ≥ 0 | drop channel values at or above this (0 keeps every value). |
| `standard` | `""` · `"a"` · `"b"` |  | `""` |  | which sample's G1 is the internal standard (a: lower G1, b: higher); empty for none. |
| `standard_size` | number |  | `0` | ≥ 0 | the standard's DNA content in pg (0 for none). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `fit` | any |  | the fitted parameters by name, stop code, iterations, nuclei counts per component, G1 CVs and the reduced chi-square; null when refused |
| `summary` | any |  | ratio to the standard, DNA content (pg) and endoreduplication index, each null when it does not apply |
| `histogram` | any |  | counts per bin, events outside the population, the fitted bins, and the starting peaks |
| `refused` | string or null |  | flowPloidy's refusal, or null |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "analyze_flow_cytometry_ploidy",
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

### analyze_rt_pcr

**Analyze rt PCR**: _Does this primer pair span an exon junction, and would genomic DNA amplify too?_

What a primer pair does on a SPLICED transcript versus genomic DNA: the products on each, whether a primer straddles an exon junction (so the assay cannot amplify gDNA at all), whether genomic DNA would still give a band, and by how many bases the two products differ on a gel. Takes the exon structure from a joined mRNA/CDS annotation on the open record, splices it, and runs the same pydna annealing on both templates.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The transcript is the exons of the named annotation, in the order the location writes them.
- Annealing is pydna's, run identically on both templates.

**Does not:**
- Answers for the ONE transcript named: another isoform of the same gene can behave differently.
- A junction-spanning primer is blind to gDNA by construction, not by efficiency — this does not model partial priming.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `forward` | string | **yes** |  |  | forward primer 5'→ 3'. |
| `reverse` | string | **yes** |  |  | reverse primer 5'→ 3'. |
| `transcript` | string |  |  |  | the joined mRNA or CDS annotation to splice, by NAME. Left empty the record's only joined annotation is used, and several are refused with their names. |
| `limit` | number |  | `13` | 6–40 | min 3' footprint match length (pydna `limit`). In bp. Advanced. |
| `mismatches` | number |  | `0` | 0–5 | substitutions a primer may carry and still prime (QUEEN `{s<=N}`). 0 is pydna's exact search. Advanced. |
| `end_length` | number |  | `3` | 1–10 | 3'-most bases that must pair exactly whatever the mismatch budget. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `junctionSpanning` | boolean |  | a primer's own footprint straddles an exon junction, so this pair cannot prime on genomic DNA at all — the property an RT-PCR assay is designed for. Branch a workflow on this |
| `gdnaWouldAmplify` | boolean |  | the same pair also makes a product on genomic DNA, so a contaminated RNA prep gives a band |
| `products` | any |  | one row per product: its transcript interval, its genomic interval, the genomic PIECES a spliced product maps to (several when it spans a junction), and whether it forms on the transcript only, genomic only, or both |
| `intronBp` | number | bp | intron removed by splicing — the size difference between a genomic and a transcript product on the gel |
| `transcriptLengthBp` | number | bp | length of the spliced transcript |
| `placements` | any |  | per primer: where it binds on the transcript, and which junction offsets its footprint straddles |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "analyze_rt_pcr",
  "arguments": {
    "forward": "<string>",
    "reverse": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### auto_gate_flow_cytometry

**Auto Gate flow cytometry**: _Where would openCyto place its automated gates on these two channels, and how many events fall on each side?_

openCyto 2.24 automated gates on two channels: a cut per axis (gate_mindensity, gate_mindensity2, gate_quantile, gate_tail from cytoUtils, or gate_flowclust_1d on a flowClust t mixture), quadrants (gate_quad_sequential or the t-mixture gate_quad_tmix), the flowClust ellipse or transitional gate on the pair (gate_flowclust_2d), and the singlet gate on area × height (gate_singlet). On the plotted values: display scale, compensated as chosen.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- The populations to separate form distinct peaks in each channel’s density.
- Singlets lie on a straight line of height against area.

**Does not:**
- One file and one pair per call; gates are not written back to a Gating-ML strategy.
- flowClust is fitted without Box-Cox estimation (trans = 0), as openCyto's gates call it, unless fc_trans asks for one λ on the cut; fc_select_k is ignored with fc_prior (the prior fixes K); with fc_prior the Bayesian prior is elicited by openCyto's prior_flowclust from every FCS file in the project, prepared as this one is.

**Validated:** against the reference implementation by 5 golden suites.

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
| `plot_x` | string |  |  |  | channel (PnN or PnS) on the density plot's x axis; empty for no plot. |
| `plot_y` | string |  |  |  | channel on the plot's y axis. |
| `plot_population` | string |  |  |  | the population plotted; empty for all events. |
| `cut` | `"none"` · `"mindensity"` · `"mindensity2"` · `"quantile"` · `"tail"` · `"otsu"` · `"flowclust"` |  | `"mindensity"` |  | the one-dimensional gate placed on each axis. Values: none (none), mindensity (minimum density), mindensity2 (spline features), quantile (quantile), tail (tail of a peak), otsu (Otsu's threshold), flowclust (t-mixture clusters). |
| `adjust` | number |  | `2` | ≥ 0.1 | KDE bandwidth multiplier (openCyto's adjust). |
| `positive` | boolean |  | `true` |  | mindensity and tail: keep the side above the cut. |
| `tail_side` | `"right"` · `"left"` |  | `"right"` |  | tail: the shoulder of the reference peak to cut. |
| `tail_method` | `"first_deriv"` · `"second_deriv"` |  | `"first_deriv"` |  | tail: first_deriv cuts where \|f'\| falls below the tolerance, second_deriv at a peak of f''. |
| `tail_tol` | number |  |  | ≥ 0 | tail, first derivative: the \|f'\| tolerance; empty for 1% of its maximum. |
| `tail_adjust` | number |  | `1` | ≥ 0.1 | tail: plug-in bandwidth multiplier. |
| `tail_peaks` | number |  | `1` | ≥ 1 | tail: peaks to find. |
| `tail_ref_peak` | number |  | `1` | ≥ 1 | tail: the reference peak, 1-based from the left. |
| `fc_k` | number |  | `2` | ≥ 2 | flowclust cut: t-mixture components fitted to each axis. |
| `fc_rule` | `"boundary"` · `"min_density"` · `"quantile"` · `"posterior_mean"` · `"prior_density"` |  | `"boundary"` |  | flowclust cut: boundary between two components, lowest mixture density between their means, a mixture quantile, the lower mean, or (with fc_prior) where the two prior densities cross. |
| `fc_neg_cluster` | number |  | `1` | ≥ 1 | flowclust cut: the component (by mean, 1-based) the cut sits above. |
| `fc_quantile` | number |  | `0.99` | 0–1 | flowclust quantile rule: the mixture quantile. |
| `fc_lower` | number |  | `0` |  | flowclust quantile rule: lower end of the search interval. |
| `fc_upper` | number |  | `10` |  | flowclust quantile rule: upper end of the search interval. |
| `fc_prior` | boolean |  | `false` |  | fit the flowclust cut and the flowClust ellipse with flowClust's Bayesian prior, elicited by openCyto's prior_flowclust from every FCS file in the project. |
| `fc_nu` | number |  | `4` | ≥ 1 | degrees of freedom of every flowClust t component. |
| `fc_gaussian` | boolean |  | `false` |  | fit the flowclust cut and the flowClust ellipse with Gaussian components (flowClust nu = Inf). |
| `fc_nu_est` | `0` · `1` · `2` · `-1` |  | `0` |  | flowClust nu.est for the cut and the ellipse: 0 keeps fc_nu, 1 one ν solved from its score, 2 one ν per component, -1 one ν maximising the likelihood (fc_nu is the start). |
| `fc_trans` | `0` · `1` |  | `0` |  | flowclust cut: flowClust trans, 0 no Box-Cox or 1 one λ estimated with the mixture. |
| `fc_select_k` | `"fixed"` · `"BIC"` · `"ICL"` |  | `"fixed"` |  | flowclust cut: fit fc_k components, or fit K = 1 to fc_k and keep the best by BIC or ICL. |
| `fc_random_start` | number |  | `0` | ≥ 0 | flowClust randomStart for the cut and the ellipse: 0 starts from kmeans; n random partitions, the long EM run from the best short EM when n >= 2. |
| `otsu_bins` | number |  | `256` | ≥ 2 | otsu: histogram bins over the axis's range; the cut is the centre of one. |
| `probs` | number |  | `0.999` | 0–1 | quantile: the quantile the cut sits at. |
| `quad` | boolean |  | `true` |  | also fit a quadrant gate. |
| `quad_method` | `"sequential"` · `"tmix"` |  | `"sequential"` |  | quadrants: sequential 1-D cuts or the t-mixture gate_quad_tmix. |
| `tmix_k` | number |  | `2` | ≥ 2 | gate_quad_tmix: t-mixture components. |
| `tmix_quantile1` | number |  | `0.8` | 0.01–0.999 | gate_quad_tmix: ellipse quantile of the top-left component. |
| `tmix_quantile3` | number |  | `0.8` | 0.01–0.999 | gate_quad_tmix: ellipse quantile of the bottom-right component. |
| `ellipse` | boolean |  | `false` |  | also fit the flowClust gate on the pair (gate_flowclust_2d). |
| `ellipse_k` | number |  | `2` | ≥ 1 | gate_flowclust_2d: t-mixture components. |
| `ellipse_quantile` | number |  | `0.9` | 0.01–0.999 | gate_flowclust_2d: quantile of the ellipse (or of the transitional χ² length). |
| `transitional` | boolean |  | `false` |  | gate_flowclust_2d: openCyto's transitional polygon instead of the ellipse. |
| `translation` | number |  | `0.25` |  | transitional gate: shift along the eigenvector, as a fraction of its half-length. |
| `singlet` | boolean |  | `true` |  | also fit the singlet gate. |
| `singlet_area` | string |  |  |  | area channel of the singlet gate; empty for FSC-A. |
| `singlet_height` | string |  |  |  | height channel of the singlet gate; empty for FSC-H. |
| `prediction_level` | number |  | `0.99` | 0.5–0.9999 | the prediction band level of the singlet polygon. |
| `wider_gate` | boolean |  | `false` |  | weight the band's ends by the extreme events' Huber weights. |
| `subsample_pct` | number |  |  | 0.01–1 | fit the singlet gate on this fraction of events; empty for every event. |
| `seed` | number |  | `42` |  | R set.seed for the singlet subsample and the kmeans start of a 2-D flowClust fit. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `cuts` | any |  | per axis: the cut, events at or above and at or below it, the rule that chose it, the KDE peaks and valleys |
| `quadrants` | any |  | sequential: the three cuts and which axis was cut first; tmix: the fit, the two ellipses and the corners the quadrants meet at; both: events per quadrant |
| `flowclust_gate` | any |  | gate_flowclust_2d: the fit (weights, means, BIC, outliers), the gated component, its ellipse or transitional polygon, and events inside |
| `singlet` | any |  | the singlet polygon in (area, height), its coefficients, residual scale, seed and events inside |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "auto_gate_flow_cytometry",
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

### batch_flow_cytometry

**Batch flow cytometry**: _How does each population change across samples, and between groups of samples?_

One strategy, compensation and scale over many project FCS files: each population's count and % per sample (samples it cannot gate listed with the reason); with a sample sheet column, populations compared between groups (Welch t, Kruskal-Wallis, Welch one-way ANOVA) or by two columns (two-way ANOVA, R aov).

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Each sample is one observation; repeated samples of one subject are not independent, which the tests assume.

**Does not:**
- Paired and mixed-effects designs are not modeled.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `samples` | string |  | `""` |  | the FCS files to run, by name or id, comma-separated; empty for every FCS file in the project. |
| `sample_sheet` | string |  | `""` |  | a CSV in the project whose first column, headed sample, names each FCS file; empty for no groups. |
| `group_by` | string |  | `""` |  | the sample sheet's column whose values are the groups to compare. |
| `measure` | `"percentOfParent"` · `"percentOfTotal"` |  | `"percentOfParent"` |  | which percentage is compared. Values: percentOfParent (% of parent), percentOfTotal (% of total). |
| `and_by` | string |  | `""` |  | a second sample-sheet column: each population's percentage by both columns at once, R summary(aov()) with sequential sums of squares (group_by first); empty for none. |
| `interaction` | boolean |  | `false` |  | with and_by, also fit the two columns' interaction (y ~ A * B). |
| `concordance` | string |  | `""` |  | a one-dimensional range gate of the strategy to compare, sample by sample, with openCyto's automated cut (gate_mindensity) on the same parent and channel, scored by Lin's concordance correlation; empty for none. |
| `cluster_channels` | string |  | `""` |  | channels to cut each sample into its own k-means clusters on (asinh), match each sample's clusters to the next's (flowMatch mixed edge cover) and place every pair of samples by earth mover's distance (emdist, at most 4 channels); comma-separated, empty for no cluster matching. |
| `cluster_k` | number |  | `5` |  | clusters per sample (R kmeans centers). |
| `cluster_cofactor` | number |  | `5` |  | each clustered channel is asinh(x / cofactor). |
| `cluster_seed` | number |  | `1` |  | R set.seed before each sample's kmeans. |
| `cluster_max_iter` | number |  | `10` |  | R kmeans iter.max. |
| `cluster_distance` | `"Mahalanobis"` · `"KL"` · `"Euclidean"` |  | `"Mahalanobis"` |  | the distance between two clusters the cover minimizes (flowMatch dist.type). |
| `cluster_penalty` | number |  | `999999` |  | the cost of leaving a cluster unmatched (flowMatch unmatch.penalty). |
| `frequency_channels` | string |  | `""` |  | channels to cluster every sample's events together on (diffcyt's pipeline: asinh, FlowSOM), then compare the samples by their cluster frequencies: Pearson cor(), cosine (lsa) and earth mover's distance (emdist, at most 4 channels); comma-separated, empty for none. |
| `frequency_cofactor` | number |  | `5` |  | each clustered channel is asinh(x / cofactor). |
| `frequency_xdim` | number |  | `10` |  | FlowSOM map columns. |
| `frequency_ydim` | number |  | `10` |  | FlowSOM map rows. |
| `frequency_meta_clustering` | boolean |  | `false` |  | group the map's nodes into metaclusters (ConsensusClusterPlus). |
| `frequency_meta_k` | number |  | `40` |  | metaclusters, with frequency_meta_clustering. |
| `frequency_seed` | number |  | `123` |  | R set.seed before the map is trained. |
| `frequency_ground` | `"euclidean"` · `"manhattan"` |  | `"euclidean"` |  | the earth mover's ground distance between cluster medians (emdist dist). Values: euclidean (Euclidean), manhattan (Manhattan). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `table` | any |  | populations × samples: counts, % of parent, % of total, and the samples refused |
| `comparisons` | any |  | per population: the groups, their means and the tests |
| `two_way` | any |  | per population: the two-way ANOVA table (df, sum of squares, mean square, F, p per term and the residuals), or why none |
| `concordance` | any |  | per sample the manual and automated % of parent and the cut, and Lin's concordance correlation with its 95% interval, scale and location shifts and bias-correction factor |
| `cluster_match` | any |  | per sample its clusters (size, asinh centre), each first-sample cluster's track through the samples, the covers between consecutive samples with their cost, and the samples × samples earth mover's distance (or why none) |
| `cluster_frequencies` | any |  | the shared clusters (count and % per sample, asinh medians) and the samples × samples Pearson correlation, cosine similarity and earth mover's distance (or why none) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "batch_flow_cytometry",
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

### blast_project_sequences

**BLAST project sequences**: _Which of this project's own records carry this span, with what E-values?_

Search a sequence against THIS PROJECT'S OWN records with blastn or blastp, on this machine: the local database is built from every project record of the program's alphabet, and every E-value is computed from that database's own size. Use it to ask which of my constructs, reads or proteins carry this span. Nothing leaves the machine; for public databases use blast_search.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- BLAST+ blastn/blastp scoring, with E-values from this project's database size.

**Does not:**
- Searches only this project's records.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `program` | `"blastn"` · `"blastp"` |  | `"blastn"` |  | blastn searches the nucleotide records, blastp the protein records. Values: blastn (blastn · nucleotide query), blastp (blastp · protein query). |
| `sequence` | string |  |  |  | the query. Wire a record or a sequence output, or paste raw/FASTA. Left empty, the region below is taken from the open record. |
| `region` | `"whole"` · `"selection"` · `"feature"` |  | `"whole"` |  | which part of the open record to search, when no sequence is wired in. Values: whole (the whole record), selection (the current selection), feature (a named feature). |
| `feature` | string |  |  |  | the feature's name, matched case-insensitively on the open record. Only applies when region is feature. |
| `maxExpect` | number |  | `10` | ≥ 0 | E-value cutoff (BLAST+'s -evalue); hits above it are not reported. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | every hit, with its HSPs, accession, organism and the links the service sent |
| `hitCount` | number |  | how many subjects matched |
| `topHit` | any |  | the best hit by E-value: what a "what is this?" step reads |
| `topExpect` | number or null |  | the best hit's E-value; wire into a $when to branch on significance |
| `topIdentity` | number | % | percent identity of the best hit's best HSP |
| `topCoverage` | number |  | what fraction of the query the best hit covers, 0–1 |
| `sequences` | string |  | the hit subjects as FASTA, ready to wire straight into an alignment or a tree |
| `tabular` | string |  | the hits as BLAST's own outfmt 6 table, for download or a downstream parser |
| `provenance` | any |  | the binary, the command line EBI ran, the databases as built, and the search space the E-values are relative to |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "blast_project_sequences",
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

### blast_search

**BLAST search**: _Which public sequences resemble this one, with what E-values?_

Search a sequence against NCBI BLAST+ at EMBL-EBI (blastn, blastp, blastx, tblastn or tblastx) over ENA, UniProtKB, PDB and the vector-screening sets. This is the similarity search a methods section cites: it turns an unnamed span into named homologues with E-values, and hands the hits, the tabular report and the job id downstream. The sequence LEAVES THE MACHINE.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network; the sequence leaves the machine.
- E-values are relative to the database searched.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `program` | `"blastn"` · `"blastp"` · `"blastx"` · `"tblastn"` · `"tblastx"` |  | `"blastn"` |  | which BLAST program. The QUERY alphabet is derived from it and never asked for: blastx takes DNA and searches protein, tblastn the reverse. Values: blastn (blastn · dna query), blastp (blastp · protein query), blastx (blastx · dna query), tblastn (tblastn · protein query), tblastx (tblastx · dna query). |
| `sequence` | string |  |  |  | the query. Wire a record or a sequence output, or paste raw/FASTA. Left empty, the region below is taken from the open record. |
| `region` | `"whole"` · `"selection"` · `"feature"` |  | `"whole"` |  | which part of the open record to search, when no sequence is wired in. Values: whole (the whole record), selection (the current selection), feature (a named feature). |
| `feature` | string |  |  |  | the feature's name, matched case-insensitively on the open record. Only applies when region is feature. |
| `databases` | string[] |  |  |  | database ids to search, as the service names them (em_rel, uniprotkb, pdb, emvec…). Several are searched together. Left empty, the service's OWN default for this program's context is used and reported back. |
| `parameters` | string |  |  |  | every other advertised parameter, one `id=value` per line, using the service's own ids (exp, matrix, filter, gapopen, gapext, wordsize, alignments, scores, taxids…). Left empty each keeps the service's default for this context. An id the service does not advertise is refused by name rather than dropped. |
| `email` | string |  |  |  | EBI requires a contact address on every submission (their abuse contact, not a login). Left empty, the one saved in any EMBL-EBI panel is used. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | every hit, with its HSPs, accession, organism and the links the service sent |
| `hitCount` | number |  | how many subjects matched |
| `topHit` | any |  | the best hit by E-value: what a "what is this?" step reads |
| `topExpect` | number or null |  | the best hit's E-value; wire into a $when to branch on significance |
| `topIdentity` | number | % | percent identity of the best hit's best HSP |
| `topCoverage` | number |  | what fraction of the query the best hit covers, 0–1 |
| `sequences` | string |  | the hit subjects as FASTA, ready to wire straight into an alignment or a tree |
| `tabular` | string |  | the hits as BLAST's own outfmt 6 table, for download or a downstream parser |
| `jobId` | string |  | the dispatcher job id: what a methods section cites and what re-fetches this exact result |
| `provenance` | any |  | the binary, the command line EBI ran, the databases as built, and the search space the E-values are relative to |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "blast_search",
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

### calibrate_flow_cytometry_beads

**Calibrate flow cytometry beads**: _Which bead population is each event, and how does each channel map to MEF?_

flowBeads gateBeads on a calibration-bead FCS tube in the project and its lot's MEF table: every bead population (flowCore's default logicle, quantile-seeded R k-means per channel, the median label per event), each population's count, mean, SD and CV per channel, and for every certified channel the least-squares line trans(MEF) = alpha + beta * trans(MFI) with its residual standard error.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The tube holds K bead populations, K the rows of the MEF table, the blank first.

**Does not:**
- flowBeads' scatter gate (norm2Filter) is a separate step and is not applied, as gateBeads does not.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `tube` | string | **yes** |  |  | the bead FCS file in the project, by name or id. |
| `mef` | string | **yes** |  |  | the lot's MEF table in the project (';'-separated, the blank row first), by name or id. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `mef` | any |  | per certified channel: alpha, beta and the residual standard error |
| `stats` | any |  | per channel, per bead population: count, mean, SD, CV |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "calibrate_flow_cytometry_beads",
  "arguments": {
    "tube": "<string>",
    "mef": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### check_assay_decay

**Check assay decay**: _How often do a published assay's oligos mismatch the genomes circulating now, and where in each oligo do the mismatches sit?_

Check a published PCR or sequencing assay against the sequences that are circulating now: for each oligo, where its best binding site is in each genome, how many positions mismatch, and whether a mismatch sits in the 3′ end a polymerase has to extend through. It answers the question an assay's age raises — the design was made against the genomes available on the day, and the target has drifted under it since — as a RATE per oligo with an exact binomial interval, plus the mismatch count at each position of the oligo, which is the shape a manufacturer's own in-silico inclusivity table takes. IUPAC codes in an oligo are read as the breadth its designers meant, so a position a code covers is never a mismatch; a site overlapping ambiguous bases in a submitted assembly is missing data and leaves that genome out of that oligo's denominator rather than counting as a match or a mismatch. A probe gets no 3′-end rate, because it is not extended. Graded against EMBOSS fuzznuc on every oligo of twelve published SARS-CoV-2 assays over 400 genomes.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Each oligo's best binding site in a genome is where it binds.
- IUPAC codes in an oligo mean the breadth its designers intended.

**Does not:**
- A mismatch count is not an amplification failure: its effect depends on chemistry, position and temperature.
- Genomes with ambiguous bases under a site leave that oligo's denominator rather than counting.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `assay` | string |  | `"assay"` |  | what the assay is called, for the result to name. |
| `primers` | string[] |  |  |  | the assay's primers, 5′→3′, IUPAC allowed. Written `name=SEQUENCE` to carry the published name. |
| `probes` | string[] |  |  |  | the assay's probes, 5′→3′. Scored the same way but with no 3′-end rule: a probe is not extended. |
| `sequences` | string[] | **yes** |  |  | the genomes to check against: wire upstream records here, or list library document names. |
| `include_subject` | boolean |  | `true` |  | also check the node's subject (the open or wired record). |
| `three_prime_window` | number |  | `5` | 1–10 | how many bases from a primer's 3′ end count as its 3′ end. 5 is the window Primer-BLAST's own specificity rule uses. In bp. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `oligos` | any |  | per oligo: genomes scored, genomes with a mismatch, the rate and its exact 95% interval, the 3′-end count, and the mismatch count at each position |
| `worst` | any |  | the oligo with the highest mismatch rate, which is the one that decides the assay |
| `worstRate` | number |  | that oligo's mismatch rate, for a threshold downstream |
| `threePrime` | number |  | how many (primer, genome) pairs carry a mismatch in the 3′-end window |
| `sites` | any |  | every (oligo, genome) site: strand, start, the mismatching positions and whether the genome could be scored |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_assay_decay",
  "arguments": {
    "sequences": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### check_flow_cytometry_quality

**Check flow cytometry quality**: _Which stretches of this acquisition were unstable, and which events should be removed?_

Acquisition quality over time by flowAI (flow rate, signal, dynamic range), PeacoQC (peak trajectories, isolation tree, MAD) or flowCut (deviant and low-density segments): events kept, removal per cause per time bin, and the tool’s own table, in raw $TIMESTEP ticks.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Events are stored in acquisition order with a time channel.

**Does not:**
- One file per call; flowAI’s outlier_binsFS and interactive modes are not implemented.

**Validated:** against the reference implementation by 3 golden suites.

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
| `tool` | `"flowai"` · `"peacoqc"` · `"flowcut"` |  | `"flowai"` |  | the method. Values: flowai (flowAI), peacoqc (PeacoQC), flowcut (flowCut). |
| `flowai_remove_from` | `"all"` · `"FR_FS"` · `"FR_FM"` · `"FS_FM"` · `"FR"` · `"FS"` · `"FM"` |  | `"all"` |  | flowAI: which checks remove events. Only applies when tool is flowai. |
| `flowai_decomp` | `"cffilter"` · `"loess"` |  | `"cffilter"` |  | flowAI decompFR: the flow rate's trend by the Christiano-Fitzgerald filter or loess. Values: cffilter (CF filter), loess (loess). Only applies when tool is flowai. |
| `flowai_mode_dev` | number |  | `0` | ≥ 0 | flowAI ModeDevFR: also flag rate bins whose trend lies this many SDs from its mode; 0 for none. Only applies when tool is flowai. |
| `flowai_outlier_bins` | boolean |  | `false` |  | flowAI outlier_binsFS: remove the signal check's outlier bins too. Only applies when tool is flowai. |
| `peaco_mad` | number |  | `6` | ≥ 1 | PeacoQC MAD. Only applies when tool is peacoqc. |
| `peaco_it_limit` | number |  | `0.6` | 0.1–1 | PeacoQC isolation tree limit. Only applies when tool is peacoqc. |
| `peaco_consecutive` | number |  | `5` | ≥ 1 | PeacoQC consecutive bins. Only applies when tool is peacoqc. |
| `flowcut_segment` | number |  | `500` | ≥ 50 | flowCut segment (events). Only applies when tool is flowcut. |
| `flowcut_max_perc_cut` | number |  | `0.3` | 0–1 | flowCut MaxPercCut. Only applies when tool is flowcut. |
| `flowcut_max_valley_hgt` | number |  | `0.1` | 0–1 | flowCut MaxValleyHgt. Only applies when tool is flowcut. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `kept` | number |  | events kept |
| `table` | any |  | the method's own result table |
| `causes` | any |  | per cause: events flagged, whether it removes, and flagged events per time bin |
| `channels` | any |  | the per-channel table (changepoints, MAD contribution, margins) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_flow_cytometry_quality",
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

### check_primer_specificity

**Check primer specificity**: _Do these primer pairs make products off their template, and which pair ranks best by it?_

Check primer pairs for products off their template, the way NCBI Primer-BLAST does, and rank them by it: each distinct primer is searched against a sequence database at EMBL-EBI with short-query BLAST, hits are paired into products by Primer-BLAST's own mismatch rule, and the template is searched too so the record identical to it is recognized as the intended target. Pairs with no product elsewhere rank first, in the order given, then pairs not checked, then pairs with a named unintended product. Primer sequences and the template LEAVE THE MACHINE; the database is a collection, not an assembled genome, and cannot be filtered by organism.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Assumes:**
- Primer-BLAST's mismatch rule for pairing hits into products.
- The EMBL-EBI database searched is a collection, not an assembled genome.

**Does not:**
- Needs the network; cannot be filtered by organism.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `forward` | string |  |  |  | one pair's forward primer, 5'→3' (wire design_primers' `forward`). |
| `reverse` | string |  |  |  | that pair's reverse primer, 5'→3' (wire design_primers' `reverse`). |
| `pairs` | string |  |  |  | several pairs to rank, one per line as `forward reverse` (whitespace or a comma between), in their design order. Taken instead of forward/reverse when given. |
| `template` | string |  |  |  | the sequence the pairs were designed on. Searched too: the database record identical to it is where the intended product lives. Left empty, the open record is used; with neither, every product counts as unintended and the result says so. |
| `database` | string |  |  |  | the nucleotide database id, as the service names it (em_all, em_rel_hum…). Left empty, the service's OWN nucleotide default is used and reported back. |
| `top_n` | number |  | `5` | 1–14 | how many of the pairs, from the top, to search. The rest rank as unchecked. At most 14, so the batch stays inside EMBL-EBI's 30 searches. |
| `email` | string |  |  |  | EBI requires a contact address on every submission (their abuse contact, not a login). Left empty, the one saved in any EMBL-EBI panel is used. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `ranked` | any |  | every pair in ranked order: its design rank, standing (specific, unchecked, non-specific), intended products and unintended products with subject, span, length and mismatches |
| `forward` | string |  | the top-ranked pair's forward primer (wire into pcr_amplify) |
| `reverse` | string |  | the top-ranked pair's reverse primer |
| `specificCount` | number |  | pairs with no product off the template; wire into a $when to branch on "any specific pair" |
| `identical` | any |  | database records identical to the template, whose products are the intended ones |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_primer_specificity",
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

### check_rows

**Check rows**: _Does every row of this table satisfy the rule, and which rows broke it?_

A QC gate over a TABLE: assert something about every row at once (every band inside a size window, no guide above an off-target score, at least three assays under a penalty). Fails the pipeline (so everything downstream skips) and names the rows that broke the rule.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The rule given is the real acceptance criterion for every row.

**Does not:**
- Asserts the same thing of every row; a cross-row comparison needs summarize_rows first.

**No scientific claim:** Applies a rule to each row and stops the run; the science is in whatever produced the table.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `items` | string[] | **yes** |  |  | the rows to check. Wire a json/list output (bands, guides, assays, amplicons). |
| `field` | string |  |  |  | which field of each row to test (e.g. `size`, `score`). Leave empty when the rows are plain numbers. |
| `require` | `"all"` · `"any"` · `"none"` · `"at_least"` · `"at_most"` · `"exactly"` |  | `"all"` |  | what must hold across the table. Values: all (every row), any (at least one row), none (no row), at_least (at least N rows), at_most (at most N rows), exactly (exactly N rows). |
| `count` | number |  |  | ≥ 0 | N, for the counted requirements. Only applies when require is at_least or at_most or exactly. |
| `operator` | `"=="` · `"!="` · `">"` · `">="` · `"<"` · `"<="` · `"between"` · `"in"` · `"not_in"` · `"contains"` · `"is_true"` · `"not_empty"` |  | `">="` |  | how each row is compared. Values: == (equals), != (does not equal), > (greater than), >= (at least), < (less than), <= (at most), between (between (inclusive)), in (is one of), not_in (is none of), contains (contains text), is_true (is true), not_empty (is not empty). |
| `value` | number |  |  |  | the value to compare against. Only applies when operator is == or != or > or >= or < or <=. |
| `min` | number |  |  |  | lower bound, inclusive. Only applies when operator is between. |
| `max` | number |  |  |  | upper bound, inclusive. Only applies when operator is between. |
| `set` | string[] |  |  |  | the values the field must be one of (or none of). Only applies when operator is in or not_in. |
| `text` | string |  |  |  | the text the field must contain. Only applies when operator is contains. |
| `label` | string |  |  |  | what this gate is checking, in your words. It becomes the message when it fails. |
| `report_only` | boolean |  | `false` |  | report the verdict instead of stopping the run: wire `passed` (or `failed`) into another step's condition to choose a branch. |
| `record` | string |  |  |  | optional: the record this gate is guarding. It comes back out of `record` when the check passes, so the gate sits in the middle of a chain. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `passed` | boolean |  | whether the requirement held. As a gate this is true whenever it is read downstream; with `report_only` on it is the real verdict, for driving a branch |
| `failed` | boolean |  | the opposite verdict, so the ELSE arm of a branch needs no extra step. Only meaningful with `report_only` on |
| `record` | object or null |  | the guarded record, unchanged. Wire it into the next node's $subject to make that step conditional |
| `matched` | number |  | how many rows met the per-row condition |
| `offenders` | any |  | the rows that did NOT meet it: what to look at when the gate fails |
| `message` | string |  | what was checked, in words |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_rows",
  "arguments": {
    "items": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### classify_flow_cytometry_events

**Classify flow cytometry events**: _Which population would a model trained on the gated ones assign each event to, or where does the density put a 2-D gate?_

Supervised and density gating on a project FCS file: a random forest (R randomForest 4.7) or a C-classification SVM (e1071 / libsvm) trained on the events of two or more of the strategy's populations (each event in exactly one of them, at most N per class drawn by R's sample()) and applied to every event of the parent, with out-of-bag or training confusion and Gini importance; or flowDensity 1.46's 2-D density gate on a channel pair (deGate threshold per channel, kept side, convex hull). Values on the display scale, compensated as chosen.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- The training populations are correct and representative of the events to be labelled; every event is forced into one class.

**Does not:**
- flowDensity's ellipse gate, control-file and margin options are not ported; nu-SVMs are not ported.

**Validated:** against the reference implementation by 3 golden suites.

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
| `classifier` | `"forest"` · `"svm"` · `"flowdensity"` |  | `"forest"` |  | random forest, support-vector machine, or flowDensity. |
| `classes` | string |  | `""` |  | comma-separated populations whose events are the classes (2 or more). |
| `channels` | string |  | `""` |  | comma-separated feature channels; empty for every channel but time. |
| `parent` | string |  | `""` |  | the population classified or density-gated; empty for all events. |
| `per_class` | number |  | `1000` | ≥ 0 | training events drawn per class (0 all). |
| `classify_seed` | number |  | `1` |  | the R seed. |
| `ntree` | number |  | `500` | ≥ 1 | trees. |
| `mtry` | number |  | `0` | ≥ 0 | channels tried per split; 0 for the square root of their count. |
| `nodesize` | number |  | `1` | ≥ 1 | minimum terminal node size. |
| `kernel` | `"radial"` · `"linear"` · `"polynomial"` · `"sigmoid"` |  | `"radial"` |  | the support-vector kernel. |
| `cost` | number |  | `1` |  | the support-vector cost. |
| `gamma` | number |  | `0` | ≥ 0 | the kernel gamma; 0 for 1 / the channel count. |
| `x` | string |  | `""` |  | flowDensity: the X channel. |
| `y` | string |  | `""` |  | flowDensity: the Y channel. |
| `side_x` | `"above"` · `"below"` · `"none"` |  | `"above"` |  | flowDensity: the side kept on X. |
| `side_y` | `"above"` · `"below"` · `"none"` |  | `"above"` |  | flowDensity: the side kept on Y. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `classes` | any |  | per class: events in it alone, trained on, predicted in the parent |
| `confusion` | any |  | observed × predicted over the training events, and the error |
| `gate` | any |  | flowDensity's thresholds, count, proportion and hull |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "classify_flow_cytometry_events",
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

### cluster_flow_cytometry_events

**Cluster flow cytometry events**: _Which clusters do the events of this population form, and how large is each?_

Clusters every event of an FCS file's population by k-means (R stats::kmeans: Hartigan-Wong, Lloyd, Forgy, MacQueen), DBSCAN, HDBSCAN or spectral clustering (scikit-learn, nearest-neighbour affinity, cluster_qr), PhenoGraph (Rphenograph's k-nearest-neighbour Jaccard graph, then R igraph cluster_louvain or cluster_leiden), flowPeaks or SamSPECTRAL (Bioconductor, on the plotted pair), a Gaussian mixture (R mclust Mclust: spherical EII/VII, diagonal EEI/VEI/EVI/VVI or ellipsoidal EEE/VEE/EVE/VVE/EEV/VEV/EVV/VVV covariance, or all of them compared, G and model chosen by BIC), or X-shift (VorteX: angular-distance kNN density gradient, roots merged by a density path and a Mahalanobis threshold). On the display scale; returns each cluster's events and channel medians, the per-event labels, and the method's own readouts.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Clusters are separable on the chosen channels after the display transform.

**Does not:**
- One file per call. flowPeaks and SamSPECTRAL cluster the plotted pair only (two channels).
- The Gaussian mixture offers all 14 of mclust's covariance models (no noise component, no prior).
- X-shift runs one K per call (VorteX sweeps a K range; call once per K to compare).

**Validated:** against the reference implementation by 10 golden suites.

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
| `plot_x` | string |  |  |  | channel (PnN or PnS) on the density plot's x axis; empty for no plot. |
| `plot_y` | string |  |  |  | channel on the plot's y axis. |
| `plot_population` | string |  |  |  | the population plotted; empty for all events. |
| `channels` | string |  |  |  | channels to cluster on, comma-separated; empty for every fluorescence channel (flowPeaks and SamSPECTRAL take plot_x and plot_y). |
| `downsample` | `"none"` · `"spade"` · `"random"` |  | `"none"` |  | downsample before clustering: none, spade (density-dependent) or random; the rest take their nearest clustered event’s label. |
| `downsample_percent` | number |  | `10` | 0.01–100 | percent of events kept (SPADE: of those left after exclusion). |
| `downsample_exclude_percent` | number |  | `1` | 0–99 | SPADE exclude_pctile, percent: the sparsest events dropped as noise. |
| `spade_kernel_mult` | number |  | `5` | ≥ 0 | SPADE kernel_mult: density radius in median nearest-neighbour distances. |
| `spade_apprx_mult` | number |  | `1.5` | ≥ 0 | SPADE apprx_mult: events this close share a density count. |
| `spade_med_samples` | number |  | `2000` | ≥ 1 | SPADE med_samples: events sampled for the median nearest-neighbour distance. |
| `cluster_method` | `"kmeans"` · `"dbscan"` · `"hdbscan"` · `"phenograph"` · `"flowpeaks"` · `"samspectral"` · `"spectral"` · `"mclust"` · `"xshift"` |  | `"phenograph"` |  | the clustering method. |
| `seed` | number |  | `42` |  | R set.seed (k-means, PhenoGraph, SamSPECTRAL, mclust subset). |
| `kmeans_centers` | number |  | `8` | ≥ 1 | k-means centers. |
| `kmeans_algorithm` | `"Hartigan-Wong"` · `"Lloyd"` · `"Forgy"` · `"MacQueen"` |  | `"Hartigan-Wong"` |  | k-means algorithm. |
| `kmeans_nstart` | number |  | `1` | ≥ 1 | k-means random starts (nstart). |
| `kmeans_max_iter` | number |  | `10` | ≥ 1 | k-means iter.max. |
| `dbscan_eps` | number |  | `0.05` | ≥ 0 | DBSCAN radius on the display scale. |
| `dbscan_min_samples` | number |  | `5` | ≥ 1 | DBSCAN core neighbours. |
| `hdbscan_min_cluster_size` | number |  | `50` | ≥ 2 | HDBSCAN min_cluster_size. |
| `hdbscan_min_samples` | number |  |  | ≥ 1 | HDBSCAN min_samples; empty means min_cluster_size. |
| `hdbscan_method` | `"eom"` · `"leaf"` |  | `"eom"` |  | HDBSCAN cluster_selection_method. |
| `hdbscan_allow_single` | boolean |  | `false` |  | HDBSCAN allow_single_cluster. |
| `pheno_k` | number |  | `30` | ≥ 2 | PhenoGraph nearest neighbours. |
| `pheno_community` | `"louvain"` · `"leiden"` |  | `"louvain"` |  | PhenoGraph community search. |
| `pheno_resolution` | number |  | `1` | ≥ 0 | PhenoGraph resolution. |
| `pheno_iterations` | number |  | `2` |  | Leiden n_iterations; negative iterates until stable. |
| `flow_peaks_tol` | number |  | `0.1` | 0–1 | flowPeaks tol. |
| `flow_peaks_h0` | number |  | `1` | ≥ 0 | flowPeaks h0. |
| `flow_peaks_h` | number |  | `1.5` | ≥ 0 | flowPeaks h. |
| `sam_sigma` | number |  | `200` | ≥ 1 | SamSPECTRAL normal.sigma. |
| `sam_separation` | number |  | `0.7` | 0–1 | SamSPECTRAL separation.factor. |
| `sam_m` | number |  | `500` | ≥ 10 | SamSPECTRAL representatives (m). |
| `spectral_clusters` | number |  | `8` | ≥ 2 | spectral clustering n_clusters. |
| `spectral_neighbors` | number |  | `10` | ≥ 2 | spectral clustering n_neighbors (the event itself counted). |
| `mclust_min_g` | number |  | `1` | ≥ 1 | mclust fewest components (G from). |
| `mclust_max_g` | number |  | `9` | ≥ 1 | mclust most components (G to). |
| `mclust_model` | `"all"` · `"EII"` · `"VII"` · `"EEI"` · `"VEI"` · `"EVI"` · `"VVI"` · `"EEE"` · `"VEE"` · `"EVE"` · `"VVE"` · `"EEV"` · `"VEV"` · `"EVV"` · `"VVV"` |  | `"VVI"` |  | mclust covariance model (modelNames): EII, VII spherical; EEI, VEI, EVI, VVI diagonal; EEE, VEE, EVE, VVE, EEV, VEV, EVV, VVV ellipsoidal; 'all' compares them by BIC. |
| `mclust_start` | `"VVV"` · `"EII"` |  | `"VVV"` |  | mclust initial hierarchy: 'VVV' is mclust's default (hcModelName VVV, hcUse SVD), 'EII' the spherical Ward start on the raw channels (hcModelName EII, hcUse VARS). |
| `xshift_k` | number |  | `30` | ≥ 3 | X-shift K (density neighbours). |
| `xshift_nsize` | number |  | `0` | ≥ 0 | X-shift neighbours searched for a denser parent; 0 is automatic. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `clusters` | any |  | per cluster: events, share of the clustered events, median per channel |
| `labels` | any |  | per event of the file, the 1-based cluster; 0 for unassigned or outside the population |
| `readouts` | any |  | the method's own readouts (tot.withinss, modularity, stability, …) |
| `unassigned` | number |  | events the method left unassigned (noise) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "cluster_flow_cytometry_events",
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

### cluster_flow_cytometry_flowsom

**Cluster flow cytometry FlowSOM**: _Which cell populations does FlowSOM find in this file, and how large is each?_

FlowSOM on an FCS file's population: a self-organizing map of the chosen channels (fluorescence on the display scale), its nodes joined by their minimum spanning tree, grouped into metaclusters by ConsensusClusterPlus, with per-node marker medians, shares of events and FlowSOM's TestOutliers report. The seed is an input and is returned.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Clusters are separable on the chosen channels after the display transform.

**Does not:**
- One file per call; the map is rebuilt each call (no FlowSOM model reuse across files).

**Validated:** against the reference implementation by 1 golden suite.

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
| `seed` | number |  | `42` |  | R set.seed for the map and the metaclustering. |
| `xdim` | number |  | `10` | 2–30 | grid width. |
| `ydim` | number |  | `10` | 2–30 | grid height. |
| `rlen` | number |  | `10` | 1–100 | training passes over the data. |
| `n_clus` | number |  | `10` | ≥ 2 | metaclusters. |
| `channels` | string |  |  |  | channels to build the map on, comma-separated; empty for every fluorescence channel. |
| `standardize` | boolean |  | `false` |  | FlowSOM scale = TRUE: center and divide each channel by its SD first. |
| `outlier_mad` | number |  | `4` | ≥ 0.5 | TestOutliers madAllowed. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `metaclusters` | any |  | per metacluster: share of events |
| `nodes` | any |  | per node: metacluster, share of events, median per map channel |
| `mst` | any |  | the minimum spanning tree: node pairs and normalized weights |
| `outliers` | any |  | per node: events, outliers, distance threshold, maximum distance |
| `seed` | number |  | the seed the run consumed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "cluster_flow_cytometry_flowsom",
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

### compare_antibodies

**Compare antibodies**: _How do these antibodies' heavy (or light) variable domains differ position by position, and how do their lengths, pI, charge, hydropathy, extinction and CDR charge compare?_

Several antibodies side by side: each record numbered by ANARCI, its heavy or its light variable domains aligned column by column by their numbering (a column is one scheme position, so nothing is re-aligned and an insertion is its own column), the CDR of every column under the chosen definition, how many columns agree, and the same properties read off each V domain: length, mass, isoelectric point, net charge, GRAVY, ε280 and the net charge of its CDRs. The alignment is abnumber's `Chain.align`, graded against it over every chain of ANARCI's PDB benchmark; the properties against Biopython ProtParam.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Columns are scheme positions: two chains share a column exactly when their numbering gives them the same position.
- Properties are of the numbered V domain, not the whole record, so constant regions do not enter the comparison.
- CDR charge sums the side-chain charges of the CDR residues at the pH (Bjellqvist pKs, as ProtParam), with no termini.

**Does not:**
- Heavy and light chains cannot share an alignment; kappa and lambda can, as both number on the light scale.
- A record with no domain of the chosen class is refused by name, as is a domain the scheme leaves un-numbered.
- Sequence-derived: no structure, so no surface patches or paratope.

**Not read from this result:** The answer is the numbered alignment and per-chain properties, which the outputs carry; the Antibody panel's Compare section shows them as a table and writes no reading over them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `antibodies` | string[] |  |  |  | the antibody chains to compare: wire several upstream records here, or list library documents or protein sequences. |
| `include_subject` | boolean |  | `true` |  | also compare the open record. |
| `chain` | `"heavy"` · `"light"` |  | `"light"` |  | which variable domains to align: heavy, or light (kappa and lambda together). Values: heavy (Heavy), light (Light (kappa and lambda)). |
| `definition` | `"imgt"` · `"kabat"` · `"chothia"` · `"north"` |  | `"kabat"` |  | the CDR definition, numbered in its own scheme (North in Chothia's). Values: imgt (IMGT), kabat (Kabat), chothia (Chothia), north (North). |
| `pH` | number |  | `7.4` |  | the pH the net charge and the CDR charge are reported at. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rows` | any |  | one gapped row per aligned chain, `{ name, aligned }`, the shape the alignment tools read |
| `positions` | any |  | the scheme position of each column (`82A`) |
| `regions` | any |  | the region of each column under the definition: FR1, CDR1 … FR4 |
| `chains` | any |  | per chain: name, record, chain type, and its V domain's length, molecularWeight (Da), isoelectricPoint, chargeAtPH, gravy, extinction (reduced and cystines) and cdrCharge |
| `mutations` | number |  | columns holding more than one residue (a gap counts as one) |
| `identical` | number |  | columns where every chain holds the same residue |
| `refused` | any |  | records that gave no chain of the class, each with its reason |
| `alignment` | string |  | the alignment as abnumber prints it: rows, identity lines, and the CDRs marked ^ (Vernier °, under Kabat) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "compare_antibodies",
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

### correct_flow_cytometry_batches_cycombine

**Correct flow cytometry batches cyCombine**: _Where must each cell move so that the batches agree within every group of similar cells, without a control sample?_

cyCombine batch correction without controls: every value on asinh(x / cofactor) (counts rounded up first), each batch scaled on its own, a kohonen self-organizing map grouping the scaled cells, then parametric ComBat inside each map node on the unscaled values with batch as the only factor (optionally onto one reference batch), each result capped to the node's range and taken back by sinh. A sample sheet names each file's batch. Per node the cells per batch and what ComBat did there; per channel and batch the median before and after.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Every batch holds the same cell populations in similar proportions; a population found in one batch only is pulled toward the others.
- Within one map node a batch effect is a shift and a scaling of each channel, as ComBat models it.

**Does not:**
- The corrected files are written to the project from the panel only; this door returns the node summary and the medians.
- No covariates or anchors, no non-parametric ComBat and no other clustering than the kohonen map.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `samples` | string |  | `""` |  | the FCS files, by name or id, comma-separated; empty for every FCS file in the project (each must be named in the sample sheet). |
| `sample_sheet` | string | **yes** |  |  | a CSV in the project whose first column, headed sample, names each FCS file, with a batch column. |
| `batch_column` | string |  | `"batch"` |  | the sample sheet's column naming each file's batch. |
| `channels` | string |  | `""` |  | the channels to correct, comma-separated PnN; empty for every channel but scatter, time and event length. |
| `asinh_cofactor` | number |  | `5` | ≥ 0.01 | the asinh cofactor (5 for mass cytometry). |
| `derand` | boolean |  | `true` |  | round counts up (ceiling) before the transform. |
| `som_width` | number |  | `8` | 2–30 | SOM map width (xdim). |
| `som_height` | number |  | `8` | 2–30 | SOM map height (ydim). |
| `epochs` | number |  | `10` | 1–100 | kohonen rlen: passes over the data. |
| `kohonen_seed` | number |  | `473` | ≥ 0 | R's set.seed before the map. |
| `ref_batch` | string |  | `""` |  | ComBat ref.batch: a batch left as it is, the others moved onto it; empty for none. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `nodes` | any |  | per map node, the cells per batch and whether ComBat corrected it (location and scale, location only, or left as it is) |
| `medians` | any |  | per channel and batch, the median before and after (asinh scale) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "correct_flow_cytometry_batches_cycombine",
  "arguments": {
    "sample_sheet": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### enzyme_cut_counts

**Enzyme cut counts**: _How many times does each enzyme cut this molecule?_

Per-enzyme cut counts on the open plasmid (the EcoRI² superscript-badge numbers).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Recognition sites are REBASE's, as the bundled table holds them.

**Does not:**
- Counts sites; it does not say whether a cut is blocked or stars.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `enzymes` | string[] | **yes** |  |  | enzyme names to scope the scan to — resolved against the bundled cut catalog (REBASE spellings; smaller than the REBASE dossier the editor shows). Left unset, the run uses your active enzyme collection. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `counts` | any |  | enzyme → cut-count map; an enzyme with no sites is present with 0, never omitted |
| `total` | number |  | total cuts across every enzyme asked about |
| `cutters` | number |  | how many of the enzymes cut at least once |
| `single` | number |  | how many cut EXACTLY once: the enzymes that linearise this molecule |
| `zero_cutters` | number |  | how many were scanned for and have no site here |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "enzyme_cut_counts",
  "arguments": {
    "enzymes": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### estimate_cytof_spillover

**Estimate cytof spillover**: _How much does each metal channel of this mass cytometry panel spill into the others?_

CATALYST bead-based spillover for mass cytometry from a single-stained bead FCS file in the project: the beads debarcoded to their stained mass (one population per mass, each separation cutoff estimated from its yield curve), then each stained channel's spill into the channels it can physically reach (one mass up or down, its oxide at +16, its element's other isotopes from NIST) as the median per-bead ratio of background-corrected receiver to spiller (or the classic ratio of trimmed means); spills below 1e-5 set to 0. Optionally fitted to an open file's metal channels.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Each bead population carries one metal, so every other signal on it is spill (plus background).
- The bead panel covers the masses of the file to compensate; a channel with no beads keeps its identity row.

**Does not:**
- Compensating a file is done from the panel (flowCore inverse or NNLS); this door returns the matrix.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `beads` | string | **yes** |  |  | the single-stained bead FCS file in the project, by name or id. |
| `masses` | string | **yes** |  |  | the stained masses, one bead population each, as ranges: 139, 141-156, 158-176. |
| `spill_estimator` | `"default"` · `"classic"` |  | `"default"` |  | computeSpillmat's estimator: per-bead ratios (default) or trimmed means (classic). Values: default (per bead), classic (classic). |
| `interactions` | `"default"` · `"all"` |  | `"default"` |  | the channel pairs estimated: the physically possible ones, or every pair. Values: default (physical), all (every pair). |
| `document` | string |  | `""` |  | an FCS file to fit the matrix to (its metal channels); empty for none. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `spillover` | any |  | the matrix: stained channels (rows) into every metal channel (columns), row-major |
| `populations` | any |  | per stained mass, its channel and the beads assigned to it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "estimate_cytof_spillover",
  "arguments": {
    "beads": "<string>",
    "masses": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### estimate_flow_cytometry_scale

**Estimate flow cytometry scale**: _Which transform parameters does this data itself support?_

Choose the transform from the data. flowVS: the asinh(x / c) cofactor of one channel that makes its density peaks' variances most alike across project FCS files (Bartlett's statistic, Brent search over e^-1..e^10). flowTrans: the arcsinh, Box-Cox, linlog or biexponential parameters that make two or more channels of one file most jointly normal (profile likelihood, L-BFGS-B).

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- flowVS: the files hold the same populations, so their peaks should share a variance.
- flowTrans: the chosen channels are jointly normal after the right transform.

**Does not:**
- flowVS chooses one cofactor per channel; flowTrans one parameter set for all its channels.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `estimator` | `"flowvs"` · `"flowtrans"` |  | `"flowvs"` |  | flowvs or flowtrans. |
| `channel` | string |  | `""` |  | flowvs: the channel. |
| `channels` | string |  | `""` |  | flowtrans: two or more channels, comma-separated. |
| `model` | `"arcsinh"` · `"boxcox"` · `"linlog"` · `"biexp"` |  | `"arcsinh"` |  | flowtrans: the transform. |
| `population` | string |  | `""` |  | a population, gated in every file; empty for all. |
| `sample_files` | string |  | `""` |  | flowvs: project FCS files, comma-separated; empty for all. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `cofactor` | number or null |  | flowVS's chosen cofactor, or null |
| `flowvs` | any |  | the search (window optima, local cofactors) and each file’s peaks at the cofactor; null for flowTrans |
| `flowtrans` | any |  | the fitted parameters, objective, convergence and the transform they define; null for flowVS |
| `scale_params` | any |  | the fit as analyze_flow_cytometry's `scale` and its parameters (flowVS: arcsinh and the cofactor), to display the data on it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "estimate_flow_cytometry_scale",
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

### estimate_spectra_from_controls

**Estimate spectra from controls**: _What spectral signatures do these single-stain controls imply?_

flowSpecs specMatCalc on spectral single-stain control tubes in the project: per tube, MAD gates on scatter and the brightest detector, the median of every detector; each group's dimmest tube subtracted, autofluorescence added, each signature scaled to its maximum. Returns the spectral matrix analyze_flow_cytometry's spectral_matrix unmixes by.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Each stained tube carries one fluorochrome; tubes acquired alike (beads, cells) share a name prefix, and the dimmest of each group is its negative.
- The autofluorescence tube is unstained cells, used as it is.

**Does not:**
- Fluorochrome names come from the tube names (the prefix and .fcs removed), as flowSpecs names them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `tubes` | string | **yes** |  |  | the control FCS files in the project, by name or id, comma-separated, the unstained and autofluorescence tubes included. |
| `groups` | string | **yes** |  |  | the tube-name prefixes that group tubes acquired alike, comma-separated (Beads_, Dead_). |
| `autofluorescence` | string | **yes** |  |  | which of the tubes is the unstained one whose spectrum is the autofluorescence, by name or id. |
| `excluded` | string |  | `"Time\|SC\|Sort\|ate\|omp\|LightLoss\|Row\|Column"` |  | regular expression for the channels that are not detectors. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `matrix` | object or null |  | the spectral matrix, rows the fluorochromes, columns the detectors |
| `matrix.rows` | string[] |  |  |
| `matrix.cols` | string[] |  |  |
| `matrix.values` | ((number or null)[])[] |  |  |
| `matrix.label` | string |  |  |
| `matrix.title` | string |  |  |
| `tubes` | any |  | what each tube's gates kept, its brightest detector and its role |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "estimate_spectra_from_controls",
  "arguments": {
    "tubes": "<string>",
    "groups": "<string>",
    "autofluorescence": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### estimate_spillover_from_controls

**Estimate spillover from controls**: _What spillover matrix do these compensation controls imply?_

flowStats spillover() on single-stained control tubes and an unstained tube from the project: per tube the median (or mean, or density mode) of every detector, the unstained baseline subtracted, each stained tube matched to its channel (by name distance or tube order), each row divided by its own detector. Returns the matrix, the tube → channel matching, flowStats' warnings, and the spillover spreading matrix (SSM) of the tubes compensated by it.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Each stained tube carries one fluorochrome and is brightest in its own detector.

**Does not:**
- norm2Filter scatter gating (useNormFilt) is not implemented.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `tubes` | string | **yes** |  |  | the control FCS files in the project, by name or id, comma-separated, the unstained one included. |
| `unstained` | string | **yes** |  |  | which of the tubes is unstained, by name or id. |
| `statistic` | `"median"` · `"mean"` · `"mode"` |  | `"median"` |  | the per-tube statistic. Values: median (median), mean (mean), mode (density mode). |
| `stain_match` | `"intensity"` · `"ordered"` |  | `"intensity"` |  | how tubes are matched to channels. Values: intensity (by name), ordered (in tube order). |
| `fsc` | string |  | `"FSC-A"` |  | forward scatter channel, left out of the matrix. |
| `ssc` | string |  | `"SSC-A"` |  | side scatter channel, left out of the matrix. |
| `pattern` | string |  | `""` |  | regular expression the detectors must match; empty for all. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `matrix` | object or null |  | the spillover matrix, rows the stained channels, columns the detectors |
| `matrix.rows` | string[] |  |  |
| `matrix.cols` | string[] |  |  |
| `matrix.values` | ((number or null)[])[] |  |  |
| `matrix.label` | string |  |  |
| `matrix.title` | string |  |  |
| `matching` | any |  | tube → channel |
| `warnings` | any |  | flowStats' warnings |
| `spread` | object or null |  | the spillover spreading matrix (Nguyen 2013, as CytoExploreR computes it) of the tubes compensated by this matrix: rows the stained channels, columns the detectors, NA on each stain’s own channel |
| `spread.rows` | string[] |  |  |
| `spread.cols` | string[] |  |  |
| `spread.values` | ((number or null)[])[] |  |  |
| `spread.label` | string |  |  |
| `spread.title` | string |  |  |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "estimate_spillover_from_controls",
  "arguments": {
    "tubes": "<string>",
    "unstained": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### filter_items

**Filter items**: _Which rows of this table meet the condition, and how many were dropped?_

Keep only the rows of a table-shaped output that meet a condition — the bands above a size, the guides over a score, the assays under a penalty. Emits the kept rows plus how many were dropped, so a downstream gate can act on the count.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Filters rows as given; it does not re-rank or recompute them.

**No scientific claim:** Selects rows by a condition; it computes no new quantity.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `items` | string[] | **yes** |  |  | the rows to filter — wire a json/list output (bands, guides, assays, amplicons). |
| `field` | string |  |  |  | which field of each row to test (e.g. `size`, `score`, `length`). Leave empty to test the row itself when it is a plain number. |
| `operator` | `"=="` · `"!="` · `">"` · `">="` · `"<"` · `"<="` · `"between"` · `"in"` · `"not_in"` · `"contains"` · `"is_true"` · `"not_empty"` |  | `">="` |  | how to compare. Values: == (equals), != (does not equal), > (greater than), >= (at least), < (less than), <= (at most), between (between (inclusive)), in (is one of), not_in (is none of), contains (contains text), is_true (is true), not_empty (is not empty). |
| `value` | number |  |  |  | the value to compare against. Only applies when operator is == or != or > or >= or < or <=. |
| `text` | string |  |  |  | the text a field must contain. Only applies when operator is contains. |
| `min` | number |  |  |  | lower bound, inclusive. Only applies when operator is between. |
| `max` | number |  |  |  | upper bound, inclusive. Only applies when operator is between. |
| `set` | string[] |  |  |  | the values the field must be one of (or none of). Only applies when operator is in or not_in. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `items` | any |  | the rows that met the condition |
| `count` | number |  | how many rows were kept — wire this into check_value to gate on it |
| `dropped` | number |  | how many rows were removed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "filter_items",
  "arguments": {
    "items": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### find_common_substructure

**Find common substructure**: _What is the largest substructure all of these molecules share?_

The maximum common substructure of a set of small molecules (RDKit FindMCS): the largest core every structure shares, as SMARTS, with its atom and bond count. This is the core decompose_r_groups takes — find it here rather than guessing one — and the answer to 'is this actually a series'. Structures RDKit cannot read are reported, never dropped silently.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's FindMCS defaults unless the two ring options are set.

**Does not:**
- One core for the whole set: a library of two unrelated series has a small MCS, which is the finding, not a failure.
- A timeout returns the best core found so far, flagged as a lower bound rather than the maximum.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `complete_rings_only` | boolean |  | `false` |  | a ring is in the core whole or not at all — the core a chemist would draw. Off, RDKit may return a partial ring, which is a valid substructure and a strange thing to call a scaffold. |
| `ring_matches_ring_only` | boolean |  | `false` |  | a ring atom only matches another ring atom, so a chain carbon never maps onto a ring one. |
| `timeout` | number |  | `60` | ≥ 1 | seconds before RDKit stops searching. The MCS problem is NP-hard, so a large diverse set can run long; a run that stops early reports its core as a lower bound. In s. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the common core in words, generated from this run |
| `smarts` | string |  | the common core as SMARTS — wire it into decompose_r_groups as `core` |
| `numAtoms` | number |  | atoms in the core |
| `numBonds` | number |  | bonds in the core |
| `canceled` | boolean |  | the search hit the timeout, so this core is a LOWER BOUND and a longer run may find a larger one |
| `unread` | any |  | input indices RDKit could not read |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_common_substructure",
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

### find_orfs

**Find ORFs**: _Which open reading frames does this molecule carry, on both strands?_

Find open reading frames on BOTH strands of the subject (origin-spanning when circular).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The start and stop codons are the chosen code's; a circular molecule's frames wrap the origin.

**Does not:**
- An ORF is a reading frame, not a gene: no promoter, RBS or expression evidence is involved.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `min_size` | number |  | `300` | 30–10000 | minimum ORF size. In bp. |
| `alternative_starts` | boolean |  | `false` |  | also accept GTG/CTG as start codons (not just ATG). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `orfs` | any |  | the ORFs (start, end, frame, strand) |
| `count` | number |  | number of ORFs found |
| `longest` | number | bp | length of the longest ORF in bp |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_orfs",
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

### find_primer_snps

**Find primer SNPs**: _Which known dbSNP variants sit under these primers, and how far is each from the 3' end?_

Find known SNPs under primers, the check NCBI Primer-BLAST makes with "Primer binding site may not contain known SNP". The template is placed on the UCSC assembly it was cut from, and the placement is proved by comparing the assembly's own sequence with the template; dbSNP 155 is then read over that span from the UCSC Genome Browser, and every primer is reported with the SNPs under it and each one's distance from the 3' end. `excluded` is the SNP spans in the form design_primer_pairs takes, to design around them. The template's sequence does not leave the machine; the assembly, chromosome and span are sent to UCSC.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Assumes:**
- The template is placed on the UCSC assembly named, and the placement is proved by comparing sequence.
- dbSNP 155 as the UCSC Genome Browser serves it.

**Does not:**
- Needs the network; only templates placed on a UCSC assembly can be checked.

**Not yet validated:** The placement and the 3'-distance arithmetic are tested, but no golden grades the SNP list against Primer-BLAST's own.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `assembly` | string | **yes** |  |  | the UCSC assembly id the template was cut from (hg38, mm39, danRer11…). |
| `position` | string | **yes** |  |  | where the template sits in that assembly, as chromosome:position, 1-based: the lowest assembly coordinate the template covers. The check finds which strand the template reads on itself. |
| `snp_set` | `"dbSnp155Common"` · `"dbSnp155"` · `"dbSnp155ClinVar"` |  | `"dbSnp155Common"` |  | `dbSnp155Common`: About 15 million variants with a minor allele frequency of at least 1% in 1000 Genomes Phase 3. The default. `dbSnp155`: Every mapped variant: 1.06 billion locations on hg38, so few primers avoid them all. `dbSnp155ClinVar`: About 820,000 variants ClinVar mentions, benign and pathogenic alike. |
| `pairs` | object[] |  |  |  | the pairs to check, as design_primer_pairs' `pairs` output (each with forward and reverse start/end on the template). |
| `forward` | string |  |  |  | a forward primer to locate on the template by exact match, when no `pairs` are given. |
| `reverse` | string |  |  |  | a reverse primer to locate by exact match of its reverse complement. |
| `template` | string |  |  |  | the sequence the primers sit on. Left empty, the open record is used. |
| `window_start` | number |  |  | ≥ 1 | 1-based first base of the template span to check. Unset = the whole template. Advanced. |
| `window_end` | number |  |  | ≥ 1 | 1-based last base of the span to check. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `primers` | any |  | every primer checked: its name, span on the template, strand, and the SNPs under it with rsID, alleles, minor allele frequency and distance from the 3′ end (1 = the 3′ base) |
| `snps` | any |  | every SNP in the span, placed on the template (0-based, end-exclusive), with alleles as they read on the template's strand and whether the template spells dbSNP's reference allele there |
| `excluded` | any |  | the SNP spans, for design_primer_pairs' `excluded` |
| `flagged` | number |  | how many primers sit on at least one known SNP |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_primer_snps",
  "arguments": {
    "assembly": "<string>",
    "position": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### fit_flow_cytometry_cell_cycle

**Fit flow cytometry cell cycle**: _What share of these DNA-stained cells is in G1, S and G2/M?_

The classical univariate cell-cycle models on a linear DNA-content channel of a project FCS file, optionally one population: Dean–Jett–Fox (Gaussian G1 and G2/M, a broadened second-order polynomial S phase, optional exponential debris and G1+G2 / G2+G2 aggregates, weighted Levenberg–Marquardt) or Watson pragmatic (Gaussians on the outer flank of each peak, S phase as the remainder). % G1, S and G2/M (with delta-method standard errors for Dean–Jett–Fox), peak means and CVs, the G2/G1 ratio, reduced chi-square, the fitted curves and the fit warnings.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The channel is linear DNA content (area) of singlets; G1 is the tallest peak (or half of it, after a G2/M arrest) and G2/M sits near twice it.
- Percentages exclude debris and aggregates, as FlowJo and ModFit report them.

**Does not:**
- One cycling population per histogram; ModFit-style Multicycle (several overlapping cycles) is not available.
- Watson pragmatic gives no standard errors; its S phase is a remainder, not a model.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `channel` | string |  | `""` |  | the DNA-content channel (PnN or PnS). |
| `population` | string |  | `""` |  | a population of the strategy to analyze; empty for every event. |
| `model` | `"djf"` · `"watson"` |  | `"djf"` |  | the cell-cycle model. Values: djf (Dean–Jett–Fox), watson (Watson pragmatic). |
| `bins` | number |  | `256` | ≥ 32 | histogram bins over 0 to 1.1 × the 99.9th percentile. |
| `ratio` | number |  | `0` | ≥ 0 | a fixed G2/G1 ratio; 0 fits it. |
| `equal_cv` | boolean |  | `true` |  | hold the G2 CV at the G1 CV. |
| `cv` | number |  | `0` | 0–0.25 | Dean–Jett–Fox: a fixed G1 CV as a fraction; 0 fits it. |
| `debris` | boolean |  | `false` |  | Dean–Jett–Fox: add exponential debris. |
| `aggregates` | boolean |  | `false` |  | Dean–Jett–Fox: add G1+G2 and G2+G2 aggregates. |
| `flank_correction` | boolean |  | `true` |  | Watson: model the S-phase edge inside each flank window; false is Watson's original outer-half fit. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `phases` | any |  | % G1, S and G2/M, their standard errors (Dean–Jett–Fox), each peak (mean, CV, SD, area), the S phase, the G2/G1 ratio |
| `fit` | any |  | chi-square, reduced chi-square, degrees of freedom, RMSD, fitted bins, parameters, convergence and the warnings |
| `curves` | any |  | the histogram and every fitted component per bin, with the bin centres |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fit_flow_cytometry_cell_cycle",
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

### fit_flow_cytometry_compass

**Fit flow cytometry COMPASS**: _Which cytokine combinations respond to stimulation in each subject, and how polyfunctional is the response?_

COMPASS polyfunctionality on Boolean cytokine-subset counts, from a project CSV (FlowJo export, stimulated and unstimulated rows paired by subject) or from the gating strategy's parent and child gates in every project FCS file a sample sheet names (COMPASSContainerFromGatingSet): each subject's posterior probability of response per subset, and functionality and polyfunctionality scores. Seeded MCMC; cost grows with iterations × subjects × subsets².

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Counts are cells per Boolean subset; the stimulated and unstimulated rows of a subject come from the same sample.
- From gates: an event is positive for a marker when it lies in that child gate of the parent, so the gates decide positivity.

**Does not:**
- A short chain need not have converged; COMPASS’s authors run 400,000 iterations × 8 replications.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"table"` · `"gating"` |  | `"table"` |  | where the subset counts come from: 'table' (a count CSV) or 'gating' (the strategy's gates in every FCS file the sample sheet names). |
| `count_table` | string |  | `""` |  | the project count CSV. Only applies when source is table. |
| `sample_sheet` | string |  | `""` |  | the sample sheet naming each FCS file (first column) with its condition and subject columns. Only applies when source is gating. |
| `gating` | string |  | `""` |  | the project gating strategy (Gating-ML or FlowJo workspace) applied to every file. Only applies when source is gating. |
| `parent` | string |  | `""` |  | the parent population whose child gates are the markers (COMPASSContainerFromGatingSet's node). Only applies when source is gating. |
| `markers` | string |  | `""` |  | comma-separated child gates of the parent to take as markers; empty for every child. Only applies when source is gating. |
| `count_filter` | number |  | `5000` | ≥ 0 | countFilterThreshold: a file whose parent holds no more events is left out (0 keeps every file). Only applies when source is gating. |
| `condition` | string |  | `""` |  | the condition column. |
| `stimulated` | string |  | `""` |  | its stimulated value. |
| `unstimulated` | string |  | `""` |  | its unstimulated value. |
| `subject` | string |  | `""` |  | the subject column. |
| `group` | string |  | `""` |  | a column to group scores by; empty for none. |
| `iterations` | number |  | `1000` | ≥ 10 | iterations per pass. |
| `replications` | number |  | `3` | ≥ 1 | sampling passes. |
| `mcmc_seed` | number |  | `100` |  | the R seed. |
| `min_stimulated` | number |  | `0` | ≥ 0 | drop subsets with fewer stimulated cells in all (0 keeps all). Only applies when source is table. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `scores` | any |  | per subject: group, functionality and polyfunctionality score |
| `mean_gamma` | any |  | subsets and, per subject, the posterior probability of response in each |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fit_flow_cytometry_compass",
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

### fit_flow_cytometry_proliferation

**Fit flow cytometry proliferation**: _How many divisions have these dye-labeled cells gone through, and what share sits in each generation?_

flowFit's division-dye model (CFSE, CellTrace, PKH26): a Gaussian fitted to a project file of unstimulated (parent) cells, then the stimulated file fitted by nls.lm as one Gaussian per generation a dye halving apart (position, width or spacing optionally held); each generation's %, flowFit's proliferation index and Roederer's indices. Or flowFit's refusal.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The dye halves at each division and the channel is acquired on a log (decades) scale, so generations are evenly spaced on it.
- The parent file holds the same cells labeled alike and left unstimulated; its peak is generation 1.

**Does not:**
- At most 20 generations; one width is shared by every generation.
- Shares integrate the fitted model, so overlapping generations are split by the model, not by gates.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `parent_file` | string |  | `""` |  | the unstimulated (parent) FCS file. |
| `channel` | string |  | `""` |  | the dye channel (PnN or PnS). |
| `population` | string |  | `""` |  | a population, gated in both files; empty for all. |
| `breaks` | number |  | `1024` | ≥ 16 | histogram breaks. |
| `smooth_window` | number |  | `2` | ≥ 1 | the smoothing window. |
| `fix_position` | boolean |  | `false` |  | hold the parent position. |
| `fix_size` | boolean |  | `false` |  | hold the parent width. |
| `fix_distance` | boolean |  | `false` |  | hold the spacing at one dye halving. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `generations` | any |  | per generation: center, rounded cell count and % of cells; null when refused |
| `fit` | any |  | the parent fit, the fitted and held parameters, spacing, iterations, deviance and the proliferation index; null when refused |
| `indices` | any |  | Roederer's division-tracking indices over flowFit's counts; null when refused |
| `refused` | string or null |  | flowFit's refusal, or null |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fit_flow_cytometry_proliferation",
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

### fit_flow_cytometry_trajectory

**Fit flow cytometry trajectory**: _Which developmental paths run through these clusters, and how far along each path is every event?_

Lineages and pseudotime on a project FCS file by Slingshot (slingshot 2.20.0): the clusters are either a clustering run here with the cluster_* knobs (as cluster_flow_cytometry_events runs it) or two or more of the strategy's populations (an event in two is left out); at most max_events events drawn by R's sample(); a minimum spanning tree over the cluster centres (Slingshot's covariance-scaled, Euclidean or Mahalanobis distance, optional outgroup), lineages from the root, and simultaneous principal curves shrunk toward their average. Per lineage: its clusters, events, median and longest pseudotime; per event: pseudotime and weight on every lineage. Values on the display scale, compensated as chosen.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- The clusters are the right states and the continuum runs through them; the tree over their centres is the path the cells take; the root is the true start.

**Does not:**
- Slingshot's own clustering-free mode, its `predict` on new cells and a dimensionality reduction before it are not run here; the channels are taken as given.

**Validated:** against the reference implementation by 1 golden suite.

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
| `plot_x` | string |  |  |  | channel (PnN or PnS) on the density plot's x axis; empty for no plot. |
| `plot_y` | string |  |  |  | channel on the plot's y axis. |
| `plot_population` | string |  |  |  | the population plotted; empty for all events. |
| `cluster_source` | `"clustering"` · `"populations"` |  | `"clustering"` |  | the clusters: a clustering run here with the cluster_* knobs, or populations. |
| `populations` | string |  | `""` |  | source populations: the comma-separated populations taken as clusters (2 or more). |
| `channels` | string |  |  |  | source clustering: channels to cluster on, comma-separated; empty for every fluorescence channel. |
| `downsample` | `"none"` · `"spade"` · `"random"` |  | `"none"` |  | downsample before clustering: none, spade (density-dependent) or random; the rest take their nearest clustered event’s label. |
| `downsample_percent` | number |  | `10` | 0.01–100 | percent of events kept (SPADE: of those left after exclusion). |
| `downsample_exclude_percent` | number |  | `1` | 0–99 | SPADE exclude_pctile, percent: the sparsest events dropped as noise. |
| `spade_kernel_mult` | number |  | `5` | ≥ 0 | SPADE kernel_mult: density radius in median nearest-neighbour distances. |
| `spade_apprx_mult` | number |  | `1.5` | ≥ 0 | SPADE apprx_mult: events this close share a density count. |
| `spade_med_samples` | number |  | `2000` | ≥ 1 | SPADE med_samples: events sampled for the median nearest-neighbour distance. |
| `cluster_method` | `"kmeans"` · `"dbscan"` · `"hdbscan"` · `"phenograph"` · `"flowpeaks"` · `"samspectral"` · `"spectral"` · `"mclust"` · `"xshift"` |  | `"phenograph"` |  | the clustering method. |
| `seed` | number |  | `42` |  | R set.seed (k-means, PhenoGraph, SamSPECTRAL, mclust subset). |
| `kmeans_centers` | number |  | `8` | ≥ 1 | k-means centers. |
| `kmeans_algorithm` | `"Hartigan-Wong"` · `"Lloyd"` · `"Forgy"` · `"MacQueen"` |  | `"Hartigan-Wong"` |  | k-means algorithm. |
| `kmeans_nstart` | number |  | `1` | ≥ 1 | k-means random starts (nstart). |
| `kmeans_max_iter` | number |  | `10` | ≥ 1 | k-means iter.max. |
| `dbscan_eps` | number |  | `0.05` | ≥ 0 | DBSCAN radius on the display scale. |
| `dbscan_min_samples` | number |  | `5` | ≥ 1 | DBSCAN core neighbours. |
| `hdbscan_min_cluster_size` | number |  | `50` | ≥ 2 | HDBSCAN min_cluster_size. |
| `hdbscan_min_samples` | number |  |  | ≥ 1 | HDBSCAN min_samples; empty means min_cluster_size. |
| `hdbscan_method` | `"eom"` · `"leaf"` |  | `"eom"` |  | HDBSCAN cluster_selection_method. |
| `hdbscan_allow_single` | boolean |  | `false` |  | HDBSCAN allow_single_cluster. |
| `pheno_k` | number |  | `30` | ≥ 2 | PhenoGraph nearest neighbours. |
| `pheno_community` | `"louvain"` · `"leiden"` |  | `"louvain"` |  | PhenoGraph community search. |
| `pheno_resolution` | number |  | `1` | ≥ 0 | PhenoGraph resolution. |
| `pheno_iterations` | number |  | `2` |  | Leiden n_iterations; negative iterates until stable. |
| `flow_peaks_tol` | number |  | `0.1` | 0–1 | flowPeaks tol. |
| `flow_peaks_h0` | number |  | `1` | ≥ 0 | flowPeaks h0. |
| `flow_peaks_h` | number |  | `1.5` | ≥ 0 | flowPeaks h. |
| `sam_sigma` | number |  | `200` | ≥ 1 | SamSPECTRAL normal.sigma. |
| `sam_separation` | number |  | `0.7` | 0–1 | SamSPECTRAL separation.factor. |
| `sam_m` | number |  | `500` | ≥ 10 | SamSPECTRAL representatives (m). |
| `spectral_clusters` | number |  | `8` | ≥ 2 | spectral clustering n_clusters. |
| `spectral_neighbors` | number |  | `10` | ≥ 2 | spectral clustering n_neighbors (the event itself counted). |
| `mclust_min_g` | number |  | `1` | ≥ 1 | mclust fewest components (G from). |
| `mclust_max_g` | number |  | `9` | ≥ 1 | mclust most components (G to). |
| `mclust_model` | `"all"` · `"EII"` · `"VII"` · `"EEI"` · `"VEI"` · `"EVI"` · `"VVI"` · `"EEE"` · `"VEE"` · `"EVE"` · `"VVE"` · `"EEV"` · `"VEV"` · `"EVV"` · `"VVV"` |  | `"VVI"` |  | mclust covariance model (modelNames): EII, VII spherical; EEI, VEI, EVI, VVI diagonal; EEE, VEE, EVE, VVE, EEV, VEV, EVV, VVV ellipsoidal; 'all' compares them by BIC. |
| `mclust_start` | `"VVV"` · `"EII"` |  | `"VVV"` |  | mclust initial hierarchy: 'VVV' is mclust's default (hcModelName VVV, hcUse SVD), 'EII' the spherical Ward start on the raw channels (hcModelName EII, hcUse VARS). |
| `xshift_k` | number |  | `30` | ≥ 3 | X-shift K (density neighbours). |
| `xshift_nsize` | number |  | `0` | ≥ 0 | X-shift neighbours searched for a denser parent; 0 is automatic. |
| `trajectory_channels` | string |  | `""` |  | channels Slingshot runs in, comma-separated; empty for the clustered channels (every channel but time for populations). |
| `max_events` | number |  | `3000` | ≥ 0 | events drawn at most by R's sample() (0 keeps all). |
| `trajectory_seed` | number |  | `1` |  | R set.seed before the draw. |
| `start_clus` | string |  | `""` |  | the root cluster ('Cluster 3', or a population's name); empty lets Slingshot choose. |
| `end_clus` | string |  | `""` |  | comma-separated clusters forced to be lineage ends. |
| `dist_method` | `"slingshot"` · `"simple"` · `"scaled.full"` · `"scaled.diag"` |  | `"slingshot"` |  | the distance between cluster centres. |
| `omega` | `"off"` · `"auto"` · `"fixed"` |  | `"off"` |  | an outgroup cluster: off, at omega_scale × the median edge, or at omega_value. |
| `omega_value` | number |  | `1` | ≥ 0 | the fixed outgroup distance. |
| `omega_scale` | number |  | `1.5` | ≥ 0 | the automatic outgroup multiple of the median edge. |
| `shrink` | number |  | `1` | ≥ 0 | shrinkage toward the average curve, 0 to 1. |
| `extend` | `"y"` · `"n"` · `"pc1"` |  | `"y"` |  | how the initial curves extend past the end clusters. |
| `reweight` | boolean |  | `true` |  | reweight shared events. |
| `reassign` | boolean |  | `true` |  | reassign events between lineages. |
| `thresh` | number |  | `0.001` | ≥ 0 | the convergence threshold. |
| `maxit` | number |  | `15` | ≥ 1 | iterations at most. |
| `stretch` | number |  | `2` | ≥ 0 | how far curve ends are extrapolated. |
| `approx_points` | number |  | `-1` | ≥ -1 | curve points; -1 for Slingshot's default (150 over 150 events), 0 for every event. |
| `shrink_method` | `"cosine"` · `"tricube"` · `"gaussian"` · `"rectangular"` · `"triangular"` · `"epanechnikov"` · `"biweight"` · `"optcosine"` |  | `"cosine"` |  | the shrinkage kernel. |
| `allow_breaks` | boolean |  | `true` |  | let lineages that diverge early skip shrinkage there. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `lineages` | any |  | per lineage: its clusters in order, events on it, median and longest pseudotime |
| `mst` | any |  | the cluster tree: from, to, distance and gain per edge |
| `pseudotime` | any |  | per event used (0-based file index): its pseudotime and weight on every lineage (null off it) |
| `curves` | any |  | each lineage curve, its points in curve order, one value per channel |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fit_flow_cytometry_trajectory",
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

### flow_cytometry_kinetics

**Flow cytometry kinetics**: _How does this channel change over the acquisition, and what are its peak, slope and area in each time range?_

One channel over acquisition time (FlowJo Kinetics): median, mean, geometric mean, a percentile or % above a threshold in equal time bins, optionally gated above the threshold and smoothed; per time range the peak and its time, mean, slope, AUC and dt.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Events are stored with a time channel (else the event number stands for time, as in FlowJo).

**Does not:**
- FlowJo's Auto-Range (ranges fitted to peaks) is not built: its rule is unpublished.

**Validated:** against the reference implementation by 2 golden suites.

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
| `channel` | string |  |  |  | the channel followed (PnN, PnS or a derived name); empty for the first fluorescence channel. |
| `population` | string |  |  |  | the population; empty for all events. |
| `statistic` | `"median"` · `"mean"` · `"geomean"` · `"percentile"` · `"percentAbove"` |  | `"median"` |  | the statistic per time bin. Values: median (median), mean (mean), geomean (geometric mean), percentile (percentile), percentAbove (% above T). |
| `percentile` | number |  | `50` | 0–100 | for statistic = percentile. Only applies when statistic is percentile. |
| `kinetic_bins` | number |  | `100` | 2–1000 | equal time bins over the population’s time span. |
| `threshold` | `"none"` · `"absolute"` · `"percentileOfRange"` |  | `"none"` |  | the threshold T. Values: none (none), absolute (a value), percentileOfRange (a percentile of a time range). |
| `threshold_value` | number |  | `0` |  | T as a channel scale value. Only applies when threshold is absolute. |
| `threshold_percentile` | number |  | `95` | 0–100 | the percentile of the range that sets T. Only applies when threshold is percentileOfRange. |
| `threshold_range` | number |  | `1` | ≥ 1 | which range (1-based) the percentile is taken from. Only applies when threshold is percentileOfRange. |
| `above_threshold_only` | boolean |  | `false` |  | the statistic of events above T only. |
| `smoothing` | `"none"` · `"movingAverage"` · `"gaussian"` |  | `"none"` |  | curve smoothing. Values: none (none), movingAverage (moving average), gaussian (Gaussian). |
| `half_width` | number |  | `2` | ≥ 1 | smoothing window, ± bins (Gaussian σ = half of it). |
| `ranges` | string |  | `""` |  | time ranges `start-end` separated by `;`, in the time unit (seconds). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `bins` | any |  | per time bin: start, end, center, events, events used, value |
| `curve` | any |  | the displayed (smoothed) value per bin |
| `ranges` | any |  | per range: start, end, dt, peak, peak t, mean Y, slope, AUC |
| `threshold` | number |  | the threshold T used (0 when none) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "flow_cytometry_kinetics",
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

### fold_rna

**Fold RNA**: _What is the minimum-free-energy secondary structure of this sequence, and its free energy?_

Minimum-free-energy secondary structure (dot-bracket + ΔG) of an RNA/DNA sequence (Turner-2004).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Turner 2004 parameters at 37 °C with dangles=2, as ViennaRNA's default model.

**Does not:**
- One structure, the minimum; suboptimal and alternative structures are not reported.
- No pseudoknots.

**Not read from this result:** The answer is the minimum-free-energy structure and its energy, which the outputs carry; no panel shows this tool yet (a recorded surface gap), so there is no panel reading to carry.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seq` | string | **yes** |  |  | the RNA/DNA sequence (T read as U). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `dotBracket` | string or null |  | MFE structure (dot-bracket) |
| `dg` | number or null | kcal/mol | ΔG [kcal/mol] |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fold_rna",
  "arguments": {
    "seq": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### fragment_ions

**Fragment ions**: _Which theoretical fragment ions does this peptide give, at each charge?_

Theoretical MS/MS fragment ion ladder of a peptide: a, b, c from the N-terminus and x, y, z from the C-terminus, with neutral-loss and radical variants, at each charge up to a maximum (validated against pyteomics, cross-checked against OpenMS). Takes ProForma modification tags (a signed mass, a Unimod name, or UNIMOD:accession) on residues and termini.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Standard backbone cleavage series with the neutral losses and radical variants requested.

**Does not:**
- A complete theoretical ladder: a real spectrum shows a subset, with intensities this does not predict.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string | **yes** |  |  | peptide: one-letter residues, optionally ProForma tags, e.g. [TMT6plex]-PEPTM[Oxidation]IDE or [+229.162932]-PEPTM[+15.994915]IDE. |
| `ionTypes` | (`"M"` · `"M-H2O"` · `"M-NH3"` · `"a"` · `"a+1"` · `"a-H2O"` · `"a-NH3"` · `"b"` · `"b-H2O"` · `"b-NH3"` · `"c"` · `"c-1"` · `"c-dot"` · `"c+1"` · `"c+2"` · `"c-H2O"` · `"c-NH3"` · `"x"` · `"x+1"` · `"x-H2O"` · `"x-NH3"` · `"y"` · `"y-H2O"` · `"y-NH3"` · `"z-1"` · `"z"` · `"z-dot"` · `"z+1"` · `"z+2"` · `"z+3"` · `"z-H2O"` · `"z-NH3"`)[] |  | `["b", "y"]` |  | ion series to generate. |
| `maxCharge` | number |  | `1` |  | highest fragment charge (every charge from 1 up to it). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `ions` | any |  | one row per fragment: ionType, index (residues), charge, name, m/z |
| `count` | number or null |  | fragments generated |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fragment_ions",
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

### gc_content

**GC content**: _What is this sequence's GC fraction, overall or along a sliding window?_

GC fraction of the subject — whole-sequence, or a sliding window profile (DnaChisel).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Ambiguity codes are counted as DnaChisel counts them.

**Does not:**
- A window profile depends on the window size, which the answer states.

**Not read from this result:** The answer is the GC fraction (and its window profile), which the outputs carry; the editor shows it as a readout and writes no reading over it.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `window` | number |  |  | 10–5000 | sliding-window size; unset = one value for the whole sequence. In bp. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `gc` | number |  | GC fraction over the whole sequence (0–1) |
| `profile` | any |  | per-window GC fractions (only when `window` is set) |
| `plot` | object or null |  | the windowed GC profile as a plot, by window centre (only when `window` is set) |
| `plot.x` | number[] |  |  |
| `plot.series` | object[] |  |  |
| `plot.series[].name` | string |  |  |
| `plot.series[].y` | (number or null)[] |  |  |
| `plot.xLabel` | string |  |  |
| `plot.yLabel` | string |  |  |
| `plot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `plot.title` | string |  |  |
| `plot.rules` | object[] |  |  |
| `plot.rules[].y` | number |  |  |
| `plot.rules[].label` | string |  |  |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "gc_content",
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

### genotype_pca

**Genotype PCA**: _What population structure do these genotypes show in their principal components?_

Principal components of a call set's genotypes, the population-structure picture: biallelic sites above a minor-allele count, LD-pruned by sliding windows, scaled per site (Patterson, standard or centring) and decomposed; every sample's coordinates with its population, and the variance each component explains (scikit-allel pca). Validated on 1000 Genomes phase 3 APOL1, all 2,504 samples.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Biallelic sites above the minor-allele count, LD-pruned, scaled as chosen.

**Does not:**
- Components are axes of variance, not populations; their sign and order are not meaningful beyond the variance explained.
- Relatedness and uneven sampling can dominate the leading components.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `vcf` | string | **yes** |  |  | the call set as VCF text (a .vcf, or a .vcf.gz already decompressed); every record's GT is read, ploidy 2. |
| `populations` | string |  |  |  | a sample table: a header row with a `sample` column and one or more grouping columns (tab-separated, as 1000 Genomes' .panel). Samples it does not list belong to no group. |
| `groupBy` | string |  | `""` |  | which column of the sample table groups the samples; empty is its first grouping column. |
| `minMac` | number |  | `3` | ≥ 1 | keep biallelic sites whose REF and first ALT are each seen at least this many times. |
| `prune` | boolean |  | `true` |  | drop sites in LD before the decomposition (locate_unlinked), as scikit-allel's PCA assumes. |
| `pruneSize` | number |  | `100` | ≥ 2 | pruning window, in sites. Only applies when prune is true. |
| `pruneStep` | number |  | `20` | ≥ 1 | sites the pruning window advances. Only applies when prune is true. |
| `pruneThreshold` | number |  | `0.1` | 0–1 | prune the later site of a pair whose Rogers–Huff r² exceeds this. Only applies when prune is true. |
| `nComponents` | number |  | `10` | ≥ 1 | components to report. |
| `scaler` | `"patterson"` · `"standard"` · `"center"` |  | `"patterson"` |  | per-site scaling before the decomposition: Patterson divides the centred dosage by √(p(1−p)); standard by its standard deviation; center only centres. Values: patterson (Patterson (√(p(1−p)))), standard (Standard deviation), center (Centre only). |
| `precision` | `"float64"` · `"float16"` |  | `"float64"` |  | float64, or float16: scikit-allel's own path when handed integer genotypes, which rounds the scaled matrix to half precision. Values: float64 (Double precision), float16 (Half precision (as scikit-allel on integer genotypes)). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `coords` | any |  | one row per sample: sample, its group, and its coordinate on each component |
| `explainedVarianceRatio` | any |  | the share of variance each reported component explains |
| `explainedVariance` | any |  | the variance each reported component explains, in the data's own units (the eigenvalues) |
| `sites` | any |  | how many sites qualified, how many pruning kept, and their positions |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "genotype_pca",
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

### hmm_build

**HMM build**: _What profile HMM does hmmbuild make of this alignment, and with what E-value statistics?_

Build a profile HMM from aligned sequences on this machine, as HMMER 3.4's hmmbuild builds one: columns whose weighted residue fraction clears `symfrac` become match states, rows are Henikoff position-based weighted so near-duplicates do not outvote a divergent member, the counts are entropy-weighted down to a target information per position, and the model is calibrated for E-values by hmmbuild's own simulation. Returns the HMMER3/f text, ready for hmm_search or hmmscan or to keep as a `.hmm`. Wire align_sequences' `alignedSequences` into `alignment`, or name a Stockholm, Clustal or aligned-FASTA file in `alignment_file`.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- The rows are a real alignment: equal length, homologous column for column.
- hmmbuild’s default build path: symfrac column assignment, PB weighting, entropy-weighted effective count, mixture Dirichlet priors.

**Does not:**
- Above 50,000 rows hmmbuild switches to subsampled weights; that path is refused, not approximated.
- Calibration simulates random sequences: a different seed gives slightly different statistics, as in hmmbuild.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `alignment` | object[] |  |  |  | the aligned rows as `{ name, aligned }`, gaps included: wire align_sequences’ `alignedSequences` here. Rows of different lengths are refused as unaligned. |
| `alignment_file` | string |  |  |  | or an alignment file, by name, from the project or the `_files` sent with the call: Stockholm, Clustal, PHYLIP, MSF or aligned FASTA, read by the same reader the alignment tab opens it with. |
| `name` | string |  | `"profile"` |  | the model’s name, written on its NAME line. |
| `alphabet` | `"auto"` · `"amino"` · `"DNA"` · `"RNA"` |  | `"auto"` |  | `auto` reads the rows the way Easel does. Set it when a short alignment is read wrongly. Values: auto (Auto (Easel’s rule)), amino (Protein), DNA (DNA), RNA (RNA). Advanced. |
| `symfrac` | number |  | `0.5` | 0–1 | hmmbuild --symfrac: a column becomes a match state when this weighted fraction of rows carry a residue there rather than a gap. |
| `fragthresh` | number |  | `0.5` | 0–1 | hmmbuild --fragthresh: a row spanning less than this fraction of the alignment is a fragment, and its leading and trailing gaps are read as missing data rather than deletions. |
| `weighting` | `"pb"` · `"none"` |  | `"pb"` |  | `pb` is Henikoff position-based weighting (hmmbuild’s default), so twenty near-identical rows do not outvote one divergent member; `none` counts every row once. Values: pb (Position-based (Henikoff)), none (Equal). |
| `effn` | `"entropy"` · `"none"` · `"set"` |  | `"entropy"` |  | `entropy` scales the counts until the model carries `ere` bits per position, which makes it a family model rather than a memory of this alignment; `none` uses the rows as counted; `set` uses `eset`. Values: entropy (Entropy-weighted), none (Actual count), set (Fixed (eset)). |
| `ere` | number |  | `0` | ≥ 0 | hmmbuild --ere: the target mean relative entropy in bits per position. 0 takes hmmbuild’s alphabet default (0.59 protein, 0.62 nucleic). Only applies when effn is entropy. |
| `esigma` | number |  | `0` | ≥ 0 | hmmbuild --esigma: the entropy target’s small-model correction. 0 takes hmmbuild’s default. Only applies when effn is entropy. Advanced. |
| `eset` | number |  |  | ≥ 0 | hmmbuild --eset: the effective sequence count to use. Only applies when effn is set. |
| `calibrate` | boolean |  | `true` |  | fit E-value statistics by simulation, as hmmbuild does. Off, the model has bit scores and no E-values, and hmmscan refuses it. |
| `seed` | number |  | `42` | ≥ 1 | hmmbuild --seed: the simulation is reproducible, and the same seed gives the same statistics. Only applies when calibrate is true. |
| `EmN` | number |  | `200` | ≥ 2 | hmmbuild --EmN: random sequences the MSV fit is made over. Only applies when calibrate is true. Advanced. |
| `EmL` | number |  | `200` | ≥ 10 | hmmbuild --EmL: their length, in residues. Only applies when calibrate is true. Advanced. |
| `EvN` | number |  | `200` | ≥ 2 | hmmbuild --EvN: random sequences the Viterbi fit is made over. Only applies when calibrate is true. Advanced. |
| `EvL` | number |  | `200` | ≥ 10 | hmmbuild --EvL: their length, in residues. Only applies when calibrate is true. Advanced. |
| `EfN` | number |  | `200` | ≥ 2 | hmmbuild --EfN: random sequences the Forward fit is made over. Only applies when calibrate is true. Advanced. |
| `EfL` | number |  | `100` | ≥ 10 | hmmbuild --EfL: their length, in residues. Only applies when calibrate is true. Advanced. |
| `Eft` | number |  | `0.04` | 0–1 | hmmbuild --Eft: the tail mass the Forward exponential is fitted to. Only applies when calibrate is true. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hmm` | string |  | the model as HMMER3/f text: wire it into hmm_search’s `profile_text`, or keep it as a `.hmm` |
| `profile` | any |  | the model built: name, match states, alphabet, effective sequence count, whether it carries E-value statistics |
| `matchColumns` | any |  | the alignment columns that became match states, 1-based |
| `weights` | any |  | each row’s relative weight, in input order |
| `fragments` | any |  | rows the fragment rule treated as partial sequences |
| `meanRelativeEntropy` | number | bits | mean relative entropy per match state, in bits (hmmbuild’s re/pos) |
| `stats` | any |  | the fitted MSV, Viterbi and Forward mu and lambda; absent when calibration was off |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "hmm_build",
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

### hmm_search

**HMM search**: _How well does each sequence score against this profile HMM, where does the model match, and does it clear the family’s own gathering cutoff?_

Score sequences against ONE profile HMM on this machine, as hmmsearch scores a family against a set: per sequence a Forward and a Viterbi bit score, an E-value when the model is calibrated, every domain with its model and sequence span and its three-line alignment, and the family's own gathering-cutoff verdict when the model publishes one (Pfam does). The model is a HMMER3 `.hmm` in the project or sent in `_files`, a Pfam accession fetched from InterPro, or the text `hmm_build` emits. Nothing but a Pfam fetch leaves the machine. Use hmmscan instead to ask which of MANY models a protein carries.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Plan7 Viterbi and Forward under HMMER 3.4’s reference (generic) DP, in local or glocal mode.
- The E-value is the model’s own Forward statistics scaled by Z, the size of the database.

**Does not:**
- Scores every sequence with the reference DP and reports every one, however poor: it runs none of hmmsearch’s acceleration filters, so a sequence the real program would drop at the MSV filter is still scored here.
- A model without STATS lines has bit scores and no E-value.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** PF00069_Pkinase.hmm

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `profile` | string |  |  |  | the `.hmm` file to score against, by name, from the project or the `_files` sent with the call. Left empty with no `profile_text` or `pfam`, the one `.hmm` present is used, and several are refused by name. |
| `profile_text` | string |  |  |  | the model itself as HMMER3 text; wire `hmm_build`’s `hmm` here to screen with a model you just built. Advanced. |
| `pfam` | string |  |  |  | a Pfam accession (PF and five digits): the family’s current HMM is fetched from InterPro for this run. Its gathering cutoff comes with it. |
| `sequences` | string[] |  |  |  | the sequences to screen: wire upstream records or sequences, or list library documents. A multi-record file named whole contributes every record. Gaps are removed before scoring. |
| `include_subject` | boolean |  | `true` |  | also screen the open or wired record (a protein record by its residues). |
| `mode` | `"local"` · `"glocal"` |  | `"local"` |  | `local` finds the model anywhere in a sequence, as hmmsearch does: right for a domain inside a longer protein. `glocal` makes the whole model align, which a full-length member of the family can and a fragment cannot. Values: local (Local (hmmsearch)), glocal (Glocal (whole model)). |
| `multihit` | boolean |  | `true` |  | allow several separate domains in one sequence (the J state). Off allows one: right when a family occurs once per protein. |
| `Z` | number |  | `0` | ≥ 0 | the database size each E-value is scaled by. 0 takes the number of sequences screened, which is what hmmsearch does with the database it searched; set it to compare against a larger search. |
| `alphabet` | `"auto"` · `"protein"` · `"nucleotide"` |  | `"auto"` |  | what the sequences are. `auto` reads them the way HMMER does (Easel’s composition rule). Set it when a short or unusual set is read wrongly: every DNA base is also an amino-acid letter, so a nucleotide set against a protein model scores without complaint and means nothing. Values: auto (Auto (Easel’s rule)), protein (Protein), nucleotide (Nucleotide). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | one row per sequence, best Forward score first: name, length, forwardBits, viterbiBits, forwardEvalue (absent for an uncalibrated model), membership against the gathering cutoff, and each domain’s seqFrom/seqTo (1-based) and hmmFrom/hmmTo with its alignment |
| `members` | number |  | sequences at or above the family’s gathering cutoff (0 when the model publishes none) |
| `profile` | any |  | the model screened against: name, accession, match states, alphabet, cutoffs, whether it carries E-value statistics |
| `count` | number |  | sequences screened |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "hmm_search",
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

### hmmscan

**Hmmscan**: _Which of these profile HMMs does the protein carry, in which domains, with what E-values?_

Which of MANY profile HMMs does this protein carry? Runs HMMER 3.4's hmmscan pipeline on this machine: the MSV, bias, Viterbi and Forward filters per model, domain definition by posterior decoding (several domains of one model are split, as hmmscan splits them), null2-corrected domain scores, and hmmscan's reporting thresholds. Every reported model with its bit score and E-value, every domain with its envelope, its alignment span on the query and the model, its independent and conditional E-values, and the family's gathering-cutoff verdict. The database is every `.hmm` named (each file may hold many models; empty takes every `.hmm` in the project or `_files`), plus any Pfam families fetched by accession. Models must carry E-value statistics, as Pfam's do and hmm_build's calibrated ones do.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- HMMER 3.4 hmmscan defaults unless changed: -E 10, --domE 10, --F1 0.02, --F2 1e-3, --F3 1e-5, bias filter and null2 on.
- E-values are scaled by the number of models scanned, so a larger database makes every E-value larger.

**Does not:**
- Answers only against the models given: an absent family is not an absent domain. A full Pfam-A scan needs the full Pfam-A file.
- Reporting is by E-value; gathering cutoffs are reported beside each hit, not applied as --cut_ga would.

**Validated:** against the reference implementation by 2 golden suites.

**Reads bundled data:** PF00069_Pkinase.hmm

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string |  |  |  | the query protein, one-letter codes. Empty takes the open record when it is a protein. |
| `profiles` | string[] |  |  |  | `.hmm` files to scan against, by name, from the project or the `_files` sent with the call; each may hold many models. Empty takes every `.hmm` there. |
| `pfam` | string |  |  |  | Pfam accessions to fetch from InterPro and add to the database, comma-separated (PF00069,PF00017). |
| `E` | number |  | `10` | ≥ 0 | hmmscan -E: report models with an E-value at or below this. |
| `domE` | number |  | `10` | ≥ 0 | hmmscan --domE: report domains with a conditional E-value at or below this. |
| `F1` | number |  | `0.02` | 0–1 | hmmscan --F1: the MSV filter’s P-value threshold. Advanced. |
| `F2` | number |  | `0.001` | 0–1 | hmmscan --F2: the Viterbi filter’s P-value threshold. Advanced. |
| `F3` | number |  | `1e-05` | 0–1 | hmmscan --F3: the Forward filter’s P-value threshold. Advanced. |
| `alphabet` | `"auto"` · `"protein"` · `"nucleotide"` |  | `"auto"` |  | what the query is. `auto` reads them the way HMMER does (Easel’s composition rule). Set it when a short or unusual set is read wrongly: every DNA base is also an amino-acid letter, so a nucleotide set against a protein model scores without complaint and means nothing. Values: auto (Auto (Easel’s rule)), protein (Protein), nucleotide (Nucleotide). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | every model that passed the pipeline, best first: model, accession, bits, evalue, reported, aboveGathering, and its domains (envFrom/envTo, aliFrom/aliTo on the query, hmmFrom/hmmTo, bits, iEvalue, cEvalue, reported, aboveGathering) |
| `domains` | any |  | the reported domains alone, in query order, each with its model name: the domain architecture |
| `reported` | number |  | models reported |
| `Z` | number |  | models scanned, which every E-value is scaled by |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "hmmscan",
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

### impute_flow_cytometry_infinity

**Impute flow cytometry infinity**: _What would every Infinity marker of the screen read on each cell, from the backbone alone?_

Infinity Flow backbone imputation for a massively parallel cytometry screen (LEGENDScreen-style): the project's FCS wells share a backbone panel and each carries one exploratory antibody; per well a regression of the exploratory channel on the logicle-transformed, per-well-scaled backbone is fitted on a random half, and every well's model imputes its marker on held-out events of every well, with isotype background correction.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Every well shares the same backbone panel; the backbone explains the exploratory marker the same way in every well.

**Does not:**
- Linear (any polynomial degree), SVM and XGBoost models; infinityFlow’s keras neural-network fitter is not ported.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `samples` | string |  | `""` |  | comma-separated FCS wells; empty for every project FCS file. |
| `sample_sheet` | string |  | `""` |  | the project sample sheet naming each well’s target and isotype. |
| `target_column` | string |  | `"target"` |  | sheet column with each well’s Infinity target. |
| `isotype_column` | string |  | `""` |  | sheet column with each well’s isotype; empty for no background correction. |
| `exploratory` | string |  | `""` |  | the exploratory channel ($PnN). |
| `backbone` | string |  | `""` |  | comma-separated backbone channels ($PnN); empty for all but time and the exploratory. |
| `degree` | number |  | `1` | ≥ 1 | polynomial degree of the linear model. |
| `svm` | boolean |  | `false` |  | also fit the eps-regression SVM. |
| `svm_cost` | number |  | `1` |  | SVM cost. |
| `xgboost` | boolean |  | `false` |  | also fit XGBoost, infinityFlow’s default model. |
| `xgb_rounds` | number |  | `500` | ≥ 1 | XGBoost boosting rounds. |
| `xgb_eta` | number |  | `0.05` |  | XGBoost learning rate. |
| `xgb_max_depth` | number |  | `6` | 1–15 | XGBoost maximum tree depth. |
| `input_events` | number |  | `0` | ≥ 0 | events kept per well (0 all). |
| `prediction_events` | number |  | `1000` | ≥ 1 | held-out events imputed per well. |
| `sample_seed` | number |  | `123` |  | the R seed. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `wells` | any |  | per well: target, isotype, events, training events, imputed events |
| `imputed` | any |  | per model: the imputed events’ well and, per target, imputed and background-corrected values |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "impute_flow_cytometry_infinity",
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

### isotope_envelope

**Isotope envelope**: _What coarse isotope pattern does this peptide or formula show: the heights and masses of M, M+1, M+2 and beyond?_

Coarse isotope pattern of a peptide or of an elemental formula (C29H31N7O, as a compound's formula reads): the relative heights and masses of its M, M+1, M+2 … peaks as an instrument that does not resolve isotopic fine structure sees them, computed by per-element convolution from natural abundances (validated against OpenMS).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Natural isotope abundances, convolved per element, as an instrument that does not resolve fine structure sees it.

**Does not:**
- Coarse: isotopic fine structure is deliberately not resolved.
- No instrument response, resolution or detector saturation.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | peptide, plain one-letter residues; give this or `formula`. |
| `formula` | string |  |  |  | elemental formula of a neutral compound (C29H31N7O; isotopes as C[13]); give this or `sequence`. |
| `maxIsotope` | number |  | `6` |  | peaks to keep (M counts as one); 0 keeps every peak. |
| `charge` | number |  | `0` |  | protons added; masses then include them (divide by the charge for m/z). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `peaks` | any |  | one row per peak: isotope index, mass, relative abundance (sums to 1) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "isotope_envelope",
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

### isotopic_composition

**Isotopic composition**: _Which isotopic composition is this peptide most likely to carry, and how abundant is it?_

The most probable isotopic composition of a peptide (e.g. how many 13C atoms it most likely carries) and that composition's relative abundance, from natural isotope abundances (validated against pyteomics).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Natural terrestrial isotope abundances.

**Does not:**
- The single most probable composition, not the whole distribution.
- Labelled samples are not natural-abundance, so the answer does not apply to them.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string | **yes** |  |  | peptide, plain one-letter residues. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `composition` | any |  | element -> isotope mass number -> atom count |
| `abundance` | number or null |  | relative abundance of that composition (0-1) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "isotopic_composition",
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

### linkage_disequilibrium

**Linkage disequilibrium**: _How much linkage disequilibrium is there between each pair of biallelic sites, and which sites survive pruning?_

Linkage disequilibrium between every pair of biallelic sites of a call set: the dosage correlation r of Rogers and Huff (scikit-allel), or haplotype r² and D′ from the maximum-likelihood two-locus haplotype frequencies (PLINK 1.9 --r2 dprime-signed), plus LD pruning by sliding windows (scikit-allel locate_unlinked). Validated on every pair of 1000 Genomes phase 3 APOL1 sites.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Rogers and Huff's dosage correlation needs no phase; haplotype r-squared and D-prime assume the maximum-likelihood two-locus frequencies.
- Samples are from one population: structure inflates LD.

**Does not:**
- LD is a property of this sample, not of the species.
- Pruning depends on the window and threshold, which the answer states.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `vcf` | string | **yes** |  |  | the call set as VCF text (a .vcf, or a .vcf.gz already decompressed); every record's GT is read, ploidy 2. |
| `populations` | string |  |  |  | a sample table: a header row with a `sample` column and one or more grouping columns (tab-separated, as 1000 Genomes' .panel). Samples it does not list belong to no group. |
| `groupBy` | string |  | `""` |  | which column of the sample table groups the samples; empty is its first grouping column. |
| `group` | string |  | `""` |  | compute over this group's samples only; empty is every sample. |
| `estimator` | `"rogersHuff"` · `"haplotype"` |  | `"rogersHuff"` |  | rogersHuff: r between alt-allele dosages, no phasing (scikit-allel). haplotype: r² and D′ from the maximum-likelihood haplotype frequencies (PLINK 1.9). Values: rogersHuff (Rogers–Huff r (genotype dosages)), haplotype (Haplotype r² and D′ (maximum likelihood)). |
| `minMac` | number |  | `1` | ≥ 1 | keep sites where REF and the first ALT are each seen at least this many times (scikit-allel is_biallelic_01 min_mac). |
| `start` | number |  | `0` | ≥ 0 | first position (1-based) of the window; 0 is the first site. |
| `end` | number |  | `0` | ≥ 0 | last position (1-based) of the window; 0 is the last site. |
| `maxSites` | number |  | `1000` | ≥ 2 | refuse more sites than this: the pair count grows with its square. |
| `pruneSize` | number |  | `100` | ≥ 2 | LD pruning window, in sites (locate_unlinked size). |
| `pruneStep` | number |  | `20` | ≥ 1 | sites the pruning window advances (locate_unlinked step). |
| `pruneThreshold` | number |  | `0.1` | 0–1 | prune the later site of a pair whose Rogers–Huff r² exceeds this (locate_unlinked threshold). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sites` | any |  | the sites compared, in order: index into the call set, chrom, pos, ref, alt, and whether pruning kept it |
| `pairs` | any |  | condensed upper triangle, pair (i, j > i) in row order: r (rogersHuff) or [r², D′] (haplotype), null where a site is monomorphic among the samples called at both |
| `summary` | any |  | sites, pairs, mean r², pairs at r² ≥ 0.8, pruning kept, and the strongest pairs |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "linkage_disequilibrium",
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

### load_trace

**Load trace**: _What bases, qualities and trim bounds does this Sanger trace carry?_

Read a Sanger trace (.ab1 / .scf / .ztr) from this project and hand its BASE CALLS onward as a record, with the per-base quality and the trim bounds beside them. This is what makes a sequencing read a pipeline input: verify it against a reference, align it, gate on its quality. The trace SIGNAL stays here — a record crosses a wire as bases, and a peak cannot be written as one.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The calls the instrument wrote into the file.

**Does not:**
- Reads the file's own calls; re-calling is call_bases_from_trace.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace file to read: its name (`read_F.ab1`) or its project file id. A file id is project-specific, so a template ships this unset. |
| `reverse_complement` | boolean |  | `false` |  | read it on the other strand. A reverse primer's trace is the reverse complement of the strand you are verifying, and a name ending _R is the convention for it. |
| `trim` | boolean |  | `true` |  | emit the quality-trimmed read rather than the whole call list. The bounds are the sliding-window mean-phred bounds the chromatogram panel trims by, so panel and pipeline cut at the same base. |
| `min_quality` | number |  | `20` | 0–60 | the mean phred a window must reach to be kept when trimming. Only applies when trim is true. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the read as a linear record, ready for any downstream step |
| `sequence` | string |  | its bases, trimmed when trimming is on |
| `length` | number |  | how many bases that is |
| `readQuality` | number |  | the read's own quality: the phred of its MEAN ERROR PROBABILITY, which is what seqkit's --avg-qual reports. Wire THIS into a gate to stop a bad read early |
| `expectedAccuracy` | number | % | the same number as a percentage of bases expected to be correct |
| `meanQuality` | number |  | the ARITHMETIC mean of the per-base phred, which is what FastQC plots. Always the higher of the two, because a phred score is a log of an error rate: keep it for comparison with other tools, gate on readQuality |
| `qualities` | any |  | per-base phred, parallel to the bases |
| `qualityPlot` | object or null |  | per-base phred as a plot along the read, with Q20 (1 error in 100) marked |
| `qualityPlot.x` | number[] |  |  |
| `qualityPlot.series` | object[] |  |  |
| `qualityPlot.series[].name` | string |  |  |
| `qualityPlot.series[].y` | (number or null)[] |  |  |
| `qualityPlot.xLabel` | string |  |  |
| `qualityPlot.yLabel` | string |  |  |
| `qualityPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `qualityPlot.title` | string |  |  |
| `qualityPlot.rules` | object[] |  |  |
| `qualityPlot.rules[].y` | number |  |  |
| `qualityPlot.rules[].label` | string |  |  |
| `ambiguous` | number |  | how many calls are not A, C, G or T: the mixed positions |
| `trace` | any |  | what the FILE says about itself: format, instrument comments, call count, trim bounds. Not the signal, which cannot ride a wire |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "load_trace",
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

### mask_sequence

**Mask sequence**: _Which stretches of this sequence should a similarity search not seed on?_

Mask the parts of a sequence a similarity search should not seed on, using BLAST's own three maskers: DUST for compositionally biased DNA (poly-A, simple repeats), SEG for the protein equivalent, and WindowMasker for repeats that are ordinary in composition but occur far more often than chance allows in the sequences given. Emits the soft- and hard-masked sequences and the masked intervals, so a pipeline can mask before it searches rather than explaining an empty hit table afterwards.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- DUST, SEG and WindowMasker as BLAST+ implements them, at the levels given.

**Does not:**
- Masks low-complexity and over-represented sequence; it does not identify what the sequence is.

**Not read from this result:** A transform: the sequence with the named spans masked, with nothing inferred; the Contamination panel's reading is on the screen that found them.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `masker` | `"dust"` · `"seg"` · `"windowmasker"` |  | `"dust"` |  | which masker. dust and windowmasker take DNA; seg takes protein. Values: dust (DUST · biased DNA composition), seg (SEG · biased protein composition), windowmasker (WindowMasker · over-represented DNA). |
| `sequence` | string |  |  |  | the sequence to mask. Wire a record or a sequence output, or paste it. Left empty, the open record is used. |
| `context` | string[] |  |  |  | WindowMasker only: the other sequences whose statistics define 'over-represented'. Its thresholds come from this SET, so wiring one plasmid asks whether a stretch is unusual for that plasmid, not for the organism. Only applies when masker is windowmasker. |
| `level` | number |  | `20` | 1–100 | DUST's T. Higher masks less. Only applies when masker is dust. |
| `window` | number |  | `0` | 0–256 | the scored window's width. 0 takes each masker's own default. |
| `locut` | number |  | `2.2` | 0–4.322 | SEG's K1, the trigger complexity in bits. Only applies when masker is seg. |
| `hicut` | number |  | `2.5` | 0–4.322 | SEG's K2, the extension complexity in bits. Only applies when masker is seg. |
| `unit_size` | number |  | `0` | 0–16 | WindowMasker's n-mer length. 0 derives it from the length of everything given, the way the tool does. Only applies when masker is windowmasker. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `masked` | string |  | the sequence soft-masked (lower case), which is what BLAST reads as masked |
| `hardMasked` | string |  | the sequence with the masked stretches replaced by N (or X for a protein) |
| `intervals` | any |  | the masked stretches, 0-based inclusive |
| `maskedFraction` | number |  | what share of the sequence was masked, 0 to 1. Wire into a $when to refuse a query that is mostly gone |
| `provenance` | any |  | the masker, the parameters it really used, and for WindowMasker the derived thresholds and the set they came from |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "mask_sequence",
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

### match_part_by_sequence

**Match part by sequence**: _Which published iGEM part carries exactly these bases?_

Identify a stretch of DNA by asking the iGEM Registry which published part carries exactly those bases, and hand back that part's own description, Sequence-Ontology role, literature citation and license. The match is decided by comparing bases, never by a name — so a pipeline can label a fragment it has assembled, or check that a feature really is the part it is called.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network; exact matches only.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string | **yes** |  |  | the bases to identify — a feature’s span, an assembled fragment, a pasted oligo. |
| `name` | string |  |  |  | a name to narrow the candidates by (a feature name, or a part id like BBa_R0040). It only narrows: the bases decide the match. Leave it empty to compare every candidate of this exact length, which is slower and can be far more requests. |
| `cap` | number |  | `40` | 1–200 | most candidate sequences to fetch and compare before stopping and saying so. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `matched` | boolean |  | whether any compared part carries these exact bases |
| `part` | string |  | the best match’s registry id, exact before reverse-complement |
| `title` | string |  | the registry’s own short title for that part |
| `description` | string |  | the registry’s own prose — the half a coordinate cannot tell you |
| `strand` | string |  | `exact` when the bases agree as given, `reverse-complement` when they agree flipped |
| `role` | string |  | its Sequence-Ontology role, as the registry files it |
| `licence` | string |  | the SPDX identifier the registry states for that part |
| `page` | string |  | the registry page, so the claim can be checked without us |
| `matches` | any |  | every part that carries these bases — several may, and the registry keeps them apart |
| `coverage` | any |  | what was and was not compared: the population at this length, the candidates the narrowing produced, how many were read back, and whether the cap stopped it. A null answer is only as strong as this. |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "match_part_by_sequence",
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

### miqe_checklist

**MIQE checklist**: _Which MIQE 2.0 items does a qPCR paper provide, and where, or why are they omitted?_

The MIQE 2.0 checklist for a qPCR paper (Bustin et al. 2025, Clin Chem 71:634, Table 1): every item in its five sections, with your answers. Each answer is Provided (yes or no) and Description/Justification: where in the article when yes, why it is omitted when no; an answer missing that is named. Returns every row, the counts and a TSV under the paper's headers. Run with no answers to read the item ids. Digital PCR has its own checklist, dMIQE 2020.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Records the author's answers; it does not check the paper.
- Digital PCR is dMIQE 2020's checklist, not this one.

**No scientific claim:** Lays the author's own answers against MIQE 2.0's published items; it computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `answers` | object |  | `{}` |  | answers by item id, e.g. {"5.8": {"provided": "yes", "description": "Results, Table 2: standard curve over five tenfold dilutions"}, "3.5": {"provided": "no", "description": "DNase-treated RNA validated DNA-free"}}. Ids run section.item over the paper's order (1 Reagent preparation · 2 Sample preparation · 3 Reverse transcription · 4 qPCR protocol · 5 Data analysis). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rows` | any |  | one row per item, in the paper's order: section, id, item, footnotes, provided, description, and the gap footnote b would still send back |
| `answered` | number |  | items answered yes or no |
| `total` | number |  | items in the checklist |
| `incomplete` | number |  | answers without the location (yes) or reason (no) the checklist asks for |
| `tsv` | string |  | the checklist as tab-separated text under the paper's own column headers, for a journal submission |
| `notes` | any |  | the table's footnotes by letter, which qualify the items that carry them |
| `reading` | string |  | what is answered and what is still owed, generated from the answers |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "miqe_checklist",
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

### normalize_cytof_beads

**Normalize cytof beads**: _How much did the instrument's sensitivity drift over these acquisitions, and what are the counts with that drift taken out?_

CATALYST normCytof bead normalization of mass cytometry acquisitions in the project, together: the beads found in every file (positive on each bead channel of the kit, negative on DNA Ir191/Ir193, by debarcoding with an estimated cutoff, then trimmed to within a number of MADs of each channel's median), each bead channel smoothed by a running median over acquisition time, each bead's least-squares slope to the baseline (the beads' mean counts) interpolated over time, and every event's counts multiplied by its slope. Per file the events, beads and removed events; the slopes; the baseline.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Every acquisition was run with the same bead kit spiked in, so the beads are a constant signal over time.
- The files are acquisitions of one panel, normalized to one baseline.

**Does not:**
- Writing the normalized files is done from the panel; this door returns the beads, slopes and baseline.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `samples` | string |  | `""` |  | the acquisitions normalized together, by name or id, comma-separated; empty for every FCS file in the project. |
| `kit` | `"dvs"` · `"beta"` |  | `"dvs"` |  | the bead kit: EQ four-element beads (Ce140, Eu151, Eu153, Ho165, Lu175) or beta beads. Values: dvs (EQ four-element), beta (beta). |
| `k` | number |  | `500` | ≥ 1 | the running median's window in beads (made odd, capped at the bead count). |
| `trim` | number |  | `5` | ≥ 0 | beads further than this many MADs from their channel's median are not used. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `files` | any |  | per acquisition: its events, the beads found in it and the events removed with them |
| `baseline` | any |  | per bead channel, the beads' mean counts every acquisition was normalized to |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "normalize_cytof_beads",
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

### normalize_flow_cytometry_batch

**Normalize flow cytometry batch**: _Do the same populations sit at the same place on each channel across these samples, and if not, by how much must each be moved?_

flowStats gaussNorm batch normalization over project FCS files: per channel, each sample's density peaks (landmarks) are found, scored by sharpness and height, matched to base landmarks (the median of each landmark class across samples), and the sample's values shifted so its landmarks land on them, each shift spread by a Gaussian around its peak; values read as flowCore reads them (linear, uncompensated) or their log10, and events at a channel's instrument range left raw. Per channel the base landmarks; per sample the landmarks moved and its confidence.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Every sample shows the same populations as density peaks on each normalized channel; gaussNorm moves peaks, it cannot tell a missing population from a shifted one.

**Does not:**
- The normalized files are written to the project from the panel only; this door returns the landmarks and confidence.
- Values are not compensated first, as flowStats runs on the frames flowCore reads.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `samples` | string |  | `""` |  | the FCS files to normalize together, by name or id, comma-separated; empty for every FCS file in the project. |
| `channels` | string |  | `""` |  | the channels to normalize, comma-separated PnN; empty for every channel but scatter and time. |
| `max_lms` | number |  | `2` | 0–4 | flowStats max.lms: landmarks moved per channel; 0 leaves a channel as it is. |
| `landmark_scale` | `"log10"` · `"linear"` |  | `"log10"` |  | the values peaks are found on: flowCore's linear values, or their log10 (every value must be above 0). Values: log10 (log10), linear (linear). |
| `peak_density_thr` | number |  | `0.05` | 0–1 | a peak lower than this share of the highest peak scores 0 (flowStats peak.density.thr). |
| `peak_distance_thr` | number |  | `0.05` | 0–1 | of two peaks closer than this share of the range, only the better scored is kept (flowStats peak.distance.thr). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `base_landmarks` | any |  | per channel, the base landmarks every sample was moved to |
| `shifts` | any |  | per channel and sample, each landmark found and the base landmark it was moved to |
| `confidence` | any |  | per sample, flowStats' confidence (1 down to 0.6^k as its landmarks sit far from the others') |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "normalize_flow_cytometry_batch",
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

### normalize_flow_cytometry_cytonorm

**Normalize flow cytometry CytoNorm**: _How must each batch be moved so that its control sample matches the others, and what does that do to the samples of that batch?_

CytoNorm batch normalization learned from controls (a reference sample run in every batch): the controls' cells, on arcsinh(x / cofactor), build a FlowSOM map grouped into metaclusters; in each metacluster each batch's control quantiles are mapped onto a goal (the mean of the batches, or one batch) by a monotone Fritsch-Carlson spline, and every file of that batch is moved by its batch's spline in each cell's metacluster, then taken back by sinh. A sample sheet names each file's batch and role (control, sample or both). Per metacluster the control cells per batch and the batches left unnormalized; per normalized file and channel the median before and after.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- The controls are the same biological sample in every batch, so every difference between them is batch effect.
- Each metacluster holds the same cell type in every batch; a batch with 50 cells or fewer in a metacluster is left as it is there.

**Does not:**
- The normalized files are written to the project from the panel only; this door returns the model summary and the medians.
- Linear float data ($PnE 0,0), as mass and spectral cytometers write; log-amplified files are refused.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `samples` | string |  | `""` |  | the FCS files, by name or id, comma-separated; empty for every FCS file in the project (each must be named in the sample sheet). |
| `sample_sheet` | string | **yes** |  |  | a CSV in the project whose first column, headed sample, names each FCS file, with a batch column and a role column. |
| `batch_column` | string |  | `"batch"` |  | the sample sheet's column naming each file's batch. |
| `role_column` | string |  | `"role"` |  | the sample sheet's column whose value is control (trains), sample (is normalized) or both. |
| `channels` | string |  | `""` |  | the channels to normalize, comma-separated PnN; empty for every channel but scatter, time and event length. |
| `arcsinh_cofactor` | number |  | `5` | ≥ 0.01 | the arcsinh cofactor (5 for mass cytometry). |
| `n_quantiles` | number |  | `99` | 2–999 | nQ: quantiles at i / (nQ + 1) per spline. |
| `grid_x` | number |  | `15` | 2–30 | FlowSOM map width (xdim). |
| `grid_y` | number |  | `15` | 2–30 | FlowSOM map height (ydim). |
| `n_metaclusters` | number |  | `10` | 2–40 | FlowSOM nClus: the cell groups normalized separately. |
| `n_cells` | number |  | `1000000` | ≥ 100 | nCells: control events the map is built on, an equal share per file. |
| `scale_markers` | boolean |  | `false` |  | scale each channel before clustering. |
| `goal` | string |  | `"mean"` |  | 'mean' for the mean of the batches, or one batch label. |
| `map_seed` | number |  | `1` | ≥ 0 | R's set.seed for the map. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `metaclusters` | any |  | per metacluster, the control cells per batch and the batches left as they are, with the reason |
| `medians` | any |  | per channel and normalized file, the median before and after (linear units) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "normalize_flow_cytometry_cytonorm",
  "arguments": {
    "sample_sheet": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### rank_reference_genes

**Rank reference genes**: _Which candidate reference genes are most stable on this plate, by geNorm, NormFinder, BestKeeper, comparative delta-Ct and their consensus?_

Which candidate reference gene is actually stable, ranked by all four published algorithms at once plus the RefFinder consensus: geNorm (pairwise variation M), NormFinder (intra/inter-group variance), BestKeeper (SD of raw Cq and correlation to the index) and the comparative delta-Ct method. They disagree on real plates, which is the point of running them side by side; the consensus is the geometric mean of the four ranks. Also returns geNorm's pairwise variation V(n/n+1), whose 0.15 cutoff is what says HOW MANY genes to normalise to.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Every candidate was measured on the same samples.
- NormFinder's group structure is the experiment's groups when the grouped arm is chosen.

**Does not:**
- The four algorithms disagree on real plates; the consensus is a geometric mean of ranks, not a fifth measurement.
- A ranking always has a most stable gene; it does not say any gene is stable enough.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cq_table` | string | **yes** |  |  | the long-format table: `Target,Sample,Cq`, one row per measurement. A fourth `Group` column is optional and is what unlocks NormFinder's GROUPED arm; without it NormFinder answers a different question and the result says so. |
| `normfinder_arm` | `"auto"` · `"ungrouped"` |  | `"auto"` |  | which NormFinder to run. `auto` uses the grouped model when the table has a Group column and the ungrouped one when it does not; `ungrouped` forces the variance-only estimate even on a grouped table. They answer DIFFERENT questions — grouped separates intra- from inter-group variation, ungrouped cannot — so this is a choice, not a fallback. Values: auto (Auto (grouped when the table says so)), ungrouped (Ungrouped (force)). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `ranking` | any |  | the consensus ranking, most stable first, with every algorithm's own rank beside it |
| `mostStable` | string |  | the consensus winner, named |
| `perMethod` | any |  | each algorithm's own order and 1-based ranks, so a consensus can be read back to the four opinions behind it |
| `genormM` | any |  | geNorm's stepwise elimination: the M value of every target at every step |
| `pairwiseV` | any |  | V(n/n+1), the pairwise variation that answers how many reference genes are enough. Below 0.15 an extra gene is not worth it (Vandesompele 2002) |
| `recommendedCount` | number |  | the smallest n whose V(n/n+1) falls under 0.15, or 0 when none does. A 0 means this plate does not support the usual answer, not that the run failed |
| `grouped` | string |  | whether NormFinder ran its grouped arm, and why not when it did not |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "rank_reference_genes",
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

### read_eds_run

**Read eds run**: _What run, plate, dyes and amplification curves does this QuantStudio .eds hold?_

Read an Applied Biosystems / Thermo QuantStudio `.eds` experiment: what the run holds (its name, plate, dyes, collection points and stages) and, on request, the amplification curves as a cycle × well table ready for call_cq. read_rdml_run reads the other instrument format; an `.eds` is not an RDML document in another spelling, so it has its own reader. Nothing is sent anywhere.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The archive is a QuantStudio `.eds` as qslib reads it (both the 1.x and 2.x layouts).

**Does not:**
- Reads what the instrument wrote: a run still in progress carries fewer collection points than its programme, and says so rather than padding them.
- Which dye is the passive reference is a fact about the assay, not the file, so it is a parameter and is never guessed.

**Not read from this result:** A reader: the run as the archive records it, with nothing inferred. The readings belong to the tools that analyze the curves it hands on (call_cq, bootstrap_cq).

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | the `.eds` to read, by name, from the project or the `_files` sent with the call. Empty reads the only one there. |
| `curves` | boolean |  | `false` |  | also return the amplification curves as a cycle × well table (tab-separated), which is what call_cq takes as its `table`. |
| `dye` | string |  |  |  | the reporter dye the curves are read from. Empty takes the run's first dye, and the answer says which. Only applies when curves is true. |
| `passive_reference` | string |  |  |  | the dye to normalize against, giving Rn (reporter ÷ passive). Empty emits the raw reporter signal and says so: picking ROX silently would be a normalization nobody chose. Only applies when curves is true. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | any |  | the run as the archive states it: name, specVersion, plate, wells, collection points, dyes and the stages they came from |
| `dyes` | any |  | the dyes this run carries, in the archive’s order |
| `wells` | number |  | wells the archive holds readings for |
| `points` | number |  | collection points — the cycles, which is what a curve has to be fitted over |
| `table` | string |  | the amplification curves as a tab-separated cycle × well table, when `curves` was asked for. Wire it into call_cq |
| `normalization` | string |  | what the table carries: the reporter's raw signal, or Rn against the named passive reference |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_eds_run",
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

### read_mgf

**Read MGF**: _What spectra does this MGF file hold?_

Read the MS/MS spectra of a Mascot Generic Format (MGF) file: each spectrum's title, precursor m/z, precursor intensity, declared charge states and peak list, interpreted as pyteomics reads MGF (validated on every spectrum of PXD000001). A spectrum it returns is what score_spectrum takes as mz, intensity and precursorCharge.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The file is MGF as pyteomics reads it.

**Does not:**
- Reads what the file says, including a declared charge that may be wrong.

**Not read from this result:** A reader: the spectra as the MGF file writes them, with nothing inferred; the Mass spec panel's readings are on the tools that score them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | **yes** |  |  | the MGF file's contents. |
| `title` | string |  |  |  | return only the spectrum with this title; empty returns every spectrum. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `spectra` | any |  | one row per spectrum: title, precursorMz, precursorIntensity, charges, mz, intensity |
| `count` | number or null |  | spectra returned |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_mgf",
  "arguments": {
    "text": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### read_mzml

**Read mzML**: _What spectra, precursors and acquisition metadata does this mzML run hold?_

Read the spectra of a PSI mzML run file: each spectrum's native id, MS level, centroid or profile, scan start time and unit, base peak, total ion current, precursor (selected ion m/z, charge, intensity, isolation window) and peak arrays, interpreted as pyteomics reads mzML (validated on every spectrum of three real runs). An MS/MS spectrum it returns is what score_spectrum takes as mz, intensity and precursorCharge.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The file is PSI mzML as pyteomics reads it.

**Does not:**
- Reads the run; it does not centroid, filter or recalibrate it.

**Not read from this result:** A reader: the spectra as the mzML file writes them, with nothing inferred; the Mass spec panel's readings are on the tools that score them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | **yes** |  |  | the mzML file's contents. |
| `id` | string |  |  |  | return only the spectrum with this native id; empty returns every spectrum. |
| `msLevel` | number |  | `0` |  | return only spectra at this MS level (0 returns every level). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `spectra` | any |  | one row per spectrum: id, msLevel, scanStartTime, precursors, mz, intensity |
| `count` | number or null |  | spectra returned |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_mzml",
  "arguments": {
    "text": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### read_structure

**Read structure**: _What is in this structure file: chains, sequences, ligands, solvent, disulfides, modified residues, B-factors, cell, resolution and experiment?_

Read a structure file — PDB, PDBx/mmCIF, or a core CIF small-molecule crystal structure — and report what is in it: the chains and what kind each is, their sequences, the ligands and ordered solvent, the disulfides, the residues the depositor declared modified, the temperature-factor range, the unit cell and space group, the resolution and the experiment. Use it to answer what a structure IS before deciding what to do with it, or to pull a chain's sequence out of a structure so it can be aligned, back-translated or ordered. Reading only: it never writes a structure file and never applies symmetry, so every count it reports is a count of what the file actually holds — for a core CIF that is the asymmetric unit, not the whole cell.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The file is PDB, PDBx/mmCIF or core CIF as deposited.

**Does not:**
- Reports what the depositor wrote, including declarations that may be wrong.
- Reading only: no geometry validation or refinement.

**Not read from this result:** A reader: the structure file's chains, residues and coordinates as written, with nothing inferred.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | **yes** |  |  | the coordinate file's contents — a PDB flat file, a PDBx/mmCIF, or a core CIF; the format is read from the bytes, not from a name, because .cif is shared by two unrelated dictionaries. |
| `model` | number |  | `1` | ≥ 1 | which model of an ensemble to describe, 1-based. An NMR entry holds many complete conformers and they are alternatives rather than parts, so the counts always describe ONE of them. The upper bound is the FILE's, so it is not declared here — an out-of-range model is refused by name, with the range that exists. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `format` | string |  | which reader actually ran: `pdb`, `mmcif`, or `smallcif` for a core CIF (small-molecule crystallography, which shares the .cif extension with mmCIF and is a different dictionary) |
| `dialect` | string |  | the same answer in words, for a reply to quote |
| `id` | string |  | the 4-character entry id the file declares about itself, empty when it declares none |
| `title` | string |  | the entry's own title line |
| `hasPolymer` | boolean |  | whether any chain is a polymer. False for a core CIF and for a coordinate set holding only a ligand — where `chains`, `residues` and `sequences` describe a wrapper rather than a molecule, and `atoms` is a count of symmetry-independent SITES |
| `formula` | string |  | the empirical formula the file STATES about itself (`_chemical_formula_sum`), empty when it states none. For a crystal structure it describes the contents of the CELL, so it can name more atoms than the sites listed |
| `method` | string |  | the experimental technique(s) — genuinely more than one for a neutron/X-ray structure |
| `resolution` | number | Å | diffraction limit in angstroms. 0 means the entry states NONE (an NMR determination has no resolution) — read `hasResolution` rather than treating 0 as sub-angstrom |
| `hasResolution` | boolean |  | whether the entry states a resolution at all |
| `models` | number |  | conformers in the file; more than one means an ensemble |
| `chains` | any |  | one row per chain: id, polymer kind, residue and atom counts, the author numbering range, and the observed one-letter sequence |
| `sequences` | any |  | the CONSTRUCT sequence per chain as the file declares it (SEQRES / _entity_poly), which includes residues that were never resolved |
| `atoms` | number |  | atoms in the model described |
| `residues` | number |  | residues in the model described, solvent included |
| `waters` | number |  | ordered solvent molecules, counted separately from ligands |
| `ligands` | any |  | non-water heteroatom components with how many copies of each — the ions, cofactors and bound compounds |
| `disulfides` | number |  | disulfide bonds the file annotates |
| `modified` | any |  | modified residues with the standard residue each stands in for, from the file's own MODRES / _pdbx_struct_mod_residue — the only authoritative source for what a component like MSE IS |
| `helices` | number |  | helices the DEPOSITOR annotated (not a calculation over the coordinates) |
| `strands` | number |  | strands the depositor annotated |
| `bFactor` | any |  | min, max and mean isotropic B over every atom, or null when the file states none |
| `extent` | number | Å | the longest side of the bounding box in angstroms — whether this will fit a pore, a groove or a box |
| `cell` | any |  | unit cell and space group, absent for a determination with no crystal |
| `warnings` | any |  | lines the reader could not parse, named rather than dropped |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_structure",
  "arguments": {
    "text": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### record_composition

**Record composition**: _What is this record made of: molecular weight under its own topology, GC and AT, and the per-symbol census?_

What the subject record is MADE OF: molecular weight under its own topology and strand count, GC and AT over the resolved bases, and the per-symbol census with the ambiguity codes broken out. The nucleic-acid counterpart of `protein_properties`, and the same derivation the editor's Properties panel, its inspector and the alignment inspector all draw (Biopython's mass model; ProtParam for a protein subject).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Weight uses the record's topology and strand count; ambiguity codes are broken out rather than resolved.

**Does not:**
- Composition only: it says nothing about what the sequence does.
- A weight over ambiguous bases is reported as a range or excluded, never silently averaged.

**Not read from this result:** The answer is the record's computed composition (weight, GC and AT, the per-symbol census), which the outputs carry; the Properties panel shows them as readouts and writes no reading over them.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `doubleStranded` | boolean |  |  |  | weigh BOTH strands (a plasmid or any dsDNA record) rather than the one strand written in the file (an oligo, an RNA, an alignment row). The two answers differ by about a factor of two, which is why it is a parameter and not a guess. Defaults to true, or false when the record is RNA (U and no T), which is also weighed with RNA residue masses. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `molecularWeight` | number |  | molecular weight — g/mol for a nucleic acid under `doubleStranded` and the record's own topology, Da for a protein |
| `strands` | number |  | how many strands the mass was taken over: 2, 1, or 0 for a protein where the question does not arise |
| `gcPercent` | number or null | % | percent G+C over the RESOLVED A/C/G/T bases (`standardCount`), which is Biopython's gc_fraction default (ambiguous="remove") — not over the full length, so it complements `atPercent` exactly. Null for a protein |
| `atPercent` | number or null | % | percent A+T over the same denominator. Null for a protein |
| `length` | number |  | symbols in the record, non-standard ones included |
| `standardCount` | number |  | how many of `length` are standard — the denominator every share here is over |
| `composition` | any |  | one row per standard symbol: code, label, count, and its percent of `standardCount` |
| `nonStandard` | any |  | the symbols the alphabet does not define — Ns, IUPAC ambiguity codes, gaps — with counts and NO share, because they are excluded from the denominator |
| `isoelectricPoint` | number or null |  | protein subjects only (ProtParam, Bjellqvist); null otherwise |
| `extinction` | any |  | protein subjects only: e280 under both cystine conventions; null otherwise |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "record_composition",
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

### relative_expression

**Relative expression**: _How much does a gene's expression change between groups, by delta-delta-Ct, delta-Ct or the standard-curve model, with a significance test on request?_

Relative gene expression from a Ct table, by all THREE models the Analyze panel offers: delta-delta-Ct (normalised to a reference gene AND calibrated to a reference group), delta-Ct (calibrated to a reference group only), and the two-step standard-curve model, which fits each gene's own dilution series and converts Ct to amount before taking the ratio. Reproduces the `pcr` package's `pcr_ddct`/`pcr_dct`/`pcr_curve`, including its separate-tube and same-tube estimators, which differ in WHEN the subtraction happens and are not a display option. A significance test runs beside the model on request - Welch t-test, the equivalent linear model, the Wilcoxon rank-sum test with R's own exactness rule, or a design-matrix lm for designs the two-group form cannot express - and delta-delta-Ct's equal-efficiency assumption can be checked in the same run.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- delta-delta-Ct assumes the target and reference genes amplify with equal efficiency; the run can check it.
- The reference gene is stable across the groups compared.

**Does not:**
- A fold change is relative to the calibrator group; it is not an absolute quantity.
- The separate-tube and same-tube estimators differ in when the subtraction happens and give different answers by design.

**Validated:** against the reference implementation by 5 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `ct_table` | string | **yes** |  |  | the Ct table: a header row of gene names, then one row per sample. Tab- or comma-separated, the same table the Analyze tab takes. |
| `groups` | string | **yes** |  |  | the group each sample belongs to, one per line, in the same order as the Ct rows (e.g. six lines of `control` then six of `treated`). |
| `reference_gene` | string |  |  |  | the gene expression is normalised to. Required for delta-delta-Ct and for the standard-curve model; ignored by delta-Ct, which normalises to a group only. Only applies when model is delta_delta_ct or relative_curve. |
| `reference_group` | string | **yes** |  |  | the group everything is calibrated against: the untreated / time-zero / wild-type arm. |
| `model` | `"delta_delta_ct"` · `"delta_ct"` · `"relative_curve"` |  | `"delta_delta_ct"` |  | which model. `delta_delta_ct` and `relative_curve` need a reference gene, `delta_ct` does not; `relative_curve` additionally needs `standard_ct_table` and `amounts`, because it fits a real dilution series rather than assuming efficiency. Values: delta_delta_ct (Delta-delta-Ct (normalised + calibrated)), delta_ct (Delta-Ct (calibrated only)), relative_curve (Standard curve (fitted amounts)). |
| `tube` | `"separate_tube"` · `"same_tube"` |  | `"separate_tube"` |  | `separate_tube`: target and reference amplified in different wells, errors independent. `same_tube`: multiplexed in one well, subtracted per well before averaging. Advanced. |
| `standard_ct_table` | string |  |  |  | the SERIAL-DILUTION Ct table the standard curve is fitted to - a second plate, not the sample one. Required by `relative_curve`, and by `assess_efficiency` on any model. Advanced. |
| `amounts` | string |  |  |  | the input amount of each dilution row, one per row of `standard_ct_table`, whitespace- or comma-separated. The fit is against log10 of these, so every value must be positive. Advanced. |
| `assess_efficiency` | boolean |  | `false` |  | run `pcr_assess(method = 'efficiency')` beside delta-delta-Ct: delta-Ct against the reference gene regressed on log10 amount, per gene. This is how the model's equal-efficiency assumption is CHECKED rather than assumed - a slope far from zero says delta-delta-Ct is the wrong model for this plate. Needs `standard_ct_table` and `amounts`. Advanced. |
| `sig_test` | `"none"` · `"t.test"` · `"lm"` · `"wilcox.test"` · `"lm.design"` |  | `"none"` |  | which significance test runs beside the model. `t.test` is Welch's two-sample test on the normalised values; `lm` is the equivalent linear model, which reports the same p with a confidence interval; `wilcox.test` is the rank-sum test, for plates too small or too skewed to assume normality; `lm.design` fits `lm(norm ~ model_matrix + 0)` for designs the two-group form cannot express, and is reported through `design` rather than the test table. Values: none (None), t.test (Welch t-test), lm (Linear model (two-group)), wilcox.test (Wilcoxon rank-sum), lm.design (Design-matrix linear model). Advanced. |
| `wilcox_alternative` | `"two.sided"` · `"less"` · `"greater"` |  | `"two.sided"` |  | the Wilcoxon alternative hypothesis. Values: two.sided (Two-sided), less (Less (shift < 0)), greater (Greater (shift > 0)). Only applies when sig_test is wilcox.test. Advanced. |
| `wilcox_exact` | `"auto"` · `"exact"` · `"normal"` |  | `"auto"` |  | which Wilcoxon null distribution. `auto` applies R's own rule (exact while both groups are under 50 and there are no ties); `exact` forces the exact distribution, which is costly on large groups; `normal` forces the approximation. Values: auto (Auto (exact if both groups < 50)), exact (Exact conditional), normal (Normal approximation). Only applies when sig_test is wilcox.test. Advanced. |
| `wilcox_correct` | `"none"` · `"continuity"` · `"1"` · `"2"` · `"3"` |  | `"continuity"` |  | tail refinement for the Wilcoxon normal approximation: `none`, R's `continuity` correction, or 1-3 Edgeworth terms. Ignored when the exact distribution is used. Values: none (None), continuity (Continuity), 1 (Continuity + Edgeworth 1), 2 (Continuity + Edgeworth 2), 3 (Continuity + Edgeworth 3). Only applies when sig_test is wilcox.test. Advanced. |
| `wilcox_conf_level` | number |  | `0.95` | 0.5–0.9999 | confidence level for the Wilcoxon location-shift interval. Only applies when sig_test is wilcox.test. Advanced. |
| `lm_formula` | string |  | `"~ group"` |  | the design formula for `lm.design`, in R's own notation (`~ group`, `~ group + dose`, `~ group * run`). `group` is always available from `groups` with no paste at all. Only applies when sig_test is lm.design. Advanced. |
| `lm_variables` | string |  |  |  | extra design variables for `lm.design`: a header row of variable names, then one row per sample in the Ct table's order. A column whose every value parses as a number is a covariate, otherwise a factor - the same distinction R makes. Leave empty to model on `group` alone. Only applies when sig_test is lm.design. Advanced. |
| `lm_mode` | `"subtract"` · `"divide"` |  | `"subtract"` |  | how `lm.design` normalises the target against the reference gene before fitting: `subtract` the reference Ct (the delta-Ct scale), or `divide` by it. Values: subtract (Subtract (ΔCt = target − reference)), divide (Divide (target ÷ reference)). Only applies when sig_test is lm.design. Advanced. |
| `lm_conf_level` | number |  | `0.95` | 0.5–0.9999 | confidence level for the `lm.design` coefficient intervals. Only applies when sig_test is lm.design. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rows` | any |  | one row per group x gene: the normalised and calibrated delta-Ct (or fitted amount ratio), the fold change and its bounds |
| `count` | number |  | how many rows the model produced |
| `model` | string |  | the model that produced them |
| `genes` | any |  | the genes measured, reference gene excluded under delta-delta-Ct |
| `groups` | any |  | the groups, in the order the rows use |
| `test` | any |  | the significance test beside the model - one row per gene, with the statistic, p value and interval - or null when none was asked for |
| `design` | any |  | the design-matrix linear model: the formula, the columns it built, and per gene a coefficient table WITH the fit diagnostics. Null unless `sig_test` is `lm.design` |
| `trend` | any |  | the per-gene standard curve (intercept, slope, R-squared) the `relative_curve` model consumed, or null |
| `standardPoints` | any |  | the dilution observations behind that curve, with fitted values and residuals - a standard curve is judged by whether a dilution sits off the line, not by R-squared |
| `efficiency` | any |  | the equal-efficiency check: delta-Ct regressed on log10 amount per gene. A slope far from zero says delta-delta-Ct is the wrong model here. Null unless `assess_efficiency` ran |
| `referenceGene` | string or null |  | the gene every target was normalised to under delta-delta-Ct; null for the models that use none |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "relative_expression",
  "arguments": {
    "ct_table": "<string>",
    "groups": "<string>",
    "reference_group": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### reverse_complement

**Reverse complement**: _What is the reverse complement of this sequence, with its annotations carried over?_

Reverse-complement the subject sequence. Emits a NEW record, so downstream nodes (map, digest, gel, ORF) run on the revcomp rather than the original.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- IUPAC complementation, including the ambiguity codes.

**Does not:**
- Feature strands and coordinates flip with the sequence; qualifiers are not reinterpreted.

**Not read from this result:** A transform: the same molecule written on the other strand, with nothing inferred.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

_No arguments beyond the shared `_subject` and `_files`._

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the reverse-complemented record |
| `sequence` | string |  | reverse complement 5'→3' |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "reverse_complement",
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

### scan_intrinsic_terminators

**Scan intrinsic terminators**: _Which rho-independent terminators does this bacterial sequence carry, and how good is each hairpin and tail?_

Find rho-independent (intrinsic) transcription terminators in a bacterial sequence: a stem-loop followed by a thymine-rich tail, scored by TransTermHP's published model (Kingsford, Ayanbule & Salzberg 2007). TWO NUMBERS, BOTH LOWER IS STRONGER - how well the hairpin folds and how thymine-rich the tail is - and NEITHER IS A FREE ENERGY: they are costs in this model's own scheme and must not be compared with a promoter's ΔG or a Turner ΔG. This is the question behind a downstream gene in an operon that goes quiet: a cryptic terminator inside an insert stops transcription that was meant to continue. Rho-DEPENDENT termination needs the protein and is not a sequence motif this or any such model can see. Reports every candidate clearing the two published cutoffs; TransTermHP itself lists one per position after its own overlap filters, so it reports fewer for the same sequence - a difference in reporting, not in scoring. No confidence value is given: TransTermHP's is a lookup into a table calibrated by its own GPL tooling, which is not shipped rather than approximated.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- TransTermHP's published scoring scheme (Kingsford, Ayanbule and Salzberg 2007).

**Does not:**
- Two costs in the model's own scheme, both lower is stronger, and neither is a free energy.
- Rho-dependent termination is a different mechanism and is not found here.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the DNA to scan - leave unset to use the open record. |
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to scan. Unset = the whole sequence; pass the selection's start to scope to it. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end. Unset = the whole sequence. Advanced. |
| `both_strands` | boolean |  | `true` |  | scan the reverse strand too. On by default: a terminator on the strand you did not draw still stops transcription that runs into it. |
| `max_results` | number |  | `50` | 1–500 | how many to return, best hairpin first. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `terminators` | any |  | the candidates, best hairpin first, each with its stem-loop, its tail, the stem length and both scores |
| `count` | number |  | how many are reported |
| `strongest` | any |  | the best-folding candidate, or null when none cleared both cutoffs |
| `strongestHairpin` | number or null |  | that candidate's hairpin score on its own, for a threshold downstream (lower is stronger). null when none cleared both cutoffs: there is no hairpin to score, and a 0 would pass a threshold as a measured value |
| `offset` | number |  | where the scanned stretch starts in the sequence: add it to every position above for sequence coordinates. 0 unless a region was given |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "scan_intrinsic_terminators",
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

### scan_sigma70_promoters

**Scan sigma70 promoters**: _Which sigma70 promoters does this bacterial sequence carry, and how strong is each by the La Fleur-Hossain-Salis biophysical model?_

Find σ70 (housekeeping) promoters in a bacterial sequence and say how strong each one is, using the published La Fleur-Hossain-Salis biophysical model - six interaction motifs (UP element, -35, spacer, extended -10, -10, discriminator) plus the R-loop strength of the first transcribed bases, fitted on 22,132 characterised promoters. THE NUMBER IS A FREE ENERGY AND MORE NEGATIVE IS STRONGER, which is the opposite direction from a score; the transcription rate beside it is the paper's own rate law over that energy. It answers "could RNA polymerase start here", not "does it": nothing here knows about regulators, supercoiling or growth phase. It is E. coli σ70 and says nothing about σ38/σ32/σ54 promoters or about another organism's polymerase.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The model's six motifs and R-loop term, as fitted on 22,132 characterised promoters in E. coli.
- The host's sigma70 holoenzyme resembles the one fitted.

**Does not:**
- The number is a free energy: more negative is stronger, and it is not a transcription rate.
- Fitted in E. coli; another organism is extrapolation.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the DNA to scan - leave unset to use the open record. |
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to scan. Unset = the whole sequence; pass the selection's start to scope to it. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end. Unset = the whole sequence. Advanced. |
| `both_strands` | boolean |  | `true` |  | scan the reverse strand too. On by default: a cryptic promoter does not care which strand your insert was drawn on, and scanning one is how one gets missed. |
| `max_dg` | number |  |  | -30–0 | report only configurations at or below this ΔG_total. UNSET BY DEFAULT and deliberately so: this model publishes no significance cutoff, so the answer is a RANKING of the strongest configurations rather than a set of calls, and inventing a floor here is the exact defect the scanner this replaces had. Set it when you have a threshold of your own. In kcal/mol. |
| `max_results` | number |  | `50` | 1–500 | how many to return, strongest (most negative) first. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `promoters` | any |  | the configurations, strongest (most negative) first, each with its six motif sequences, their positions and the per-motif energies that sum to its total |
| `count` | number |  | how many are reported (`max_results`, or fewer if the sequence is short or `max_dg` was set) |
| `strongest` | any |  | the most negative ΔG_total, or null when the sequence is too short to hold one |
| `strongestDg` | number or null |  | that hit's ΔG_total on its own, for a threshold downstream, or null when there is no hit |
| `offset` | number |  | where the scanned stretch starts in the sequence: add it to every position above for sequence coordinates. 0 unless a region was given |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "scan_sigma70_promoters",
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

### scan_splice_sites

**Scan splice sites**: _Which splice donors and acceptors does this sequence spell, by maximum-entropy strength and by typicality against measured Arabidopsis sites?_

Find the splice sites a sequence accidentally spells - the check a codon-optimised CDS needs before it goes into a plant or any other eukaryotic host, because a synonymous swap chosen for codon usage or GC can spell a donor or acceptor that was not there before, and the transcript is then spliced somewhere nobody intended. Every GT and AG is scored two ways that are NOT on one scale and are never combined: `maxEnt` is strength under Yeo & Burge's published maximum-entropy model, and `typicality` is log-odds against base frequencies MEASURED at the annotated splice sites of Arabidopsis thaliana TAIR10 (Ensembl Plants 63). IT RETURNS NO VERDICT and has no default threshold: neither model publishes a cutoff, so this RANKS candidates and what counts as dangerous is your call, with both numbers in front of you.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- MaxEnt is Yeo and Burge's published model with their trained tables.
- Typicality is log-odds against base frequencies measured at TAIR10's annotated sites, so it speaks for a plant host.

**Does not:**
- No verdict and no threshold: neither model publishes a cutoff, so it ranks and the call is yours.
- The two numbers are on different scales and are never combined.
- The Arabidopsis matrices have no upstream to grade them: the claim is that re-running their generator against Ensembl Plants 63 reproduces them exactly.

**Not read from this result:** The ranked splice sites with their MaxEnt bits; the Optimize panel lists them against the annotated introns and writes no sentence over them. The optimizer's reading is on optimize_sequence.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the DNA to scan - leave unset to use the open record. |
| `strand` | `"both"` · `"forward"` · `"reverse"` |  | `"both"` |  | which strand to read. Both by default: an antisense site still splices a transcript made from the other strand, and in a construct both may be transcribed. Name the gene's own strand when you know it, and the other strand's candidates stop crowding the ranking. |
| `min_maxent` | number |  |  | -30–20 | report only sites at or above this MaxEntScan score, in bits. UNSET BY DEFAULT and deliberately so - MaxEntScan publishes no significance cutoff and the measured matrices are a description rather than a classifier, so a default here would be a decision boundary nobody has published. Set it when you have a threshold of your own. In bits. |
| `max_results` | number |  | `50` | 1–500 | how many to return, strongest first. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sites` | any |  | the candidates, strongest MaxEnt first, each with its kind, position on the strand you passed, the window that was scored, and both scores |
| `count` | number |  | how many are reported |
| `strongest` | any |  | the highest-scoring candidate, or null when the sequence is too short to hold a window |
| `strongestMaxEnt` | number or null |  | that candidate's MaxEntScan score on its own, for a comparison downstream, or null when there is no candidate: 0 is a real MaxEntScan score |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "scan_splice_sites",
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

### score_spectrum

**Score spectrum**: _How well does this MS/MS spectrum match this peptide, by X!Tandem HyperScore?_

Score how well an MS/MS spectrum matches a peptide with the X!Tandem HyperScore (validated against OpenMS): b and y ions are generated for the peptide, matched to the observed peaks within a tolerance, and scored as ln(1 + dot product) + ln(matched b!) + ln(matched y!).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- b and y ions explain the spectrum; peaks match within the tolerance given.

**Does not:**
- A score, not a probability: a q-value needs target_decoy_qvalues over a whole set.
- Only b and y series are scored.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `peptide` | string | **yes** |  |  | candidate peptide, one-letter residues with optional ProForma tags (a signed mass, a Unimod name, or UNIMOD:accession). |
| `mz` | number[] | **yes** |  |  | observed peak m/z values. |
| `intensity` | number[] | **yes** |  |  | observed peak intensities, one per m/z. |
| `precursorCharge` | number |  | `2` |  | precursor charge; fragments are generated at charges 1 to max(1, charge - 1). |
| `tolerance` | number |  | `0.02` |  | fragment match tolerance. |
| `toleranceUnit` | `"Da"` · `"ppm"` |  | `"Da"` |  | unit of the tolerance. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `score` | number or null |  | HyperScore (natural log scale; higher is a better match) |
| `detail` | any |  | matched b and y ion counts, mean match error, theoretical peak count |
| `matches` | any |  | one row per matched ion: ion name, theoretical and observed m/z, intensity, error in the tolerance unit |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "score_spectrum",
  "arguments": {
    "peptide": "<string>",
    "mz": [],
    "intensity": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### size_fragments

**Size fragments**: _What size in bases is each peak of this fragment run, against its own size standard?_

Size the peaks of a fragment-analysis run (.fsa / .hid) against its own size standard, and hand them on as lengths in bases. A fragment run carries no sequence at all — dye channels and a ladder — so this is the node that turns one into numbers a pipeline can act on: allele sizes, a peak table, and the ladder's own measured accuracy beside them.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The size standard and sizing method named, as GeneMapper and PeakScanner define them.

**Does not:**
- Sizes peaks; allele calls follow the tolerance and the kit given.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which fragment file to read: its name (`ladder.fsa`) or its project file id. A file id is project-specific, so a template ships this unset. |
| `method` | `"local-southern"` · `"global-southern"` · `"least-squares-2"` · `"least-squares-3"` · `"cubic-spline"` |  | `"local-southern"` |  | the sizing curve. Local methods use the standard fragments nearest each peak and are the more accurate on a real ladder; the global reciprocal fit is less affected by one standard fragment running anomalously. Applied Biosystems, DNA Fragment Analysis by Capillary Electrophoresis, Ch. 5. Values: local-southern (Local Southern), global-southern (Global Southern), least-squares-2 (Least squares (2nd order)), least-squares-3 (Least squares (3rd order)), cubic-spline (Cubic spline). |
| `threshold` | number |  | `100` | 0–30000 | minimum peak height, in the channel's own units. |
| `min_size` | number |  | `0` | 0–2000 | ignore peaks sized below this. In bases. |
| `max_size` | number |  | `1000` | 1–2000 | ignore peaks sized above this. In bases. |
| `ladder_dye` | number |  |  | 1–8 | which dye carries the size standard. Left unset it is MEASURED, by matching the standard's own scans against each channel's peaks — the copy of the table in the file says nothing about which channel it ran in. Advanced. |
| `kit` | `"none"` · `"file"` · `"cordisplus"` · `"cofiler"` · `"geneprint10"` · `"globalfiler"` · `"identifilerlessils250"` · `"identifilerpluslessils250"` · `"identifilerplus"` · `"identifiler"` · `"microreaderyprime"` · `"minifiler"` · `"ngmselect"` · `"ngm"` · `"niddkfragilex1"` · `"netbioflexplex"` · `"ppfusion6c"` · `"ppfusion-v2-6"` · `"ppfusion"` · `"ppgeneprint24"` · `"pplexy23-v2-6"` · `"pplexy23"` · `"powerplex1-2"` · `"powerplex16"` · `"powerplex18d-v2-6"` · `"powerplex18d"` · `"powerplex21-v2-6"` · `"powerplex21"` · `"powerplexs5"` · `"powerplexy"` · `"powerplex-esi16-v2-6"` · `"powerplex-esi16"` · `"powerplex-esi17-v2-6"` · `"powerplex-esi17"` · `"powerplex-esx16-v2-6"` · `"powerplex-esx16"` · `"powerplex-esx17-v2-6"` · `"powerplex-esx17"` · `"profilerplus"` · `"q-investigator24plex"` · `"q-investigatorargusx12"` · `"q-investigatorargusx12-qs"` · `"ryanclarkecannabis"` · `"sefilerplus"` · `"sgmplus"` · `"yfilerplus"` · `"yfiler"` · `"iplexstrliz500less250"` · `"iplexstr"` |  | `"none"` |  | name each peak's locus and allele from a marker kit's own ladder definition. Left unset the node reports sizes, which is a complete measurement — a genotype needs a kit. Values: none (No kit — sizes only), file (A kit definition in this project), cordisplus (COrDIS Plus), cofiler (Cofiler), geneprint10 (GenePrint 10), globalfiler (GlobalFiler), identifilerlessils250 (Identifiler Less ILS250), identifilerpluslessils250 (IdentifilerPlus Less ILS250), identifilerplus (IdentifilerPlus), identifiler (Identifiler), microreaderyprime (Microreader Y Prime), minifiler (Minifiler), ngmselect (NGMSElect), ngm (NGM), niddkfragilex1 (NIDDKFragileX1), netbioflexplex (NetBio_FlexPlex), ppfusion6c (PowerPlex Fusion 6C), ppfusion-v2-6 (PowerPlex Fusion (v2.6)), ppfusion (PowerPlex Fusion), ppgeneprint24 (PowerPlex GenePrint24), pplexy23-v2-6 (PowerPlex Y23 (v2.6)), pplexy23 (PowerPlex Y23), powerplex1-2 (PowerPlex 1.2), powerplex16 (PowerPlex 16), powerplex18d-v2-6 (PowerPlex 18D (v2.6)), powerplex18d (PowerPlex 18D), powerplex21-v2-6 (PowerPlex 21 (v2.6)), powerplex21 (PowerPlex 21), powerplexs5 (PowerPlexS5), powerplexy (PowerPlex Y), powerplex-esi16-v2-6 (PowerPlex ESI16 (v2.6)), powerplex-esi16 (PowerPlex ESI16), powerplex-esi17-v2-6 (PowerPlex ESI17 (v2.6)), powerplex-esi17 (PowerPlex ESI17), powerplex-esx16-v2-6 (PowerPlex ESX16 (v2.6)), powerplex-esx16 (PowerPlex ESX16), powerplex-esx17-v2-6 (PowerPlex ESX17 (v2.6)), powerplex-esx17 (PowerPlex ESX17), profilerplus (ProfilerPlus), q-investigator24plex (QiagenInvestigator24plex), q-investigatorargusx12 (QiagenArgusX12), q-investigatorargusx12-qs (QiagenArgusX12_QS), ryanclarkecannabis (Cannabis), sefilerplus (SEfilerPlus), sgmplus (SGM Plus), yfilerplus (Yfiler Plus), yfiler (Yfiler), iplexstrliz500less250 (iPLEXSTRLIZ500less250), iplexstr (iPLEXSTR). |
| `kit_file` | string |  | `""` |  | which kit definition in this project, by file name or file id — for a kit this build does not bundle, which is the ordinary case for a regional or in-house panel. An OSIRIS `*_LadderInfo.xml`. Left empty when the project holds exactly one, it is used. Only read when `kit` is `file`. Only applies when kit is file. |
| `lane_standard` | string |  | `""` |  | the internal lane standard this run used, by its name (`ABI-LIZ-600-60-TO-460`, `Promega-ILS-600`, …). Only read when the FILE records no size standard of its own, which is every 3500 `.hid`: there the ruler has to be named because it was never written down. A `.fsa` carries its own table, which is a measurement of that run and always wins. NCBI OSIRIS's library, 133 standards across 24 families. |
| `ladder_run` | string |  | `""` |  | an ALLELIC LADDER of the same kit, in this project, to call against instead of the kit file's nominal sizes: its name (`identifiler-ladder.fsa`) or its file id. A kit's sizes are the manufacturer's own reference run, and yours reads them systematically long or short by length — measured on the bundled pairs, a ladder sits 0.27 bases from nominal at 175-200 and 1.40 at 300-325, and the sample beside it is off by the same amount, so comparing the two cancels what comparing to the table does not. Graded on the published 9947A profile over four kits: 24 of 42 loci exact against nominal, 35 of 44 against the ladder. A locus whose ladder does not produce all its declared alleles keeps its nominal sizes and says so rather than being labeled partly. Only applies when kit is file or cordisplus or cofiler or geneprint10 or globalfiler or identifilerlessils250 or identifilerpluslessils250 or identifilerplus or identifiler or microreaderyprime or minifiler or ngmselect or ngm or niddkfragilex1 or netbioflexplex or ppfusion6c or ppfusion-v2-6 or ppfusion or ppgeneprint24 or pplexy23-v2-6 or pplexy23 or powerplex1-2 or powerplex16 or powerplex18d-v2-6 or powerplex18d or powerplex21-v2-6 or powerplex21 or powerplexs5 or powerplexy or powerplex-esi16-v2-6 or powerplex-esi16 or powerplex-esi17-v2-6 or powerplex-esi17 or powerplex-esx16-v2-6 or powerplex-esx16 or powerplex-esx17-v2-6 or powerplex-esx17 or profilerplus or q-investigator24plex or q-investigatorargusx12 or q-investigatorargusx12-qs or ryanclarkecannabis or sefilerplus or sgmplus or yfilerplus or yfiler or iplexstrliz500less250 or iplexstr. |
| `require_resolvable` | boolean |  | `false` |  | leave a peak unnamed when the neighboring allele is closer than twice THIS RUN's own sizing error at that length, instead of naming the nearest. Off by default: the error is measured with each size-standard fragment withheld, which is harsher than sizing a peak with all of them present, so in a sparsely anchored region it is pessimistic. On a run whose standard has a wide gap it is what stops a confident wrong allele; on an evenly anchored one it changes nothing. Every call carries the number either way. |
| `allele_tolerance` | number |  | `2` | 0.1–4 | how far a peak may sit from a ladder allele and still be called it. Above half the repeat unit (4 bases for most STR loci) a peak reaches two alleles and is reported as ambiguous rather than guessed. In bases. Only applies when kit is file or cordisplus or cofiler or geneprint10 or globalfiler or identifilerlessils250 or identifilerpluslessils250 or identifilerplus or identifiler or microreaderyprime or minifiler or ngmselect or ngm or niddkfragilex1 or netbioflexplex or ppfusion6c or ppfusion-v2-6 or ppfusion or ppgeneprint24 or pplexy23-v2-6 or pplexy23 or powerplex1-2 or powerplex16 or powerplex18d-v2-6 or powerplex18d or powerplex21-v2-6 or powerplex21 or powerplexs5 or powerplexy or powerplex-esi16-v2-6 or powerplex-esi16 or powerplex-esi17-v2-6 or powerplex-esi17 or powerplex-esx16-v2-6 or powerplex-esx16 or powerplex-esx17-v2-6 or powerplex-esx17 or profilerplus or q-investigator24plex or q-investigatorargusx12 or q-investigatorargusx12-qs or ryanclarkecannabis or sefilerplus or sgmplus or yfilerplus or yfiler or iplexstrliz500less250 or iplexstr. Advanced. |
| `min_peak_spacing` | number |  | `0.5` | 0–2 | two maxima closer than this in one channel are one peak with a noisy top rather than two fragments: the separation is by length and no two fragments differ by less than one base. The taller is kept. 0 reports every maximum the detector finds. In bases. Advanced. |
| `adenylation_threshold` | number |  | `0.3333` | 0–1 | a peak within one base of a taller one in the same locus, below this fraction of its height, is an incompletely adenylated shoulder of it rather than an allele. 0.3333 is NCBI OSIRIS's own AdenylationThreshold default. 0 calls every peak. Only applies when kit is file or cordisplus or cofiler or geneprint10 or globalfiler or identifilerlessils250 or identifilerpluslessils250 or identifilerplus or identifiler or microreaderyprime or minifiler or ngmselect or ngm or niddkfragilex1 or netbioflexplex or ppfusion6c or ppfusion-v2-6 or ppfusion or ppgeneprint24 or pplexy23-v2-6 or pplexy23 or powerplex1-2 or powerplex16 or powerplex18d-v2-6 or powerplex18d or powerplex21-v2-6 or powerplex21 or powerplexs5 or powerplexy or powerplex-esi16-v2-6 or powerplex-esi16 or powerplex-esi17-v2-6 or powerplex-esi17 or powerplex-esx16-v2-6 or powerplex-esx16 or powerplex-esx17-v2-6 or powerplex-esx17 or profilerplus or q-investigator24plex or q-investigatorargusx12 or q-investigatorargusx12-qs or ryanclarkecannabis or sefilerplus or sgmplus or yfilerplus or yfiler or iplexstrliz500less250 or iplexstr. Advanced. |
| `stutter_threshold` | number |  | `0.15` | 0–1 | the same test one repeat below rather than one base. 0.15 is OSIRIS's own StutterThreshold default, and the repeat unit is read off each locus's own ladder rather than typed in. 0 disables it. Only applies when kit is file or cordisplus or cofiler or geneprint10 or globalfiler or identifilerlessils250 or identifilerpluslessils250 or identifilerplus or identifiler or microreaderyprime or minifiler or ngmselect or ngm or niddkfragilex1 or netbioflexplex or ppfusion6c or ppfusion-v2-6 or ppfusion or ppgeneprint24 or pplexy23-v2-6 or pplexy23 or powerplex1-2 or powerplex16 or powerplex18d-v2-6 or powerplex18d or powerplex21-v2-6 or powerplex21 or powerplexs5 or powerplexy or powerplex-esi16-v2-6 or powerplex-esi16 or powerplex-esi17-v2-6 or powerplex-esi17 or powerplex-esx16-v2-6 or powerplex-esx16 or powerplex-esx17-v2-6 or powerplex-esx17 or profilerplus or q-investigator24plex or q-investigatorargusx12 or q-investigatorargusx12-qs or ryanclarkecannabis or sefilerplus or sgmplus or yfilerplus or yfiler or iplexstrliz500less250 or iplexstr. Advanced. |
| `pullup_threshold` | number |  |  | 0–1 | a peak whose top sits inside the saturated top of a taller peak in ANOTHER dye, at or below this fraction of it, is named pull-up rather than called. Omitted, the kit's own published sample value from NCBI OSIRIS (0.2 for most kits; off where OSIRIS publishes none). 0 disables it. Only applies when kit is file or cordisplus or cofiler or geneprint10 or globalfiler or identifilerlessils250 or identifilerpluslessils250 or identifilerplus or identifiler or microreaderyprime or minifiler or ngmselect or ngm or niddkfragilex1 or netbioflexplex or ppfusion6c or ppfusion-v2-6 or ppfusion or ppgeneprint24 or pplexy23-v2-6 or pplexy23 or powerplex1-2 or powerplex16 or powerplex18d-v2-6 or powerplex18d or powerplex21-v2-6 or powerplex21 or powerplexs5 or powerplexy or powerplex-esi16-v2-6 or powerplex-esi16 or powerplex-esi17-v2-6 or powerplex-esi17 or powerplex-esx16-v2-6 or powerplex-esx16 or powerplex-esx17-v2-6 or powerplex-esx17 or profilerplus or q-investigator24plex or q-investigatorargusx12 or q-investigatorargusx12-qs or ryanclarkecannabis or sefilerplus or sgmplus or yfilerplus or yfiler or iplexstrliz500less250 or iplexstr. Advanced. |
| `include_ladder_channel` | boolean |  | `false` |  | also report the size standard's own peaks. They are the ruler, so they are excluded by default. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `peaks` | any |  | every sized peak: size in bases, dye, height, scan, and whether it saturated |
| `sizes` | any |  | just the lengths in bases, ascending — the list a downstream gate reads |
| `peakCount` | number |  | how many peaks were sized |
| `accuracy` | any |  | this run's own sizing error in bases, measured by leaving each standard fragment out and sizing it from the others. A difference smaller than this is not one the run can resolve |
| `sizeStandard` | any |  | the ladder the sizes rest on: its fragments, the channel it was found in, and how that channel was chosen |
| `alleles` | any |  | each peak's locus and allele under the chosen kit, with the ones that could not be named and WHY. Null when no kit was named |
| `genotype` | any |  | the alleles called per locus — the readout a downstream step compares. Null when no kit was named |
| `run` | any |  | what the FILE says about itself: sample, instrument, polymer, dye names, scan count. Not the channels, which cannot ride a wire |
| `ladder_calibration` | any |  | when a ladder run was named: which loci it labeled, at what spacing correlation, which it refused and why, and how many alleles were re-expressed in this instrument's own sizes. Null when the kit's nominal sizes were used |
| `lane_standard_fit` | any |  | how a NAMED lane standard was fitted, when one was used: the peaks it matched, the correlation it reached and the threshold that had to be cleared, so a caller can see why the sizes are trusted. Null for a run whose file records its own standard |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "size_fragments",
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

### summarize_rows

**Summarize rows**: _What is this table column's summary: its largest, smallest, median, mean or spread, overall or per group?_

Reduce a whole TABLE column to one number — the largest band, the median guide score, the spread of a set of melting temperatures. This is what makes a CROSS-ROW check expressible: `check_rows` can only assert the same thing of every row, so "the largest fragment is at least twice the smallest" needed two summaries and a comparison and had nowhere to come from. Name a `group_field` and it summarizes each group instead of the whole table (the mean product size per template), emitting a table a gate can then check group by group; pick a pairwise operation and it relates two columns of the same rows.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The column holds comparable numbers.

**Does not:**
- A summary of the rows given, not of a population: no standard error or inference.

**No scientific claim:** Reduces a column with named arithmetic so a cross-row check can be expressed.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `items` | string[] | **yes** |  |  | the rows to summarize. Wire a json/list output (bands, guides, assays, amplicons). |
| `field` | string |  |  |  | which field of each row to reduce (e.g. `size`, `score`). Leave empty when the rows are plain numbers; a tuple row is indexed by number, so `0` is the first column. |
| `operation` | `"sum"` · `"min"` · `"max"` · `"absmin"` · `"absmax"` · `"range"` · `"count"` · `"first"` · `"last"` · `"mode"` · `"antimode"` · `"unique"` · `"collapse"` · `"countunique"` · `"mean"` · `"geomean"` · `"harmmean"` · `"trimmean"` · `"median"` · `"q1"` · `"q3"` · `"iqr"` · `"perc"` · `"pstdev"` · `"sstdev"` · `"pvar"` · `"svar"` · `"ms"` · `"rms"` · `"mad"` · `"madraw"` · `"sskew"` · `"pskew"` · `"skurt"` · `"pkurt"` · `"jarque"` · `"dpo"` · `"scov"` · `"pcov"` · `"spearson"` · `"ppearson"` |  | `"max"` |  | which summary to take. The vocabulary is GNU datamash's, so a number here is the number `datamash <op>` gives for the same column. The last four relate TWO columns and need a `second_field`. Values: sum (sum), min (minimum), max (maximum), absmin (smallest by magnitude), absmax (largest by magnitude), range (range (max − min)), count (count of values), first (first value), last (last value), mode (most common value), antimode (least common value), unique (the distinct values, sorted), collapse (every value, in order), countunique (count of distinct values), mean (mean), geomean (geometric mean), harmmean (harmonic mean), trimmean (trimmed mean), median (median), q1 (lower quartile), q3 (upper quartile), iqr (interquartile range), perc (percentile), pstdev (standard deviation (population)), sstdev (standard deviation (sample)), pvar (variance (population)), svar (variance (sample)), ms (mean square), rms (root mean square), mad (median absolute deviation, scaled), madraw (median absolute deviation, unscaled), sskew (skewness (sample)), pskew (skewness (population)), skurt (excess kurtosis (sample)), pkurt (excess kurtosis (population)), jarque (Jarque–Bera normality p-value), dpo (D'Agostino–Pearson normality p-value), scov (covariance (sample)), pcov (covariance (population)), spearson (Pearson correlation (sample)), ppearson (Pearson correlation (population)). |
| `group_field` | string |  |  |  | split the rows by this field first and summarize each group: `template` on a multiplex screen, `strand` on a guide table. Leave empty to summarize the whole table. |
| `second_field` | string |  |  |  | the second column for the pairwise operations, the one this field is related TO (e.g. `gc` against `size`). Only applies when operation is scov or pcov or spearson or ppearson. |
| `trim` | number |  | `0` | 0–0.5 | the fraction to drop from EACH end before averaging, 0-0.5. datamash's own bound: 0.5 keeps only the middle value. Only applies when operation is trimmean. |
| `percentile` | number |  | `50` | 0–100 | which percentile to take, 0–100. In %. Only applies when operation is perc. |
| `label` | string |  |  |  | what this summary IS, in your words. It becomes the message the run reports. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `value` | any |  | the summary itself. Wire it into a gate's `value` or its `against`; with a `group_field` this is the first group's value, and `groups` is the table you want |
| `number` | number or null |  | the same answer as a number, so it can drive a numeric port directly. Absent for the text summaries (`first`, `unique`, …) |
| `groupCount` | number or null |  | how many distinct groups the split found. Absent when nothing was grouped — an ungrouped summary has no group count, and a 0 would read as one |
| `count` | number |  | how many rows went into it: a summary of three bands and a summary of thirty are different claims |
| `used` | number |  | how many of those rows actually carried a number. Lower than `count` means the column has gaps, and the summary says so rather than implying it read them all |
| `groups` | any |  | one row per group (`{ group, value, count, used }`) when a `group_field` is set. Wire it into `check_rows` to gate every group at once |
| `message` | string |  | what was summarized, in words |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "summarize_rows",
  "arguments": {
    "items": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### synthesize_flow_cytometry

**Synthesize flow cytometry**: _What does this file support, read before any question is asked?_

What an FCS file supports before any question (dynamic synthesis): channel roles, the events at each channel's storable maximum, the logicle flowCore estimateLogicle fits to each fluorescence channel's instrument range, flowDensity deGate's density valleys per scaled channel, and every population's share of its parent with its exact (Clopper–Pearson, R binom.test) interval.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Each reading is the graded function it names, run on the same events.

**Does not:**
- Flow-rate anomalies and time drift are the Quality tools (check_flow_cytometry_quality), not repeated here.

**Validated:** against the reference implementation by 2 golden suites.

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
| `conf_level` | number |  | `0.95` | 0.5–0.999 | the confidence level of every population interval. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `channels` | any |  | per channel: role, events at maximum, the fitted logicle and the density valleys |
| `populations` | any |  | per population: count, % of parent and that share's exact interval |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "synthesize_flow_cytometry",
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

### target_decoy_qvalues

**Target decoy qvalues**: _What q-value does each peptide-spectrum match get by target-decoy competition, and how many pass a threshold?_

False discovery rate and q-values for peptide-spectrum matches by target-decoy competition (validated against pyteomics): give each match's score and whether it hit a decoy; returns every match's q-value, the whole set's FDR, and how many targets pass a q-value threshold. Supports the +1 and finite-sample corrections of Levitsky et al. 2017.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Decoys are a fair null for the targets, and the search was the same for both.

**Does not:**
- An FDR is a property of the whole set at a threshold, not a probability for one match.
- The +1 and finite-sample corrections change the numbers, and the answer says which was used.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `scores` | number[] | **yes** |  |  | one score per match. |
| `isDecoy` | boolean[] | **yes** |  |  | one flag per match: true when it is a decoy hit. |
| `higherIsBetter` | boolean |  | `true` |  | true for scores like HyperScore; false for e-values and PEPs. |
| `formula` | `1` · `2` |  | `2` |  | 1: decoys / targets. 2: (decoys + estimated false targets) / all matches. |
| `ratio` | number |  | `1` |  | decoy-to-target database size ratio. |
| `correction` | number |  | `0` |  | 0 none; 1 the +1 correction; 2 finite-sample expectation; a value in (0, 1) is a confidence level. |
| `threshold` | number |  | `0.01` |  | q-value cut-off for the accepted count. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `q` | any |  | q-value per match, in input order |
| `fdr` | number or null |  | FDR of the whole set |
| `accepted` | number or null |  | target matches at or under the q-value threshold |
| `threshold` | number or null |  | the q-value cut-off `accepted` was counted at |
| `targets` | number or null |  | how many target matches were scored |
| `decoys` | number or null |  | how many decoy matches were scored; the FDR estimate stands on this count |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "target_decoy_qvalues",
  "arguments": {
    "scores": [],
    "isDecoy": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### test_cytometry_spatial_interactions

**Test cytometry spatial interactions**: _Which cell types sit next to each other more, or less, often than a random arrangement of the same cells?_

imcRtools' testInteractions on a project single-cell table (imaging mass cytometry, CODEX, MIBI): per image, a k-nearest or radius neighbour graph on the cell centroids, then for every ordered pair of cell types a neighbourhood statistic (classic, histoCAT conditional, patch or interaction share) against permutations of the cell-type labels within the image; p (smaller side), z-score and the interaction or avoidance call.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Cells are exchangeable within an image: the null keeps every position and permutes the labels.

**Does not:**
- The neighbour graph is exact brute force; BiocNeighbors' tie order in kNN is not reproduced. p-values are not corrected across pairs.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `table` | string |  | `""` |  | the project cell table (CSV or TSV, one row per cell). |
| `image` | string |  | `""` |  | the image column; empty to guess it. |
| `x` | string |  | `""` |  | the centroid X column; empty to guess it. |
| `y` | string |  | `""` |  | the centroid Y column; empty to guess it. |
| `label` | string |  | `""` |  | the cell-type column; empty to guess it. |
| `graph` | `"knn"` · `"expansion"` |  | `"knn"` |  | k nearest cells, or every cell within a radius. |
| `neighbours` | number |  | `3` | ≥ 1 | neighbours per cell. |
| `radius` | number |  | `20` | ≥ 0 | the expansion radius, in position units. |
| `interaction_statistic` | `"classic"` · `"conditional"` · `"patch"` · `"interaction"` |  | `"classic"` |  | the neighbourhood statistic. |
| `patch_size` | number |  | `3` | ≥ 1 | patch: to-type neighbours a cell needs. |
| `permutations` | number |  | `1000` | ≥ 1 | label permutations. |
| `interaction_p` | number |  | `0.01` | ≥ 0 | significance threshold. |
| `spatial_seed` | number |  | `123` |  | the R seed. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `pairs` | any |  | per image and ordered type pair: statistic, p, z and the call |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "test_cytometry_spatial_interactions",
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

### translate_sequence

**Translate sequence**: _What protein does this DNA encode, under the genetic code chosen?_

Translate the subject DNA to protein (Biopython `Bio.Seq.translate` semantics). The SUBJECT is the selection when there is one, the named feature when `feature` is given, and the whole record otherwise — the `region` output says which, so never paste bases in to scope it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The region translated is in frame, as the `region` output states.
- Biopython's translate semantics for ambiguity, stops and partial codons.

**Does not:**
- Translates what it is given; it does not find the reading frame or the start codon.

**Not read from this result:** A transform: the protein a reading frame encodes under the genetic code given, with nothing inferred.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `table` | number |  | `1` | 1–33 | NCBI genetic-code table id (1 = standard). |
| `to_stop` | boolean |  | `false` |  | stop at the first stop codon instead of emitting the stop symbol. |
| `cds` | boolean |  | `false` |  | strict CDS: require a length multiple of 3, a start codon and a terminal stop (errors otherwise). Advanced. |
| `feature` | string |  |  |  | translate this annotated coding feature by NAME instead of the selection (e.g. "ADH1"). A name the record does not annotate is refused with the names it does. |
| `reverse` | boolean |  |  |  | read the region as the reverse complement. Stated explicitly this always wins; left out, the selection's or the feature's own strand decides. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `protein` | string |  | the translated protein |
| `length` | number |  | protein length in residues |
| `region` | string |  | what was translated, and on which strand |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "translate_sequence",
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
