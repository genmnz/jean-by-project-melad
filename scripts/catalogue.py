"""Regenerate every tool listing in this repository from the live server.

Writes, from https://jeanpm.vercel.app/mcp at run time:

- README.md: the tool count (COUNT markers) and the catalogue (TOOLS markers), each tool linked
  to its reference entry;
- docs/tools/<section>.md: the full reference for every tool: its question, full description,
  every argument (nested options flattened, with type, default, range, unit and allowed values),
  every output field, its contract (assumptions, limits, validation, network, randomness);
- docs/tools/README.md: the section index and an A–Z table of every tool;
- docs/protocol.md: the handshake, the server's own instructions and the subject sources, between
  their markers (the prose around them is written by hand).

Nothing in those files is typed by hand, so they can never describe a tool the server does not
have. Run daily by .github/workflows/registry.yml; by hand with `python3 scripts/catalogue.py`
(`--cache DIR` reuses saved server responses while you iterate, instead of calling the server).
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

ENDPOINT = "https://jeanpm.vercel.app/mcp"
ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
DOCS = ROOT / "docs"
TOOLS_DIR = DOCS / "tools"
PROTOCOL = DOCS / "protocol.md"

# Shown in this order. A tool lands in the first section whose rule matches; anything unmatched
# falls into its server-declared capability, so a new tool is never dropped from the list.
SECTIONS = [
    ("cloning", "🧬 Cloning & assembly", "Digests, ligations, Gibson, Golden Gate, Gateway-style recombination, part grammars and assembly planning."),
    ("amplify", "🔥 PCR, primers & thermocycling", "Primer design for every kind of PCR, melting temperatures and reaction simulation."),
    ("crispr", "✂️ CRISPR & genome editing", "Guide design and scoring, off-targets, screens, and editing outcomes measured from traces."),
    ("sequencing", "📈 Sanger, sequencing & verification", "Trace reading, base calling, construct verification, read QC and alignment to a reference."),
    ("qpcr", "🧪 qPCR & digital PCR", "Amplification and melt curves, RDML runs, droplet gating, uncertainty and relative quantification."),
    ("design", "🎛️ Design & expression", "Codon optimisation, RBS and operons, probes, barcodes, genetic circuits and annotation."),
    ("phylo", "🌳 Alignment & phylogenetics", "Pairwise and multiple alignment, dot plots, model selection, trees and tree comparison."),
    ("variants", "🧫 Genomics, variants & copy number", "Variant calls, copy-number segmentation, LOH and mosaicism, genome regions."),
    ("protein", "🧩 Proteins, domains & proteomics", "Domains and motifs, residue sites, protein properties and peptide evidence."),
    ("chem", "⚗️ Cheminformatics", "Molecules, conformers, scaffolds, reactions, chemical space and library screening."),
    ("discovery", "🔬 Expression & hypothesis testing", "Differential expression, gene-set enrichment and falsification-tested discovery programmes."),
    ("data", "🗄️ Public databases & records", "Search and fetch from NCBI, EMBL-EBI, UCSC, UniProt and more, then hand the record to any tool."),
    ("analyze", "📊 Sequence analysis", "Everything else a bench scientist asks of a sequence."),
    ("pipelines", "🔗 Pipelines & lab records", "Chain tools into reproducible workflows, export records, keep lab notes."),
]

RULES = [
    ("cloning", r"gel|digest|ligat|gibson|golden_gate|assembl|domesticat|overhang"),
    ("design", r"codon|back_translate|rbs|operon|probe|circuit|barcode|index_oligo|annotat"),
    ("protein", r"antibody|antigen"),
    ("crispr", r"crispr|guide|sgrna|off_?target|base_edit|indel|tide|screen_"),
    ("qpcr", r"qpcr|cq|melt|rdml|droplet|dpcr|taqman|uncertainty|amplification"),
    ("phylo", r"tree|phylo|align|dot_plot|substitution|msa"),
    ("variants", r"variant|copy_number|region|cnv|loh|mosaic|population"),
    ("chem", r"molecul|compound|tautomer|conformer|scaffold|reaction|protonation|r_groups|activity_cliff|chemical|structure_library"),
    ("protein", r"protein|domain|motif|residue|peptide|blast_cdd|smart|proteom"),
    ("discovery", r"discover|differential|gene_set|enrichment|hypothes|gene_trait|falsif"),
    ("data", r"search_|fetch_|lookup_|query_database|list_databases|literature|accession|find_assemblies|list_samples|ontology|omics"),
    ("pipelines", r"workflow|experiment|export|deposit|construction|preference|collection|report"),
]

# Editor-state tools: they read or write the open project inside the workbench. Over this stateless
# endpoint they have no project to act on, so the README leaves them out; the reference lists them
# in their own section so a client that sees them in tools/list can look them up.
WORKSPACE = ("workspace", "🖥️ Workbench state", "Tools that read or write the open project inside the Jean workbench. Over this stateless endpoint there is no open project, so they matter only to the in-app assistant.")
SKIP_CAPABILITIES = {"workspace"}
# The server's index of its own listing (the full text of each brief description), not a tool.
# docs/protocol.md documents it.
SKIP_NAMES = {"describe_tools"}
ENVELOPE = {"_subject", "_files"}


# ── server ─────────────────────────────────────────────────────────────────────────────────────

class Server:
    def __init__(self, cache=None):
        self.cache = Path(cache) if cache else None
        self.next_id = 0

    def rpc(self, method, params=None, key=None):
        path = self.cache / f"{key or method.replace('/', '_')}.json" if self.cache else None
        if path and path.exists():
            return json.loads(path.read_text())
        self.next_id += 1
        body = json.dumps({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}}).encode()
        req = urllib.request.Request(
            ENDPOINT,
            data=body,
            headers={"content-type": "application/json", "accept": "application/json, text/event-stream"},
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                text = r.read().decode()
        except urllib.error.HTTPError as e:
            if 300 <= e.code < 400:
                sys.exit(f"{ENDPOINT} moved ({e.code}) to {e.headers.get('location')}: update ENDPOINT here, "
                         "in .github/workflows/registry.yml and in every connect snippet.")
            raise
        line = next(l for l in text.splitlines() if l.startswith("data: "))
        msg = json.loads(line[6:])
        if "error" in msg:
            sys.exit(f"{method}: {msg['error']}")
        result = msg["result"]
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result))
        return result

    def full_descriptions(self, names):
        """describe_tools, in batches: the listing carries only each description's opening."""
        out = {}
        for i in range(0, len(names), 50):
            batch = names[i:i + 50]
            res = self.rpc("tools/call", {"name": "describe_tools", "arguments": {"names": batch}}, key=f"describe_{i}")
            data = res.get("structuredContent") or json.loads(res["content"][0]["text"])
            out.update({t["name"]: t["description"] for t in data.get("tools", [])})
        return out


# ── text helpers ───────────────────────────────────────────────────────────────────────────────

def cell(text):
    return re.sub(r"\s*\n\s*", " ", str(text)).replace("|", "\\|").strip()


def contract_of(tool):
    return tool.get("_meta", {}).get("bio.jane/contract", {})


def title_of(tool):
    return tool.get("annotations", {}).get("title", tool["name"])


def one_line(tool):
    contract = contract_of(tool)
    text = contract.get("question") or tool.get("description", "")
    text = re.sub(r"`([^`]*)`", r"\1", text).replace("\n", " ").strip()
    # Workbench phrasing: over MCP the caller passes the data; there is no open project.
    text = re.sub(r"THIS PROJECT'S OWN records", "your own records", text)
    text = re.sub(r"\s+(in|into|from) this project\b", "", text)
    text = text.replace("the open record", "the record").replace("on the trace that is open", "on the trace")
    if not contract.get("question"):
        text = re.split(r"(?<=[.!?])\s|\s—\s", text, maxsplit=1)[0]
    return text if len(text) <= 220 else text[:217].rstrip() + "…"


def section_of(tool):
    cap = tool.get("_meta", {}).get("bio.jane/capability")
    if cap in SKIP_CAPABILITIES:
        return "workspace"
    name = tool["name"]
    for key, pattern in RULES:
        if re.search(pattern, name, re.I):
            return key
    if cap == "record":
        return "data"
    if cap in {s[0] for s in SECTIONS}:
        return cap
    return "pipelines" if cap is None else "analyze"


def link(tool, from_dir):
    page = f"{section_of(tool)}.md#{tool['name']}"
    return page if from_dir == "tools" else f"docs/tools/{page}"


# ── schema flattening ──────────────────────────────────────────────────────────────────────────

def type_of(s):
    if "enum" in s:
        return " · ".join(f"`{json.dumps(v, ensure_ascii=False)}`" for v in s["enum"])
    if "anyOf" in s or "oneOf" in s:
        return " or ".join(type_of(x) for x in s.get("anyOf") or s.get("oneOf"))
    t = s.get("type")
    if isinstance(t, list):
        return " or ".join(t)
    if t == "array":
        items = s.get("items") or {}
        inner = type_of(items) if items else "any"
        return f"{inner}[]" if " " not in inner else f"({inner})[]"
    return t or "any"


def bounds(s):
    parts = []
    lo, hi = s.get("minimum", s.get("exclusiveMinimum")), s.get("maximum", s.get("exclusiveMaximum"))
    if lo is not None and hi is not None:
        parts.append(f"{lo}–{hi}")
    elif lo is not None:
        parts.append(f"≥ {lo}")
    elif hi is not None:
        parts.append(f"≤ {hi}")
    if "minItems" in s or "maxItems" in s:
        parts.append(f"{s.get('minItems', 0)}–{s.get('maxItems', '∞')} items")
    if "minLength" in s or "maxLength" in s:
        parts.append(f"{s.get('minLength', 0)}–{s.get('maxLength', '∞')} chars")
    if s.get("contentEncoding"):
        parts.append(s["contentEncoding"])
    return ", ".join(parts)


def flatten(schema, prefix="", required=(), depth=0):
    """Yield (path, schema, required) for every property, nested objects and object arrays included."""
    for name, s in (schema.get("properties") or {}).items():
        if not prefix and name in ENVELOPE:
            continue
        path = f"{prefix}{name}"
        yield path, s, name in required
        if depth < 6:
            if s.get("properties"):
                yield from flatten(s, f"{path}.", s.get("required", ()), depth + 1)
            items = s.get("items") or {}
            if s.get("type") == "array" and items.get("properties"):
                yield from flatten(items, f"{path}[].", items.get("required", ()), depth + 1)


def input_table(schema):
    rows = list(flatten(schema, required=schema.get("required", ())))
    if not rows:
        return "_No arguments beyond the shared `_subject` and `_files`._" if takes_subject(schema) else "_No arguments._"
    out = ["| Argument | Type | Required | Default | Range | Description |", "|---|---|---|---|---|---|"]
    for path, s, req in rows:
        default = f"`{json.dumps(s['default'], ensure_ascii=False)}`" if "default" in s else ""
        out.append(f"| `{path}` | {cell(type_of(s))} | {'**yes**' if req else ''} | {cell(default)} | {cell(bounds(s))} | {cell(s.get('description', ''))} |")
    return "\n".join(out)


def output_table(schema):
    rows = list(flatten(schema or {}))
    if not rows:
        return None
    out = ["| Field | Type | Unit | Description |", "|---|---|---|---|"]
    for path, s, _ in rows:
        out.append(f"| `{path}` | {cell(type_of(s))} | {cell(s.get('x-unit', ''))} | {cell(s.get('description', ''))} |")
    return "\n".join(out)


def takes_subject(schema):
    return "_subject" in (schema.get("properties") or {})


def skeleton(tool):
    """The smallest arguments object the schema accepts: required fields only, each shown by its type."""
    schema = tool["inputSchema"]
    def value(s):
        if "default" in s:
            return s["default"]
        if "enum" in s:
            return s["enum"][0]
        t = s.get("type")
        if t == "object" and s.get("properties"):
            return {k: value(v) for k, v in s["properties"].items() if k in s.get("required", ())}
        return {"string": "<string>", "number": "<number>", "integer": "<integer>", "boolean": False,
                "array": [], "object": {}}.get(t if isinstance(t, str) else None, "<value>")
    args = {k: value(v) for k, v in (schema.get("properties") or {}).items() if k in schema.get("required", ())}
    if takes_subject(schema):
        args["_subject"] = {"sequence": "<bases, or use accession / sample / file>"}
    return json.dumps({"name": tool["name"], "arguments": args}, ensure_ascii=False, indent=2)


# ── renderers ──────────────────────────────────────────────────────────────────────────────────

def behaviour(tool):
    a, c = tool.get("annotations", {}), contract_of(tool)
    meta = tool.get("_meta", {})
    items = []
    items.append("read-only" if a.get("readOnlyHint") else "returns new records" if c.get("writes") else "computes")
    net = c.get("network")
    if net:
        items.append({"local": "runs locally on the engine", "remote-service": "calls a public database or service"}.get(net, f"network: {net}"))
    if a.get("openWorldHint"):
        items.append("open-world (reaches outside services)")
    rnd = c.get("randomness")
    if rnd and rnd != "none":
        items.append({"seeded": "randomised, reproducible with its seed"}.get(rnd, f"randomness: {rnd}"))
    if meta.get("bio.jane/async"):
        items.append("long-running")
    if meta.get("bio.jane/deliverable"):
        items.append(f"deliverable: {meta['bio.jane/deliverable']}")
    return " · ".join(items)


def render_tool(tool, full):
    c = contract_of(tool)
    out = [f"### {tool['name']}", "", f"**{title_of(tool)}**" + (f": _{c['question']}_" if c.get("question") else ""), ""]
    out += [full.get(tool["name"]) or tool.get("description", ""), ""]
    out += [f"<sub>{behaviour(tool)}</sub>", ""]
    if c.get("assumptions"):
        out += ["**Assumes:**", *[f"- {cell(x)}" for x in c["assumptions"]], ""]
    if c.get("limits"):
        out += ["**Does not:**", *[f"- {cell(x)}" for x in c["limits"]], ""]
    if c.get("noScientificClaim"):
        out += [f"**No scientific claim:** {cell(c['noScientificClaim'])}", ""]
    if c.get("noReading"):
        out += [f"**Not read from this result:** {cell(c['noReading'])}", ""]
    n = len(c.get("validatedBy") or [])
    if n:
        out += [f"**Validated:** against the reference implementation by {n} golden suite{'s' if n > 1 else ''}.", ""]
    elif c.get("unvalidated"):
        out += [f"**Not yet validated:** {cell(c['unvalidated'])}", ""]
    if c.get("reads"):
        out += [f"**Reads bundled data:** {', '.join(Path(r).name for r in c['reads'])}", ""]
    out += ["**Arguments**", "", input_table(tool["inputSchema"]), ""]
    if takes_subject(tool["inputSchema"]):
        out += ["Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.", ""]
    table = output_table(tool.get("outputSchema"))
    if table:
        out += ["<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>", "", table, "", "</details>", ""]
    out += ["<details><summary><b>Minimal call</b></summary>", "", "```json", skeleton(tool), "```", "", "</details>", "",
            "[↑ top](#contents)", "", "---", ""]
    return "\n".join(out)


def all_sections():
    return [*SECTIONS, WORKSPACE]


def render_section_page(key, heading, blurb, items, full):
    head = [f"# {heading}", "", f"_{blurb}_", "",
            f"{len(items)} tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. "
            "How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).", "",
            "## Contents", "", "| Tool | What it answers |", "|---|---|"]
    head += [f"| [`{t['name']}`](#{t['name']}) | {cell(one_line(t))} |" for t in items]
    head += ["", "---", ""]
    return "\n".join(head) + "\n" + "\n".join(render_tool(t, full) for t in items)


def render_index(groups, total):
    out = ["# Tool reference", "",
           f"Every tool on `{ENDPOINT}`: **{total}** in all. Generated from the live server by `scripts/catalogue.py`; "
           "do not edit by hand. Read [the protocol guide](../protocol.md) first: it explains the arguments every tool shares.", "",
           "## Sections", "", "| Section | Tools | Covers |", "|---|---|---|"]
    for key, heading, blurb in all_sections():
        if groups.get(key):
            out.append(f"| [{heading}]({key}.md) | {len(groups[key])} | {blurb} |")
    out += ["", "## A–Z", "", "| Tool | Title | Section |", "|---|---|---|"]
    names = {k: h for k, h, _ in all_sections()}
    every = sorted((t for v in groups.values() for t in v), key=lambda t: t["name"])
    out += [f"| [`{t['name']}`]({link(t, 'tools')}) | {cell(title_of(t))} | {names[section_of(t)]} |" for t in every]
    return "\n".join(out) + "\n"


def render_readme_catalogue(groups):
    out = []
    for key, heading, blurb in SECTIONS:
        items = groups.get(key, [])
        if not items:
            continue
        out.append(f"<details>\n<summary><b>{heading}</b> · {len(items)} tools</summary>\n\n_{blurb}_ "
                   f"Full reference: [docs/tools/{key}.md](docs/tools/{key}.md).\n")
        out.append("| Tool | What it answers |\n|---|---|")
        for t in items:
            out.append(f"| **{cell(title_of(t))}** <br><sub>[`{t['name']}`]({link(t, 'root')})</sub> | {cell(one_line(t))} |")
        out.append("\n</details>\n")
    return "\n".join(out)


def render_server(init, resources):
    info = init["serverInfo"]
    caps = ", ".join(f"`{k}`" + (" (listChanged)" if v.get("listChanged") else "") for k, v in init["capabilities"].items())
    rows = [("Name", f"`{info['name']}`"), ("Title", info.get("title", "")), ("Version", f"`{info.get('version', '')}`"),
            ("Protocol version", f"`{init['protocolVersion']}`"), ("Capabilities", caps)]
    rows += [("Resource", f"`{r['uri']}` ({r.get('mimeType', '')})") for r in resources.get("resources", [])]
    return "\n| | |\n|---|---|\n" + "\n".join(f"| {k} | {cell(v)} |" for k, v in rows) + "\n"


def render_sources(tools):
    for t in tools:
        src = (t["inputSchema"].get("properties", {}).get("_subject", {}).get("properties", {}).get("source") or {})
        if src.get("enum"):
            return " · ".join(f"`{v}`" for v in src["enum"])
    return "_(none declared)_"


def replace_between(path, text, tag, body):
    pattern = re.compile(rf"(<!-- {tag}:START -->)(.*?)(<!-- {tag}:END -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"{path.name} has no {tag} markers")
    return pattern.sub(lambda m: f"{m.group(1)}{body}{m.group(3)}", text)


def rewrite(path, pairs):
    text = path.read_text(encoding="utf-8")
    for tag, body in pairs:
        text = replace_between(path, text, tag, body)
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", help="directory of saved server responses to reuse (and fill)")
    server = Server(ap.parse_args().cache)

    init = server.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                     "clientInfo": {"name": "catalogue", "version": "1"}})
    resources = server.rpc("resources/list")
    tools = [t for t in server.rpc("tools/list")["tools"] if t["name"] not in SKIP_NAMES]
    full = server.full_descriptions([t["name"] for t in tools])

    groups = defaultdict(list)
    for t in tools:
        groups[section_of(t)].append(t)
    for v in groups.values():
        v.sort(key=lambda t: title_of(t).lower())
    shown = sum(len(v) for k, v in groups.items() if k != "workspace")

    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    keep = set()
    for key, heading, blurb in all_sections():
        if groups.get(key):
            page = TOOLS_DIR / f"{key}.md"
            page.write_text(render_section_page(key, heading, blurb, groups[key], full), encoding="utf-8", newline="\n")
            keep.add(page.name)
    for stale in TOOLS_DIR.glob("*.md"):
        if stale.name not in keep | {"README.md"}:
            stale.unlink()
    (TOOLS_DIR / "README.md").write_text(render_index(groups, len(tools)), encoding="utf-8", newline="\n")

    rewrite(README, [("COUNT", str(shown)), ("TOOLS", "\n" + render_readme_catalogue(groups) + "\n")])
    rewrite(PROTOCOL, [("SERVER", render_server(init, resources)),
                       ("INSTRUCTIONS", "\n" + "\n".join(f"> {l}" if l else ">" for l in init.get("instructions", "").splitlines()) + "\n"),
                       ("SOURCES", render_sources(tools)),
                       ("TOTAL", str(len(tools)))])
    print(f"{shown} tools in the README; {len(tools)} in docs/tools/")


if __name__ == "__main__":
    main()
