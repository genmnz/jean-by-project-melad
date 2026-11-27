# 📈 Sanger, sequencing & verification

_Trace reading, base calling, construct verification, read QC and alignment to a reference._

18 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`adopt_trace_calls`](#adopt_trace_calls) | Replace the open read's calls with TraceTuner's. |
| [`call_bases_from_trace`](#call_bases_from_trace) | What bases does the signal call, independent of the instrument's calls? |
| [`call_mixed_bases_from_trace`](#call_mixed_bases_from_trace) | Where does a second allele sit under the primary call? |
| [`compare_reads_to_reference`](#compare_reads_to_reference) | Where do this set of reads, aligned in one frame, differ from the reference, and what does each change do to the protein? |
| [`consensus_from_traces`](#consensus_from_traces) | What is the consensus of these one or two reads? |
| [`demultiplex_reads`](#demultiplex_reads) | Which index did each read come from, and how many cannot be assigned reliably? |
| [`draw_trace`](#draw_trace) | Draw this window of the read as a figure. |
| [`fastq_qc`](#fastq_qc) | Is this FASTQ run fit to use, module by module, the way a FastQC report would grade it? |
| [`map_reads`](#map_reads) | Where on the reference does each read or contig align, with what MAPQ, as SAM? |
| [`read_sequencing_qc`](#read_sequencing_qc) | Is a disappointing read the clone's fault or the run's, from the provider's coverage table or summary? |
| [`read_structure_consensus`](#read_structure_consensus) | Which base pairs does a Stockholm alignment's consensus structure state, and how many aligned rows actually form each one? |
| [`recompute_trace_quality`](#recompute_trace_quality) | What Phred quality does each of this trace's calls earn, measured from its peaks? |
| [`restore_trace_file_calls`](#restore_trace_file_calls) | Put the open read back on its file's own calls. |
| [`trace_raw_signal`](#trace_raw_signal) | What did the instrument record before processing: scans, baselines and peak values per channel? |
| [`trim_reads`](#trim_reads) | What do these FASTQ reads look like after the adapters and low-quality ends are trimmed, and how much was removed? |
| [`trim_trace`](#trim_trace) | Where should this read's low-quality ends be cut, by the method named? |
| [`verify_construct`](#verify_construct) | Where does the sequencing result differ from the designed construct, and what does each difference land in? |
| [`verify_read`](#verify_read) | Does a sequencing read verify the reference, and which differences does it show? |

---

### adopt_trace_calls

**Adopt trace calls**: _Replace the open read's calls with TraceTuner's._

Replace a Sanger read's own base calls with TraceTuner's, on the trace that is open, so the rest of the editor works from the re-called read: its sequence, its consensus, its verification against a reference, and every export. The signal is untouched — this is the same electropherogram with a second opinion about where the bases are — and every coordinate already on the read is carried across the peaks it sits on, so a trim window, a hand-corrected call and an annotation all follow. Reports what moved and what could not be placed. Use `call_bases_from_trace` instead to ASK what the re-call says without changing the read.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- TraceTuner's calls under the table and mode given.

**Does not:**
- Writes to the open read; restore_trace_file_calls undoes it.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `mode` | `"rescore"` · `"denovo"` · `"het"` · `"mix"` |  | `"rescore"` |  | which reading to adopt. `rescore` keeps the instrument's bases and only re-measures their confidence; `denovo` derives the bases from the signal and can return a different read LENGTH; `het` and `mix` derive them and write a two-base IUB code where a second allele is present, differing only in whether the two are assumed equal in amount. |
| `table` | `"3700pop5"` · `"3700pop6"` · `"3100pop6"` · `"3730pop7"` |  | `"3730pop7"` |  | the instrument and polymer the quality scale was calibrated on. There is no universal default: a base scores differently under a different table. |
| `min_ratio` | number |  | `0.1` | 0.05–0.9 | for `het` and `mix` only: how tall a second peak must be, as a fraction of the called one, to be called as a second allele. Ignored by the other two modes. Only applies when mode is het or mix. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `bases` | number |  | how many bases the read carries after the adoption |
| `basesBefore` | number |  | how many it carried before it, so a gate can see the read change length |
| `sequence` | string |  | the read the document now carries, trimmed and with manual calls applied |
| `everythingPlaced` | boolean |  | false when any annotation end sat on a call the new reading does not make, so it was placed at its nearest neighbor. Wire it into a gate before trusting a boundary |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "adopt_trace_calls",
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

### call_bases_from_trace

**Call bases from trace**: _What bases does the signal call, independent of the instrument's calls?_

Call the bases of a Sanger trace from the signal, discarding the instrument's calls and deriving the bases, their positions and their quality from the peaks. The read can come back a DIFFERENT LENGTH than the file's. This ANSWERS the question; `adopt_trace_calls` is what puts the answer onto the read.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- TraceTuner's base caller and the calibration table named.

**Not read from this result:** The answer is the called read itself (bases, positions, Phred), which the outputs carry; the Recompute quality section shows it as a track to adopt and writes its reading only on adoption, which adopt_trace_calls returns.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace to run on: a file name (`read_F.ab1`) or its project file id. Leave unset to use the trace tab on screen. A file id is project-specific, so a template ships this unset. |
| `table` | `"3700pop5"` · `"3700pop6"` · `"3100pop6"` · `"3730pop7"` |  | `"3730pop7"` |  | the instrument/polymer calibration table to score against. The same signal scores differently under each, so a quality value is only interpretable with the table named. Defaults to ABI 3730 POP-7. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `bases` | number |  | how many bases the reading called |
| `instrumentBases` | number |  | how many the FILE carries, so a gate can see a de-novo reading change the read's length |
| `meanQuality` | number |  | the mean Phred of the reading, on the calibration table it names |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "call_bases_from_trace",
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

### call_mixed_bases_from_trace

**Call mixed bases from trace**: _Where does a second allele sit under the primary call?_

Call the bases of a Sanger trace AND ask at every position whether a second allele is present, writing a two-base IUB code (R, Y, S, W, K, M) where it is. `mode: het` assumes the two alleles are present in equal amounts, which is the diploid heterozygote case; `mode: mix` assumes nothing about their ratio, for a mixed template, a contaminated read or a pooled sample. The two disagree: on this repo's own corpus they differ on 348 of 5,605 calls. Also returns the ALTERNATIVE calls the search considered and rejected.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- TraceTuner's mixed-base caller at the ratio given.

**Not read from this result:** The answer is the called read and its mixed positions, which the outputs carry; the Recompute quality section shows them as a track to adopt and writes its reading only on adoption, which adopt_trace_calls returns.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace to run on: a file name (`read_F.ab1`) or its project file id. Leave unset to use the trace tab on screen. A file id is project-specific, so a template ships this unset. |
| `table` | `"3700pop5"` · `"3700pop6"` · `"3100pop6"` · `"3730pop7"` |  | `"3730pop7"` |  | the instrument/polymer calibration table to score against. The same signal scores differently under each, so a quality value is only interpretable with the table named. Defaults to ABI 3730 POP-7. |
| `mode` | `"het"` · `"mix"` |  | `"het"` |  | het = the two alleles are assumed present 1:1 (a diploid heterozygote); mix = no assumption is made about their ratio. |
| `min_ratio` | number |  | `0.1` | 0–1 | how tall a second peak must be, as a fraction of the called peak, before the search will consider it as a second allele. Lowering it widens what is considered, which is not the same as calling more mixed bases. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `bases` | number |  | how many bases the reading called |
| `instrumentBases` | number |  | how many the FILE carries, so a gate can see a de-novo reading change the read's length |
| `meanQuality` | number |  | the mean Phred of the reading, on the calibration table it names |
| `mixedBases` | number |  | how many positions were called as carrying two alleles. Reported as 0 rather than omitted when none were, because a missing field is not an answer |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "call_mixed_bases_from_trace",
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

### compare_reads_to_reference

**Compare reads to reference**: _Where do this set of reads, aligned in one frame, differ from the reference, and what does each change do to the protein?_

Compare a SET of sequencing reads against one reference in ONE shared frame: align every read to the reference, vote a consensus column by column, and report the positions where the reads differ from it, each with the change it makes to the protein. This is the whole-plate answer that grading reads one at a time cannot give — a variant is accepted only when every covering read agrees, so a single bad call does not become a mutation. Reads arrive as records or bases; the reference is the record this step runs on.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- A variant is accepted only when every covering read agrees.
- The genetic code named.

**Does not:**
- Reads that do not align are reported, not forced; indels in low-quality ends are trimmed by the filter given.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `reads` | string[] |  |  |  | the reads to compare — wire a batch of trace RECORDS in (their names come with them, and the per-read table is keyed by name), wire plain sequences, or name project documents. |
| `quality_filter` | boolean |  | `false` |  | mask low-quality bases before the vote. Off by default, deliberately: a comparison shows what the FILES say before it shows what a filter says. |
| `min_phred` | number |  | `20` | 0–60 | mask any single base below this phred score. Only applies when quality_filter is true. |
| `end_phred` | number |  | `20` | 0–60 | end trimming: the read becomes readable where three consecutive bases reach this score, and everything outside is masked. A Sanger read is unreliable at both ends by construction, which is why the ends are trimmed by RUN rather than per base. Only applies when quality_filter is true. |
| `genetic_code` | number |  | `1` | 1–33 | NCBI genetic-code table id, used to say what a variant does to the protein of a CDS on the reference. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `consensus` | string |  | the voted consensus as a sequence, gaps and unresolved insertions removed — the sequence to hand on |
| `alignmentFigure` | string or null |  | the reference and every read in the shared frame, 80 columns around the first ACCEPTED change (else the first difference, else the start), shaded by column identity; draw_alignment draws any other window of `alignedReads` |
| `variants` | any |  | one row per column where a read differs from the reference: its position, the reference base, the voted base, whether the vote ACCEPTED it, the coverage behind it and the consequence for the protein |
| `accepted` | number |  | how many of those the vote accepted — every covering read agreed |
| `coveragePct` | number | % | how much of the reference any read covers at all |
| `identityPct` | number | % | of the covered columns, how many match the reference |
| `perRead` | any |  | each read's own coverage, identity and substitution / deletion / insertion counts, plus how often it disagrees with the accepted consensus — the row that says WHICH read is the problem |
| `gaps` | any |  | stretches of the reference no read covers, as 1-based inclusive runs. A clean comparison over 60% of a construct is not a verified construct, and this is the half that says so |
| `conclusion` | string |  | the run's headline in one sentence, generated from THIS result and identical to the words the panel shows |
| `cautions` | any |  | every caution this comparison raises, each naming its own subject: uncovered stretches, reads that reach across only part of the frame, reads that dissent from the accepted consensus, insertions the reads could not resolve, mixed peaks |
| `derivation` | any |  | the chain behind the numbers: what identity was measured over (and that an indel does not lower it), the unanimity rule, how one frame came out of N pairwise alignments, the quality gate, the genetic code and the inputs |
| `record` | object |  | the consensus as a linear record, ready for any downstream step |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "compare_reads_to_reference",
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

### consensus_from_traces

**Consensus from traces**: _What is the consensus of these one or two reads?_

Merge one or two Sanger reads into a consensus with the validated SeqTrace caller. With two reads (typically a forward and a reverse of the same amplicon) an IUPAC ambiguity code marks a position the two DISAGREE about; with one read there is nothing to disagree with and a code marks a position where no single base cleared the confidence bar. Returns the consensus, how many positions are ambiguous, and how many the consensus's own trimming stage cut from the ends.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The consensus algorithm and confidence threshold named.

**Does not:**
- At most two reads.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | the first read: its name or its project file id. |
| `second_document` | string |  |  |  | the second read, usually the reverse of the same amplicon. Leave empty for a single-read consensus, which is a different question and is reported as one. |
| `reverse_complement_second` | boolean |  | `true` |  | reverse-complement the second read before merging. A reverse read of the same amplicon needs this; two forward reads do not. |
| `algorithm` | `"Bayesian"` · `"legacy"` |  | `"Bayesian"` |  | Bayesian converts each base's Phred to a posterior and combines the reads position by position; legacy lets the higher-confidence base win each position outright. They are different callers, not settings of one. |
| `min_conf` | number |  | `20` | 1–61 | the confidence a base must clear to be called rather than written as a code. SeqTrace range 1-61. |
| `quality_trim` | boolean |  | `false` |  | trim the consensus's own ends by quality. Note this is the stage primer trimming lives inside, so primer trimming does nothing without it. |
| `trim_window` | number |  | `10` | ≥ 1 | how many consensus bases the quality-trim mean is taken over. Wider is more forgiving of a single bad base and slower to stop at a genuinely bad end. Advanced. |
| `trim_min_good` | number |  | `8` | ≥ 1 | how many of those bases must clear `min_conf` for the window to be kept. It cannot exceed `trim_window` and is clamped to it rather than refused. Advanced. |
| `trim_end_gaps` | boolean |  | `false` |  | also cut the gap runs at each end, where only one read reached. With two reads those stretches are single-read consensus and read as agreement when they are not. Advanced. |
| `trim_primers` | boolean |  | `false` |  | cut the primers off the consensus ends. It runs INSIDE the quality-trim stage, so turning it on turns that stage on too. |
| `forward_primer` | string |  |  |  | the forward primer to cut, 5→3. Only applies when trim_primers is true. |
| `reverse_primer` | string |  |  |  | the reverse primer to cut, 5→3. Only applies when trim_primers is true. |
| `primer_match` | number |  | `0.8` | 0–1 | the fraction of a primer that must match for it to be cut. 1 is exact; lower tolerates the mismatches a real read carries at its noisy start. Only applies when trim_primers is true. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `consensus` | string |  | the consensus, compact (no spacers) — what you would export or align |
| `length` | number |  | its length in bases |
| `ambiguousPositions` | number |  | positions written as an IUPAC code. Wire it into a gate — but read `readsUsed` first, because the number means two different things |
| `readsUsed` | number |  | how many reads went in. With 1, an ambiguity is low confidence; with 2, it is disagreement |
| `trimmedFromEnds` | number |  | positions the consensus's own trimming stage removed |
| `reading` | string |  | the same sentence the editor shows for this run, generated from it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "consensus_from_traces",
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

### demultiplex_reads

**Demultiplex reads**: _Which index did each read come from, and how many cannot be assigned reliably?_

Assign reads to the index each one came from, and say how many could NOT be assigned reliably — a hit further from a barcode than the set's guaranteed correction radius is not that barcode, and counting it as one is how a demultiplexing report hides a failed run.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The index set's guaranteed correction radius bounds what may be corrected.

**Does not:**
- A hit further from a barcode than that radius is not assigned, which is what keeps a failed run visible.
- Index reads only: it does not detect index hopping.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `barcodes` | string[] | **yes** |  |  | the index set the reads were tagged with. |
| `reads` | string[] | **yes** |  |  | the observed index reads to assign. |
| `metric` | `"hamming"` · `"seqlev"` · `"levenshtein"` |  | `"seqlev"` |  | must match the error model the set was designed under. Values: hamming (Hamming (substitutions)), seqlev (Sequence-Levenshtein (indels)), levenshtein (Levenshtein). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | each read with the barcode it was assigned to and the distance |
| `assigned` | number |  | reads assigned within the guaranteed correction radius |
| `ambiguous` | number |  | reads whose nearest barcode is further than the set can correct — these are NOT that sample |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "demultiplex_reads",
  "arguments": {
    "barcodes": [],
    "reads": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### draw_trace

**Draw trace**: _Draw this window of the read as a figure._

Draw a window of a Sanger read as an SVG figure: the four dye traces over their called bases, the per-base Phred bars and a base ruler. The same geometry the Chromatogram tab draws with, so the figure and the tab put every peak in the same place. Name the window around whatever you are asking about — a mutation site, a trim bound, an ambiguous call — because a whole 1,000-base read drawn at once shows nothing.

<sub>read-only · runs locally on the engine · long-running</sub>

**No scientific claim:** Draws a figure of the trace; computes no quantity.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace file to draw: its name (`read_F.ab1`) or its project file id. A file id is project-specific, so a template ships this unset. |
| `from` | number |  | `1` | ≥ 1 | first base drawn, 1-based and inclusive. Clamped into the read. |
| `bases` | number |  | `60` | 5–500 | how many bases to draw. Keep it to a window you can read: past about 120 the peaks are narrower than the letters over them. |
| `width` | number |  | `900` | 200–4000 | figure width. It SETS the per-base zoom for the window asked for, never crops it. In px. |
| `trace_height` | number |  | `180` | 60–800 | height of the peak band, under the ruler, quality and base rows. In px. Advanced. |
| `palette` | `"classic"` · `"cvd"` · `"print"` |  | `"print"` |  | which ink each dye is drawn in. `print` is the default here because the figure travels outside the app and onto white; `cvd` is the color-vision-deficiency-safe set. Values: classic (Classic (ABI)), cvd (Color-blind safe), print (Print (on white)). |
| `quality` | boolean |  | `true` |  | print the per-base Phred bars. A file with no confidence (many SCFs) draws none whatever this says. |
| `bases_row` | boolean |  | `true` |  | print the called bases between the ruler and the peaks. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `svg` | string or null |  | the trace window as an SVG figure |
| `width` | number | px | figure width in px |
| `height` | number | px | figure height in px |
| `read` | string |  | the read drawn |
| `firstBase` | number |  | first base drawn, 1-based inclusive, AFTER clamping into the read |
| `lastBase` | number |  | last base drawn, 1-based inclusive |
| `sequence` | string |  | the calls in the window drawn, so the picture and the string cannot disagree |
| `meanQuality` | number |  | mean Phred over the window drawn, or 0 when the file carries no confidence — read `hasQuality` beside it rather than reading 0 as bad calls |
| `hasQuality` | boolean |  | whether this file carries per-base confidence at all |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "draw_trace",
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

### fastq_qc

**FASTQ QC**: _Is this FASTQ run fit to use, module by module, the way a FastQC report would grade it?_

FastQC's report on FASTQ reads, every module a default FastQC run reports: per-base quality boxes, per-tile quality (when the headers carry a tile), per-sequence quality, per-base sequence content, per-sequence GC against FastQC's theoretical normal, per-base N content, sequence length distribution, duplication levels, overrepresented sequences with their possible source, and adapter content, each with FastQC's own pass/warn/fail grade and the limit it was graded on. The numbers are FastQC 0.13.0's, checked against the real program, including its quirks: a read's mean quality is the integer mean of its characters, GC is counted on the read cut to a whole 100 (or 1,000) bases, duplication is counted on the first 50 bases, and an adapter found at a position counts at every position after it, so the curve is cumulative. FastQC does not detect the encoding: Phred+33 unless you say 64. It does not trim or filter anything.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Quality scores are Phred at the stated offset; FastQC does not infer it.
- The adapter list is the one the library could carry (FastQC's own list unless one is given).

**Does not:**
- No k-mer module: FastQC's own defaults switch it off.
- Grades use FastQC's default limits.

**Not read from this result:** FastQC's own answer is a pass, warn or fail grade per module, which the outputs carry; the FASTQ canvas draws those grades and writes no sentence over them.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `reads` | string | **yes** |  |  | the reads, as FASTQ: four lines per record, quality line required. |
| `grouping` | `"linear"` · `"none"` · `"exponential"` |  | `"linear"` |  | how read positions pool into one group: FastQC's default (the first 9 bases one by one, then groups sized to stay under 75), none (one per base, --nogroup) or exponential (--expgroup). |
| `phred_offset` | number |  | `33` | 33–64 | quality encoding: 33 for every modern FASTQ, 64 only for pre-1.8 Illumina (FastQC's --phred64). Advanced. |
| `adapters` | string |  |  |  | adapters to search for, in FastQC's --adapters format (a name, a tab, a sequence, one per line). Unset searches FastQC's own list. Advanced. |
| `contaminants` | string |  |  |  | sequences an overrepresented read is matched against for its possible source, in FastQC's --contaminants format (a name, a tab, a sequence, one per line). Unset uses FastQC's own list. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `report` | any |  | every module's table and grade: perBaseQuality (boxes), perTileQuality (null without tiles), perSequenceQuality, perBaseContent, perSequenceGc (counts, theoretical, mode, stdev, deviationPercent), nContent, lengthDistribution, duplication (percentOfTotal, percentRemaining), overrepresented (sequences with count, percentage, possibleSource), adapterContent |
| `grades` | any |  | module name to pass, warn or fail |
| `failed` | number |  | how many modules FastQC would fail |
| `gcDeviationPercent` | number | % | how far the per-read GC distribution sits from FastQC's normal, as a percent of reads |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fastq_qc",
  "arguments": {
    "reads": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### map_reads

**Map reads**: _Where on the reference does each read or contig align, with what MAPQ, as SAM?_

Map sequencing reads (FASTQ or FASTA) or assembled contigs onto a reference and return the alignment as SAM, the file a pileup viewer, a variant caller or `samtools` reads next. This is minimap2 (minimizer seeds, chaining, banded dual-affine extension with inversion detection, MAPQ), ported and checked record for record against the minimap2 2.31 CLI under every `preset` it offers: Illumina short reads (`sr`, the default), RNA-seq across introns (`splice:sr` for short reads, `splice` and `splice:hq` for long RNA or cDNA, which also report every splice junction with its read support), Nanopore, PacBio HiFi and CLR, accurate long reads, Illumina Complete Long Reads, assemblies at three divergence levels, and all-vs-all read overlaps (`ava-pb`, `ava-ont`, where the reads are their own reference and the output is PAF). Give `mates` to map read pairs (`sr` and `splice:sr`): the two inputs pair record for record, mate 2 facing mate 1 (FR), and pairing lifts a mate placed in a repeat by its uniquely placed partner. Leave `reference` unset to map against the record this step runs on; a multi-record FASTA maps against every record.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The preset matches the read type (short reads, long reads, assemblies).

**Does not:**
- A read in a repeat is placed once with a low MAPQ, not at every copy.
- Mapping only: variant calling is a separate step.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `reads` | string | **yes** |  |  | the reads: FASTQ (quality kept in the SAM) or FASTA (QUAL written as `*`). |
| `mates` | string |  |  |  | mate-2 reads, pairing record for record with `reads`. Empty maps the reads single-end. |
| `reference` | string |  |  |  | what to map against: bases, or a FASTA with one or more records. Unset, it is the record this step runs on. |
| `preset` | `"sr"` · `"splice:sr"` · `"splice"` · `"splice:hq"` · `"map-ont"` · `"lr:hq"` · `"map-hifi"` · `"map-pb"` · `"map-iclr"` · `"lr:hqae"` · `"asm5"` · `"asm10"` · `"ava-pb"` · `"ava-ont"` · `"asm20"` |  | `"sr"` |  | what is being mapped (`-x`): it sets every option below to minimap2's values for that data. The defaults shown are the short-read preset's; an option left unset takes the chosen preset's own value. Values: sr (Short reads), splice:sr (Short RNA-seq reads), splice (Long RNA reads, cDNA), splice:hq (Accurate long RNA reads), map-ont (Nanopore), lr:hq (Accurate long reads), map-hifi (PacBio HiFi), map-pb (PacBio CLR), map-iclr (Illumina Complete Long Reads), lr:hqae (Assembly evaluation), asm5 (Assembly, ~0.1% divergent), asm10 (Assembly, ~1% divergent), ava-pb (PacBio all-vs-all overlaps), ava-ont (Nanopore all-vs-all overlaps), asm20 (Assembly, several % divergent). |
| `homopolymer_compressed` | boolean |  | `false` |  | seed on homopolymer-compressed sequence (`-H`), so runs of one base count once: the PacBio CLR preset's answer to its length errors in homopolymers. Advanced. |
| `k` | number |  | `21` | 1–28 | k-mer size of the minimizer seeds (`-k`). Advanced. |
| `w` | number |  | `11` | 1–255 | minimizer window (`-w`): one seed kept per this many consecutive k-mers. Advanced. |
| `max_seed_occurrence` | number |  | `1000` | ≥ 1 | seeds occurring more often than this in the reference are skipped (`-f`); the query length they cover is what `rep_len` reports, and it lowers MAPQ. Advanced. |
| `min_minimizers` | number |  | `2` | ≥ 1 | fewest seeds a chain may have (`-n`). Advanced. |
| `bandwidth` | number |  | `100` | ≥ 1 | band of the chaining and alignment dynamic programming (`-r`, first value): the most the two sequences may drift against each other inside one chain. In bp. Advanced. |
| `bandwidth_long` | number |  | `100` | ≥ 1 | wider band for the long join (`-r`, second value): when the best chain leaves much of a long read unexplained, its seeds are re-chained in this band. No effect under the short-read preset. In bp. Advanced. |
| `max_gap` | number |  | `100` | ≥ 1 | a chain stops at a gap longer than this between seeds (`-g`). In bp. Advanced. |
| `min_chain_score` | number |  | `25` | ≥ 0 | lowest chaining score kept (`-m`), roughly the number of matching bases the seeds cover. |
| `match_score` | number |  | `2` | 1–127 | score per matching base (`-A`). Advanced. |
| `mismatch_penalty` | number |  | `8` | 0–127 | penalty per mismatch (`-B`). Advanced. |
| `transition_penalty` | number |  | `0` | 0–127 | penalty for a transition (A↔G, C↔T) mismatch (`-b`); 0 scores it as any mismatch. Illumina Complete Long Reads use 4. Advanced. |
| `gap_open` | number |  | `12` | 0–127 | gap-open penalty of the short-gap cost (`-O`, first value). Advanced. |
| `gap_open_long` | number |  | `24` | 0–127 | gap-open penalty of the long-gap cost (`-O`, second value); a gap costs the cheaper of the two. Advanced. |
| `gap_extend` | number |  | `2` | 1–127 | per-base extension of the short-gap cost (`-E`, first value). Advanced. |
| `gap_extend_long` | number |  | `1` | 1–127 | per-base extension of the long-gap cost (`-E`, second value). Advanced. |
| `zdrop` | number |  | `100` | ≥ 0 | Z-drop (`-z`): stop extending when the score falls this far below its best, which clips a read at a junction instead of forcing it through. Advanced. |
| `noncanonical_penalty` | number |  | `9` | 0–127 | cost of a splice site that is not GT..AG, GC..AG or AT..AC (`-C`). Only the splice presets align across introns. Only applies when preset is splice or splice:hq or splice:sr. Advanced. |
| `max_intron` | number |  | `200000` | ≥ 1 | longest intron an alignment may span (`-G`); it also sets the reference gap and both chaining bands, as minimap2 does. In bp. Only applies when preset is splice or splice:hq or splice:sr. Advanced. |
| `zdrop_inversion` | number |  | `100` | ≥ 0 | Z-drop at which a stalled long alignment is tested for an inversion (`-z`, second value); an inverted segment found there is written as its own record. Advanced. |
| `end_bonus` | number |  | `10` | ≥ 0 | bonus for reaching the read's end (`--end-bonus`); higher prefers end-to-end alignment over soft-clipping. Advanced. |
| `min_dp_score` | number |  | `40` | ≥ 0 | lowest peak alignment score kept (`-s`). |
| `max_fragment_length` | number |  | `800` | ≥ 1 | longest fragment (insert) two mates may span and still pair (`--frag`/`-I`). In bp. Only applies when mates is set. |
| `secondary_ratio` | number |  | `0.5` | 0–1 | a secondary placement is kept when its score is at least this fraction of the primary's (`-p`). |
| `max_secondary` | number |  | `20` | ≥ 0 | most secondary placements kept per read (`-N`). |
| `output_format` | `"sam"` · `"paf"` |  |  |  | SAM (`-a`, every read with its alignment) or PAF (minimap2's default: one line per hit, no read sequence). Unset: PAF for the all-vs-all presets, SAM otherwise. Values: sam (SAM), paf (PAF). |
| `base_alignment` | boolean |  | `false` |  | in PAF, align base by base (`-c`): exact ends, CIGAR as `cg:Z`, NM. Off, a hit's coordinates are its chain's ends, which is much faster. SAM always aligns. Only applies when output_format is paf. |
| `write_secondary` | boolean |  | `false` |  | also write secondary records to the SAM (`--secondary=yes`); off, they are counted but not written, as minimap2 does for short reads. |
| `mark_duplicates` | boolean |  | `false` |  | mark PCR and optical duplicates (`samtools fixmate -m`, `sort`, `markdup`): reads whose 5′ ends, strands and mate position match are copies of one fragment; the best by base quality is kept and the rest flagged 0x400. The SAM comes back sorted by coordinate, and flagstat, coverage and depth then count the flags. |
| `markdup_mode` | `"t"` · `"s"` |  | `"t"` |  | what makes two reads duplicates (`-m`): the template's two outer ends (samtools' default, as Picard), or each read's start by strand. Values: t (Template ends), s (Read starts). Only applies when mark_duplicates is true. |
| `markdup_optical_distance` | number |  | `0` | ≥ 0 | also call a duplicate optical when its Illumina tile x/y lies within this many pixels of the original's (`-d`); 0 is off. Illumina suggests 100 for unpatterned flow cells and 2,500 for patterned ones. In px. Only applies when mark_duplicates is true. |
| `markdup_remove` | boolean |  | `false` |  | remove the duplicates from the SAM instead of flagging them (`-r`). Only applies when mark_duplicates is true. |
| `markdup_supplementary` | boolean |  | `false` |  | also flag the supplementary, secondary and unmapped records of a duplicate (`-S`). Only applies when mark_duplicates is true. |
| `markdup_tag` | boolean |  | `false` |  | tag each duplicate with the name of the read it copies (`do:Z`, `-t`). Only applies when mark_duplicates is true. |
| `depth` | `"none"` · `"covered"` · `"all"` |  | `"none"` |  | per-base read depth of the SAM written (`samtools depth`): off; every position inside some read's span (an intron or deletion inside a read prints 0); or every position of each reference a read landed on (`-a`). Reads that are unmapped, secondary, QC-failed or duplicate are not counted. Values: none (Off), covered (Covered positions), all (Every position (-a)). |
| `depth_count_deletions` | boolean |  | `false` |  | count a read's deletions toward the depth under them (`-J`); off, a deleted base is not covered by that read. Only applies when depth is covered or all. |
| `depth_remove_overlaps` | boolean |  | `false` |  | count the overlap of a read pair once (`-s`): the second mate starts counting where the first ended. Only applies when depth is covered or all. |
| `depth_min_base_quality` | number |  | `0` | 0–93 | a base below this quality does not count (`-q`). Only applies when depth is covered or all. |
| `depth_min_mapping_quality` | number |  | `0` | 0–255 | a read below this mapping quality does not count (`-Q`). Only applies when depth is covered or all. |
| `depth_min_read_length` | number |  | `0` | ≥ 0 | a read with fewer aligned bases than this (soft clips excluded) does not count (`-l`). In bp. Only applies when depth is covered or all. |
| `md_tag` | boolean |  | `false` |  | write MD tags (`--MD`); the consensus uses them to trust reads with edits nearby less. |
| `consensus` | `"off"` · `"fasta"` · `"fastq"` · `"pileup"` |  | `"off"` |  | the sample's sequence called from the reads over the reference (`samtools consensus`); N where no call is confident. Values: off (Off), fasta (FASTA), fastq (FASTQ (with quality)), pileup (Pileup (every column)). |
| `consensus_mode` | `"bayesian"` · `"bayesian_p"` · `"bayesian_m"` · `"bayesian_116"` · `"simple"` |  | `"bayesian"` |  | how a column is called (`-m`). Values: bayesian (Bayesian), bayesian_p (Bayesian, precise), bayesian_m (Bayesian, blended), bayesian_116 (Bayesian (samtools 1.16)), simple (Simple counting). Only applies when consensus is fasta or fastq or pileup. |
| `consensus_profile` | `"none"` · `"hiseq"` · `"hifi"` · `"r10.4_sup"` · `"r10.4_dup"` · `"ultima"` |  | `"none"` |  | a platform's quality calibration and tuned parameters (`-X`). Values: none (None), hiseq (Illumina HiSeq), hifi (PacBio HiFi), r10.4_sup (Nanopore R10.4 simplex (sup)), r10.4_dup (Nanopore R10.4 duplex), ultima (Ultima Genomics). Only applies when consensus is fasta or fastq or pileup. |
| `consensus_positions` | `"covered"` · `"reference"` · `"all"` |  | `"covered"` |  | which positions are written. Values: covered (Covered span), reference (Whole reference (-a)), all (Every reference (-aa)). Only applies when consensus is fasta or fastq or pileup. |
| `consensus_fill_reference` | boolean |  | `false` |  | the reference's base where no read gives one (`-T`), instead of N. Only applies when consensus is fasta or fastq or pileup. |
| `consensus_region` | string |  | `""` |  | one region (`-r`): name or name:start-end, 1-based. Only applies when consensus is fasta or fastq or pileup. |
| `consensus_show_deletions` | boolean |  | `false` |  | write a deletion as `*` (`--show-del`). Only applies when consensus is fasta or fastq or pileup. |
| `consensus_show_insertions` | boolean |  | `true` |  | write inserted bases (`--show-ins`). Only applies when consensus is fasta or fastq or pileup. |
| `consensus_ambiguity` | boolean |  | `false` |  | a heterozygous call as its IUPAC code (`-A`). Only applies when consensus is fasta or fastq or pileup. |
| `consensus_min_depth` | number |  | `1` | ≥ 1 | fewer usable reads than this is N (`-d`). Only applies when consensus is fasta or fastq or pileup. |
| `consensus_args` | string |  | `""` |  | further `samtools consensus` options, applied last (e.g. `--min-MQ 20 -t :hiseq`); all but files and threads. Only applies when consensus is fasta or fastq or pileup. |
| `variants` | boolean |  | `false` |  | call SNVs and indels from the SAM written (`bcftools mpileup \| bcftools call -mv`): genotype, quality, allelic depths and strand counts per site, as VCF. |
| `variants_indels` | boolean |  | `true` |  | call indels too, with bcftools' default indel model (off is `-I`, SNVs only). Only applies when variants is true. |
| `variants_baq` | boolean |  | `true` |  | recalibrate base qualities by their alignment uncertainty near indels (BAQ, bcftools' default; off is `-B`). Only applies when variants is true. |
| `variants_full_baq` | boolean |  | `false` |  | run BAQ on every read at a column with an indel, not only the reads it is likely to change (`-D`; nothing with BAQ off). Only applies when variants is true. |
| `variants_adjust_mq` | number |  | `0` | 0–255 | cap the mapping quality of reads with many high-quality mismatches (`-C`; 50 for BWA reads, 0 is off, values up to 10 do nothing). Only applies when variants is true. |
| `variants_min_mapping_quality` | number |  | `0` | 0–255 | skip reads below this mapping quality (`-q`). Only applies when variants is true. |
| `variants_min_base_quality` | number |  | `1` | 0–93 | skip bases below this quality (`-Q`). Only applies when variants is true. |
| `variants_max_depth` | number |  | `250` | 1–255 | most reads piled up per position (`-d`); at most 255, where bcftools starts downsampling at random. Only applies when variants is true. |
| `variants_count_orphans` | boolean |  | `false` |  | keep reads paired but not properly paired (`-A`). Only applies when variants is true. |
| `variants_overlap_adjustment` | boolean |  | `true` |  | where two mates overlap, count the shared bases once by zeroing one mate's qualities (off is `-x`). Only applies when variants is true. |
| `variants_min_indel_reads` | number |  | `2` | ≥ 1 | fewest reads carrying an indel for it to be considered (`-m`). Only applies when variants is true. |
| `variants_min_indel_fraction` | number |  | `0.05` | 0–1 | smallest fraction of reads carrying an indel for it to be considered (`-F`). Only applies when variants is true. |
| `variants_gap_open` | number |  | `40` | 0–255 | phred-scaled probability that sequencing opens a gap (`-o`); lower calls more indels. Only applies when variants is true. |
| `variants_gap_extend` | number |  | `20` | 0–255 | phred-scaled probability that sequencing extends a gap (`-e`). Only applies when variants is true. |
| `variants_homopolymer` | number |  | `500` | ≥ 0 | how strongly a homopolymer run lowers an indel's quality (`-h`); lower trusts indels in runs less. Only applies when variants is true. |
| `variants_indel_size` | number |  | `110` | ≥ 20 | approximate largest indel considered, in bases (`--indel-size`, at least 20). Only applies when variants is true. |
| `variants_indel_bias` | number |  | `1` | ≥ 0 | raise to favour indel recall over precision (`--indel-bias`). Only applies when variants is true. |
| `variants_max_indel_depth` | number |  | `250` | ≥ 1 | positions this deep or deeper get no indel call (`-L`). Only applies when variants is true. |
| `variants_prior` | number |  | `0.0011` | 0–0.99 | the mutation-rate prior (`call -P`): higher calls more sites. Only applies when variants is true. |
| `variants_keep_reference` | boolean |  | `false` |  | also write the positions where the reads agree with the reference (`call -m` without `-v`): one record per covered position, variant or not. Only applies when variants is true. |
| `variants_args` | string |  | `""` |  | further `bcftools mpileup` options (`--max-BQ`, `--delta-BQ`, `--ff`, `-M`, `-E`). Only applies when variants is true. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sam` | string |  | the alignment as SAM text (header + records), as `minimap2 -ax <preset>` writes it. Open it in the pileup, or hand it to a variant caller |
| `paf` | string |  | the hits as PAF, as minimap2 writes it by default (empty when the output is SAM); for the all-vs-all presets, every overlap between two reads |
| `mapped` | number |  | reads with a primary placement |
| `unmapped` | number |  | reads with none |
| `properlyPaired` | number |  | reads in a proper pair (0 when mapped single-end) |
| `mapq0` | number |  | mapped reads with MAPQ 0: placed, but with an equally good placement elsewhere |
| `meanIdentity` | number or null |  | mean identity of primary alignments, matching bases over aligned columns (0–1). Null when no read aligned, so there is nothing to measure: a 0 would read as every base mismatched |
| `stats` | any |  | every count: reads, fragments, mapped, unmapped, MAPQ bins, proper pairs, supplementary and secondary placements, reads spanning an intron, and per reference its reads and covered bases |
| `options` | any |  | every minimap2 option the run used, with its flag, the preset value, and whether it was changed |
| `junctions` | string |  | splice junctions as `minimap2 --write-junc` writes them (BED-like: reference, start, end, read, motif score, strand; one line per intron per read, primary alignments of MAPQ 10 or more). Empty outside the splice presets |
| `junctionTable` | any |  | each distinct junction once: reference, start, end, strand, motif score (6 = GT..AG) and the number of reads that support it |
| `flagstat` | string |  | `samtools flagstat` of the SAM written, as samtools prints it (QC-passed + QC-failed: total, primary, secondary, supplementary, duplicates, mapped, paired, properly paired, singletons, mates on another reference). Empty for PAF. Null for PAF output, which writes no SAM to summarize |
| `coverage` | any |  | `samtools coverage` of the SAM written: per reference its reads, covered bases, percent covered, mean depth, mean base quality and mean mapping quality (reads that are unmapped, secondary, QC-failed or duplicate excluded, as samtools does). Null for PAF output, which writes no SAM to summarize |
| `markdup` | string |  | `samtools markdup`'s statistics when duplicates were marked: reads examined, pairs and singles, duplicate pairs and singles, optical duplicates, and the estimated library size. Empty otherwise |
| `depth` | string |  | `samtools depth` of the SAM written, as samtools prints it (reference, 1-based position, depth; one line per position). Empty unless `depth` asks for it |
| `consensus` | string |  | `samtools consensus` of the SAM written, as samtools prints it (FASTA, FASTQ or pileup). Empty unless `consensus` asks for it |
| `consensusSummary` | any |  | the consensus counted: sequences, bases, N (no call), IUPAC ambiguity codes, lower-case and deletion calls, mean quality, and the samtools arguments used |
| `vcf` | string |  | SNVs called from the SAM written, as `bcftools call -mv` writes the VCF (GT, PL, AD; DP, DP4, MQ and the bias tests per site). Empty unless `variants` is on. Open it in the variant viewer |
| `calls` | any |  | each call: contig, position, reference and alternate alleles, QUAL, genotype, depth, DP4, allelic depths, PL and mean mapping quality. Empty unless `variants` is on |
| `variantSummary` | any |  | the calls counted: SNVs, indels, homozygous and heterozygous, transitions and transversions among the SNVs, covered positions, and the bcftools command used |
| `reading` | string |  | what the run found, generated from its counts: the conclusion, then each qualifier the run earned |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "map_reads",
  "arguments": {
    "reads": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### read_sequencing_qc

**Read sequencing QC**: _Is a disappointing read the clone's fault or the run's, from the provider's coverage table or summary?_

Read the QC files a sequencing provider returns alongside the reads: a per-base COVERAGE table, or a Plasmidsaurus summary (k-mer composition and the contamination estimate with its named source). These are the numbers that say whether a disappointing read is the clone's fault or the run's — a base called wrong under 3x coverage is a sequencing problem, not a cloning one. For a coverage table it also measures the track's SHAPE, because a mean has none: a run averaging 200x with one uncovered region reads as excellent. The provider states one number and two shapes — 20x for an accurate consensus, and a large gap or a sudden large increase meaning an assembly issue or a mixture of plasmid species — so the longest stretch under the line and the largest change in level are both measured and located. How large is large is NOT a number they publish, and none is invented here: the shapes are reported and the call is the reader's.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Depth is counted as htslib piles up the provider's alignments.

**Does not:**
- Reads what the provider computed; it does not re-map the reads.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | **yes** |  |  | the file's contents — a per-base coverage TSV (pos / ref / reads_all), or the provider's summary text. |
| `kind` | `"auto"` · `"perbase"` · `"plasmidsaurus"` |  | `"auto"` |  | which report this is; `auto` sniffs it. Values: auto (Detect from the contents), perbase (Per-base coverage table), plasmidsaurus (Plasmidsaurus summary). |
| `coverage_line` | number |  | `20` | ≥ 1 | the depth a position must reach to count as well covered. The default is the provider's own published line and nothing of ours; raise it for a construct you intend to publish. |
| `step_window` | number |  | `25` | ≥ 1 | positions either side of a boundary whose MEDIAN depth is compared, when looking for a sudden change in level. A median over a window rather than two adjacent positions, so one spike is not a step and a real change in level is. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `kind` | string |  | which report was actually read |
| `perbase` | any |  | per-base coverage: positions counted, mean/min/max read depth, and how many positions reach 20x |
| `minCoverage` | number or null |  | the LOWEST depth anywhere in the read — the number that decides whether a disagreement with the reference is believable. Null for a Plasmidsaurus summary, which measures no depth |
| `positionsAbove20x` | number or null |  | positions at 20x or better, out of the total. Null for a Plasmidsaurus summary |
| `contaminationPct` | number or null | % | Plasmidsaurus' contamination estimate, as a percentage. Null when the summary states none, and for a coverage table: a 0 would read as a clean run nobody measured |
| `contaminationSource` | string or null |  | what the provider says the contaminant IS — the half of the estimate that tells you what to do about it. Null when the summary names none, and for a coverage table |
| `plasmidsaurus` | any |  | the whole parsed summary, including the raw text it came from |
| `shape` | any |  | the coverage track's SHAPE: its median, how many positions fall under the line and in how many separate runs, the longest such run with its coordinates and its floor, and the largest change in level with the position it is at |
| `longestGap` | number or null |  | positions in the longest unbroken stretch under the coverage line — the provider's first warning shape. 0 means no position falls under it; null for a Plasmidsaurus summary, which has no track |
| `largestStepFold` | number or null |  | the largest sustained rise in depth, as a multiple — the provider's second warning shape. Branch on this rather than re-deriving it from the profile. Null when no step could be measured (a track shorter than two windows, or a Plasmidsaurus summary): a 0 is not a fold |
| `depthProfile` | object or null |  | the depth track drawn: the MINIMUM and the mean depth per window, with the coverage line and the track's median as rules, so a drop-out reads as a drop-out rather than being averaged away. Null for a Plasmidsaurus summary, which measures no track |
| `depthProfile.x` | number[] |  |  |
| `depthProfile.series` | object[] |  |  |
| `depthProfile.series[].name` | string |  |  |
| `depthProfile.series[].y` | (number or null)[] |  |  |
| `depthProfile.xLabel` | string |  |  |
| `depthProfile.yLabel` | string |  |  |
| `depthProfile.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `depthProfile.title` | string |  |  |
| `depthProfile.rules` | object[] |  |  |
| `depthProfile.rules[].y` | number |  |  |
| `depthProfile.rules[].label` | string |  |  |
| `reading` | string |  | what the coverage track says, generated from the profile that was measured rather than from the request, with the provider's own sentence quoted as theirs |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_sequencing_qc",
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

### read_structure_consensus

**Read structure consensus**: _Which base pairs does a Stockholm alignment's consensus structure state, and how many aligned rows actually form each one?_

Read the consensus RNA secondary structure a Stockholm alignment states in its `#=GC SS_cons` line (WUSS, the notation Rfam and Infernal write), and measure how well the aligned rows actually support it. Reports the base pairs, what each unpaired column is (hairpin, bulge, multifurcation, external, insertion, local end), and per pair the fraction of rows whose two bases form a canonical or GU wobble pair. Use it to check whether a family's published structure is borne out by the sequences, or to pull a pair table out of an alignment for drawing. Reading only, and it REFUSES a Pfam alignment by name: `SS_cons` is two alphabets, and Pfam writes protein DSSP states in the same field, where C/H/E are pseudoknot letters in WUSS — parsing one as the other would invent base pairs for a protein.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- SS_cons is WUSS notation (Rfam, Infernal); a Pfam file is refused because the same field holds protein states there.
- Canonical and GU wobble pairs count as support.

**Does not:**
- Measures support for the stated structure; it does not predict or fold one.

**Not read from this result:** The answer is the stated pairs and how many rows form each, which the outputs carry; the MSA canvas draws them as a structure line and a support histogram and writes no reading over them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | **yes** |  |  | the alignment file's contents. Stockholm is the only format that records `#=GC` annotation, so a CLUSTAL or PHYLIP file is refused by name rather than returning an empty structure. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `pairs` | number |  | base pairs the consensus states |
| `columns` | number |  | alignment width the annotation covers |
| `rows` | number |  | aligned sequences the support was measured over |
| `pairTable` | any |  | per column, its partner column or -1 — the same shape `pairTable` returns, so it wires straight into an arc drawing |
| `pairList` | any |  | every pair as {i, j}, plus `knotLetter` when it came from a pseudoknot letter rather than a bracket |
| `roles` | any |  | per column, what its glyph said: pair, hairpin, bulge, multifurcation, external, insertion or missing |
| `medianSupport` | number |  | the median, over pairs that any row spans, of the fraction of those rows forming a canonical or wobble pair. The panel's own headline number — a family whose structure is real sits high here, and a low value means the rows do not do what the annotation says |
| `support` | any |  | per column, {observed, paired} or null where the column is unpaired — the denominator travels so a caller can say "no evidence" instead of drawing a zero |
| `alphabet` | string |  | which alphabet the `SS_cons` line was written in: `wuss`, `protein-dssp`, or `unknown` |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_structure_consensus",
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

### recompute_trace_quality

**Recompute trace quality**: _What Phred quality does each of this trace's calls earn, measured from its peaks?_

Re-score a Sanger trace's own base calls from the signal, replacing the instrument's Phred values with ones measured from the peaks. Keeps the bases; only their quality changes. Reports the read's mean quality, its lowest-scoring base and the four trace parameters that base was scored from, which are the whole input to the quality table.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- TraceTuner's quality model and the calibration table named.

**Does not:**
- Keeps the bases; only the qualities change.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace to run on: a file name (`read_F.ab1`) or its project file id. Leave unset to use the trace tab on screen. A file id is project-specific, so a template ships this unset. |
| `table` | `"3700pop5"` · `"3700pop6"` · `"3100pop6"` · `"3730pop7"` |  | `"3730pop7"` |  | the instrument/polymer calibration table to score against. The same signal scores differently under each, so a quality value is only interpretable with the table named. Defaults to ABI 3730 POP-7. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `bases` | number |  | how many bases the reading called |
| `instrumentBases` | number |  | how many the FILE carries, so a gate can see a de-novo reading change the read's length |
| `meanQuality` | number |  | the mean Phred of the reading, on the calibration table it names |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "recompute_trace_quality",
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

### restore_trace_file_calls

**Restore trace file calls**: _Put the open read back on its file's own calls._

Put an open Sanger read back on the base calls its FILE carries, undoing an adopted re-call. The same carry runs in the other direction, so the trim window, the hand-corrected calls and the annotations come back with it rather than being left on indices the file does not have. Not the same as clearing the read's edits, which also discards the trim and the manual calls.

<sub>returns new records · runs locally on the engine</sub>

**No scientific claim:** Restores the calls the file carries; computes nothing.

**Arguments**

_No arguments beyond the shared `_subject` and `_files`._

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `bases` | number |  | how many bases the file's own reading carries |
| `sequence` | string |  | the read the document now carries |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "restore_trace_file_calls",
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

### trace_raw_signal

**Trace raw signal**: _What did the instrument record before processing: scans, baselines and peak values per channel?_

The UNPROCESSED signal of a Sanger trace: how many scans the instrument recorded, where each channel's baseline sits, the peak raw value, and how many scans analysis discarded off the front as dye front. This separates an instrument problem from an analysis problem — a read whose analyzed trace looks wrong while its raw channels are clean was mis-analyzed, not mis-run, and a baseline spread far above the others names the channel responsible. ABIF only: SCF and ZTR store no raw channels, and this refuses rather than substituting the processed ones.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- Only files that carry raw channels.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace file to read: its name (`read_F.ab1`) or its project file id. A file id is project-specific, so a template ships this unset. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rawScans` | number |  | scans the instrument recorded, on its own time base |
| `droppedFromFront` | number |  | scans analysis discarded off the front (dye front and primer peak). Gate on it: an unusually long discard is a run that took a long time to resolve |
| `peakRawValue` | number |  | the largest raw sample across all four channels |
| `baselineSpread` | number |  | highest channel baseline minus lowest. A large spread is one dye channel sitting high, which analysis removes and a raw view shows |
| `baseline` | any |  | per-channel median raw sample (A/C/G/T) — the offset analysis subtracts |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "trace_raw_signal",
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

### trim_reads

**Trim reads**: _What do these FASTQ reads look like after the adapters and low-quality ends are trimmed, and how much was removed?_

Trim sequencing adapters and low-quality ends off FASTQ reads before mapping, and report what was removed. This is cutadapt's algorithm: quality trimming is BWA's running-sum rule (not a threshold - a single bad base in a good tail is absorbed, a real decline is not), and the adapter is found by semiglobal alignment allowing errors, so a PARTIAL adapter at the very end of a read is caught where a substring search would miss it. Quality trimming runs FIRST and adapter removal second, which is cutadapt's own order and changes the result when a low-quality tail is also the start of an adapter. THE REPORT ATTRIBUTES EVERY REMOVED BASE TO THE STEP THAT REMOVED IT, because losing 30% of your bases to quality means a bad sequencing run and losing it to adapter means a short insert - different problems that one total cannot distinguish. It does not map anything and does not filter reads: a read trimmed to nothing is returned empty and counted, never silently dropped.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Quality scores are Phred at the stated offset.
- The adapter given is the one ligated.

**Does not:**
- Trims; it does not filter contaminants or correct bases.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `reads` | string | **yes** |  |  | the reads to trim, as FASTQ - quality lines are required, because both halves of this need them. |
| `adapter` | string |  |  |  | the adapter sequence to remove. Unset means quality trimming only. Illumina TruSeq is AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC and Nextera is CTGTCTCTTATACACATCT. |
| `adapter_kind` | `"three_prime"` · `"five_prime"` |  | `"three_prime"` |  | which end the adapter sits at. A read running off the end of its insert hits the 3' adapter, which is why that is the default. |
| `quality_cutoff_back` | number |  | `0` | 0–93 | quality cutoff for the 3' end, where quality decays with cycle number. 0 is off; 20 is the usual choice. NOT a threshold on individual bases - see the description. |
| `quality_cutoff_front` | number |  | `0` | 0–93 | quality cutoff for the 5' end, which fails for different reasons than the 3' end and so takes its own number. 0 is off, and off is the usual answer. Advanced. |
| `max_error_rate` | number |  | `0.1` | 0–0.5 | errors allowed in the adapter match, as a fraction of the overlap. cutadapt's own default. Advanced. |
| `min_overlap` | number |  | `3` | 1–30 | an adapter overlap shorter than this is ignored. Low values trim real bases by chance - at 1, a read ending in the adapter's first base is 'trimmed'. Advanced. |
| `min_length` | number |  | `0` | 0–1000 | reads shorter than this after trimming are COUNTED as too short, not removed - this tool does not filter. 0 reports none. Advanced. |
| `phred_offset` | number |  | `33` | 33–64 | quality encoding: 33 for every modern FASTQ, 64 only for pre-1.8 Illumina. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `trimmedFastq` | string |  | the trimmed reads as FASTQ, ready for `map_reads` |
| `report` | any |  | what was removed and by which step: bases before and after, the two attributed counts, reads with an adapter, reads emptied and reads left too short |
| `readsWithAdapter` | number |  | how many reads carried the adapter - the number that says whether your insert size is shorter than your read length |
| `basesRemovedByAdapter` | number |  | bases removed by adapter trimming alone |
| `basesRemovedByQuality` | number |  | bases removed by quality trimming alone |
| `readsEmptied` | number |  | reads trimmed to nothing at all - a different alarm from 'too short', because it usually means the read was all adapter |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "trim_reads",
  "arguments": {
    "reads": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### trim_trace

**Trim trace**: _Where should this read's low-quality ends be cut, by the method named?_

Trim a Sanger read's low-quality ends, by either of the two methods that answer different questions: the instrument's own Mott record as written into the file, or a sliding mean-Phred window computed here. Returns the kept interval as 1-based inclusive bounds, and the mean quality of what it KEPT beside the mean of what it DISCARDED — the pair that says whether the trim was worth making, because a trim whose discarded ends score no worse than the bases it left has shortened the read for nothing.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Mott's algorithm as the instrument recorded it, or a quality window at the threshold given.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace file to read: its name (`read_F.ab1`) or its project file id. A file id is project-specific, so a template ships this unset. |
| `method` | `"auto"` · `"mott"` · `"window"` |  | `"auto"` |  | auto = the file's own Mott record when it has one and the sliding window when it does not; mott = the instrument's record, which SCF and ZTR never carry; window = always compute it here. |
| `win_size` | number |  | `10` | ≥ 1 | bases in the sliding window, when the window method runs. |
| `min_q` | number |  | `20` | ≥ 0 | the mean Phred the window has to hold for a bound to stop walking inward. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `firstBaseKept` | number |  | 1-based inclusive, matching every trim readout in the editor |
| `lastBaseKept` | number |  | 1-based inclusive |
| `keptBases` | number |  | how many bases survived. Wire it into a gate: a read trimmed to nothing is not a read |
| `sequence` | string |  | the trimmed read, ready to align or verify |
| `methodUsed` | string |  | which one actually ran. `auto` and `mott` both answer `window` when the file carries no Mott record, and a pipeline that assumed otherwise trimmed on a threshold nobody chose |
| `meanQualityKept` | number |  | mean Phred over the kept interval |
| `meanQualityDiscarded` | number |  | mean Phred over what was cut. Read it AGAINST the kept figure: if it is not lower, the trim removed nothing bad |
| `reading` | string |  | the same sentence the editor shows for this run, generated from it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "trim_trace",
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

### verify_construct

**Verify construct**: _Where does the sequencing result differ from the designed construct, and what does each difference land in?_

Compare a sequencing RESULT against the construct you designed and say what differs, where, and what it lands in. Aligns the two, reports every substitution, indel and uncalled position, then maps each onto the design's features and ranks them by Ensembl's published consequence severity — so a pipeline can gate on 'nothing worse than synonymous' rather than on a bare difference count.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The result aligns to the design under the scoring given.

**Does not:**
- Positions the result does not cover are reported as uncovered, never as matching.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `design` | string | **yes** |  |  | the construct you INTENDED — wire an upstream record or name a library document. Its features come with it, and they are what turns a difference into a consequence. |
| `result` | string | **yes** |  |  | what actually came back from sequencing — wire a record or name a document. |
| `word_size` | number |  | `16` | 8–64 | alignment limit `wordSize`, as the Verify panel's own slider sets it. Advanced. |
| `band_margin` | number |  | `32` | 0–4096 | alignment limit `bandMargin`, as the Verify panel's own slider sets it. Advanced. |
| `min_result_fraction` | number |  | `0.2` | 0–1 | alignment limit `minResultFraction`, as the Verify panel's own slider sets it. Advanced. |
| `min_coverage` | number |  | `0.35` | 0–1 | alignment limit `minCoverage`, as the Verify panel's own slider sets it. Advanced. |
| `confident_coverage` | number |  | `0.8` | 0–1 | alignment limit `confidentCoverage`, as the Verify panel's own slider sets it. Advanced. |
| `match` | number |  | `1` | 1–10 | alignment limit `match`, as the Verify panel's own slider sets it. Advanced. |
| `mismatch` | number |  | `-1` | -10–-1 | alignment limit `mismatch`, as the Verify panel's own slider sets it. Advanced. |
| `gap_open` | number |  | `1` | 0–20 | alignment limit `gapOpen`, as the Verify panel's own slider sets it. Advanced. |
| `gap_extend` | number |  | `1` | 0–20 | alignment limit `gapExtend`, as the Verify panel's own slider sets it. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `identity` | number | % | positions where design and result agree, over the aligned length, as a PERCENTAGE — 100 for an exact match, not 1 |
| `differenceCount` | number |  | substitutions, insertions and deletions found — NOT counting positions the sequencer could not call |
| `uncalledPositions` | number |  | positions the result could not call. Counted apart from differences on purpose: an uncalled base is not a mutation, and folding the two together reports a clean read as a damaged one |
| `worstConsequence` | string |  | the most severe consequence term any affected feature carries, by Ensembl's published ranking — the one value a gate should read |
| `affectedFeatures` | any |  | features with a real difference, missing bases or uncalled positions — worst first |
| `differences` | any |  | every difference with its 1-based position on the design and a one-line description |
| `largeEvents` | any |  | structural events — a dropped cassette or a duplicated span reads as one event here rather than as hundreds of substitutions |
| `report` | any |  | the whole verification, including the alignment frame and band |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "verify_construct",
  "arguments": {
    "design": "<string>",
    "result": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### verify_read

**Verify read**: _Does a sequencing read verify the reference, and which differences does it show?_

Grade a sequencing read against a reference (✓ verified / ⚠ near / ~ partial / ✗ divergent) from an alignment.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The alignment given is the read against its intended reference.

**Does not:**
- The verdict's identity and coverage thresholds are SpliceCraft's defaults unless changed; it grades the alignment, not the trace.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `aligned_read` | string | **yes** |  |  | gapped read (query) row. |
| `aligned_ref` | string | **yes** |  |  | gapped reference (target) row. |
| `target_name` | string |  | `"reference"` |  | what to call the reference in the report row. |
| `read_name` | string |  | `"read"` |  | what to call the read in the report row. |
| `target_len` | number | **yes** |  | ≥ 1 | reference length in bp. In bp. |
| `verified_ungapped_pct` | number |  | `99.5` | 0–100 | ungapped identity required to grade a read verified — NOT the gap-inclusive `identity` output. In %. |
| `verified_coverage_pct` | number |  | `99` | 0–100 | reference coverage required to grade a read verified. In %. |
| `verified_max_gaps` | number |  | `0` | ≥ 0 | gaps tolerated in a verified alignment. |
| `near_ungapped_pct` | number |  | `95` | 0–100 | ungapped identity required to grade a read near — NOT the gap-inclusive `identity` output. In %. |
| `near_coverage_pct` | number |  | `80` | 0–100 | reference coverage required to grade a read near. In %. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `status` | string |  | the grade: verified / near / partial / divergent |
| `identity` | number | % | gap-inclusive identity % (BLAST convention) |
| `mismatches` | number |  | mismatch count |
| `report` | any |  | the row that goes in the record: target, read, grade, ungapped identity, coverage, mismatches and indel events |
| `coveragePct` | number | % | how much of the reference the read actually covers — a perfect identity over 20% of the target is not a verified clone |
| `indelEvents` | number |  | insertion/deletion EVENTS, not bases — one 12 bp deletion is one event |
| `result` | any |  | the full alignment result (matches, mismatches, gaps, identities) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "verify_read",
  "arguments": {
    "aligned_read": "<string>",
    "aligned_ref": "<string>",
    "target_len": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
