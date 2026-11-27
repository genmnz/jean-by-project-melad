# 🗄️ Public databases & records

_Search and fetch from NCBI, EMBL-EBI, UCSC, UniProt and more, then hand the record to any tool._

21 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`apply_feature_file`](#apply_feature_file) | Which features from this GTF land on the record, and which do not fit? |
| [`cancel_research_run`](#cancel_research_run) | Which pending hypotheses of a research run should never run? |
| [`confirm_literature_hit`](#confirm_literature_hit) | Has a paper someone read already reported this supported hypothesis? |
| [`fetch_article`](#fetch_article) | Give me this paper's open-access full text. |
| [`fetch_clinvar_vcf`](#fetch_clinvar_vcf) | Which ClinVar records does this release VCF hold in this region? |
| [`fetch_record`](#fetch_record) | Give me this accession's record from the archive named. |
| [`find_accessions`](#find_accessions) | Which archive records does this text name? |
| [`history_protocol`](#history_protocol) | What numbered bench protocol does a construct's build history describe? |
| [`list_databases`](#list_databases) | Which authoritative databases are available, and what does each cover? |
| [`list_research_runs`](#list_research_runs) | Which research runs are there, and what state is each in? |
| [`list_samples`](#list_samples) | Which bundled sample files can a project start from? |
| [`lookup_clinical`](#lookup_clinical) | What does the authority named return for this clinical or translational question? |
| [`lookup_gene`](#lookup_gene) | What does the authority named return for this gene or genomic region? |
| [`lookup_omics`](#lookup_omics) | What does the authority named return for this omics or regulation record? |
| [`lookup_ontology`](#lookup_ontology) | What does the authority named return for this ontology term, pathway or cell type? |
| [`notebook_cross_refs`](#notebook_cross_refs) | Which plasmids, actions and gels does a notebook entry refer to? |
| [`query_database`](#query_database) | What does this authoritative database return for this query? |
| [`research_run_status`](#research_run_status) | What state is a research run in, and what would resuming it do? |
| [`resume_research_run`](#resume_research_run) | What verdicts does a research run reach once its failed, deferred and never-attempted hypotheses have run? |
| [`search_literature`](#search_literature) | What does the authority named return for this literature search? |
| [`search_records`](#search_records) | Which archive records match this text? |

---

### apply_feature_file

**Apply feature file**: _Which features from this GTF land on the open record, and which do not fit?_

Put the features from a GTF in this project onto the open record. A GTF lists features and their positions and carries no sequence, so this is how one reaches a molecule. It REFUSES unless something says the two are in the same coordinate space: if the file names a genome build and the record names the same one it proceeds; if they name different ones it refuses outright; if either is silent it refuses until you pass coordinates_only, which states that you are applying the intervals as positions in this record's own numbering with no genome correspondence checked. Reports what would not fit rather than trimming it.

<sub>returns new records · runs locally on the engine · long-running</sub>

**Assumes:**
- The GTF and the record share a coordinate space: the same genome build, or coordinates_only stated.

**Does not:**
- Refuses on a build mismatch; intervals that fall off the record are reported, not trimmed.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `file` | string |  |  |  | the annotation file in this project, by name. Unset with exactly one present uses it; with several, this refuses and names them rather than picking. |
| `sequence` | string |  |  |  | the seqid within the file whose features to apply (a GTF names one per row). Unset with exactly one present uses it; with several, this refuses and names them — applying the wrong chromosome's intervals is the mistake this parameter exists to prevent. |
| `coordinates_only` | boolean |  | `false` |  | state that you are applying the intervals as COORDINATES — positions in this record’s own numbering — with no genome correspondence checked. Applying coordinates on that basis is a claim about your own data, and the run records it as the basis it used. Required whenever either side is silent about its assembly; it cannot rescue two assemblies that disagree. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the open record with the applied features added |
| `added` | number |  | how many features were written — branch on this rather than counting |
| `basis` | string |  | what earned the apply: 'matched' when both assemblies agreed, 'coordinate-space-only' when you stated it. A run's provenance, not a status |
| `outOfRange` | any |  | the features whose spans run past the end of the record, each with the end it really has. Reported, never trimmed: a span cut to fit is a different feature |
| `duplicate` | number |  | how many were already on the record at the same span, strand and type, so they were not written twice |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "apply_feature_file",
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

### cancel_research_run

**Cancel research run**: _Which pending hypotheses of a research run should never run?_

Withdraw a research run's pending hypotheses (all of them, or the ones named) so no resume runs them, and return the sealed run file. Nothing is deleted: a canceled hypothesis stays registered and still counts in e-BH with e 1, because it was registered before any result and dropping it would raise the others' chance of support after the fact. Answered and settled hypotheses cannot be canceled. To stop a run that is advancing in budgeted slices, stop calling resume_research_run; cancel when the pending hypotheses should never run.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Canceled hypotheses stay in e-BH's count with e 1.

**No scientific claim:** Bookkeeping on a run file; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `run` | object | **yes** |  |  | the run file to cancel pending hypotheses in. |
| `hypotheses` | string[] |  |  |  | the pending hypotheses to cancel, by id; unset cancels every pending one. |
| `reason` | string |  |  |  | why, recorded on each canceled attempt. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `cancelled` | any |  | the hypotheses this call canceled |
| `run` | any |  | the whole program as a sealed jane.research-run file: the ledger, every corpus input pinned by SHA-256, the last attempt at each hypothesis. Pass it back to continue |
| `status` | any |  | the canceled run's status: counts, pending (now none of the canceled), settled and canceled hypotheses |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "cancel_research_run",
  "arguments": {
    "run": {},
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### confirm_literature_hit

**Confirm literature hit**: _Has a paper someone read already reported this supported hypothesis?_

Record that a person read one paper a literature check returned for a supported hypothesis and that it reports the finding: the hypothesis becomes known in the run's ledger, citing that paper, and the run file is sealed again. Only a paper the recorded check returned can be confirmed, so the citation always traces to the query that found it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The caller read the paper and judged that it reports the hypothesis; the engine does not read papers.

**Does not:**
- Confirms only one of the papers the run's own literature check returned (run_discovery_programme with check_literature).

**No scientific claim:** Records a reader's judgement in a run file; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `run` | object | **yes** |  |  | the run file whose literature check returned the paper. |
| `hypothesis` | string | **yes** |  |  | the supported hypothesis the paper reports, by id. |
| `paper` | string | **yes** |  |  | the paper, by its PMID or DOI as the check returned it. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `known` | any |  | the hypothesis's literature record: status known, the citation, and the query and results that found it |
| `run` | any |  | the whole program as a sealed jane.research-run file: the ledger, every corpus input pinned by SHA-256, the last attempt at each hypothesis. Pass it back to continue |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "confirm_literature_hit",
  "arguments": {
    "run": {},
    "hypothesis": "<string>",
    "paper": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### fetch_article

**Fetch article**: _Give me this paper's open-access full text._

Fetch a paper's whole open-access text from Europe PMC by PMCID or PMID: title, authors, journal, license, abstract, every section and every figure caption, as Markdown. This is how a pipeline reads a paper rather than its abstract; pass the Markdown to find_accessions for the records it names. Only Europe PMC's open-access subset is served, and an article outside it is refused with Europe PMC's own reason.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.
- Only Europe PMC's open-access subset has full text; figures are their captions and tables are left out.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `id` | string | **yes** |  |  | the PMCID (PMC13627669) or PMID (39012345) of the paper. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `markdown` | string |  | the whole article as Markdown, figure references linked to their captions |
| `pmcid` | string |  | the PMCID Europe PMC served it under |
| `title` | string |  | the article's title |
| `license` | any |  | the article's own license statement, as the publisher wrote it |
| `endpoints` | any |  | the URLs actually called |
| `retrievedAt` | string |  | when it was fetched |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fetch_article",
  "arguments": {
    "id": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### fetch_clinvar_vcf

**Fetch ClinVar VCF**: _Which ClinVar records does this release VCF hold in this region?_

Read one region of ClinVar's monthly release VCF, as the VCF ClinVar publishes: its header, then every record overlapping the region, through the release's tabix index so only those blocks are fetched. The ID column is the ClinVar Variation ID and INFO carries ClinVar's own CLNSIG, CLNREVSTAT and CLNDN. Use it to put ClinVar's calls for a locus beside your own.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.
- Human only: ClinVar publishes one VCF per assembly, GRCh37 and GRCh38.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `assembly` | `"GRCh38"` · `"GRCh37"` |  | `"GRCh38"` |  | which release VCF to read. |
| `chrom` | string | **yes** |  |  | the chromosome, with or without its chr prefix. |
| `start` | number | **yes** |  | ≥ 1 | first base of the region (1-based). |
| `end` | number | **yes** |  | ≥ 1 | last base of the region (1-based, inclusive). |
| `max_records` | number |  | `1000` | ≥ 1 | cap on records returned; the result says when the region held more. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | which release was read, and how many records the region held |
| `vcf` | string |  | ClinVar's header and the region's records, as the file holds them |
| `records` | number |  | how many records the region returned |
| `truncated` | boolean |  | whether the region held more records than max_records |
| `fileDate` | string |  | the release's own ##fileDate, which names the release read |
| `endpoints` | any |  | the VCF and index URLs actually read |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fetch_clinvar_vcf",
  "arguments": {
    "chrom": "<string>",
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

### fetch_record

**Fetch record**: _Give me this accession's record from the archive named._

Fetch a sequence by accession from an authoritative archive (NCBI Nucleotide or Protein, ENA, UniProtKB, the iGEM Registry, Addgene, or the EBI Dbfetch gateway) and hand it downstream as a real record with its annotations. This is how a pipeline starts from a published sequence rather than from whatever happens to be open.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `accession` | string | **yes** |  |  | the accession to fetch, e.g. NC_005816, U49845, P38398, BBa_R0040. An NCBI accession may carry a window: `NC_005816 REGION: 5000..7000`. |
| `source` | `"ncbi"` · `"ncbi-protein"` · `"ena"` · `"uniprot"` · `"igem"` · `"addgene"` · `"dbfetch"` |  | `"ncbi"` |  | which archive holds it. Values: ncbi (NCBI Nucleotide), ncbi-protein (NCBI Protein), ena (ENA), uniprot (UniProtKB), igem (iGEM Registry), addgene (Addgene), dbfetch (EBI Dbfetch). |
| `db` | string |  |  |  | Dbfetch only: which of its databases. Only applies when source is dbfetch. |
| `format` | string |  |  |  | Dbfetch only: which of that database's formats. Only applies when source is dbfetch. |
| `record_index` | number |  | `0` | ≥ 0 | which record to emit when the fetched file holds several (0-based). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the fetched sequence, ready for a downstream node's $subject |
| `name` | string |  | the record name the archive gave it |
| `length` | number |  | its length in bases (or residues, for a protein) |
| `circular` | boolean |  | whether the archive says it is circular |
| `featureCount` | number |  | how many annotations came with it |
| `provenance` | any |  | the archive, the accession, the URL and when it was fetched — what makes the result re-fetchable |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fetch_record",
  "arguments": {
    "accession": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### find_accessions

**Find accessions**: _Which archive records does this text name?_

Find the sequence accessions a text names (a paper's methods, a notebook, a report) and resolve each against its archive: identifiers.org's own pattern for every namespace a fetch target serves, scanned over the text, then one batched search per archive. A span is listed only when the archive returns a record with that accession, so a catalog number with an accession's shape is reported as unresolved rather than as a hit. Hand `accessions` to fetch_record.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Assumes:**
- identifiers.org's registry pattern, made fit for running text, is what an accession of that namespace looks like.

**Does not:**
- Needs the network: the patterns come from identifiers.org and every candidate is resolved at its archive.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | **yes** |  |  | the text to scan, e.g. the markdown fetch_article returns. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many accessions resolved, at which archives, and how many spans did not |
| `accessions` | any |  | every resolved accession as the text writes it, in text order |
| `found` | any |  | each resolved accession with the record it names (archive, title, organism, length) and how often the text mentions it |
| `unresolved` | any |  | spans a pattern admitted that no archive holds |
| `namespaces` | any |  | the identifiers.org namespaces read, by prefix and registry name |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_accessions",
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

### history_protocol

**History protocol**: _What numbered bench protocol does a construct's build history describe?_

Render a construct's build history into a numbered bench-recipe protocol.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The history's steps are the ones the build actually took.

**Does not:**
- Renders the history; it adds no reaction conditions the history lacks.
- The SpliceCraft vectors it is graded against have no generator in the tree, so they cannot be regenerated.

**Not read from this result:** An export: the recorded steps written out as a bench protocol, with nothing inferred.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `root` | object | **yes** |  |  | a history-node tree. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `protocol` | string |  | numbered bench-recipe protocol text |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "history_protocol",
  "arguments": {
    "root": {},
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### list_databases

**List databases**: _Which authoritative databases are available, and what does each cover?_

The authoritative databases available, with what each one covers, whether it is reachable from the browser, and any license or coverage caveat. Call this before searching if unsure which source answers a question.

<sub>read-only · runs locally on the engine · long-running</sub>

**No scientific claim:** Lists the connectors; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `domain` | `"genomics"` · `"proteins"` · `"chemistry"` · `"clinical"` · `"omics"` · `"cells"` · `"ontology"` · `"literature"` · `"funding"` |  |  |  | restrict to one subject area (all areas when unset). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sources` | any |  | every authority in the requested domain: its id, what it covers, its measured browser transport verdict, and any license or coverage caveat |
| `count` | number |  | how many authorities the filter left |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_databases",
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

### list_research_runs

**List research runs**: _Which research runs are there, and what state is each in?_

List research runs without running anything: the runs this project holds (in the app), or the run files given (`runs`, which is how an HTTP or MCP caller lists the files it kept). For each run: whether its seal holds, its id, how many hypotheses it registered and how many are supported, not supported or without evidence, how many a resume would run, how many inputs it pins, and what resuming would do. A file whose seal fails is listed as refused with the reason, never dropped. Hand one to research_run_status for its decisions, or to resume_research_run.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Lists the files it is given or the project holds; there is no server-side run store, so a stateless door lists only what its caller passes.

**No scientific claim:** Reads sealed run files' bookkeeping; every verdict it reports was computed by run_discovery_programme.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `runs` | object[] |  |  |  | the run files to list; in the app, left unset, the research runs this project holds. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `runs` | any |  | one row per run whose seal holds: id, hypotheses, supported, not supported, without evidence, pending, settled, canceled, inputs pinned and the next action |
| `refused` | any |  | each file whose seal failed, by position, with the reason |
| `count` | number |  | how many runs opened under their seal |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_research_runs",
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

### list_samples

**List samples**: _Which bundled sample files can a project start from?_

Browse the bundled sample library: the real bio files a new project can start from (GenBank and SnapGene plasmids, FASTA sets, alignments, Sanger traces, structures, variant calls and more), each with its id, format and size, and its archive provenance where the corpus records one. This is the headless form of starting a project from a sample: pass an id as a `_subject` or `_files` entry's `sample` and the file is read exactly as the lobby opens it.

<sub>read-only · runs locally on the engine · long-running</sub>

**No scientific claim:** Lists the bundled sample library; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `query` | string |  |  |  | words that must all appear in the sample’s id, name, category or format label (case-insensitive), e.g. "pUC", "genbank plasmid", "ab1". Empty lists everything. |
| `kind` | string |  |  |  | restrict to one importer kind (sequence, msa, trace, structure, variants, alignment, tabular, …). Each entry reports its own, so the vocabulary is whatever the library holds. |
| `limit` | number |  | `50` | 1–1000 | most entries to return; `total` says how many matched. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `samples` | any |  | the matching entries: id, name, category, format, label, kind, size and provenance when recorded |
| `ids` | any |  | just the ids, in the same order — the list to scatter a per-sample step over |
| `total` | number |  | how many entries matched before `limit` was applied |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_samples",
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

### lookup_clinical

**Lookup clinical**: _What does the authority named return for this clinical or translational question?_

Look up clinical and translational evidence: ClinicalTrials.gov trials, FDA labels and adverse events, Open Targets associations, CIViC cancer variant evidence, ClinGen curation, cBioPortal cohorts, or DepMap dependencies.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"clinicaltrials"` · `"openfda"` · `"opentargets"` · `"civic"` · `"clingen"` · `"cosmic"` · `"cbioportal"` · `"depmap"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | a drug, gene, disease or trial id, or a command such as "clingen_gene_validity:BRCA2". |
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
  "name": "lookup_clinical",
  "arguments": {
    "source": "clinicaltrials",
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

### lookup_gene

**Lookup gene**: _What does the authority named return for this gene or genomic region?_

Look up a gene or genomic region: NCBI Gene records, HGNC nomenclature, Ensembl records, cross-references, MyGene identifiers, UCSC assembly data, GTEx expression, or BioMart tables.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"ncbi-gene"` · `"hgnc"` · `"ensembl"` · `"mygene"` · `"ucsc"` · `"gtex"` · `"biomart"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | a gene symbol or identifier (e.g. "BRCA2"), or a command such as "ensembl_lookup:BRCA2" or "ensembl_xrefs:ENSG00000139618". |
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
  "name": "lookup_gene",
  "arguments": {
    "source": "ncbi-gene",
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

### lookup_omics

**Lookup omics**: _What does the authority named return for this omics or regulation record?_

Look up omics and regulation records: GEO and ArrayExpress experiments, PRIDE proteomics, MetaboLights, MGnify, ENCODE experiments and files, JASPAR motifs, or UniBind TF binding sites.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"geo"` · `"arrayexpress"` · `"pride"` · `"metabolights"` · `"mgnify"` · `"encode"` · `"jaspar"` · `"unibind"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | an accession or search term, or a command such as "geo_get_series:GSE12345" or "encode_get_file:ENCFF002JUR". |
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
  "name": "lookup_omics",
  "arguments": {
    "source": "geo",
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

### lookup_ontology

**Lookup ontology**: _What does the authority named return for this ontology term, pathway or cell type?_

Resolve an ontology term, taxon, pathway or cell type: OLS ontologies, NCBI Taxonomy, QuickGO annotations, Reactome pathways, KEGG entries, Rfam RNA families, CellGuide/PanglaoDB cell types and markers, an antibody RRID, or an identifiers.org prefix and the pattern its ids follow.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"ols"` · `"ncbi-taxonomy"` · `"quickgo"` · `"reactome"` · `"kegg"` · `"rfam"` · `"cellguide"` · `"panglaodb"` · `"antibodyregistry"` · `"identifiers-org"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | a term, accession or command such as "get_go_annotations:P04637" or "map_reactome_pathways:TP53". |
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
  "name": "lookup_ontology",
  "arguments": {
    "source": "ols",
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

### notebook_cross_refs

**Notebook cross refs**: _Which plasmids, actions and gels does a notebook entry refer to?_

Extract @plasmid / !action / &gel cross-references from a lab-notebook markdown body.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- References use SpliceCraft's @, ! and & markers.

**Does not:**
- Finds the markers; it does not check that what they name exists.

**Not read from this result:** A lookup of the notebook's own links between entries and records, listed as stored; nothing is inferred.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `body_md` | string | **yes** |  |  | the notebook entry body (markdown). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `plasmids` | any |  | @plasmid references |
| `actions` | any |  | !action references |
| `gels` | any |  | &gel references |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "notebook_cross_refs",
  "arguments": {
    "body_md": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### query_database

**Query database**: _What does this authoritative database return for this query?_

Ask one of the ~60 authoritative databases a question and hand its rows downstream — Ensembl, UniProt, ClinVar, gnomAD, ChEMBL, PubChem, InterPro, STRING, PDB, AlphaFold, the GWAS Catalog, PubMed and the rest. Nothing here computes science: a connector returns what the authority already published, which is the rule that an authoritative registry outranks anything kept locally.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `authority` | `"pubmed"` · `"pmc-idconv"` · `"europepmc"` · `"openalex"` · `"crossref"` · `"arxiv"` · `"biorxiv"` · `"medrxiv"` · `"datacite"` · `"ensembl"` · `"ucsc"` · `"biomart"` · `"mygene"` · `"ncbi-gene"` · `"hgnc"` · `"gnomad"` · `"clinvar"` · `"dbsnp"` · `"variation"` · `"cadd"` · `"gtex"` · `"eqtlcatalogue"` · `"gwascatalog"` · `"pheweb"` · `"uniprot"` · `"interpro"` · `"string"` · `"proteinatlas"` · `"alphafold"` · `"pdb"` · `"emdb"` · `"complexportal"` · `"intact"` · `"chembl"` · `"pubchem"` · `"chebi"` · `"bindingdb"` · `"zinc"` · `"rhea"` · `"clinicaltrials"` · `"openfda"` · `"opentargets"` · `"civic"` · `"clingen"` · `"cosmic"` · `"depmap"` · `"cbioportal"` · `"geo"` · `"arrayexpress"` · `"pride"` · `"metabolights"` · `"mgnify"` · `"encode"` · `"jaspar"` · `"unibind"` · `"cellguide"` · `"panglaodb"` · `"antibodyregistry"` · `"ols"` · `"quickgo"` · `"identifiers-org"` · `"ncbi-taxonomy"` · `"reactome"` · `"kegg"` · `"rfam"` · `"grantsgov"` | **yes** |  |  | which database to ask. Values: pubmed (NCBI PubMed (E-utilities) — literature), pmc-idconv (NCBI PMC ID Converter — literature), europepmc (Europe PMC — literature), openalex (OpenAlex — literature), crossref (Crossref — literature), arxiv (arXiv — literature), biorxiv (bioRxiv — literature), medrxiv (medRxiv — literature), datacite (DataCite — literature), ensembl (Ensembl REST — genomics), ucsc (UCSC Genome Browser API — genomics), biomart (Ensembl BioMart — genomics), mygene (MyGene.info — genomics), ncbi-gene (NCBI Gene (E-utilities) — genomics), hgnc (HGNC (genenames.org) — genomics), gnomad (gnomAD (Broad) — genomics), clinvar (NCBI ClinVar — genomics), dbsnp (NCBI dbSNP — genomics), variation (NCBI Variation Services — genomics), cadd (CADD (Kircher lab) — genomics), gtex (GTEx Portal — genomics), eqtlcatalogue (eQTL Catalogue (EBI) — genomics), gwascatalog (GWAS Catalog (EBI/NHGRI) — genomics), pheweb (PheWeb / FinnGen — genomics), uniprot (UniProt — proteins), interpro (InterPro / Pfam (EBI) — proteins), string (STRING — proteins), proteinatlas (Human Protein Atlas — proteins), alphafold (AlphaFold DB (EBI) — proteins), pdb (RCSB PDB — proteins), emdb (EMDB (EBI) — proteins), complexportal (Complex Portal (EBI) — proteins), intact (IntAct (EBI) — proteins), chembl (ChEMBL (EBI) — chemistry), pubchem (PubChem (NCBI) — chemistry), chebi (ChEBI (EBI) — chemistry), bindingdb (BindingDB — chemistry), zinc (ZINC (CartBlanche, UCSF) — chemistry), rhea (Rhea (EBI) — chemistry), clinicaltrials (ClinicalTrials.gov — clinical), openfda (openFDA — clinical), opentargets (Open Targets Platform — clinical), civic (CIViC — clinical), clingen (ClinGen (erepo.genome.network) — clinical), cosmic (COSMIC via NLM Clinical Tables — clinical), depmap (Cell Model Passports (Sanger) — clinical), cbioportal (cBioPortal — clinical), geo (NCBI GEO — omics), arrayexpress (ArrayExpress / BioStudies (EBI) — omics), pride (PRIDE (EBI) — omics), metabolights (MetaboLights (EBI) — omics), mgnify (MGnify (EBI) — omics), encode (ENCODE Project — omics), jaspar (JASPAR (Elixir) — omics), unibind (UniBind (Univ. of Oslo) — omics), cellguide (CellGuide (CZI CELLxGENE) — cells), panglaodb (PanglaoDB — cells), antibodyregistry (Antibody Registry (RRID) — cells), ols (OLS4 (EBI) — ontology), quickgo (QuickGO (EBI) — ontology), identifiers-org (identifiers.org registry — ontology), ncbi-taxonomy (NCBI Taxonomy (E-utilities) — ontology), reactome (Reactome — ontology), kegg (KEGG — ontology), rfam (Rfam (EBI) — ontology), grantsgov (Grants.gov — funding). |
| `query` | string | **yes** |  |  | what to ask, in the authority's own terms — an identifier, a gene symbol, or one of its command forms such as `ensembl_lookup:BRCA2`. |
| `limit` | number |  | `10` | ≥ 1 | cap on rows returned, where the authority honours one. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `results` | any |  | the rows the authority returned — wire into filter_items, check_rows or summarize_rows |
| `count` | number |  | how many rows came back |
| `authority` | string |  | which authority answered, stated rather than implied |
| `endpoints` | any |  | the URLs actually called — the provenance a methods section needs |
| `retrievedAt` | string |  | when it was fetched, because a live lookup is a fact about a moment |
| `envelope` | any |  | the whole response, for a row shape this node's `results` does not name |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "query_database",
  "arguments": {
    "authority": "pubmed",
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

### research_run_status

**Research run status**: _What state is a research run in, and what would resuming it do?_

Read a research run file without running anything: whether its seal holds (an edited or truncated file is refused), every hypothesis's verdict and the rule its evidence was merged by, which hypotheses a resume would run (no evidence, and the last attempt failed or was deferred by a call's budget) and which are settled or canceled, and what resuming would do. Given the corpus, also reports every pinned input whose content changed under the same name, which a resume refuses.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Reads the file; runs nothing.

**No scientific claim:** Reads a sealed run file's bookkeeping; every verdict it reports was computed by run_discovery_programme.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `run` | object | **yes** |  |  | the run file run_discovery_programme or resume_research_run returned. |
| `sequences` | string[] |  |  |  | optionally, the corpus as it is now, to check against the run's pinned inputs. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `status` | any |  | id, hypothesis counts by verdict, pending and settled hypotheses, and the next action |
| `pending` | any |  | hypotheses a resume would run |
| `decisions` | any |  | every hypothesis's verdict, merged e-value, tests and merge rule |
| `drift` | any |  | pinned inputs whose content changed, when a corpus was given; null when none was |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "research_run_status",
  "arguments": {
    "run": {},
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### resume_research_run

**Resume research run**: _What verdicts does a research run reach once its failed, deferred and never-attempted hypotheses have run?_

Continue a research run from its file after an interruption or a failed test: the seal is checked, every pinned input the corpus still holds must have the content it had (a changed file is refused by name), and only the hypotheses with no evidence whose last attempt failed or was deferred are run, each with the settings it was registered with. Answered, settled and canceled hypotheses are never run again, so a resumed run reaches the verdicts an uninterrupted one would. With budget_seconds, a long run continues in slices: call again with the returned file until nothing is pending. Returns the updated run file with the same outputs as run_discovery_programme.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The corpus still holds every pinned input with the content it had.

**Does not:**
- A changed input is refused by name rather than rerun.

**No scientific claim:** Re-runs the registered tests unchanged; the science is run_discovery_programme's and the tests', each graded on its own.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `run` | object | **yes** |  |  | the run file to continue. |
| `sequences` | string[] |  |  |  | the corpus the run was registered over: library document or file names, or wired records. |
| `budget_seconds` | number |  |  | ≥ 0 | seconds this call may spend running tests: whole tests run until the budget is spent and the rest are deferred, so a long program returns before a client's timeout and resume_research_run continues it. A test is never cut short and at least one runs per call. Unset: every test runs in this call. In s. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `decisions` | any |  | every hypothesis: verdict, merged e-value, tests and merge rule |
| `resumed` | any |  | the hypotheses this call ran |
| `run` | any |  | the whole program as a sealed jane.research-run file: the ledger, every corpus input pinned by SHA-256, the last attempt at each hypothesis. Pass it back to continue |
| `report` | any |  | the resume as text lines: what ran, what was refused, the verdicts |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "resume_research_run",
  "arguments": {
    "run": {},
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### search_literature

**Search literature**: _What does the authority named return for this literature search?_

Search the published literature: PubMed, Europe PMC (including open-access full-text sections), OpenAlex, Crossref, arXiv, bioRxiv/medRxiv preprints or DataCite datasets.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"pubmed"` · `"europepmc"` · `"openalex"` · `"crossref"` · `"arxiv"` · `"biorxiv"` · `"medrxiv"` · `"datacite"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | search terms, or a command such as "pmid:35486828", "fulltext:PMC9046468" or "openalex_search_works:CRISPR". |
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
  "name": "search_literature",
  "arguments": {
    "source": "pubmed",
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

### search_records

**Search records**: _Which archive records match this text?_

Search the sequence archives by free text (a gene name, a protein, an organism, a phrase) across NCBI Nucleotide and Protein, ENA (plain records, WGS and TSA/TLS assembly sets, and annotated coding/non-coding features), UniProtKB and the iGEM Registry at once, and hand back the matching accessions. This is the half of Fetch from database that answers "which record do I want?"; fetch_record answers "give me that one". A source that is down does not fail the search: its error comes back beside the hits the others returned.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network; a source that is down is reported beside the others' hits.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `query` | string | **yes** |  |  | the words to search for. Archive query syntax is accepted where the archive accepts it, but plain words are the normal case: "beta-lactamase Escherichia coli", "GFP", "pUC19". |
| `sources` | (`"ncbi"` · `"ena"` · `"ena-wgs"` · `"ena-tsa"` · `"ena-feature"` · `"igem"` · `"ncbi-protein"` · `"uniprot"`)[] |  | `["ncbi", "ena"]` |  | which archives to ask. Each is searched independently and the hits are interleaved, so asking more costs time rather than accuracy. Defaults to the nucleotide pair the panel opens on. |
| `limit` | number |  | `20` | 1–100 | how many hits to ask each source for. The panel pages at this size, and every source is asked for the same number. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `accession` | string |  | the top hit's accession, ready for a fetch_record node's $accession. This is the seam between searching and fetching |
| `source` | string |  | which archive the top hit came from, ready for the same node's $source where the two vocabularies agree |
| `hitCount` | number |  | how many records came back across every source asked |
| `accessions` | string |  | every hit’s accession, newline-separated, in the order they are ranked |
| `hits` | any |  | the full result rows: accession, title, source, organism, length, molecule kind and the archive’s own reported fields |
| `unavailable` | any |  | the sources that could not answer, each with the reason: empty when every source answered. A search is not a failure because one archive is down, and hiding that would make a short list read as a small literature |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "search_records",
  "arguments": {
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
