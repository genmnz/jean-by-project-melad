# 🔗 Pipelines & lab records

_Chain tools into reproducible workflows, export records, keep lab notes._

14 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`build_addgene_deposit`](#build_addgene_deposit) | Fill Addgene's deposit spreadsheet from this record. |
| [`compare_constructions`](#compare_constructions) | Were these two constructs built the same way, step by step? |
| [`enzyme_collection`](#enzyme_collection) | Which enzymes does this saved collection hold, which can the cut catalog resolve, and how often does each cut the record? |
| [`export_construction_record`](#export_construction_record) | Write this construct's recorded build as the document named. |
| [`export_map_svg`](#export_map_svg) | What does this molecule's map look like as a publication figure, circular or linear? |
| [`export_trace`](#export_trace) | Write this read in the format named. |
| [`get_construction_history`](#get_construction_history) | What was this construct built from, by which recorded operations? |
| [`list_workflow_templates`](#list_workflow_templates) | The built-in starter workflows |
| [`plan_rnaseq_experiment`](#plan_rnaseq_experiment) | For an RNA-seq experiment testing thousands of genes at a target false discovery rate, how many biological replicates per group are needed, and what power does a given number give? |
| [`read_answer_window`](#read_answer_window) | Read one window of an answer that came back cut to the size budget: the tool, the same arguments, the field its notice named, and which items or characters to return. |
| [`remember_lab_preference`](#remember_lab_preference) | Remember the polymerase, primer window and expression host this lab uses. |
| [`run_workflow`](#run_workflow) | Run a workflow graph: nodes naming tools, wires carrying one node’s output into another’s input, $whenExpression to make a step conditional, and scatter to run a step once per element of a list. |
| [`save_enzyme_collection`](#save_enzyme_collection) | Save these enzymes as a named collection. |
| [`validate_workflow`](#validate_workflow) | Would this workflow graph run? |

---

### build_addgene_deposit

**Build addgene deposit**: _Fill Addgene's deposit spreadsheet from this record._

Fill Addgene's own deposit spreadsheet from a record: one row per plasmid with its name and sequence, plus your answers for every plasmid (purpose, plasmid type, cloning method, resistance, growth strain and the other drop-downs). The sheet is fetched from Addgene each run, so its columns and choices are current; a value it would refuse is left out and named, and `columns` lists every column with its choices. It WRITES A FILE and sends nothing.

<sub>read-only · runs locally on the engine · long-running</sub>

**No scientific claim:** Fills a submission form from the record and the user's answers; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `genbank` | string | **yes** |  |  | the plasmids to deposit, as GenBank text: one row per nucleotide record. |
| `answers` | object |  | `{}` |  | the sheet's columns to fill for every plasmid, header → value, e.g. {"Purpose": "Expresses EGFP in E. coli", "Bacterial Resistance": "Ampicillin"}. A drop-down column takes one of its own choices; run once without answers to read them from `columns`. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `file` | any |  | the filled workbook: `name`, and its bytes as `base64` |
| `written` | number |  | plasmids written into the sheet |
| `problems` | any |  | every value left out because the sheet would refuse it, with the plasmid, the column and the reason |
| `columns` | any |  | every column of Addgene's sheet: its header, Addgene's help text, and its choices where it has a drop-down |
| `reading` | string |  | what was written and what is left for the depositor, generated from the run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "build_addgene_deposit",
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

### compare_constructions

**Compare constructions**: _Were these two constructs built the same way, step by step?_

Align two constructs' build procedures step by step, in order — was this built the same way as that? Works across formats: a build received as a SnapGene binary and the same build received as an OpenCloning strategy align, because each step's identity is derived from the reaction and its parameters rather than assigned.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Each step's identity is derived from its reaction and parameters.

**Does not:**
- Compares recorded procedures, not the resulting sequences.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | File id or name for THIS side. The focused document when omitted. |
| `against` | string | **yes** |  |  | File id or name of the construct to compare against, in the same project. |
| `key` | `"abstract"` · `"processId"` |  | `"abstract"` |  | what to align on: `abstract` is the PROCEDURE (the command with its molecules abstracted away, so the same method on different DNA still matches); `processId` is the EXACT recorded operation, identical only when the very same step ran on the very same molecules. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `similarity` | number | % | shared steps as a percentage of the alignment |
| `shared` | number |  | steps both procedures have, in the same order |
| `rows` | any |  | the whole aligned history, row by row: shared, only-here, or only-there |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "compare_constructions",
  "arguments": {
    "against": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### enzyme_collection

**Enzyme collection**: _Which enzymes does this saved collection hold, which can the cut catalog resolve, and how often does each cut the open record?_

Resolve one of your saved enzyme collections to the enzyme names in it, so a later step can scan, digest or design with 'my Golden Gate set' by name instead of whatever happens to be selected. Names the collection, says which of its enzymes the cut catalog can resolve and which it cannot, and — when a record is open — how many times each one cuts it. Left unnamed it answers for the collection that is currently active, and says that is what it did.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Enzyme names resolve against the bundled REBASE cut catalog.

**Does not:**
- A name the catalog does not hold is reported, never guessed.
- Counts cuts on the open record only.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `name` | string |  |  |  | the collection to resolve, by the name it has in the Enzyme Collections panel. Left unset, the active collection is used; with none active, the whole catalog is in scope and this says so rather than returning an empty set. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `enzymes` | any |  | the enzyme names in the collection, ready to wire into any tool's `enzymes` parameter — the resolvable ones only, so a downstream digest never refuses on a name this step already knew was unusable |
| `collection` | string |  | the collection this answered for, or 'the whole catalog' when nothing is scoped |
| `count` | number |  | how many enzymes resolved — branch on this rather than counting the array |
| `unresolved` | any |  | names in the collection that the bundled cut catalog does not carry, usually a custom enzyme defined in the panel or a supplier spelling. Reported rather than dropped: a set that silently shrinks is the reason a digest comes back short |
| `census` | any |  | what this collection does to the open record, counted once: bases scanned, whether the scan wrapped the origin, names asked and resolved, total cuts, and how many enzymes cut it once, twice or more. Absent when nothing is open. This is the collection panel's own reading, so the sentence the door returns and the numbers it returns cannot disagree |
| `cutting` | any |  | per enzyme, how many times it cuts the OPEN record — absent when nothing is open, because a cut count with no molecule behind it is a number nobody asked for |
| `singleCutters` | any |  | the enzymes cutting the open record exactly once — the ones a linearization or a directional clone can use. Empty when nothing is open |
| `available` | any |  | every collection you have, by name, with its size and whether it is the active one — so a run that named the wrong collection can say what the right names were |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "enzyme_collection",
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

### export_construction_record

**Export construction record**: _Write this construct's recorded build as the document named._

Write a construct's recorded build out as a document: a methods section, a step spreadsheet, the full decoded record, the molecule carrying its own history as GenBank qualifiers, the whole strategy as an OpenCloning document, the runnable QUEEN script that rebuilds it, or the build as an SBOL 2 document. This is the Export tab of the History & Provenance panel (the same seven writers), refusing the same formats that source cannot produce.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- Refuses a format the recorded history cannot produce.

**Not read from this result:** An export: the construction history written in the format asked for, with nothing inferred; the Provenance panel's reading is on the history itself.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | File id or name. The focused document when omitted, exactly as the panel. |
| `format` | `"methods"` · `"steps_csv"` · `"record_json"` · `"genbank"` · `"opencloning"` · `"queen_script"` · `"sbol"` |  | `"methods"` |  | which document to write. `methods` is the default because it is the panel’s first row and the only one every source can produce; the other six each need something of the record, and asking for one a source cannot carry is refused by name rather than answered with an empty file. Values: methods (Methods (Markdown)), steps_csv (Steps (CSV)), record_json (Full record (JSON)), genbank (GenBank with construction history), opencloning (OpenCloning document (JSON)), queen_script (Reconstruction script (Python)), sbol (SBOL 2 construction record). |
| `sbol_syntax` | `"rdfxml"` · `"turtle"` · `"ntriples"` · `"nquads"` · `"trig"` · `"jsonld"` |  | `"rdfxml"` |  | which RDF syntax to write the SBOL record in. SBOL is RDF and the six concrete syntaxes encode ONE graph, so this changes how the document is written down and never what it says. `rdfxml` is the default because it is what the writer composes and what libSBOLj validates; the rest are re-serialised from that exact document. Ignored unless `format` is `sbol`, and saying so is refused rather than silently dropped. Values: rdfxml (RDF/XML), turtle (Turtle), ntriples (N-Triples), nquads (N-Quads), trig (TriG), jsonld (JSON-LD). Only applies when format is sbol. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `text` | string |  | the document itself, byte for byte what the panel’s download writes |
| `syntax` | string |  | the RDF syntax the SBOL record was written in, echoed because it is defaulted. Empty for every other format, which do not have one |
| `filename` | string |  | the name the panel saves it under, so a pipeline writing several agrees with it |
| `format` | string |  | the format actually written: echoed because it is defaulted, not required |
| `source` | string |  | which of the 5 records this was written from: the workbench log, a SnapGene .dna reaction graph, a QUEEN build script, an OpenCloning strategy, or an SBOL 2/3 construction record |
| `available` | any |  | the formats THIS record can produce, and for each one it cannot, why: the panel’s own enabled/disabled derivation, so a pipeline can branch on it instead of failing |
| `caution` | string |  | what the panel warns about after this write, when it warns. Empty is the healthy case: a GenBank whose construct carries no other annotation will not read its own history back, and the file looks perfect either way |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "export_construction_record",
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

### export_map_svg

**Export map SVG**: _What does this molecule's map look like as a publication figure, circular or linear?_

Render the open record's map to a publication SVG string, circular or linear — the same figure the Export panel draws, with the same knobs and the same defaults. Give it enzymes to draw the restriction sites. The linear layout can draw both strands' bases and a window of the record (start/end), which is the sequence view as a figure.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Draws the record's features and the chosen enzymes' sites; it infers nothing.

**Not read from this result:** A rendering: the map drawn as SVG, with nothing inferred.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `title` | string |  | `""` |  | figure title; left empty, the record's own name is used. |
| `size` | number |  | `1400` | 300–8000 | square canvas edge, before a legend strip is added below it. In px. |
| `transparent` | boolean |  | `false` |  | omit the backing rect, so the figure drops onto any ground. |
| `show_labels` | boolean |  | `true` |  | draw each feature's name beside its arc. |
| `collapse_duplicate_labels` | boolean |  | `true` |  | fold leader labels that would repeat a name into one row, as `misc_binding ×13` — the same rule the interactive map uses. Off reproduces the upstream renderer's figure exactly, one leader per feature. |
| `show_sites` | boolean |  | `true` |  | draw the outer restriction-site ring. |
| `legend` | boolean |  | `false` |  | add a colour key on its own strip below the map. |
| `font` | `"sans"` · `"serif"` · `"mono"` |  | `"sans"` |  | figure font — one of the three stacks that survive an SVG-to-PDF conversion without substitution. |
| `layout` | `"circular"` · `"linear"` |  | `"circular"` |  | circular: the ring; linear: the record unrolled into rows, features in lanes under a ruler and sites above it. |
| `show_bases` | boolean |  | `false` |  | linear only: draw both strands' bases over the ruler; rows wrap to keep each base readable. Only applies when layout is linear. |
| `start` | number |  |  | ≥ 1 | linear only: first base of the window to draw (1-based); left unset, the record's first base. In bp. Only applies when layout is linear. |
| `end` | number |  |  | ≥ 1 | linear only: last base of the window to draw (1-based, inclusive); left unset, the record's last base. In bp. Only applies when layout is linear. |
| `enzymes` | string[] |  |  |  | enzymes whose cut sites fill the site ring — resolved against the bundled cut catalog (REBASE spellings; smaller than the REBASE dossier the editor shows). Left unset, the run uses your active enzyme collection; with none active the ring is drawn empty rather than silently filled. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `svg` | string or null |  | publication SVG string |
| `width` | number | px | rendered width in px |
| `height` | number | px | rendered height in px — taller than the width when a legend strip was added |
| `sites` | number |  | cut sites drawn (the outer ring, or the ticks above a linear map's ruler) |
| `rows` | number |  | rows a linear map wrapped into; 0 for the circular layout |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "export_map_svg",
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

### export_trace

**Export trace**: _Write this read in the format named._

Write a Sanger read out in any of the eight formats the trace editor's Export section offers, and hand the file back as TEXT in the pipeline rather than as a download. Reports what the chosen target DROPPED — a read written as FASTA loses its annotations, and every target but FASTQ loses the per-base quality — because those losses are invisible in the file itself. Trims the ends first when asked, by the same three methods the Trim section offers, so a graph does not need a separate step to write a trimmed read.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- The formats the trace editor exports.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | which trace file to write: its name (`read_F.ab1`) or its project file id. A file id is project-specific, so a template ships this unset. |
| `format` | `"raw"` · `"plaintext"` · `"fasta"` · `"fastq"` · `"genbank"` · `"embl"` · `"gcg"` · `"nexus"` |  | `"fasta"` |  | the target. FASTQ is the only one that carries the per-base Phred; GenBank and EMBL are the only two that carry annotations; the rest are a bare sequence. |
| `trim` | `"none"` · `"auto"` · `"mott"` · `"window"` |  | `"none"` |  | trim the ends before writing, the same three ways the Trim section does. `none` writes the file's calls as they are; `auto` uses the file's own Mott record when it has one and the sliding window when it does not; `mott` is the instrument's record, which SCF and ZTR never carry; `window` always computes it here. |
| `use_internal_name` | boolean |  | `false` |  | name the record and the filename from the instrument's own sample record (ABIF `SMPL`) rather than from the file name. The instrument's name is often a plate well that means nothing outside the run; a file with no internal record uses its filename either way, and says so. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `text` | string |  | the file, as text. A VALUE and not a download, deliberately: a graph step that wrote to disk could not be composed with the step after it |
| `filename` | string |  | the name this would be saved as, with the user's own extension for this format applied |
| `sequence` | string |  | just the bases that were written, so a downstream step does not have to parse the record back apart |
| `bases` | number |  | how many bases the file carries |
| `fileBases` | number |  | how many calls the trace file holds. Read it against `bases`: the difference is what the bounds cut |
| `carriedQuality` | boolean |  | whether the per-base Phred reached the file. False on every target but FASTQ, and on a read that never had one |
| `firstBaseKept` | number |  | 1-based inclusive, the same convention `trim_trace` reports in and every trim readout in the editor uses |
| `lastBaseKept` | number |  | 1-based inclusive |
| `trimUsed` | string |  | which trim actually ran. `auto` answers `window` on a file with no Mott record, so a pipeline that assumed otherwise trimmed on a threshold nobody chose — the same trap `trim_trace`'s `methodUsed` exists for |
| `reading` | string |  | the same sentence the editor shows for this export, generated from it |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "export_trace",
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

### get_construction_history

**Get construction history**: _What was this construct built from, by which recorded operations?_

What a construct was BUILT from: the recorded operations, the molecules they consumed, how many rounds deep the build goes, and which of the 5 sources the record came from. This is the build history, not the edit history — for what CHANGED in a document and when, call get_document_history instead.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The history recorded in the file (SnapGene, QUEEN, OpenCloning or SBOL).

**Does not:**
- Only what the file recorded; an unrecorded step is absent.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string |  |  |  | File id or name. The focused document when omitted, exactly as the panel. |
| `limit` | number |  |  | 1–500 | How many steps to return, oldest first. All of them when omitted. |
| `molecule` | string |  |  |  | Keep only the steps that produced or consumed this molecule, by its recorded name — the panel’s graph-node filter. Names that are not in the history are refused with the list of the ones that are. |
| `query` | string |  |  |  | Free text over the operation, the recorded command, its info field, the process id and name, and every molecule the step names — the panel’s step filter. Composes with `molecule` rather than replacing it. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `conclusion` | string |  | one generated sentence: how much was recorded, over how many rounds, from how many starting materials, and on whose authority. The same `conclusionOf` the panel headlines |
| `source` | string |  | which of the 5 records this came from: the workbench log, a SnapGene .dna reaction graph, a QUEEN build script, an OpenCloning strategy, or an SBOL 2/3 construction record |
| `steps` | any |  | the recorded operations, oldest first, with their inputs, products and enzymes. A step that records a coordinate also carries `window`: the bounds as the file writes them, the molecule they are an index INTO (never this one), and the intervals of this record they project onto through the map QUEEN writes into it — empty, with a stated reason, when those bases are not in the finished molecule |
| `matched` | number |  | how many steps the `molecule`/`query` filters kept — the panel prints `matched/total`, and collapsing the two would make "12 of 12" and "12 of 76" the same answer |
| `total` | number |  | recorded operations in the whole build, before any filter |
| `origin` | string |  | the record this was decoded out of — NOT always the document asked for: a file with no history falls back to the project, and this names what actually answered |
| `enzymes` | any |  | the enzymes this build cut with, as the history records them |
| `derivation` | any |  | the chain behind the answer: this history ← decoder ← read from ← graded against. The last link is absent for a build recorded here, which has no oracle behind it |
| `depth` | number |  | longest chain of operations from a starting material to the construct — 1 is a single round, and more means it was built on builds |
| `graph` | any |  | the lineage itself: `levels`, the molecule names by round with the starting materials at 0, and `edges`, every parent → product pair. This is the Graph and Lineage tabs’ own derivation, and without it a caller holding `steps` would have to rebuild it from the recorded commands |
| `process_flow` | any |  | the build as named processes: `groups` (the author’s process names, each with its operations in execution order), `operations` (the quinable call, its depth, what it consumed and produced, and its recorded arguments), and `depth`. Absent for a record that carries no re-executable command list — only a QUEEN history does — and `unavailable` with the upstream reason for the one build shape QUEEN cannot draw itself |
| `inputs` | number |  | molecules the history starts from: nothing recorded produced them |
| `cautions` | any |  | only what THIS history earned — a step the decoder could not follow, products a reaction could not have made, or a limitation of the source format. Empty is the healthy case |
| `protocol` | string |  | the same numbered bench-recipe protocol the panel renders and exports |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "get_construction_history",
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

### list_workflow_templates

**List workflow templates**

The built-in starter workflows — id, name, what each does and which tools it chains. Pass an `id` to get that template’s graph back, ready to hand to `run_workflow`. This server is stateless, so these are the shipped templates only, not anything a person has saved in their own editor.

<sub>read-only</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `id` | string |  |  |  | one template id; omit for the whole listing |

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_workflow_templates",
  "arguments": {}
}
```

</details>

[↑ top](#contents)

---

### plan_rnaseq_experiment

**Plan rnaseq experiment**: _For an RNA-seq experiment testing thousands of genes at a target false discovery rate, how many biological replicates per group are needed, and what power does a given number give?_

How many biological replicates an RNA-seq experiment needs when the question is about the WHOLE experiment rather than one gene: the exact negative-binomial test with the per-gene α derived from a target false discovery rate across m genes of which m1 are expected to move (RnaSeqSampleSize 2.23.0, Zhao et al. 2018; the test is Robinson & Smyth 2008's, edgeR's exactTest), or the AVERAGE power across genes whose effects differ, with the FDR controlled (ssizeRNA 1.3.3, Bi & Liu 2016). Give `solve_for` n to size the experiment or power to score a design. With `counts` and `dispersions` from a pilot, the power is computed per gene over that real distribution rather than for one idealised gene. Unlike calculate_rnaseq_power this makes no normal approximation, so it is the one to use at small n or low counts.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Counts are negative binomial; the gene-level test is the exact conditional test on the two groups' totals, not a normal approximation.
- `exact` holds every prognostic gene at one average count and one dispersion unless `counts` and `dispersions` are given; `average_power` lets each gene's log-fold-change vary, drawn from a normal.
- The per-gene α is derived from the FDR as m1·power·f / ((m − m1)(1 − f)), which is the FDR-to-α step both packages use.

**Does not:**
- `exact` solves power on a whole-percent grid, so a power it returns is quantised to 0.01 — that is upstream's resolution, not a rounding here.
- `average_power` reaches its answer through a minimizer whose critical value is pinned to about 1e-3; the sample size it returns is exact, the power behind it to about 2e-7.
- A dispersion estimated from a small pilot is itself uncertain, and the answer is more sensitive to it than to the fold change.
- Power by simulating whole experiments through edgeR, stratified by expression, is simulate_rnaseq_power's; ssizeRNA's own voom/limma simulation wrapper is not ported.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `method` | `"exact"` · `"average_power"` |  | `"exact"` |  | which question. `exact` powers one prognostic gene with the exact negative-binomial test at an α derived from the FDR; `average_power` asks what the mean power across genes is when each gene's effect is drawn from a normal. Values: exact (Exact negative-binomial test), average_power (Average power across genes). |
| `solve_for` | `"n"` · `"power"` |  | `"n"` |  | size the experiment, or score a design you already have. Values: n (Replicates per group), power (Power). |
| `power` | number |  | `0.8` | 0–1 | the power to reach, when solving n. |
| `n` | number |  |  | ≥ 2 | biological replicates in the control group, when solving power. Only applies when solve_for is power. |
| `fdr` | number |  | `0.05` | 0–1 | the false discovery rate to control across the experiment. |
| `m` | number |  | `20000` | ≥ 2 | genes tested. Only applies when method is exact. |
| `m1` | number |  | `200` | ≥ 1 | genes expected to be differentially expressed. Only applies when method is exact. |
| `fold_change` | number |  | `2` | ≥ 0 | ρ, the minimum fold change to detect in a prognostic gene. Only applies when method is exact. |
| `count` | number |  | `5` | ≥ 0 | λ₀, the average read count for a prognostic gene in the control group. Only applies when method is exact. |
| `dispersion` | number |  | `0.5` | ≥ 0 | φ₀, the negative-binomial dispersion of a prognostic gene — the square of the biological coefficient of variation. Only applies when method is exact. |
| `size_ratio` | number |  | `1` | ≥ 0 | k, the ratio of treatment to control group size. Only applies when method is exact. Advanced. |
| `normalization_ratio` | number |  | `1` | ≥ 0 | w, the ratio of the two groups' normalization factors. Only applies when method is exact. Advanced. |
| `counts` | number[] |  |  |  | a pilot's average read count per gene. With `dispersions`, the power is computed for each of these genes and averaged, instead of for one idealised gene. Only applies when method is exact. |
| `dispersions` | number[] |  |  |  | the dispersion of each gene in `counts`, in the same order. Only applies when method is exact. |
| `effect_mean` | number |  | `1.2` |  | the mean of the normal each gene's true log-fold-change is drawn from. Only applies when method is average_power. |
| `effect_sd` | number |  | `0.1` | ≥ 0 | the spread of those true effects ACROSS genes; 0 would make every gene identical. Only applies when method is average_power. |
| `sigma` | number |  | `1` | ≥ 0 | the common within-gene standard deviation on that scale. Only applies when method is average_power. |
| `pi0` | number[] |  |  |  | the proportion of genes with no effect. A list asks the question once per proportion, which is how the answer's sensitivity to it is read. Only applies when method is average_power. |
| `max_n` | number |  | `35` | ≥ 3 | the largest replicate count to search. Only applies when method is average_power. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `method` | string or null |  | which of the two questions was answered |
| `solved` | string or null |  | which quantity was solved |
| `n` | number or null |  | replicates per group (the control group, when the groups differ) |
| `power` | number or null |  | the power that number of replicates gives |
| `alpha` | number or null |  | the per-gene α the FDR target implies |
| `curve` | object or null |  | power against replicates, which is the plot this question is read from |
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
| `rows` | any |  | each (n, power) the search evaluated, one row per n in n order, or every (pi0, n, power) for average power |
| `perGene` | any |  | the power of each gene in `counts`, when a pilot distribution was given |
| `rCall` | string or null |  | the R call that reproduces the answer |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "plan_rnaseq_experiment",
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

### read_answer_window

**Read answer window**

Read one window of an answer that came back cut to the size budget: the tool, the same arguments, the field its notice named, and which items or characters to return. The answer is derived again, so the window is the one that was cut.

<sub>read-only</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `tool` | string | **yes** |  |  | the tool whose answer was cut |
| `arguments` | object |  |  |  | the same arguments as that call |
| `field` | string | **yes** |  |  | the field the notice named ('' for the answer itself) |
| `offset` | integer |  | `0` | ≥ 0 |  |
| `limit` | integer |  | `1000` | ≥ 1 |  |

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "read_answer_window",
  "arguments": {
    "tool": "<string>",
    "field": "<string>"
  }
}
```

</details>

[↑ top](#contents)

---

### remember_lab_preference

**Remember lab preference**: _Remember the polymerase, primer window and expression host this lab uses._

Remember what this lab uses, so the PCR program, primer design and codon optimization start on it: the polymerase, the primer length and GC windows, and the expression host. Use it when the user says what they use ("we use Q5", "our primers are 20 to 24 nt"). Saved where the user reads and edits it, Settings · Lab; each panel still says when it is showing the lab's choice, and a project can still choose otherwise. Enzyme supplier order is saved in Enzyme Collections, not here.

<sub>returns new records · runs locally on the engine</sub>

**Does not:**
- Stored in this browser.

**No scientific claim:** Stores the user's preferences; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `polymerase` | `"keep"` · `"taq"` · `"dbd"` |  | `"keep"` |  | the polymerase family the PCR program starts on, or `keep` to leave the saved one as it is. Values: keep (Keep as saved), taq (Taq), dbd (Phusion / Q5 (DNA-binding domain)). |
| `polymerase_product` | `"generic"` · `"takara-taq"` · `"takara-ex-taq"` · `"takara-la-taq"` · `"takara-ex-premier"` · `"primestar-gxl"` · `"primestar-hs"` · `"primestar-max"` · `"primestar-longseq"` · `"cloneamp-hifi"` · `"speedstar-hs"` · `"terra-direct"` · `"titanium-taq"` · `"advantage-hd"` · `"qiagen-taq"` · `"qiagen-hotstartaq"` |  | `"generic"` |  | the cataloged product within that family, or `generic` for the preset alone. Values: generic (Generic preset (no datasheet)), takara-taq (Takara Bio · TaKaRa Taq / EmeraldAmp GT), takara-ex-taq (Takara Bio · TaKaRa Ex Taq / EmeraldAmp MAX), takara-la-taq (Takara Bio · TaKaRa LA Taq), takara-ex-premier (Takara Bio · TaKaRa Ex Premier), primestar-gxl (Takara Bio · PrimeSTAR GXL DNA Polymerase), primestar-hs (Takara Bio · PrimeSTAR HS DNA Polymerase), primestar-max (Takara Bio · PrimeSTAR Max DNA Polymerase Ver.2), primestar-longseq (Takara Bio · PrimeSTAR LongSeq DNA Polymerase), cloneamp-hifi (Takara Bio · CloneAmp HiFi PCR Premix), speedstar-hs (Takara Bio · SpeedSTAR HS DNA Polymerase), terra-direct (Takara Bio · Terra PCR Direct Polymerase Mix), titanium-taq (Takara Bio · Titanium Taq DNA Polymerase), advantage-hd (Takara Bio · Advantage HD Polymerase Mix), qiagen-taq (QIAGEN · Taq DNA Polymerase), qiagen-hotstartaq (QIAGEN · HotStarTaq DNA Polymerase). Only applies when polymerase is taq or dbd. |
| `primer_length_min` | number |  |  | ≥ 1 | shortest primer, nt. |
| `primer_length_max` | number |  |  | ≥ 1 | longest primer, nt. |
| `primer_gc_min` | number |  |  | 0–100 | lowest primer GC, %. |
| `primer_gc_max` | number |  |  | 0–100 | highest primer GC, %. |
| `expression_host` | string |  |  |  | the organism codon optimization targets: a scientific name or an NCBI taxonomy id. |
| `clear` | (`"polymerase"` · `"primer_length"` · `"primer_gc"` · `"expression_host"`)[] |  |  |  | preferences to forget, so those panels start on their own defaults again. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `preferences` | any |  | every lab preference as saved after this call; null where none is set |
| `changed` | any |  | which preferences this call set or cleared |
| `reading` | string |  | the saved preferences in one sentence, as the assistant reads them each turn |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "remember_lab_preference",
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

### run_workflow

**Run workflow**

Run a workflow graph: nodes naming tools, wires carrying one node’s output into another’s input, `$whenExpression` to make a step conditional, and `scatter` to run a step once per element of a list. Returns the run record — per-node status, outputs and errors, in topological order.

<sub>computes · open-world (reaches outside services)</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `graph` | object | **yes** |  |  | A workflow graph: nodes naming tools, wires carrying one node’s output into another’s input, and the two constructs a single tool call cannot express — `$whenExpression` (run this node only if…) and `scatter` (run it once per element of a list input, gathering every output into an array). |
| `graph.id` | string |  |  |  | graph id; any stable string |
| `graph.name` | string |  |  |  | a label for the run record |
| `graph.nodes` | object[] | **yes** |  |  | one entry per step: `{ id, tool, params }`, where `params` are that tool’s own arguments as the tool listing documents them. Add `"$whenExpression": "subject.length > 500"` to make the step conditional — Operators: == != < > <= >= and or not && \|\| ! + - * / % ?? (`and`/`or`/`not` are the words for `&&`/`\|\|`/`!`). Functions: abs, ceil, contains, floor, isset, len, lower, max, min, number, round, upper. Property access and indexing work (`subject.length`, `rows[0].name`); method calls do not, and there is no ternary — a condition returns one verdict. — or `scatter: ["port"]` to run it once per element of that input. |
| `graph.edges` | object[] |  |  |  | the wires: `{ id, from: { node, port }, to: { node, port } }`, naming a node by its `id` and a port by the output or input name the tool listing gives. Wire an output into `$subject` to hand the product downstream, or into `$when` to gate a step on an upstream result. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "run_workflow",
  "arguments": {
    "graph": {
      "nodes": []
    },
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### save_enzyme_collection

**Save enzyme collection**: _Save these enzymes as a named collection._

Save a set of enzymes as a named collection in your Enzyme Collections panel, so a scan that found the enzymes worth keeping ends by keeping them instead of asking you to retype the list. Every name is checked against the cut catalog first and an unknown one refuses the whole save by name, because a collection that silently lost two enzymes is worse than one that was never made. An existing collection is never overwritten unless you say so.

<sub>returns new records · runs locally on the engine</sub>

**Does not:**
- Names the catalog cannot resolve are kept and reported.

**No scientific claim:** Stores the user's choice of enzymes; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `name` | string | **yes** |  |  | what to call the collection, as it will read in the panel. |
| `enzymes` | string[] | **yes** |  |  | the enzyme names to save — wire these from a scan (enzyme_cut_counts, digest_fragments) or from enzyme_collection rather than typing them, so the set is one the engine has already resolved. |
| `replace` | boolean |  | `false` |  | overwrite a collection that already has this name. Left false, a name clash refuses and says which collection it would have replaced. |
| `activate` | boolean |  | `true` |  | make it the active collection, which is what the panel does when you create one — every enzyme parameter that is left unset then scopes to it. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `collection` | string |  | the name it was saved under |
| `count` | number |  | how many enzymes it holds |
| `created` | boolean |  | true for a new collection, false when an existing one of the same name was replaced |
| `enzymes` | any |  | the names as saved, de-duplicated in the order given — wireable straight into a scan |
| `active` | boolean |  | whether this collection is now the one an unset enzyme parameter resolves to |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "save_enzyme_collection",
  "arguments": {
    "name": "<string>",
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

### validate_workflow

**Validate workflow**

Would this workflow graph run? Returns the blocking errors — an unknown tool, a wire into a port that does not exist, a cycle — each naming the node and the port, without running anything.

<sub>read-only</sub>

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `graph` | object | **yes** |  |  | A workflow graph: nodes naming tools, wires carrying one node’s output into another’s input, and the two constructs a single tool call cannot express — `$whenExpression` (run this node only if…) and `scatter` (run it once per element of a list input, gathering every output into an array). |
| `graph.id` | string |  |  |  | graph id; any stable string |
| `graph.name` | string |  |  |  | a label for the run record |
| `graph.nodes` | object[] | **yes** |  |  | one entry per step: `{ id, tool, params }`, where `params` are that tool’s own arguments as the tool listing documents them. Add `"$whenExpression": "subject.length > 500"` to make the step conditional — Operators: == != < > <= >= and or not && \|\| ! + - * / % ?? (`and`/`or`/`not` are the words for `&&`/`\|\|`/`!`). Functions: abs, ceil, contains, floor, isset, len, lower, max, min, number, round, upper. Property access and indexing work (`subject.length`, `rows[0].name`); method calls do not, and there is no ternary — a condition returns one verdict. — or `scatter: ["port"]` to run it once per element of that input. |
| `graph.edges` | object[] |  |  |  | the wires: `{ id, from: { node, port }, to: { node, port } }`, naming a node by its `id` and a port by the output or input name the tool listing gives. Wire an output into `$subject` to hand the product downstream, or into `$when` to gate a step on an upstream result. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "validate_workflow",
  "arguments": {
    "graph": {
      "nodes": []
    },
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
