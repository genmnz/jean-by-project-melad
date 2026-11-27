# 🖥️ Workbench state

_Tools that read or write the open project inside the Jean workbench. Over this stateless endpoint there is no open project, so they matter only to the in-app assistant._

12 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`add_notebook_figure`](#add_notebook_figure) | Add this drawing to the lab notebook as a figure. |
| [`check_value`](#check_value) | Does this value meet its threshold, and should the pipeline continue? |
| [`describe_project`](#describe_project) | What files does this project hold, what does each carry, and which tool reads it? |
| [`get_open_record`](#get_open_record) | Which record is open in the editor? |
| [`get_selection`](#get_selection) | What is the region selected on the canvas, as a record? |
| [`list_experiments`](#list_experiments) | Which lab-notebook entries match this search, newest first? |
| [`list_library`](#list_library) | Which sequence documents does the project hold? |
| [`list_traces`](#list_traces) | Which Sanger trace files does this project hold? |
| [`load_record`](#load_record) | What does a named project document hold, as a record? |
| [`pick_first`](#pick_first) | Which branch of a conditional pipeline actually ran? |
| [`plan_next_tools`](#plan_next_tools) | Which tools can run on what this run produced, what would each add, and what is the shortest chain to the output I want? |
| [`record_experiment`](#record_experiment) | Write this text into the lab notebook. |

---

### add_notebook_figure

**Add notebook figure**: _Add this drawing to the lab notebook as a figure._

Put a drawing that is on screen into the lab notebook as a numbered figure: a chart, gel, map or any other picture a tool drew on the stage. It is appended to the entry the user has open (or to the one you name), captioned with the drawing, the tool that drew it and what that tool concludes now, and numbered where it falls, exactly as the Export panel and a chart's own menu do it. Vector drawings stay vector.

<sub>returns new records · runs locally on the engine · long-running</sub>

**Assumes:**
- The drawing is on screen: a figure is taken from the live picture.

**Does not:**
- Writes to the notebook held in this browser.

**No scientific claim:** Stores a picture the app already drew; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `drawing` | string |  |  |  | the drawing to take, by its name (a chart's title, e.g. "Melt curve"). Leave it out to take the first drawing of the tab. |
| `tab` | string |  |  |  | the stage tab or the tool surface id it shows (e.g. `qpcr-curves`). Leave it out for the tab the user is looking at. |
| `entry_id` | string |  |  |  | append to this entry instead of the open one; with neither, a new entry is started and named after the drawing. |
| `caption` | string |  |  |  | a caption to use instead of the generated one. Leave it out unless the user asked for wording: the generated caption names the drawing, the tool and its reading. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `entry_id` | string |  | the entry the figure went into |
| `figure` | number |  | its figure number in that entry, as the preview and every export print it |
| `caption` | string |  | the caption written |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "add_notebook_figure",
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

### check_value

**Check value**: _Does this value meet its threshold, and should the pipeline continue?_

A QC gate. Compares a wired value against a threshold and PASSES or FAILS the pipeline there — every node downstream of a failed gate is skipped, so a run stops at the first check that does not hold. This is how a pipeline expresses 'only continue if the clone is right'.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The threshold given is the real acceptance criterion.

**Does not:**
- Compares one value; a table needs check_rows.

**No scientific claim:** Compares a value with a threshold and stops the run; the science is in whatever produced the value.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `value` | number | **yes** |  |  | the value to check — wire a number (cut count, product size, tip count, Tm) or any output; a list is compared by its length. |
| `operator` | `"=="` · `"!="` · `">"` · `">="` · `"<"` · `"<="` · `"between"` · `"in"` · `"not_in"` · `"contains"` · `"is_true"` · `"not_empty"` |  | `">="` |  | how to compare. Values: == (equals), != (does not equal), > (greater than), >= (at least), < (less than), <= (at most), between (between (inclusive)), in (is one of), not_in (is none of), contains (contains text), is_true (is true), not_empty (is not empty). |
| `threshold` | number |  |  |  | the value to compare against. Leave it unset and wire `against` instead to compare two steps. Only applies when operator is == or != or > or >= or < or <=. |
| `against` | number |  |  |  | optional: compare against another step's value instead of the fixed threshold. When wired, this wins over `threshold`. Only applies when operator is == or != or > or >= or < or <=. |
| `against_factor` | number |  | `1` |  | multiply the compared-against value by this first, so `at least twice the smallest band` is one gate rather than an arithmetic step. Only applies when operator is == or != or > or >= or < or <=. |
| `against_offset` | number |  | `0` |  | then add this, so `within 50 bp of the predicted size` is expressible against a computed value. Only applies when operator is == or != or > or >= or < or <=. |
| `min` | number |  |  |  | lower bound, inclusive. Only applies when operator is between. |
| `max` | number |  |  |  | upper bound, inclusive. Only applies when operator is between. |
| `set` | string[] |  |  |  | the values the checked value must be one of (or none of), compared as text, so `1` matches 1. Only applies when operator is in or not_in. |
| `text` | string |  |  |  | the text the value must contain. Only applies when operator is contains. |
| `label` | string |  |  |  | what this gate is checking, in your words — it becomes the message when the gate fails (e.g. 'single EcoRI site'). |
| `report_only` | boolean |  | `false` |  | report the verdict instead of stopping the run: wire `passed` (or `failed`) into another step's condition to choose a branch. |
| `record` | string |  |  |  | optional: the record this gate is guarding. It comes straight back out of the `record` output when the check passes, so the gate sits in the middle of a chain. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `passed` | boolean |  | whether the check held. As a gate this is true whenever it is read downstream, since a failure stops the run; with `report_only` on it is the real verdict, for driving a branch |
| `failed` | boolean |  | the opposite verdict, so the ELSE arm of a branch needs no extra step. Only meaningful with `report_only` on |
| `record` | object or null |  | the guarded record, unchanged — wire it into the next node's $subject to make that step conditional on this check |
| `value` | any |  | the value that was checked, passed straight through so the gate can sit mid-chain |
| `message` | string |  | what was compared, in words |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_value",
  "arguments": {
    "value": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### describe_project

**Describe project**: _What files does this project hold, what does each carry, and which tool reads it?_

Describe the project the way the copilot is told about it: every file, what it carries and which tool reads it, which files are indexed or paired with each other, the codon-usage tables a tool resolves by name, and each small text file (4 KB or less) attached whole. Over the API or MCP it describes the files sent as _files; in the app it describes the open project and adds the readings the panels and open documents produced.

<sub>read-only · runs locally on the engine · long-running</sub>

**Does not:**
- Describes what the importer read from each file; a file it could not read is listed with its reason, not described.

**No scientific claim:** Describes the project's files as the copilot is told about them; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `title` | string |  |  |  | the project's name, for the header line when the files were sent with the call. In the app the open project's own title is used. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `text` | string |  | the project section (and, in the app, the readings section) exactly as the copilot receives it, one line per fact |
| `files` | number |  | how many files it describes |
| `unread` | any |  | files sent with the call that the importer could not read, each with its reason. They are not in the project, exactly as a file the app refuses at import is not |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "describe_project",
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

### get_open_record

**Get open record**: _Which record is open in the editor?_

Return the plasmid/sequence currently open in the editor. Emits it as a `record`, so it is the SOURCE node of a pipeline — wire its record into any downstream node's $subject.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Reads the editor's state; with nothing open there is no record.

**No scientific claim:** Hands on the open record unchanged; it computes nothing.

**Arguments**

_No arguments beyond the shared `_subject` and `_files`._

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the open sequence record (subject for downstream nodes) |
| `sequence` | string |  | the sequence 5'→3' |
| `length` | number | bp | length in bp |
| `name` | string |  | record name |
| `circular` | boolean |  | topology (true = circular) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "get_open_record",
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

### get_selection

**Get selection**: _What is the region selected on the canvas, as a record?_

The region selected on the canvas, as its own record. This is what makes a highlighted stretch a pipeline INPUT: wire its record into any node's subject and that step runs on the selection rather than on the whole molecule.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Reads the selection; with none there is no record.

**No scientific claim:** Hands on the selected region unchanged.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `reverse_complement` | boolean |  | `false` |  | emit the bottom strand of the selection (what a feature on the minus strand actually reads). |
| `pad` | number |  | `0` | 0–10000 | extend the selection by this many bases on each side, clamped to the molecule (or wrapped, on a circular one). In bp. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the selected region as a linear record (subject for downstream nodes) |
| `sequence` | string |  | the selected bases 5'→3' |
| `start` | number |  | 0-based start on the parent molecule |
| `end` | number |  | end on the parent, exclusive |
| `length` | number | bp | length in bp |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "get_selection",
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

### list_experiments

**List experiments**: _Which lab-notebook entries match this search, newest first?_

Your lab-notebook entries, newest first — id, title, tags, collection, when they changed, and the @plasmid / !action / &gel cross-references each one names. Filter by a tag, by collection, or by text in the title and body, so a run can find the entry it is continuing instead of starting a second one about the same experiment.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Only the notebook held in this browser.

**No scientific claim:** Lists the user's own notebook entries; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `search` | string |  |  |  | match on title or body text, case-insensitively. Left unset, every entry is listed. |
| `tag` | string |  |  |  | only entries carrying this tag. |
| `collection` | string |  |  |  | only entries filed in this collection. |
| `limit` | number |  | `20` | 1–200 | how many entries to return, newest first. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `entries` | any |  | the matching entries: id, title, tags, collection, created_at, updated_at, the three cross-reference lists and the body length. The BODY itself is not here — a notebook is long and a listing is for finding, so read one with the id this gives you |
| `count` | number |  | how many matched — branch on this rather than counting the array |
| `total` | number |  | how many entries the notebook holds in all, so a filter that matched nothing can say whether the notebook is empty or the filter was wrong |
| `collections` | any |  | every collection you have, with how many entries it holds |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_experiments",
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

### list_library

**List library**: _Which sequence documents does the project hold?_

List the project's sequence documents (id, name, length, topology, kind).

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Lists names and lengths; it opens nothing.

**No scientific claim:** Lists the project's documents; it computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `kind` | `"plasmid"` · `"fragment"` · `"amplicon"` · `"protein"` |  |  |  | restrict to one document kind (all kinds when unset). Kind is derived from the record itself — `amplicon` is provenance, not a file property, so documents read from disk are never classified as one. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `items` | any |  | the library entries |
| `count` | number |  | number of entries |
| `ids` | any |  | just the entry ids, in the same order — the list to scatter a per-document step over |
| `names` | any |  | just the entry names, in the same order |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_library",
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

### list_traces

**List traces**: _Which Sanger trace files does this project hold?_

List the Sanger trace files in this project (.ab1 / .abi / .scf / .ztr) — the list a batch runs over. Wire its `names` into a trace reader's For-each so every read in the project is processed in one pipeline, instead of one node per read.

<sub>read-only · runs locally on the engine · long-running</sub>

**No scientific claim:** Lists the project's trace files; computes nothing.

**Arguments**

_No arguments beyond the shared `_subject` and `_files`._

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `names` | any |  | the trace file names, in project order — the list to scatter a trace reader over |
| `ids` | any |  | their project file ids, in the same order (unambiguous where two names match) |
| `count` | number |  | how many traces that is |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "list_traces",
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

### load_record

**Load record**: _What does a named project document hold, as a record?_

Read a CHOSEN project document as a record — the pipeline's data-reader source, for running on a specific file instead of whatever happens to be open in the editor. Wire its `record` into any downstream node's $subject.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Reads the stored document; it does not check it.

**No scientific claim:** Reads a stored document unchanged; it computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `document` | string | **yes** |  |  | the project document to read — its id, or its exact name (`list_library` lists them). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the chosen document as a record (subject for downstream nodes) |
| `sequence` | string |  | the sequence 5'→3' |
| `length` | number | bp | length in bp |
| `name` | string |  | document name |
| `circular` | boolean |  | topology (true = circular) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "load_record",
  "arguments": {
    "document": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### pick_first

**Pick first**: _Which branch of a conditional pipeline actually ran?_

Rejoin two branches: takes the outputs of several conditional steps and emits the first one that actually ran. This is how a two-way branch comes back together: wire both arms in, and whichever arm ran is what continues.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Emits the first arm that ran; it does not compare the arms.

**No scientific claim:** Rejoins branches of a pipeline; it computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `values` | string[] |  |  |  | the branches to choose between, in preference order. Wire one output from each arm. |
| `fallback` | string |  |  |  | what to emit when NO branch ran. Leave empty to make that an error instead, which is usually what you want, because silently continuing with nothing is how a pipeline reports a result it never computed. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `value` | any |  | the first branch that produced anything |
| `record` | object or null |  | the same value when it is a record, so it can drive a downstream $subject |
| `index` | number |  | which branch it came from (0 = the first wired) |
| `ranCount` | number |  | how many branches produced anything. More than 1 means the conditions were not exclusive |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "pick_first",
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

### plan_next_tools

**Plan next tools**: _Which tools can run on what this run produced, what would each add, and what is the shortest chain to the output I want?_

What can run next, and what each next step would add. Give it a tool whose run just finished (or the output types in hand) and it returns the tools whose own declared inputs those outputs fill, each with the parameter the wire lands on, the question that tool answers, its limits, what grades it, whether it is seeded, asynchronous, writing or leaving the machine, and which of its DECLARED data files the run in hand already read, so a step that would re-read the same table can be told apart. Few tools declare the data they read, so an empty list is no claim that a step brings independent evidence. Ask for a `target_type` and it returns the shortest chains of tools that reach it. The hand-offs are the workflow builder's own port graph, so a step it names is a wire the builder would draw.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- A hand-off is a declared domain-typed output meeting a declared input of the same type — the builder's own rule.
- What a candidate claims and reads is its own declared contract.

**Does not:**
- Only declared types: a tool whose parameter is untyped `json` accepts anything by the builder's rule, so those are listed apart and the type proves nothing about the hand-off.
- It ranks nothing: scientific usefulness is not a property of the graph, so the contract fields are reported for the caller to weigh.
- Shared evidence is shared data FILES, not shared assumptions.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `after` | string |  |  |  | the tool whose run just finished — its declared outputs are what is in hand. Leave unset and give `output_types` instead. |
| `output_types` | string[] |  |  |  | the port types in hand, when no single tool produced them (`sequence`, `record`, `bands`, `sites`, `protocol`, `matrix`, `series`). |
| `target_type` | string |  |  |  | optional: the output type you want to reach. Returns the shortest chains of tools that get there. |
| `max_steps` | number |  | `3` | 1–6 | longest chain to consider when a `target_type` is given. |
| `read_only` | boolean |  | `false` |  | keep only steps that write nothing. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `count` | number |  | how many tools can consume these outputs by their declared types |
| `tools` | any |  | the candidates, in catalog order: the parameter each wire lands on, the question that tool answers, its limits, what grades it, and what it reads |
| `untyped` | any |  | tools declaring an untyped parameter the builder would let this be wired into — a wire the graph cannot vouch for |
| `paths` | any |  | the shortest chains of tools reaching `target_type`, when one was asked for |
| `outputs` | any |  | the types the walk started from |
| `message` | string |  | what was walked, in words |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "plan_next_tools",
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

### record_experiment

**Record experiment**: _Write this text into the lab notebook._

Write what just happened into your lab notebook: a new entry, or more text appended to one you name. The body is markdown and its @plasmid / !action / &gel references are extracted as you write, so an entry made by a run is cross-linked exactly like one you typed — and carries the `automated` tag, so you can always tell which is which. Use it to end a pipeline with a record of itself instead of a reminder to write one.

<sub>returns new records · runs locally on the engine · long-running</sub>

**Does not:**
- Writes to the notebook held in this browser.

**No scientific claim:** Stores the user's text; computes nothing.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `title` | string |  |  |  | the entry title. A new entry needs one. On an append, giving a title RENAMES the experiment, so leave it out to keep the name it has. |
| `body_md` | string | **yes** |  |  | the entry body, markdown. `@plasmid-name`, `!action-id` and `&gel-id` references in it are extracted into the entry's cross-reference lists, which is what makes a notebook searchable by construct. |
| `entry_id` | string |  |  |  | append to this entry instead of creating one — the id `list_experiments` returns. A pipeline that runs twice should append to its own entry rather than leaving two. |
| `tags` | string[] |  |  |  | tags to file it under, beyond the `automated` tag every entry written here carries. |
| `collection` | string |  |  |  | file it in this collection, creating the collection if it does not exist — the notebook's own grouping, the same one the panel lists. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `entry_id` | string |  | the entry written — pass it back to append to this same experiment next time |
| `created` | boolean |  | true for a new entry, false when text was appended to an existing one |
| `title` | string |  | the title it now carries |
| `tags` | any |  | the tags as stored, including `automated` — the engine caps and cleans these, so read them back rather than assuming |
| `crossRefs` | any |  | the @plasmid / !action / &gel references the engine extracted from the body — empty lists are a real answer and mean the body named no construct, which is worth noticing in an entry about one |
| `collection` | string |  | the collection it is filed in, or an empty string when it is filed in none |
| `unresolved` | any |  | `{ references, citations }`: every `@` / `!` / `&` reference in the stored body that names nothing in this workspace, as written, and every citation key that is not a DOI, PMID or PMCID. Empty lists mean every reference resolves; fix and append when they are not. Null when the write ran without the check (a blocking workflow run) |
| `bodyChars` | number |  | the stored body length. The engine caps a body at 1,000,000 bytes, so a long append can be shorter here than what was sent — read it rather than assuming the write was whole |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "record_experiment",
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
