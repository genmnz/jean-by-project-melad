# Calling Jean over MCP

How a client talks to the Jean server: the endpoint, the handshake, the arguments every tool
shares, the shape of a result, and how errors look. The per-tool arguments and outputs are in the
[tool reference](tools/README.md).

Blocks between `<!-- … -->` markers are written by `scripts/catalogue.py` from the live server.
The rest is prose, and every example below is a real exchange with the server.

## Contents

- [Endpoint and transport](#endpoint-and-transport)
- [The server](#the-server)
- [The server's own instructions](#the-servers-own-instructions)
- [A raw session with curl](#a-raw-session-with-curl)
- [Naming the molecule: `_subject`](#naming-the-molecule-_subject)
- [More records: `_files`](#more-records-_files)
- [What a result contains](#what-a-result-contains)
- [Errors and refusals](#errors-and-refusals)
- [Tool metadata](#tool-metadata)
- [Full descriptions: `describe_tools`](#full-descriptions-describe_tools)
- [Long answers: `read_answer_window`](#long-answers-read_answer_window)
- [Workflows: one call, many tools](#workflows-one-call-many-tools)

## Endpoint and transport

| | |
|---|---|
| URL | `https://jeanpm.vercel.app/mcp` |
| Transport | [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#streamable-http): JSON-RPC 2.0 requests sent by `POST` |
| Request headers | `content-type: application/json` and `accept: application/json, text/event-stream` |
| Response | an event stream; the JSON-RPC reply is the `data:` line |
| Authentication | none |
| State | none. Nothing is kept between calls, so every call carries its own data |

The old address `https://jeanslabs.vercel.app/mcp` answers with a `308` redirect to the URL above.
Clients that follow redirects keep working, but some HTTP libraries (Python's `urllib`, for one)
do not follow a `308` on a `POST`. Configure the URL above.

## The server

The `initialize` handshake reports:

<!-- SERVER:START -->
| | |
|---|---|
| Name | `jane-engine` |
| Title | Jean — Molecular Biology & Genomics |
| Version | `2.0.0` |
| Protocol version | `2025-06-18` |
| Capabilities | `tools` (listChanged), `resources` (listChanged) |
| Resource | `ui://jane/result.html` (text/html;profile=mcp-app) |
<!-- SERVER:END -->

The resource is the HTML view that clients supporting
[MCP Apps](https://modelcontextprotocol.io/extensions/apps) open for a result. Each tool points
to it in `_meta.ui.resourceUri`.

## The server's own instructions

The server sends these instructions to every client at `initialize`. They are the shortest
statement of the calling contract, quoted exactly:

<!-- INSTRUCTIONS:START -->
> Golden-validated life-science tools: cloning and assembly simulation, primer and CRISPR guide design, sequence and protein analysis, Sanger traces, variant and copy-number calls, qPCR, flow cytometry, antibodies, population genetics and phylogenetics.
>
> This server holds no project. Name the molecule to act on as `_subject`, by exactly one of: `sequence` (the bases), `accession` (+ `source`; `search_records` finds one), `sample` (a bundled file; `list_samples` lists them) or `file` ({name, text} or {name, base64}). A tool that needs one and is not given it refuses by name rather than guessing.
>
> Pass further files as `_files` (a list of the same references): their records become the library documents a tool's `sequences`/`parts`/`document` arguments name, and `list_library` shows what they held. A file holding several records sent as `_subject` is refused with the list, so you choose one by `record_index`.
>
> Results carry `structuredContent` matching each tool's `outputSchema`. Numbers come from the engine; none are estimated here.
>
> Each tool description here is its opening sentences; `describe_tools` returns the full text for the tools you name.
>
> Figures (plasmid maps, gels, trees, chromatograms, alignment blocks, and every profile, curve, histogram and heatmap a tool declares) arrive as PNG images beside the JSON, drawn by the engine: refer to them rather than redrawing or re-describing the data. In a client that supports MCP Apps the whole result also opens as an interactive view in the chat.
<!-- INSTRUCTIONS:END -->

## A raw session with curl

```bash
curl -sS -X POST https://jeanpm.vercel.app/mcp \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"find_restriction_sites","arguments":{"_subject":{"sequence":"GGATCCAAAA"},"enzymes":["BamHI"]}}}'
```

The `data:` line of the reply carries the result:

```json
{
  "content": [
    { "type": "text", "text": "[{\"top\":1,\"bot\":5,\"kind\":\"5'\",\"overhangSeq\":\"GATC\",\"enzyme\":\"BamHI\",\"wraps\":false}]" },
    { "type": "text", "text": "1 cut from 1 of the 1 enzymes asked for; BamHI cuts exactly once.\n\nWhat would undermine this:\n…" }
  ],
  "structuredContent": {
    "sites": [{ "top": 1, "bot": 5, "kind": "5'", "overhangSeq": "GATC", "enzyme": "BamHI", "wraps": false }]
  }
}
```

`tools/list` returns <!-- TOTAL:START -->358<!-- TOTAL:END --> tools, each with an `inputSchema`, an
`outputSchema`, `annotations` and `_meta`. `resources/list` returns the result view. The server
has no prompts or resource templates.

## Naming the molecule: `_subject`

Every tool that acts on a record takes `_subject`, and it names **exactly one** of these:

| Field | Give | Example |
|---|---|---|
| `sequence` | the bases or residues, with optional `name`, `circular` (topology) and `features` | `{"sequence": "AATTCTTAGGATCCG", "circular": true}` |
| `accession` + `source` | an archive accession. `source` is one of <!-- SOURCES:START -->`ncbi` · `ncbi-protein` · `ena` · `uniprot` · `igem` · `addgene` · `dbfetch`<!-- SOURCES:END -->. `db` and `format` apply only to `dbfetch`. An NCBI accession may carry a window: `NC_005816 REGION: 5000..7000` | `{"accession": "U49845", "source": "ncbi"}` |
| `sample` | a bundled real data file, by the `id` that `list_samples` returns | `{"sample": "data/DnaChisel/tests/data/10_emma_genbanks/p8_Linker1.gb"}` |
| `file` | your own file, as `{name, text}` or `{name, base64}`. The format is read from the content and the name | `{"file": {"name": "clone.gb", "text": "LOCUS …"}}` |

`record_index` (0-based) picks one record from a file or accession that holds several. Without
it, a multi-record subject is refused, and the refusal lists the records so you can choose.

The result echoes what it acted on in a `resolved:` text block. For example, from `design_primers`
on the sample above:

```text
resolved: {"subject":{"id":"sample:data/DnaChisel/tests/data/10_emma_genbanks/p8_Linker1.gb","name":"p8_Linker1","length":1864,"circular":false,"features":11,"unit":"bp","from":"the bundled sample data/DnaChisel/tests/data/10_emma_genbanks/p8_Linker1.gb"}}
```

To find a subject:

- `search_records` searches NCBI, ENA, UniProtKB and iGEM by free text and returns accessions.
- `list_samples` lists the bundled files. Filter with `query` and `kind`.

## More records: `_files`

`_files` is a list of references shaped like `_subject`. The records in them become the library
that `sequences`, `parts` and `document` arguments name, the way a multi-part assembly names its
fragments. A trace or an alignment is found by its file name. `list_library` shows what the files
held.

## What a result contains

A successful `tools/call` returns:

| Part | What it is |
|---|---|
| `structuredContent` | the answer as JSON, matching the tool's `outputSchema`. Fields carrying a unit say so in `x-unit` (`°C`, `bp`, `nM`, …). This is the part to compute from |
| `content[0]` | the full engine result as JSON text. It is often richer than `structuredContent`: `design_primers`, for example, adds each primer's footprint, coordinates and GC, and the product sequence |
| `content` `resolved:` block | the subject the tool acted on, and where it came from |
| `content` explanation block | the conclusion in a sentence; **What would undermine this**, the caveats this particular run earned; **How it was derived**, the method and its citation; then the readouts as `name: value` |
| image blocks | figures (plasmid maps, gels, trees, chromatograms, alignments, curves, histograms, heatmaps) as PNG, drawn by the engine, for tools that declare them |

The explanation is generated from the run, not fixed text. For `design_primers` it began:

```text
A 1864 bp product from a 17 / 14 nt pair melting at 59.5 / 59.8 °C, annealing at 58.6 °C on the Taq program.

What would undermine this:
- Both primers sit on the template's own ends, so this amplifies the WHOLE open record (1864 bp) rather than a part of it …
- No buffer was stated, so every temperature here is in the nearest-neighbour defaults rather than in your mix. … Set `conditions` to design in the reaction you will run.
```

## Errors and refusals

There are three kinds, and only the first is a JSON-RPC error:

| Kind | Looks like | Real example |
|---|---|---|
| Unknown tool | JSON-RPC `error`, code `-32602` | `{"error":{"code":-32602,"message":"Tool nope not found"}}` |
| Arguments that break the schema | result with `isError: true`, text starting `Input validation error:` | `Input validation error: Invalid arguments for tool design_primers: invalid arguments: data/target_tm must be number` |
| The engine declines | result with `isError: true`, text starting `the engine declined this request:` and naming what is missing | `the engine declined this request: no record is open — open a sequence in the editor, or wire a record into this step's \`_subject\`` |

A refusal is a real answer. It names the missing or contradictory input rather than returning an
empty list that reads as "nothing found". Over MCP, "no record is open" means `_subject` was not
given.

## Tool metadata

Every tool carries standard MCP `annotations` and Jean's own `_meta`. The reference shows both on
each entry.

| Key | Meaning |
|---|---|
| `annotations.title` | display name |
| `annotations.readOnlyHint` | `true`: reads or lists only |
| `annotations.destructiveHint` | `false` wherever it is set: no tool deletes anything, because the server holds nothing |
| `annotations.openWorldHint` | `true`: the tool reaches an outside service (an archive, a literature index) |
| `_meta["bio.jane/capability"]` | the engine area (`amplify`, `cloning`, `sequencing`, `design`, `record`, `analyze`, `workspace`) |
| `_meta["bio.jane/category"]` | the kind of step: `read` (answers about what it is given), `design`, `build` (makes a new construct) or `export` |
| `_meta["bio.jane/async"]` | `true`: the tool runs long (seconds to minutes). Allow a generous client timeout |
| `_meta["bio.jane/deliverable"]` | the tool assembles a complete package (a knockout design, an expression set) |
| `_meta["bio.jane/contract"].question` | the scientific question the tool answers |
| `….assumptions` / `….limits` | what the answer takes for granted, and what it deliberately does not do (and which tool does) |
| `….validatedBy` | the golden suites that check the engine against the field's reference implementation |
| `….network` | `local` (computed on the engine) or `remote-service` (queries an outside archive or service) |
| `….randomness` | `none`, or `seeded`: give the tool's seed argument to reproduce a run exactly |
| `….writes` | `true`: the result includes new records (a product, an assembled construct) a later step can take |
| `….noScientificClaim` / `….noReading` | the tool computes nothing (a lister or a reader), or which rows of its output carry no reading of their own |
| `_meta.ui.resourceUri` | the MCP Apps view for the result |

## Full descriptions: `describe_tools`

To keep `tools/list` small, each listed description is only its opening sentences.
`describe_tools` returns the full text: what the tool computes, its models and options, and what
it refuses.

```json
{ "name": "describe_tools", "arguments": { "names": ["design_primers"] } }
```

```json
{ "tools": [{ "name": "design_primers", "description": "Design a forward + reverse primer pair to amplify the subject (pydna `primer_design`), with Tm, Ta and suggested Taq/Phusion cycling programs. Emits both primers so a downstream pcr_amplify runs on them — the design→PCR→gel loop." }], "unknown": [] }
```

Names it does not know come back in `unknown`. The tool reference prints every tool's full description.

## Long answers: `read_answer_window`

An answer larger than the size budget comes back cut, with a notice naming the field that was
cut. `read_answer_window` takes the same tool, the same `arguments`, that `field`, and an
`offset` and `limit`, and returns that window of the answer. The answer is derived again, so the
window comes from the same result.

## Workflows: one call, many tools

| Tool | Does |
|---|---|
| `list_workflow_templates` | lists the built-in starter workflows. Pass an `id` to get its graph |
| `validate_workflow` | reports what would stop a graph from running (an unknown tool, a wire into a missing port, a cycle), naming the node and the port, without running anything |
| `run_workflow` | runs a graph and returns per-node status, outputs and errors in topological order |

A graph is nodes naming tools and wires carrying one node's output into another's input, plus
two things a single call cannot express: `$whenExpression` (run this node only if …) and
`scatter` (run it once per element of a list and gather the outputs). Start from a template:
`list_workflow_templates` with an `id` returns a graph ready for `run_workflow`.
