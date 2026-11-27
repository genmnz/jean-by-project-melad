# 🧬 Cloning & assembly

_Digests, ligations, Gibson, Golden Gate, Gateway-style recombination, part grammars and assembly planning._

37 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`assemble_index_oligos`](#assemble_index_oligos) | What oligos does a synthesizer make for these indexes on these adapter arms or primer? |
| [`assemble_multiple_inserts`](#assemble_multiple_inserts) | Which construct does this backbone, opened at several sites, make with these inserts placed at once? |
| [`assemble_operon`](#assemble_operon) | What does an operon of these CDSs look like with a fresh RBS in front of each, designed against its real upstream context? |
| [`assembly_plan_simulate`](#assembly_plan_simulate) | What final construct does a multi-level assembly plan give, each level's products becoming the next level's parts? |
| [`build_assembly_report`](#build_assembly_report) | What does DnaCauldron's assembly report say about this assembly result? |
| [`check_golden_gate_parts`](#check_golden_gate_parts) | Which of each part's Type-IIS sites are the flanking sites the assembly needs and which are internal sites that will mis-cut it? |
| [`check_methylation_block`](#check_methylation_block) | Does the host's methylation block these enzymes at each of their sites on this molecule? |
| [`classify_grammar_part`](#classify_grammar_part) | Which Golden Braid, MoClo or Yeast ToolKit grammar, position and level does this record represent? |
| [`design_combinatorial_library`](#design_combinatorial_library) | Which constructs does this set of part bins make, member by member, and which combinations did a design rule forbid? |
| [`design_fusion_site_primers`](#design_fusion_site_primers) | Which primers add a Type-IIS site, spacer and chosen overhang to a part on a Tm-matched annealing footprint? |
| [`design_gibson_primers`](#design_gibson_primers) | Which primers amplify each fragment with the 5' overhang that fuses it to its neighbour, Tm-matched within each pair? |
| [`design_ligation_independent_primers`](#design_ligation_independent_primers) | Which primers amplify each fragment with the arm that makes a junction this method's chemistry can close, and is that arm one its own authority stands behind? |
| [`design_multisite_primers`](#design_multisite_primers) | Which one-reaction QCLM primers make several mutations at once, with codons from an organism's usage table? |
| [`design_mutagenesis_primers`](#design_mutagenesis_primers) | Which primers introduce this point change in a CDS by SOE-PCR or QuikChange? |
| [`design_overhang_set`](#design_overhang_set) | Which overhang set of a given size ligates with high fidelity by measured data, keeping any junctions that cannot change? |
| [`design_saturation_primers`](#design_saturation_primers) | Which overlapping primer pairs, one per site, carry a degenerate codon at every site in one reaction? |
| [`design_split_sites`](#design_split_sites) | Where should one sequence be cut into Golden Gate fragments so that the overhangs the cuts create ligate efficiently and faithfully? |
| [`digest_fragments`](#digest_fragments) | Which fragments, with which ends, does a digest of this molecule produce? |
| [`digest_reaction_conditions`](#digest_reaction_conditions) | Which buffer, temperature, cofactors and heat inactivation does a digest with these enzymes need, by NEB's own data? |
| [`domesticate_part`](#domesticate_part) | Which silent codon changes remove a part's internal Type-IIS sites without changing its protein? |
| [`draw_gel`](#draw_gel) | Where does each lane's fragments run on an agarose gel against the marker ladder? |
| [`find_assemblies`](#find_assemblies) | Which published genome assemblies, and which replicons in each, does NCBI hold for this organism? |
| [`find_restriction_sites`](#find_restriction_sites) | Where do these enzymes cut this molecule, on which strand, and what end does each cut leave? |
| [`find_star_sites`](#find_star_sites) | Where else could these enzymes cut this molecule under star conditions, by REBASE's star-activity list and its one-base rule? |
| [`gibson_assemble`](#gibson_assemble) | What construct do these fragments make when they are joined by their terminal homology (Gibson, NEBuilder, In-Fusion)? |
| [`golden_gate_assemble`](#golden_gate_assemble) | What construct do these parts make in a Type-IIS (Golden Gate, MoClo) reaction? |
| [`ligate_fragments`](#ligate_fragments) | What products do these fragments make when their ends are ligated (after any per-fragment digest)? |
| [`ligation_independent_clone`](#ligation_independent_clone) | What does this set of fragments give under LIC, SLIC, In-Fusion, CPEC or USER, and is the homology arm one the method's own authority stands behind? |
| [`plan_thermocycler_program`](#plan_thermocycler_program) | What cycling program does this amplicon need on this polymerase, by its manufacturer's protocol? |
| [`protein_digest`](#protein_digest) | Which peptides, masses and m/z values does a proteolytic digest of this protein give? |
| [`rank_strategies`](#rank_strategies) | Which assembly chemistries can build a construct from these parts, and what does each cost and risk? |
| [`recombine`](#recombine) | What products does a site-specific or homologous recombination between these molecules give (Gateway BP/LR, Cre/loxP, a serine integrase, homology arms, CRISPR knock-in)? |
| [`restriction_ligate`](#restriction_ligate) | What products survive a one-pot restriction-ligation, where re-formed sites are cut again? |
| [`run_gel_lane`](#run_gel_lane) | Which bands, and in which DNA form, does a ladder, plasmid, digest or PCR lane of this molecule give? |
| [`run_gel_plate`](#run_gel_plate) | Where does each band run on this agarose gel, lane by lane? |
| [`score_overhang_fidelity`](#score_overhang_fidelity) | What fraction of assemblies will ligate every junction correctly with this overhang set, by measured T4 ligase data? |
| [`scrub_restriction_sites`](#scrub_restriction_sites) | Which fewest silent codon changes remove the forbidden restriction sites from a CDS? |

---

### assemble_index_oligos

**Assemble index oligos**: _What oligos does a synthesizer make for these indexes on these adapter arms or primer?_

Turn index sequences into the oligos a synthesiser makes: each index spliced between 5'/3' adapter arms, or onto a PCR primer in either orientation with an optional spacer. Audited for the problems that only exist once tag and oligo are concatenated and that no check of the index alone can see — a homopolymer run across the junction, a 5' tetramer recurring as its reverse complement, and an oligo over the synthesis length guideline.

<sub>read-only · runs locally on the engine</sub>

**Does not:**
- Splices sequences as given; no thermodynamic check of the result.

**No scientific claim:** Concatenates supplied index sequences with adapter arms or a primer (optionally reverse-complemented); computes no quantity.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `barcodes` | string[] | **yes** |  |  | the index sequences to assemble. |
| `format` | `"adapter"` · `"primer"` |  | `"adapter"` |  | adapter arms around the index, or a tagged PCR primer. Values: adapter (5'/3' adapter arms), primer (Tagged PCR primer). |
| `adapter_5` | string |  | `"AATGATACGGCGACCACCGAGATCTACAC"` |  | 5' arm the index is spliced after — the Illumina P5, and the panel's own default. |
| `adapter_3` | string |  | `"ACACTCTTTCCCTACACGACGCTCTTCCGATCT"` |  | 3' arm the index is spliced before — the TruSeq read-1 primer, and the panel's own default. |
| `primer` | string |  | `""` |  | the PCR primer the tag is appended to — required when `format` is `primer`. |
| `spacer` | string |  | `""` |  | bases between the tag and the primer. Heterogeneity/phasing spacers are routine on a low-diversity library. Advanced. |
| `reverse_complement_tag` | boolean |  | `false` |  | use each tag as its reverse complement, in an adapter or on a primer, as the instrument requires for some read orientations. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `oligos` | any |  | each assembled oligo with its name, sequence and length |
| `count` | number |  | how many oligos were assembled |
| `warnings` | any |  | junction problems that only exist once tag and oligo are joined: a run across the junction, a self-complementary 5' tetramer, an oligo over the synthesis guideline |
| `longest` | number |  | the longest assembled oligo, in bases — the number a synthesis quote turns on |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "assemble_index_oligos",
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

### assemble_multiple_inserts

**Assemble multiple inserts**: _Which construct does this backbone, opened at several sites, make with these inserts placed at once?_

Open ONE circular backbone at several places and place several inserts in a single step. A complete digest at n sites leaves n arcs and n gaps between them, and every gap has to be filled for the ring to close; the arcs and the inserts go to the same homology assembler the single-insert tool uses, and which insert lands in which gap is read off each construct the homology graph closes rather than guessed. It designs no homology arm: an insert arrives with the ends it has, and a set whose ends do not meet the arcs is the assembler's own refusal.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Each insert already carries terminal homology with the arcs on both sides of its gap.
- The digest is complete: every site of every named enzyme is cut.

**Does not:**
- Predicts the constructs, not their yield.
- One insert per gap; a gap taking two fragments is an ordinary multi-fragment assembly.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `backbone` | string |  |  |  | the circular vector to open. Leave unset to use the open record. |
| `enzymes` | string[] | **yes** |  |  | the enzymes that open the backbone, by name (1409 in the cloning catalogue). Their sites ARE the insertion points, so two single-cutters give two of them; a name the catalogue does not carry is refused by name rather than ignored. |
| `inserts` | (string or object)[] | **yes** |  |  | the fragments to place, one per insertion point — wire upstream `record` outputs here, or name library documents. |
| `min_homology_bp` | number |  | `20` | 10–200 | minimum terminal homology for two ends to join. In bp. |
| `max_homology_bp` | number |  | `100` | 15–500 | longest terminal homology considered; the bound is EXCLUSIVE, as upstream's own range is. In bp. |
| `max_constructs` | number |  | `40` | 1–500 | cap on how many distinct constructs are enumerated. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first construct, as a record |
| `placements` | any |  | every construct the ring closes on, each with the inserts in the order they sit around it |
| `arcs` | any |  | the backbone's arcs: their lengths and the enzyme that made each end — the insertion points, made readable |
| `insertionPoints` | number |  | how many gaps the digest left, which is how many inserts the step takes |
| `cutCounts` | any |  | sites found per enzyme, so an enzyme that does not cut is named rather than silently absent |
| `reading` | string |  | what was planned, generated from the enumeration rather than the request |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "assemble_multiple_inserts",
  "arguments": {
    "enzymes": [],
    "inserts": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### assemble_operon

**Assemble operon**: _What does an operon of these CDSs look like with a fresh RBS in front of each, designed against its real upstream context?_

Stack several CDSs into one contiguous operon, designing a fresh ribosome-binding site in front of each one AGAINST ITS REAL UPSTREAM CONTEXT — which is why the RBS for gene 2 is not the RBS design_rbs would give it in isolation. Returns the assembled sequence, its layout, and each gene's achieved strength.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Each gene's RBS is designed in the context the preceding gene leaves, which is why it differs from the same design in isolation.

**Does not:**
- Reports each gene's achieved relative strength, not expression levels or polar effects.
- Transcriptional terminators and internal promoters are not placed or avoided here.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds` | string[] | **yes** |  |  | the coding sequences to stack, in order — wire upstream `record` outputs here, or name library documents. |
| `include_subject` | boolean |  | `false` |  | put the node's subject first, as the first gene. |
| `target_strength` | number |  | `1` | ≥ 0.01 | relative initiation strength to aim for at every gene, on the model's own scale — 1 is as strong as its reference site. Overridden per gene by `target_strengths`. |
| `target_strengths` | number[] |  |  |  | per-gene target strengths, aligned to `cds` — the Operon panel gives every row its own, and a run through this door could not say the same thing. Shorter than `cds` falls back to `target_strength` for the rest. Advanced. |
| `promoter` | string |  |  |  | promoter sequence to place in front of the operon (optional). Advanced. |
| `terminator` | string |  |  |  | terminator sequence to place after the last gene (optional). Advanced. |
| `leader` | string |  |  |  | leader placed before the FIRST ribosome-binding site (defaults to the design leader). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the assembled operon as a record |
| `sequence` | string |  | the assembled operon sequence |
| `layout` | any |  | every element in order — promoter, each RBS, each CDS, terminator — with its start and end |
| `genes` | any |  | per gene: the RBS designed for it, its spacing, the strength achieved and whether it hit the target |
| `onTarget` | boolean |  | true when EVERY gene reached its target strength — the number to check before ordering |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "assemble_operon",
  "arguments": {
    "cds": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### assembly_plan_simulate

**Assembly plan simulate**: _What final construct does a multi-level assembly plan give, each level's products becoming the next level's parts?_

Run a MULTI-LEVEL assembly plan (DnaCauldron `AssemblyPlan`): several assemblies arranged into dependency levels, where each level's products become parts for the next. Emits the FINAL construct as a record. The plan is DnaCauldron's own spreadsheet shape — one row per construct, `construct_name, part, part, …`.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Each level's assembly follows its chemistry's own simulation.

**Does not:**
- Errors compound across levels; a level with no product stops the plan, and it says where.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `parts` | (string or object)[] |  |  |  | the physical parts — wire upstream `record` outputs here, or list library document names/ids. A part is addressed by this NAME in the plan rows. |
| `plan` | string | **yes** |  |  | the plan, in DnaCauldron's spreadsheet shape: one line per construct, `name,partA,partB`. A construct name may itself be used as a part in a later line — that is what makes the plan multi-level. |
| `method` | `"type2s"` · `"gibson"` · `"biobrick"` · `"basic"` · `"lcr"` · `"annealing"` |  | `"biobrick"` |  | the assembly chemistry every step uses (upstream passes one class per spreadsheet). Values: type2s (Golden Gate (Type-IIS)), gibson (Gibson / homologous), biobrick (BioBrick standard), basic (BASIC (linker-based)), lcr (Ligase cycling reaction), annealing (Oligo pair annealing). |
| `include_subject` | boolean |  | `true` |  | also offer the node's subject as a part. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the final construct (deepest level), as a record |
| `constructs` | any |  | every construct produced, in build order |
| `levels` | any |  | the derived build order: which steps happen at which level |
| `leafParts` | any |  | the physical parts a bench user must actually have |
| `built` | number |  | steps that produced a construct |
| `failed` | number |  | steps that errored |
| `cancelled` | number |  | steps never attempted because a dependency failed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "assembly_plan_simulate",
  "arguments": {
    "plan": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### build_assembly_report

**Build assembly report**: _What does DnaCauldron's assembly report say about this assembly result?_

Build DnaCauldron's assembly report from an assembly result: the per-construct summary table, the constructs and errors spreadsheets as pandas-compatible CSV, and the Outcome / Number of assemblies stats. Wire `golden_gate_assemble` or `gibson_assemble`'s `products`, `errors` and `warnings` outputs into it.

<sub>read-only · runs locally on the engine</sub>

**Not read from this result:** DnaCauldron's spreadsheets and summary table, which the outputs carry; the assembly itself is read by golden_gate_assemble or gibson_assemble, and a report over their result adds no second verdict.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `products` | object[] |  |  |  | the enumerated constructs — wire an assembly node's `products` output. Each needs `id`, `sequence` and `fragmentNames`, which is what both assembly nodes emit. |
| `errors` | object[] |  |  |  | structured assembly errors — wire the assembly node's `errors` output. These become the errors spreadsheet, which is the most useful thing in a report about a run that did not work. |
| `warnings` | object[] |  |  |  | structured assembly warnings — wire the assembly node's `warnings` output. |
| `assembly_name` | string |  | `"assembly"` |  | the name for this assembly: the `assembly_name` column of the summary table and the first field of every errors row. |
| `enzyme` | string |  | `""` |  | the Type-IIS enzyme, for a method that has one — it becomes the report's `enzymes` column, mirroring DnaCauldron's `Type2sRestrictionAssembly.get_extra_construct_data()`. Leave it empty for Gibson, which has no enzyme: an empty column would imply one exists. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summaryCsv` | string |  | the constructs spreadsheet, pandas-compatible CRLF CSV — upstream's `constructs.csv` |
| `errorsCsv` | string |  | the errors spreadsheet — upstream's `errors.csv`, or an empty string when the run had none. Faithful to upstream's own 4-header / 3-field mismatch |
| `warningsCsv` | string |  | the warnings spreadsheet, or an empty string when the run had none |
| `constructCount` | number |  | how many constructs the summary table describes |
| `partsUsed` | any |  | every part name that appears in at least one construct |
| `stats` | any |  | the Outcome / Number of assemblies table, as `compute_stats` produces it |
| `summaryText` | string |  | the report as plain text, for a run record or a note |
| `report` | any |  | the whole report object, including the summary dataframe and the plots decision |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "build_assembly_report",
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

### check_golden_gate_parts

**Check Golden Gate parts**: _Which of each part's Type-IIS sites are the flanking sites the assembly needs and which are internal sites that will mis-cut it?_

Check parts BEFORE a Type-IIS assembly: how many recognition sites each carries, which of them are the two deliberate flanking sites and which are internal sites that will mis-cut the part. This is what answers “why will this assembly not work” — an internal site has to be domesticated (silently recoded) before the reaction can be trusted.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The recognition site is the enzyme's canonical one, on either strand.

**Does not:**
- Finds the sites to domesticate; it does not recode them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `parts` | (string or object)[] |  |  |  | the parts to check — wire upstream `record` outputs here, or list library document names/ids. |
| `include_subject` | boolean |  | `true` |  | also check the node's subject. |
| `enzyme` | string |  | `"BsaI"` |  | the Type-IIS enzyme the assembly will use. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `parts` | any |  | one row per part: site count, internal-site count, whether it is assembly-ready, and the problem when it is not |
| `ready` | boolean |  | true when every part carries exactly its two flanking sites |
| `needsDomestication` | any |  | the parts carrying internal sites, each with every offending site's position and strand |
| `internalSiteCount` | number |  | internal sites across all parts — the number that must reach zero |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_golden_gate_parts",
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

### check_methylation_block

**Check methylation block**: _Does the host's methylation block these enzymes at each of their sites on this molecule?_

Whether the host's own methylation blocks the given enzymes ON THIS PLASMID, from REBASE's methylation-sensitivity tables localised onto your sites. The other term of the same reaction question `find_star_sites` answers. It is deliberately per-SITE and not per-enzyme: REBASE says Dam blocks ClaI, and pBR322's single ClaI site carries no overlapping GATC, so the enzyme-level warning does not apply there. An enzyme REBASE has never examined comes back `examined: false`, which is UNTESTED and never a clearance.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Sensitivity is REBASE's per-methylase table, localised by whether the methylase's motif overlaps the site's marked base.
- The host carries the methylases named.

**Does not:**
- Says whether a site is blocked, not how much activity survives a partial block.

**Validated:** against the reference implementation by 2 golden suites.

**Reads bundled data:** methylation-sensitivity

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `enzymes` | string[] | **yes** |  |  | enzymes to check — resolved against the bundled cut catalog (REBASE spellings; smaller than the REBASE dossier the editor shows). Left unset, the run uses your active enzyme collection. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `enzymes` | any |  | per enzyme: its REBASE recognition site, how many sites this molecule carries, whether REBASE has examined it, and one verdict row per methylase localised onto those sites |
| `blocked` | number |  | how many of the enzymes are blocked or impaired at at least one site HERE — branch on this rather than on the presence of a verdict, because a `cut` verdict is also a verdict |
| `blockedEnzymes` | any |  | the names of those enzymes, for a message that says which one to swap |
| `unexamined` | number |  | how many of the enzymes REBASE has NOT tested against any methylase |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "check_methylation_block",
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

### classify_grammar_part

**Classify grammar part**: _Which Golden Braid, MoClo or Yeast ToolKit grammar, position and level does this record represent?_

Which Golden Braid / MoClo / Yeast ToolKit grammar, position and level the open plasmid represents (or null). Reads the record's own annotations, which is what lets an assembled transcription unit be recognised by its backbone half, and what lets a Level-0 module whose own backbone carries an extra site for the release enzyme be told from that backbone. Configured entry vectors are a Parts Bin concept and are NOT available here, so a TU sitting in a named acceptor is reported by its overhangs rather than by that acceptor's name.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The record's annotations and Type-IIS sites follow one of the three published grammars.

**Does not:**
- A part outside the three grammars is null, not a guess.

**Not read from this result:** The classification record itself: grammar, position, level and release enzyme, or null. The Parts Bin shows it as a row and the assembly's reading is on golden_gate_assemble.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

_No arguments beyond the shared `_subject` and `_files`._

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `grammar` | string |  | grammar name, or empty when unclassified |
| `position` | string |  | position name within the grammar |
| `level` | number |  | assembly level |
| `releaseEnzyme` | string |  | enzyme that releases the part |
| `spans` | any |  | for a COMPOSITE position, the slots it occupies end to end (YTK Type 234 spans 2, 3 and 4); empty otherwise |
| `isVector` | boolean |  | true when a part at this position is also the acceptor backbone for its level (YTK Type 8, 8a, 678) |
| `releaseCuts` | number |  | how many times the release enzyme cut. 2 for a clean excise; 3 for a GoldenBraid Level-0 module, whose pUPD backbone carries its own site, so the backbone is released in two pieces and the insert is identified by carrying no backbone marker |
| `classification` | any |  | the full classification (null when no grammar matches) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "classify_grammar_part",
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

### design_combinatorial_library

**Design combinatorial library**: _Which constructs does this set of part bins make, member by member, and which combinations did a design rule forbid?_

Design a combinatorial library in one step: SLOTS, each offering a bin of interchangeable parts, plus the CONSTANTS every member carries. The member set is the Cartesian product of the bins — one part per slot — pruned by design rules, and each surviving member is assembled by the SAME end-homology (Gibson/NEBuilder/In-Fusion) or plain-concatenation engine the single-construct tools use, so a member's construct is identical to assembling its parts on their own. It builds no second assembler; combinatorial Golden Gate lives in the grammar-assembly panel. Every pruned member is kept in the answer with the rule that removed it.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Within a bin the parts are interchangeable: each occupies the same slot in the assembly order.
- For the end-homology chemistry, every adjacent pair already shares terminal homology, as the single-construct Gibson tool requires.

**Does not:**
- Predicts the constructs, not their yields or relative abundance.
- Combinatorial Golden Gate is served by the grammar-assembly panel, not here.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `bins` | object[] | **yes** |  |  | the variable slots: each {slot, parts} names a slot and the interchangeable parts (record names/ids, or wired `record` outputs) that may fill it. The member set is the Cartesian product across bins. |
| `constants` | (string or object)[] |  |  |  | parts every member carries, assembled before the slot choices — the backbone and any fixed linker. |
| `chemistry` | `"gibson"` · `"concat"` |  | `"gibson"` |  | `gibson` is terminal-homology assembly (Gibson/NEBuilder/In-Fusion/homology, one engine); `concat` is a deterministic head-to-tail join with no homology or digest. Values: gibson (End homology (Gibson)), concat (Concatenation). |
| `rules` | object[] |  |  |  | j5/Eugene design rules that prune combinations: {kind:'notWith',a,b} (never together), {kind:'with',a,b} (if a then b), {kind:'notMoreThan',part,count} (at most count copies, constants included). Advanced. |
| `topology` | `"circular"` · `"linear"` · `"both"` |  | `"circular"` |  | Gibson only: which products to enumerate per member. Values: circular (Circular), linear (Linear), both (Both). Advanced. |
| `min_homology_bp` | number |  | `20` | 10–200 | Gibson only: shortest terminal homology that counts as a join. In bp. Advanced. |
| `max_members` | number |  | `200` | 1–2000 | cap on Cartesian members enumerated, before pruning. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first member's construct, as a record |
| `members` | any |  | every built member: its slot→part lineage, the parts assembled, the construct(s) and any flaws |
| `pruned` | any |  | every combination removed before assembly, each with the rule that removed it — never dropped silently |
| `cartesian` | number |  | Cartesian product size, before pruning (the product of the bin sizes) |
| `built` | number |  | members that closed at least one construct |
| `reading` | string |  | what was enumerated, built and pruned, read off the run |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_combinatorial_library",
  "arguments": {
    "bins": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_fusion_site_primers

**Design fusion site primers**: _Which primers add a Type-IIS site, spacer and chosen overhang to a part on a Tm-matched annealing footprint?_

Design the PCR primers that ADD Type-IIS fusion sites to a part: enzyme site, spacer and the four-base overhang you chose, on a Tm-matched annealing footprint. This is how a sequence that is not yet a Golden Gate part becomes one, and it is the other half of check_golden_gate_parts — that says which parts are unusable, this makes one usable.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Annealing Tm is pydna's primer design model.

**Does not:**
- No upstream designs tailed primers: the test feeds the products to the graded Golden Gate assembler and checks it rebuilds the templates.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the template to amplify — wire a record, name a library document, or leave unset to use the open record. |
| `enzyme` | string |  | `"BsaI"` |  | the Type-IIS enzyme the assembly will use. |
| `left_overhang` | string | **yes** |  |  | the top-strand overhang to leave at the START of the released part — its length must match the enzyme's own overhang. |
| `right_overhang` | string | **yes** |  |  | the top-strand overhang to leave at the END of the released part. |
| `target_tm` | number |  | `60` | 45–72 | target annealing temperature for the template-binding footprint. In °C. |
| `buffer_bases` | string |  | `"AAAAAA"` |  | 5' buffer bases outside the recognition site, so the enzyme has somewhere to sit (NEB recommends 6 nt). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `forward` | string |  | the forward primer, 5'→3': buffer, recognition site, spacer, your overhang, then the annealing footprint |
| `reverse` | string |  | the reverse primer, same construction on the other end |
| `forwardTm` | number | °C | melting temperature of the forward primer's ANNEALING footprint — the tail does not bind the template on the first cycle |
| `reverseTm` | number | °C | the same for the reverse primer; the pair is matched, so a gap between these two is the thing to notice |
| `product` | string |  | what the pair amplifies, tails included |
| `releasedPart` | string |  | what the enzyme cuts OUT of that product — the part that actually enters the assembly, carrying your two overhangs |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_fusion_site_primers",
  "arguments": {
    "left_overhang": "<string>",
    "right_overhang": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_gibson_primers

**Design Gibson primers**: _Which primers amplify each fragment with the 5' overhang that fuses it to its neighbour, Tm-matched within each pair?_

Design the PCR primers that CREATE the terminal homology a Gibson/NEBuilder/In-Fusion assembly needs: a Tm-matched pair per fragment, each carrying the 5' overhang that fuses it to its neighbour in the order given (pydna assembly_fragments). This is the step that turns a planned assembly into oligos you can order.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The fragments are joined in the order given.
- Melting temperatures are the stated nearest-neighbour model's at the stated conditions.

**Does not:**
- Does not screen the primers for dimers, hairpins or off-target priming; check them separately.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the fragments to join, IN ASSEMBLY ORDER — wire upstream `record` outputs here, or list library document names/ids. |
| `include_subject` | boolean |  | `true` |  | put the node's subject first, as the backbone. |
| `target_tm` | number |  | `58` | 40–72 | target annealing Tm for each primer's 3' footprint. In °C. |
| `overlap` | number |  | `30` | 15–80 | homology shared between two adjacent fragments. pydna splits it across the junction, so each primer's 5' tail is about half this. In bp. |
| `circular` | boolean |  | `true` |  | close the ring: the last fragment also overlaps the first. |
| `min_footprint` | number |  | `13` | 8–40 | shortest annealing footprint the designer may settle for (pydna's `limit`). In nt. Advanced. |
| `synthesis_scale` | string |  | `"auto"` |  | catalogue product to price the oligos at (an `oligo-list-prices` record id); `auto` prices each at the cheapest product whose published length range covers it. Advanced. |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method the target Tm is measured in. Left unset it is filled from your reaction-conditions settings, and falls back to pydna's Taq defaults when there are none. Advanced. |
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
| `primers` | any |  | per fragment: the tailed amplicon its primers make, that amplicon's length, and both primers with tail, footprint, length and footprint Tm |
| `amplicons` | any |  | the PCR products these primers make, as sequence RECORDS carrying each fragment's features at their shifted positions. THIS is what assembles: wire it into `gibson_assemble.fragments`, not the untailed fragments |
| `cost` | any |  | what the oligo set costs at a vendor's published list price: per oligo the product, per-base rate and price, plus the set total, the oligos no listed product covers, and the date the prices were read. One supplier's list price, not a quote |
| `costTotal` | number |  | list-price total for the oligos that could be priced (see `cost.unpriced` for any that could not) |
| `primerCount` | number |  | oligos to order (two per fragment) |
| `overlap` | number | bp | homology designed between neighbours (bp) |
| `circular` | boolean |  | whether the ring was closed |
| `conditions` | any |  | the buffer the target Tm was measured in — salt, magnesium, dNTPs, oligo concentration and the salt-correction method — or a note saying pydna's defaults were used |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_gibson_primers",
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

### design_ligation_independent_primers

**Design ligation independent primers**: _Which primers amplify each fragment with the arm that makes a junction this method's chemistry can close, and is that arm one its own authority stands behind?_

Design the PCR primers a ligation-independent reaction needs — LIC, SLIC, In-Fusion, CPEC or USER: a Tm-matched pair per amplified fragment, in the order given. The first four carry the homology arm their own method's authority states (pydna assembly_fragments); USER instead carries a complementary deoxyuridine tail PAIR at each junction, 6–10 nt, found rather than chosen so each dU lands on a dT (Bitinaite et al. 2007; pydna user_assembly_design). This is the step `ligation_independent_clone` assumes has already happened: that tool predicts the reaction, this one produces the oligos to order.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The fragments are joined in the order given, the first being the backbone.
- Each method's arm is its own authority's number, stated per primer (Novagen TB163, EMBL PEPcore, Takara, the CPEC protocol sheet).
- Melting temperatures are the stated nearest-neighbour model's at the stated conditions.

**Does not:**
- USER designs CONSECUTIVE junctions only, as its own designer does: there is no wrap from the last fragment back to the first, because a circular USER construct closes on the vector's own fixed 3' extensions (Bitinaite et al. use pNEB206A's 8 nt), which this does not design.
- USER's extension is found, not chosen, so `arm_nt` does not apply to it: the dU has to land on a dT and the two tails at a junction have to be each other's reverse complement. Each junction's extension is reported in `extensions`.
- A USER chain whose junction has no A-to-T pair inside 6–10 nt is refused by name rather than designed around: the upstream search then tails one primer twice, giving two uracils and a nicked molecule that cannot anneal.
- Does not screen the primers for dimers, hairpins or off-target priming; check them separately.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the fragments to join, IN ASSEMBLY ORDER, the first being the backbone — wire upstream `record` outputs here, or name library documents. |
| `include_subject` | boolean |  | `true` |  | put the node's subject first, as the backbone. |
| `method` | `"lic"` · `"slic"` · `"in-fusion"` · `"cpec"` · `"user"` |  | `"in-fusion"` |  | the cloning method, which decides what the tail is: LIC's arm is the Ek/LIC vectors' fixed overhang, SLIC's and CPEC's are ranges, In-Fusion widens its own for more than one insert, and USER's is a complementary dU pair whose length the search finds. Values: lic (LIC), slic (SLIC), in-fusion (In-Fusion), cpec (CPEC), user (USER). |
| `arm_nt` | number |  |  | 4–80 | the homology arm on ONE primer, which is the unit every one of these authorities states. Left unset, the method's own recommended arm. Does not apply to USER, which finds its extension instead. In nt. |
| `backbone` | `"amplified"` · `"linearized"` |  | `"amplified"` |  | whether the first fragment is amplified with the others (pydna splits each junction across the two neighbouring primers, so the junction is twice the arm) or supplied already cut (the whole arm goes on its neighbour's primer, and the junction is the arm). Values: amplified (Amplified), linearized (Linearized). |
| `eklic` | boolean |  | `false` |  | LIC only: use the Ek/LIC vectors' own fixed extensions (Novagen TB163) instead of designing an arm. One insert only, and the vector is supplied cut. |
| `eklic_tag` | boolean |  | `true` |  | Ek/LIC only: keep the C-terminal tag, or close the insert with the in-frame stop TB163 gives for a construct that omits it. Only applies when eklic is true. Advanced. |
| `target_tm` | number |  | `58` | 40–72 | target annealing Tm for each primer's 3' footprint. In °C. |
| `circular` | boolean |  | `true` |  | close the ring: the last fragment also overlaps the first. USER does not wrap on its own, so a USER ring needs a vector named below. |
| `user_vector` | `"none"` · `"pNEB206A"` |  | `"none"` |  | USER only: join the two outer ends to a vector that already carries fixed 3' extensions, which is how a USER construct closes a ring. pNEB206A is the vector the method's own paper uses. Values: none (None (linear chain)), pNEB206A (pNEB206A). Only applies when method is user. |
| `user_vector_end` | `"left"` · `"right"` |  | `"left"` |  | USER with a vector: which of its two DIFFERENT extensions the first fragment's forward primer matches, which is what sets the insert's orientation in the vector. Values: left (Left (GGAGACAU)), right (Right (GGGAAAGU)). Only applies when user_vector is pNEB206A. Advanced. |
| `min_footprint` | number |  | `13` | 8–40 | shortest annealing footprint the designer may settle for (pydna's `limit`). In nt. Advanced. |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method the target Tm is measured in. Left unset it is filled from your reaction-conditions settings, and falls back to pydna's Taq defaults when there are none. Advanced. |
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
| `primers` | any |  | per amplified fragment: the tailed amplicon its primers make, that amplicon's length, and both primers with tail, footprint, length and footprint Tm |
| `reactants` | any |  | the molecules that actually react, as sequence RECORDS: the amplicons where primers were designed, and any fragment supplied cut as itself. THIS is what to wire into `ligation_independent_clone.fragments`, not the untailed fragments |
| `junctionBp` | number | bp | the homology the design creates at each junction — the number `ligation_independent_clone.arm_nt` needs for the reaction to be predicted as designed |
| `armNt` | number | nt | the arm on one primer |
| `armVerdict` | string |  | whether that arm is one the method's authority stands behind, in its own words |
| `extensions` | any |  | USER only: per junction, the two fragments it joins, the single-stranded 3' extension each side gets (which is also where the dU sits), both tails, and whether that length is one the authority stands behind |
| `vectorEnds` | any |  | USER with a vector: the two FIXED extensions that close the ring, which tail went on which outer primer, and where they come from. Not designed, because the vector was manufactured with them. Null when no vector is named, since a linear chain has no fixed ends to close on |
| `primerCount` | number |  | oligos to order (two per amplified fragment) |
| `summary` | string |  | what was designed, naming the method and its chemistry |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_ligation_independent_primers",
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

### design_multisite_primers

**Design multisite primers**: _Which one-reaction QCLM primers make several mutations at once, with codons from an organism's usage table?_

Design QCLM (quick-change lightning multi-site) oligos: one primer per mutated site, all annealing in one reaction, with the codons drawn from an organism's usage table. A design/write.

<sub>returns new records · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The codon usage table is the organism's.

**Does not:**
- Designs the oligos; the yield of all-sites-mutated clones is not predicted.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds` | string | **yes** |  |  | the CDS nucleotide sequence, in frame from the start codon. |
| `mutations` | string | **yes** |  |  | the substitutions, comma- or space-separated, as [WT][pos][MUT] — e.g. "E42L, E42W, K107M". Several entries at one position are ONE site delivering several aminos. |
| `seed` | number |  | `24301` | ≥ 0 | seed for the codon draw. The same seed and the same request give the same oligos; change it to re-roll. |
| `organism` | `"e-coli"` · `"yeast"` |  | `"e-coli"` |  | codon-usage table the synonymous choice is drawn from. |
| `five_end_flank` | string |  |  |  | explicit 5' context. Left empty, 60 bp is read off the open record either side of the CDS. Advanced. |
| `three_end_flank` | string |  |  |  | explicit 3' context, the partner of `five_end_flank`. Advanced. |
| `min_temperature` | number |  | `75` | 40–95 | lowest Tm threshold the growth scan sweeps. In °C. |
| `max_temperature` | number |  | `90` | 40–95 | highest Tm threshold swept. In °C. |
| `temp_range_size` | number |  | `5` | 0–20 | width of the acceptable Tm window around the reaction temperature. In °C. Advanced. |
| `temp_threshold_step` | number |  | `1` | 1–10 | step between Tm thresholds tried. In °C. Advanced. |
| `min_primer_size` | number |  | `23` | 10–120 | shortest oligo. In nt. Advanced. |
| `max_primer_size` | number |  | `60` | 10–120 | longest oligo. In nt. Advanced. |
| `min_three_end_size` | number |  | `10` | 0–90 | bases between the last mutated codon and the 3' terminus, minimum. In nt. Advanced. |
| `max_three_end_size` | number |  | `40` | 0–90 | longest 3' tail. In nt. Advanced. |
| `min_five_end_size` | number |  | `10` | 0–90 | bases between the 5' terminus and the first mutated codon, minimum. In nt. Advanced. |
| `max_five_end_size` | number |  | `40` | 0–90 | longest 5' lead. In nt. Advanced. |
| `min_gc_content` | number |  | `40` | 0–100 | lowest oligo GC accepted. In %. Advanced. |
| `max_gc_content` | number |  | `60` | 0–100 | highest GC accepted. In %. Advanced. |
| `use_degeneracy_codon` | boolean |  | `true` |  | collapse a site's codons into one IUPAC-degenerate codon (upstream's default). Off, each amino gets its own oligo. |
| `codon_usage_frequency_threshold` | number |  | `0.1` | 0–1 | discard synonymous codons rarer than this fraction in the chosen organism. |
| `na` | number |  | `0` | 0–1000 | sodium concentration the salt correction is computed for. In mM. Only applies when gc_value_set is Schildkraut_1965 or Primer3 or Ahsen_2001. Advanced. |
| `k` | number |  | `50` | 0–1000 | potassium concentration. In mM. Advanced. |
| `tris` | number |  | `20` | 0–1000 | Tris concentration. In mM. Only applies when gc_value_set is Schildkraut_1965 or Primer3 or Ahsen_2001. Advanced. |
| `mg` | number |  | `2` | 0–200 | magnesium concentration — the term the Owczarzy corrections are most sensitive to. In mM. Advanced. |
| `dntp` | number |  | `0.2` | 0–100 | total dNTP concentration, which chelates magnesium and so lowers the effective Mg²⁺. In mM. Advanced. |
| `precision` | number |  | `1` | 0–1 | decimal places the reported Tm is rounded to. In dp. Advanced. |
| `gc_value_set` | `"QuickChange"` · `"Chester_1993"` · `"Schildkraut_1965"` · `"Primer3"` · `"Ahsen_2001"` |  | `"QuickChange"` |  | which published GC-formula parameter set the melting temperature is computed under. Values: QuickChange (QuikChange (the kit manufacturer’s own formula)), Chester_1993 (Marmur-Doty (Chester & Marshak 1993)), Schildkraut_1965 (Schildkraut & Lifson 1965 (Marmur-Doty + log[Na⁺])), Primer3 (Primer3Plus product Tm (Biopython’s default set)), Ahsen_2001 (von Ahsen 2001 (accuracy against ease of use)). Advanced. |
| `non_overlapping_primers` | boolean |  | `false` |  | forbid oligos from overlapping each other. Upstream ranks only the LAST split's solutions with this on (a reproduced bug, see the port header). Advanced. |
| `use_primer3` | boolean |  | `true` |  | apply primer3 hairpin / homodimer / heterodimer penalties. Advanced. |
| `temp_weight` | number |  | `16` | 0–256 | score weight on Tm deviation. Advanced. |
| `primer_size_weight` | number |  | `4` | 0–256 | score weight on oligo length deviation. Advanced. |
| `three_end_size_weight` | number |  | `8` | 0–256 | score weight on 3'-tail length deviation. Advanced. |
| `five_end_size_weight` | number |  | `1` | 0–256 | score weight on 5'-lead length deviation. Advanced. |
| `gc_content_weight` | number |  | `0` | 0–256 | score weight on GC overflow. Advanced. |
| `mutation_coverage_weight` | number |  | `160` | 0–512 | score weight on how many of the requested aminos the design actually delivers — upstream's dominant term. Advanced. |
| `hairpin_temperature_weight` | number |  | `32` | 0–256 | score weight on hairpin Tm. Advanced. |
| `primer_dimer_temperature_weight` | number |  | `32` | 0–256 | score weight on dimer Tm. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `oligos` | any |  | one oligo per site, with its span, Tm, GC and the degenerate codons it installs |
| `mutationCoverage` | number |  | fraction of the requested amino acids the design actually delivers, 0–1 |
| `reactionTemperature` | number | °C | the ONE annealing temperature the winning solution is built for |
| `failureCount` | number |  | constraint breaches in the winning solution (0 = every oligo inside its limits) |
| `seed` | number |  | the seed this design was drawn with — change it to re-roll, keep it to reproduce |
| `fullSequence` | string |  | the construct the oligo coordinates are on: flank + CDS + flank |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_multisite_primers",
  "arguments": {
    "cds": "<string>",
    "mutations": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_mutagenesis_primers

**Design mutagenesis primers**: _Which primers introduce this point change in a CDS by SOE-PCR or QuikChange?_

Design site-directed mutagenesis (SOE-PCR/QuikChange) primers for a point change on a CDS: the ranked inner mutagenic pairs, the constant outer pair, and the single spanning primer that replaces an outer when the site sits too near a CDS end. A design/write.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The CDS is in frame and the change is the codon substitution named.

**Does not:**
- Ranks inner pairs by SpliceCraft's score; it does not screen them for dimers.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds` | string | **yes** |  |  | the CDS nucleotide sequence, in frame from the start codon. |
| `mutation` | string | **yes** |  |  | the change as [WT][pos][MUT], e.g. "W140F" (1-based residue). |
| `tm_model` | `"santalucia"` · `"wallace"` · `"gc:Chester_1993"` · `"gc:QuickChange"` · `"gc:Schildkraut_1965"` · `"gc:Wetmur_Melting_1991"` · `"gc:Wetmur_RNA_1991"` · `"gc:Wetmur_DNA_RNA_1991"` · `"gc:Primer3"` · `"gc:Ahsen_2001"` |  | `"santalucia"` |  | Tm scale the candidates are scored and ranked on. The 55-75 °C window is calibrated for SantaLucia NN; `wallace` is upstream's primer3-free fallback, kept for golden parity. Values: santalucia (SantaLucia nearest-neighbor (Biopython Tm_NN defaults)), wallace (Wallace rule (4 °C per G·C, 2 °C per A·T)), gc:Chester_1993 (GC formula: Marmur-Doty (Chester & Marshak 1993)), gc:QuickChange (GC formula: QuikChange (the kit manufacturer’s own formula)), gc:Schildkraut_1965 (GC formula: Schildkraut & Lifson 1965 (Marmur-Doty + log[Na⁺])), gc:Wetmur_Melting_1991 (GC formula: Wetmur 1991, DNA (MELTING 4.3 approximate mode)), gc:Wetmur_RNA_1991 (GC formula: Wetmur 1991, RNA), gc:Wetmur_DNA_RNA_1991 (GC formula: Wetmur 1991, RNA/DNA hybrid), gc:Primer3 (GC formula: Primer3Plus product Tm (Biopython’s default set)), gc:Ahsen_2001 (GC formula: von Ahsen 2001 (accuracy against ease of use)). |
| `codon_usage_tsv` | string |  |  |  | codon-usage table the mutant codon is drawn from, as a Kazusa-style TSV. Left empty it is the built-in E. coli K12 table, which is what the panel's codon picker opens on. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `mutCodon` | string |  | the mutant codon installed |
| `wtCodon` | string |  | the wild-type codon replaced |
| `ntPosition` | number |  | 1-based nt position of the changed codon's first base, counting from the start of the CDS (the engine returns `ntStart + 1`). This said 0-based until 2026-09-02 and it never was — a coordinate convention stated wrongly is worse than one left unstated, because a downstream node acts on it |
| `ntChanges` | number |  | number of nucleotides changed |
| `candidates` | any |  | the candidate inner primer pairs (with Tm) |
| `outer` | any |  | the constant outer primer pair (BsaI-tailed), each with its annealing Tm and GC |
| `edgeCase` | any |  | set only when the site sits too close to a CDS end for an inner pair: the single spanning primer to use and which outer it replaces. Null otherwise |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_mutagenesis_primers",
  "arguments": {
    "cds": "<string>",
    "mutation": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_overhang_set

**Design overhang set**: _Which overhang set of a given size ligates with high fidelity by measured data, keeping any junctions that cannot change?_

Design a high-fidelity Golden Gate overhang set of a given size against measured ligation data, optionally pinning junctions you cannot change (a fixed vector's own overhangs). The counterpart to score_overhang_fidelity: that grades a set you already have, this proposes one. The search is greedy-plus-steepest-ascent over the same golden-validated objective: real measured data, a heuristic path, no claim of finding the optimum.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Fidelity is the measured T4 ligase data the scorer uses.

**Does not:**
- A greedy-plus-steepest-ascent search: no claim of finding the optimum.
- The golden grades the fidelity objective, not the search path.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `size` | number |  | `6` | 2–30 | how many junctions the assembly needs (parts + 1 for a circular construct, counted as junctions). |
| `fixed` | string[] |  |  |  | junctions you cannot change, such as a destination vector's own overhangs. They are never considered for replacement and are counted inside `size`. |
| `enzyme` | string |  |  |  | the Type-IIS enzyme the reaction uses, which picks that enzyme's own measured matrix when one exists. Only applies when dataset is not given. |
| `dataset` | `"BsaI-HFv2"` · `"BsmBI-v2"` · `"Esp3I"` · `"BbsI-HF"` · `"SapI"` · `"T4-01h-25C"` · `"T4-01h-37C"` · `"T4-18h-25C"` · `"T4-18h-37C"` |  |  |  | design against this measured matrix instead of the one the enzyme implies. Values: BsaI-HFv2 (BsaI-HFv2, Golden Gate cycling (4 nt)), BsmBI-v2 (BsmBI-v2, Golden Gate cycling (4 nt)), Esp3I (Esp3I, Golden Gate cycling (4 nt)), BbsI-HF (BbsI-HF, Golden Gate cycling (4 nt)), SapI (SapI, Golden Gate cycling (3 nt)), T4-01h-25C (T4 DNA ligase, 1 h at 25 C (4 nt)), T4-01h-37C (T4 DNA ligase, 1 h at 37 C (4 nt)), T4-18h-25C (T4 DNA ligase, 18 h at 25 C (4 nt)), T4-18h-37C (T4 DNA ligase, 18 h at 37 C (4 nt)). |
| `start_from` | string[] |  |  |  | the set you already have, as a second starting point. Given one of the same size, the answer is never WORSE than it: the greedy build alone can land in its own basin and lose points against a real set. Wire `golden_gate_assemble.overhangs` here. |
| `candidate_pool` | number |  | `96` | 8–256 | how many of the strongest-annealing overhangs the search considers. Higher is a better set and a slower run. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `overhangs` | any |  | the designed set, pinned junctions first. Wire it into score_overhang_fidelity to see the full per-junction breakdown |
| `fidelity` | number |  | the designed set's fidelity, 0-1, on the same measured matrix |
| `percent` | number | % | the same number as a percentage |
| `dataset` | string |  | the measured matrix designed against |
| `fixed` | any |  | the junctions that were pinned and never replaced |
| `from` | string |  | which starting point won: `greedy` for the built set, `yours` for `start_from` improved in place |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_overhang_set",
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

### design_saturation_primers

**Design saturation primers**: _Which overlapping primer pairs, one per site, carry a degenerate codon at every site in one reaction?_

Design site-saturation mutagenesis (SSM) primers: one overlapping forward/reverse pair per site, each carrying a degenerate codon, sharing ONE reaction-level overlap and 3' temperature so every site amplifies in the same tube (both of Mutation Maker's solvers: fast approximation by default, exhaustive search on request). Every Tm is Biopython's `Tm_NN` over the Allawi & SantaLucia 1997 nearest-neighbour table (`DNA_NN3`, upstream's own), under the salt correction and buffer below. A design/write.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Tm is Biopython's Tm_NN over the Allawi and SantaLucia 1997 table at the stated conditions.

**Does not:**
- The fast solver approximates; only the exhaustive one searches every option.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `cds` | string | **yes** |  |  | the CDS nucleotide sequence, in frame from the start codon (length must be a multiple of 3). |
| `sites` | string | **yes** |  |  | the saturation sites, comma- or space-separated, as [WT][pos]X — e.g. "V2X, K107X". 1-based residue positions. |
| `degenerate_codon` | string |  | `"NNK"` |  | the degenerate codon installed at every site (NNK is the common 32-codon choice). |
| `solver` | `"fast"` · `"exhaustive"` |  | `"fast"` |  | which of Mutation Maker's two solvers designs the pairs. `fast` grows one candidate per site per temperature combination (upstream's own default, milliseconds). `exhaustive` enumerates every primer of every allowed length at every allowed start and scores every geometrically valid pair — hundreds of thousands per site, seconds rather than milliseconds, and it reports what it searched. Values: fast (Fast approximation), exhaustive (Exhaustive search). |
| `forward_primer` | string |  |  |  | 5' flanking primer, 5'→3'. Left empty, it is read off the open plasmid 56 bp either side of the CDS (22 nt, and only when it occurs there exactly once). |
| `reverse_primer` | string |  |  |  | 3' flanking primer, 5'→3' on its own strand. Left empty, it is read off the open plasmid 56 bp either side of the CDS (22 nt, and only when it occurs there exactly once). |
| `five_end_flank` | string |  |  |  | explicit 5' flanking sequence — only for a free-standing gene with no plasmid open, and then the 3' flank is required too. Advanced. |
| `three_end_flank` | string |  |  |  | explicit 3' flanking sequence, the partner of `five_end_flank`. Advanced. |
| `min_overlap_temperature` | number |  | `57` | 30–95 | lowest overlap Tm the reaction may settle on. In °C. |
| `max_overlap_temperature` | number |  | `85` | 30–95 | highest overlap Tm allowed. In °C. |
| `min_three_end_temperature` | number |  | `57` | 30–95 | lowest 3'-end Tm (used when `exclude_flanking_primers` is on; otherwise the window comes from the flanking pair). In °C. Only applies when exclude_flanking_primers is true. |
| `max_three_end_temperature` | number |  | `85` | 30–95 | highest 3'-end Tm allowed. In °C. |
| `three_end_temp_range` | number |  | `5` | 0–20 | width of the 3'-end Tm window scanned around each candidate temperature. In °C. Advanced. |
| `overlap_temp_range` | number |  | `5` | 0–20 | width of the overlap Tm window. In °C. Advanced. |
| `three_end_temp_range_step` | number |  | `2` | 1–10 | step between 3'-end temperatures tried. In °C. Advanced. |
| `overlap_temp_range_step` | number |  | `3` | 1–10 | step between overlap temperatures tried. In °C. Advanced. |
| `separate_forward_reverse_temperatures` | boolean |  | `true` |  | optimise the forward and reverse 3' temperatures independently. Advanced. |
| `exclude_flanking_primers` | boolean |  | `false` |  | take the 3' Tm window from the explicit min/max above instead of from the flanking pair's own Tm. Advanced. |
| `min_primer_size` | number |  | `33` | 10–120 | shortest whole primer. In nt. Advanced. |
| `max_primer_size` | number |  | `60` | 10–120 | longest whole primer. In nt. Advanced. |
| `min_overlap_size` | number |  | `33` | 6–120 | shortest shared overlap. In nt. Advanced. |
| `max_overlap_size` | number |  | `60` | 6–120 | longest overlap. Upstream's scan stops two short of this (a reproduced quirk, see the port header). In nt. Advanced. |
| `min_three_end_size` | number |  | `15` | 3–90 | shortest 3' arm beyond the mutated codon. In nt. Advanced. |
| `min_five_end_size` | number |  | `3` | 0–90 | shortest 5' arm before the mutated codon. In nt. Advanced. |
| `max_three_end_size` | number |  | `42` | 3–120 | longest 3' arm beyond the mutated codon. Bounds the search area and discards candidates whose 3' arm overruns it. In nt. Only applies when solver is exhaustive. Advanced. |
| `max_five_end_size` | number |  | `60` | 0–120 | longest 5' arm before the mutated codon. In nt. Only applies when solver is exhaustive. Advanced. |
| `min_gc_content` | number |  | `40` | 0–100 | lowest primer GC accepted before a primer is flagged out of range. In %. Advanced. |
| `max_gc_content` | number |  | `60` | 0–100 | highest GC accepted. In %. Advanced. |
| `three_end_temp_weight` | number |  | `16` | 0–128 | score weight on 3'-end Tm deviation. Advanced. |
| `three_end_size_weight` | number |  | `8` | 0–128 | score weight on 3'-end length deviation. Advanced. |
| `overlap_temp_weight` | number |  | `1` | 0–128 | score weight on overlap Tm deviation. Advanced. |
| `gc_content_weight` | number |  | `0` | 0–128 | score weight on GC overflow. Upstream's default is 0, and its GC term counts G twice and never counts C (a reproduced bug, see the port header) — raising this weight makes that quirk observable. Advanced. |
| `hairpin_temperature_weight` | number |  | `32` | 0–128 | score weight on hairpin Tm. Only applies when compute_hairpin_homodimer is true. Advanced. |
| `primer_dimer_temperature_weight` | number |  | `32` | 0–128 | score weight on homo/heterodimer Tm. Only applies when compute_hairpin_homodimer is true. Advanced. |
| `compute_hairpin_homodimer` | boolean |  | `false` |  | add the hairpin/homodimer/heterodimer penalty to the score (roughly doubles the run; off upstream). Advanced. |
| `salt_correction` | `"No"` · `"Schildkraut_1965"` · `"Wetmur_1991"` · `"SantaLucia_1996"` · `"SantaLucia_1998"` · `"SantaLucia_DeltaS_1998"` · `"Owczarzy_2004"` · `"Owczarzy_2008"` |  | `"Owczarzy_2004"` |  | salt-correction method, in Biopython's `saltcorr` order. Values: No (None), Schildkraut_1965 (Schildkraut & Lifson 1965 (16.6 · log[Na⁺])), Wetmur_1991 (Wetmur 1991 (16.6 · log[Na⁺/(1 + 0.7 · Na⁺)])), SantaLucia_1996 (SantaLucia 1996 (12.5 · log[Na⁺])), SantaLucia_1998 (SantaLucia 1998 (11.7 · log[Na⁺])), SantaLucia_DeltaS_1998 (SantaLucia 1998, entropy (corrects ΔS, not Tm)), Owczarzy_2004 (Owczarzy 2004 (GC-dependent, corrects 1/Tm)), Owczarzy_2008 (Owczarzy 2008 (Mg²⁺ decision tree, dNTP-corrected)). Advanced. |
| `na` | number |  | `50` | 0–1000 | sodium concentration the salt correction is computed for. In mM. Advanced. |
| `k` | number |  | `50` | 0–1000 | potassium concentration. In mM. Advanced. |
| `tris` | number |  | `20` | 0–1000 | Tris concentration. In mM. Advanced. |
| `mg` | number |  | `2` | 0–200 | magnesium concentration — the term the Owczarzy corrections are most sensitive to. In mM. Advanced. |
| `dntp` | number |  | `0.2` | 0–100 | total dNTP concentration, which chelates magnesium and so lowers the effective Mg²⁺. In mM. Advanced. |
| `dnac1` | number |  | `500` | 0–100000 | the higher-concentration strand (the primer, in a large excess). In nM. Advanced. |
| `dnac2` | number |  | `25` | 0–100000 | the lower-concentration strand (the template). In nM. Advanced. |
| `precision` | number |  | `0` | 0–1 | decimal places the reported Tm is rounded to. In dp. Advanced. |
| `oligo_prefix` | string |  | `"ssm"` |  | prefix for the designed oligo names. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `pairs` | any |  | one designed forward/reverse pair per site, with its overlap, temperatures, GC and in-range flags |
| `siteCount` | number |  | sites requested |
| `foundCount` | number |  | sites the solver found a pair for (< siteCount means the parameters were too tight for some) |
| `overlapTemperature` | number | °C | the ONE overlap Tm the whole reaction settled on |
| `forwardTemperature` | number | °C | reaction-level forward 3'-end Tm |
| `reverseTemperature` | number | °C | reaction-level reverse 3'-end Tm |
| `fullSequence` | string |  | the construct the design spans, flanking primer to flanking primer |
| `search` | any |  | what the solver actually searched: candidates enumerated and kept, pairs scored, temperature combinations tried. Null for the fast solver, which enumerates nothing |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_saturation_primers",
  "arguments": {
    "cds": "<string>",
    "sites": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### design_split_sites

**Design split sites**: _Where should one sequence be cut into Golden Gate fragments so that the overhangs the cuts create ligate efficiently and faithfully?_

Decide where to CUT one sequence into Golden Gate fragments, optimising the split positions and the overhangs they create together. Where design_overhang_set proposes junctions for parts you already have, this fragments a sequence you are about to order: it searches every legal arrangement of fragments in your length window and ranks them by the measured ligation efficiency and fidelity of the overhangs each arrangement produces. Ported from OOGGA (Mukundan & Madhusudhan 2025) and scored against the same Potapov 2018 T4 ligase data the fidelity tools use.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Fragment lengths must fall in the stated window.
- Ligation efficiency and fidelity are the measured Potapov 2018 T4 ligase data.

**Does not:**
- Ranks arrangements by the overhangs only; synthesis difficulty of each fragment is not scored.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the sequence to fragment, in one piece. Leave it empty to fragment the open record. |
| `min_length` | number |  | `300` | ≥ 8 | shortest allowed fragment, in bases — usually what your synthesis vendor will accept. |
| `max_length` | number |  | `600` | ≥ 8 | longest allowed fragment, in bases — the vendor's upper limit, or the length you can sequence in one read. |
| `traces` | number |  | `5` | 1–25 | how many ranked alternatives to return. The best arrangement is rarely the only acceptable one, and the runner-up often avoids a site you care about. |
| `fragments` | number |  |  | 2–40 | pin the number of fragments instead of letting the search choose. Leave empty to take whatever the length window allows. |
| `efficiency_weight` | number |  | `1` | 0–10 | exponent on the running ligation EFFICIENCY — raise it to favour junctions that ligate readily. Efficiency and fidelity are different failure modes: a junction can ligate eagerly and promiscuously. Advanced. |
| `fidelity_weight` | number |  | `1` | 0–10 | exponent on the running FIDELITY — raise it to favour junctions that ligate to the right partner rather than a mismatched one. Advanced. |
| `max_overhang_identity` | number |  | `2` | 0–3 | most positions two overhangs in the set may share before they are treated as confusable. Lower is stricter and rules out more arrangements. Advanced. |
| `alien_overhangs` | string[] |  |  |  | junctions already committed elsewhere in the assembly (a fixed vector's own ends), which this set must not collide with. Advanced. |
| `exclude_from` | number |  |  | ≥ 0 | start of a span no cut may fall in — a feature you need kept intact. Use with exclude_to. Advanced. |
| `exclude_to` | number |  |  | ≥ 0 | end of that span, exclusive. Only applies when exclude_from is set. Advanced. |
| `dataset` | `"BsaI-HFv2"` · `"BsmBI-v2"` · `"Esp3I"` · `"BbsI-HF"` · `"SapI"` · `"T4-01h-25C"` · `"T4-01h-37C"` · `"T4-18h-25C"` · `"T4-18h-37C"` |  | `"T4-18h-37C"` |  | the measured ligation matrix to score against. OOGGA's own published choice is the T4 18 h 37 C set. Values: BsaI-HFv2 (BsaI-HFv2, Golden Gate cycling (4 nt)), BsmBI-v2 (BsmBI-v2, Golden Gate cycling (4 nt)), Esp3I (Esp3I, Golden Gate cycling (4 nt)), BbsI-HF (BbsI-HF, Golden Gate cycling (4 nt)), SapI (SapI, Golden Gate cycling (3 nt)), T4-01h-25C (T4 DNA ligase, 1 h at 25 C (4 nt)), T4-01h-37C (T4 DNA ligase, 1 h at 37 C (4 nt)), T4-18h-25C (T4 DNA ligase, 18 h at 25 C (4 nt)), T4-18h-37C (T4 DNA ligase, 18 h at 37 C (4 nt)). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `breaks` | any |  | the winning arrangement's cut positions, in reading order |
| `fragments` | any |  | the fragments to order: sequence, span, length and the overhang at each end. Consecutive fragments overlap by exactly the four-base junction |
| `overhangs` | any |  | the junctions the winning arrangement creates — wire this straight into score_overhang_fidelity to grade the set it chose |
| `score` | number |  | the objective for the winning arrangement: net efficiency^w x net fidelity^w |
| `net_efficiency` | number |  | net ligation efficiency across every junction, 0-1 |
| `net_fidelity` | number |  | net fidelity across every junction, 0-1 |
| `fragment_count` | number |  | how many fragments the winning arrangement needs |
| `alternatives` | any |  | the other ranked arrangements, each with its own breaks, score and junctions — the best is rarely the only acceptable one |
| `candidates` | number |  | how many arrangements were feasible at all under these constraints |
| `dataset` | string |  | the measured matrix actually scored against |
| `report` | any |  | the whole result, every arrangement in full |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_split_sites",
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

### digest_fragments

**Digest fragments**: _Which fragments, with which ends, does a digest of this molecule produce?_

Digest the subject with the given enzymes into real fragments (sequence + both overhangs). Emits the selected fragment as a NEW record, so a downstream gel/map/ORF runs on that fragment — the digest→assembly hand-off.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Each enzyme's site and cut offsets are REBASE's; every site is cut.

**Does not:**
- Complete digestion is assumed: partials are not modelled.
- Fragment ends are as the enzymes leave them; no end treatment is applied.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `enzymes` | string[] | **yes** |  |  | enzymes to digest with — resolved against the bundled cut catalog (REBASE spellings; smaller than the REBASE dossier the editor shows). Left unset, the run uses your active enzyme collection. |
| `fragment_index` | number |  | `0` | 0–99 | which fragment to emit as the downstream record (0-based, in cut order). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the selected fragment as a linear record |
| `fragments` | any |  | every fragment (sequence + left/right overhang + enzyme) |
| `lengths` | any |  | fragment lengths in cut order |
| `count` | number |  | number of fragments |
| `parentSpan` | any |  | where the emitted fragment sat on the parent, [start, end). A start above the end spans the origin |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "digest_fragments",
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

### digest_reaction_conditions

**Digest reaction conditions**: _Which buffer, temperature, cofactors and heat inactivation does a digest with these enzymes need, by NEB's own data?_

The reaction a digest needs, from NEB's own data: the NEBuffer that serves every enzyme together (scored on the WORST enzyme's percent activity, a star-activity buffer disqualified at any percent), the incubation temperature(s), any cofactor that must be added (SAM or ATP), and each product's heat-inactivation step, or the products NEB cannot heat-inactivate. One call is one tube: enzymes that need different temperatures or have no common buffer come back with `singleTube: false`. Needs no open record.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- NEB's published percent activities and flags hold for the products named.
- One tube: the buffer is scored on the worst enzyme's activity.

**Does not:**
- NEB products only; another supplier's enzyme of the same name may differ.
- Enzymes needing different temperatures are reported as such, not reconciled.

**Not read from this result:** The buffer, temperature, cofactor and inactivation rows the Reaction conditions block prints; the cautions a reaction earns are part of the digest's own reading, on digest_fragments.

**Validated:** against the reference implementation by 2 golden suites.

**Reads bundled data:** nebcutter-enzymes.json

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `enzymes` | string[] | **yes** |  |  | enzymes or NEB product names in one tube (EcoRI, BamHI-HF). A name NEB does not sell is returned under `unknown`, never dropped. Left unset, the run uses your active enzyme collection. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `buffer` | string or null |  | the recommended NEBuffer, or null when every buffer is starred or at 0% for one of the enzymes |
| `singleTube` | boolean |  | true when one buffer AND one temperature serve every enzyme |
| `temperaturesC` | any |  | incubation temperatures required, ascending; more than one means more than one step |
| `cofactors` | any |  | cofactors the reaction requires (SAM, ATP), from REBASE |
| `heatInactivation` | any |  | whether the tube can be heat-killed, each product's NEB step (temperature, minutes), and the products that need a column or gel cleanup instead |
| `buffers` | any |  | every NEBuffer scored, best first: worst percent, star-active enzymes, usable, per-enzyme activity |
| `unknown` | any |  | names NEB does not sell, so no conditions exist for them |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "digest_reaction_conditions",
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

### domesticate_part

**Domesticate part**: _Which silent codon changes remove a part's internal Type-IIS sites without changing its protein?_

Silently recode the internal Type-IIS sites inside a part's coding sequence so the part can be used in a Golden Gate assembly — same protein, no recognition site. Only occurrences the given CDS covers can be fixed this way; any outside it are reported untouched rather than skipped quietly, because a site in a promoter needs a different answer.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The CDS given is in frame and translated by the chosen code.
- The outermost sites are the deliberate flanks; that is a part-design convention, not a measurement.

**Does not:**
- Sites outside the CDS are reported, not fixed.
- The recoding is graded against SpliceCraft; the site classification and splice-back have no upstream and are checked by contract in the test.

**Not read from this result:** The silent substitutions that clear the internal sites, with the site survey beside them; the Domestication dialog shows the counts and the edits, and the assembly's reading is on golden_gate_assemble.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the part to domesticate — wire a record, name a library document, or leave unset to use the open record. |
| `enzyme` | string |  | `"BsaI"` |  | the Type-IIS enzyme whose sites must go. |
| `cds_start` | number | **yes** |  | ≥ 0 | 0-based start of the coding sequence within the part. |
| `cds_end` | number | **yes** |  | ≥ 1 | 0-based end of the coding sequence (exclusive). |
| `cds_strand` | `1` · `-1` |  | `1` |  | 1 for the top strand, -1 for the bottom. Values: 1 (Top strand), -1 (Bottom strand). |
| `table` | string |  |  |  | the codon-usage table to guide the synonymous choice, BY NAME, as the Codon Usage panel lists it. This is the way to pass a table: it resolves against the tables loaded in this project, so the numbers come from one someone built or fetched. Leave unset and the active table is used. |
| `table_tsv` | string |  |  |  | ONLY for a table you are pasting yourself, measured elsewhere — prefer `table`, which names one this project already has. Do NOT write a table out from memory: codon frequencies are measured data, and a typed one is indistinguishable from a real one in the result. TSV: codon<TAB>count. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sequence` | string |  | the part with every reachable internal site recoded |
| `fixedCount` | number |  | how many internal occurrences were actually fixed |
| `fixes` | any |  | one line per synonymous swap, as the engine logs it |
| `outsideCds` | any |  | internal sites the CDS does NOT cover — left untouched, and yours to solve another way |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "domesticate_part",
  "arguments": {
    "cds_start": "<number>",
    "cds_end": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### draw_gel

**Draw gel**: _Where does each lane's fragments run on an agarose gel against the marker ladder?_

Run an agarose gel and photograph it: every lane's fragments migrated by the validated pydna model, drawn as a gel-doc image with the marker ladder's bp marks and each lane's name. The same plate the gel panels draw, so the figure and the rail put every fragment in the same place. Wire `fragments` from a digest or `lengths` from an assembly into `lanes`. A fragment the calibrating curve cannot place is COUNTED in `offScale`, never drawn at the well.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Migration follows pydna's ladder-calibrated interpolation.

**Does not:**
- A fragment the calibrating curve cannot place is counted, not drawn.
- Band brightness is not modelled.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `lanes` | object[] | **yes** |  |  | the lanes, each {name, lengths: [bp, …]}. The marker lane is added for you — `ladder` chooses it. |
| `ladder` | `"generuler_1kb_plus"` · `"hi_lo"` · `"generuler_1kb"` · `"generuler_100bp"` · `"generuler_100bp_plus"` · `"thermo_1kb_plus"` · `"neb_1kb"` · `"neb_100bp"` · `"lambda_hindiii"` · `"penn_state"` |  | `"generuler_1kb_plus"` |  | the MW marker in the reference lane, which is also the curve every lane's migration is read off unless `agarose_percent` is set. Values: generuler_1kb_plus (GeneRuler 1 kb Plus (75–20,000)), hi_lo (Hi-Lo DNA Marker (50–10,000)), generuler_1kb (GeneRuler 1 kb (250–10,000)), generuler_100bp (GeneRuler 100 bp (100–3,000)), generuler_100bp_plus (GeneRuler 100 bp Plus (100–3,000)), thermo_1kb_plus (Thermo 1 Kb Plus (100–15,000)), neb_1kb (NEB 1 kb (500–10,000)), neb_100bp (NEB 100 bp (100–1,517)), lambda_hindiii (Lambda DNA / HindIII (125–23,130)), penn_state (PennState (500–10,000)). |
| `agarose_percent` | number |  |  | 0.3–4 | the gel's agarose (% w/v). Set it and migration comes from a concentration law instead of the ladder's own spline, so the gel responds to the percentage the way a real one does; leave it unset for the ladder-calibrated placement. In %. |
| `mobility_model` | `"helling-goodman-boyer"` · `"rill-van-winkle"` |  | `"helling-goodman-boyer"` |  | which published mobility law the agarose % is applied through. Ignored unless `agarose_percent` is set. Values: helling-goodman-boyer (Helling-Goodman-Boyer), rill-van-winkle (Rill / Van Winkle). Only applies when agarose_percent is set. Advanced. |
| `dna_form` | `"linear"` · `"supercoiled"` · `"nicked"` · `"relaxed"` |  | `"linear"` |  | topology of the sample DNA: supercoiled and nicked circles do not migrate where a linear fragment of the same length does. Only the Helling-Goodman-Boyer law uses it. Values: linear (Linear), supercoiled (Supercoiled), nicked (Nicked), relaxed (Relaxed). Only applies when agarose_percent is set. Advanced. |
| `stain` | `"etbr"` · `"sybr-safe"` · `"sybr-gold"` · `"gelred"` |  | `"etbr"` |  | the dye the plate was stained with; its published emission maximum is the colour the bands are drawn in. Values: etbr (Ethidium bromide), sybr-safe (SYBR Safe), sybr-gold (SYBR Gold), gelred (GelRed). |
| `exposure` | `"plate"` · `"lane"` |  | `"plate"` |  | Whole plate: brightness against the brightest band on the plate (a lightly loaded lane, the ladder included, can draw almost black); Per lane: brightness against each lane's own brightest band (brightness can no longer be compared between lanes). Values: plate (Whole plate), lane (Per lane). |
| `lane_width` | number |  | `46` | 20–160 | how wide each lane is drawn. In px. Advanced. |
| `labels` | boolean |  | `true` |  | print the ladder's readable bp marks, each lane's number above its well and a legend naming it. Off gives the bare plate, for a figure that captions itself. |
| `caption` | boolean |  | `true` |  | the line under the plate naming the curve that positioned the bands and what their brightness is relative to. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `svg` | string or null |  | the gel as an SVG figure, carrying the photographed plate and its labels |
| `width` | number | px | figure width in px |
| `height` | number | px | figure height in px |
| `laneCount` | number |  | sample lanes drawn, the marker lane excluded |
| `bandCount` | number |  | bands with a position on this plate — what the picture shows |
| `offScale` | number |  | fragments the curve could not place, so they are NOT on the picture — check this before reading a lane as complete |
| `ladder` | string |  | the marker in the reference lane |
| `calibratedBy` | string |  | the (bp, Rf) curve that positioned every lane |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "draw_gel",
  "arguments": {
    "lanes": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### find_assemblies

**Find assemblies**: _Which published genome assemblies, and which replicons in each, does NCBI hold for this organism?_

Resolve an organism to its published genome assemblies and the chromosomes, plasmids and organelles each one is made of, with every accession and length NCBI reports. This is how a pipeline starts from a SPECIES rather than from an accession somebody looked up by hand: hand the replicon accession it returns to fetch_record, with a region, to pull a window of that chromosome. Assemblies come back reference-first, so the default pick is the canonical genome.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `organism` | string | **yes** |  |  | a scientific name, a common name, or a taxonomy id (NCBI Datasets accepts all three). "Escherichia coli", "human", "559292" are all valid. |
| `assembly` | string |  |  |  | an assembly accession to take the replicons of, instead of this organism's top one. Use it to pin a pipeline to one genome build rather than to whatever is reference today. |
| `replicons` | boolean |  | `true` |  | list the chosen assembly's assembled molecules too. Off costs one request and answers 'which assemblies exist'; on costs two and answers 'which chromosome do I fetch'. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `assembly` | string |  | the chosen assembly accession: the one asked for, else this organism’s reference-first top hit |
| `accession` | string |  | the largest replicon's nucleotide accession: for most genomes the main chromosome, and what a fetch_record node's $accession wants |
| `length` | number |  | that replicon’s length in bases, so a region can be chosen against a real span |
| `organism` | string |  | the assembly record's own organism name, canonical rather than the words that were typed |
| `assemblies` | any |  | every current assembly NCBI publishes for the organism: accession, RefSeq or GenBank, assembly level, organism, tax id, release date and total length |
| `replicons` | any |  | the chosen assembly's assembled molecules (accession, name, length and molecule type), or empty when replicons were not asked for |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_assemblies",
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

### find_restriction_sites

**Find restriction sites**: _Where do these enzymes cut this molecule, on which strand, and what end does each cut leave?_

Cut positions of the given enzymes on the open plasmid (top/bottom cut, overhang, kind).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Each enzyme's recognition site and cut offsets are REBASE's, as the bundled table holds them.
- The molecule's topology is as the record states, so a site across the origin of a circular one is found.

**Does not:**
- Cut positions only: methylation blocks and star activity are check_methylation_block's and find_star_sites' questions.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `enzymes` | string[] | **yes** |  |  | enzyme names to scan for — resolved against the bundled cut catalog (REBASE spellings; smaller than the REBASE dossier the editor shows), e.g. EcoRI, BsaI. Left unset, the run uses your active enzyme collection. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sites` | any |  | cut sites on the subject |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_restriction_sites",
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

### find_star_sites

**Find star sites**: _Where else could these enzymes cut this molecule under star conditions, by REBASE's star-activity list and its one-base rule?_

Where the given enzymes could ALSO cut the open plasmid under non-standard conditions, from REBASE's own star-activity list and its one-base rule. Not cut sites: these need low ionic strength, high pH, Mn²⁺ for Mg²⁺, glycerol, DMSO or some detergents, and are what turns an over-digested reaction into a band pattern that reads as the wrong clone.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Star activity follows REBASE's rule: a site differing from the recognition site at one base.

**Does not:**
- These are possible sites, not cuts: they need non-standard conditions, and the list says nothing about their rate.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** staract.608

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `enzymes` | string[] | **yes** |  |  | enzymes to check — resolved against the bundled cut catalog (REBASE spellings; smaller than the REBASE dossier the editor shows). Left unset, the run uses your active enzyme collection. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `enzymes` | any |  | per enzyme: whether REBASE examined it, and its possible star sites here |
| `sites` | number |  | total possible star sites across the enzymes REBASE has examined |
| `unexamined` | number |  | how many of the enzymes REBASE has NOT tested for star activity |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_star_sites",
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

### gibson_assemble

**Gibson assemble**: _What construct do these fragments make when they are joined by their terminal homology (Gibson, NEBuilder, In-Fusion)?_

Assemble fragments by terminal homology (Gibson / NEBuilder / In-Fusion, DnaCauldron). Emits the first product as a NEW record for downstream nodes.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Adjacent fragments share terminal homology of at least the stated length.

**Does not:**
- Predicts the products, not their yield; only the first is emitted as a record.
- Does not model exonuclease chew-back, secondary structure or mispriming.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the fragments to assemble — wire upstream `record` outputs here, or list library document names/ids. |
| `include_subject` | boolean |  | `true` |  | also include the node's subject as a fragment. |
| `min_homology_bp` | number |  | `20` | 10–200 | minimum terminal homology for two ends to join. In bp. |
| `max_homology_bp` | number |  | `100` | 15–500 | longest terminal homology considered. The bound is EXCLUSIVE, as upstream's own `range(min, max)` is: a maximum of 40 rejects a 40 bp arm. In bp. |
| `min_tm` | number |  | `0` | 0–200 | optional floor on the junction's GATE value (DnaCauldron's naive A/T = 2, G/C = 4 sum, not a nearest-neighbour temperature). 0 = no constraint. In °C. Advanced. |
| `max_tm` | number |  | `0` | 0–200 | optional ceiling on the same gate scale. 0 = no constraint. In °C. Advanced. |
| `topology` | `"circular"` · `"linear"` · `"both"` |  | `"circular"` |  | product topology to enumerate. Values: circular (Circular), linear (Linear), both (Both). |
| `preserve_backbone_origin` | boolean |  | `false` |  | for circular products, rotate the origin to the start of the backbone fragment and name the product after it. Advanced. |
| `expect_no_unused_parts` | boolean |  | `true` |  | treat a fragment left out of every construct as an error rather than a warning (upstream's own default). |
| `max_constructs` | number |  | `40` | 1–500 | cap on how many distinct constructs are enumerated, so an ambiguous fragment set cannot run away. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first assembled product, as a record |
| `products` | any |  | every enumerated product |
| `productCount` | number |  | number of products (>1 = ambiguous assembly) |
| `warnings` | any |  | assembly warnings |
| `errors` | any |  | assembly errors — the structured flaws DnaCauldron's errors spreadsheet is built from |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "gibson_assemble",
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

### golden_gate_assemble

**Golden Gate assemble**: _What construct do these parts make in a Type-IIS (Golden Gate, MoClo) reaction?_

Assemble parts with a Type-IIS enzyme (Golden Gate / MoClo, DnaCauldron). Emits the first construct as a NEW record for downstream nodes.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The enzyme cuts every recognition site it meets, and matching overhangs ligate.

**Does not:**
- Predicts the products, not their yield or ligation fidelity (score_overhang_fidelity grades that); only the first is emitted.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `parts` | (string or object)[] |  |  |  | the parts to assemble — wire upstream `record` outputs here, or list library document names/ids. |
| `include_subject` | boolean |  | `true` |  | also include the node's subject as a part. |
| `enzyme` | string |  |  |  | Type-IIS enzyme, or leave unset to let DnaCauldron pick one. |
| `connectors` | (string or object)[] |  |  |  | candidate bridging LINKERS, a library distinct from `parts`. The engine reaches for one as a FALLBACK, where the parts alone do not close a construct, and names the ones it added in `warnings`; a candidate it does not need is silently unused. |
| `expected_constructs` | number |  |  | 1–200 | expect exactly this many constructs and fail when the count differs. Leave unset to enumerate every valid one. |
| `expect_no_unused_parts` | boolean |  | `true` |  | treat a part the assembly did not consume as an error, which is DnaCauldron's own default. |
| `max_constructs` | number |  | `40` | 1–200 | cap on enumerated constructs. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first assembled construct, as a record |
| `products` | any |  | every enumerated construct |
| `productCount` | number |  | number of constructs |
| `enzyme` | string |  | the Type-IIS enzyme actually used |
| `warnings` | any |  | assembly warnings |
| `errors` | any |  | assembly errors — the structured flaws DnaCauldron's errors spreadsheet is built from |
| `overhangs` | any |  | the first construct’s junction overhangs, in assembly order: wire this into score_overhang_fidelity |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "golden_gate_assemble",
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

### ligate_fragments

**Ligate fragments**: _What products do these fragments make when their ends are ligated (after any per-fragment digest)?_

Ligate fragments by their overhangs (pydna ligation_assembly) — sticky, optionally blunt. Each input may be digested by its own enzymes first, which is the digest → ligate hand-off. Emits the first product as a NEW record.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Compatible overhangs anneal and ligate; blunt ends join only when allowed.
- Ends are as the digest or end treatments left them.

**Does not:**
- All possible products are enumerated, not their relative yield.
- Digest-then-ligate is a different reaction from one-pot restriction-ligation (restriction_ligate).

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the fragments to ligate — wire upstream `record` outputs here, or name library documents. |
| `include_subject` | boolean |  | `true` |  | also include the node's subject as a fragment. |
| `enzymes` | string[] |  |  |  | digest every input with these enzymes before ligating. Left unset, the run uses your active enzyme collection. |
| `fragment_indices` | number[] |  |  |  | which band to take from each input's digest, positionally (0 = first fragment). Leave empty to use every fragment — which frequently yields no product, exactly as at the bench. |
| `blunt` | boolean |  | `false` |  | allow blunt-end joins as well as sticky. |
| `allow_partial_overlap` | boolean |  | `false` |  | allow partially overlapping sticky ends. Advanced. |
| `circular_only` | boolean |  | `true` |  | report only circular products. |
| `end_origins` | (`"restriction"` · `"synthetic-oligo"` · `"pcr"` · `"pcr-phosphorylated"` · `"unspecified"`)[] |  |  |  | what MADE each input's ends, positionally — this fixes the 5'-phosphate before any treatment. Leave empty for `unspecified`, which is treated as phosphorylated and reproduces a run with no end chemistry at all. Advanced. |
| `end_treatments` | (`"none"` · `"phosphatase"` · `"kinase"`)[] |  |  |  | the phosphatase or kinase applied to each input AFTER it was made, positionally. Dephosphorylating the vector is what stops it self-ligating; a junction with no 5'-phosphate on either strand forms no bond and the product is dropped. Advanced. |
| `fill_in` | boolean[] |  |  |  | positional booleans: fill that input's 5' overhangs with Klenow after its digest, so its cut ends join blunt (needs `blunt`). Each join then reports the bases the fill-in added. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first ligation product, as a record |
| `products` | any |  | every product |
| `productCount` | number |  | number of products (>1 = ambiguous ligation) |
| `junctions` | any |  | the junctions formed, with the overhang each was made by |
| `layout` | any |  | where each piece and join sits ON the product: the spans the map draws |
| `nickedJunctions` | any |  | indices of junctions left NICKED by a missing 5'-phosphate on one strand — the product still transforms and is repaired in vivo. Empty when every junction sealed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "ligate_fragments",
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

### ligation_independent_clone

**Ligation independent clone**: _What does this set of fragments give under LIC, SLIC, In-Fusion, CPEC or USER, and is the homology arm one the method's own authority stands behind?_

Join fragments without a ligase by one of the five named methods — LIC, SLIC, In-Fusion, CPEC or USER (pydna). Each method's chemistry decides which end survives, and its own authority states the arm it needs.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The fragments already carry the method's tails: this predicts the reaction, it does not design the primers.
- LIC's chew-back is T4 with dATP alone and USER's is a single dU per tail, as those methods define them.

**Does not:**
- Predicts the products, not their yield, and models no mispriming or secondary structure.
- USER needs a molecule whose uracils are in the primer tails: a uracil in the middle leaves a nicked molecule, which is refused by name rather than assembled.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the fragments to join — wire upstream `record` outputs here, or name library documents. |
| `include_subject` | boolean |  | `true` |  | also include the node's subject as a fragment. |
| `method` | `"lic"` · `"slic"` · `"in-fusion"` · `"cpec"` · `"user"` |  | `"in-fusion"` |  | the cloning method, which decides the chemistry: LIC and SLIC and In-Fusion chew 3' ends, CPEC removes nothing, USER excises a uracil. Values: lic (LIC), slic (SLIC), in-fusion (In-Fusion), cpec (CPEC), user (USER). |
| `arm_nt` | number |  |  | 4–80 | homology per junction. Left unset, the method's own recommended arm is used (In-Fusion widens its own for more than one insert). In nt. |
| `circular_only` | boolean |  | `false` |  | report only circular products. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first product, as a record |
| `products` | any |  | every product |
| `productCount` | number |  | number of products (>1 = ambiguous) |
| `arm` | number | nt | the homology arm the run used |
| `armVerdict` | string |  | whether that arm is one the method's authority stands behind, in its own words |
| `summary` | string |  | what the reaction gave, naming the method and its chemistry |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "ligation_independent_clone",
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

### plan_thermocycler_program

**Plan thermocycler program**: _What cycling program does this amplicon need on this polymerase, by its manufacturer's protocol?_

Plan the cycling programme for an amplicon on a NAMED enzyme, and check the reaction against that manufacturer's own published limits. The extension rate and the denaturation step come from the product's datasheet and protocol manual; the annealing temperature is yours (from design_primers or pcr_amplify), and anything the manufacturer does not publish comes from the pydna-faithful Taq or Phusion/Q5 preset — the result says which numbers came from where. The check reports the product as a percentage of the vendor's stated maximum, the extension time its rate implies, the substitutions expected per molecule and the fraction of molecules that should be error-free, each finding quoting the specification line it rests on.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The manufacturer's published protocol for the enzyme named, as cached.

**Does not:**
- Scheduling from the protocol; it does not predict yield.

**Not read from this result:** The answer is the program and the vendor findings, each quoting the specification line it rests on, which the outputs carry; the PCR panel shows them as its Reaction check list and writes no conclusion over them.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `amplicon_bp` | number | **yes** |  | ≥ 1 | product length [bp] — pcr_amplify and design_primers both emit it. |
| `gc_percent` | number | **yes** |  | 0–100 | product GC [%], which decides whether the vendor's GC window is cleared. In %. |
| `anneal_c` | number | **yes** |  | 30–80 | annealing temperature [°C] for the pair — the Ta the Tm model gave you, not a guess this tool makes. In °C. |
| `polymerase` | `"taq"` · `"dbd"` |  | `"taq"` |  | which annealing convention and which preset supplies whatever the datasheet does not. Values: taq (Taq), dbd (Phusion / Q5 (DNA-binding domain)). |
| `enzyme` | `"generic"` · `"takara-taq"` · `"takara-ex-taq"` · `"takara-la-taq"` · `"takara-ex-premier"` · `"primestar-gxl"` · `"primestar-hs"` · `"primestar-max"` · `"primestar-longseq"` · `"cloneamp-hifi"` · `"speedstar-hs"` · `"terra-direct"` · `"titanium-taq"` · `"advantage-hd"` · `"qiagen-taq"` · `"qiagen-hotstartaq"` |  | `"generic"` |  | the cataloged product to plan on, or `generic` for the preset alone. Its datasheet supplies the extension rate and, where its manual states one, the denaturation step. Values: generic (Generic preset (no datasheet)), takara-taq (Takara Bio · TaKaRa Taq / EmeraldAmp GT), takara-ex-taq (Takara Bio · TaKaRa Ex Taq / EmeraldAmp MAX), takara-la-taq (Takara Bio · TaKaRa LA Taq), takara-ex-premier (Takara Bio · TaKaRa Ex Premier), primestar-gxl (Takara Bio · PrimeSTAR GXL DNA Polymerase), primestar-hs (Takara Bio · PrimeSTAR HS DNA Polymerase), primestar-max (Takara Bio · PrimeSTAR Max DNA Polymerase Ver.2), primestar-longseq (Takara Bio · PrimeSTAR LongSeq DNA Polymerase), cloneamp-hifi (Takara Bio · CloneAmp HiFi PCR Premix), speedstar-hs (Takara Bio · SpeedSTAR HS DNA Polymerase), terra-direct (Takara Bio · Terra PCR Direct Polymerase Mix), titanium-taq (Takara Bio · Titanium Taq DNA Polymerase), advantage-hd (Takara Bio · Advantage HD Polymerase Mix), qiagen-taq (QIAGEN · Taq DNA Polymerase), qiagen-hotstartaq (QIAGEN · HotStarTaq DNA Polymerase). |
| `cycles` | number |  | `30` | 1–99 | cycles in the main block. |
| `steps` | `"auto"` · `"3"` · `"2"` |  | `"auto"` |  | 3-step keeps a separate annealing stage; 2-step merges it into the extension, which is what a high-Tm pair allows. `auto` lets the builder decide from the primer Tms. Advanced. |
| `touchdown` | boolean |  | `false` |  | start with a touchdown block: the annealing temperature starts high and drops each cycle to the Ta, so early cycles favor the specific product (Korbie & Mattick 2008). |
| `touchdown_delta_c` | number |  | `1` |  | how far the annealing temperature drops per touchdown cycle. In °C. Only applies when touchdown is true. |
| `touchdown_cycles` | number |  | `10` |  | touchdown cycles before the main block (they add to `totalCycles`). Only applies when touchdown is true. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `program` | string |  | the planned programme as a thermocycler would take it, stage by stage |
| `denatureC` | number | °C | per-cycle denaturation temperature [°C] actually planned |
| `denatureSec` | number |  | per-cycle denaturation time [s] actually planned |
| `extensionSec` | number |  | extension time [s] this amplicon needs at the enzyme's published rate |
| `totalCycles` | number |  | cycles including any touchdown block |
| `fromDatasheet` | any |  | which of the planned numbers came from the product (the rest are the preset’s) — the same list the panel turns into its sentence |
| `findings` | any |  | the reaction check: each finding with its severity, its sentence and the vendor line it quotes. Empty for a reaction inside every published limit, and absent entirely for `generic`, which has no limits to check. |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "plan_thermocycler_program",
  "arguments": {
    "amplicon_bp": "<number>",
    "gc_percent": "<number>",
    "anneal_c": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### protein_digest

**Protein digest**: _Which peptides, masses and m/z values does a proteolytic digest of this protein give?_

In-silico proteolytic digest of a protein (ExPASy PeptideCutter / PeptideMass): peptides with coordinates, average and monoisotopic masses, m/z per charge state, and the MS mass-window filter. 49 proteases and chemicals — or an enzyme of your own written in RPG rule grammar — one or several at a time; a multi-enzyme digest runs concurrently (all at once, products re-digested until nothing changes) or sequentially (one result per enzyme).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The protease's cleavage rules are PeptideCutter's or the RPG grammar given.
- Complete digestion with the missed cleavages allowed.

**Does not:**
- In-silico: digestion efficiency, modifications and detectability are not predicted.
- The MS window filters what an instrument would see, it does not predict intensity.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (unambiguous one-letter codes); wire it from translate_sequence. |
| `enzyme` | `"arg-c"` · `"asp-n"` · `"asp-n-sg"` · `"bnps-skatole"` · `"bromelain"` · `"caspase-1"` · `"caspase-10"` · `"caspase-2"` · `"caspase-3"` · `"caspase-4"` · `"caspase-5"` · `"caspase-6"` · `"caspase-7"` · `"caspase-8"` · `"caspase-9"` · `"chymotrypsin-high"` · `"chymotrypsin-low"` · `"clostripain"` · `"cnbr"` · `"elastase"` · `"enterokinase"` · `"factor-xa"` · `"ficin"` · `"formic-acid"` · `"glu-c"` · `"glutamyl-endopeptidase"` · `"granzyme-b"` · `"hydroxylamine"` · `"iodosobenzoic-acid"` · `"lysc"` · `"lysn"` · `"lysarginase"` · `"neutrophil-elastase"` · `"ntcb"` · `"papain"` · `"pepsin-ph2.0"` · `"pepsin-ph1.3"` · `"proalanase"` · `"proline-endopeptidase"` · `"proteinase-k"` · `"staph-peptidase-i"` · `"tev"` · `"thermolysin"` · `"thrombin"` · `"thrombin-sg"` · `"trypsin"` · `"trypsin-low"` · `"trypsin-simple"` · `"alp"` · `"custom"` |  | `"trypsin"` |  | protease or chemical (single-enzyme digest), or 'custom' to use `customCleave`. Values: arg-c (Arg-C proteinase), asp-n (Asp-N endopeptidase), asp-n-sg (Asp-N, sequencing grade (D and C)), bnps-skatole (BNPS-Skatole), bromelain (Bromelain), caspase-1 (Caspase 1), caspase-10 (Caspase 10), caspase-2 (Caspase 2), caspase-3 (Caspase 3), caspase-4 (Caspase 4), caspase-5 (Caspase 5), caspase-6 (Caspase 6), caspase-7 (Caspase 7), caspase-8 (Caspase 8), caspase-9 (Caspase 9), chymotrypsin-high (Chymotrypsin (high specificity)), chymotrypsin-low (Chymotrypsin (low specificity)), clostripain (Clostripain (Arg-C)), cnbr (CNBr), elastase (Elastase), enterokinase (Enterokinase), factor-xa (Factor Xa), ficin (Ficin), formic-acid (Formic acid), glu-c (Glu-C (D and E)), glutamyl-endopeptidase (Glutamyl endopeptidase), granzyme-b (Granzyme B), hydroxylamine (Hydroxylamine), iodosobenzoic-acid (Iodosobenzoic acid), lysc (Lys-C), lysn (Lys-N), lysarginase (LysargiNase), neutrophil-elastase (Neutrophil elastase), ntcb (NTCB (2-nitro-5-thiocyanobenzoic acid)), papain (Papain), pepsin-ph2.0 (Pepsin (pH > 2)), pepsin-ph1.3 (Pepsin (pH 1.3)), proalanase (ProAlanase), proline-endopeptidase (Proline endopeptidase), proteinase-k (Proteinase K), staph-peptidase-i (Staphylococcal peptidase I), tev (TEV protease (Tobacco Etch Virus)), thermolysin (Thermolysin), thrombin (Thrombin), thrombin-sg (Thrombin (sequencing grade)), trypsin (Trypsin), trypsin-low (Trypsin (low specificity)), trypsin-simple (Trypsin (simple K/R)), alp (α-lytic protease (aLP)), custom (Custom cleavage rule). |
| `enzymes` | (`"arg-c"` · `"asp-n"` · `"asp-n-sg"` · `"bnps-skatole"` · `"bromelain"` · `"caspase-1"` · `"caspase-10"` · `"caspase-2"` · `"caspase-3"` · `"caspase-4"` · `"caspase-5"` · `"caspase-6"` · `"caspase-7"` · `"caspase-8"` · `"caspase-9"` · `"chymotrypsin-high"` · `"chymotrypsin-low"` · `"clostripain"` · `"cnbr"` · `"elastase"` · `"enterokinase"` · `"factor-xa"` · `"ficin"` · `"formic-acid"` · `"glu-c"` · `"glutamyl-endopeptidase"` · `"granzyme-b"` · `"hydroxylamine"` · `"iodosobenzoic-acid"` · `"lysc"` · `"lysn"` · `"lysarginase"` · `"neutrophil-elastase"` · `"ntcb"` · `"papain"` · `"pepsin-ph2.0"` · `"pepsin-ph1.3"` · `"proalanase"` · `"proline-endopeptidase"` · `"proteinase-k"` · `"staph-peptidase-i"` · `"tev"` · `"thermolysin"` · `"thrombin"` · `"thrombin-sg"` · `"trypsin"` · `"trypsin-low"` · `"trypsin-simple"` · `"alp"` · `"custom"`)[] |  |  |  | two or more proteases for a multi-enzyme digest; overrides `enzyme`. Order matters in concurrent mode. 'custom' takes its place in the order like any other. |
| `customCleave` | string[] |  |  |  | cleaving rules for the 'custom' enzyme, in RPG grammar: the comma is the cut, so '(,A)' cleaves before A and '(K or R,)' after K or R. Empty parentheses mean any residue. |
| `customExceptions` | string[] |  |  |  | exceptions for the 'custom' enzyme; each must repeat the rule it blocks, e.g. '(K or R,)(P)' = not when P follows. |
| `customRegex` | string |  |  |  | the 'custom' enzyme as a regular expression instead of RPG grammar (pyteomics' `rule=`): it matches at P1 and the cut falls after the match, e.g. '[KR]' cleaves after K or R. Single-enzyme only, and mutually exclusive with `customCleave`. Advanced. |
| `mode` | `"concurrent"` · `"sequential"` |  | `"concurrent"` |  | multi-enzyme only. 'concurrent' = all at once, re-digesting products until nothing changes (can cut where no single enzyme cuts the intact chain); 'sequential' = one result per enzyme, each on the intact protein. |
| `missedCleavages` | number |  | `0` |  | single enzyme: allow up to this many internal sites per peptide (pyteomics). Multi-enzyme: append runs of up to this many merged adjacent peptides (RPG). |
| `keilExceptions` | boolean |  | `true` |  | apply Keil's exception rules (sites trypsin does NOT cut despite matching). Only defined for trypsin. PeptideCutter and Bioconductor cleaver apply these by default, which is why this does too; pyteomics does not, so turn it off to cross-check against pyteomics. |
| `semi` | boolean |  | `false` |  | also emit semi-enzymatic peptides (one ragged terminus). |
| `minLength` | number |  | `1` |  | drop peptides shorter than this (residues). |
| `maxLength` | number |  | `200` |  | drop peptides longer than this (residues). |
| `massMin` | number |  |  |  | keep only peptides at or above this monoisotopic mass [Da]; omit for no lower bound. |
| `massMax` | number |  |  |  | keep only peptides at or below this monoisotopic mass [Da]; omit for no upper bound. |
| `charges` | number[] |  | `[1, 2, 3]` |  | charge states to report m/z for, e.g. [1,2,3] — [M+zH]z+ from the monoisotopic mass. |
| `cysteine` | `"none"` · `"iodoacetamide"` · `"iodoacetic-acid"` · `"vinylpyridine"` · `"acrylamide"` |  | `"none"` |  | cysteine alkylation applied before the digest, as ExPASy PeptideMass offers it. Mass deltas are Unimod's. |
| `metOxidation` | `"off"` · `"all"` · `"both"` |  | `"off"` |  | methionine oxidation. 'all' oxidises every Met (masses move, peptide list unchanged); 'both' lists each Met peptide TWICE, unmodified and oxidised, as PeptideMass does. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `peptides` | any |  | peptides with start/end, sequence, missed cleavages, masses and m/z (all results pooled in multi-enzyme mode) |
| `results` | any |  | multi-enzyme only: one entry per digestion (per enzyme in sequential mode, one for the whole set in concurrent), each with its own peptides, sites and coverage |
| `count` | number |  | peptides returned after any mass filter |
| `totalPeptides` | number |  | peptides the digest produced BEFORE the mass filter |
| `sites` | any |  | cleavage-site positions (0-based residue index the next peptide starts at) |
| `coverage` | number |  | fraction of the protein covered by the peptides returned |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_digest",
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

### rank_strategies

**Rank strategies**: _Which assembly chemistries can build a construct from these parts, and what does each cost and risk?_

Compare EVERY assembly chemistry this engine has against one set of parts, and say what each one costs and risks. It runs them all, keeps the ones that really produce a construct, and reports the rest with the refusal the chemistry itself gave — so 'Golden Gate is the only way to build this, and its overhangs ligate correctly 99.8% of the time' is one step rather than six runs and a spreadsheet. There is deliberately no single 'best' score: combining the criteria needs weights nobody has settled, and the one criterion every published ranking leads with (cost) has no price this app can honestly cache. So the comparison is the answer, and the sort is by whichever criterion you name.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Each chemistry's own simulation is the arbiter of whether it builds the construct.

**Does not:**
- No single best score: combining criteria needs weights nobody has settled, so the comparison is the answer.
- Cost is not ranked: there is no price this app can honestly cache.
- No upstream ranks strategies; the golden grades each chemistry's products and the ligation-fidelity scores, not the ordering.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `parts` | string[] |  |  |  | the parts to assemble, in order — order is meaningful for Type-IIS. Wire records in, or name project documents. |
| `order_by` | `"steps"` · `"junctions"` · `"primers"` · `"overhangFidelity"` · `"weakestJunctionTm"` · `"framesBroken"` · `"diagnosticCutters"` · `"cost"` |  | `"junctions"` |  | which criterion to order the feasible strategies by. Every criterion is reported for every strategy whichever one you pick. Values: steps (Steps (lower is better)), junctions (Junctions (lower is better)), primers (Primers (lower is better)), overhangFidelity (Overhang fidelity (higher is better)), weakestJunctionTm (Weakest junction Tm (higher is better)), framesBroken (Frames broken (lower is better)), diagnosticCutters (Diagnostic cutters (higher is better)), cost (Cost (lower is better)). |
| `enzyme` | string |  | `"auto"` |  | Type-IIS enzyme for the chemistries that use one. `auto` is DnaCauldron's own default: it picks the enzyme from the sites the parts carry. |
| `digest_enzymes` | string[] |  |  |  | the enzymes a verification digest may use. Left unset the run uses your active enzyme collection; with neither, the diagnostic-digest criterion is reported as unavailable rather than guessed, because a digest is only meaningful against enzymes you have. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `best` | string or null |  | the chemistry at the top of the order you asked for — a position in that order, not a verdict. Null when no chemistry built these parts |
| `feasible` | number |  | how many chemistries produced a construct from these parts |
| `ranked` | any |  | every feasible strategy in order, each with every criterion and the reason for any it could not score |
| `refused` | any |  | the chemistries that produced nothing, each with the refusal it gave. Never dropped: 'this cannot be built that way, and here is why' is half the answer |
| `notScored` | any |  | criteria NO strategy could score, with the reason — so an empty column says why it is empty |
| `criteria` | any |  | the criteria themselves: what each one means and which direction is better |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "rank_strategies",
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

### recombine

**Recombine**: _What products does a site-specific or homologous recombination between these molecules give (Gateway BP/LR, Cre/loxP, a serine integrase, homology arms, CRISPR knock-in)?_

Recombination between molecules — Gateway BP/LR (att sites), Cre/loxP, a serine integrase whose two half-sites you supply, plain homologous recombination through shared arms, or a CRISPR knock-in that keeps only products whose repair region contains every guide's cut. Emits the first product as a NEW record for downstream nodes.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The att, lox or integrase half-sites are the canonical ones (or the ones supplied), recognised exactly.
- Homologous recombination needs the stated length of identical shared sequence.

**Does not:**
- Predicts which products are possible, not their yield or which dominates.
- Emits only the first product as a new record; the rest are listed.

**Validated:** against the reference implementation by 5 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the molecules to react — wire upstream `record` outputs here, or name library documents. |
| `include_subject` | boolean |  | `true` |  | also include the node's subject as a reactant. |
| `system` | `"gateway-BP"` · `"gateway-LR"` · `"cre-lox"` · `"recombinase"` · `"homologous"` · `"crispr-knock-in"` |  | `"gateway-LR"` |  | recombination system. Values: gateway-BP (Gateway BP (attB × attP → entry)), gateway-LR (Gateway LR (attL × attR → expression)), cre-lox (Cre / loxP), recombinase (Serine integrase (your two half-sites)), homologous (Homologous recombination (shared arms)), crispr-knock-in (CRISPR knock-in (guide-gated HR)). |
| `greedy` | boolean |  | `false` |  | permissive att core matching. Only applies when system is gateway-BP or gateway-LR. Advanced. |
| `multi_site_only` | boolean |  | `true` |  | keep only products where BOTH sites recombined (drops single-site intermediates). Only applies when system is gateway-BP or gateway-LR. |
| `circular_only` | boolean |  | `false` |  | report only circular products. |
| `site1` | string |  |  |  | the recombinase's first half-site (e.g. attP). Case is meaningful: the lower-case middle is the overlap the enzyme crosses over in. Only applies when system is recombinase. |
| `site2` | string |  |  |  | the recombinase's second half-site (e.g. attB), same convention. Only applies when system is recombinase. |
| `homology_bp` | number |  | `40` | 10–500 | shortest homology arm that counts as a shared end. In bp. Only applies when system is homologous or crispr-knock-in. |
| `guides` | string[] |  |  |  | protospacers whose cut must fall inside the repaired region — a product cut elsewhere by any of them is discarded and counted. Only applies when system is crispr-knock-in. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first product, as a record |
| `products` | any |  | every product |
| `productCount` | number |  | number of products |
| `sites` | any |  | per-input report of the recombination sites found |
| `discarded` | number |  | CRISPR knock-in only: products dropped because a guide also cuts OUTSIDE the repair. A non-zero count is a finding about the guide, not a warning to swallow |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "recombine",
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

### restriction_ligate

**Restriction ligate**: _What products survive a one-pot restriction-ligation, where re-formed sites are cut again?_

Cut and ligate in ONE POT (pydna restriction_ligation_assembly): every input is digested by the same enzymes inside the reaction and the pieces are joined as they appear, so a junction that re-forms a recognition site can be cut again. This is the reaction Golden Gate is a special case of, and it is a different chemistry from ligate_fragments, which digests first and then ligates whatever the digest left. Reports how many sites of the FIRST enzyme each product still carries — a finished construct has none.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Every input is digested by the same enzymes throughout the reaction.

**Does not:**
- Enumerates products, not yields; a finished construct is one with no sites of the first enzyme left.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the molecules to put in the pot — wire upstream `record` outputs here, or name library documents. |
| `include_subject` | boolean |  | `true` |  | also put the node's subject in the pot. |
| `enzymes` | string[] |  |  |  | the enzymes in the pot — used for every input. Left unset, the run uses your active enzyme collection. |
| `blunt` | boolean |  | `true` |  | allow blunt-end joins as well as sticky. |
| `circular_only` | boolean |  | `true` |  | report only circular products. |
| `sort_by_recognition_sites` | boolean |  | `true` |  | sort products by how many sites of the FIRST enzyme they still carry, fewest first — this floats the finished construct to the top. |
| `end_origins` | (`"restriction"` · `"synthetic-oligo"` · `"pcr"` · `"pcr-phosphorylated"` · `"unspecified"`)[] |  |  |  | what MADE each input's ends, positionally. In a one-pot reaction almost every end is cut INSIDE the tube and is therefore freshly 5'-phosphorylated, so this changes the answer only for an input's own original terminus — reachable only when it arrives already sticky, which today means an annealed oligo adapter. Advanced. |
| `end_treatments` | (`"none"` · `"phosphatase"` · `"kinase"`)[] |  |  |  | the phosphatase or kinase applied to each input, positionally. Same reach as `end_origins`: an original sticky terminus only. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the first product, as a record — with the sort on, the one carrying the fewest remaining sites |
| `products` | any |  | every product |
| `productCount` | number |  | number of products (>1 = the pieces go together more than one way) |
| `recognitionSites` | number |  | sites of the FIRST enzyme still in the first product. 0 = finished: the reaction cannot re-cut it |
| `junctions` | any |  | the junctions formed, with the overhang each was made by — wire into score_overhang_fidelity |
| `nickedJunctions` | any |  | indices of junctions left NICKED by a missing 5'-phosphate on one strand — the product still transforms and is repaired in vivo |
| `partiallyDigested` | any |  | inputs whose products were DROPPED because they would have needed a partial digest — a product that needs the enzyme to skip a site it must have cut is not a bench outcome |
| `layout` | any |  | where each piece and join sits ON the product: the spans the map draws |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "restriction_ligate",
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

### run_gel_lane

**Run gel lane**: _Which bands, and in which DNA form, does a ladder, plasmid, digest or PCR lane of this molecule give?_

Resolve a gel lane (ladder / plasmid / digest / pcr) into [bp, form] bands for the open plasmid.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Uncut plasmid runs as its supercoiled, linear and open-circular forms; migration follows SpliceCraft's agarose model.

**Does not:**
- Band positions, not intensities or smearing.

**Not read from this result:** One lane's bands as [bp, form] pairs. A gel's reading is over a whole plate and is carried by draw_gel, which runs one; a single lane has no plate to read.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"ladder"` · `"plasmid"` · `"digest"` · `"pcr"` | **yes** |  |  | what this lane holds. Values: ladder (DNA ladder), plasmid (Uncut plasmid), digest (Restriction digest), pcr (PCR product). |
| `detail` | string |  |  |  | for a ladder: its name; for a digest: comma-separated enzymes. Unused for plasmid/pcr lanes. Only applies when source is ladder or digest. |
| `product_bp` | number |  |  | ≥ 1 | for a pcr lane: the product length, e.g. the length of the record `pcr_amplify` emits. Required for a pcr lane. In bp. Only applies when source is pcr. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `bands` | any |  | [bp, form] gel bands |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "run_gel_lane",
  "arguments": {
    "source": "ladder",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### run_gel_plate

**Run gel plate**: _Where does each band run on this agarose gel, lane by lane?_

Run a multi-lane virtual agarose gel and return its READING, not just its bands: how many lanes carrying how many bands over what range, positioned by which ladder, plus only the cautions this plate earned — a lane running off the top or bottom of the reference ladder entirely (no mark to interpolate against, so the position is the calibration curve extrapolated), a band inside the ladder but outside the resolving window of the agarose percentage cast, two fragments co-migrating as one drawn band, a DNA form the chosen law cannot move, an empty lane, and a refused calibration. Wire one `run_gel_lane` per lane into `lanes`. The migration model is `@ports/gel`, the same one the Virtual Gel Bench panel draws.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The mobility model, agarose percentage, DNA form and ladder given.

**Does not:**
- A model of migration, not a photograph.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `lanes` | any[][] | **yes** |  |  | the lanes, in edge order — each a `[bp, form]` band list, which is exactly what `run_gel_lane` emits. A bare list of fragment lengths is also accepted and runs at the plate `form`. Several wires land here. |
| `lane_names` | string[] |  | `[]` |  | a name per lane, in the same order. Unnamed lanes become `Lane 1`, `Lane 2`, … — the reading names the lane every caution is about, so a plate of unnamed lanes still says which one is off scale. |
| `ladder` | `"generuler_1kb_plus"` · `"hi_lo"` · `"generuler_1kb"` · `"generuler_100bp"` · `"generuler_100bp_plus"` · `"thermo_1kb_plus"` · `"neb_1kb"` · `"neb_100bp"` · `"lambda_hindiii"` · `"penn_state"` |  | `"generuler_1kb_plus"` |  | the reference ladder drawn beside the samples, and what "off the scale" is measured against. Values: generuler_1kb_plus (GeneRuler 1 kb Plus (75–20,000)), hi_lo (Hi-Lo DNA Marker (50–10,000)), generuler_1kb (GeneRuler 1 kb (250–10,000)), generuler_100bp (GeneRuler 100 bp (100–3,000)), generuler_100bp_plus (GeneRuler 100 bp Plus (100–3,000)), thermo_1kb_plus (Thermo 1 Kb Plus (100–15,000)), neb_1kb (NEB 1 kb (500–10,000)), neb_100bp (NEB 100 bp (100–1,517)), lambda_hindiii (Lambda DNA / HindIII (125–23,130)), penn_state (PennState (500–10,000)). |
| `agarose_percent` | number |  |  | 0.3–3 | the casting percentage, which activates a concentration law and a resolving window. LEAVE UNSET for the bench's own default: ladder-calibrated migration, interpolated on the ladder's measured curve with no concentration term. In %. |
| `mobility_model` | `"helling-goodman-boyer"` · `"rill-van-winkle"` |  | `"helling-goodman-boyer"` |  | which empirical agarose-% mobility law — helling-goodman-boyer (Helling–Goodman–Boyer (default)) · rill-van-winkle (Rill/Van Winkle). Values: helling-goodman-boyer (Helling–Goodman–Boyer (default)), rill-van-winkle (Rill/Van Winkle). Only applies when agarose_percent is set. Advanced. |
| `form` | `"linear"` · `"supercoiled"` · `"nicked"` · `"relaxed"` |  | `"linear"` |  | the DNA topology a lane runs at when its bands do not carry one. Only moves a band under a concentration law: ladder-calibrated migration reads every band off the ladder's own curve, and the reading says so rather than leaving the setting silently inert. Advanced. |
| `render_mode` | `"bands"` · `"raster"` · `"both"` |  | `"bands"` |  | how the plate would be drawn. Echoed into the derivation chain because a raster merges what bands separate, so the reading is about a different picture. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `conclusion` | string |  | the one-sentence reading, generated from this run: lanes, bands, the size range they span, and the ladder that positioned them |
| `cautions` | any |  | only the cautions this plate earned, each carrying the measurement that produced it and naming the lane it is about. Empty when every band is measurable |
| `derivation` | any |  | the machinery, one row per fact: what placed the lanes, the ladder that calibrated them and whether its curve is its own or borrowed, the resolving window, each lane`s DNA form, and how the plate is drawn |
| `bands` | any |  | every placed band: lane, length in bp, Rf and migration on the shared coordinate system, and whether this gel can measure it |
| `unmeasurable` | any |  | per lane, the two failures kept apart because different actions fix them: `offScale` (outside the reference ladder entirely — read it off the table) and `outOfWindow` (inside the ladder, outside this percentage`s resolving range — cast a different gel) |
| `calibratedBy` | string |  | the ladder whose measured curve positioned every lane — which is NOT always the ladder drawn: 2 of the 10 built-ins carry (bp, Rf) points, and a gel showing one of the other 8 is positioned on the default curve |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "run_gel_plate",
  "arguments": {
    "lanes": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### score_overhang_fidelity

**Score overhang fidelity**: _What fraction of assemblies will ligate every junction correctly with this overhang set, by measured T4 ligase data?_

Score a Golden Gate junction (fusion-site) set against MEASURED T4 DNA ligase end-joining data. It is the number NEB's Ligase Fidelity Viewer reports: the expected fraction of assemblies in which EVERY junction ligated correctly. This is the quantitative counterpart to check_golden_gate_parts: that says whether the parts will be cut, this says whether the pieces will go back together in the right order. Wire golden_gate_assemble's `overhangs` output straight into it.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The measured ligation frequencies (Potapov 2018) hold for the conditions the dataset was measured under.

**Does not:**
- A dataset's temperature and buffer are its own; other conditions are not modelled.
- Scores the junctions only, not the cutting of the parts.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `overhangs` | string[] | **yes** |  |  | the junction overhangs, one per junction, top strand (e.g. AATG, GCTT). Wire `golden_gate_assemble.overhangs` here, or list them. |
| `enzyme` | string |  |  |  | the Type-IIS enzyme the reaction uses, which picks that enzyme's own measured matrix when one exists. Only applies when dataset is not given. |
| `dataset` | `"BsaI-HFv2"` · `"BsmBI-v2"` · `"Esp3I"` · `"BbsI-HF"` · `"SapI"` · `"T4-01h-25C"` · `"T4-01h-37C"` · `"T4-18h-25C"` · `"T4-18h-37C"` |  |  |  | score against this measured matrix instead of the one the enzyme implies. Values: BsaI-HFv2 (BsaI-HFv2, Golden Gate cycling (4 nt)), BsmBI-v2 (BsmBI-v2, Golden Gate cycling (4 nt)), Esp3I (Esp3I, Golden Gate cycling (4 nt)), BbsI-HF (BbsI-HF, Golden Gate cycling (4 nt)), SapI (SapI, Golden Gate cycling (3 nt)), T4-01h-25C (T4 DNA ligase, 1 h at 25 C (4 nt)), T4-01h-37C (T4 DNA ligase, 1 h at 37 C (4 nt)), T4-18h-25C (T4 DNA ligase, 18 h at 25 C (4 nt)), T4-18h-37C (T4 DNA ligase, 18 h at 37 C (4 nt)). |
| `remedies` | boolean |  | `true` |  | also compute what to CHANGE: the drop-the-worst repair, and replacement candidates for each flagged junction. Off makes the run cheaper on a large set. |
| `replacements_per_junction` | number |  | `10` | 1–20 | how many replacement candidates to rank per flagged junction. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `fidelity` | number |  | expected fraction of fully-correct assemblies, 0-1 |
| `percent` | number | % | the same number as a percentage, which is how every incumbent reports it |
| `dataset` | string |  | the measured matrix actually scored against |
| `junctions` | any |  | per junction: overhang, correct/total measured events, its own fidelity, Watson-Crick strength, and its strongest mismatch partners |
| `worst` | any |  | the weakest junctions, worst first: what to change to raise the score |
| `flags` | any |  | weak, self-misannealing and cross-misannealing junction indices, plus the structural verdict |
| `meaningful` | boolean |  | false when a STRUCTURAL error makes the fidelity number misleading rather than merely bad: do not present `fidelity` on its own when this is false |
| `repair` | any |  | the drop-the-worst repair: which junctions to remove, what is left, and the fidelity that leaves. Null when `remedies` is off |
| `replacements` | any |  | per FLAGGED junction, the best overhangs to swap in, each with the whole set’s fidelity after the swap. Empty when `remedies` is off |
| `atMeasurementCeiling` | boolean |  | true when NO mismatch ligation was measured between any two junctions, so the score is exactly 100%: the floor the source experiment can resolve, not a guarantee |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "score_overhang_fidelity",
  "arguments": {
    "overhangs": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### scrub_restriction_sites

**Scrub restriction sites**: _Which fewest silent codon changes remove the forbidden restriction sites from a CDS?_

Propose the minimal SILENT synonymous edits that remove forbidden restriction sites from a CDS (a design/write).

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The CDS is in frame and the codon choices come from the chosen organism's table.

**Does not:**
- Silent at the protein level only: mRNA structure and codon context are not scored.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `dna` | string | **yes** |  |  | the CDS nucleotide sequence (in frame). |
| `protein` | string | **yes** |  |  | the CDS translation (for silence checking). |
| `table` | string |  |  |  | the codon-usage table to guide synonym choice, BY NAME, as the Codon Usage panel lists it. This is the way to pass a table: it resolves against the tables loaded in this project, so the numbers come from one someone built or fetched. Leave unset and the active table is used. |
| `table_tsv` | string |  |  |  | ONLY for a table you are pasting yourself, measured elsewhere — prefer `table`, which names one this project already has. Do NOT write a table out from memory: codon frequencies are measured data, and a typed one is indistinguishable from a real one in the result. TSV: codon<TAB>count. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `dna` | string |  | the scrubbed CDS (silent edits applied) |
| `fixes` | any |  | one entry per synonymous swap made |
| `fixCount` | number |  | number of codons changed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "scrub_restriction_sites",
  "arguments": {
    "dna": "<string>",
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
