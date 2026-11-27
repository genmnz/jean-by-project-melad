# 🎛️ Design & expression

_Codon optimisation, RBS and operons, probes, barcodes, genetic circuits and annotation._

42 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`annotate_region`](#annotate_region) | What genes, transcripts and dosage-sensitive regions does this genomic region overlap or contain? |
| [`audit_barcodes`](#audit_barcodes) | What minimum distance does this index set have, how many errors does that correct, and which subset survives a stricter budget? |
| [`audit_cds_annotations`](#audit_cds_annotations) | Does every annotated CDS of a map translate cleanly from its own bases and genetic code? |
| [`auto_annotate`](#auto_annotate) | Which known parts (vector elements, origins, markers, tags, lox and att sites) does this sequence carry, and where? |
| [`back_translate`](#back_translate) | What coding sequence encodes this protein under this host's codon usage and this rule? |
| [`build_codon_table_from_cds`](#build_codon_table_from_cds) | What codon usage does this genome show, across its highly-expressed genes or all of them? |
| [`build_ena_submission`](#build_ena_submission) | What flat file and manifest does ENA's Webin-CLI take for this record, and what would its validator refuse? |
| [`build_genbank_submission`](#build_genbank_submission) | What submission set (fasta with source modifiers and a feature table) does NCBI's table2asn take for this record, and what had to be refused or migrated? |
| [`calculate_power`](#calculate_power) | How many replicates does a planned test need to detect an effect, or what power, detectable effect or significance level does a fixed design give? |
| [`calculate_rnaseq_power`](#calculate_rnaseq_power) | How many biological replicates, or how much sequencing depth, does an RNA-seq comparison need to detect a fold change in one gene? |
| [`check_color_balance`](#check_color_balance) | Will the sequencer see a signal in every channel at every index cycle for these indexes, on each chemistry? |
| [`check_index_pool`](#check_index_pool) | Will this pool of sample indexes sequence: duplicates, length, pairwise distance, color balance and hopping risk? |
| [`check_manufacturability`](#check_manufacturability) | Does this sequence meet what a named synthesis vendor publishes it can make: length, GC, homopolymers and repeats? |
| [`check_scorpion_stem`](#check_scorpion_stem) | Does a Scorpion probe's stem melt below the loop-target duplex by the margin the design needs? |
| [`codon_optimality`](#codon_optimality) | What share of this CDS's codons are the optimal ones for this host (Fop)? |
| [`codon_table_fetch`](#codon_table_fetch) | What is this organism's codon usage, counted from its annotated CDS or as a published table? |
| [`codon_usage_analysis`](#codon_usage_analysis) | How does this CDS's codon usage compare with an organism's: CAI, GC, rare codons, and the two reference-free bias measures? |
| [`codon_usage_distance`](#codon_usage_distance) | How far is this region's codon usage from the record's other genes (CUFS)? |
| [`debarcode_mass_cytometry`](#debarcode_mass_cytometry) | Which barcoded sample does each event of a pooled mass cytometry acquisition belong to? |
| [`design_barcodes`](#design_barcodes) | Which index set of this size has a guaranteed minimum distance, and what does it actually correct? |
| [`design_codon_tiling_primers`](#design_codon_tiling_primers) | Which primers tile this CDS, one degenerate codon per position, inside a Tm window? |
| [`design_free_codes`](#design_free_codes) | Which barcodes of this length correct this many insertions, deletions and substitutions? |
| [`design_gene_fragment_order`](#design_gene_fragment_order) | What sheet does IDT's gene-fragment plate upload take for these fragments, and which of them can the product not be ordered as? |
| [`design_genetic_circuit`](#design_genetic_circuit) | Which characterised repressor gates compute this logic function — given as a named gate, a truth table or a Verilog module — with what ON/OFF dynamic range, and what DNA does the circuit need? |
| [`design_hcr_probes`](#design_hcr_probes) | Which HCR v3.0 split-initiator probe pairs tile this target within their composition and free-energy windows? |
| [`design_ish_probes`](#design_ish_probes) | Which oligo set images this target best: tiled candidates meeting Tm, GC and composition, screened for off-target binding and abundant k-mers, and gathered into a set? |
| [`design_knockout_package`](#design_knockout_package) | What does a complete knockout or knock-in build need: guides, an off-target census, a repair template with arms, screening primers outside the arms, the protocol, and what to buy? |
| [`design_merfish_probes`](#design_merfish_probes) | Which encoding probes make this transcript readable in a MERFISH experiment under this codeword, and how specific is each? |
| [`design_oligo_plate_order`](#design_oligo_plate_order) | In which wells, in the supplier's own fill order, does an oligo set go on a plate order? |
| [`design_padlock_probes`](#design_padlock_probes) | Which padlock probes target this transcript for in-situ sequencing, and which junctions could be ligated on another transcript? |
| [`design_rbs`](#design_rbs) | Which 5'UTR puts a CDS's translation initiation at a target strength? |
| [`design_xenium_probes`](#design_xenium_probes) | Which 40 nt targets of this transcript meet 10x's Xenium custom-panel rules, and which would another transcript also bind? |
| [`discover_annotation_contradictions`](#discover_annotation_contradictions) | Which signal peptides or transmembrane segments in reviewed human UniProt does a sequence predictor contradict? |
| [`discover_codon_outliers`](#discover_codon_outliers) | Which genes of a genome use synonymous codons in a way the genome's own average does not explain? |
| [`estimate_effect_size`](#estimate_effect_size) | How large is the effect in pilot data, standardized, with a confidence interval, ready to size the full experiment? |
| [`export_barcodes`](#export_barcodes) | What does this index set look like as an order sheet, a FASTA, a SampleSheet, or the actual oligos? |
| [`optimize_sequence`](#optimize_sequence) | What sequence satisfies these constraints and scores best on these objectives? |
| [`rank_next_tests`](#rank_next_tests) | Which candidate experiment would teach the most about the hypothesis it is registered against, and how much of it is worth running? |
| [`rank_tradeoffs`](#rank_tradeoffs) | Which candidates in a table does no other candidate beat on every objective at once, how deep does each of the rest sit, and which candidate beats it? |
| [`score_rbs`](#score_rbs) | How strong is the ribosome-binding site already in front of this start codon, and what sets that strength? |
| [`simulate_rnaseq_power`](#simulate_rnaseq_power) | For a two-group RNA-seq experiment analyzed with edgeR, what power and false discovery rate does each number of replicates actually achieve, for genes at each expression level, and how would more sequencing depth chan… |
| [`tree_taxon_annotations`](#tree_taxon_annotations) | What does this NeXML file say about each of its taxa? |

---

### annotate_region

**Annotate region**: _What genes, transcripts and dosage-sensitive regions does this genomic region overlap or contain?_

Say what a genomic region holds in the reference tracks: the genes and RefSeq transcripts it overlaps, which complete coding sequences it CONTAINS (the only case where a residue-level design is honest), the DGV structural variants seen there in control populations with their frequencies, and how much of it lies in segmental duplications and how similar the best paralogue is. Every track answers with its authority, table and retrieval date. Coordinates are 1-based and inclusive, as a person writes chr17:41196312-41277500.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The reference tracks for the build named.

**Does not:**
- Only the bundled tracks.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `build` | string | **yes** |  |  | the assembly the coordinates are on, by the UCSC name the cached tracks use (hg19, hg38). A build with no cached track is refused by name rather than answered empty. |
| `chromosome` | string | **yes** |  |  | UCSC-style sequence name; a bare `17` or `X` is read as `chr17`/`chrX`. |
| `start` | number | **yes** |  | ≥ 1 | first base of the region, 1-based. |
| `end` | number | **yes** |  | ≥ 1 | last base of the region, 1-based and inclusive. |
| `dosage` | `"any"` · `"loss"` · `"gain"` |  | `"any"` |  | which DGV evidence is comparable: `loss` for a deletion call, `gain` for a duplication, `any` for either. Balanced and unclassified variant types (insertions, inversions) are never counted as dosage evidence, and the count of them is reported instead. Values: any (Either direction), loss (Loss), gain (Gain). |
| `tracks` | string |  |  |  | which tracks to read, comma-separated: `genes`, `dgv`, `segdups`. Unset reads all three. The coding verdict comes with `genes`. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | what each track answered for this region, generated from the run |
| `genes` | any |  | overlapping gene symbols, the ones with coding sequence in the region, and every transcript with the exons it touches; carries the track provenance |
| `coding` | any |  | the coding verdict (none, noncoding, partial, whole), the complete CDSs the region contains, the partial ones with how much of each it holds, and the reason a residue-level action is refused when it is |
| `dgv` | any |  | DGV records of comparable dosage with study, sample size, frequency and reciprocal overlap; the fraction of the region they cover; how many balanced or unclassified records were not counted; the track provenance |
| `segdups` | any |  | segmental duplications overlapping the region with their partner locus and identity, the fraction of the region they cover, and the track provenance |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "annotate_region",
  "arguments": {
    "build": "<string>",
    "chromosome": "<string>",
    "start": "<number>",
    "end": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### audit_barcodes

**Audit barcodes**: _What minimum distance does this index set have, how many errors does that correct, and which subset survives a stricter budget?_

Check an index set you ALREADY have, rather than designing a new one: the minimum distance between any two, how many errors that guarantees correcting, the full distance matrices, and — optionally — the subset that survives pruning to a stricter error budget. This is the question asked of a set inherited from a kit or a previous experiment.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The distance measure chosen (Hamming, Levenshtein or sequence-Levenshtein) matches the error model of the platform.

**Does not:**
- A guaranteed correction radius is a combinatorial property of the set, not a measured error rate.
- Audits a set you have; design_barcodes makes one.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `barcodes` | string[] | **yes** |  |  | the index sequences to audit. |
| `metric` | `"hamming"` · `"seqlev"` · `"levenshtein"` |  | `"seqlev"` |  | error model to audit against — a set safe under substitutions may be unsafe under indels. Values: hamming (Hamming (substitutions)), seqlev (Sequence-Levenshtein (indels)), levenshtein (Levenshtein). |
| `required_distance` | number |  | `3` | 2–10 | the minimum distance the set is supposed to have — the audit says whether it does. |
| `prune_to_errors` | number |  | `0` | 0–4 | also report the subset that would survive pruning to a free code correcting this many errors. 0 = do not prune. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `audit` | any |  | the verdict: the set's real minimum distance, what it guarantees, and every pair that falls short |
| `analysis` | any |  | per-metric analysis of the whole set |
| `matrices` | any |  | the pairwise distance matrix under each metric |
| `distanceMap` | object or null |  | the pairwise distance matrix under the chosen metric, as a heatmap |
| `distanceMap.rows` | string[] |  |  |
| `distanceMap.cols` | string[] |  |  |
| `distanceMap.values` | ((number or null)[])[] |  |  |
| `distanceMap.label` | string |  |  |
| `distanceMap.title` | string |  |  |
| `distanceHistogram` | object or null |  | how many PAIRS sit at each distance under the chosen metric: the shape behind the minimum |
| `distanceHistogram.x` | number[] |  |  |
| `distanceHistogram.series` | object[] |  |  |
| `distanceHistogram.series[].name` | string |  |  |
| `distanceHistogram.series[].y` | (number or null)[] |  |  |
| `distanceHistogram.xLabel` | string |  |  |
| `distanceHistogram.yLabel` | string |  |  |
| `distanceHistogram.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `distanceHistogram.title` | string |  |  |
| `distanceHistogram.rules` | object[] |  |  |
| `distanceHistogram.rules[].y` | number |  |  |
| `distanceHistogram.rules[].label` | string |  |  |
| `neighbourHistogram` | object or null |  | how many BARCODES have each nearest-neighbour distance: where the weak links are |
| `neighbourHistogram.x` | number[] |  |  |
| `neighbourHistogram.series` | object[] |  |  |
| `neighbourHistogram.series[].name` | string |  |  |
| `neighbourHistogram.series[].y` | (number or null)[] |  |  |
| `neighbourHistogram.xLabel` | string |  |  |
| `neighbourHistogram.yLabel` | string |  |  |
| `neighbourHistogram.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `neighbourHistogram.title` | string |  |  |
| `neighbourHistogram.rules` | object[] |  |  |
| `neighbourHistogram.rules[].y` | number |  |  |
| `neighbourHistogram.rules[].label` | string |  |  |
| `gcHistogram` | object or null |  | how many barcodes sit at each GC percentage |
| `gcHistogram.x` | number[] |  |  |
| `gcHistogram.series` | object[] |  |  |
| `gcHistogram.series[].name` | string |  |  |
| `gcHistogram.series[].y` | (number or null)[] |  |  |
| `gcHistogram.xLabel` | string |  |  |
| `gcHistogram.yLabel` | string |  |  |
| `gcHistogram.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `gcHistogram.title` | string |  |  |
| `gcHistogram.rules` | object[] |  |  |
| `gcHistogram.rules[].y` | number |  |  |
| `gcHistogram.rules[].label` | string |  |  |
| `baseComposition` | object or null |  | the fraction of the set reading each base at each cycle |
| `baseComposition.x` | number[] |  |  |
| `baseComposition.series` | object[] |  |  |
| `baseComposition.series[].name` | string |  |  |
| `baseComposition.series[].y` | (number or null)[] |  |  |
| `baseComposition.xLabel` | string |  |  |
| `baseComposition.yLabel` | string |  |  |
| `baseComposition.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `baseComposition.title` | string |  |  |
| `baseComposition.rules` | object[] |  |  |
| `baseComposition.rules[].y` | number |  |  |
| `baseComposition.rules[].label` | string |  |  |
| `statistics` | any |  | the whole-set statistics the four charts above are drawn from, which a min-distance figure hides: GC mean, spread and range, Shannon entropy per cycle, the fraction reading each base at each cycle, groups sharing a prefix in the first cycles read, duplicates, and the per-metric distance distributions |
| `kept` | any |  | the barcodes surviving `prune_to_errors` (the whole set when pruning is off) |
| `dropped` | number |  | how many the prune removed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "audit_barcodes",
  "arguments": {
    "barcodes": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### audit_cds_annotations

**Audit CDS annotations**: _Does every annotated CDS of a map translate cleanly from its own bases and genetic code?_

Check every annotated CDS of one or more GenBank maps against its own bases and genetic code: a frame that does not close (frameshift), a stop inside the reading frame, a first codon the code cannot start with, a last codon that is not a stop, and a /translation the bases do not give. A partial end (< or >) is not judged, and a /pseudo CDS carries no flag. Where an annotation ends without a stop it reads on in frame (round the origin of a circular map) to the first stop and says how many codons that adds, whether it runs into another annotated CDS (a fusion annotated in pieces) and the read-through a random backbone of the same composition would give. Extraction and translation match Biopython on all 1,871 CDS of 695 NCBI vector records.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The /transl_table qualifier, or the record's default, is the code the CDS uses.

**Does not:**
- Partial ends and /pseudo CDS are not judged.
- A flag says the annotation and the bases disagree, not which one is wrong.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `genbank` | string[] | **yes** |  |  | the GenBank files' contents, one string per file (a file may hold several records). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `flags` | any |  | per flag, how many CDS carry it and in how many records |
| `flagged` | any |  | every CDS with a flag: record, feature, label, location and the flags |
| `readThrough` | any |  | every annotation that ends without a stop, with where reading on stops |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "audit_cds_annotations",
  "arguments": {
    "genbank": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### auto_annotate

**Auto annotate**: _Which known parts (vector elements, origins, markers, tags, lox and att sites) does this sequence carry, and where?_

Find and name known features on the subject — vector parts, origins, resistance markers and tags — by exact match, by local alignment (which finds a diverged copy and reports the identity and coverage that earned it), or by both, on either strand and across the origin, plus Cre/loxP and Gateway att recognition sites. Emits an annotated record, so a downstream map or export carries the annotations.

<sub>returns new records · runs locally on the engine · long-running</sub>

**Assumes:**
- The bundled feature libraries are the reference set.
- Exact match and local alignment under the identity and coverage cutoffs given.

**Does not:**
- A part absent from the libraries cannot be found; a diverged copy is reported with its identity, not named as exact.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `libraries` | string[] |  | `[]` |  | which feature corpora to search, by id (an id from annotation-library/manifest.json, or "legacy" for the unsourced set). Empty means the ones the panel starts with, which is every corpus but the two it leaves off for their size, AMRFinderPlus and Rfam; name those to search them too. |
| `policy` | `"merge"` · `"overwrite"` · `"clear"` |  | `"merge"` |  | what the emitted record does with the features it already had: `merge` keeps them all and skips a hit already there to the base, `overwrite` replaces a same-strand feature a hit overlaps, `clear` drops every existing feature first. |
| `lox_p` | boolean |  | `true` |  | detect Cre/loxP-family recognition sites. |
| `gateway` | boolean |  | `false` |  | detect Gateway att recombination sites. |
| `greedy_gateway` | boolean |  | `false` |  | permissive att core matching — finds more sites, including partial ones. Only applies when gateway is true. Advanced. |
| `mode` | `"exact"` · `"alignment"` · `"both"` |  | `"both"` |  | how to match a library entry: "exact" finds only a sequence spelled byte for byte, "alignment" finds a diverged copy and reports its identity and coverage, "both" runs each and keeps what only the other found. |
| `min_pi_per_match` | number |  | `3` |  | lowest identity-weighted coverage worth reporting; upstream's own floor is 3, below which a hit is a fragment of a composite feature rather than the feature. Only applies when mode is alignment or both. Advanced. |
| `accepted_only` | boolean |  | `false` |  | keep only hits clearing the corpus authority's own acceptance policy (>=95% identity, with a coverage bar that depends on the feature's length). Also decides overlaps: a hit the authority would reject cannot displace one it would accept. Only applies when mode is alignment or both. Advanced. |
| `hide_fragments` | boolean |  | `false` |  | hide hits covering under 95% of their database entry, which upstream calls fragments. Only applies when mode is alignment or both. Advanced. |
| `max_expect` | number |  | `1e-05` |  | protein corpora only: the E-value a translated (six-frame) match must beat to be reported. It also sets the score the search runs at, so a stricter cutoff is a faster scan. Advanced. |
| `min_identity` | number |  | `0` |  | protein corpora only: drop a translated call under this percent identity over the residues aligned. Advanced. |
| `min_coverage` | number |  | `50` |  | protein corpora only: drop a translated call covering less than this much of the database protein's own length. Advanced. |
| `alternatives` | number |  | `4` |  | protein corpora only: how many runners-up to keep on each call, so a near relative is reported rather than implied. Advanced. |
| `genetic_code` | number |  | `1` |  | protein corpora only: the NCBI translation table the six frames are read under. 1 is the standard code. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the subject with the found features added |
| `features` | any |  | every feature found, with its source detector |
| `featureCount` | number |  | how many features were found |
| `perSource` | any |  | hit count per detector |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "auto_annotate",
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

### back_translate

**Back translate**: _What coding sequence encodes this protein under this host's codon usage and this rule?_

Protein → DNA: the coding sequence that would encode a protein, weighted by a real codon-usage table. Four rules — the host's most-frequent codon (EMBOSS backtranseq), a draw from the family's real frequency distribution, the IUPAC-degenerate consensus for primers/probes (EMBOSS backtranambig), or DnaChisel's table-free first codon. It does NOT optimize: for restriction-site avoidance, a GC target or repeat removal, follow it with optimize_sequence.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The codon-usage table and genetic code named.
- The `seed` fixes the weighted draw.

**Does not:**
- Does not optimize for restriction sites, GC or repeats; that is optimize_sequence.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence, one-letter codes (B/Z/J/U/O/X and gaps are handled and reported); wire it from translate_sequence. |
| `strategy` | `"mostFrequent"` · `"weightedRandom"` · `"ambiguous"` · `"firstCodon"` |  | `"mostFrequent"` |  | mostFrequent — EMBOSS backtranseq, and SnapGene's “Preferred Codons”: every residue takes its host's single most-used codon. \| weightedRandom — Each residue is drawn from its family's real frequency distribution: a natural-looking gene rather than a run of one codon. \| ambiguous — EMBOSS backtranambig: one ambiguity-coded codon covering EVERY codon for the residue. The degenerate-primer answer; needs no usage table. \| firstCodon — DnaChisel's reverse_translate. Deterministic and table-free, but it is not a biological preference: use it only to reproduce a DnaChisel result. |
| `host` | `"E. coli K-12"` · `"H. sapiens"` · `"S. cerevisiae"` |  | `"E. coli K-12"` |  | codon-usage table to weight by, named as the workbench knows it. Required for the two table-driven strategies and ignored by the other two. Tables loaded in the Back-translate or Optimizer panel this session are valid names as well as the bundled ones. Only applies when strategy is mostFrequent or weightedRandom. |
| `table` | `"Standard"` · `"Bacterial"` · `"Vertebrate Mitochondrial"` |  | `"Standard"` |  | genetic code the codons are chosen under. |
| `append_stop` | boolean |  | `false` |  | append a stop codon, chosen by the same strategy and table as every other codon. Skipped when the residues already end in *. |
| `seed` | number |  |  |  | seed for the usage-weighted draw, which makes a sampled design reproducible. Omit for an unseeded draw; ignored by the three deterministic rules. Only applies when strategy is weightedRandom. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `dna` | string |  | the coding sequence — wire it into optimize_sequence, or open it as a record |
| `gc` | number |  | GC fraction of the product (0–1), over unambiguous bases only |
| `residues` | any |  | every residue with the codon chosen, its share of its synonymous family, and why if it took a special path |
| `unweightedResidues` | any |  | residues whose synonymous family carried NO weight in this table, so codon order decided the answer rather than usage — empty is the healthy case |
| `undefinedResidues` | any |  | residues the genetic code has no codon for; each became NNN |
| `conclusion` | string |  | one generated sentence saying what this product IS — size, GC, and how adapted it is to the table you named. Built from the run by the same `conclusionOf` the panel headlines, so a turn and the panel cannot state different things about one design |
| `cautions` | any |  | only the caveats THIS product earned, each with its measurement and whose published limit it crossed — an empty list is the healthy case and is not padded |
| `provenance` | any |  | the assumptions the answer rests on: strategy, genetic code, codon-usage table and residue count — the same facts the panel prints under the product |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "back_translate",
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

### build_codon_table_from_cds

**Build codon table from CDS**: _What codon usage does this genome show, across its highly-expressed genes or all of them?_

Build a codon-usage table from a genome's CDS FASTA (an NCBI `cds_from_genomic.fna`): either from its highly-expressed genes — the ribosomal proteins, which is what a codon-optimization reference table means — or from every CDS in the genome. Returns the table as a Kazusa-style TSV that optimize_sequence, codon_usage_analysis and design_expression_variants all take, with the accounting of how many CDSs went into it.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The FASTA is in-frame CDS records, as NCBI writes `cds_from_genomic.fna`.
- Highly-expressed means the ribosomal proteins, recognized from the record headers.

**Does not:**
- HEG mode selects by HEADER text: a FASTA whose deflines do not name genes has no ribosomal proteins to find, and the refusal says so rather than returning the genome table under the HEG label.
- An amino acid absent from the HEG set is backfilled from the whole genome, and every backfilled residue is named.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | the CDS FASTA to read, by name, from the project or the `_files` sent with the call. Empty reads the only FASTA there. |
| `fasta` | string |  |  |  | or the CDS FASTA itself, in frame, one record per CDS. |
| `mode` | `"heg"` · `"genome"` |  | `"heg"` |  | `heg` builds the table from the ribosomal-protein genes, which is the reference set a codon-optimization table means. `genome` uses every CDS, which is the honest choice for a plasmid or any corpus whose highly-expressed genes are not in it. Values: heg (Highly-expressed genes (ribosomal proteins)), genome (Every CDS in the corpus). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `tsv` | string |  | the usage table as a Kazusa-style TSV — wire it into optimize_sequence, codon_usage_analysis or design_expression_variants |
| `mode` | string |  | which reference set this table was built from |
| `cdsUsed` | number |  | CDS records that went into the table |
| `cdsTotal` | number |  | CDS records read from the corpus |
| `codons` | number |  | codons counted |
| `gc3` | number | % | GC at the third codon position of the reference set, the usual summary of a genome’s codon bias |
| `backfilled` | any |  | amino acids absent from the highly-expressed set, taken from the whole genome instead. Empty in genome mode |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "build_codon_table_from_cds",
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

### build_ena_submission

**Build ENA submission**: _What flat file and manifest does ENA's Webin-CLI take for this record, and what would its validator refuse?_

Turn a record into what ENA's Webin-CLI takes for an annotated sequence (`-context sequence`): an ENA flat file (`.embl`) and its manifest. Features are checked against the tables ENA's own validator reads, so what Webin-CLI would refuse (an unknown key, a missing mandatory qualifier, a double quote in a value, a duplicate feature) is refused or rewritten here, by name. A description under 10 characters, an entry under 100 bp and a missing study are reported first. It WRITES FILES and sends nothing.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- ENA's feature and qualifier tables are those its own validator reads, as cached.

**Does not:**
- Builds the files; Webin-CLI's own validation and the upload are not run here.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `genbank` | string | **yes** |  |  | the record to submit, as GenBank text. Its features, topology and DEFINITION are read from it. |
| `study` | string |  | `""` |  | the Webin Portal study accession (PRJEB… or ERP…). Webin-CLI refuses a set without one; left empty, the files are written and the reason reported. |
| `description` | string |  | `""` |  | the DE line, what the sequence is. Left empty, each record's own DEFINITION is used; ENA refuses one shorter than 10 characters. |
| `collection_date` | string |  | `"missing: lab stock"` |  | when the sample was collected, on the source feature. Optional, but must be INSDC-legal; a construct takes a missing-value term such as `missing: lab stock`. |
| `geo_loc_name` | string |  | `"missing: lab stock"` |  | where the sample came from, from the INSDC vocabulary, or a missing-value term. |
| `organism` | string |  | `"synthetic construct"` |  | the scientific name of the source organism; ENA checks it against its taxonomy. `synthetic construct` is a real answer for a built vector. |
| `mol_type` | `"genomic DNA"` · `"genomic RNA"` · `"mRNA"` · `"rRNA"` · `"tRNA"` · `"other RNA"` · `"other DNA"` · `"transcribed RNA"` · `"viral cRNA"` · `"unassigned DNA"` · `"unassigned RNA"` |  | `"other DNA"` |  | the source feature's mandatory /mol_type. `other DNA` is the INSDC value for a synthetic construct. |
| `topology` | `""` · `"circular"` · `"linear"` |  | `""` |  | circular for a plasmid (the ID line; only then may a feature cross the origin). Left empty, the record's own topology is used. Values:  (From the record), circular (Circular), linear (Linear). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `files` | any |  | the flat file and its manifest, each with its `name` and `text`. Gzip the flat file before running Webin-CLI; the manifest already names the `.gz` |
| `flatFile` | string |  | the `.embl` alone, for reading or diffing |
| `changes` | any |  | every feature the writer refused, rewrote or left a qualifier off, each with ENA's reason |
| `problems` | any |  | why Webin-CLI will refuse the set as it stands: a short description, a short entry, no study, or a malformed date or locality. Empty means none of those, never that the validator will be silent |
| `written` | number |  | features written, source excluded |
| `command` | string |  | the exact gzip and webin-cli invocation, with -validate |
| `reading` | string |  | what the set is, generated from what was written |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "build_ena_submission",
  "arguments": {
    "genbank": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### build_genbank_submission

**Build GenBank submission**: _What submission set (fasta with source modifiers and a feature table) does NCBI's table2asn take for this record, and what had to be refused or migrated?_

Turn a record into the SUBMISSION SET NCBI's `table2asn` consumes: a `.fsa` whose defline carries the source modifiers, and a 5-column feature table (`.tbl`) beside it. This is not a GenBank export — GenBank's submission pipeline takes neither a `.gb` nor a plain fasta. Its real work is REFUSING and MIGRATING what GenBank will not accept: twelve feature keys were retired in 2014 in favour of `regulatory` (promoter, terminator and RBS among them, so every plasmid map is affected), a qualifier not on a key's approved list is dropped by name, and an unapproved key is kept as a `misc_feature` carrying its original name. Since December 2024 GenBank has required `collection_date` and `geo_loc_name` on every submission, and both are validated here against the INSDC vocabularies BEFORE a file is written. It WRITES FILES and sends nothing: no account, no key, no upload — `table2asn` stays yours to run, and the submission template it also wants is yours to make.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The feature keys and qualifiers GenBank accepts are the current INSDC tables the builder carries.

**Does not:**
- Builds the files; the submission itself and NCBI's own validation are not run here.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `genbank` | string | **yes** |  |  | the record to submit, as GenBank text. Its features and topology are read from it — wire it from an export, or paste it. |
| `collection_date` | string |  | `"missing: lab stock"` |  | when the sample was collected. MANDATORY on every GenBank submission since December 2024. `DD-Mmm-YYYY`, `Mmm-YYYY`, `YYYY`, an ISO form, or two of them separated by `/` for a range. A construct that was never collected anywhere takes an INSDC missing-value term such as `missing: lab stock`. |
| `geo_loc_name` | string |  | `"missing: lab stock"` |  | where the sample came from: a country, ocean or sea from the INSDC vocabulary, optionally `:region` and `, locality`. MANDATORY since December 2024, and it takes the same missing-value terms. |
| `organism` | string |  | `"synthetic construct"` |  | the scientific name of the source organism. `synthetic construct` is a real answer for a built vector, not an absence. |
| `mol_type` | `"genomic DNA"` · `"genomic RNA"` · `"mRNA"` · `"rRNA"` · `"tRNA"` · `"other RNA"` · `"other DNA"` · `"transcribed RNA"` · `"viral cRNA"` · `"unassigned DNA"` · `"unassigned RNA"` |  | `"genomic DNA"` |  | one of INSDC's two MANDATORY qualifiers on the source key. Omitting it lets table2asn choose, which is a scientific fact picked by a tool. |
| `topology` | `""` · `"circular"` · `"linear"` |  | `""` |  | circular for a plasmid. With this omitted table2asn writes `linear` into the LOCUS line, so a plasmid is deposited as a linear molecule with no error anywhere. Left empty, the record's own topology is used. Values:  (From the record), circular (Circular), linear (Linear). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `files` | any |  | the submission set: one entry per file, each with its `name` and `text`. The two names share a basename, which is how table2asn pairs them |
| `featureTable` | string |  | the `.tbl` alone, for pasting or diffing |
| `changes` | any |  | every feature the writer migrated, relabelled, refused or stripped a qualifier from, each with the authority's reason. Never empty-because-nothing-was-checked |
| `problems` | any |  | why the set cannot be submitted as it stands — an illegal collection date or a locality outside the vocabulary. Empty means the two mandatory modifiers are good, never that NCBI will be silent |
| `written` | number |  | features written into the table. Branch on this rather than counting `changes` |
| `command` | string |  | the exact table2asn invocation for the set, naming the submission template the user must make first |
| `reading` | string |  | what the set is, generated from the record that was written rather than from the request |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "build_genbank_submission",
  "arguments": {
    "genbank": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### calculate_power

**Calculate power**: _How many replicates does a planned test need to detect an effect, or what power, detectable effect or significance level does a fixed design give?_

Power and sample size for a planned experiment: how many replicates a test needs to detect an effect, or what power, detectable effect or significance level a design that is already fixed gives. Leave ONE quantity out with `solve_for` and it is solved; everything else is given. Thirteen tests in two families: Cohen's standardized effect sizes (pwr 1.3-0: t one/two-sample/paired and unequal n, one and two proportions by arcsine h, normal mean, correlation, chi-square w, one-way ANOVA f, linear-model f²) and raw units (R's power.t.test from a difference and SD, power.prop.test from two proportions, power.anova.test from variances). Every number is R's, reproduced: the solved value is uniroot's root at R's tolerance, and an unreachable target is refused with R's own message. Returns the power curve around the answer and the R call that reproduces it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The test named is the test the experiment will run, on independent observations.
- The effect size is the true one: a pilot or literature estimate carries its own uncertainty into the answer.
- The t tests assume normal errors (equal variances unless the unequal-n form is chosen); the proportion tests use the normal approximation (arcsine h for pwr, R's power.prop.test otherwise).

**Does not:**
- A sample size is a minimum for the stated power, not a guarantee: attrition, dropout and failed samples are not included.
- No multiple-testing adjustment is made; pass the per-test significance level the analysis will use.
- Count data (RNA-seq) is calculate_rnaseq_power's question, not this one's.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `test` | `"t"` · `"t_unequal"` · `"two_proportions"` · `"two_proportions_unequal"` · `"one_proportion"` · `"normal_mean"` · `"correlation"` · `"chisq"` · `"anova"` · `"linear_model"` · `"t_raw"` · `"proportions_raw"` · `"anova_raw"` | **yes** |  |  | which test the experiment will be analyzed with; the power answer belongs to that test and no other. Values: t (t test: one-sample, two-sample or paired, Cohen's d), t_unequal (two-sample t test, unequal group sizes, Cohen's d), two_proportions (two proportions, equal n, Cohen's h), two_proportions_unequal (two proportions, unequal n, Cohen's h), one_proportion (one proportion against a null value, Cohen's h), normal_mean (normal mean, known variance, effect d), correlation (Pearson correlation, r), chisq (chi-square goodness of fit or independence, Cohen's w), anova (balanced one-way ANOVA, Cohen's f), linear_model (linear model F test (multiple regression), Cohen's f²), t_raw (t test in raw units: difference and standard deviation), proportions_raw (two proportions in raw units: p1 and p2), anova_raw (balanced one-way ANOVA in raw units: between- and within-group variance). |
| `solve_for` | `"n"` · `"n1"` · `"n2"` · `"N"` · `"k"` · `"groups"` · `"u"` · `"v"` · `"effect"` · `"difference"` · `"sd"` · `"p1"` · `"p2"` · `"between_var"` · `"within_var"` · `"sig_level"` · `"power"` |  |  |  | the one quantity to solve. Left unset it is the test's sample size (n; n2 for unequal groups, N for chi-square, v for the linear model). `effect` solves the smallest detectable effect. |
| `effect` | number |  |  |  | the standardized effect: Cohen's d for t and normal-mean tests, h for proportions, r for correlation, w for chi-square, f for ANOVA, f² for the linear model. Give a value or `effect_size` instead. Only applies when test is t or t_unequal or two_proportions or two_proportions_unequal or one_proportion or normal_mean or correlation or chisq or anova or linear_model. |
| `effect_size` | `"small"` · `"medium"` · `"large"` |  |  |  | Cohen's conventional small, medium or large effect for this test (pwr's cohen.ES), when there is no estimate from data. A convention, not a measurement, and every answer built on it says so. Only applies when test is t or t_unequal or two_proportions or two_proportions_unequal or one_proportion or normal_mean or correlation or chisq or anova or linear_model. |
| `n` | number |  |  | ≥ 1 | observations per group (pairs, for paired; the sample, for one-sample and correlation). Only applies when test is t or two_proportions or one_proportion or normal_mean or correlation or anova or t_raw or proportions_raw or anova_raw. |
| `n1` | number |  |  | ≥ 2 | observations in the first group. Only applies when test is t_unequal or two_proportions_unequal. |
| `n2` | number |  |  | ≥ 2 | observations in the second group. Only applies when test is t_unequal or two_proportions_unequal. |
| `N` | number |  |  | ≥ 1 | total observations across every cell. Only applies when test is chisq. |
| `df` | number |  |  | ≥ 1 | degrees of freedom of the chi-square test: (cells − 1) for goodness of fit, (rows − 1)(columns − 1) for independence. Only applies when test is chisq. |
| `k` | number |  |  | ≥ 2 | number of groups. Only applies when test is anova. |
| `groups` | number |  |  | ≥ 2 | number of groups. Only applies when test is anova_raw. |
| `u` | number |  |  | ≥ 1 | numerator degrees of freedom: the number of predictors tested. Only applies when test is linear_model. |
| `v` | number |  |  | ≥ 1 | denominator degrees of freedom: n − u − 1 for n observations. Only applies when test is linear_model. |
| `difference` | number |  |  |  | δ, the true difference in means, in the measurement's units. Only applies when test is t_raw. |
| `sd` | number |  |  | ≥ 0 | the standard deviation, in the same units (of the differences, for paired); R's default is 1. Only applies when test is t_raw. |
| `p1` | number |  |  | 0–1 | the proportion in group 1. Only applies when test is proportions_raw. |
| `p2` | number |  |  | 0–1 | the proportion in group 2. Only applies when test is proportions_raw. |
| `between_var` | number |  |  | ≥ 0 | variance of the group means. Only applies when test is anova_raw. |
| `within_var` | number |  |  | ≥ 0 | variance within groups. Only applies when test is anova_raw. |
| `sig_level` | number |  | `0.05` | 0–1 | α, the type I error rate; R's default. |
| `power` | number |  |  | 0–1 | 1 − β, the chance of detecting the effect if it is real. No default: the target is yours to choose. |
| `alternative` | `"two.sided"` · `"less"` · `"greater"` · `"one.sided"` |  | `"two.sided"` |  | two-sided, or the direction a one-sided test looks in (the raw-unit t and proportion tests take only two.sided or one.sided). Only applies when test is t or t_unequal or two_proportions or two_proportions_unequal or one_proportion or normal_mean or correlation or t_raw or proportions_raw. |
| `type` | `"two.sample"` · `"one.sample"` · `"paired"` |  | `"two.sample"` |  | the t test's design. Only applies when test is t or t_raw. |
| `strict` | boolean |  | `false` |  | two-sided raw-unit tests: also count rejections in the wrong tail, as R's strict = TRUE. Only applies when test is t_raw or proportions_raw. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `solved` | string |  | which quantity was solved |
| `value` | number or null |  | the solved quantity's value |
| `power` | number or null |  | the power of the design |
| `values` | any |  | every quantity of the test, the solved one included, by R's name |
| `wholeUnits` | any |  | the sample size rounded up to whole units and the power that whole number gives |
| `powerCurve` | object or null |  | power against the sample size, every other quantity held |
| `powerCurve.x` | number[] |  |  |
| `powerCurve.series` | object[] |  |  |
| `powerCurve.series[].name` | string |  |  |
| `powerCurve.series[].y` | (number or null)[] |  |  |
| `powerCurve.xLabel` | string |  |  |
| `powerCurve.yLabel` | string |  |  |
| `powerCurve.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `powerCurve.title` | string |  |  |
| `powerCurve.rules` | object[] |  |  |
| `powerCurve.rules[].y` | number |  |  |
| `powerCurve.rules[].label` | string |  |  |
| `rCall` | string |  | the R call that reproduces the answer |
| `warnings` | any |  | R's own warnings for this solve, verbatim |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "calculate_power",
  "arguments": {
    "test": "t",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### calculate_rnaseq_power

**Calculate rnaseq power**: _How many biological replicates, or how much sequencing depth, does an RNA-seq comparison need to detect a fold change in one gene?_

Sample size and power for an RNA-seq comparison of two groups, one gene at a time: the biological replicates per group needed to detect a fold change at a given sequencing depth and within-group coefficient of variation, or the power, detectable fold change, CV or α a fixed design gives. Leave one of n, cv, effect, alpha and power out (or name it in `solve_for`). Every quantity takes a list, and the answer is the whole grid, so depth against replicates is one call. RNASeqPower 1.52.0 (Hart et al. 2013), reproduced: a negative binomial count with Poisson sequencing noise 1/depth plus biological variance CV².

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Counts are negative binomial with the stated biological coefficient of variation; RNASeqPower's normal approximation to the log-fold-change test.
- The depth is the gene's expected count per sample, not the library size.

**Does not:**
- One gene at a per-gene significance level, by a normal approximation. For a whole experiment at a false discovery rate, or at small n where the approximation does not hold, use plan_rnaseq_experiment (the exact negative-binomial test, and average power across genes).
- The biological CV must come from a comparable experiment; it dominates the answer.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `solve_for` | `"n"` · `"cv"` · `"effect"` · `"alpha"` · `"power"` |  |  |  | the quantity to solve. Left unset, it is the one of n, cv, effect, alpha and power that was not given. Values: n (n per group), cv (CV), effect (fold change), alpha (α), power (power). |
| `depth` | number[] | **yes** |  | ≥ 0 | average depth of coverage of the gene: its expected read count per sample. Hart et al. found most genes at 0.1 per million mapped reads, so 4 at 40 million. |
| `n` | number[] |  |  | ≥ 1 | biological replicates in group 1 (and in group 2, unless `n2` is given). |
| `n2` | number[] |  |  | ≥ 1 | replicates in group 2, one per `n`. Advanced. |
| `cv` | number[] |  |  | ≥ 0 | the biological coefficient of variation within a group: 0.4 or less for most genes in human studies, about 0.1 in inbred animals (Hart et al.). |
| `cv2` | number[] |  |  | ≥ 0 | the CV within group 2, one per `cv`. Advanced. |
| `effect` | number[] |  |  | ≥ 0 | the fold change to detect; 2 and 0.5 are the same change. |
| `alpha` | number[] |  |  | 0–1 | α, the two-sided false-positive rate per gene. |
| `power` | number[] |  |  | 0–1 | 1 − β, the chance of detecting the change if it is real. No default: the target is yours to choose. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `solved` | string |  | which quantity was solved |
| `value` | number or null |  | the solved value, when the design is a single cell |
| `grid` | any |  | every design in the grid: each quantity, and the solved one |
| `curve` | object or null |  | the solved quantity along the first quantity given as a list, one line per value of the second |
| `curve.x` | number[] |  |  |
| `curve.series` | object[] |  |  |
| `curve.series[].name` | string |  |  |
| `curve.series[].y` | (number or null)[] |  |  |
| `curve.xLabel` | string |  |  |
| `curve.yLabel` | string |  |  |
| `curve.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `curve.title` | string |  |  |
| `curve.rules` | object[] |  |  |
| `curve.rules[].y` | number |  |  |
| `curve.rules[].label` | string |  |  |
| `rCall` | string |  | the R call that reproduces the grid |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "calculate_rnaseq_power",
  "arguments": {
    "depth": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### check_color_balance

**Check color balance**: _Will the sequencer see a signal in every channel at every index cycle for these indexes, on each chemistry?_

Will the sequencer SEE these indexes? Per-cycle channel occupancy for a set of index sequences under an instrument's own SBS chemistry, checked against Illumina's rules (no dark cycle, both channels preferred, no GG in the first two cycles), each violation citing the vendor article it comes from — and the same set scored across EVERY chemistry generation at once, because XLEAP moved the dual-color base from A to C and a set balanced on a NovaSeq 6000 is not balanced on a NovaSeq X. This is the color question alone; check_index_pool asks it alongside distance, duplicates and hopping for a whole pool.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Illumina's documented color rules for each instrument's SBS chemistry, as cached in the vendor dataset.

**Does not:**
- Checks color balance only; distance, duplicates and hopping are check_index_pool's questions.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** illumina-index-color-balance.json

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `barcodes` | string[] | **yes** |  |  | the index sequences to score, one per sample. |
| `instrument` | `"iSeq 100"` · `"MiniSeq"` · `"MiniSeq Rapid kits"` · `"NextSeq 500/550"` · `"NextSeq 1000/2000"` · `"NovaSeq 6000"` · `"NovaSeq X / X Plus"` · `"MiSeq"` · `"HiSeq 2000"` · `"HiSeq 2500"` · `"HiSeq 3000/4000/X"` |  | `"NovaSeq X / X Plus"` |  | the instrument whose chemistry the set is judged under, and whose index-2 orientation applies. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `tier` | string |  | Illumina's own grading of this set on this instrument: `ideal`, `acceptable` or `unacceptable` |
| `ok` | boolean |  | whether the set clears every rule for this chemistry |
| `violations` | any |  | each rule broken, the cycles it was broken at, and the vendor article it comes from |
| `cycles` | any |  | per-cycle channel occupancy — the census the tier is computed from |
| `channelPlot` | object or null |  | the fraction of the pool producing signal in each channel at each index cycle; the series are named after the channels, and their colors are not the dyes |
| `channelPlot.x` | number[] |  |  |
| `channelPlot.series` | object[] |  |  |
| `channelPlot.series[].name` | string |  |  |
| `channelPlot.series[].y` | (number or null)[] |  |  |
| `channelPlot.xLabel` | string |  |  |
| `channelPlot.yLabel` | string |  |  |
| `channelPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `channelPlot.title` | string |  |  |
| `channelPlot.rules` | object[] |  |  |
| `channelPlot.rules[].y` | number |  |  |
| `channelPlot.rules[].label` | string |  |  |
| `acrossChemistries` | any |  | the SAME set scored under every chemistry generation, so a set that passes here and fails on another instrument says so before the run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_color_balance",
  "arguments": {
    "barcodes": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### check_index_pool

**Check index pool**: _Will this pool of sample indexes sequence: duplicates, length, pairwise distance, color balance and hopping risk?_

Will this pool of sample indexes actually sequence? One verdict over the indexes a lab is about to load: duplicates, uniform length, the distance the set really guarantees against the distance it claims, per-cycle color balance on the chosen instrument's own chemistry, the index-2 orientation that instrument reads, and index-hopping exposure — how many i7 x i5 combinations exist against how many are in use, and which swaps would turn one sample's read into another's undetectably. Takes a pasted list or a vendor kit by id. It CHECKS a pool; design_barcodes builds one.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Index kits, color rules and hopping-rate classes are the vendor datasets as cached.
- Distance is the metric named, as DNABarcodes computes it.

**Does not:**
- Predicts demultiplexing risk; it does not demultiplex reads.

**Validated:** against the reference implementation by 3 golden suites.

**Reads bundled data:** illumina-index-color-balance.json, illumina-index-hopping-rates.json, illumina-index-kits.json

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `pool` | string |  |  |  | the pool as text — one row per sample: `name<TAB>i7[<TAB>i5]`, or bare index sequences one per line, with or without a header. Rows that cannot be read are REPORTED with their line number, never dropped. |
| `kit` | `""` · `"truseq-single-indexes"` · `"truseq-cd-indexes"` · `"idt-truseq-ud-indexes"` · `"idt-illumina-ud-plate-a"` · `"idt-illumina-ud-plate-b"` · `"idt-illumina-ud-plate-c"` · `"idt-illumina-ud-plate-d"` |  | `""` |  | a vendor kit id instead of a pasted list — the kit's own indexes are resolved and checked. Ignored when `pool` is given. Values:  (No kit — paste a list instead), truseq-single-indexes (TruSeq Single Indexes — Illumina, 24 indexes), truseq-cd-indexes (TruSeq DNA and RNA CD Indexes — Illumina, 96 indexes), idt-truseq-ud-indexes (IDT for Illumina–TruSeq DNA and RNA UD Indexes — Illumina / IDT, 100 indexes), idt-illumina-ud-plate-a (IDT for Illumina UD Indexes, Plate A/Set 1 — Illumina / IDT, 96 indexes), idt-illumina-ud-plate-b (IDT for Illumina UD Indexes, Plate B/Set 2 — Illumina / IDT, 96 indexes), idt-illumina-ud-plate-c (IDT for Illumina UD Indexes, Plate C/Set 3 — Illumina / IDT, 98 indexes), idt-illumina-ud-plate-d (IDT for Illumina UD Indexes, Plate D/Set 4 — Illumina / IDT, 100 indexes). Only applies when pool is not given. |
| `instrument` | `"iSeq 100"` · `"MiniSeq"` · `"MiniSeq Rapid kits"` · `"NextSeq 500/550"` · `"NextSeq 1000/2000"` · `"NovaSeq 6000"` · `"NovaSeq X / X Plus"` · `"MiSeq"` · `"HiSeq 2000"` · `"HiSeq 2500"` · `"HiSeq 3000/4000/X"` |  | `"NovaSeq X / X Plus"` |  | which instrument the run is on. It decides the chemistry the color balance is judged under AND the orientation index 2 is read in — a pool balanced on a NovaSeq 6000 is not balanced on a NovaSeq X. |
| `metric` | `"hamming"` · `"seqlev"` · `"levenshtein"` |  | `"seqlev"` |  | error model the distance guarantee is measured under — a pool safe under substitutions may be unsafe under indels. Values: hamming (Hamming (substitutions)), seqlev (Sequence-Levenshtein (indels)), levenshtein (Levenshtein). |
| `i7_cycles` | number |  | `0` | 0–24 | index-1 read length from the RUN RECIPE, when it differs from the index length — a 10 nt index read at 8 cycles is an 8 nt index for every purpose here. 0 = use the indexes' own length. |
| `i5_cycles` | number |  | `0` | 0–24 | index-2 read length from the run recipe. 0 = use the indexes' own length. |
| `required_distance` | number |  | `0` | 0–10 | the minimum distance the pool is SUPPOSED to guarantee, if it was designed to one — the check says whether it does. 0 = report the distance without judging it. Advanced. |
| `library_prep` | `"patterned-examp"` · `"truseq-pcr-free"` |  | `"patterned-examp"` |  | which of Illumina's published hopping-rate classes applies. The check multiplies the published RANGE by what this pool can throw away, to report how much is unrecoverable — it never predicts a rate for your run. Values: patterned-examp (Patterned flow cell, ExAmp chemistry), truseq-pcr-free (TruSeq PCR-Free libraries). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `verdict` | string |  | the pool-level verdict: `ok`, `warning` or `fail` |
| `failures` | number |  | checks that FAILED — a warn and a skip are each counted by their own status in `checks`, never folded in here |
| `checks` | any |  | every check with its own result — a check with no input to run against reports SKIPPED, never passed |
| `reads` | any |  | per index read: cycles, color-balance tier and the per-cycle channel census |
| `hopping` | any |  | index-hopping exposure: combinations possible against combinations in use, the removable share, and the undetectable swaps. Absent for a single-index pool, which has no i5 to swap. |
| `closestPairs` | any |  | the pairs that get confused first |
| `samples` | number |  | how many samples were checked |
| `guarantee` | any |  | how many errors this pool can CORRECT and DETECT under the chosen metric — the number the whole check exists to establish |
| `skipped` | any |  | rows the parse could not read, each with its line number and the reason — these are usually WHY a check refused |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_index_pool",
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

### check_manufacturability

**Check manufacturability**: _Does this sequence meet what a named synthesis vendor publishes it can make: length, GC, homopolymers and repeats?_

Measure a sequence against what a NAMED synthesis vendor publishes it can make: length, average and windowed GC, homopolymer runs, tandem repeats, long repeats and hairpin-forming inverted repeats. Every threshold is the vendor's own, read from the vendor's own page with the date it was read, and every finding carries the span it is about so it can be drawn. It reports the limits that are MET as well as the ones exceeded, because a list of failures cannot tell a clean sequence from an unchecked one. It never predicts a synthesis outcome and never rules a sequence out: a vendor publishes what it supports, so being outside a published window is a conversation with the supplier, not a rejection.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The vendor's thresholds are the ones its page stated on the retrieval date the profile carries.

**Does not:**
- A vendor may change its limits; being outside one is not a refusal by that vendor.
- Only the six repeat screens are graded by a reference; the GC and length checks are threshold comparisons.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `vendor` | `"idt-gblocks"` · `"idt-eblocks"` · `"twist-clonal"` · `"twist-fragments"` |  | `"idt-gblocks"` |  | which vendor product to measure against. Each carries its own limits, and two vendors can honestly disagree about one sequence. Values: idt-gblocks (IDT gBlocks Gene Fragments), idt-eblocks (IDT eBlocks Gene Fragments), twist-clonal (Twist Bioscience Clonal Genes), twist-fragments (Twist Bioscience Gene Fragments). |
| `sequence` | string |  |  |  | the sequence to measure. Leave unset to use the open record, or the current selection when there is one. |
| `feature` | string |  |  |  | measure a named feature of the open record instead of the whole thing — the insert you are about to order rather than the vector it sits in. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `verdict` | string |  | `within` when every published limit is met, `outside` when any is exceeded. Not a prediction and not a refusal: it is whether the sequence sits inside the envelope the vendor publishes |
| `length` | number | bp | the bases actually measured — the whole record, or the selection or named feature when one scoped the run. Every limit below was graded on this many |
| `outside` | number |  | how many published limits this sequence exceeds — the number to branch a workflow on |
| `checked` | number |  | how many limits were graded. Read it beside `outside`: 0 of 4 and 0 of 7 are different answers, because vendors publish different numbers of limits |
| `findings` | any |  | every limit, met or not, with what this sequence measures, what the vendor publishes, and the span it is about where it has one |
| `spans` | any |  | just the spans of the exceeded limits, 0-based half-open, ready to draw on the map — the half of a finding a user cannot act on without |
| `notGraded` | any |  | limits the vendor publishes that this sequence could not be graded on, each with the reason. A 40 bp insert has no 50 bp GC window, and silence would make a shorter sequence look like a cleaner one |
| `profile` | any |  | the vendor profile every verdict here was made against, including the page it was read from and the date — a threshold whose source is not stated is not checkable |
| `reading` | string |  | the report in words, generated from the findings: which limits are exceeded by how much, what could not be graded, and the standing qualification that published support is not a refusal policy |
| `repeatScreens` | any |  | the Synthesis Success Calculator's six published repeat-density screens (Halper, Hossain & Salis 2020), independent of vendor: each with its rule, whether it fires (null where it does not apply, as the 500 bp window under 1,000 bp), what was measured and the first span that tripped it. Rules from the literature, not a vendor's acceptance limits |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_manufacturability",
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

### check_scorpion_stem

**Check scorpion stem**: _Does a Scorpion probe's stem melt below the loop-target duplex by the margin the design needs?_

A Scorpion probe's two melting temperatures, side by side: the stem-loop's own hairpin and the duplex the loop makes with its target on the amplicon. A Scorpion is a primer carrying a stem-loop probe on a non-amplifiable blocker (Whitcombe 1999), and it reports by the loop finding its target and pulling the stem apart - so the design question is a RELATION between those two structures, not a property of either. Returns both temperatures, their difference, the stem's GC, and a verdict against WHATEVER margin you pass. It does not apply a margin of its own authority: the widely-quoted 5-10 °C figure comes from one design tool's tech note and has no primary citation, so the default is labelled as that rule of thumb and every result says which margin produced its verdict.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Both melting temperatures are primer3 thal's nearest-neighbour values at the stated salt and oligo conditions.

**Does not:**
- The default margin is a design tool's rule of thumb with no primary citation; the verdict is only as good as the margin passed.
- Says nothing about the blocker or the primer's own priming.

**Not read from this result:** The Design tab's Scorpion section shows the two temperatures, the difference and the margin flag with whose rule it is; it writes no sentence over them, and the door returns the same fields.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `probe` | string | **yes** |  |  | the whole probe element, 5' stem arm + loop + 3' stem arm. The element is what folds, so it is what the structure engine is given - the loop alone would compute a hairpin the molecule does not have. |
| `target` | string | **yes** |  |  | the loop's target on the amplicon, 5'->3'. This is the OTHER temperature: a Scorpion opens because the loop finds this, so it is the loop-target duplex that has to be stable, not the loop's own self-structure. |
| `stem_length` | number |  | `6` | 3–12 | how many bases of the 5' end form the stem arm. Reported back rather than guessed. The two vendors disagree on the range - LGC Biosearch, who sell Scorpions, publish 5-7 nt and PremierBiosoft's design tool says 6-7 - so neither is enforced. In nt. |
| `margin` | number |  | `5` | 0–30 | how many °C the stem Tm must exceed the loop-target Tm for the verdict to pass. Yours to set: the 5-10 °C rule of thumb this defaults to the floor of is a design tool's, not a measured value from the primary literature. In °C. |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method the stem Tm is measured in. Left unset it is filled from your reaction-conditions settings, and falls back to primer3's defaults when there are none. Advanced. |
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
| `stemTm` | number or null | °C | melting temperature of the probe element's own hairpin, °C - null when no stem forms |
| `probeTm` | number or null | °C | melting temperature of the loop-target duplex, °C |
| `difference` | number or null | °C | stemTm - probeTm, the quantity the design rule is about |
| `clearsMargin` | any |  | whether the difference clears the margin GIVEN - null when either temperature could not be computed |
| `marginSource` | string |  | where the margin came from, carried with the verdict so an unsourced rule of thumb is never mistaken for a measurement |
| `stemGcPercent` | number or null |  | GC of the 5' stem arm - both vendors ask for a GC-rich stem |
| `notes` | any |  | why a temperature is missing, in the words the panel shows. Empty when both were computed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_scorpion_stem",
  "arguments": {
    "probe": "<string>",
    "target": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### codon_optimality

**Codon optimality**: _What share of this CDS's codons are the optimal ones for this host (Fop)?_

Frequency of optimal codons (Fop, Ikemura 1981) for an in-frame CDS against a real codon-usage table: what share of its codons are the ones a highly-expressed gene in that host would use. Where CAI scores how CLOSE each codon is to its family's best, Fop scores only whether it IS one of the best, which makes it comparable across genes of different amino-acid composition. Name a table this project holds in `table`, or one of the bundled hosts in `host`.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The codon-usage table named, and Ikemura's definition of an optimal codon at the threshold given.

**Does not:**
- Needs an in-frame CDS; scores codon choice only, not expression.

**Not read from this result:** Fop, RCBS and DCBS for the region, which the Codon optimality section shows as readouts under the cutoff that produced them; the gene's codon reading is on codon_usage_analysis.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the coding sequence, in frame (a length that is not a multiple of 3 is refused with the reason). Leave it empty to score the open record. |
| `table` | string |  |  |  | a codon-usage table this project holds, BY NAME, as the Codon Usage panel lists it — any organism. Takes precedence over `host`. This is the way to pass a table you fetched or built; `host` is only the three tables bundled with the app. |
| `host` | `"E. coli K-12"` · `"H. sapiens"` · `"S. cerevisiae"` |  | `"E. coli K-12"` |  | one of the three codon-usage tables bundled with the app. Only applies when table is not given. |
| `threshold` | number |  | `0.8` |  | Ikemura's optimality cutoff: a codon counts as optimal at this share of its family's most-used codon. 0.8 is the convention, not a measurement, and the right value is host-dependent. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `fop` | number |  | frequency of optimal codons, 0-1 |
| `scored` | number |  | codons that carried a call — stops and unevidenced families are excluded from both halves |
| `nonOptimal` | number |  | how many codons are NOT optimal (the honest denominator beside fop) |
| `optimalCodons` | number |  | size of the optimal set the reference defines |
| `report` | any |  | the full readout, including which host table answered |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "codon_optimality",
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

### codon_table_fetch

**Codon table fetch**: _What is this organism's codon usage, counted from its annotated CDS or as a published table?_

Fetch a real codon-usage table for an organism and save it into this project, so later steps can score against it by name. NCBI builds the table by counting codons in the annotated CDS of a RefSeq assembly (the same counting the Codon Usage panel does, with the assembly and CDS count in the provenance); the Kazusa mirror serves a published table for an organism the mirror covers. The table LEAVES NOTHING but takes a network round-trip. Hand the saved name to `codon_usage_analysis` or `codon_optimality` in `table`.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Assumes:**
- NCBI's RefSeq assembly annotation, or the Kazusa mirror's table, as served at the time of the fetch.

**Does not:**
- Counts only annotated CDS; an organism neither source covers cannot be fetched.

**Not read from this result:** A reader: the codon usage table as the authority publishes it, with nothing inferred; the Codon usage panel's readings are on the tools that use it.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"ncbi"` · `"kazusa"` |  | `"ncbi"` |  | which register to build the table from. `ncbi` counts the CDS of a RefSeq assembly and covers any organism with one; `kazusa` serves a published table and covers only the organisms its mirror bundles. Values: ncbi (NCBI RefSeq — counted from annotated CDS, any organism), kazusa (Kazusa/CUTG mirror — published table, bundled organisms only). |
| `organism` | string | **yes** |  |  | the organism: a scientific name ("Saccharomyces cerevisiae") or an NCBI taxonomy id ("4932"). Resolved live against NCBI — no allow-list (§1 r4) — and the assembly it picks comes back in `report.builtFrom`. |
| `mode` | `"heg"` · `"genome"` |  | `"heg"` |  | which CDS set to count. `heg` uses the highly-expressed-gene set, which is what CAI and Fop reference tables are conventionally built from; `genome` counts every annotated CDS, which describes the organism's average gene rather than its best-expressed one. Values: heg (Highly-expressed genes — the CAI/Fop convention), genome (Whole genome — every annotated CDS). Only applies when source is ncbi. |
| `coverage` | `"complete"` · `"budgeted"` |  | `"complete"` |  | how much of a multi-replicon assembly to download. `complete` takes every replicon; `budgeted` takes the largest ones that fit a memory budget and SAYS which it used. The panel defaults to complete and falls back when the browser cannot hold the whole thing. Values: complete (Complete assembly), budgeted (Budgeted — largest replicons that fit). Only applies when source is ncbi. |
| `save_as` | string |  |  |  | the name to save the table under, as `table` on the other codon tools will spell it. Defaults to the resolved organism plus the basis, which is what the panel names it. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `table` | any |  | the saved name — wire this straight into `table` on codon_usage_analysis or codon_optimality |
| `organism` | string |  | the organism as the register resolved it, which may be more specific than asked |
| `codons` | number or null |  | total codons counted, the weight behind every frequency. ABSENT when the register publishes frequencies rather than counts (the Kazusa mirror does) — never 0, which would be a number you could quote |
| `cds` | number or null |  | how many CDS the table was counted from — the reference-set size, and the number a thin table is thin by. Absent on a register that publishes no counts |
| `gc3` | number or null | % | GC at the third codon position (%), the usage fingerprint. NCBI only; absent elsewhere |
| `report` | any |  | the full provenance: register, resolved organism, the identifier the table was built from, and any coverage fallback |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "codon_table_fetch",
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

### codon_usage_analysis

**Codon usage analysis**: _How does this CDS's codon usage compare with an organism's: CAI, GC, rare codons, and the two reference-free bias measures?_

Codon-usage analysis of an in-frame CDS: CAI / expression stats, GC, and every rare-codon occurrence for the chosen organism (pydna port), plus the two bias measures that need NO reference table — ENC (Wright 1990) and RCBS (Roymondal 2009), which are therefore computable for any organism.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The CDS is in frame.
- The organism's usage table is the one named; CAI is relative to it.

**Does not:**
- CAI needs a reference table; ENC and RCBS do not, which is why they are reported for any organism.
- A bias measure is not a prediction of expression.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `organism` | `"sce"` · `"eco"` |  | `"sce"` |  | reference organism for CAI weights + rare codons. Only some organisms carry CAI weights; the rest still get the rare-codon scan + GC. |
| `reverse` | boolean |  |  |  | read the region as the reverse complement. Leave unset to take the strand from the annotation when the selection is exactly an annotated CDS or gene, which is what the panel does. |
| `feature` | string |  |  |  | score this annotated CDS or gene by NAME instead of the selection (the panel's "A CDS / feature…" mode). Its own strand is used unless `reverse` says otherwise. |
| `table` | string |  |  |  | score CAI and rare codons against a codon-usage table this project holds, BY NAME, as the Codon Usage panel lists it — any organism, not just the two pydna curates. Takes precedence over `organism`, and switches the rare-codon call from pydna's curated list to `rare_threshold`. Leave unset for the curated pydna report, which is the only arm carrying start/stop weights and the N-end half-life. |
| `rare_threshold` | number |  | `0.3` | 0.05–0.5 | a codon is rare when its relative adaptiveness w = f/f_max falls below this. 0.30 is GenScript GenRCA's CFD cutoff, a convention rather than a measurement, so retune it per host. Only applies when table is set. |
| `enc_bg_correction` | boolean |  | `false` |  | correct ENC for the sequence's own base composition (Novembre 2002). Off is Wright's 1990 ENC, which reads GC-rich genes as more biased than they are. |
| `enc_pairs` | boolean |  | `false` |  | count codon PAIRS rather than single codons for ENC (k-mer 2) — bias in the junctions rather than in the codons. |
| `rcbs_directional` | boolean |  | `false` |  | RCBS weights taken as max(observed/expected, expected/observed), so under-use counts as bias too rather than only over-use. |
| `rcbs_mean` | `"geometric"` · `"arithmetic"` |  | `"geometric"` |  | how the per-codon RCBS weights are averaged. Roymondal 2009 uses the geometric mean. Values: geometric (Geometric (Roymondal 2009)), arithmetic (Arithmetic). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `caiAvailable` | boolean |  | whether a CAI could be computed at all. FALSE means `cai` is null because there was no reference to score against, NOT that adaptation is poor |
| `cai` | number or null |  | Codon Adaptation Index, or null when nothing could be scored — check `caiAvailable` before comparing it, and `referenceTable` before comparing two runs |
| `gc` | number |  | GC fraction (0–1) |
| `codons` | number |  | number of codons |
| `rareFraction` | number |  | fraction of codons that are rare (0–1) |
| `rareHits` | any |  | every rare-codon occurrence with its position |
| `enc` | number |  | effective number of codons, 20 (one per residue) to 61 (uniform) — needs no reference table |
| `rcbs` | number |  | relative codon bias vs the sequence's own base composition; 0 = as predicted — needs no reference table |
| `codonMap` | object or null |  | how often each of the 64 codons occurs in the measured region, laid out as the genetic-code chart: rows are the first two bases, columns the third |
| `codonMap.rows` | string[] |  |  |
| `codonMap.cols` | string[] |  |  |
| `codonMap.values` | ((number or null)[])[] |  |  |
| `codonMap.label` | string |  |  |
| `codonMap.title` | string |  |  |
| `region` | string |  | what was actually measured — the selection when there is one, otherwise the whole record, naming the STRAND and where it came from |
| `strandSource` | string |  | `explicit` (you passed `reverse`), `feature` (taken from the annotation the selection matches) or `default` (forwards, nothing said otherwise) |
| `referenceTable` | string |  | the project table CAI was scored against, or empty when the curated pydna organism answered |
| `rareBasis` | string |  | `curated` (pydna's published low-usage list for this organism — `rare_threshold` did not apply) or `threshold` (relative adaptiveness below `rare_threshold`). Rare counts from the two are different claims and do not compare |
| `report` | any |  | the full codon report |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "codon_usage_analysis",
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

### codon_usage_distance

**Codon usage distance**: _How far is this region's codon usage from the record's other genes (CUFS)?_

How this region's codon usage compares with the record's OTHER genes (CUFS, Diament, Pinter & Tuller 2014). Every other codon score grades one sequence against a reference TABLE; this one grades two sequences against each other, so it stays available for an organism no authority covers. Answers 'does the gene I inserted use codons like the rest of this construct'.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Both sides are in-frame coding sequence.

**Does not:**
- Compares two sequences with each other, so it needs no reference table and makes no claim about an organism's optimum.

**Not read from this result:** The CUFS distance to each of the record's other genes, which the panel shows as a sorted table; the gene's own codon reading is on codon_usage_analysis.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `synonymous` | boolean |  | `true` |  | normalise each amino acid's codons to sum to 1 (synCUFS), so what remains is the synonymous choice alone. Off compares all 64 codon frequencies, which also reflects amino-acid composition. |
| `reverse` | boolean |  |  |  | read the region as the reverse complement. Leave unset to take the strand from the annotation when the selection is exactly an annotated CDS or gene, which is what the panel does. |
| `feature` | string |  |  |  | score this annotated CDS or gene by NAME instead of the selection (the panel's "A CDS / feature…" mode). Its own strand is used unless `reverse` says otherwise. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `neighbours` | any |  | every other coding feature with its CUFS distance, nearest first — name, span, codons compared and distance |
| `nearest` | string |  | the feature whose codon usage is closest to the scored region |
| `nearestDistance` | number |  | its distance. 0 would mean an identical codon distribution; the maximum depends on the mode and is reported as `ceiling` beside it — sqrt(2 ln 2) = 1.177 for the plain form, sqrt(2 ln 2 F) = 5.396 for the synonymous one, which normalises each amino acid separately |
| `ceiling` | number |  | the largest distance this run could have produced, for the mode it ran in — read a distance against THIS, never against a constant |
| `furthest` | string |  | the feature whose codon usage is least like the scored region — the odd one out |
| `compared` | number |  | how many features were compared |
| `skipped` | any |  | features that were NOT compared and why — a feature too short for the statistic is reported, never dropped |
| `synonymous` | boolean |  | whether amino-acid composition was normalised away — the same column of figures means a different thing under each |
| `region` | string |  | what was actually scored, naming the STRAND and where it came from — a reverse-strand gene read forwards is a wrong answer, not a missing one |
| `strandSource` | string |  | `explicit` (you passed `reverse`), `feature` (taken from the annotation the selection matches) or `default` (forwards, nothing said otherwise) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "codon_usage_distance",
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

### debarcode_mass_cytometry

**Debarcode mass cytometry**: _Which barcoded sample does each event of a pooled mass cytometry acquisition belong to?_

CATALYST single-cell debarcoding of a barcoded mass cytometry FCS file in the project, with a barcoding key (a CSV: barcode id, then one 0/1 column per barcode mass): each event's barcode from the order of its asinh-transformed barcode channels, the channels scaled per barcode by the 95th percentile of its positive values, events whose separation is below the cutoff (one for every barcode, or each barcode's own estimated from its yield curve, estCutoffs) or whose Mahalanobis distance from their barcode's population exceeds the cutoff unassigned; per-barcode yields.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The barcode channels are named by their mass ((Pd102)Di, 102Pd…), which is how they are found.

**Does not:**
- An estimated cutoff comes from each barcode's own yield curve, so a barcode with few events gets a noisy one; a fit that fails gives that barcode cutoff 1 (nothing kept), as CATALYST applies it.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the FCS file in the project, by name or id. |
| `gating` | string |  | `""` |  | a Gating-ML or FlowJo .wsp in the project; empty for none. |
| `compensation` | `"auto"` · `"file"` · `"none"` · `"custom"` |  | `"auto"` |  | as analyze_flow_cytometry. |
| `compensation_method` | `"flowkit"` · `"flowcore"` |  | `"flowkit"` |  | as analyze_flow_cytometry. |
| `derived` | string |  | `""` |  | as analyze_flow_cytometry. |
| `key` | string |  | `""` |  | the barcoding key CSV in the project, by name or id; empty when the project holds one. |
| `barcode_cofactor` | number |  | `5` | ≥ 0.001 | barcode intensities read as asinh(x / barcode_cofactor); CATALYST's 5. |
| `sep_cutoff` | number |  | `0.35` | 0–1 | the separation below which an event is unassigned; 0.35 is CATALYST's example. |
| `estimate_cutoffs` | boolean |  | `false` |  | estimate each barcode's separation cutoff from its yield curve (CATALYST estCutoffs: a three-parameter log-logistic and a linear fit, weighted by their residuals) instead of sep_cutoff. |
| `mhl_cutoff` | number |  | `30` | ≥ 0 | the Mahalanobis distance beyond which an event is unassigned; CATALYST's 30. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `yields` | any |  | per barcode: events assigned before and after the cutoffs, and the cutoff used (estimated or given) |
| `unassigned` | number or null |  | events left unassigned |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "debarcode_mass_cytometry",
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

### design_barcodes

**Design barcodes**: _Which index set of this size has a guaranteed minimum distance, and what does it actually correct?_

Design a set of NGS sample-index barcodes with a guaranteed minimum distance, and report what that set actually corrects — substitutions, or indels too (DNABarcodes).

<sub>returns new records · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The code construction and distance measure chosen (DNABarcodes, or FREE divergence codes for indels).

**Does not:**
- What it corrects is a property of the code, not a measured error rate on an instrument.
- The heuristic constructions do not claim the largest possible set.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `length` | number |  | `8` | 3–20 | barcode length in bases. In bp. |
| `min_distance` | number |  | `3` | 2–10 | required minimum distance between any two barcodes — this is what buys the error correction. |
| `metric` | `"hamming"` · `"seqlev"` · `"levenshtein"` · `"phaseshift"` |  | `"seqlev"` |  | error model. A set correcting one substitution may correct zero indels, so this choice is the design, not a display option. Values: hamming (Hamming (substitutions)), seqlev (Sequence-Levenshtein (indels)), levenshtein (Levenshtein), phaseshift (Phaseshift). |
| `heuristic` | `"conway"` · `"clique"` · `"sampling"` · `"ashlock"` |  | `"conway"` |  | set-construction strategy. Values: conway (Conway (greedy)), clique (Clique), sampling (Sampling), ashlock (Ashlock). |
| `filter_triplets` | boolean |  | `true` |  | reject barcodes containing a homotriplet (AAA…). Advanced. |
| `filter_gc` | boolean |  | `true` |  | keep only balanced-GC barcodes (suppressed for length ≤ 3). Advanced. |
| `filter_self_complementary` | boolean |  | `true` |  | reject barcodes that are their own reverse complement. Advanced. |
| `seed` | number |  | `1` |  | PRNG seed for a stochastic search: the same seed always gives the same set. Only applies when heuristic is sampling or ashlock. |
| `iterations` | number |  | `100` | ≥ 1 | random restarts of the Conway closure (sampling) or generations of the evolutionary search (ashlock); DNABarcodes' default. Only applies when heuristic is sampling or ashlock. |
| `population` | number |  | `200` | ≥ 2 | chromosomes carried per Ashlock generation; DNABarcodes' default. Only applies when heuristic is ashlock. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `reading` | string |  | what the search returned against what was asked of it, generated from the run: the set size, the realized minimum distance and what it guarantees. The panel's own sentence |
| `cautions` | any |  | what would undermine the reading, earned by this run: a realized distance above the one requested, a suppressed GC filter, a stochastic search's seed dependence, a pool the constraint exhausted |
| `derivation` | string |  | the machinery: the heuristic, the screened pool out of the enumerated words, the metric, and how the guarantee follows from the realized distance |
| `barcodes` | any |  | the designed set |
| `count` | number |  | how many barcodes the search actually found |
| `guarantee` | any |  | correctable / detectable errors under the design metric |
| `analysis` | any |  | the set's properties under EVERY metric, not just the design one |
| `warnings` | any |  | what the search had to say |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_barcodes",
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

### design_codon_tiling_primers

**Design codon tiling primers**: _Which primers tile this CDS, one degenerate codon per position, inside a Tm window?_

Codon-tiling mutagenesis primers for a whole CDS: one primer per codon, each carrying a degenerate codon (NNN/NNK/NNS/NNC/NNG) at its centre, with the flanks grown or shrunk so every primer lands inside a Tm window (jbloomlab CodonTilingPrimers). This is the library-scale counterpart to design_saturation_primers, which solves one site at a time. Takes the CDS from the open record by name or from `cds`, and takes the flanking bases each primer anneals in from the record around it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The CDS is in frame and a whole number of codons.
- Tm is Biopython's `Tm_NN(strict=false)` under the named model, which is what upstream tiles against.

**Does not:**
- Decides WHERE the primers sit, not which degenerate codon to use: one ambiguous codon is installed at every position.
- A primer whose flanks cannot reach the Tm window inside the length limits is returned at the closest length upstream accepts, not dropped.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds` | string |  |  |  | the CDS to tile, in frame. Left empty the record's `cds_feature`, or the selection, is tiled and the flanking bases come from the record around it. |
| `cds_feature` | string |  |  |  | tile this annotated CDS of the open record by NAME, on its own strand, exactly as `codon_usage_analysis` takes one. The flanks come from the record either side of it. |
| `flanks` | string |  |  |  | with a literal `cds`: the bases either side of it, as `5'flank,3'flank`. Upstream anneals every primer in these, so without them a tiled primer has nothing to grow into — give at least `(primer_length - 3) / 2` bases per side. Advanced. |
| `primer_length` | number |  | `37` | ≥ 9 | starting primer length, in bases. Must be ODD: the flanks are (n-3)/2 per side. Upstream's own default. In nt. |
| `ambiguous_codon` | `"NNN"` · `"NNK"` · `"NNS"` · `"NNC"` · `"NNG"` |  | `"NNN"` |  | the degenerate codon installed at every position. NNK and NNS halve the stop codons NNN introduces; NNC and NNG are narrower still. |
| `min_primer_tm` | number |  | `60` |  | lowest acceptable primer Tm. In °C. |
| `max_primer_tm` | number |  | `61` |  | highest acceptable primer Tm; must be above `min_primer_tm`. In °C. |
| `min_length` | number |  | `25` | ≥ 9 | shortest primer the flank search may shrink to. In nt. Advanced. |
| `max_length` | number |  | `51` | ≥ 9 | longest primer it may grow to. In nt. Advanced. |
| `first_codon` | number |  | `1` |  | the number given to the first codon in primer NAMES. Set it when the CDS you are tiling starts part-way through a protein. Advanced. |
| `prefix` | string |  | `"tile"` |  | prefix for the generated primer names. Advanced. |
| `tm_model` | `"santalucia"` · `"wallace"` · `"gc:Chester_1993"` · `"gc:QuickChange"` · `"gc:Schildkraut_1965"` · `"gc:Wetmur_Melting_1991"` · `"gc:Wetmur_RNA_1991"` · `"gc:Wetmur_DNA_RNA_1991"` · `"gc:Primer3"` · `"gc:Ahsen_2001"` |  | `"santalucia"` |  | Tm scale the window is judged on. Upstream tiles against Biopython's nearest-neighbour Tm, which is `santalucia` here. Values: santalucia (SantaLucia nearest-neighbor (Biopython Tm_NN defaults)), wallace (Wallace rule (4 °C per G·C, 2 °C per A·T)), gc:Chester_1993 (GC formula: Marmur-Doty (Chester & Marshak 1993)), gc:QuickChange (GC formula: QuikChange (the kit manufacturer’s own formula)), gc:Schildkraut_1965 (GC formula: Schildkraut & Lifson 1965 (Marmur-Doty + log[Na⁺])), gc:Wetmur_Melting_1991 (GC formula: Wetmur 1991, DNA (MELTING 4.3 approximate mode)), gc:Wetmur_RNA_1991 (GC formula: Wetmur 1991, RNA), gc:Wetmur_DNA_RNA_1991 (GC formula: Wetmur 1991, RNA/DNA hybrid), gc:Primer3 (GC formula: Primer3Plus product Tm (Biopython’s default set)), gc:Ahsen_2001 (GC formula: von Ahsen 2001 (accuracy against ease of use)). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `primers` | any |  | one row per codon: name, seq (with the degenerate codon at its centre), length, tm, codonIndex, and `start`, the 0-based offset in the tiled string |
| `count` | number |  | primers designed, which is the number of codons tiled |
| `codons` | number |  | codons in the tiled CDS |
| `tmRange` | any |  | the lowest and highest Tm actually achieved, against the window asked for: `{ min, max, wanted: { min, max } }` |
| `outsideWindow` | number |  | primers whose Tm the flank search could not bring inside the window within the length limits. Reported rather than dropped |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_codon_tiling_primers",
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

### design_free_codes

**Design FREE codes**: _Which barcodes of this length correct this many insertions, deletions and substitutions?_

Generate INDEL-correcting barcodes — FREE divergence codes (Hawkins et al., PNAS 2018) — by reserving each codeword's error sphere over the whole 4^k space, so the guarantee survives an insertion or deletion rather than only a substitution. Or prune a set you already own down to a valid FREE code, and see which members' decode spheres collided. This is a different construction from design_barcodes' distance-based search, and answers a different question: a Levenshtein-distance set corrects indels between two barcodes, a FREE code corrects them in the read.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- FREE divergence (Hawkins et al., PNAS 2018) as freebarcodes computes it.

**Does not:**
- Exhaustive over 4^k, so long codes are slow; GC and homopolymer filters prune after generation.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `mode` | `"generate"` · `"prune"` |  | `"generate"` |  | generate a new code, or prune an existing set down to a valid one. Values: generate (Generate a code), prune (Prune a set to a valid code). |
| `length` | number |  | `8` | 4–12 | barcode length k. The search is over the whole 4^k space, so cost rises steeply with it. |
| `max_errors` | number |  | `1` | 1–3 | how many insertions/deletions/substitutions each codeword must tolerate. Each extra error costs most of the code. |
| `barcodes` | string[] |  | `[]` |  | the set to prune — required when `mode` is `prune`, ignored when generating. Only applies when mode is prune. |
| `reserved` | string[] |  | `[]` |  | codewords already in use, whose decode spheres are claimed BEFORE generation — this is how a code is EXTENDED rather than regenerated, so what comes back is compatible with the indexes a lab already owns. |
| `max_homopolymer` | number |  | `0` | 0–6 | reject a candidate with a run of this many identical bases. 0 = no limit. Advanced. |
| `max_gc` | number |  | `0` | 0–1 | reject a candidate above this GC fraction. 0 = no limit. Advanced. |
| `limit` | number |  | `0` | 0–100000 | stop after this many codewords. 0 = take the whole code. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `barcodes` | any |  | the codewords — generated, or the ones that survived pruning |
| `count` | number |  | how many codewords came back |
| `dropped` | any |  | prune only: the codewords removed because their decode spheres collided — a user pruning their own set needs to know which indexes to stop using, not how many |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_free_codes",
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

### design_gene_fragment_order

**Design gene fragment order**: _What sheet does IDT's gene-fragment plate upload take for these fragments, and which of them can the product not be ordered as?_

Write the sheet IDT's gene-fragment PLATE upload takes for one or more designed fragments: one worksheet per 96-well plate, wells in the template's own order, and the template's four columns (well, name, sequence, 5' phosphorylation). A fragment outside the product's length range, unnamed, or carrying a non-IUPAC base is refused by name; one outside the product's published GC or homopolymer limits is kept and named, because a vendor publishes what it supports, not what it rejects. It WRITES A FILE and sends nothing: no account, no key, no network call.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The column shape, well order and phosphorylation values are those of IDT's published plate upload template.
- Each product's length range is the one its manufacturability profile carries, read from IDT's own pages.

**Does not:**
- IDT only: Twist's order template is behind an account and is not written.
- 96-well plates only, the one layout the template lists.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `product` | `"idt-gblocks"` · `"idt-eblocks"` |  | `"idt-gblocks"` |  | which IDT fragment product to order the fragments as. It sets the length range a fragment must fall in, and eBlocks take a per-plate minimum. Values: idt-gblocks (gBlocks Gene Fragments (125–3,000 bp)), idt-eblocks (eBlocks Gene Fragments (300–1,500 bp)). |
| `sequences` | string[] |  |  |  | the fragments to order, 5'→3'. Leave unset to order the open record, or the current selection or named `feature` of it, under the record's name. |
| `names` | string[] |  |  |  | a name per fragment, in the same order. Required with `sequences`: a well is ordered by name, so an unnamed fragment is refused rather than numbered. |
| `feature` | string |  |  |  | order a named feature of the open record instead of the whole record: the insert rather than the vector it sits in. Advanced. |
| `phosphorylate` | boolean |  | `false` |  | ask for 5' phosphorylation on every fragment. IDT offers it for blunt cloning only. |
| `plate_name` | string |  | `"Plate 1"` |  | the plate's name, which becomes the worksheet's name. Several plates get ' (2)', ' (3)' appended. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sheets` | any |  | one entry per PLATE: its worksheet name and every laid-out well, each with the published limits it sits outside |
| `rows` | any |  | every plate as header-first rows in the template's column shape, keyed by worksheet name: what the .xlsx holds |
| `plateCount` | number |  | how many plates the fragments needed |
| `columns` | any |  | the template's header row |
| `refused` | any |  | every fragment left OUT, with the reason |
| `plateMinimum` | string |  | set when the product takes a minimum per plate and a plate falls under it; empty otherwise |
| `profile` | any |  | the vendor profile the length range came from, with its page and retrieval date |
| `reading` | string |  | what the order is, generated from the laid-out plates |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_gene_fragment_order",
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

### design_genetic_circuit

**Design genetic circuit**: _Which characterised repressor gates compute this logic function — given as a named gate, a truth table or a Verilog module — with what ON/OFF dynamic range, and what DNA does the circuit need?_

Design a genetic circuit that computes: give it a logic function — a named gate, a truth table, or a Verilog module — and it synthesizes a NOR/NOT netlist, assigns real characterized repressor gates from a Cello UCF library, predicts the dynamic range between ON and OFF, and emits the construct's DNA. The gate parameters are MEASURED, from the published libraries, with the host and growth conditions they were measured under reported alongside — never estimated here.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Cello's UCF gate parameters are measured values, in the host and growth conditions the library reports.
- The response functions compose as Cello's model says.

**Does not:**
- The predicted dynamic range is the model's, in the library's host and conditions, not yours.
- The assignment search finds the same maximum as Cello; ties are not broken meaningfully.
- A Verilog module is read in Cello's dialect, which is not legal IEEE 1364: its own corpus assigns a net procedurally throughout. A module a conforming simulator accepts is read too, but the two notations are not the same language.

**Validated:** against the reference implementation by 6 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `logic` | string |  | `"AND"` |  | the function the circuit computes, written any of three ways: a named gate (NOT, AND, OR, NAND, NOR, XOR, XNOR, AND3, OR3, MAJORITY-3); a truth table as one bit per input combination with the first input most significant (AND is `0001`), using `x` for a row you do not care about, which lets synthesis pick whichever value costs fewer gates; or a whole VERILOG MODULE, in any of the three notations Cello accepts — a `case` block, a netlist of gate instantiations, or an `assign` expression. |
| `verilog_output` | string |  |  |  | which output of a multi-output Verilog module to build. One construct drives one reporter, so a module with several outputs is several circuits and there is no default — unset, a multi-output module is refused with its output names listed. Advanced. |
| `library` | `"Bth1C1G1T1"` · `"Eco1C1G1T1"` · `"Eco1C2G2T2"` · `"Eco2C1G3T1"` · `"Eco2C1G5T1"` · `"SC1C1G1T1"` |  | `"Eco1C1G1T1"` |  | the characterized gate library to build from. Each was measured in one host under one growth condition, and the prediction inherits both. |
| `sensors` | string |  |  |  | comma-separated input sensors the search may use. Leave unset to consider every sensor the library carries. Advanced. |
| `reporters` | string |  |  |  | comma-separated output reporters the search may use. Leave unset to consider all of them. Advanced. |
| `groups` | string |  |  |  | comma-separated repressor groups the search may draw on. Narrowing this is how a large search is made tractable — and how a gate you cannot obtain is kept out of the design. Advanced. |
| `max_assignments` | number |  | `200000` | ≥ 1 | refuse rather than search past this many assignments. A ceiling, not a target: the search is EXHAUSTIVE, so it is never sampled — a best-of-some reported as a best-of-all is a wrong answer rather than a slow one. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `score` | number |  | the predicted dynamic range: the dimmest ON output divided by the brightest OFF, across every input combination |
| `assignment` | any |  | which sensors, gate groups and reporters the winning design uses |
| `truthTable` | any |  | every input combination with its logic values and its analog levels in RPU, per node |
| `sequence` | string |  | the construct's DNA, the devices concatenated in the order the library's placement rules put them |
| `dna` | any |  | the construct broken into devices and parts, each with its own sequence, plus the solved device order and every placement constraint the library declares |
| `placement` | any |  | how the device order was solved: the arrangement including the library's landing pads, how many of its placement constraints bound this construct, and any rule whose operator is not implemented |
| `toxicity` | any |  | what the circuit costs the host: relative growth per truth-table row, the worst row, and per-gate detail — plus how many of the assigned gates actually carried a measured growth table, because a growth of 1.00 means something different when nothing was measured |
| `curves` | any |  | each assigned gate's transfer function sampled around its own midpoint, with this design's operating points on it — one curve per physical gate that won a row, so a group won by two gates gives two curves |
| `curvesFigure` | string or null |  | the curves above drawn as the panel draws them: one panel per gate, all on the same log-log axes, the response as a line and this design's operating points on it, ON in green and OFF in red |
| `netlist` | any |  | the NOR/NOT netlist synthesized from the logic function, and the table it was checked to compute, with any rows the specification left as don't-cares named |
| `verilog` | any |  | when the specification was a Verilog module: the notation it was written in, its port names, the case concatenation order, the gate netlist if it was structural, and the notes the reader raised — a tolerated upstream defect, an undeclared output, a don't-care row. Null for a truth table or a named gate |
| `explanation` | any |  | the derivation chain: conclusion, interpretation, earned cautions and machinery, generated from this run |
| `libraries` | any |  | every shipped library with its host, growth conditions and gate count, so a caller can choose one |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_genetic_circuit",
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

### design_hcr_probes

**Design HCR probes**: _Which HCR v3.0 split-initiator probe pairs tile this target within their composition and free-energy windows?_

Design HCR v3.0 split-initiator probe pairs against the subject: tile its reverse complement into 52 nt windows, drop windows with C or G runs, a stable hairpin, G+C or RNA:DNA free energy outside their windows, or (given a bowtie2 alignment of the tiles) more than one genome hit, then pick non-overlapping tiles closest to the target free energy and split each around a 2 nt gap into an odd and an even probe carrying half of the chosen amplifier's initiator. Each stage reports how many tiles it kept.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- HCR v3.0's 52 nt window and split geometry; RNA:DNA free energies from the stated model.

**Does not:**
- Genome uniqueness is only checked when a bowtie2 alignment of the tiles is given.
- Designs pairs; amplifier kinetics and signal are not modelled.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `channel` | `"B1"` · `"B2"` · `"B3"` · `"B4"` · `"B5"` |  | `"B1"` |  | HCR amplifier whose split initiator the pair carries; one channel per target in a multiplexed experiment. |
| `max_probes` | number |  | `20` | 1–200 | most probe pairs to return. |
| `tile_size` | number |  | `52` | 20–60 | length of the target window each pair covers, both halves and the 2 nt gap. In nt. Advanced. |
| `min_gc` | number |  | `45` | 0–100 | lowest percent G+C of a tile. In %. |
| `max_gc` | number |  | `55` | 0–100 | highest percent G+C of a tile. In %. |
| `min_gibbs` | number |  | `-70` | -200–0 | most stable RNA:DNA free energy to accept (at 37 °C, 0.33 M Na⁺). In kcal/mol. |
| `max_gibbs` | number |  | `-50` | -200–0 | least stable RNA:DNA free energy to accept. In kcal/mol. |
| `target_gibbs` | number |  | `-60` | -200–0 | free energy the selection ranks tiles by closeness to. In kcal/mol. |
| `max_run_length` | number |  | `7` | 2–30 | window length for the C and G run check. In nt. Advanced. |
| `max_run_mismatches` | number |  | `2` | 0–29 | bases in that window allowed to differ from the run base. In nt. Advanced. |
| `max_hairpin_tm` | number |  | `45` | 0–100 | drop a tile whose primer3 hairpin melts at or above this. In °C. Advanced. |
| `dtm_filter` | boolean |  | `false` |  | also require the two halves' melting temperatures to agree. Advanced. |
| `dtm_max` | number |  | `5` | 0–50 | largest allowed difference between the halves' melting temperatures. In °C. Only applies when dtm_filter is true. Advanced. |
| `alignment_sam` | string |  |  |  | SAM from bowtie2 -k 3 -f of the tiles FASTA this tool returns, against your genome or transcriptome. Without it no tile is checked for uniqueness and the result says so. |
| `num_hits_allowed` | number |  | `1` | 0–3 | most alignments a tile may have and still be kept (its own locus counts as one). Only applies when alignment_sam is set. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `pairs` | any |  | the selected probe pairs, ranked by closeness to the target free energy, each with both oligos, its 1-based start, G+C, Tm, half-Tm difference, free energy and genome hits |
| `pairCount` | number |  | how many probe pairs were selected |
| `stages` | any |  | how many tiles each stage kept, in pipeline order |
| `tilesFasta` | string |  | the tiles that pass the run and hairpin checks, as FASTA, for bowtie2 -k 3 -f |
| `orderTable` | string |  | every odd then every even oligo as a Name/Sequence table for plate ordering |
| `explanation` | any |  | the derivation chain: conclusion, interpretation and machinery, generated from this run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_hcr_probes",
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

### design_ish_probes

**Design ish probes**: _Which oligo set images this target best: tiled candidates meeting Tm, GC and composition, screened for off-target binding and abundant k-mers, and gathered into a set?_

Design an in-situ hybridization probe against the subject: tile it into candidate oligos that meet a melting-temperature, G+C and composition specification, screen them for off-target binding against an alignment and for k-mers abundant in a reference, and gather the survivors into the set that images best. Merges OligoMiner's tiling, its trained specificity model and its k-mer filter with iFISH's probe-set selection; each stage reports what it removed and why.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- OligoMiner's tiling and trained specificity model, and iFISH's set selection.
- The alignment given represents what the probes could cross-hybridise with.
- The k-mer reference or dictionary given represents the genome the probes will meet.

**Does not:**
- Each stage reports what it removed and why; a probe surviving is predicted specific against what was searched, not against the genome.
- No prediction of signal intensity.

**Validated:** against the reference implementation by 4 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `min_length` | number |  | `36` | 15–200 | shortest oligo to accept. In nt. |
| `max_length` | number |  | `41` | 15–200 | longest oligo to accept; the tiler grows a window until one fits, so a wide range yields more probes. In nt. |
| `min_tm` | number |  | `42` | 0–100 | lowest melting temperature to accept, AFTER the formamide correction. In °C. |
| `max_tm` | number |  | `47` | 0–100 | highest melting temperature to accept. In °C. |
| `min_gc` | number |  | `20` | 0–100 | lowest percent G+C to accept. In %. |
| `max_gc` | number |  | `80` | 0–100 | highest percent G+C to accept. In %. |
| `sodium` | number |  | `390` | 1–2000 | monovalent cation concentration of the hybridization buffer. In mM. |
| `formamide` | number |  | `50` | 0–100 | formamide in the hybridization buffer; it lowers every melting temperature by about 0.65 °C per percent. In %. |
| `dnac1` | number |  | `25` | 0.1–100000 | concentration of the higher-concentration strand, typically the probe, in the melting-temperature calculation (OligoMiner `--dnac1`). In nM. |
| `dnac2` | number |  | `25` | 0–100000 | concentration of the lower-concentration strand, typically the target (OligoMiner `--dnac2`). The Tm uses dnac1 − dnac2/2, so equal values halve the effective concentration. In nM. |
| `spacing` | number |  | `0` | 0–1000 | bases forced between consecutive oligos. In nt. Advanced. |
| `prohibited` | string |  | `"AAAAA,TTTTT,CCCCC,GGGGG"` |  | comma-separated subsequences an oligo may not contain; the default bans homopolymer runs, which hybridize promiscuously. Advanced. |
| `overlap` | boolean |  | `false` |  | report every window that qualifies, including overlapping ones. Off by default because overlapping oligos cannot be used together in one probe. Advanced. |
| `origin` | number |  |  | ≥ 1 | coordinate of the subject's first base, when it is a window cut from a larger sequence. Read from a UCSC-style `range=` header when the subject carries one. Advanced. |
| `alignment_sam` | string |  |  |  | SAM the candidates were aligned with, for off-target screening. Without it the oligos are returned UNSCREENED and the result says so. |
| `screen_mode` | `"lda"` · `"unique"` · `"zero"` |  | `"lda"` |  | trained model (recovers usable probes near repeats) · unique alignment only (strict) · no alignment at all (for a sequence that should be absent). Values: lda (Trained model), unique (Unique alignment only), zero (No alignment at all). Only applies when alignment_sam is set. |
| `hybridization_temperature` | `32` · `37` · `42` · `47` · `52` · `57` |  | `42` |  | temperature the specificity model was trained at. Only these six exist; the coefficients change sign across the range, so an intermediate value is a different model rather than a blend. In °C. Only applies when alignment_sam is set. |
| `max_off_target_probability` | number |  | `0.5` | 0–1 | keep an oligo whose modelled chance of a real off-target site is below this. Only applies when alignment_sam is set. Advanced. |
| `kmer_reference` | string |  |  |  | FASTA of the reference to count k-mers in, for OligoMiner's k-mer screen. Counted here, so a whole genome belongs in kmer_dump instead. Without either the oligos are returned with k-mer abundance UNCHECKED and the result says so. |
| `kmer_dump` | string |  |  |  | `jellyfish dump` of a genome's k-mer dictionary, for a reference too large to count here: `jellyfish count -m 18 -L 5` then `jellyfish dump -c -L 5` keeps only the k-mers a screen at 5 acts on. Advanced. |
| `kmer_length` | number |  | `18` | 8–31 | k, the k-mer length counted in kmer_reference (OligoMiner's README builds 18); a dump carries its own. In nt. Only applies when kmer_reference is set. |
| `kmer_threshold` | number |  | `5` | 1–100000 | drop an oligo holding any k-mer that occurs this many times or more in the reference. |
| `kmer_canonical` | boolean |  | `false` |  | count a k-mer and its reverse complement as one (jellyfish -C). Off as OligoMiner's dictionary is; for a dump it must match how the dictionary was counted. Advanced. |
| `oligos_per_probe` | number |  |  | 2–500 | oligos to gather into one probe. Leave unset to return every surviving oligo instead of a set. |
| `filter_by` | `"centrality"` · `"size"` · `"homogeneity"` |  | `"centrality"` |  | feature that defines the band of acceptable sets. Values: centrality (Centrality on the region), size (Compactness), homogeneity (Even spacing). Only applies when oligos_per_probe is set. Advanced. |
| `rank_by` | `"centrality"` · `"size"` · `"homogeneity"` |  | `"size"` |  | feature that ranks the sets inside that band. Values: centrality (Centrality on the region), size (Compactness), homogeneity (Even spacing). Only applies when oligos_per_probe is set. Advanced. |
| `filter_threshold` | number |  | `0.1` | 0–1 | width of the band around the best set, as a fraction of its own value. Only applies when oligos_per_probe is set. Advanced. |
| `probes` | number |  | `1` | 1–50 | how many probe sets to return. Only applies when oligos_per_probe is set. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `probes` | any |  | the chosen probe sets, best first, each with its oligos and its three scores |
| `oligos` | any |  | every oligo that survived all stages, in target order |
| `oligoCount` | number |  | how many oligos survived |
| `coveredFraction` | number |  | fraction of the target covered by at least one surviving oligo (0-1) |
| `stages` | any |  | what each stage took in, put out, and removed - with the reasons named |
| `kmer` | any |  | the k-mer screen's reading of each oligo it saw: its start, the highest count charged to it, and whether it was kept. Absent when no k-mer reference or dump was given |
| `explanation` | any |  | the derivation chain: conclusion, interpretation and machinery, generated from this run |
| `coverage` | any |  | the coverage track, gaps, spacings and the Tm/G+C distributions a renderer draws |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_ish_probes",
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

### design_knockout_package

**Design knockout package**: _What does a complete knockout or knock-in build need: guides, an off-target census, a repair template with arms, screening primers outside the arms, the protocol, and what to buy?_

The complete build package for a knockout or knock-in, as one object: guides inside the target, an off-target census for the chosen one within this molecule, a repair template with real homology arms, a screening PCR whose primers sit OUTSIDE the arms, the protocol in order, the fragments and oligos to buy, and every coordinate ready for the map. Two donor modes: by default the arms sit on the cut (a point insertion — the target's own sequence is kept on both sides), and with `replace_target` the arms flank the whole target and it is deleted, which is the mode for replacing one CDS with another (an empty insert then deletes the target cleanly). It refuses rather than guessing: no PAM in the target, arms that run off a linear molecule, a screening amplicon that cannot clear the arms, or a non-DNA insert; and in the default mode it WARNS when an insert lands inside the target, because that is a fusion rather than a replacement. Arm length, screening flank and guide count are yours to state, because each follows the delivery method and the organism.

<sub>returns new records · runs locally on the engine · deliverable: knockout</sub>

**Assumes:**
- The donor mode chosen matches the intent: arms on the cut inserts, arms flanking the target replaces it.
- The molecule's topology is as the record states.

**Does not:**
- It refuses rather than guessing: no PAM in the target, arms off a linear end, an amplicon that cannot clear the arms.
- No upstream produces this composite, so the golden grades the hand-offs between its sections, not an upstream's output.

**Not read from this result:** A composed package (guides, donor, screening primers, protocol, order list) whose report output is the document a bench reader follows; each part's reading is on the tool that made it.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `subject` | string |  |  |  | the molecule to edit — wire a record or name a library document; leave unset to edit the open record. |
| `target_start` | number | **yes** |  | ≥ 0 | start of the gene to knock out (0-based, inclusive). In bp. |
| `target_end` | number | **yes** |  | ≥ 1 | end of the gene to knock out (0-based, exclusive). In bp. |
| `target_name` | string |  | `"target"` |  | what the target is called, so every mark, primer and order line names its subject. |
| `arm_length` | number | **yes** |  | 100–2000 | homology-arm length on EACH side of the cut, in bp. A protocol decision that follows the delivery method, so there is no default: state what yours needs. The published working range is 100-800 (100-400 nt synthetic, up to ~800 bp cloned). In bp. |
| `screen_flank` | number | **yes** |  | 0–5000 | how far OUTSIDE the arms the screening primers must bind, in bp. Not decoration: a primer inside the arms amplifies the repair template as readily as the locus, so the assay cannot tell an edited colony from plasmid carry-over. In bp. |
| `insert` | string |  |  |  | sequence to place at the cut (a tag, a selection cassette). Leave empty for a scarless rejoin — the package then WARNS that the two screening products are the same length. |
| `replace_target` | boolean |  | `false` |  | replace the WHOLE target region with the insert, arms flanking the target — the gene-replacement donor. Off (default): the arms sit on the cut and the target's own sequence is kept on both sides of the insert (a point insertion), so this must be ON to knock one CDS in for another. Empty insert + this = a clean deletion of the target. Advanced. |
| `insert_name` | string |  |  |  | what the insert is called in the protocol and on the order form. |
| `guides` | number |  | `3` | 1–20 | how many guides to carry into the package, best-scoring first. The rest are the alternatives, not filler. |
| `nuclease` | `"SpCas9"` · `"SpCas9-NG"` · `"SpG"` · `"SpRY"` · `"xCas9"` · `"SaCas9"` · `"SaCas9-KKH"` · `"AsCas12a"` · `"LbCas12a"` · `"enAsCas12a"` |  | `"SpCas9"` |  | the nuclease (PAM + spacer length) to scan the target for. Values: SpCas9 (SpCas9: NGG (3')), SpCas9-NG (SpCas9-NG: NG (3')), SpG (SpG: NGN (3')), SpRY (SpRY: NRN (3')), xCas9 (xCas9: NG (3')), SaCas9 (SaCas9: NNGRRT (3')), SaCas9-KKH (SaCas9-KKH: NNNRRT (3')), AsCas12a (AsCas12a: TTTV (5')), LbCas12a (LbCas12a: TTTV (5')), enAsCas12a (enAsCas12a: TTTV (5')). |
| `max_mismatches` | number |  | `3` | 0–6 | mismatch ceiling for the off-target search within this molecule. Advanced. |
| `primer_tm` | number |  |  | 40–75 | target melting temperature for the screening primers [°C] — follows your polymerase and buffer. In °C. Advanced. |
| `restriction_enzymes` | string[] |  |  |  | cloning enzymes whose recognition site must NOT appear in a spacer. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the repair template as a sequence record, so the run leaves the user holding the thing to order |
| `guides` | any |  | every guide inside the target, scored, best first |
| `chosen` | any |  | the guide the package was built around |
| `offTargets` | any |  | the off-target census for the chosen spacer WITHIN this molecule, with the scope stated |
| `donor` | any |  | the repair template: both arms with their genomic spans, the insert, and the junctions to sequence across |
| `screening` | any |  | the screening PCR: the pair, the two product lengths, and the span they cover |
| `steps` | any[] |  | the protocol in the order it is done |
| `order` | any |  | the fragments and oligos to buy, each with the design decision it comes from |
| `marks` | any |  | every span this package names, ready for the map |
| `report` | string |  | the whole package as Markdown — protocol, order form, guides, template, screening and marks — so it survives outside the transcript |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_knockout_package",
  "arguments": {
    "target_start": "<number>",
    "target_end": "<number>",
    "arm_length": "<number>",
    "screen_flank": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_merfish_probes

**Design MERFISH probes**: _Which encoding probes make this transcript readable in a MERFISH experiment under this codeword, and how specific is each?_

Design MERFISH encoding probes for the subject transcript: tile it into target regions, keep those whose G+C and melting temperature fall in their windows, that share no k-mer with an rRNA or tRNA, and whose k-mers occur in this gene's transcripts and nowhere else in the transcriptome; attach readout sequences that spell the gene's codeword, add the amplification primers, screen the whole oligo again, select probes that cover every on-bit evenly with least overlap, and drop probes complementary to one another. Each stage reports how many it kept.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- Specificity is counted against the transcriptome given, each transcript weighted by the expression given (1 where none is).
- Melting temperature by nearest neighbours (SantaLucia & Hicks 2004) with a linear formamide correction.

**Does not:**
- Off-targets are exact shared k-mers, not alignments: a near match is not counted.
- Without rRNA/tRNA sequences that screen does not run, and the result says so.
- Designs one transcript's probes; the codebook (which gene gets which codeword) is an input.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `transcriptome` | string |  |  |  | every transcript of the organism as FASTA (RefSeq titles name the gene in their last parentheses); the subject is found in it by sequence. |
| `target_id` | string |  |  |  | the transcript to design for, by its FASTA id. Empty: the transcript whose sequence is the subject's. Advanced. |
| `barcode` | string |  |  |  | the gene's codeword, one 0 or 1 per bit, 1 where the bit is on. |
| `readouts` | string |  |  |  | the readout sequences as FASTA, one per bit, in bit order. |
| `rtrna_reference` | string |  |  |  | rRNA and tRNA sequences as FASTA. An Ensembl ncRNA FASTA is filtered to those biotypes by its headers. Empty: the rRNA/tRNA screen does not run. |
| `expression` | string |  |  |  | expression per transcript, one 'id value' line each (FPKM or TPM). Empty: every transcript weighs 1, MERFISH_probe_design's own choice without expression data. Advanced. |
| `target_length` | number |  | `30` | 15–60 | length of each target region. In nt. |
| `min_gc` | number |  | `40` | 0–100 | lowest G+C of a target region (exclusive). In %. |
| `max_gc` | number |  | `70` | 0–100 | highest G+C of a target region (exclusive). In %. |
| `min_tm` | number |  | `50` | 0–100 | lowest melting temperature of a target region (exclusive). In °C. |
| `max_tm` | number |  | `65` | 0–100 | highest melting temperature of a target region (exclusive). In °C. |
| `sodium_mm` | number |  | `390` | 1–2000 | monovalent salt of the hybridization buffer. In mM. Advanced. |
| `formamide` | number |  | `30` | 0–70 | formamide in the hybridization buffer. In %. Advanced. |
| `probe_nm` | number |  | `5` | 0.1–1000 | concentration of each probe. In nM. Advanced. |
| `min_specificity` | number |  | `0.999` | 0–1 | lowest specificity to keep (exclusive): the share of a region's k-mers found only in this gene. |
| `specificity_k` | number |  | `17` | 8–30 | k-mer length of the specificity and readout off-target counts. Advanced. |
| `rtrna_k` | number |  | `15` | 8–30 | k-mer length of the rRNA/tRNA screen. Advanced. |
| `max_rtrna_ot` | number |  | `0.5` | 0–100 | highest rRNA/tRNA off-target count to keep (exclusive); 0.5 keeps only regions with none. Advanced. |
| `cross_talk_k` | number |  | `15` | 8–30 | k-mer length of the library-wide cross-hybridization screen. Advanced. |
| `readouts_per_probe` | number |  | `2` | 1–6 | readout sequences carried by each probe, split between its two ends. |
| `readout_assignment` | `"balanced"` · `"random"` |  | `"balanced"` |  | how each probe's on-bits are drawn: balanced keeps every on-bit equally used down the transcript. Advanced. |
| `one_bit_per_probe` | boolean |  | `false` |  | give each probe copies of a single readout. Advanced. |
| `spacer` | string |  | `"A"` |  | bases between each readout and the target. Advanced. |
| `max_readout_ot_increase` | number |  |  | 0–1000 | drop a probe whose readouts add this many expression-weighted off-target k-mers or more (the single-molecule pipeline's check). Empty: not checked. Advanced. |
| `reverse_primer` | string |  |  |  | reverse primer, T7 promoter at its 5' end. Empty: no primers are added. Advanced. |
| `forward_primer` | string |  |  |  | forward primer; its reverse complement ends the oligo. Only applies when reverse_primer is set. Advanced. |
| `t7_length` | number |  | `17` | 0–40 | bases of the reverse primer lost in in vitro transcription. In nt. Only applies when reverse_primer is set. Advanced. |
| `probes_per_transcript` | number |  | `72` | 1–500 | probes to select. |
| `trials` | number |  | `5` | 1–50 | selection runs; the one with the most even on-bit coverage is kept. Advanced. |
| `seed` | number |  | `0` | 0–4294967295 | seed for the random draws in readout assignment and selection. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `probes` | any |  | the selected encoding probes in selection order, each with its 0-based shift, target, G+C, Tm, specificity, isospecificity, readouts, barcode and the oligo to order |
| `probeCount` | number |  | how many encoding probes were kept |
| `stages` | any |  | what each stage took in and kept, in pipeline order, with the reason a skipped stage did not run |
| `report` | any |  | the transcript-level report: probes, probes per on-bit, the fewest on any bit, and how many could be placed without overlap before and after selection |
| `orderTable` | string |  | every probe as a Name/Sequence table for pool ordering |
| `explanation` | any |  | the derivation chain: conclusion, interpretation and machinery, generated from this run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_merfish_probes",
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

### design_oligo_plate_order

**Design oligo plate order**: _In which wells, in the supplier's own fill order, does an oligo set go on a plate order?_

Lay a set of oligos out as a supplier's PLATE order sheet: one worksheet per plate, in the well order the supplier's own order form fills, with the column shape its loading direction requires. A plate order is addressed BY WELL, which a flat tube list cannot express — so this is the shape an oligo set actually gets ordered in once it outgrows a handful of tubes. With `mixed`, a forward and a reverse share one well, which is what the supplier's doubled mix-plate layouts encode. It WRITES A FILE and sends nothing: no account, no key, no network call.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The supplier's well orderings are those of IDT's published plate order form.

**Does not:**
- Lays out the order; it checks nothing about the oligos themselves.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `oligos` | string[] | **yes** |  |  | the oligos to lay out, 5'→3'. Wire them from a design run, or list them. With `mixed`, these are read in FORWARD, REVERSE order — two entries per well. |
| `names` | string[] | **yes** |  |  | a name per oligo, in the same order. A plate well is ORDERED BY NAME, so an unnamed oligo is refused rather than numbered: the label is what the supplier ships the tube under. |
| `format` | `96` · `384` |  | `96` |  | wells per plate. Values: 96 (96 well), 384 (384 well). |
| `fill` | `"rows"` · `"columns"` · `"explicit"` |  | `"rows"` |  | how the plate is loaded. It decides the FILE'S COLUMNS, not just the order: a plate filled by row or by column carries no well column at all, because the supplier derives each position from the row order. Values: rows (Rows (A1, A2, A3 …)), columns (Columns (A1, B1, C1 …)), explicit (Explicitly entered). |
| `plate_name` | string |  | `"Plate 1"` |  | the plate's name, which becomes the worksheet's name. Several plates get ' (2)', ' (3)' appended. |
| `mixed` | boolean |  | `false` |  | one well per PRIMER PAIR: `oligos` is read as forward, reverse, forward, reverse, and each plate is written as every well once carrying the forwards and again carrying the reverses. |
| `pad_to_capacity` | boolean |  | `false` |  | write every unused well as the supplier's blank-name, blank-sequence row rather than ending the sheet short. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sheets` | any |  | one entry per PLATE: its name, its grid, how many wells it fills against the plate's capacity, and every laid-out well |
| `tsv` | string |  | the FIRST plate as tab-delimited text, in the column shape the loading direction requires — the shape the supplier's own paste box accepts verbatim. Several plates means several sheets: read `sheets` for the rest |
| `plateCount` | number |  | how many plates the set needed. Branch a workflow on this rather than re-deriving it |
| `columns` | any |  | the header row this order was written with, which is the two-vs-three column rule the loading direction decided |
| `refused` | any |  | every oligo left OUT, with the reason. Never empty-because-nothing-was-checked: an order that is quietly short is one the user pays a supplier for |
| `reading` | string |  | what the order is, generated from the laid-out plates rather than from the request |
| `wellNote` | string |  | why the well labels are written unpadded, which is a collision in the supplier's own form rather than our choice |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_oligo_plate_order",
  "arguments": {
    "oligos": [],
    "names": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_padlock_probes

**Design padlock probes**: _Which padlock probes target this transcript for in-situ sequencing, and which junctions could be ligated on another transcript?_

Design padlock probes for in-situ sequencing against the subject: find the two-arm targets whose melting temperature falls in a window, check each against a BLAST search for any other transcript that could be ligated across the junction, pack non-overlapping targets from the 3' end, and assemble each into its padlock with the backbone given. Without BLAST results it returns the targets to search, and says the junction check has not been run.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Two-arm Tm falls in the window given; the backbone is the one supplied.

**Does not:**
- Without BLAST results it returns the targets to search and says the junction check did not run.
- Packs non-overlapping targets from the 3' end; it does not rank by detection efficiency.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `arm_length` | number |  | `20` | 7–60 | length of each target arm; the target is twice this. In nt. |
| `interval` | number |  | `0` | 0–1000 | fewest bases between two packed targets. In nt. |
| `min_tm` | number |  | `65` | 0–100 | lowest target melting temperature to accept (exclusive), at 0.1 µM probe, 75 mM monovalent, 10 mM divalent salt and 20% formamide. In °C. |
| `max_tm` | number |  | `75` | 0–100 | highest target melting temperature to accept (exclusive). In °C. |
| `blast_csv` | string |  |  |  | blastn -outfmt 10 output for the targets FASTA this tool returns (run with -word_size 7 -strand plus against your transcriptome). Without it no target is checked for junction specificity. |
| `variants` | string |  |  |  | comma-separated accessions (no version) that count as the target itself, such as its isoforms. Empty: a hit counts as the target only when its accession is in the subject's name. Only applies when blast_csv is set. Advanced. |
| `linker_upstream` | string |  | `"LINKERFIRST"` |  | backbone sequence between the 3' arm and the barcode. Advanced. |
| `barcode` | string |  | `"XXXX"` |  | the barcode read out by sequencing. Advanced. |
| `linker_downstream` | string |  | `"LINKERSECOND"` |  | backbone sequence between the barcode and the 5' arm. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `padlocks` | any |  | the final padlock probes (target found in the database), each with its start, target, full sequence and Tm. Null until `blast_csv` is given: the junction check has not been run |
| `packed` | any |  | every packed target before the database-mappability filter. Null until `blast_csv` is given |
| `targetsFasta` | string |  | the melting-temperature-passing targets as FASTA, named target_N, for blastn |
| `padlockCount` | number or null |  | how many padlock probes survived. Null until `blast_csv` is given, because a 0 would read as none surviving a check that has not been run |
| `explanation` | any |  | the derivation chain: conclusion, interpretation and machinery, generated from this run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_padlock_probes",
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

### design_rbs

**Design RBS**: _Which 5'UTR puts a CDS's translation initiation at a target strength?_

Design a 5'UTR (Shine-Dalgarno + spacer) in front of a CDS to hit a target translation-initiation strength (SC-08 engine, Turner-2004 folding).

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The strength model is the one score_rbs reports, folded under Turner 2004.
- A bacterial host matching the model's anti-SD sequence.

**Does not:**
- Hits a relative strength, not an absolute protein yield.
- The search is over Shine-Dalgarno and spacer; the CDS's own 5' end is not recoded.

**Not read from this result:** The RBS tab shows the designed 5′UTR with its predicted strength, ΔG, spacing and whether it reached the target, and writes no sentence over them; the strength reading belongs to score_rbs, which carries one.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds` | string |  |  |  | the CDS starting at its start codon; unset = the open record's sequence. |
| `target_strength` | number | **yes** | `1` | ≥ 0 | target relative strength, on the model's own scale — 1 is as strong as its reference site, and real sites do score above it. |
| `upstream` | string |  |  |  | upstream context 5' of the UTR (engine default when unset). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `utr` | string |  | the designed 5'UTR |
| `sd` | string |  | the Shine-Dalgarno core |
| `full` | string |  | UTR + CDS |
| `spacing` | number |  | SD→start spacing |
| `relStrength` | number |  | achieved relative strength |
| `onTarget` | boolean |  | whether the target strength was reachable |
| `dgTotal` | number or null | kcal/mol | the predicted total free energy of translation initiation (ΔG_total, kcal/mol) for the designed site; null when the model could not fold it |
| `achievableMin` | number or null |  | the weakest relative strength any candidate site reached in this search, which bounds what a target below it can get |
| `achievableMax` | number or null |  | the strongest relative strength any candidate site reached in this search, which bounds what a target above it can get |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_rbs",
  "arguments": {
    "target_strength": 1,
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_xenium_probes

**Design xenium probes**: _Which 40 nt targets of this transcript meet 10x's Xenium custom-panel rules, and which would another transcript also bind?_

Design Xenium custom-panel padlock targets on the subject transcript to 10x Genomics' published rules (CG000683): two 20 nt arms whose primer3 melting temperatures fall in their windows, a ligation-junction dinucleotide the Xenium ligase accepts, no run of five G in the probe, at least four mismatches across both arms to every other transcript in a BLAST search, and probes at least 10 bp apart. Without BLAST results it returns the targets to search and says the off-target check has not been run.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Tm is primer3's calc_tm with the buffer 10x lists (10 mM monovalent, 20 mM divalent, 10 mM dNTP, 5 µM oligo, Schildkraut salt correction).
- The accessions given as the gene, its isoforms included, are not off-targets.

**Does not:**
- Without BLAST results no target is checked for off-target homology, and the result says so.
- Homopolymers and low complexity are not screened: the note names them without a threshold.
- Which passing targets to keep is ours (preferred junctions, then the coding sequence, then 5' to 3'); 10x's own designer is not public.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `arm_length` | number |  | `20` | 10–30 | length of each arm; the target is twice this. 10x's arms are 20 nt, shorter only for a short target whose Tm stays in range. In nt. Advanced. |
| `tm_rule` | `"either"` · `"full"` · `"arms"` · `"both"` |  | `"either"` |  | which melting temperatures must fall in their windows. 10x: the full length between 68 and 82 °C or each arm between 50 and 70 °C. |
| `min_full_tm` | number |  | `68` | 0–100 | lowest Tm of the whole target (inclusive). In °C. |
| `max_full_tm` | number |  | `82` | 0–100 | highest Tm of the whole target (inclusive). In °C. |
| `min_arm_tm` | number |  | `50` | 0–100 | lowest Tm of each arm (inclusive). In °C. |
| `max_arm_tm` | number |  | `70` | 0–100 | highest Tm of each arm (inclusive). In °C. |
| `junctions` | `"preferred"` · `"preferred and neutral"` · `"any"` |  | `"preferred and neutral"` |  | ligation-junction dinucleotides to accept, from 10x's empirical ligase preferences; 10x strongly recommends avoiding the nonpreferred four. |
| `max_g_run` | number |  | `4` | 1–40 | longest run of G the probe may carry; 10x: avoid five or more. Advanced. |
| `blast_csv` | string |  |  |  | blastn -outfmt 10 output for the targets FASTA this tool returns, searched against the transcriptome (not the genome) with -word_size 7 -strand plus. Without it no target is checked for off-target homology. |
| `gene_accessions` | string |  |  |  | comma-separated accessions (no version) that are this gene, its isoforms included: hits to them are not off-targets. Empty: the subject's name. Only applies when blast_csv is set. |
| `min_mismatches` | number |  | `4` | 1–40 | fewest mismatches across both arms an off-target hit must carry for the target to be kept; gaps and unaligned ends count. Only applies when blast_csv is set. |
| `spacing` | number |  | `10` | 0–1000 | fewest bases between two kept targets. In bp. |
| `probes_per_gene` | number |  | `8` | 1–100 | targets to keep; 10x's predesigned panels use eight per gene. |
| `prefer_cds` | boolean |  | `true` |  | rank targets inside the subject's CDS feature before the untranslated regions, as 10x advises where possible. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `probes` | any |  | the kept targets, each with its 0-based start, target (mRNA sense), probe (its reverse complement), arm and full-length Tm, junction and its class, and the fewest off-target mismatches. Null until `blast_csv` is given |
| `probeCount` | number or null |  | how many targets were kept. Null until `blast_csv` is given |
| `stages` | any |  | what each rule took in and kept, in order, with the reason a skipped check did not run |
| `targetsFasta` | string |  | the targets that pass the Tm, junction and G-run rules as FASTA, named xenium_<1-based start>, for blastn |
| `explanation` | any |  | the derivation chain: conclusion, interpretation and machinery, generated from this run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_xenium_probes",
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

### discover_annotation_contradictions

**Discover annotation contradictions**: _Which signal peptides or transmembrane segments in reviewed human UniProt does a sequence predictor contradict?_

Find the signal peptides or transmembrane segments in reviewed human UniProt that a sequence predictor contradicts. Each feature backed by experiment (evidence code ECO:0000269) is scored to say what a confirmed feature looks like to the predictor; every other feature, annotated from similarity, sequence analysis or a rule, is ranked among those scores, and its conformal p-value (1 + experimental features scoring at or below it) / (experimental + 1) is corrected across all of them. Signal, by either predictor: von Heijne's weight-matrix score (EMBOSS sigcleave) of the cleavage site UniProt annotates, or DeepSig's probability that the protein carries a signal peptide at all (its eukaryotic network ensemble, from the first 96 residues). Transmembrane: the share of the segment the HMM-TM topology model labels membrane helix. A contradiction is a disagreement between two models, to be read, not a correction of UniProt: von Heijne's matrix and the HMM-TM model are weaker than the SignalP and TMHMM runs behind most such annotations; DeepSig is of their generation. The result carries a self-check, half the experimental features tested against the other half, whose calls are all false by construction.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Experimentally confirmed features (ECO:0000269) show what a true feature looks like to the predictor.
- Conformal p-values: confirmed and other features are exchangeable under the null.

**Does not:**
- A contradiction is a disagreement between two models, to be read, not a correction of UniProt.
- von Heijne's matrix and the HMM-TM model are weaker than the predictors behind most annotations.

**Validated:** against the reference implementation by 2 golden suites.

**Reads bundled data:** uniprot-human-signal-transmembrane.json, euk-dnn.json, hmmtm.mdel

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `feature` | `"signal"` · `"transmembrane"` |  | `"signal"` |  | which annotation to test: signal peptides or transmembrane segments. Values: signal (Signal peptides), transmembrane (Transmembrane segments). |
| `predictor` | `"von-heijne"` · `"deepsig"` |  | `"von-heijne"` |  | signal only: von Heijne's matrix asks whether signal peptidase would cut where UniProt says; DeepSig asks whether the protein has a signal peptide at all (it loads 9.8 MB of network weights and runs twenty networks per protein, so it is far slower than the matrix). Values: von-heijne (von Heijne matrix), deepsig (DeepSig). Only applies when feature is signal. |
| `alpha` | number |  | `0.05` | 0.0001–0.5 | false discovery rate at which an annotation is called contradicted. |
| `correction` | `"BH"` · `"BY"` |  | `"BH"` |  | Benjamini–Hochberg (independent or positively dependent tests; conformal p-values against one calibration set are positively dependent) or Benjamini–Yekutieli (any dependence; less power). Values: BH (Benjamini–Hochberg), BY (Benjamini–Yekutieli). |
| `decoding` | `"viterbi"` · `"posterior-viterbi"` · `"optimal-accuracy"` |  | `"viterbi"` |  | transmembrane only: which HMM-TM decoder labels the residues. N-best is left out: it takes minutes per long protein, and the corpus has 5,231. Values: viterbi (Viterbi), posterior-viterbi (Posterior-Viterbi), optimal-accuracy (Optimal accuracy). Only applies when feature is transmembrane. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `contradicted` | any |  | the annotations contradicted at the chosen false discovery rate: accession, gene, span, statistic, p and q |
| `count` | number |  | how many annotations are contradicted |
| `selfCheck` | any |  | half the experimental features tested against the other half: raw p ≤ α should be near α of them, and FDR calls near none |
| `result` | any |  | the full result, every tested annotation included |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_annotation_contradictions",
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

### discover_codon_outliers

**Discover codon outliers**: _Which genes of a genome use synonymous codons in a way the genome's own average does not explain?_

Score every coding sequence of a genome against the genome's own codon usage and report the genes whose synonymous codon choice that average does not explain, with the false discovery rate controlled across the genes. Records from different files are different genomes: each is scored against its own file's usage, and the false discovery rate is controlled once across every gene of every genome. Each gene gets Karlin's B and Supek & Vlahoviček's MILC against the pooled usage of the genes, and a G-test of its codon choice within each amino acid against that usage (χ², degrees of freedom from the amino acids it uses). Outliers are typically highly expressed genes (ribosomal proteins are the most deviant class), genes of unusual composition, and some of foreign origin; an outlier is NOT evidence of horizontal transfer, since codon bias is a poor indicator of transfer.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Records from one file are one genome, scored against that genome's pooled codon usage.
- The genetic code given is the one the genes are translated with.

**Does not:**
- An outlier is typically highly expressed or of unusual composition; it is not evidence of horizontal transfer.
- Genes below the minimum codon count are left out and listed.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] |  |  |  | the genomes' coding sequences: wire upstream records here, or list library document names (each record of a CDS FASTA is one gene, read in frame from its first base; each file is one genome). |
| `genetic_code` | `1` · `2` · `3` · `4` · `5` · `6` · `9` · `10` · `11` · `12` · `13` · `14` · `15` · `16` · `21` · `22` · `23` · `24` · `25` · `26` · `27` · `28` · `29` · `30` · `31` · `32` · `33` |  | `1` |  | NCBI genetic code the genes are read with (4 for Mycoplasma, 11 for most bacteria; 1 and 11 group codons identically). Values: 1 (1 · Standard), 2 (2 · Vertebrate Mitochondrial), 3 (3 · Yeast Mitochondrial), 4 (4 · Mold Mitochondrial, Protozoan Mitochondrial, Coelenterate Mitochondrial, Mycoplasma, Spiroplasma), 5 (5 · Invertebrate Mitochondrial), 6 (6 · Ciliate Nuclear, Dasycladacean Nuclear, Hexamita Nuclear), 9 (9 · Echinoderm Mitochondrial, Flatworm Mitochondrial), 10 (10 · Euplotid Nuclear), 11 (11 · Bacterial, Archaeal and Plant Plastid), 12 (12 · Alternative Yeast Nuclear), 13 (13 · Ascidian Mitochondrial), 14 (14 · Alternative Flatworm Mitochondrial), 15 (15 · Blepharisma Macronuclear), 16 (16 · Chlorophycean Mitochondrial), 21 (21 · Trematode Mitochondrial), 22 (22 · Scenedesmus obliquus Mitochondrial), 23 (23 · Thraustochytrium Mitochondrial), 24 (24 · Rhabdopleuridae Mitochondrial), 25 (25 · Candidate Division SR1 and Gracilibacteria), 26 (26 · Pachysolen tannophilus Nuclear), 27 (27 · Karyorelict Nuclear), 28 (28 · Condylostoma Nuclear), 29 (29 · Mesodinium Nuclear), 30 (30 · Peritrich Nuclear), 31 (31 · Blastocrithidia Nuclear), 32 (32 · Balanophoraceae Plastid), 33 (33 · Cephalodiscidae Mitochondrial). |
| `min_codons` | number |  | `80` | 0–1000 | genes with no more codons than this leave the reference and the result: the G-test's χ² limit is poor for short genes. In codons. |
| `alpha` | number |  | `0.05` | 0.0001–0.5 | false discovery rate at which a gene is reported as an outlier. |
| `correction` | `"BH"` · `"BY"` |  | `"BH"` |  | Benjamini–Hochberg (independent or positively dependent tests) or Benjamini–Yekutieli (any dependence; less power). Values: BH (Benjamini–Hochberg), BY (Benjamini–Yekutieli). |
| `file_codes` | string[] |  |  |  | a genetic code for one file, as `file=code` (e.g. `Mycoplasma_genitalium_cds.fna=4`): that file's genes are read with it, every other file with genetic_code. For a corpus whose genomes translate differently. Advanced. |
| `pool_files` | boolean |  | `false` |  | score every named record as ONE genome, for a genome split across files (one per chromosome). Off: each file is its own genome, scored against its own usage. |
| `alt_init` | boolean |  | `false` |  | count every alternative start codon as Met throughout each gene, as coRdon does by default. Off reads an internal alternative start codon as its own amino acid. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `outliers` | any |  | genes at q ≤ alpha, largest MILC first |
| `outlierCount` | number |  | how many genes were called outliers |
| `genes` | any |  | every gene scored: codons, B, MILC, G, degrees of freedom, p and q |
| `skipped` | any |  | genes left out as too short, with their codon counts |
| `result` | any |  | the full result, with the settings that produced it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_codon_outliers",
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

### estimate_effect_size

**Estimate effect size**: _How large is the effect in pilot data, standardized, with a confidence interval, ready to size the full experiment?_

The effect a power calculation needs, measured from a pilot instead of guessed: two groups of one measurement in a table, standardized as Hedges' g (default), Cohen's d or Glass's Δ with its noncentral-t confidence interval (effectsize 1.0.3, reproduced), and the two-sample t design sized at the estimate and at the interval limit nearest zero. A column can be subtracted row by row first (a reference gene's Ct, giving delta-Ct). Returns the `design` calculate_power takes: Cohen's d for the `t` test, the raw difference and SD for `t_raw`.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The pilot measures the same quantity, on the same population, as the planned experiment.
- Observations are independent within groups; the noncentral-t interval assumes normal errors.

**Does not:**
- A small pilot gives a wide interval; sizing from the point estimate alone understates the samples needed when the true effect sits at the low end.
- Pilot effects are biased upward when a pilot was continued because it looked promising.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `table` | string | **yes** |  |  | the pilot: a header row, then one row per observation. Tab- or comma-separated. |
| `value` | string | **yes** |  |  | the column holding the measurement. |
| `subtract` | string |  |  |  | a column subtracted from the measurement row by row before anything else: a reference gene's Ct (giving delta-Ct), a baseline. |
| `group_column` | string |  |  |  | the column naming each row's group. Or give `groups`. |
| `groups` | string |  |  |  | one group label per data row, in row order, separated by commas, spaces or new lines, when the table has no group column. |
| `group` | string |  |  |  | the group compared. Left unset, the second group to appear. |
| `reference` | string |  |  |  | the group it is compared against (the control). Left unset, the first group to appear. |
| `estimator` | `"hedges_g"` · `"cohens_d"` · `"glass_delta"` |  | `"hedges_g"` |  | Hedges' g corrects Cohen's d's small-sample bias by the exact J(df); Cohen's d is the uncorrected standardized difference; Glass's Δ standardizes by the reference group's SD alone, for when the treatment changes the spread. Values: hedges_g (Hedges' g), cohens_d (Cohen's d), glass_delta (Glass's Δ). |
| `pooled_sd` | boolean |  | `true` |  | standardize by the pooled SD (Student). Off averages the two variances, with Welch's df. Only applies when estimator is hedges_g or cohens_d. |
| `paired` | boolean |  | `false` |  | the two groups are the same subjects measured twice, paired by row order within each group. Only applies when estimator is hedges_g or cohens_d. |
| `ci` | number |  | `0.95` | 0.5–0.999 | the confidence level of the interval. |
| `alternative` | `"two.sided"` · `"less"` · `"greater"` |  | `"two.sided"` |  | a two-sided interval, or one bounded on one side. Values: two.sided (Two-sided), less (Less (upper bound only)), greater (Greater (lower bound only)). Advanced. |
| `power` | number |  |  | 0–1 | size the design for this power; leave empty to estimate the effect only. |
| `sig_level` | number |  | `0.05` | 0–1 | α for the sizing. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `estimate` | number or null |  | the standardized effect |
| `interval` | any |  | the confidence interval: level, low, high |
| `groups` | any |  | every group in the table: n, mean and SD of the measurement |
| `design` | any |  | what calculate_power takes: the t test's d (`effect`), and the raw `difference` and `sd` for t_raw |
| `sizing` | any |  | pwr.t.test's sample size at the estimate and at the limit nearest zero, when power was given |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "estimate_effect_size",
  "arguments": {
    "table": "<string>",
    "value": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### export_barcodes

**Export barcodes**: _What does this index set look like as an order sheet, a FASTA, a SampleSheet, or the actual oligos?_

Write an index set out in the form the next step needs: a CSV or TSV order sheet, FASTA, an IDT bulk-input sheet of the bare tags, an Illumina BCLConvert SampleSheet, or the actual oligos — adapters built on a template, or primers carrying the tag — with the junction warnings that emission produces.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Emits the set with its junction warnings; it designs and checks nothing.

**No scientific claim:** Writes an index set in the form the next step reads; the set's properties come from audit_barcodes.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `barcodes` | string[] | **yes** |  |  | the index sequences to write out. |
| `format` | `"csv"` · `"tsv"` · `"fasta"` · `"idt"` · `"samplesheet"` · `"adapters"` · `"primers"` |  | `"csv"` |  | what to write. Values: csv (CSV order sheet), tsv (TSV), fasta (FASTA), idt (IDT bulk input), samplesheet (Illumina SampleSheet), adapters (Adapter oligos), primers (Tagged primers). |
| `prefix` | string |  | `"BC"` |  | name prefix for the rows (BC001, BC002 …). |
| `idt_scale` | string |  |  |  | IDT synthesis scale, exactly as IDT writes it (e.g. 25nm, 100nm, 250nm). Asked for rather than defaulted: which options exist depends on oligo length. Only applies when format is idt. |
| `idt_purification` | string |  |  |  | IDT purification (e.g. STD, PAGE, HPLC). Check what your scale allows before ordering. Only applies when format is idt. |
| `primer` | string |  |  |  | the primer the tag is added to. Only applies when format is primers. |
| `adapter_5` | string |  | `"AATGATACGGCGACCACCGAGATCTACAC"` |  | sequence 5' of the tag in the adapter — the Illumina P5, as the panel offers. Only applies when format is adapters. |
| `adapter_3` | string |  | `"ACACTCTTTCCCTACACGACGCTCTTCCGATCT"` |  | sequence 3' of the tag in the adapter — the TruSeq read-1 primer, as the panel offers. Only applies when format is adapters. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `text` | string |  | the written file, for the text formats |
| `oligos` | any |  | the emitted oligos, for the adapter and primer formats — empty for the text formats |
| `warnings` | any |  | junction warnings the emission found — a tag that creates a homopolymer or a restriction site at its junction. Empty for the text formats, which build no junction |
| `count` | number |  | how many barcodes were written |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "export_barcodes",
  "arguments": {
    "barcodes": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### optimize_sequence

**Optimize sequence**: _What sequence satisfies these constraints and scores best on these objectives?_

Run the DnaChisel optimizer over the subject with real constraints/objectives (GC window, pattern avoidance, translation enforcement, …). Emits the optimized sequence as a NEW record for downstream nodes.

<sub>returns new records · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The constraints and objectives given state the real requirements; DnaChisel's solver resolves them.

**Does not:**
- A constraint the solver cannot satisfy is reported as unresolved, not silently dropped.
- The search is heuristic: a better sequence may exist.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `constraints` | object[] |  |  |  | DnaChisel constraint specs, e.g. [{"kind":"EnforceGCContent","mini":0.4,"maxi":0.6,"window":50}] — hard requirements the solution must satisfy. Valid `kind` values: EnforceTranslation, AvoidPattern, EnforceGCContent, AvoidHairpins, AvoidRareCodons, UniquifyAllKmers, CodonOptimize, EnforceSequence, AvoidChanges, EnforceChoice, EnforcePatternOccurence, AvoidStopCodons, EnforceMeltingTemperature, EnforceChanges, EnforceTerminalGCContent, SequenceLengthBounds, EnforceRbsStrength, AvoidHeterodimerization, AllowPrimer, EnforceRegionsCompatibility, AvoidMatches, AvoidBlastMatches. |
| `objectives` | object[] |  |  |  | DnaChisel objective specs — soft goals the solver maximises. Same `kind` values as constraints: EnforceTranslation, AvoidPattern, EnforceGCContent, AvoidHairpins, AvoidRareCodons, UniquifyAllKmers, CodonOptimize, EnforceSequence, AvoidChanges, EnforceChoice, EnforcePatternOccurence, AvoidStopCodons, EnforceMeltingTemperature, EnforceChanges, EnforceTerminalGCContent, SequenceLengthBounds, EnforceRbsStrength, AvoidHeterodimerization, AllowPrimer, EnforceRegionsCompatibility, AvoidMatches, AvoidBlastMatches. |
| `candidates` | number |  | `1` | 1–12 | how many alternative solutions to produce (1 = a single solve). Candidate 1 is the plain unseeded answer; the rest run at seed+1, seed+2, …, so a listed alternative can be asked for again. Max 12. |
| `seed` | number |  | `1` | ≥ 0 | base seed for the alternatives — the same seed returns the same set. Advanced. |
| `randomization_threshold` | number |  |  | ≥ 1 | DnaChisel `randomization_threshold` (default 10000). LOWER it to force the stochastic search: an objective-driven problem is deterministic, so without this every candidate comes back identical. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the optimized sequence as a record |
| `sequence` | string |  | the optimized sequence |
| `success` | boolean |  | all hard constraints satisfied |
| `nEdits` | number |  | nucleotides changed |
| `gcAfter` | number |  | GC fraction after optimization |
| `caiAfter` | number or null |  | CAI after optimization, or null when not computable (no codon table to score against): a 0 would read as the worst possible adaptation |
| `candidates` | any |  | every alternative solution: its seed, sequence, edit count, GC and CAI — compare them before choosing. Empty unless `candidates` asks for more than one |
| `distinct` | number |  | how many of the candidates are DIFFERENT sequences — 1 means the problem has a single answer, not that the run failed. The engine omits it for a single-candidate run, where it is 1 by definition |
| `gcProfile` | object or null |  | windowed GC before and after, at each window's centre: the stretches the solver moved, which the two whole-sequence GC numbers average away |
| `gcProfile.x` | number[] |  |  |
| `gcProfile.series` | object[] |  |  |
| `gcProfile.series[].name` | string |  |  |
| `gcProfile.series[].y` | (number or null)[] |  |  |
| `gcProfile.xLabel` | string |  |  |
| `gcProfile.yLabel` | string |  |  |
| `gcProfile.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `gcProfile.title` | string |  |  |
| `gcProfile.rules` | object[] |  |  |
| `gcProfile.rules[].y` | number |  |  |
| `gcProfile.rules[].label` | string |  |  |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "optimize_sequence",
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

### rank_next_tests

**Rank next tests**: _Which candidate experiment would teach the most about the hypothesis it is registered against, and how much of it is worth running?_

Rank candidate experiments by what running them would TEACH — Lindley's expected information gain, the drop in uncertainty about a hypothesis expected before anything is run. Three grains: `tests` ranks candidate falsification tests against the beliefs a discovery ledger holds, each with the posterior its two outcomes would leave, by gain and separately by gain per unit cost; `measurements` says what n readings of a normal quantity would teach, and how many it takes to reach a target; `trials` says the same for a rate held as a Beta. A gain is what a result would settle whichever way it lands — never evidence that a hypothesis is true, which stays with the ledger's e-values.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- A candidate's power is its power at the effect that matters, and its alpha the size it will be run at; the gain is no better than those two numbers.
- The belief a test is ranked against is the ledger's elicited belief for that hypothesis, or one the caller supplied.
- `measurements` assumes a normal quantity with known noise; `trials` assumes exchangeable draws at one rate.

**Does not:**
- An informative test is not a test worth running: a high gain on a hypothesis nobody cares about is still high.
- Two candidates reading the same data are not two independent looks; the overlap is named, never subtracted, because what it costs depends on how each test uses the data.
- A hypothesis with no recorded belief is not ranked, since an invented prior would decide the order.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `mode` | `"tests"` · `"measurements"` · `"trials"` |  | `"tests"` |  | which grain of the question: rank candidate tests, size a run of measurements, or size a run of trials. Values: tests (Candidate tests), measurements (Measurements of a mean), trials (Trials of a rate). |
| `tests` | object[] |  |  |  | the candidates, each `{id, hypothesis, power, alpha}` and optionally `cost`, `reads` (what it would read) and `label`. Only applies when mode is tests. |
| `ledger` | object |  |  |  | a jane.discovery-ledger file, as `run_discovery_programme` returns: its elicited beliefs and the sources its evidence already read. Only applies when mode is tests. |
| `beliefs` | object |  |  |  | belief that each hypothesis is true, as `{hypothesisId: probability}` — given directly, or to override the ledger's. Only applies when mode is tests. |
| `prior_sd` | number |  |  | ≥ 0 | how uncertain the mean is now, as a standard deviation. Only applies when mode is measurements. |
| `noise_sd` | number |  |  | ≥ 0 | the measurement noise, in the same units. Only applies when mode is measurements. |
| `n` | number |  | `1` | ≥ 1 | how many measurements the run would take. Only applies when mode is measurements. |
| `target_bits` | number |  |  | ≥ 0 | a gain to reach: the answer says how many measurements it would take. Only applies when mode is measurements. |
| `alpha` | number |  | `1` | ≥ 0 | the Beta prior's α — successes already believed in. Only applies when mode is trials. |
| `beta` | number |  | `1` | ≥ 0 | the Beta prior's β — failures already believed in. Only applies when mode is trials. |
| `trials` | number |  | `10` | ≥ 1 | how many trials the run would take. Only applies when mode is trials. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `best` | string |  | the most informative candidate's id, or the mode's own answer in words |
| `bits` | number or null |  | the expected information gain of the top answer, in bits |
| `ranked` | any |  | every ranked candidate: gain, gain per unit cost, the prior it stands on and the posterior each outcome would leave |
| `byCost` | any |  | the same candidates ordered by gain per unit cost, when every one was priced |
| `beliefs` | any |  | the belief each hypothesis was ranked against, and where it came from |
| `samplesForTarget` | number or null |  | how many measurements reach `target_bits`; null when no target was set |
| `gain` | any |  | the gain itself: nats, bits, and the entropies before and after. Absent when candidate tests were ranked, where each one carries its own |
| `note` | string |  | why a ranking is short or empty, when it is |
| `result` | any |  | the full answer, with the settings that produced it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "rank_next_tests",
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

### rank_tradeoffs

**Rank tradeoffs**: _Which candidates in a table does no other candidate beat on every objective at once, how deep does each of the rest sit, and which candidate beats it?_

Which candidates in a table are not beaten on every objective at once: Pareto (non-dominated) sorting of rows scored on several columns, each to maximize or minimize. Returns each candidate's front (1 = non-dominated), the candidate one front up that beats it, and its crowding distance within its front (how isolated it is, so a short list can be spread along the front). Rows can be filtered first (`em_max>=580, agg=m`), and rows with an empty objective are left out and counted, never ranked last. moocore 0.3.2's pareto_rank and is_nondominated, emoa 0.5-3's and pymoo 0.6.2's crowding distances, reproduced.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Each objective column is a number where higher (maximize) or lower (minimize) is better.
- Measured values are taken as exact.

**Does not:**
- The first front does not choose for the user: which weighting of the objectives is right is a scientific judgement.
- Two candidates whose values differ by less than measurement error are still ordered by those values.
- With many objectives most candidates are non-dominated.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `table` | string | **yes** |  |  | the candidates: a header row, then one row per candidate. Comma- or tab-separated, quoted cells allowed. |
| `maximise` | string |  |  |  | the columns where higher is better, separated by commas. |
| `minimise` | string |  |  |  | the columns where lower is better, separated by commas. |
| `label` | string |  |  |  | the column naming each candidate. Left unset, the first column. |
| `filter` | string |  |  |  | keep only rows passing every clause, separated by commas: a column, one of = != >= <= > <, and a value (`em_max>=580, agg=m`). Numbers compare as numbers; a blank cell passes no ordering clause. |
| `crowding` | `"normalised"` · `"raw"` |  | `"normalised"` |  | how isolation along a front is measured: NSGA-II's normalized distance (each gap over the objective's range, averaged), or the raw sum of gaps in each objective's own units. Values: normalised (NSGA-II (normalized)), raw (raw gaps). Advanced. |
| `keep_duplicates` | boolean |  | `true` |  | keep every copy of candidates with identical values on the first front; off keeps the first copy and names it as what the others duplicate. Advanced. |
| `order` | `"crowding"` · `"hypervolume"` |  | `"crowding"` |  | what orders candidates within a front: crowding distance (how isolated each is), or exclusive hypervolume contribution (how much of the objective space the front loses without it). Values: crowding (crowding distance), hypervolume (hypervolume contribution). |
| `reference` | string |  |  |  | the hypervolume's reference point, one `column=value` per objective (`brightness=0, maturation=500`), each worse than every candidate. Left unset, each objective's worst value pushed out by 10% of its range. Only applies when order is hypervolume. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `front` | any |  | the non-dominated candidates (front 1), most isolated first |
| `ranked` | any |  | every candidate ranked: front, flag, crowding distance, the candidate that beats it, its objective values |
| `fronts` | any |  | how many candidates sit on each front |
| `counts` | any |  | rows in the table, filtered out, left out for an empty objective, ranked |
| `order` | string or null |  | what ordered candidates within a front: crowding or hypervolume |
| `hypervolume` | number or null |  | the objective space front 1 dominates up to the reference point (hypervolume order only) |
| `reference` | any |  | the reference point the hypervolume was measured from, and whether it was derived (hypervolume order only) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "rank_tradeoffs",
  "arguments": {
    "table": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### score_rbs

**Score RBS**: _How strong is the ribosome-binding site already in front of this start codon, and what sets that strength?_

Score the ribosome-binding site already in front of a start codon: the Shine-Dalgarno hybridisation energy, the mRNA folding that competes with it, the spacing it implies, and the resulting relative initiation strength. This reads an existing 5'UTR — design_rbs writes a new one.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The Shine-Dalgarno hybridisation and competing mRNA folding are the model's terms, folded under Turner 2004.
- A bacterial host with the 16S anti-SD sequence the model uses.

**Does not:**
- A relative strength, not a measured protein yield.
- Reads an existing 5'UTR; design_rbs writes one.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `mrna` | string |  |  |  | the mRNA (or DNA) carrying the UTR and the CDS — leave unset to use the open record. |
| `start_pos` | number | **yes** |  | ≥ 0 | 0-based position of the start codon's first base within `mrna`. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `relStrength` | number |  | relative initiation strength (higher = stronger) |
| `dgTotal` | number or null |  | total free energy of the initiation state (null when no Shine-Dalgarno could be placed) |
| `dgHybrid` | number or null |  | Shine-Dalgarno · anti-SD hybridisation energy (null when no Shine-Dalgarno could be placed) |
| `dgMrna` | number |  | folding energy of the mRNA window that competes with initiation |
| `spacing` | number or null |  | bases between the Shine-Dalgarno and the start codon (null when no Shine-Dalgarno could be placed) |
| `sdStart` | number or null |  | 0-based position in `mrna` where the winning Shine-Dalgarno begins (null when none could be placed) |
| `sdLength` | number or null |  | length of that Shine-Dalgarno, in bases (null when no Shine-Dalgarno could be placed) |
| `structure` | string |  | dot-bracket secondary structure of the folded initiation window (empty when the window is too short to fold) |
| `structureStart` | number |  | 0-based position in `mrna` that the first character of `structure` sits on |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "score_rbs",
  "arguments": {
    "start_pos": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### simulate_rnaseq_power

**Simulate rnaseq power**: _For a two-group RNA-seq experiment analyzed with edgeR, what power and false discovery rate does each number of replicates actually achieve, for genes at each expression level, and how would more sequencing depth change it?_

Power and FDR for a two-group RNA-seq experiment by SIMULATION (PROPER 1.44.0): whole experiments drawn from a real pilot (Cheung, Gilad, Bottomly, MAQC, or a sequencing depth), each run through edgeR's exact test at every sample size. Reports power stratified by expression, the FDR actually achieved, true and false calls, and power at other depths; reproducible from its seed, value for value against R.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- Counts are negative binomial with the pilot's per-gene mean and dispersion; the DE genes are a random `changed_fraction` of all genes, with log fold changes from PROPER's normal(0, 1.5) unless one is given.
- Every experiment is analyzed with edgeR's classic pipeline (TMM, common then tagwise dispersion, exact test, Benjamini-Hochberg).
- A pilot's parameters stand for the experiment to be run: same organism, tissue and protocol.

**Does not:**
- The answer is a Monte-Carlo estimate: its standard error is reported, and more rounds narrow it.
- Only edgeR's exact test is simulated; PROPER's DESeq2 and DSS arms are not run, and a lab using another pipeline sees a different power.
- Depth re-weighting (power.seqDepth) reuses the stratified power at the simulated depth; after filtering PROPER misaligns it, which is reproduced and flagged.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `pilot` | `"cheung"` · `"gilad"` · `"bottomly"` · `"maqc"` · `"depth"` · `"constant"` |  | `"cheung"` |  | where each gene's baseline expression comes from: one of PROPER's pilots, a sequencing depth applied to aggregated human expression, or one constant. Values: cheung (Cheung (unrelated people, large dispersion)), gilad (Gilad (human liver, moderate)), bottomly (Bottomly (inbred mice, small)), maqc (MAQC (technical replicates)), depth (Sequencing depth), constant (One constant). |
| `reads_per_sample` | number |  |  | ≥ 1 | total reads per sample. Only applies when pilot is depth. |
| `log_mean` | number |  |  |  | the natural-log mean count every gene shares. Only applies when pilot is constant. |
| `dispersion` | number |  |  | ≥ 0 | one dispersion (BCV²) for every gene, instead of the pilot's; left unset, the pilot's own. Advanced. |
| `dispersion_pilot` | `"cheung"` · `"gilad"` · `"bottomly"` · `"maqc"` |  |  |  | take dispersions from this pilot instead (with a depth or a constant baseline, Cheung's unless set). Advanced. |
| `genes` | number |  | `20000` | ≥ 100 | genes in the simulated experiment. |
| `changed_fraction` | number |  | `0.05` | 0–1 | the proportion of genes that are differentially expressed. |
| `log_fold_change` | number |  |  |  | one log fold change for every DE gene; left unset, PROPER's normal(0, 1.5) draws. Advanced. |
| `replicates` | number[] |  | `[3, 5, 7, 10]` |  | replicates per group at each sample size to evaluate. |
| `second_group` | number[] |  |  |  | replicates in the second group at each size, when the groups differ. Advanced. |
| `rounds` | number |  | `20` | 1–1000 | simulated experiments. PROPER's own default is 100; each is a full edgeR run at every sample size, so time grows with it. |
| `seed` | number |  | `11111` |  | the seed; round i uses seed + i, as PROPER does. Advanced. |
| `call_by` | `"fdr"` · `"pval"` |  | `"fdr"` |  | call a gene by its FDR or its raw p-value. Values: fdr (FDR), pval (raw p-value). |
| `cutoff` | number |  | `0.1` | 0–1 | the cut-off a gene is called at. |
| `target` | `"lfc"` · `"effectsize"` |  | `"lfc"` |  | which DE genes count as worth finding: by \|log fold change\|, or by \|log fold change\| / √dispersion. Values: lfc (Log fold change), effectsize (Effect size). |
| `threshold` | number |  | `0.5` | ≥ 0 | the threshold a DE gene's size must exceed to count. |
| `stratify_by` | `"expr"` · `"dispersion"` |  | `"expr"` |  | stratify the power by expression (mean normalized count) or by dispersion. Values: expr (Expression), dispersion (Dispersion). Advanced. |
| `strata` | number[] |  |  |  | stratum break points; unset, PROPER's: 0, 10, 20, 40 … 1280, ∞ for expression. Advanced. |
| `filter_by` | `"none"` · `"expr"` |  | `"none"` |  | drop the lowest expression strata before counting, and recompute BH over what is left. Values: none (Keep every gene), expr (Drop low expression). Advanced. |
| `dropped_strata` | number[] |  |  |  | which strata (1-based) to drop. Only applies when filter_by is expr. Advanced. |
| `depth_factors` | number[] |  | `[0.2, 0.5, 1, 2, 5, 10]` |  | sequencing depth multipliers to re-weight power to. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | any |  | per sample size: nominal and achieved FDR (or type I error), marginal power, mean true and false discoveries, false discovery cost |
| `power` | any |  | marginal power at each sample size |
| `powerSE` | any |  | the Monte-Carlo standard error of each marginal power |
| `stratifiedPower` | object or null |  | power by expression (or dispersion) stratum, one line per sample size |
| `stratifiedPower.x` | number[] |  |  |
| `stratifiedPower.series` | object[] |  |  |
| `stratifiedPower.series[].name` | string |  |  |
| `stratifiedPower.series[].y` | (number or null)[] |  |  |
| `stratifiedPower.xLabel` | string |  |  |
| `stratifiedPower.yLabel` | string |  |  |
| `stratifiedPower.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `stratifiedPower.title` | string |  |  |
| `stratifiedPower.rules` | object[] |  |  |
| `stratifiedPower.rules[].y` | number |  |  |
| `stratifiedPower.rules[].label` | string |  |  |
| `strata` | any |  | the stratum intervals the stratified readouts are over |
| `stratifiedFDR` | any |  | achieved FDR by stratum and sample size |
| `seqDepth` | any |  | marginal power re-weighted to each sequencing depth factor, per sample size |
| `rScript` | string |  | the R that reproduces the run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "simulate_rnaseq_power",
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

### tree_taxon_annotations

**Tree taxon annotations**: _What does this NeXML file say about each of its taxa?_

Read what a NeXML tree file says about each of its taxa: every annotation on every OTU (an NCBI taxon, a rank, a parent taxon), one row per annotation, plus how many distinct values each property takes. This is the tip data the phylogeny canvas draws as a strip beside the tips, where a value that recurs further down is a group the tree does not keep together.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The annotations are the file author's; nothing here checks them against the authority they link to.

**Does not:**
- NeXML only: Newick carries no taxon annotations, and NEXUS and PhyloXML annotations are not read.
- An IRI value is reported as written; resolving an NCBI taxon id to a name needs the network.

**Not read from this result:** The answer is the annotations the tree file carries, listed as written; nothing is inferred from them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `nexml` | string | **yes** |  |  | a NeXML document (the text of a .xml tree file). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `annotations` | any |  | one row per annotation: otu id, taxon label, property and value, in document order |
| `properties` | any |  | each annotated property with its count of distinct values |
| `count` | number |  | annotations read |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "tree_taxon_annotations",
  "arguments": {
    "nexml": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
