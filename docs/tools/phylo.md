# 🌳 Alignment & phylogenetics

_Pairwise and multiple alignment, dot plots, model selection, trees and tree comparison._

20 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`align_pair`](#align_pair) | How do these two sequences line up on their own, end to end or over their best-matching stretch? |
| [`align_read`](#align_read) | How does one sequencing read align to the reference, as two gapped rows? |
| [`align_sequences`](#align_sequences) | How do these sequences line up column by column, by partial-order alignment (a pile of reads over one locus) or progressive alignment (a family of homologous genes)? |
| [`alignment_agreement`](#alignment_agreement) | How well do the reads in this window agree with the reference beneath them? |
| [`alignment_pca`](#alignment_pca) | How do the rows of this alignment group, on the principal axes of their pairwise similarity? |
| [`alignment_redundancy`](#alignment_redundancy) | Which rows of this alignment are near-copies of a longer row, at what identity? |
| [`alignment_window`](#alignment_window) | Which reads, what depth and what pairing does this window of the BAM or SAM hold? |
| [`build_tree`](#build_tree) | What phylogeny do these aligned sequences support, under a distance, parsimony, maximum-likelihood or Bayesian method, with branch support? |
| [`compare_trees`](#compare_trees) | How far apart are these trees over the same taxa, and what topology do they share? |
| [`discover_gene_tree_discordance`](#discover_gene_tree_discordance) | Which genes' own alignments reject the species tree (Shimodaira-Hasegawa test against its nearest-neighbour rearrangements)? |
| [`discover_tree_incongruence`](#discover_tree_incongruence) | Do some loci of a multi-locus alignment have a different history from the rest (incongruence length difference test)? |
| [`dot_plot`](#dot_plot) | Where does this sequence resemble itself or another, as a dot plot of repeats, inversions and shared regions? |
| [`dot_plot_grid`](#dot_plot_grid) | Which members of this sequence set share material with which, as an all-against-all grid of dot plots? |
| [`draw_alignment`](#draw_alignment) | What does this window of an alignment look like as a figure? |
| [`draw_tree`](#draw_tree) | What does this tree look like as a figure? |
| [`ebi_align`](#ebi_align) | What does the EMBL-EBI reference tool named return for these sequences? |
| [`export_tree`](#export_tree) | What does this tree look like in Newick, NEXUS, PhyloXML or NeXML? |
| [`select_substitution_model`](#select_substitution_model) | Which substitution model do these data prefer, by AIC, AICc or BIC with Akaike weights? |
| [`transform_tree`](#transform_tree) | What does this tree look like re-rooted, pruned, ladderized, or with weak branches collapsed? |
| [`tree_statistics`](#tree_statistics) | What shape does this tree have: tips, height, balance, the gamma statistic, lineages through time, and the patristic distances? |

---

### align_pair

**Align pair**: _How do these two sequences line up on their own, end to end or over their best-matching stretch?_

Align TWO sequences on their own, globally (Needleman-Wunsch, or Gotoh with an affine penalty) or locally (Smith-Waterman / Gotoh), through biotite's `align_optimal` with the MSA panel's own knobs: substitution matrix, linear or affine gaps, and for a global alignment whether end gaps are charged. Local returns only the best-scoring stretch, with where it lies in each input. The MSA canvas offers it on any row as "Align globally/locally with".

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The two sequences are homologous over the region aligned.
- Scores are the substitution matrix's; a gap costs `gap_penalty` per column, or `gap_open` + k × `gap_extend`.

**Does not:**
- One optimal alignment is returned; others with the same score may exist.
- A local alignment with no positively scoring pair is refused rather than returned empty.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] | **yes** |  |  | exactly two sequences: wire two upstream outputs here, or name two library documents. |
| `mode` | `"global"` · `"local"` |  | `"global"` |  | `global` aligns the two end to end; `local` finds the best-scoring stretch shared by both. Values: global (Global (Needleman-Wunsch / Gotoh)), local (Local (Smith-Waterman / Gotoh)). |
| `align_matrix` | `"auto"` · `"EDNAFULL"` · `"BLOSUM62"` |  | `"auto"` |  | the substitution matrix. `auto` reads the alphabet: EDNAFULL for nucleotides, BLOSUM62 for protein. Values: auto (Auto - from the alphabet), EDNAFULL (EDNAFULL - nucleotides (EMBOSS NUC.4.4)), BLOSUM62 (BLOSUM62 - amino acids). |
| `affine_gap` | boolean |  | `false` |  | `true` charges separate opening and extension penalties (Gotoh); `false` one flat penalty per gap column. |
| `gap_penalty` | number |  | `-10` |  | the flat penalty per gap column. Negative. Only applies when affine_gap is false. |
| `gap_open` | number |  | `-12` |  | affine only: the penalty for starting a gap. Negative. Only applies when affine_gap is true. |
| `gap_extend` | number |  | `-2` |  | affine only: the penalty for each column a gap is extended by. Negative. Only applies when affine_gap is true. |
| `terminal_penalty` | boolean |  | `true` |  | global only: `true` charges overhanging ends like an internal gap; `false` makes them free. Only applies when mode is global. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the method, the score and where the aligned stretch lies in each input |
| `alignedSequences` | any |  | the two aligned rows, {name, aligned}, over the aligned stretch |
| `score` | number |  | the alignment score under the matrix and gap penalties |
| `spans` | any |  | 1-based first and last residue of each input inside the aligned stretch |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "align_pair",
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

### align_read

**Align read**: _How does one sequencing read align to the reference, as two gapped rows?_

Pairwise-align ONE sequencing read against a reference and hand on the two gapped rows, so the read can be graded. Needleman-Wunsch with free end gaps and the IUPAC substitution matrix — SeqTrace's aligner, the same call the trace editor makes, so a pipeline and the panel align a read identically. Leave `reference` unset to align against the record this step runs on.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Needleman-Wunsch with free end gaps and the IUPAC substitution matrix is the right model for a read against its reference.

**Does not:**
- One read at a time; a read from elsewhere in the genome still aligns somewhere.

**Not read from this result:** An intermediate step: two gapped rows handed to verify_read, which grades them and carries the Verify panel's reading. The panel never shows an alignment ungraded.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `read` | string | **yes** |  |  | the read's bases — wire a trace reader's `sequence` output here, or paste them. |
| `reference` | string |  |  |  | what to align against. Unset, it is the record this step runs on (the open plasmid, or an upstream product wired into the subject). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `alignedRead` | string |  | the read with gaps inserted — wire into `verify_read.aligned_read` |
| `alignedReference` | string |  | the reference with gaps inserted — wire into `verify_read.aligned_ref` |
| `referenceLength` | number | bp | the reference's ungapped length in bp — wire into `verify_read.target_len` |
| `identity` | number | % | % identity over the columns where both rows have a base (gaps excluded) |
| `mismatches` | number |  | columns where the two rows carry different bases |
| `columns` | number |  | the alignment's width, gaps included |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "align_read",
  "arguments": {
    "read": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### align_sequences

**Align sequences**: _How do these sequences line up column by column, by partial-order alignment (a pile of reads over one locus) or progressive alignment (a family of homologous genes)?_

Multiple-sequence alignment over several sequences, under either of TWO engines that answer different questions and neither of which is a fallback for the other. `poa` (partial-order, poapy) aligns into a graph, keeps every path a read took and produces its own consensus row — what a pile of reads over one locus wants. `progressive` (biotite) computes Feng-Doolittle distances, clusters them into a guide tree and merges along it under "once a gap, always a gap" — the classic MSA algorithm, what a FAMILY of homologous genes wants, and what a reader coming from Clustal or MUSCLE expects. Wire many upstream `record`/`sequence` outputs into `sequences`, or name library documents.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The sequences are homologous over the region aligned.
- Progressive: once a gap, always a gap; the guide tree follows Feng-Doolittle distances.

**Does not:**
- An alignment is one hypothesis of homology; the fit block flags rows held out of register.
- The guide tree carries no branch lengths and is not a phylogeny.

**Validated:** against the reference implementation by 5 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] |  |  |  | the sequences to align — wire several upstream outputs here, or list library document names/ids. |
| `include_subject` | boolean |  | `true` |  | also align the node's subject (the open or wired record). |
| `engine` | `"poa"` · `"progressive"` |  | `"poa"` |  | which aligner builds the alignment. They answer DIFFERENT questions: `poa` keeps every path through a pile of reads and emits its own consensus row, `progressive` merges a family along a guide tree the way Clustal and MUSCLE do. Each engine reads only its own parameters below. Values: poa (Partial-order (poapy) - reads over one locus), progressive (Progressive (biotite) - a family, guide-tree merged). |
| `global_align` | boolean |  | `true` |  | global alignment rather than local. Poapy's own default is LOCAL; both this tool and the MSA inspector open on global, which is the choice a full-length comparison wants - switch it off for reads over part of a locus. Only applies when engine is poa. Advanced. |
| `match` | number |  | `1` |  | `poa` only: score for a pair of identical symbols. Only applies when engine is poa. Advanced. |
| `mismatch` | number |  | `-1` |  | `poa` only: score for a mismatching pair. Negative. Only applies when engine is poa. Advanced. |
| `gap` | number |  | `-2` |  | `poa` only: score for a gap column. Negative. Only applies when engine is poa. Advanced. |
| `align_matrix` | `"auto"` · `"EDNAFULL"` · `"BLOSUM62"` |  | `"auto"` |  | `progressive` only: the substitution matrix the ALIGNMENT itself is scored with - distinct from `score_matrix`, which only scores the quality report afterwards. `auto` reads the alphabet: EDNAFULL for nucleotides, BLOSUM62 for protein. Naming the wrong one is not an error the engine can raise - BLOSUM62 reads A, C, G and T as alanine, cysteine, glycine and threonine and returns a number. Values: auto (Auto - from the alignment's alphabet), EDNAFULL (EDNAFULL - nucleotides (EMBOSS NUC.4.4)), BLOSUM62 (BLOSUM62 - amino acids). Only applies when engine is progressive. |
| `guide_tree` | `"upgma"` · `"nj"` · `"bionj"` · `"wpgma"` |  | `"upgma"` |  | `progressive` only: which tree the merge follows. The Feng-Doolittle distances are the aligner's either way; this chooses only how they are clustered into an order. UPGMA is biotite's own and the one the port reproduces byte-for-byte; neighbour-joining and BIONJ do not assume a molecular clock, so on sequences evolving at different rates they group by relatedness where UPGMA groups by raw similarity - which is exactly the case where the guide tree changes the alignment. Values: upgma (UPGMA (biotite's own)), nj (Neighbour-joining), bionj (BIONJ), wpgma (WPGMA). Only applies when engine is progressive. |
| `affine_gap` | boolean |  | `false` |  | `progressive` only: `false` charges one flat penalty per gap column; `true` charges separate opening and extension penalties, which is what keeps a real indel as ONE gap instead of many. Only applies when engine is progressive. |
| `gap_penalty` | number |  | `-10` |  | `progressive` only: the flat penalty per gap column. Negative. Only applies when affine_gap is false. |
| `gap_open` | number |  | `-12` |  | `progressive`, affine only: the penalty for STARTING a gap. Negative. Only applies when affine_gap is true. |
| `gap_extend` | number |  | `-2` |  | `progressive`, affine only: the penalty for each column a gap is extended by. Negative, and gentler than `gap_open` - an extension harsher than the opening makes the aligner prefer many short gaps to one long indel. Only applies when affine_gap is true. |
| `terminal_penalty` | boolean |  | `true` |  | `progressive` only: `true` charges overhanging ends like an internal gap - right for full-length homologues. `false` makes them free, which is right when a sequence covers only part of the region, e.g. a read against a gene. Only applies when engine is progressive. |
| `score_matrix` | `"PAM250"` · `"BLOSUM62"` · `"EDNAFULL"` |  |  |  | substitution matrix for the pyMSA sum-of-pairs and star scores in the quality report. Both engines. Left unset only the matrix-free scores are computed (entropy, % non-gaps, % totally conserved columns) - an honest absence rather than a score under a matrix that does not match the alphabet. Values: PAM250 (PAM250 - amino acids, greater evolutionary distance), BLOSUM62 (BLOSUM62 - amino acids), EDNAFULL (EDNAFULL - nucleotides). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rows` | any |  | aligned rows (name + gapped sequence) |
| `length` | number |  | alignment width in columns |
| `count` | number |  | number of aligned sequences (excluding the consensus row) |
| `consensus` | string |  | the per-column majority consensus (POA returns its own graph consensus row; the progressive engine has no graph, so the majority is the consensus for both) |
| `alignedSequences` | any[] |  | the aligned input rows only, excluding the generated consensus — wire this into build_tree |
| `conservation` | string |  | the Clustal-style conservation line, one character per column — `*` where every row carries the same residue and the column is ungapped |
| `engine` | string |  | which aligner produced this alignment — `poa` or `progressive` |
| `scores` | any |  | the pyMSA quality scores: summed entropy (nats, pyMSA's sign — negative), % non-gaps, % totally conserved columns, and the sum-of-pairs/star pair when a `score_matrix` was named |
| `guideTreeNewick` | string |  | `progressive` only: the guide tree the merge followed, in Newick, labelled with the row names. Branch lengths are deliberately omitted — a guide tree's heights are a clustering artifact, not divergence estimates |
| `figure` | string or null |  | the alignment's first 80 columns drawn as the MSA canvas opens on them: rows named, residues shaded by column identity, the conservation line under the block. draw_alignment draws any other window |
| `fit` | any |  | per row: its closest row in this alignment, their identity here, and the same pair's identity aligned on its own with free end gaps (biotite align_optimal) — the loss shows where the alignment holds a row out of register; `outliers` names the rows flagged. `{ ok: false, reason }` when the check could not run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "align_sequences",
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

### alignment_agreement

**Alignment agreement**: _How well do the reads in this window agree with the reference beneath them?_

Read an alignment window and say how well its reads agree with the reference underneath them, the way the pileup's own bar does: the compared and differing base counts, plus the RefSeq gene models and known dbSNP variants over the same window. The reference is a FASTA in this project or a public UCSC assembly, exactly as the panel offers it. There is no threshold and no verdict: a rate in the tens of percent almost always means the reads were aligned to a different assembly than the one asked for, and when the file declares its own reference length the answer says so as a fact rather than as a judgement.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The reference is the FASTA or UCSC assembly named.

**Does not:**
- No threshold and no verdict; gene models and dbSNP need the network.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `alignment` | string |  |  |  | which BAM or SAM in this project, by name. Unset, it is the project's only alignment — and it refuses rather than guessing when there is more than one. |
| `reference` | string |  |  |  | what to compare against: a FASTA in this project by name, or a UCSC assembly id (`hg38`, `hg19`, `mm39` — the same list the panel's picker fetches). Unset is the panel's own default, No reference, and then only the window and its annotation are reported. |
| `locus` | string |  |  |  | the window, as a locus string (`chrM:3,300-3,460`). Unset, it is the whole of the alignment's first reference — the window the panel opens on. |
| `gene_track` | `"ncbiRefSeqSelect"` · `"ncbiRefSeqCurated"` · `"ncbiRefSeq"` · `"ncbiRefSeqPredicted"` |  | `"ncbiRefSeqSelect"` |  | which NCBI RefSeq set the gene models come from. Only meaningful against a UCSC assembly. The default is one curated transcript per protein-coding gene, which carries no mitochondrial genes at all — RefSeq Curated does. Values: ncbiRefSeqSelect (RefSeq Select and MANE), ncbiRefSeqCurated (RefSeq Curated), ncbiRefSeq (RefSeq All), ncbiRefSeqPredicted (RefSeq Predicted). |
| `variants` | boolean |  | `false` |  | also report the known dbSNP variants in the window. Off by default, as in the panel: it is a third layer over the reads and a dense window can hold thousands. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `conclusion` | string |  | the reading in one sentence, generated from this run — the panel's own words |
| `cautions` | any |  | what this run earned: a reference whose length disagrees with the one the file declares, no-call bases counted as neither, and the window the numbers describe |
| `rate` | number |  | differing aligned bases as a fraction of compared ones, 0 when nothing matched up |
| `compared` | number |  | aligned bases that had a reference base to compare against — the denominator |
| `mismatched` | number |  | of those, how many differ |
| `noCall` | number |  | aligned bases where one side is N — counted as neither, which is where this differs from an aligner's NM |
| `reads` | number |  | reads read for the window |
| `window` | string |  | the window actually measured, as a locus string |
| `genes` | any |  | the RefSeq models overlapping the window: symbol, accession, strand and bounds, as UCSC states them |
| `variants` | any |  | the dbSNP records in the window when asked for: rsID, alleles, class, highest reported frequency and ClinVar significance |
| `pathogenic` | number |  | how many of those ClinVar calls pathogenic |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "alignment_agreement",
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

### alignment_pca

**Alignment PCA**: _How do the rows of this alignment group, on the principal axes of their pairwise similarity?_

Principal component analysis of the rows of an alignment: the pairwise similarity of every two rows under PID or a substitution matrix (BLOSUM62, PAM250 for protein; Jalview's DNA matrix for nucleotides), decomposed into eigenvectors, and each row's coordinate on the leading components, so rows that cluster sit together. Jalview's PCA, with its parameters: gap–gap and gap–residue columns counted, a gap never matching. Needs 4 rows. Wire `alignedSequences` from align_sequences.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The rows are aligned; similarity is summed column by column under the chosen model.

**Does not:**
- The similarity matrix is not centred, so the first axis often tracks overall similarity rather than a split.
- An eigenvalue near zero makes its coordinates huge and meaningless; the eigenvalues are reported so they can be read.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `rows` | object[] | **yes** |  |  | the ALIGNED rows, each {name, aligned}. Wire `alignedSequences` from align_sequences. |
| `model` | `"PID"` · `"BLOSUM62"` · `"PAM250"` · `"DNA"` |  | `"PID"` |  | the similarity model: PID for any alphabet, BLOSUM62 or PAM250 for protein, DNA for nucleotides. Values: PID (Percent identity), BLOSUM62 (BLOSUM62), PAM250 (PAM250), DNA (DNA). |
| `components` | number |  | `3` | 1–10 | how many leading components to report per row. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the model, the leading eigenvalues and their share of the total |
| `coordinates` | any |  | each row's coordinates on the leading components, {name, pc: [PC1, PC2, …]} |
| `eigenvalues` | any |  | every eigenvalue, largest first |
| `similarity` | any[] |  | the pairwise similarity matrix the analysis decomposed, rows in alignment order |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "alignment_pca",
  "arguments": {
    "rows": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### alignment_redundancy

**Alignment redundancy**: _Which rows of this alignment are near-copies of a longer row, at what identity?_

Find the rows of an alignment that repeat another: each row's redundancy is its highest percent identity to a row at least as long (ungapped residues), and a row at or above the threshold is redundant, so filtering keeps the longest representative of each near-identical group. Jalview's definition: a gap matches anything and the pair is compared over the shorter row. Wire `alignedSequences` from align_sequences.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The rows are aligned; identity is read column by column.

**Does not:**
- A gap counts as matching anything, so two rows that differ only where one has gaps are 100% identical.
- Of a near-identical pair only the shorter row is charged, so a cluster keeps its longest member.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `rows` | object[] | **yes** |  |  | the ALIGNED rows, each {name, aligned}. Wire `alignedSequences` from align_sequences. |
| `threshold` | number |  | `100` | 0–100 | percent identity at or above which a row is redundant. In %. |
| `from` | number |  | `1` | ≥ 1 | first column compared, 1-based inclusive. Advanced. |
| `to` | number |  | `0` | ≥ 0 | last column compared, 1-based inclusive; 0 means the last column. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many rows are redundant at the threshold, and which |
| `redundant` | any |  | the redundant rows, each {name, identity}, most redundant first |
| `kept` | any |  | the names of the rows that survive the filter, in alignment order |
| `rows` | any |  | every row's redundancy, {name, identity}, in alignment order |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "alignment_redundancy",
  "arguments": {
    "rows": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### alignment_window

**Alignment window**: _Which reads, what depth and what pairing does this window of the BAM or SAM hold?_

Read one window of a BAM or SAM in this project: its reads, the depth across it, and what the pairs say about the library — the same window, filters and record cap the pileup draws. Wire `reads` into an alignment or a screen the way the pane's own hand-offs do.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The filters and record cap given.

**Does not:**
- Capped at the record limit; reads beyond it are counted, not returned.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `alignment` | string |  |  |  | which BAM or SAM in this project, by name. Unset, it is the project's only alignment — and it refuses rather than guessing when there is more than one. |
| `locus` | string |  |  |  | the window, as a locus string (`ctgA:1-50,001`). Unset, it is the whole of the alignment's first reference — the window the panel opens on. |
| `min_mapq` | number |  | `0` | 0–255 | hide reads below this mapping quality, as the pane’s Filter reads operation does. The reads are still counted — `hidden` says how many this removed. |
| `hide_secondary` | boolean |  | `false` |  | drop secondary alignments (FLAG 0x100). |
| `hide_supplementary` | boolean |  | `false` |  | drop supplementary alignments (FLAG 0x800). |
| `hide_duplicates` | boolean |  | `false` |  | drop reads marked as PCR or optical duplicates (FLAG 0x400). |
| `max_reads` | number |  | `3000` | 1–20000 | the record cap. More reads than this overlap the window and the result is an even SAMPLE of them, with `sampled` saying so — the pane’s own cap is the default. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `reads` | any |  | the reads in the window after filters: name, reference, 1-based start and end, strand, MAPQ, CIGAR, TLEN and sequence — the shape an alignment or a screen takes |
| `read_count` | number |  | how many reads that is |
| `hidden` | number |  | reads in the window the filters removed — 0 with an active filter is a real answer |
| `sampled` | boolean |  | more reads overlap the window than the cap allows, so `reads` is an even sample rather than all of them |
| `window` | string |  | the window actually read, as a locus string |
| `depth_mean` | number |  | mean depth across the window’s coverage bins, over ALL reads — the coverage track is full-depth, as BamView’s is, so filters do not move it |
| `depth_max` | number |  | the deepest bin |
| `coverage` | any |  | the depth profile as bins across the window, in order |
| `depthPlot` | object or null |  | the coverage track as the pileup draws it: each bin's lowest, mean and highest per-base depth over ALL reads, so a dropout narrower than a bin still shows in the minimum |
| `depthPlot.x` | number[] |  |  |
| `depthPlot.series` | object[] |  |  |
| `depthPlot.series[].name` | string |  |  |
| `depthPlot.series[].y` | (number or null)[] |  |  |
| `depthPlot.xLabel` | string |  |  |
| `depthPlot.yLabel` | string |  |  |
| `depthPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `depthPlot.title` | string |  |  |
| `depthPlot.rules` | object[] |  |  |
| `depthPlot.rules[].y` | number |  |  |
| `depthPlot.rules[].label` | string |  |  |
| `insert_size` | any |  | the \|TLEN\| band this library’s own proper pairs define — `min`, `max` and whether it was MEASURED here or is the untuned fallback, which is what decides whether an insert is abnormal |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "alignment_window",
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

### build_tree

**Build tree**: _What phylogeny do these aligned sequences support, under a distance, parsimony, maximum-likelihood or Bayesian method, with branch support?_

Build a phylogeny from aligned sequences — distance methods (NJ, BIONJ, FastME, UPGMA/WPGMA), parsimony, maximum likelihood, or Bayesian MCMC under a strict clock and coalescent prior — with branch support from a bootstrap, aLRT or aBayes, or, for the Bayesian method, clade posterior probabilities. Wire it downstream of align_sequences.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The alignment is correct; the substitution model and rate heterogeneity are as chosen.
- Bayesian runs assume a strict clock and the coalescent prior stated.

**Does not:**
- A tree is an estimate: support values say how well the data pin each clade, and a bootstrap is not a probability of truth.
- Heuristic topology search: a better tree may exist.

**Validated:** against the reference implementation by 7 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] |  |  |  | aligned sequences — wire align_sequences' rows here, or name library documents. |
| `include_subject` | boolean |  | `false` |  | also include the node's subject. |
| `method` | `"nj"` · `"bionj"` · `"fastme-bal"` · `"fastme-ols"` · `"upgma"` · `"wpgma"` · `"parsimony"` · `"ml"` · `"bayesian"` |  | `"nj"` |  | tree-building method; distance methods are fast, ML is the slowest and best-justified. Values: nj (Neighbor-Joining), bionj (BIONJ), fastme-bal (FastME (balanced)), fastme-ols (FastME (OLS)), upgma (UPGMA), wpgma (WPGMA), parsimony (Maximum Parsimony), ml (Maximum Likelihood), bayesian (Bayesian (MCMC)). |
| `model` | `"raw"` · `"N"` · `"TS"` · `"TV"` · `"JC69"` · `"K80"` · `"F81"` · `"K81"` · `"F84"` · `"T92"` · `"TN93"` · `"logdet"` · `"indel"` · `"indelblock"` |  | `"K80"` |  | distance/substitution model (ape's names). K80 is the engine's default; very divergent sequences need raw or JC69. |
| `pairwise_deletion` | boolean |  | `false` |  | exclude a gapped site only from the pairs it is missing in, rather than from every pair. ape's default is off (complete deletion), which keeps distances mutually comparable but discards a column if ANY sequence has a gap there — turn this on for gappy alignments. |
| `gamma` | number |  | `0` | 0–10 | gamma shape for among-site rate variation in the DISTANCE correction; 0 disables. Not the ML +Γ, which is `ml_gamma_categories`. Advanced. |
| `support_method` | `"bootstrap"` · `"alrt"` · `"abayes"` · `"shalrt"` |  | `"bootstrap"` |  | which branch support to attach. `bootstrap` resamples alignment columns and rebuilds the tree per replicate (uses `bootstrap`/`bootstrap_seed`). The three branch tests re-infer nothing: they score each internal branch against its two nearest-neighbour rearrangements under the ML model, three likelihood evaluations per branch instead of N whole re-inferences. `alrt` is the parametric test of Anisimova & Gascuel (2006), read against a mixture-of-chi-squares null, and it saturates at 99.985%. `abayes` is the Bayesian support of Anisimova et al. (2011). `shalrt` is the Shimodaira-Hasegawa-corrected variant (PhyML `-b -4`): the same three fits, but the gap is read against a null built by RELL-resampling their per-site log-likelihoods `sh_replicates` times from `bootstrap_seed` — slower than the other two, does not saturate, and usually more conservative. All three use `ml_model`/`ml_gamma_categories`/`ml_shape`/`ml_invariant` for the model, whichever `method` built the tree. Values: bootstrap (Bootstrap), alrt (aLRT), abayes (aBayes), shalrt (SH-aLRT). |
| `bootstrap` | number |  | `100` | 0–1000 | bootstrap replicates; 0 disables. Each replicate rebuilds the whole tree, so cost scales with it — 100 is the conventional minimum for a published tree and is the panel's default. Only applies when support_method is bootstrap. |
| `bootstrap_measure` | `"fbp"` · `"tbe"` |  | `"fbp"` |  | which bootstrap statistic to report. `fbp` is Felsenstein's proportion: the share of replicates that carry this exact branch: a yes/no question per replicate, so one taxon landing elsewhere makes the answer no, which is why a well-supported clade can read near zero on a large tree. `tbe` is the transfer bootstrap expectation (Lemoine et al. 2018, Nature 556:452-456): 1 minus the average number of taxa that would have to move to turn a replicate's nearest branch into this one, over the branch's depth. TBE reads higher than FBP on the same replicates and the two are NOT interchangeable, so say which one a number is. Both read the SAME replicates, so `tbe` costs no extra inference. Only applies when support_method is bootstrap. |
| `bootstrap_seed` | number |  | `1` | ≥ 0 | seed for whichever resampling this run does — the bootstrap's replicates, or SH-aLRT's. The same seed always reproduces the same support values. Only applies when support_method is bootstrap or shalrt. Advanced. |
| `sh_replicates` | number |  | `10000` | 1–1000000 | RELL replicates behind `shalrt` — resamples the three fits' per-site log-likelihoods, not the alignment, so a replicate costs microseconds rather than a whole re-inference. PhyML uses 10,000. Ignored unless `support_method` is `shalrt`. Only applies when support_method is shalrt. Advanced. |
| `parsimony_rearrangement` | `"nni"` · `"spr"` · `"tbr"` |  | `"nni"` |  | parsimony topology search: `nni` hill-climbs by nearest-neighbour interchange, `spr` adds prune-and-regraft when NNI stalls (phangorn's own default), `tbr` adds bisect-and-reconnect when SPR stalls. Nested, not alternatives: each runs the cheaper moves first, because every NNI move is an SPR move and every SPR move is a TBR move. `tbr` searches the largest neighbourhood this tool offers — 1,950 distinct topologies against SPR's 814 on an 18-taxon tree — and rescores each candidate whole, where SPR scores incrementally, so it is markedly the slowest. Values: nni (Nearest-neighbour interchange), spr (Subtree prune-and-regraft), tbr (Tree bisection and reconnection). Only applies when method is parsimony. Advanced. |
| `fastme_nni` | boolean |  | `true` |  | FastME refinement by nearest-neighbour interchange (ape's `nni = TRUE`). Only applies when method is fastme-bal or fastme-ols. Advanced. |
| `fastme_spr` | boolean |  | `true` |  | FastME balanced refinement by subtree prune-and-regraft (ape's `spr = TRUE`). Only applies when method is fastme-bal. Advanced. |
| `ml_model` | `"JC69"` · `"F81"` · `"K80"` · `"HKY"` · `"TN93"` · `"GTR"` |  | `"GTR"` |  | ML substitution model. Values: JC69 (JC69), F81 (F81), K80 (K80), HKY (HKY), TN93 (TN93), GTR (GTR). Only applies when method is ml, or when support_method is alrt or abayes or shalrt. Advanced. |
| `ml_gamma_categories` | number |  | `1` | 1–8 | discrete-Γ rate categories for the rate heterogeneity across sites; 1 disables it. Only applies when method is ml, or when support_method is alrt or abayes or shalrt. Advanced. |
| `ml_shape` | number |  | `1` | ≥ 0.02 | α of the discrete-Γ distribution over site rates — lower means more rate variation between sites. The starting value when the shape is estimated, and the fixed value when it is not. Inert while `ml_gamma_categories` is 1, because one category has no spread. Only applies when method is ml, or when support_method is alrt or abayes or shalrt. Advanced. |
| `ml_invariant` | number |  | `0` | 0–0.99 | proportion of sites that never change; 0 disables. The starting value when it is estimated. Only applies when method is ml, or when support_method is alrt or abayes or shalrt. Advanced. |
| `ml_optimise_topology` | boolean |  | `true` |  | let the ML search move the topology. With this off the result is the Neighbor-Joining topology with ML branch lengths, and the engine says so in a warning. Only applies when method is ml. Advanced. |
| `ml_rearrangement` | `"nni"` · `"spr"` · `"tbr"` |  | `"nni"` |  | topology search moves for the ML fit. `nni` moves one subtree past its neighbour and stops at the first topology no single move improves, which is a local optimum. `spr` runs that first and then sweeps prune-and-regraft, which reaches trees NNI cannot — at a quadratic number of rearrangements per sweep rather than a linear one. `tbr` runs both and then sweeps tree bisection and reconnection, which cuts a branch and rejoins the two halves by any pair of their branches: the largest neighbourhood here, measured at 1,950 distinct topologies against SPR's 814 on an 18-taxon tree, so roughly 2.4x an SPR sweep. Ignored unless `method` is `ml` and `ml_optimise_topology` is on. Values: nni (NNI), spr (NNI, then SPR), tbr (NNI, then SPR, then TBR). Only applies when method is ml. Advanced. |
| `ml_optimise_rates` | boolean |  | `true` |  | fit the substitution rates rather than holding the model's own. Only applies when method is ml. Advanced. |
| `ml_optimise_base_frequencies` | boolean |  | `true` |  | fit base frequencies rather than holding them equal. Only applies when method is ml. Advanced. |
| `ml_optimise_shape` | boolean |  | `false` |  | fit the discrete-Γ shape rather than holding `ml_shape`. Costs a degree of freedom in AIC/BIC, and does nothing while `ml_gamma_categories` is 1. Only applies when method is ml. Advanced. |
| `ml_optimise_invariant` | boolean |  | `false` |  | fit the proportion of invariant sites rather than holding `ml_invariant`. Costs a degree of freedom in AIC/BIC. Only applies when method is ml. Advanced. |
| `bayesian_model` | `"JC69"` · `"F81"` · `"K80"` · `"HKY"` |  | `"JC69"` |  | substitution model for the Bayesian chain, its parameters held fixed for the run: base frequencies are the alignment's own for F81/HKY, and kappa is `bayesian_kappa` for K80/HKY. Values: JC69 (JC69), F81 (F81), K80 (K80), HKY (HKY). Only applies when method is bayesian. |
| `bayesian_kappa` | number |  | `2` | ≥ 0.01 | transition/transversion ratio for K80/HKY, held fixed. Only applies when method is bayesian. |
| `bayesian_iterations` | number |  | `20000` | ≥ 1000 | Metropolis-Hastings proposals. Each rescores the alignment, so time grows with iterations x taxa x site patterns. Only applies when method is bayesian. |
| `bayesian_burn_in` | number |  | `5000` | ≥ 0 | iterations discarded from the start. Only applies when method is bayesian. |
| `bayesian_sample_frequency` | number |  | `100` | ≥ 1 | keep one tree every this many iterations after burn-in. Only applies when method is bayesian. Advanced. |
| `bayesian_gamma_categories` | number |  | `1` | 1–16 | discrete-Gamma categories for among-site rate variation (+G, each category its bin mean); 1 is equal rates. Only applies when method is bayesian. |
| `bayesian_shape` | number |  | `1` | ≥ 0.01 | Gamma shape (alpha) for +G, held fixed for the run; smaller means more rate variation among sites. Only applies when method is bayesian. |
| `bayesian_sample_shape` | boolean |  | `false` |  | sample the Gamma shape under MrBayes' Exponential(1) prior instead of holding it at bayesian_shape (which becomes the start); needs bayesian_gamma_categories > 1. Only applies when method is bayesian. |
| `bayesian_sample_kappa` | boolean |  | `false` |  | sample kappa (K80/HKY) under MrBayes' Beta(1,1) prior on kappa/(1+kappa), starting from bayesian_kappa. Only applies when method is bayesian. |
| `bayesian_sample_frequencies` | boolean |  | `false` |  | sample the base frequencies (F81/HKY) under a flat Dirichlet, starting from the alignment's own. Only applies when method is bayesian. |
| `bayesian_clock` | `"strict"` · `"ucln"` · `"none"` |  | `"strict"` |  | clock model: strict (one rate on every branch), ucln, the uncorrelated lognormal relaxed clock (each branch its own rate, mean 1, log-scale sd sampled under Exponential(mean 1/3), as BEAST's UCRelaxedClockModel), or none: an unrooted tree with free branch lengths under an Exponential prior and no coalescent (MrBayes' unconstrained model). Only applies when method is bayesian. |
| `bayesian_clock_sd` | number |  | `0.1` | ≥ 0.001 | where the relaxed clock's sigma (log-scale sd of branch rates) starts; always sampled. Only applies when bayesian_clock is ucln. Advanced. |
| `bayesian_brlen_rate` | number |  | `10` | ≥ 0.01 | with no clock: rate of the Exponential prior on each branch length (MrBayes brlenspr=unconstrained:exp(rate)); 10 means a prior mean of 0.1 substitutions per site. Only applies when bayesian_clock is none. Advanced. |
| `bayesian_chains` | number |  | `1` | 1–8 | Metropolis-coupled chains per run (MrBayes nchains; its default is 4): the extra chains sample a flattened posterior and swap states with the cold one, so a run can cross valleys a single chain cannot. Each chain costs a full chain's time. Only applies when method is bayesian. |
| `bayesian_temp` | number |  | `0.1` | ≥ 0.001 | heating increment (MrBayes temp): chain j samples the posterior raised to 1/(1 + temp*j). Only applies when method is bayesian. Advanced. |
| `bayesian_runs` | number |  | `1` | 1–8 | independent runs (MrBayes nruns), seeded seed, seed+1, ...; 2 or more pools their samples and reports the average standard deviation of split frequencies and the PSRF. Only applies when method is bayesian. |
| `bayesian_min_part_freq` | number |  | `0.1` | 0–1 | a clade enters the split-frequency deviation only if some run sampled it at least this share of the time (MrBayes minpartfreq). Only applies when method is bayesian. Advanced. |
| `bayesian_seed` | number |  | `1` | ≥ 0 | seed of the chain; the same seed and settings reproduce the same samples. Only applies when method is bayesian. Advanced. |
| `bayesian_theta_prior_mean` | number |  | `0.036` | ≥ 0.0001 | mean of the Gamma prior on theta = 4N mu, in substitutions per site. Only applies when method is bayesian. Advanced. |
| `bayesian_theta_shape` | number |  | `2` | ≥ 0.1 | shape of the Gamma prior on theta. Only applies when method is bayesian. Advanced. |
| `bayesian_theta_start` | number |  | `0.02` | ≥ 0.0001 | starting theta of the chain (not a prior). Only applies when method is bayesian. Advanced. |
| `midpoint_root` | boolean |  | `false` |  | root the result at its midpoint — a drawing convention, not evidence about where the true root is. Advanced. |
| `ladderize` | boolean |  | `true` |  | order each node's children by clade size, so the drawing reads as a ladder. Changes the Newick's child order and nothing about the topology. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `newick` | string |  | the tree in Newick format |
| `tipCount` | number |  | number of tips (leaves) |
| `statistics` | any |  | tree statistics: tips, height, total length, diameter, the branch-length distribution, Colless/Sackin imbalance, cherries, treeness, the Pybus-Harvey gamma with its two-tailed P, and the ultrametricity readouts gamma depends on (`isUltrametric`, `rootToTipSpread`, `clockDeviationInBranches`) |
| `gamma` | number or null |  | the Pybus-Harvey gamma statistic: negative if branching clusters toward the root (an early burst), positive if toward the tips. A standard normal deviate under the constant-rate null — read it with `gammaP`, and only if `clockDeviationInBranches` is below 1 |
| `gammaP` | number or null |  | two-tailed P for `gamma` against the constant-rate (pure-birth) null |
| `clockDeviationInBranches` | number or null |  | how far from clock-like the tree is, in MEAN BRANCH LENGTHS. `gamma` and any lineages-through-time reading assume an ultrametric tree; below 1 the raggedness cannot reorder a branching event, above it the statistic is partly rate variation and is not a diversification result |
| `distanceMatrix` | any |  | the pairwise distance matrix the tree was built from |
| `distanceMap` | object or null |  | that distance matrix as a heatmap |
| `distanceMap.rows` | string[] |  |  |
| `distanceMap.cols` | string[] |  |  |
| `distanceMap.values` | ((number or null)[])[] |  |  |
| `distanceMap.label` | string |  |  |
| `distanceMap.title` | string |  |  |
| `transfer` | any |  | under `support_method: bootstrap` with `bootstrap_measure: tbe`: per branch, its clade (the smaller side), its depth, the mean transfer distance over the replicates and the support on 0..1. Absent under `fbp`, which puts its values on the tree and nowhere else |
| `branchSupport` | any |  | under `alrt`/`abayes`: the measure, the model, the tree's log-likelihood, and per branch its clade, the two alternative log-likelihoods, the statistic and the support (a fraction, not a percentage). Absent under `bootstrap` |
| `bayesian` | any |  | under `method: bayesian`: the chain (iterations, burn-in, samples, seed, acceptance per operator), the fixed model, the priors, mean / 95% HPD / ESS of log L, theta and root height, every clade's posterior probability (0..1), the commonest topologies and the highest-posterior state. Absent under every other method |
| `warnings` | any |  | what the method had to say about the data |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "build_tree",
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

### compare_trees

**Compare trees**: _How far apart are these trees over the same taxa, and what topology do they share?_

Compare trees over the same taxa: the Robinson-Foulds distance between two of them, and the consensus of any number. Two methods disagreeing is a result about the data, so the distance and the shared topology are reported together.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The trees cover the same taxon set.

**Does not:**
- Robinson-Foulds counts clade differences; it does not weigh them by branch length or support.
- Two methods disagreeing is a result about the data, so the distance and the consensus are reported together.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `trees` | string[] | **yes** |  |  | two or more trees in Newick (NEXUS, PhyloXML and NeXML pastes are sniffed too) — wire `newick` outputs here. |
| `mode` | `"majority"` · `"strict"` |  | `"majority"` |  | how strict the consensus is: strict keeps only clades in EVERY tree; majority keeps those above the cutoff. Values: majority (Majority-rule), strict (Strict). |
| `cutoff` | number |  | `0.5` | 0.5–1 | the fraction of trees a clade must appear in for a majority consensus. Only applies when mode is majority. |
| `sharedTaxaOnly` | boolean |  | `false` |  | prune every tree to the taxa they ALL share before comparing, instead of refusing a mismatch. The numbers then describe the pruned trees, and pruning can only remove or merge splits, so the distance is a lower bound on the disagreement between the trees as given. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `consensus` | string |  | the consensus tree, in Newick |
| `rf` | number |  | Robinson-Foulds distance between the first two trees (absent for one tree) |
| `normalized` | number |  | the same distance as a fraction of its maximum, 0 = identical topology, 1 = share nothing |
| `distances` | any |  | every distance the comparison computes, not just RF |
| `treeCount` | number |  | how many trees went into the consensus |
| `comparedTaxa` | number |  | how many taxa the distances were computed over — under `sharedTaxaOnly` this is the shared set, which is smaller than either tree |
| `prunedTaxa` | any |  | under `sharedTaxaOnly`: the labels dropped from each tree, so a comparison over a smaller set can never be read as one over the whole |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "compare_trees",
  "arguments": {
    "trees": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### discover_gene_tree_discordance

**Discover gene tree discordance**: _Which genes' own alignments reject the species tree (Shimodaira-Hasegawa test against its nearest-neighbour rearrangements)?_

Find the genes whose own alignment rejects the species tree. Each named alignment file is one gene, its records the taxa, named as the species tree's tips. For every gene the species tree and each of its nearest-neighbour rearrangements (two per internal branch) is fitted by maximum likelihood under GTR + Γ (rates, base frequencies and shape fitted on the species tree, branch lengths refitted on each rearrangement), and the Shimodaira–Hasegawa test asks whether the species tree is significantly worse than the best of them; the false discovery rate is controlled across genes. A rejection says the gene fits another tree better: incomplete lineage sorting does that to a share of genes among closely spaced species, and so do hidden paralogy, alignment error and transfer, so it is a gene to read, never a call of any one of them. Also reports which genes' best tree is not the species tree, rejected or not, and which alternative trees they choose. Graded against phangorn's pml, optim.pml and SH.test on 122 great-ape genes. About a second of fitting per gene in a browser.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- GTR + Γ fits each gene well enough for likelihoods to compare trees.
- Tips are named as the species tree's tips.

**Does not:**
- A rejection says another tree fits better; incomplete lineage sorting, hidden paralogy, alignment error and transfer all do that, so it is a gene to read, never a call of one of them.
- Only nearest-neighbour rearrangements of the species tree are tested.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `alignments` | string[] | **yes** |  |  | the gene alignments: library file names, each an aligned multi-FASTA with one record per taxon, the record names being the species tree's tips. |
| `species_tree` | string | **yes** |  |  | the species tree in Newick, tips named as the alignments' records. Rooted or not; it is tested unrooted. |
| `alpha` | number |  | `0.05` | 0.0001–0.5 | false discovery rate at which a gene counts as rejecting the species tree. |
| `correction` | `"BH"` · `"BY"` |  | `"BH"` |  | Benjamini–Hochberg (independent or positively dependent tests) or Benjamini–Yekutieli (any dependence; less power). Values: BH (Benjamini–Hochberg), BY (Benjamini–Yekutieli). |
| `replicates` | number |  | `1000` | 100–100000 | RELL bootstrap replicates of the SH test. The smallest nonzero p is 1 / replicates; a p of 0 means no replicate reached the observed difference, which evidence reads as 1 / (replicates + 1). |
| `sh_form` | `"published"` · `"phangorn"` |  | `"published"` |  | how each replicate is measured: from its best tree, as Shimodaira and Hasegawa (1999) and Goldman et al. (2000) define the test, or from its worst, as phangorn's SH.test computes it. They agree when the replicates are symmetric. Values: published (Published (from the best tree)), phangorn (phangorn (from the worst tree)). Advanced. |
| `gamma_categories` | number |  | `4` | 1–8 | discrete Gamma rate categories; 1 fits no rate variation among sites. Advanced. |
| `seed` | number |  | `1` | ≥ 0 | seed for the bootstrap. Each gene draws from seed + its own index, so a gene's p does not depend on the rest of the corpus. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rejected` | number |  | genes whose alignment rejects the species tree at the chosen false discovery rate |
| `discordant` | number |  | genes whose best tree is not the species tree, rejected or not |
| `genes` | any |  | every gene: sites, each candidate tree's log-likelihood and SH p, the species tree's p and q |
| `alternatives` | any |  | each alternative tree some gene prefers, with how many prefer it and how many of those reject the species tree |
| `sweep` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_gene_tree_discordance",
  "arguments": {
    "alignments": [],
    "species_tree": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### discover_tree_incongruence

**Discover tree incongruence**: _Do some loci of a multi-locus alignment have a different history from the rest (incongruence length difference test)?_

Ask whether some loci of a multi-locus alignment have a different history from the rest, by the incongruence length difference test (Farris et al. 1994). Each locus is one aligned FASTA file (or a set of wired alignment rows) over the same taxa, named alike in every file. D is the extra parsimony steps one shared tree costs over each locus's own tree; the null deals the same columns into parts of the same sizes at random. One global test over every locus, and one per locus against all the others combined, with the false discovery rate controlled across loci. A locus that recombined or was transferred costs steps when forced onto the others' tree, but so does a locus evolving at a different rate (Darlu & Lecointre 2002), so a call is a candidate for a tree comparison, never a recombination call. Lengths are NNI parsimony searches from each alignment's own neighbour-joining tree. Cost: a run is 1 + k + k·n + k·(1 + 2n) searches for k loci and n permutations, and a search grows fast with taxa: the default 99 permutations over seven Neisseria MLST loci took 23 s on 12 strains, 48 s on 16 and 122 s on 20, and one search of the 62-strain concatenation takes about 8 s, so 62 strains is hours. Each file is one locus; records wired with no file are grouped by the part of their name before ` · `.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- Every alignment covers the same taxa, named alike.
- Parsimony tree lengths from NNI searches stand for the best trees.

**Does not:**
- A locus evolving at a different rate also fails the test, so a call is a candidate for a tree comparison, never a recombination call.
- Cost grows fast with taxa: tens of strains are minutes, sixty are hours.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `loci` | string[] | **yes** |  |  | the loci: one aligned FASTA file per locus (its records are the taxa), or library document names. Every file must name the same taxa. |
| `permutations` | number |  | `99` | 9–999 | random deals of the columns per test. The smallest p is 1 / (permutations + 1), which bounds how small a corrected q can get. |
| `alpha` | number |  | `0.05` | 0.0001–0.5 | false discovery rate at which a locus is called. |
| `correction` | `"BH"` · `"BY"` |  | `"BH"` |  | Benjamini–Hochberg (independent or positively dependent tests) or Benjamini–Yekutieli (any dependence; less power). Values: BH (Benjamini–Hochberg), BY (Benjamini–Yekutieli). |
| `seed` | number |  | `1` | ≥ 0 | seed for the column deals. Each permutation draws from its own stream, so one can be re-run alone. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `loci` | any |  | per locus: its length, the rest's, D, the permutations' mean D, p, q and whether it is called |
| `called` | any |  | the loci called at q ≤ alpha |
| `global` | any |  | the test over every locus at once: D, its null, p |
| `nullModel` | string |  | the null and the search, stated with every run |
| `result` | any |  | the full result |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "discover_tree_incongruence",
  "arguments": {
    "loci": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### dot_plot

**Dot plot**: _Where does this sequence resemble itself or another, as a dot plot of repeats, inversions and shared regions?_

Self-similarity or pairwise comparison of the subject as a dot plot — repeats, inversions and shared regions. Three real engines: exact k-mer (FlexiDot/dottup), windowed identity (seqinr) and windowed substitution-matrix scoring (EMBOSS dotmatcher), which answer different questions.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The engine chosen matches the question: exact k-mers, windowed identity, or windowed matrix score.

**Does not:**
- The three engines answer different questions and their scores are not comparable.
- A dot plot shows similarity; it does not call homology.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `other` | string |  |  |  | the sequence to compare against — wire a record or name a library document; leave unset for self-vs-self. |
| `engine` | `"word"` · `"window"` · `"matrix"` |  | `"word"` |  | exact k-mer (blind to diverged repeats) · windowed identity · matrix-scored windows (the only one that grades a substitution). Values: word (Exact k-mer (dottup)), window (Windowed identity (seqinr)), matrix (Substitution matrix (dotmatcher)). |
| `word_size` | number |  |  | 3–200 | k for the k-mer engine, or the window length for the other two. In bp. |
| `reverse_complement` | boolean |  | `true` |  | also plot matches against the reverse complement (k-mer engine). Only applies when engine is word. |
| `best_path_only` | boolean |  | `false` |  | reduce forward segments to a non-overlapping best path (EMBOSS dotpath). Only applies when engine is word. Advanced. |
| `threshold` | number |  | `23` | 0–200 | score a window must reach (EMBOSS default 23). Only applies when engine is matrix. Advanced. |
| `nucleotide` | boolean |  | `true` |  | nucleotide rather than protein. Advanced. |
| `step` | number |  | `1` | 1–100 | residues between window starts (seqinr `wstep`). 1 compares every position. Only applies when engine is window. Advanced. |
| `min_matches` | number |  | `1` | 1–200 | positions inside the window that must agree for it to be marked (seqinr `nmatch`). At 1 almost every window qualifies; raise it toward the window length to demand real identity. Only applies when engine is window. |
| `shift` | number |  | `0` | 0–100 | phase offset applied to the second sequence's windows (seqinr `shift`). Only applies when engine is window. Advanced. |
| `max_cells` | number |  | `40000000` | ≥ 1000 | refuse rather than compute past this many window comparisons. A ceiling, not a target: raise it for a large pair. Only applies when engine is window. Advanced. |
| `matrix` | `"EDNAFULL"` · `"EBLOSUM62"` |  |  |  | which substitution matrix scores the windows. Unset picks EDNAFULL for nucleotide and EBLOSUM62 for protein, as EMBOSS dotmatcher does. Values: EDNAFULL (EDNAFULL (nucleotide)), EBLOSUM62 (EBLOSUM62 (protein)). Only applies when engine is matrix. Advanced. |
| `matrix_text` | string |  |  |  | a custom scoring matrix in EMBOSS/NCBI format, overriding `matrix`. Only applies when engine is matrix. Advanced. |
| `dedupe` | boolean |  | `false` |  | drop the duplicate runs dotmatcher's two passes leave on the shared diagonal. Off matches upstream; a caller that COUNTS runs wants it on. Only applies when engine is matrix. Advanced. |
| `convert_wobbles` | boolean |  | `false` |  | expand IUPAC ambiguity codes so a wobble matches what it stands for (FlexiDot). Only applies when engine is word. Advanced. |
| `max_unknown_percent` | number |  | `0` | 0–100 | percentage of a k-mer allowed to be N (or X for protein) before it is skipped. In %. Only applies when engine is word. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `stats` | any |  | longest runs, run counts and per-sequence coverage |
| `longestForward` | number |  | residues on the longest uninterrupted forward run |
| `coverage` | number |  | fraction of the subject covered by at least one forward match (0–1) |
| `plot` | any |  | the full result — segments or points, plus axis lengths |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "dot_plot",
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

### dot_plot_grid

**Dot plot grid**: _Which members of this sequence set share material with which, as an all-against-all grid of dot plots?_

All-against-all dot plot over a sequence SET — EMBOSS `polydot`. Every ordered pair is plotted with the exact k-mer engine and laid out as an N×N grid, so shared regions, repeats and inversions across a whole family are visible in one picture. Answers a different question from `dot_plot`, which compares exactly two: this one ranks which members share material and how much. Wire many upstream record/sequence outputs into `sequences`, or name library documents.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Exact k-mer matching, as EMBOSS polydot does it.

**Does not:**
- Ranks which pairs share material; it is not an alignment or a tree.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] | **yes** |  |  | the set to compare all against all — wire several upstream outputs here, or list library document names/ids. |
| `include_subject` | boolean |  | `true` |  | also include the node's subject (the open or wired record) as a member of the set. |
| `word_size` | number |  | `6` | 3–200 | k. EMBOSS polydot's default is 6, which is smaller than dottup's because a grid of short panels needs a shorter word to show anything. In bp. |
| `reverse_complement` | boolean |  | `true` |  | plot each pair against the reverse complement too. Not an EMBOSS capability — ours, so an inversion between two members is visible. |
| `best_path_only` | boolean |  | `false` |  | reduce each panel's forward runs to a non-overlapping best path (EMBOSS dotpath). Advanced. |
| `convert_wobbles` | boolean |  | `false` |  | expand IUPAC ambiguity codes so a wobble matches what it stands for. Advanced. |
| `max_unknown_percent` | number |  | `0` | 0–100 | percentage of a k-mer allowed to be N (or X for protein) before it is skipped. In %. Advanced. |
| `nucleotide` | boolean |  | `true` |  | nucleotide rather than protein. Advanced. |
| `gap` | number |  | `10` | 0–1000 | residues of blank space drawn between panels in the composite layout (EMBOSS default 10). Advanced. |
| `max_sequences` | number |  | `12` | 2–200 | refuse a set larger than this rather than starting N² comparisons. Advanced. |
| `max_residues` | number |  | `500000` | ≥ 1000 | refuse when the set's total residue count exceeds this. In bp. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | any |  | EMBOSS's per-sequence table — name, length, and the matches drawn in that sequence's whole column |
| `sequences` | any |  | the set as plotted, in grid order, with each member's length |
| `memberCount` | number |  | members in the set (the grid is this squared) |
| `sharingPairs` | number |  | off-diagonal panels carrying at least one shared word — how connected the set is, the leading diagonal excluded because a member always matches itself |
| `grid` | any |  | the full result — every panel's runs plus its offset in the composite coordinate space |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "dot_plot_grid",
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

### draw_alignment

**Draw alignment**: _What does this window of an alignment look like as a figure?_

Draw a block of an alignment as an SVG figure: the rows named, the residues shaded by how much of their column agrees with them, the column numbers over the block and Easel's Clustal conservation line under it. Wire `alignedSequences` from align_sequences. Name the window around whatever you are asking about — a variable site, a motif, a gap — because a 2,000-column alignment drawn at once shows nothing.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Draws a window, not the alignment; the identity it reports is the window's.

**No scientific claim:** Draws an alignment someone else computed; the shading and conservation line are read from it, not inferred.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `rows` | object[] | **yes** |  |  | the ALIGNED rows, each {name, aligned}; every row must already be the same length. Wire `alignedSequences` from align_sequences. |
| `from` | number |  | `1` | ≥ 1 | first column drawn, 1-based and inclusive. Clamped into the alignment. |
| `columns` | number |  | `80` | 5–400 | how many columns to draw. Past about 200 the letters are narrower than the strokes that make them. |
| `scheme` | `"identity"` · `"nucleotide"` |  | `"identity"` |  | identity shades a residue by how much of its column agrees with it, which works for any alphabet; nucleotide paints QUEEN's own base colours and is IGNORED over protein rows, which the answer's `scheme` then says. Values: identity (Column identity), nucleotide (Base colours). |
| `cell_width` | number |  | `11` | 4–40 | width of one column's cell. In px. Advanced. |
| `row_height` | number |  | `15` | 6–48 | height of one row. In px. Advanced. |
| `name_chars` | number |  | `14` | 4–60 | how many characters of a row's name to print; a longer one is elided in the middle, keeping the tail where two rows of a family differ. Advanced. |
| `conservation` | boolean |  | `true` |  | print the conservation line under the block. |
| `ruler` | boolean |  | `true` |  | print the column numbers over the block. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `svg` | string or null |  | the alignment block as an SVG figure |
| `width` | number | px | figure width in px |
| `height` | number | px | figure height in px |
| `rows` | number |  | rows drawn |
| `firstColumn` | number |  | first column drawn, 1-based inclusive, AFTER clamping |
| `lastColumn` | number |  | last column drawn, 1-based inclusive |
| `columns` | number |  | columns in the WHOLE alignment, so the window can be read against it |
| `meanIdentity` | number |  | mean per-column identity over the window drawn, 0-1 — the window's, not the alignment's |
| `conservedColumns` | number |  | columns in the window every row agrees on and none gaps — the `*` marks |
| `scheme` | string |  | the scheme ACTUALLY used, which is `identity` whenever `nucleotide` was asked for over protein rows |
| `alphabet` | string |  | the alphabet the conservation line was computed for — Easel marks the strong and weak groups for protein only |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "draw_alignment",
  "arguments": {
    "rows": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### draw_tree

**Draw tree**: _What does this tree look like as a figure?_

Draw a tree as an SVG figure — rectangular, slanted, circular or unrooted, as a phylogram or a cladogram, with tip names, branch support and a scale bar. The same layout the phylogeny panel draws with, so the figure and the panel place every node identically. Wire `newick` from build_tree or edit_tree.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Draws the tree given; it estimates nothing.

**No scientific claim:** Lays out a tree someone else inferred, with the same layout the panel uses.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `newick` | string | **yes** |  |  | the tree to draw — wire `newick` from build_tree, or paste one. |
| `layout` | `"rectangular"` · `"slanted"` · `"circular"` · `"unrooted"` |  | `"rectangular"` |  | drawing style; `unrooted` is the only honest one for a tree whose method inferred no root, because a rectangular drawing of it implies a root that was never inferred. Values: rectangular (Rectangular), slanted (Slanted), circular (Circular), unrooted (Unrooted). |
| `width` | number |  | `640` | 200–4000 | figure width. In px. |
| `height` | number |  | `480` | 200–4000 | figure height. In px. |
| `branch_lengths` | boolean |  | `true` |  | phylogram: horizontal distance IS evolutionary distance. Off draws a cladogram, which shows the topology alone — and then no scale bar is drawn, because the drawing is not to scale. |
| `tip_labels` | boolean |  | `true` |  | print each tip's name, reserving the gutter they need. |
| `support` | boolean |  | `false` |  | print each internal branch's support value where it carries one. |
| `min_support` | number |  | `50` | 0–100 | below this, a support value is not printed. Only applies when support is true. Advanced. |
| `font_size` | number |  | `11` | 6–32 | tip-label size. In px. Advanced. |
| `unrooted_method` | `"equal-angle"` · `"equal-daylight"` |  | `"equal-angle"` |  | which unrooted algorithm places the nodes; equal daylight only rotates subtrees about their nodes, so it preserves every branch length. Only applies when layout is unrooted. Advanced. |
| `length_unit` | string |  | `"substitutions/site"` |  | what the branch lengths MEAN, for the scale bar's caption. A tree read from a file carries no unit, so say what it is rather than letting the bar claim substitutions/site. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `svg` | string or null |  | the figure as an SVG string |
| `width` | number | px | figure width in px |
| `height` | number | px | figure height in px |
| `tipCount` | number |  | tips drawn |
| `pixelsPerUnit` | number |  | px per unit of branch length in THIS drawing, or 0 when the drawing is not to scale and no bar was drawn |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "draw_tree",
  "arguments": {
    "newick": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### ebi_align

**EBI align**: _What does the EMBL-EBI reference tool named return for these sequences?_

Run a sequence through EMBL-EBI's Job Dispatcher: Clustal Omega, MUSCLE, MAFFT, Kalign, T-Coffee, EMBOSS needle/water/matcher/stretcher, LALIGN, phmmer, hmmscan, PSI-BLAST or Phobius. These are the reference implementations a methods section names, so a local alignment can be checked against the tool the field actually cites. The sequences LEAVE THE MACHINE.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network; the sequences leave the machine.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `service` | `"clustalo"` · `"muscle"` · `"mafft"` · `"kalign"` · `"tcoffee"` · `"emboss_needle"` · `"emboss_water"` · `"emboss_matcher"` · `"emboss_stretcher"` · `"lalign"` · `"hmmer3_phmmer"` · `"hmmer3_hmmscan"` · `"psiblast"` · `"phobius"` · `"radar"` · `"pratt"` |  | `"clustalo"` |  | which EBI service to run. Values: clustalo (Clustal Omega — HMM-profile progressive MSA), muscle (MUSCLE — Iterative refinement MSA), mafft (MAFFT — FFT-based progressive/iterative MSA), kalign (Kalign — Wu-Manber approximate-string-matching MSA), tcoffee (T-Coffee — Consistency-based MSA), emboss_needle (EMBOSS needle — Needleman–Wunsch GLOBAL pairwise alignment: end-to-end, the whole of both sequences.), emboss_water (EMBOSS water — Smith–Waterman LOCAL pairwise alignment: the best-matching subregion, ignoring the rest.), emboss_matcher (EMBOSS matcher — Waterman–Eggert local pairwise alignment, like water, but it can report several alternative non-overlapping local alignments instead of only the single best one.), emboss_stretcher (EMBOSS stretcher — Myers–Miller GLOBAL pairwise alignment in linear space: the same answer needle gives, on sequence pairs too long for needle to hold in memory.), lalign (LALIGN — Huang & Miller), hmmer3_phmmer (HMMER phmmer — Profile HMM search of one protein against a protein database), hmmer3_hmmscan (HMMER hmmscan — Search ONE protein against a profile-HMM library), psiblast (PSI-BLAST — Position-Specific Iterated BLAST: it builds a profile from the hits of one round and searches again with it, which finds remote homologues plain blastp misses.), phobius (Phobius — Combined signal-peptide and transmembrane-topology prediction: the two are modeled together, so a signal peptide is not miscalled as a TM helix.), radar (RADAR — Rapid Automatic Detection and Alignment of Repeats: finds a protein’s INTERNAL repeats and aligns the copies against each other, without a library to match them to.), pratt (Pratt — Pattern discovery). |
| `sequences` | string[] |  |  |  | the sequences to align. Wire records or sequence outputs, or paste FASTA. Multiple-alignment services take all of them; a pairwise service takes exactly two. |
| `include_subject` | boolean |  | `true` |  | include the record this step is running on as the first sequence. |
| `stype` | `"dna"` · `"protein"` |  | `"dna"` |  | query alphabet, where the service takes one. Values: dna (nucleotide), protein (protein). |
| `parameters` | string |  |  |  | every other parameter the chosen service advertises, one `id=value` per line, using its own ids (matrix, gapopen, gapext, format, iterations…). Left empty each keeps the service's default. An id the service does not advertise is refused by name rather than dropped, and so is a value outside the list it publishes for this alphabet. |
| `email` | string |  |  |  | EBI requires a contact address on every submission (their abuse contact, not a login). Left empty, the one saved in any EMBL-EBI panel is used. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `alignment` | any |  | the aligned sequences (multiple-alignment services) |
| `rows` | any |  | the aligned rows as plain strings, ready to wire into build_tree or a scorer |
| `newick` | string |  | the service's own guide tree, ready for the Phylogenetics tool |
| `identity` | any |  | the percent-identity matrix the service computed |
| `pairwise` | any |  | the pairwise report (needle/water/matcher/stretcher) |
| `local` | any |  | LALIGN’s non-overlapping local alignments, each with its own score, E-value and spans |
| `profileHits` | any |  | the HMMER hits (phmmer, hmmscan) with their domains and inclusion thresholds |
| `topology` | any |  | the Phobius signal-peptide and transmembrane features, with their spans |
| `hits` | any |  | the PSI-BLAST hit table, in the same shape blast_search hands downstream |
| `repeats` | any |  | RADAR’s internal repeat families, each copy with its residue span and its two scores |
| `patterns` | any |  | Pratt’s discovered patterns in PROSITE notation, each with where it matched in every sequence |
| `jobId` | string |  | the dispatcher job id: what a methods section cites and what re-fetches this exact result |
| `raw` | string |  | the native text the service returned, for download |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "ebi_align",
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

### export_tree

**Export tree**: _What does this tree look like in Newick, NEXUS, PhyloXML or NeXML?_

Convert a tree between the four formats this workbench reads and writes — Newick, NEXUS, PhyloXML and NeXML — sniffing the input format rather than making the caller declare it. Newick loses annotations the richer formats carry, which is why the conversion is a step you choose rather than something done silently on export.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Newick loses annotations the richer formats carry, which is why the conversion is a step you choose.

**Not read from this result:** A format conversion: the same tree written in another format, with nothing inferred.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `tree` | string | **yes** |  |  | the tree, in any of the four formats. |
| `format` | `"newick"` · `"nexus"` · `"phyloxml"` · `"nexml"` |  | `"newick"` |  | the format to write. Values: newick (Newick), nexus (NEXUS), phyloxml (PhyloXML), nexml (NeXML). |
| `name` | string |  | `"tree1"` |  | the tree's name inside the written file (NEXUS and NeXML carry one). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `text` | string |  | the tree written in the requested format |
| `sourceFormat` | string |  | the format the input was sniffed as — check this when a conversion surprises you |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "export_tree",
  "arguments": {
    "tree": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### select_substitution_model

**Select substitution model**: _Which substitution model do these data prefer, by AIC, AICc or BIC with Akaike weights?_

Choose the substitution model for a maximum-likelihood phylogeny by fitting every candidate — model x rate-heterogeneity x invariant-sites — on ONE shared topology and ranking them by AIC, AICc or BIC with Akaike weights. Fitting on a shared topology is the point: a model test that also searched topologies would vary two things at once, and a log-likelihood measured on a different tree answers a different question. Wire the winning model into build_tree's `ml_model`.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Every candidate is fitted on ONE shared topology, so only the model varies.

**Does not:**
- A ranking among the candidates fitted, not a claim that the best one is adequate.
- A log-likelihood measured on a different topology answers a different question and is not comparable.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequences` | string[] | **yes** |  |  | aligned sequences — wire align_sequences' rows here, or name library documents. |
| `include_subject` | boolean |  | `false` |  | also include the node's subject. |
| `models` | (`"JC69"` · `"F81"` · `"K80"` · `"HKY"` · `"TN93"` · `"GTR"`)[] |  | `["JC69", "F81", "K80", "HKY", "TN93", "GTR"]` |  | candidate substitution models. Every one is fitted; the sweep costs one ML optimisation per candidate. |
| `gamma_categories` | number[] |  | `[1, 4]` |  | discrete-Γ category counts to try. `[1]` is no rate heterogeneity; `[1, 4]` is the usual sweep and is the panel's default. |
| `include_invariant` | boolean |  | `true` |  | also try each model with a proportion of invariant sites (+I), doubling the candidate count. |
| `criterion` | `"AIC"` · `"AICc"` · `"BIC"` |  | `"AIC"` |  | which information criterion ranks the table. Changing it re-ranks candidates that are already fitted — it does not re-fit them. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `best` | string |  | the winning model in the conventional shorthand (e.g. `GTR+G4+I`) |
| `weight` | number |  | the winner's Akaike weight — the share of the evidence it carries. A low weight means the data do not choose between the top models, which is a finding and not a failure |
| `fits` | any |  | every candidate with its log-likelihood, free parameters, AIC/AICc/BIC and Akaike weight |
| `candidates` | number |  | how many candidates were fitted |
| `startingTree` | string |  | the ONE topology every candidate was fitted on, in Newick — reported because it is a shared assumption of the whole table |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "select_substitution_model",
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

### transform_tree

**Transform tree**: _What does this tree look like re-rooted, pruned, ladderized, or with weak branches collapsed?_

Edit a tree that is already built — re-root it (at its midpoint, on an outgroup, or remove the root), prune taxa away or down to a set, ladderize it, or collapse branches that are too weakly supported or too short to believe. Pruning the TREE keeps the branch lengths estimated from the full alignment, which is a different answer from rebuilding without those taxa.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The input tree's branch lengths were estimated from the full alignment, and pruning keeps them.

**Does not:**
- Pruning the tree is not rebuilding without those taxa; the two give different answers.
- Collapsing by support discards a topology the data weakly preferred.

**Not read from this result:** A re-rooted, pruned, ladderised or collapsed tree is an edit of the input, returned whole; there is no estimate to read.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `newick` | string | **yes** |  |  | the tree to edit — wire `newick` from build_tree, or paste one. |
| `operation` | `"reroot-midpoint"` · `"reroot-outgroup"` · `"unroot"` · `"prune-keep"` · `"prune-remove"` · `"ladderize"` · `"collapse"` |  | `"reroot-midpoint"` |  | what to do to the tree. Values: reroot-midpoint (Re-root at the midpoint), reroot-outgroup (Re-root on an outgroup), unroot (Remove the root (unroot)), prune-keep (Prune down to these taxa), prune-remove (Prune these taxa away), ladderize (Ladderize (presentation only)), collapse (Collapse weak or short branches). |
| `taxa` | string[] |  |  |  | tip labels — the outgroup for a re-root, or the taxa to keep/remove for a prune. Only applies when operation is reroot-outgroup or prune-keep or prune-remove. |
| `position` | number |  | `0` | 0–1 | where along the outgroup edge the root lands, 0 = at the outgroup, 1 = at its sister. Only applies when operation is reroot-outgroup. Advanced. |
| `min_support` | number |  | `0` | 0–100 | contract any branch whose support is below this (0 = do not). Only applies when operation is collapse. |
| `max_length` | number |  | `0` | 0–1 | collapse any branch shorter than this (0 = do not). Only applies when operation is collapse. |
| `ascending` | boolean |  | `true` |  | ladderize small clades first, rather than large. Only applies when operation is ladderize. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `newick` | string |  | the edited tree |
| `tipCount` | number |  | tips remaining — the number to check after a prune |
| `statistics` | any |  | statistics RE-DERIVED for the edited tree, because rerooting or pruning changes them and the previous numbers beside a changed tree would be wrong. Absent for `ladderize`, which only reorders tips and changes no statistic |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "transform_tree",
  "arguments": {
    "newick": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### tree_statistics

**Tree statistics**: _What shape does this tree have: tips, height, balance, the gamma statistic, lineages through time, and the patristic distances?_

Describe a tree without rebuilding it: its shape statistics (tips, height, balance, the gamma statistic), the lineages-through-time curve, and the patristic distance matrix — the path lengths through the tree, which is what to compare against the alignment distances that built it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The branch lengths are in the units the tree was built in.

**Does not:**
- Describes the tree as given; a shape statistic on a poorly supported tree describes the estimate, not the clade's history.
- The gamma statistic assumes a complete, ultrametric tree.

**Not read from this result:** The answer is the tree's measurements (tip and node counts, height, the lineage-through-time curve, patristic distances), which the outputs carry; the Stats tab shows them as readouts and writes no reading over them.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `newick` | string | **yes** |  |  | the tree to describe — wire `newick` from build_tree, or paste one. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `statistics` | any |  | tips, height, balance and the gamma statistic (with the reason when gamma is undefined for this tree) |
| `ltt` | any |  | lineages-through-time: the points of the curve and the coalescence times behind it |
| `patristic` | any |  | labels and the matrix of path lengths between every pair of tips |
| `lttPlot` | object or null |  | the lineages-through-time curve as a plot |
| `lttPlot.x` | number[] |  |  |
| `lttPlot.series` | object[] |  |  |
| `lttPlot.series[].name` | string |  |  |
| `lttPlot.series[].y` | (number or null)[] |  |  |
| `lttPlot.xLabel` | string |  |  |
| `lttPlot.yLabel` | string |  |  |
| `lttPlot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `lttPlot.title` | string |  |  |
| `lttPlot.rules` | object[] |  |  |
| `lttPlot.rules[].y` | number |  |  |
| `lttPlot.rules[].label` | string |  |  |
| `patristicMap` | object or null |  | the patristic distances as a heatmap |
| `patristicMap.rows` | string[] |  |  |
| `patristicMap.cols` | string[] |  |  |
| `patristicMap.values` | ((number or null)[])[] |  |  |
| `patristicMap.label` | string |  |  |
| `patristicMap.title` | string |  |  |
| `tipCount` | number |  | number of tips |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "tree_statistics",
  "arguments": {
    "newick": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
