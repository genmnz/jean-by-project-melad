# 🔥 PCR, primers & thermocycling

_Primer design for every kind of PCR, melting temperatures and reaction simulation._

15 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`convert_mass_moles`](#convert_mass_moles) | How many picomoles, or how many copies, is this much of this molecule? |
| [`design_bisulfite_primers`](#design_bisulfite_primers) | Which BSP or MSP primers work on the bisulfite-converted strands, and where are the CpG islands? |
| [`design_codehop`](#design_codehop) | Which hybrid degenerate-core primers does a block of aligned protein give, for homologues too diverged for nucleotide design? |
| [`design_degenerate_primers`](#design_degenerate_primers) | Which degenerate primers amplify every member of this aligned family, and how much of it does each cover? |
| [`design_lamp_primers`](#design_lamp_primers) | Which four core LAMP oligos, and optional loop primers, does this template give, judged against PrimerExplorer V5's criteria? |
| [`design_primer_pairs`](#design_primer_pairs) | Which primer pairs in this window score best on Tm, dimers, hairpins, 3' stability, repeats, clamp and specificity under these weights? |
| [`design_primers`](#design_primers) | Which primer pair amplifies this region, at what Tm, annealing temperature and cycling programme? |
| [`design_sequencing_primers`](#design_sequencing_primers) | Which walk of primers reads this whole region, with what overlap, and what cannot be reached? |
| [`fusion_pcr`](#fusion_pcr) | What single product does overlap-extension PCR give from fragments that share terminal homology? |
| [`multiplex_pcr`](#multiplex_pcr) | What does a primer pool do on these templates: products, off-target binding, template-distinguishing pairs, and the dimer matrix? |
| [`pcr_amplify`](#pcr_amplify) | What product does this primer pair amplify from the template? |
| [`plan_master_mix`](#plan_master_mix) | How much of each reagent goes into a master mix for this many reactions? |
| [`plan_serial_dilution`](#plan_serial_dilution) | How do I make a dilution series from this stock? |
| [`primer_check`](#primer_check) | Where does a primer anneal on this molecule, and how well does each site match? |
| [`solve_dilution`](#solve_dilution) | How much stock, diluent or final concentration does a dilution need? |

---

### convert_mass_moles

**Convert mass moles**: _How many picomoles, or how many copies, is this much of this molecule?_

Convert a mass of a molecule to an amount in moles and a number of molecules, or an amount back to a mass. The weight is the open record's own, computed from its sequence (both strands of a double-stranded record under its topology, a protein from its residues), or one you give.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The sample is the molecule as written: no counter-ions, modifications or water are weighed.

**Does not:**
- The weight is the free acid. A table using an average 660 g/mol per base pair (Promega's BioMath does) gives several percent fewer moles.
- Purity and concentration error are not modelled.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `mass` | number |  |  | ≥ 0 | the mass to convert. Leave it or `amount` empty: the empty one is calculated. |
| `mass_unit` | `"g"` · `"mg"` · `"µg"` · `"ng"` · `"pg"` |  | `"ng"` |  | the unit of the mass, given or solved. |
| `amount` | number |  |  | ≥ 0 | the amount in moles to convert. Leave it or `mass` empty. |
| `amount_unit` | `"mol"` · `"mmol"` · `"µmol"` · `"nmol"` · `"pmol"` · `"fmol"` |  | `"pmol"` |  | the unit of the amount, given or solved. |
| `molecular_weight` | number |  |  | ≥ 0 | g/mol. Leave empty to weigh the open record from its sequence; give it for a molecule that is not open. In g/mol. Advanced. |
| `strands` | `"record"` · `"double"` · `"single"` |  | `"record"` |  | which strands of the open record to weigh. From the record weighs both strands of DNA and the one strand of an RNA (U and no T); choose one strand for an oligo. Values: record (From the record), double (Both strands), single (One strand). Only applies when molecular_weight is not given. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `mass` | number or null |  | the mass, in its unit |
| `amount` | number or null |  | the amount in moles, in its unit |
| `copies` | number or null |  | number of molecules |
| `molecularWeight` | number or null | g/mol | the weight used |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "convert_mass_moles",
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

### design_bisulfite_primers

**Design bisulfite primers**: _Which BSP or MSP primers work on the bisulfite-converted strands, and where are the CpG islands?_

Design BSP or MSP primers for a methylation assay, on the CONVERTED strands: after bisulfite treatment every unmethylated C reads as T, which is a different template from the one every other designer sees. BSP primers avoid CpGs so they amplify regardless of methylation state; MSP primers sit ON CpGs so they discriminate. Also reports the CpG islands (EMBOSS cpgplot) the assay should target.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Conversion is complete: every unmethylated C reads as T.
- BSP avoids CpGs so it amplifies either state; MSP sits on them so it discriminates.

**Does not:**
- The island scan is graded against EMBOSS cpgplot; the primer design has no runnable oracle (MethPrimer is web-only), so every returned pair is re-checked against the published rules by independent recomputation.
- Incomplete conversion is a bench failure mode the design cannot see.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `assay` | `"BSP"` · `"MSP"` |  | `"BSP"` |  | BSP = bisulfite sequencing PCR: primers avoid CpG sites so both methylated and unmethylated template amplify equally, and the methylation is read from the SEQUENCE afterwards. MSP = methylation-specific PCR: primers cover CpG sites so amplification ITSELF is the readout. They answer different questions and are not interchangeable. Values: BSP (BSP - amplify regardless of methylation), MSP (MSP - amplify only one state). |
| `max_results` | number |  | `5` | 1–50 | how many primer pairs to return, best first. |
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to design in. Unset = the whole sequence; pass the selection's start to scope to it. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end. Unset = the whole sequence. Advanced. |
| `criteria` | `"cpgplot"` · `"takaiJones"` |  | `"cpgplot"` |  | which published criteria call a CpG island: Gardiner-Garden & Frommer 1987 as EMBOSS cpgplot encodes it, or the stricter Takai & Jones 2002, which excludes most Alu repeats. Values: cpgplot (Gardiner-Garden & Frommer (cpgplot)), takaiJones (Takai & Jones 2002 (promoter islands)). |
| `island_window` | number |  |  | ≥ 10 | sliding window over which C, G and CpG are counted (cpgplot -window); unset takes the preset's. In bp. Advanced. |
| `island_min_length` | number |  |  | ≥ 10 | minimum island length (cpgplot -minlen); unset takes the preset's. In bp. Advanced. |
| `island_min_obs_exp` | number |  |  | 0–2 | minimum observed/expected CpG (cpgplot -minoe); unset takes the preset's. Advanced. |
| `island_min_percent` | number |  |  | 0–100 | minimum %C+%G (cpgplot -minpc); unset takes the preset's. In %. Advanced. |
| `design_in_island` | number |  |  | ≥ 1 | design inside this island only, by its rank in the reported list (1 = first). Unset designs anywhere in the region; the panel instead asks for an island to be picked. |
| `min_length` | number |  | `20` | 12–40 | shortest primer considered. In nt. Advanced. |
| `opt_length` | number |  | `25` | 12–40 | primer length the ranking prefers. In nt. |
| `max_length` | number |  | `30` | 12–45 | longest primer considered. In nt. Advanced. |
| `min_tm` | number |  | `50` | 35–75 | primers below this Tm are rejected outright. In °C. Advanced. |
| `opt_tm` | number |  | `55` | 35–75 | target Tm; candidates rank by distance from it. Bisulfite-converted DNA is C-poor, so these run lower than an ordinary design. In °C. |
| `max_tm` | number |  | `62` | 35–85 | primers above this Tm are rejected outright. In °C. Advanced. |
| `min_gc` | number |  | `20` | 0–100 | lowest acceptable GC. The floor is low on purpose: after conversion every unmethylated C is a T, so converted DNA is genuinely GC-poor and an ordinary 40% floor rejects correct primers. In %. Advanced. |
| `max_gc` | number |  | `65` | 0–100 | highest acceptable GC. In %. Advanced. |
| `product_min` | number |  | `100` | 50–2000 | shortest acceptable amplicon. In bp. |
| `product_max` | number |  | `400` | 50–3000 | longest acceptable amplicon. In bp. |
| `min_non_cpg_c` | number |  | `2` | 0–10 | BSP ONLY. The fewest non-CpG cytosines the ORIGINAL sequence under a primer must carry - the rule that makes a BSP primer bisulfite-SPECIFIC, because those cytosines become T only if conversion worked. A primer with none anneals to untreated DNA just as well and the assay silently reports on template that was never converted. In nt. |
| `min_cpg` | number |  | `1` | 0–10 | MSP ONLY. The fewest CpG sites a primer must cover, so it can discriminate methylated from unmethylated at all. In sites. |
| `max_cpg_distance_from_3` | number |  | `5` | 0–20 | MSP ONLY. How close to the 3' end the last CpG must sit. A mismatch discriminates most strongly at the 3' end, because that is where the polymerase extends. In nt. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `pairs` | any |  | the primer pairs, best first: each with both oligos, their coordinates on the ORIGINAL unconverted sequence, Tm, GC, CpG count and the non-CpG C conversion check |
| `count` | number |  | how many pairs were found |
| `forward` | string |  | the best pair's forward primer (wire into pcr_amplify) |
| `reverse` | string |  | the best pair's reverse primer |
| `islands` | any |  | CpG islands in the record (EMBOSS cpgplot criteria) - what a methylation assay should be aimed at |
| `islandCount` | number |  | how many CpG islands were found |
| `assay` | string |  | which assay was designed, echoed so a result never has to be guessed at |
| `methylatedPairs` | any |  | MSP: the pairs specific for the METHYLATED allele. Empty under BSP |
| `unmethylatedPairs` | any |  | MSP: the pairs specific for the UNMETHYLATED allele - the other half of the assay, and the control that tells a negative from a failed reaction. Empty under BSP |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_bisulfite_primers",
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

### design_codehop

**Design CODEHOP**: _Which hybrid degenerate-core primers does a block of aligned protein give, for homologues too diverged for nucleotide design?_

Design CODEHOP hybrid oligos from a block of aligned PROTEIN - for homologues too diverged for nucleotide-level design to see at all. Each primer is a 3' DEGENERATE core over a few conserved residues fused to a 5' non-degenerate consensus clamp, back-translated through a codon-usage table. A different algorithm from the degenerate designer, not a variant of it.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- The aligned block is real homology; the clamp is back-translated through the codon table named.

**Does not:**
- Both original CODEHOP servers are gone and no runnable oracle exists, so every number is recomputed in the test by a path that does not call the engine's own predicates.
- Designs primers; it does not predict which homologues amplify.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `alignment` | object[] |  |  |  | the ALIGNED PROTEIN rows, each { name, sequence } in one-letter amino acids with gaps preserved - wire an upstream protein alignment here. At least 3 sequences: the clamp is a CONSENSUS, and two have none worth the name. |
| `alignment_fasta` | string |  |  |  | an aligned PROTEIN FASTA, when there is no upstream alignment to wire. |
| `table` | string | **yes** |  |  | the codon-usage table to back-translate the clamp through, BY NAME as the Codon Usage panel lists it. REQUIRED and deliberately without a default: a CODEHOP designed under the wrong organism's usage is wrong in a way nothing downstream can detect, so picking one here would silently pick a host (§1). |
| `block_index` | number |  | `0` | 0–200 | which gapless block to design in, 0-based, ordered as `gaplessBlocks` returns them (blocks of at least 8 ungapped columns). Unset = the first. |
| `strand` | `"forward"` · `"reverse"` · `"both"` |  | `"both"` |  | which strand to design on. `both` returns forward and reverse sets, which is what a PCR needs. |
| `max_core_degeneracy` | number |  | `128` | 2–4096 | degeneracy ceiling for the 3' core (Rose 2003 step 7: "a maximum degeneracy of 128"). |
| `clamp_tm` | number |  | `60` | 40–80 | target melting temperature for the non-degenerate 5' clamp (Rose 2003 step 8: "the current default is 60 °C, which usually provides a clamp of ~20 nucleotides"), measured as nearest-neighbour Tm in the buffer `conditions` names. In °C. |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method and any additives the clamp Tm is measured in. Left unset it is filled from your reaction-conditions settings, and falls back to pydna's Taq defaults (SantaLucia & Hicks 2004 table, 250 nM primer, Owczarzy 2008 salt correction) when there are none. Advanced. |
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
| `max_run` | number |  | `5` | 2–12 | longest single-base run allowed; 2003's stated polynucleotide run limit. A primer exceeding it is rejected. In nt. Advanced. |
| `base_cutoff` | number |  | `0` | 0–1 | minimum predicted probability for a base to enter the degenerate core. Advanced. |
| `max_clamp_length` | number |  | `40` | 10–100 | ceiling on clamp growth, so an unreachable Tm REFUSES instead of consuming the whole block. Ours, and a stop condition rather than a published criterion - 40 nt is already twice the ~20 the paper expects. In nt. Advanced. |
| `genetic_code_id` | number |  | `1` | 1–33 | NCBI `transl_table` id for the codon-to-residue map. Advanced. |
| `core_lengths` | number[] |  | `[11, 12]` |  | core lengths the scan tries, in residues — every length here is scanned and the best-scoring core kept. Advanced. |
| `weighting` | `"pb"` · `"none"` |  | `"pb"` |  | how the alignment's rows are weighted before the core's consensus is read. Values: pb (Position-based (Henikoff & Henikoff 1994)), none (None — every row counts once). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `primers` | any |  | the designed oligos: each with its degenerate 3' core, its consensus 5' clamp, the residues it covers and its degeneracy |
| `primerCount` | number |  | how many oligos were designed |
| `forward` | string |  | the first forward oligo, clamp + core |
| `reverse` | string |  | the first reverse oligo |
| `rejections` | any |  | why each candidate position was rejected - degeneracy, run length, or a clamp that could not reach the Tm |
| `blockCount` | number |  | how many gapless blocks the alignment offers, so a caller can see there were others to choose |
| `table` | string |  | which codon table the clamp was back-translated through, named so a design is never unattributable |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_codehop",
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

### design_degenerate_primers

**Design degenerate primers**: _Which degenerate primers amplify every member of this aligned family, and how much of it does each cover?_

Design degenerate primers from a multiple-sequence ALIGNMENT - the 'amplify every homologue in this family' question, which a single-template designer cannot answer because it only ever sees one sequence. A faithful port of DegePrime (Hugerth et al. 2014). Wire an upstream align_sequences `rows` output straight in, or paste an aligned FASTA.

<sub>returns new records · runs locally on the engine · randomised, reproducible with its seed</sub>

**Assumes:**
- The alignment is the family's; DegePrime's window and degeneracy rules apply.

**Does not:**
- DegePrime's own oligo comes from a randomised unseeded search that no port can reproduce, so it is used as a bar our search must clear at every window, with an exact branch-and-bound as the third check.
- Coverage is over the alignment given, not over the family in nature.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `alignment` | object[] |  |  |  | the ALIGNED rows to scan, each `{ name, sequence }` with gaps preserved - wire an upstream `align_sequences` rows output here. Gaps carry information the scan reads, so an unaligned set is not a substitute. |
| `alignment_fasta` | string |  |  |  | an aligned FASTA to scan, when there is no upstream alignment to wire. Sequences must already BE aligned - equal length, gaps as `-`. |
| `algorithm` | `"wrm"` · `"summation"` · `"expansion"` · `"constriction"` · `"exhaustive"` |  | `"wrm"` |  | which search picks each window's oligo. `wrm` is DegePrime's own default and is randomised (hence `seed`); `exhaustive` is an exact branch-and-bound that GRADES the heuristics rather than letting them grade each other, and REFUSES a window too large to solve rather than guessing - the problem is NP-hard. |
| `length` | number |  | `16` | 8–40 | oligomer length (DegePrime `-l`). In nt. |
| `max_degeneracy` | number |  | `4` | 1–4096 | degeneracy ceiling (`-d`) - how many distinct oligos the IUPAC code is allowed to stand for. Coerced DOWN when no combination of positions can multiply to it, and the run says so. |
| `min_product` | number |  | `300` | 50–5000 | shortest product, in TRIMMED alignment columns. In col. |
| `max_product` | number |  | `800` | 50–10000 | longest product, in TRIMMED alignment columns. In col. |
| `min_fraction_matching` | number |  | `0.8` | 0–1 | a window must bind at least this fraction of the spanning sequences to be a candidate - the coverage floor, and the number that decides whether 'every homologue' is true. |
| `trim_cutoff` | number |  | `0.9` | 0–1 | columns occupied by less than this fraction of sequences are dropped before scanning. Trimming renumbers the alignment, which is why `keptColumns` comes back with the result. Advanced. |
| `min_depth` | number |  | `1` | 1–1000 | fewest gapless sequences a window needs before it is reported at all (`-depth`). Advanced. |
| `skip` | number |  | `20` | 0–200 | bases excluded at each end of every sequence (`-skip`). In nt. Advanced. |
| `iterations` | number |  | `100` | 1–10000 | WRM restarts (`-iter`). Only applies when algorithm is wrm. Advanced. |
| `seed` | number |  | `1` | 0–1000000 | seed for WRM's draw, so a run is REPRODUCIBLE. Upstream is unseeded, so the same alignment can give two answers; a design you cannot reproduce is not one you can order from. Only applies when algorithm is wrm. Advanced. |
| `exhaustive_mer_limit` | number |  | `22` | 2–64 | largest number of distinct mers `exhaustive` will attempt before refusing a window. Only applies when algorithm is exhaustive. Advanced. |
| `limit` | number |  | `100` | 1–1000 | how many pairs to return, best coverage first. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `pairs` | any |  | the primer pairs, best coverage first: both oligos in IUPAC letters, their degeneracy, the fraction of the family each binds, and the product span in trimmed columns |
| `pairCount` | number |  | how many pairs were found |
| `forward` | string |  | the best pair's forward oligo, IUPAC. Empty when no pair satisfied the constraints |
| `reverse` | string |  | the best pair's reverse oligo AS ORDERED (reverse-complemented). Empty when no pair satisfied the constraints |
| `windows` | any |  | every scanned window with its degeneracy, entropy and coverage - the scan behind the pairs |
| `keptColumns` | any |  | which columns of the ORIGINAL alignment survived trimming - trimmed column 40 is not alignment column 40, and this is the map back |
| `maxDegeneracyUsed` | number |  | the degeneracy ceiling actually applied - LOWER than asked when no combination of IUPAC positions can multiply to the request |
| `degeneracyCoerced` | boolean |  | true when the ceiling was lowered, so a run never silently answers a different question than it was asked |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_degenerate_primers",
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

### design_lamp_primers

**Design LAMP primers**: _Which four core LAMP oligos, and optional loop primers, does this template give, judged against PrimerExplorer V5's criteria?_

Design LAMP (loop-mediated isothermal amplification) primer SETS - four core oligos (F3 · B3 · FIP · BIP) plus optional loop primers, judged against Eiken's own PrimerExplorer V5 criteria. Not a pair: LAMP needs six binding regions in the published order and the distances BETWEEN them are as much of the design as the oligos. Each set comes back with the arithmetic behind its rank.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Eiken's published distance, Tm and free-energy criteria define an acceptable set.
- Melting temperatures are the nearest-neighbour model's at the stated conditions.

**Does not:**
- No runnable LAMP designer exists to grade against, so every returned set is re-checked against the published criteria by independent recomputation, over every set rather than a sample.
- Designs sets; amplification time and specificity on the bench are not predicted.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to design into (LAMP designs into a stretch, not a whole plasmid). Unset = the whole sequence; pass the selection's start to scope to it. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end. Unset = the whole sequence. Advanced. |
| `max_sets` | number |  | `5` | 1–50 | how many sets to return, best first. |
| `loop_primers` | boolean |  | `true` |  | design LF/LB as well. They are optional in LAMP and accelerate the reaction. |
| `end_stability_dg` | number |  | `4` | 0–10 | the terminal-6-base stability rule (manual §2.2: the ΔG "is -4 kcal/mol or less"). In kcal/mol. Advanced. |
| `end_stability_nt` | number |  | `6` | 2–12 | how many terminal bases the end-stability rule measures (manual §2.2: 6). In nt. Advanced. |
| `length_min` | number |  |  |  | length window for the outer/inner binding regions (manual §4.2) - lower bound. Unset = the preset for this template's GC class. In nt. Advanced. |
| `length_max` | number |  |  |  | length window for the outer/inner binding regions (manual §4.2) - upper bound. Unset = the preset for this template's GC class. In nt. Advanced. |
| `tm_inner_min` | number |  |  |  | Tm window for F1c / B1c - the manual's "about 65 °C" - lower bound. Unset = the preset for this template's GC class. In °C. Advanced. |
| `tm_inner_max` | number |  |  |  | Tm window for F1c / B1c - the manual's "about 65 °C" - upper bound. Unset = the preset for this template's GC class. In °C. Advanced. |
| `tm_outer_min` | number |  |  |  | Tm window for F2 / B2 / F3 / B3 - the manual's "about 60 °C" - lower bound. Unset = the preset for this template's GC class. In °C. Advanced. |
| `tm_outer_max` | number |  |  |  | Tm window for F2 / B2 / F3 / B3 - the manual's "about 60 °C" - upper bound. Unset = the preset for this template's GC class. In °C. Advanced. |
| `tm_loop_min` | number |  |  |  | Tm window for the loop primers LF / LB - lower bound. Unset = the preset for this template's GC class. In °C. Advanced. |
| `tm_loop_max` | number |  |  |  | Tm window for the loop primers LF / LB - upper bound. Unset = the preset for this template's GC class. In °C. Advanced. |
| `gc_min` | number |  |  |  | GC FRACTION window, 0-1 (manual §2.3: "between about 40% to 65%") - lower bound. Unset = the preset for this template's GC class. Advanced. |
| `gc_max` | number |  |  |  | GC FRACTION window, 0-1 (manual §2.3: "between about 40% to 65%") - upper bound. Unset = the preset for this template's GC class. Advanced. |
| `amplified_span_min` | number |  |  |  | F2 5' to B2 5', the amplified region. THE TWO AUTHORITIES DISAGREE: PrimerExplorer V5 says 120-160, the Eiken genome site 120-180; the default follows PrimerExplorer and this is the knob for the other reading - lower bound. Unset = the preset for this template's GC class. In bp. Advanced. |
| `amplified_span_max` | number |  |  |  | F2 5' to B2 5', the amplified region. THE TWO AUTHORITIES DISAGREE: PrimerExplorer V5 says 120-160, the Eiken genome site 120-180; the default follows PrimerExplorer and this is the knob for the other reading - upper bound. Unset = the preset for this template's GC class. In bp. Advanced. |
| `loop_span_min` | number |  |  |  | 5' of F2 to 5' of F1 - the portion that forms the loop (manual §2.5: 40-60) - lower bound. Unset = the preset for this template's GC class. In bp. Advanced. |
| `loop_span_max` | number |  |  |  | 5' of F2 to 5' of F1 - the portion that forms the loop (manual §2.5: 40-60) - upper bound. Unset = the preset for this template's GC class. In bp. Advanced. |
| `outer_gap_min` | number |  |  |  | F3 to F2 and B3 to B2 gap. THE TWO AUTHORITIES DISAGREE here too: PrimerExplorer V5 says 0-60, the Eiken genome site 0-20 - lower bound. Unset = the preset for this template's GC class. In bp. Advanced. |
| `outer_gap_max` | number |  |  |  | F3 to F2 and B3 to B2 gap. THE TWO AUTHORITIES DISAGREE here too: PrimerExplorer V5 says 0-60, the Eiken genome site 0-20 - upper bound. Unset = the preset for this template's GC class. In bp. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sets` | any |  | the primer sets, best first: six regions in the literature order with every measurement that decided each one |
| `setCount` | number |  | how many sets were found |
| `fip` | string |  | the best set's FIP (F1c + F2), as ordered |
| `bip` | string |  | the best set's BIP (B1c + B2), as ordered |
| `f3` | string |  | the best set's F3 outer primer |
| `b3` | string |  | the best set's B3 outer primer |
| `penaltyTerms` | any |  | what the best set's rank is MADE OF - one entry per criterion with the value measured, the window it was judged against and its cost. The costs sum to the penalty |
| `targetClass` | string |  | which preset the search ran under - atRich, normal or gcRich, chosen from the template's own GC content (manual §4.3) |
| `constraints` | any |  | every window the search actually ran under, so a readout never has to restate them or guess which preset applied |
| `offset` | number |  | where the designed-in stretch starts in the record: add it to every position above for record coordinates. 0 unless a region was given |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_lamp_primers",
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

### design_primer_pairs

**Design primer pairs**: _Which primer pairs in this window score best on Tm, dimers, hairpins, 3' stability, repeats, clamp and specificity under these weights?_

The Primer Designer's own ranked search: scan the open record for primer pairs inside a product-size, Tm, length and GC window, score every candidate on Tm, dimers, hairpins, 3' stability, repeats, clamp and specificity under weights you set, and return the best N. With `task: existing`, supply one primer and it designs the mate. Emits the top pair so a downstream pcr_amplify runs on it. For a sequencing walk use design_sequencing_primers; for pydna's single-pair designer use design_primers.

<sub>returns new records · runs locally on the engine · long-running</sub>

**Assumes:**
- Primer3's thermodynamic model and the Tm conditions named.
- The weights given decide the ranking.

**Does not:**
- Specificity is against the open record and the mispriming library given, not a genome.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `task` | `"new"` · `"existing"` |  | `"new"` |  | `new` ranks candidate pairs; `existing` keeps the primer you supply and designs its mate. |
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to design within. Unset = the whole template. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end of the region to design within. Advanced. |
| `target_start` | number |  |  | ≥ 0 | 0-based inclusive start of a target the amplicon must flank, with no primer on it. Advanced. |
| `target_end` | number |  |  | ≥ 0 | 0-based inclusive end of the target. Advanced. |
| `product_size_min` | number |  | `300` | ≥ 40 | shortest acceptable amplicon. In bp. |
| `product_size_max` | number |  | `700` | ≥ 40 | longest acceptable amplicon. In bp. |
| `target_tm` | number |  | `60` | 40–75 | the Tm each primer is scored toward. In °C. |
| `tm_window_min` | number |  | `57` |  | lowest primer Tm accepted at all. In °C. |
| `tm_window_max` | number |  | `63` |  | highest primer Tm accepted at all. In °C. |
| `primer_length_min` | number |  | `18` | ≥ 8 | shortest primer. In nt. |
| `primer_length_max` | number |  | `27` | ≥ 8 | longest primer. In nt. |
| `gc_min` | number |  | `40` | 0–100 | lowest primer GC accepted. In %. |
| `gc_max` | number |  | `60` | 0–100 | highest primer GC accepted. In %. |
| `n_pairs` | number |  | `5` | 1–50 | how many ranked pairs to return. |
| `mispriming_library` | `"none"` · `"human"` · `"rodent"` · `"drosophila"` |  | `"none"` |  | a Primer3 repeat library to screen every primer against. `none` skips the screen. Advanced. |
| `existing_forward` | string |  |  |  | with `task: existing`, the forward primer to keep. Only applies when task is existing. |
| `existing_reverse` | string |  |  |  | with `task: existing`, the reverse primer to keep. Only applies when task is existing. |
| `fwd_tail` | string |  |  |  | 5' non-annealing tail added to every forward primer (a restriction site or adapter). The footprint, and so binding and Tm, is unchanged. Advanced. |
| `rev_tail` | string |  |  |  | 5' non-annealing tail added to every reverse primer. Advanced. |
| `weight_tm` | number |  | `1` | ≥ 0 | scoring weight for the `tm` penalty (0 switches it off). Advanced. |
| `weight_tm_pair` | number |  | `1` | ≥ 0 | scoring weight for the `tmPair` penalty (0 switches it off). Advanced. |
| `weight_gc` | number |  | `0.5` | ≥ 0 | scoring weight for the `gc` penalty (0 switches it off). Advanced. |
| `weight_length` | number |  | `0.3` | ≥ 0 | scoring weight for the `length` penalty (0 switches it off). Advanced. |
| `weight_self_dimer` | number |  | `1.5` | ≥ 0 | scoring weight for the `selfDimer` penalty (0 switches it off). Advanced. |
| `weight_self_end` | number |  | `3` | ≥ 0 | scoring weight for the `selfEnd` penalty (0 switches it off). Advanced. |
| `weight_hairpin` | number |  | `1.5` | ≥ 0 | scoring weight for the `hairpin` penalty (0 switches it off). Advanced. |
| `weight_cross_dimer` | number |  | `1.5` | ≥ 0 | scoring weight for the `crossDimer` penalty (0 switches it off). Advanced. |
| `weight_cross_end` | number |  | `3` | ≥ 0 | scoring weight for the `crossEnd` penalty (0 switches it off). Advanced. |
| `weight_end3` | number |  | `1` | ≥ 0 | scoring weight for the `end3` penalty (0 switches it off). Advanced. |
| `weight_poly_x` | number |  | `1` | ≥ 0 | scoring weight for the `polyX` penalty (0 switches it off). Advanced. |
| `weight_di_repeat` | number |  | `1` | ≥ 0 | scoring weight for the `diRepeat` penalty (0 switches it off). Advanced. |
| `weight_gc_clamp` | number |  | `1` | ≥ 0 | scoring weight for the `gcClamp` penalty (0 switches it off). Advanced. |
| `weight_specificity` | number |  | `6` | ≥ 0 | scoring weight for the `specificity` penalty (0 switches it off). Advanced. |
| `weight_mispriming` | number |  | `4` | ≥ 0 | scoring weight for the `mispriming` penalty (0 switches it off). Advanced. |
| `excluded` | object[] |  |  |  | spans no primer may sit on, as find_primer_snps' `excluded` emits them: a list of {start, end}, 0-based and end-exclusive, where start = end is an insertion between two bases. The amplicon may run across them. The panel's Avoid known SNPs. Advanced. |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method the Tm window is measured in. Left unset it is filled from your reaction-conditions settings, as the panel's are. Advanced. |
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
| `forward` | string |  | the top pair's forward primer (wire into pcr_amplify) |
| `reverse` | string |  | the top pair's reverse primer |
| `pairs` | any |  | every returned pair in rank order: score, both primers (sequence, span, Tm, GC), product length, Tm and Ta |
| `pairCount` | number |  | how many pairs came back |
| `ta` | number | °C | the top pair's annealing temperature [°C] |
| `productLen` | number | bp | the top pair's amplicon length [bp] |
| `shortfall` | string |  | why fewer pairs came back than were asked for; empty when the run was not short |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_primer_pairs",
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

### design_primers

**Design primers**: _Which primer pair amplifies this region, at what Tm, annealing temperature and cycling programme?_

Design a forward + reverse primer pair to amplify the subject (pydna `primer_design`), with Tm, Ta and suggested Taq/Phusion cycling programs. Emits both primers so a downstream pcr_amplify runs on them — the design→PCR→gel loop.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Tm is the nearest-neighbour model's at the stated salt and primer conditions; the cycling programme follows the polymerase named.

**Does not:**
- Designs a pair; screening it for dimers, hairpins and off-target sites is screen_oligo_structure's and primer_check's job.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `target_tm` | number |  | `55` | 40–75 | target melting temperature (pydna default 55). In °C. |
| `conditions` | object |  |  |  | salt, magnesium, dNTP and oligo concentrations plus the salt-correction method and any additives the target Tm is measured in. Left unset it is filled from your reaction-conditions settings, and falls back to the nearest-neighbour defaults when there are none. Advanced. |
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
| `limit` | number |  | `13` | 8–40 | minimum primer length (pydna `limit`). In bp. Advanced. |
| `forward_primer` | string |  |  |  | supply one primer to design only its mate. Advanced. |
| `reverse_primer` | string |  |  |  | supply one primer to design only its mate. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `forward` | string |  | forward primer 5'→3' (wire into pcr_amplify) |
| `reverse` | string |  | reverse primer 5'→3' (wire into pcr_amplify) |
| `forwardTm` | number | °C | forward primer Tm [°C] |
| `reverseTm` | number | °C | reverse primer Tm [°C] |
| `ta` | number | °C | suggested annealing temperature [°C] |
| `productTm` | number | °C | amplicon melting temperature [°C] (Rychlik 1990, at the run's own monovalent salt) — 70% of `ta` on the Taq path |
| `productLen` | number | bp | amplicon length [bp] |
| `program` | string |  | suggested Taq cycling program |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_primers",
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

### design_sequencing_primers

**Design sequencing primers**: _Which walk of primers reads this whole region, with what overlap, and what cannot be reached?_

Design a WALK of sequencing primers that reads a whole region, not one pair: tiled reads with confirmed overlap, on both strands by default, plus the coverage the walk actually achieves and any stretch it cannot reach. This is the 'how do I read all 6 kb of this construct' question, which a single pair does not answer. Read length and dead zone default to a named facility's published figures (MSU RTSF, ABI 3730XL) rather than to round numbers.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Read length and dead zone are the facility's published figures, or the ones given.

**Does not:**
- Reports the coverage the walk achieves and any stretch it cannot reach rather than claiming full coverage.
- Each primer is the graded pair designer's; what this adds is the walk, whose coverage the test re-derives by a second algorithm.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `read_length` | number |  | `800` | 100–1200 | usable bases per read, AFTER the dead zone. Default 800 is the shortest read MSU RTSF Genomics Core, Sanger Sequencing Best and Worst Practices (2024-04-25), ABI 3730XL promises (it quotes 800-900), which is the cautious end of a published range rather than a round number. In bp. |
| `dead_zone` | number |  | `35` | 0–100 | bases at the start of a read that are not trustworthy. Default 35 is the LONGEST the same source warns about (it says the first 25-35 bases are poor), so an untouched walk is the cautious reading in both directions. In bp. Advanced. |
| `overlap` | number |  | `100` | 0–400 | confirmed overlap required between consecutive reads on one strand. Overlap is what turns abutting reads into a contig. Default 100 has NO published source and is a judgement, which is why it is stated rather than dressed as a figure. In bp. |
| `both_strands` | boolean |  | `true` |  | read every base from both directions - what a sequencing facility means by double-stranded coverage, and the standard for anything deposited or published. |
| `region_start` | number |  |  | ≥ 0 | 0-based inclusive start of the region to read. Unset = the whole template. Advanced. |
| `region_end` | number |  |  | ≥ 0 | 0-based inclusive end of the region to read. Unset = the whole template. Advanced. |
| `target_tm` | number |  |  | 40–75 | target melting temperature for each primer in the walk. In °C. Advanced. |
| `min_length` | number |  |  | 8–40 | shortest acceptable primer. In bp. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `reads` | any |  | one entry per primer in the walk: name (F1, R1, ...), sequence, strand, and the stretch it is expected to read |
| `primers` | any |  | just the primer sequences, in walk order, for ordering |
| `readCount` | number |  | how many primers the walk needs |
| `complete` | boolean |  | true when every base of the region is read at least once |
| `doubleStranded` | boolean |  | true when every base is read from both directions |
| `gaps` | any |  | stretches no read reaches - empty means the region is fully read |
| `singleStranded` | any |  | stretches read from one strand only, when both were asked for |
| `coverage` | any |  | every stretch of the region, contiguous and in order, with its depth |
| `skipped` | any |  | anchors where no primer could be designed, each with the reason - never a silently short walk |
| `used` | any |  | the parameters the plan was actually built under, so a readout never restates them |
| `authority` | any |  | the published source the read-length and dead-zone defaults come from |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "design_sequencing_primers",
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

### fusion_pcr

**Fusion PCR**: _What single product does overlap-extension PCR give from fragments that share terminal homology?_

Overlap-extension (fusion) PCR — join fragments that share terminal homology into one product, carrying their features across (pydna). Emits the fused product as a NEW record.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Adjacent fragments share enough terminal homology to anneal and extend.

**Does not:**
- Does not model mispriming, the polymerase or cycling; the overlap rule is sequence identity.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `fragments` | (string or object)[] |  |  |  | the fragments to fuse, in order — wire upstream `record` outputs here, or name library documents. |
| `include_subject` | boolean |  | `true` |  | also include the node's subject as the first fragment. |
| `limit` | number |  | `15` | 6–100 | minimum shared terminal homology two fragments must have to fuse (pydna's own default is 15). In bp. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the fused product, as a record |
| `products` | any |  | every fused product |
| `productCount` | number |  | number of products (>1 = ambiguous fusion) |
| `productTm` | number | °C | product melting temperature of the first product |
| `junctions` | any |  | the first product's joins: each overlap's product coordinates (0-based inclusive), bases, length and Tm |
| `report` | string |  | the engine's own summary (count + sizes) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "fusion_pcr",
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

### multiplex_pcr

**Multiplex PCR**: _What does a primer pool do on these templates: products, off-target binding, template-distinguishing pairs, and the dimer matrix?_

Screen a primer POOL against one or more templates: every predicted product, per-primer off-target binding, the pairs that tell templates apart on a gel, and the all-against-all primer-dimer matrix a pool actually lives or dies by (pydna primer_screen + primer3 thal).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Annealing follows pydna's rule; dimer free energies are primer3 thal's at the stated conditions.

**Does not:**
- Predicts products and interactions, not the yields that decide a multiplex on the bench.
- Products are those the templates given can make; a genome may hold others.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `primers` | string[] |  |  |  | the primer pool — literal sequences, or wire primer outputs from upstream design nodes. |
| `templates` | (string or object)[] |  |  |  | extra templates to screen against — wire records or name library documents (the subject is included by default). |
| `include_subject` | boolean |  | `true` |  | screen against the node's subject as a template. |
| `limit` | number |  | `16` | 8–40 | minimum 3' footprint match for a primer to be considered bound (pydna's own default is 16). In bp. |
| `min_size` | number |  | `50` | 20–2000 | smallest product to report. In bp. |
| `max_size` | number |  | `5000` | 100–20000 | largest product to report. In bp. |
| `conditions` | object |  |  |  | the reaction buffer every temperature here is computed in - Na+/K+/Tris/Mg2+/dNTPs, the primer concentration, the salt-correction method and the melting model. Left unset it is filled from your reaction-conditions settings, so this node and the PCR panel describe ONE tube; with neither it falls back to pydna's Taq defaults, which is what every golden was captured under. Advanced. |
| `pool` | boolean |  | `false` |  | also partition the screened reactions into compatible tubes (MultiPLX grouping), judged by the preset and cutoffs below. |
| `pool_preset` | `"high"` · `"normal"` · `"low"` · `"primer3"` |  | `"normal"` |  | which authority's limits a tube is judged by: MultiPLX's three stringencies, or primer3's own structural limits (calibrated for the ΔG engine computing the scores). Only applies when pool is true. |
| `max_groups` | number |  | `12` |  | most tubes the pool may be split into. Only applies when pool is true. |
| `max_per_group` | number |  | `6` |  | most reactions one tube may hold. Only applies when pool is true. |
| `cutoff_prim_prim_end2` | number |  |  |  | Primer–primer, both 3′ ends [kcal/mol]: A blunt 3′–3′ dimer: each primer can extend on the other, so the pair consumes itself and makes a short artefact band. Unset keeps the preset's value. In kcal/mol. Only applies when pool is true. Advanced. |
| `cutoff_prim_prim_end1` | number |  |  |  | Primer–primer, one 3′ end [kcal/mol]: One primer's 3′ end anneals anywhere on the other. Extendable, so it competes with the template. Unset keeps the preset's value. In kcal/mol. Only applies when pool is true. Advanced. |
| `cutoff_prim_prim_any` | number |  |  |  | Primer–primer, anywhere [kcal/mol]: Any duplex between two primers. Not extendable on its own, but it takes primer out of the reaction. Unset keeps the preset's value. In kcal/mol. Only applies when pool is true. Advanced. |
| `cutoff_prim_prod_end1` | number |  |  |  | Primer–product, 3′ end [kcal/mol]: A primer's 3′ end annealing inside another reaction's amplicon: it primes on the wrong molecule. Unset keeps the preset's value. In kcal/mol. Only applies when pool is true. Advanced. |
| `cutoff_prim_prod_any` | number |  |  |  | Primer–product, anywhere [kcal/mol]: Any duplex between a primer and another reaction’s amplicon. Unset keeps the preset's value. In kcal/mol. Only applies when pool is true. Advanced. |
| `cutoff_max_prim_prim_any_tm` | number |  |  |  | Cross-dimer Tm, anywhere [°C]: primer3's own limit, on the scale our ΔG engine is calibrated for. A dimer melting above this competes with template annealing. Unset keeps the preset's value. In °C. Only applies when pool is true. Advanced. |
| `cutoff_max_prim_prim_end_tm` | number |  |  |  | Cross-dimer Tm, 3′ end [°C]: primer3's limit for the 3′-end dimer: the configuration that extends. Unset keeps the preset's value. In °C. Only applies when pool is true. Advanced. |
| `cutoff_min_prod_len_diff` | number |  |  |  | Band separation (ladder) [bp]: Products in one tube must differ by at least this much, or the bands co-migrate and you cannot tell which reaction worked. Unset keeps the preset's value. In bp. Only applies when pool is true. Advanced. |
| `cutoff_max_prod_len_diff` | number |  |  |  | Band spread (range) [bp]: Products in one tube must differ by no more than this, so one extension time suits them all. Unset keeps the preset's value. In bp. Only applies when pool is true. Advanced. |
| `cutoff_max_tm_diff` | number |  |  |  | Primer Tm spread [°C]: Largest primer Tm difference allowed inside a tube: one annealing temperature has to work for every reaction in it. Unset keeps the preset's value. In °C. Only applies when pool is true. Advanced. |
| `cutoffs_off` | (`"cutoff_prim_prim_end2"` · `"cutoff_prim_prim_end1"` · `"cutoff_prim_prim_any"` · `"cutoff_prim_prod_end1"` · `"cutoff_prim_prod_any"` · `"cutoff_max_prim_prim_any_tm"` · `"cutoff_max_prim_prim_end_tm"` · `"cutoff_min_prod_len_diff"` · `"cutoff_max_prod_len_diff"` · `"cutoff_max_tm_diff"`)[] |  |  |  | cutoffs to switch off (not applied at all), whatever the preset says. Only applies when pool is true. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `amplicons` | any |  | every predicted product (which pair, which template, what size) |
| `ampliconCount` | number |  | number of predicted products |
| `primerStats` | any |  | per-primer binding counts, including off-target |
| `diagnostics` | any |  | pairs that discriminate the templates by product size |
| `crossDimers` | any |  | all-against-all primer-dimer matrix, or null with fewer than two primers |
| `dimerMap` | object or null |  | the all-against-all dimer ΔG as a heatmap, the most stable structure each pair forms anywhere along the oligos |
| `dimerMap.rows` | string[] |  |  |
| `dimerMap.cols` | string[] |  |  |
| `dimerMap.values` | ((number or null)[])[] |  |  |
| `dimerMap.label` | string |  |  |
| `dimerMap.title` | string |  |  |
| `pools` | any |  | with `pool` on: the tubes, the per-tube verification, and a refusal naming the limit and pair that forced it when no partition fits |
| `poolCount` | number |  | with `pool` on: how many tubes the partition needed (0 when it refused) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "multiplex_pcr",
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

### pcr_amplify

**PCR amplify**: _What product does this primer pair amplify from the template?_

Amplify the subject template with a forward + reverse primer (pydna Anneal). Emits the first product as a NEW sequence record so downstream tools (digest, gel, map) operate on the amplicon, not the template — the tool→tool hand-off.

<sub>returns new records · runs locally on the engine</sub>

**Assumes:**
- Primers anneal where their 3' end matches by pydna's annealing rule.

**Does not:**
- Predicts the product sequence, not its yield; only the first product is emitted.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `forward` | string | **yes** |  |  | forward primer 5'→3'. |
| `reverse` | string | **yes** |  |  | reverse primer 5'→3'. |
| `limit` | number |  | `13` | 6–40 | min 3' footprint match length (pydna `limit`). In bp. Advanced. |
| `mismatches` | number |  | `0` | 0–5 | substitutions a primer may carry and still prime (QUEEN `{s<=N}`). 0 is pydna's exact search, which is what the panel opens on and what every golden was captured under. Advanced. |
| `end_length` | number |  | `3` | 1–10 | 3'-most bases that must pair exactly whatever the mismatch budget (QUEEN `endlength`) — a polymerase extends from a paired 3' terminus, so this is not negotiable by the budget. Advanced. |
| `dimer_threshold` | number |  | `-4.43` | -40–0 | the dimer-free cut-off `primerDimerScore` is judged against (PCR-35). The default is the value PrimerROC publishes, which that paper fitted on its own gels and says is specific to its PCR conditions — refit it on your own gel-scored pairs with `primerRocFit` rather than guessing one. Advanced. |
| `nn_table` | `"DNA_NN1"` · `"DNA_NN2"` · `"DNA_NN3"` · `"DNA_NN4"` · `"RNA_NN1"` · `"RNA_NN2"` · `"RNA_NN3"` · `"R_DNA_NN1"` |  | `"DNA_NN4"` |  | nearest-neighbour table the Tm and Ta are computed on. Left unset it is the panel's own default, SantaLucia & Hicks 2004 unified. Values: DNA_NN1 (Breslauer 1986), DNA_NN2 (Sugimoto 1996), DNA_NN3 (Allawi & SantaLucia 1997), DNA_NN4 (SantaLucia & Hicks 2004 (unified)), RNA_NN1 (Freier 1986 (RNA/RNA)), RNA_NN2 (Xia 1998 (RNA/RNA)), RNA_NN3 (Chen 2012 (RNA/RNA, GU wobble)), R_DNA_NN1 (Sugimoto 1995 (RNA/DNA hybrid)). Advanced. |
| `dmso` | number |  | `0` | 0–20 | DMSO in the reaction, % (v/v) — depresses every primer Tm and therefore the annealing temperature. In %. Advanced. |
| `dmso_model` | `"ahs01"` · `"mus81"` · `"cul76"` · `"esc80"` |  | `"ahs01"` |  | which published DMSO depression to apply; they disagree by 2 °C at 8% DMSO, so a Tm quoted without naming one is not reproducible. Values: ahs01 (Ahsen et al. (2001)), mus81 (Musielski et al. (1981)), cul76 (Cullen and Bick (1976)), esc80 (Escara and Hutton (1980)). Only applies when dmso is set. Advanced. |
| `conditions` | object |  |  |  | the reaction buffer every temperature here is computed in - Na+/K+/Tris/Mg2+/dNTPs, the primer concentration, the salt-correction method and the melting model. Left unset it is filled from your reaction-conditions settings, so this node and the PCR panel describe ONE tube; with neither it falls back to pydna's Taq defaults, which is what every golden was captured under. Advanced. |
| `inner_forward` | string |  |  |  | nested PCR: the inner forward primer 5'→3'. With `inner_reverse`, `forward`/`reverse` are the outer pair and every output below describes ROUND 2. Advanced. |
| `inner_reverse` | string |  |  |  | nested PCR: the inner reverse primer 5'→3'. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `record` | object or null |  | the amplicon as a sequence record (subject for downstream nodes) |
| `sequence` | string |  | amplicon sequence 5'→3'. Empty when the pair made no product |
| `productCount` | number |  | number of products (>1 = non-specific pair) |
| `annealingTempC` | number or null | °C | annealing temperature for the first product, under the Taq convention. Null when the pair made no product |
| `forwardTmC` | number | °C | forward primer melting temperature, under the table and additives set above |
| `reverseTmC` | number | °C | reverse primer melting temperature |
| `crossDimerTmC` | number | °C | the forward x reverse 3'-end cross-dimer temperature — the primer-dimer that extends into a band. 0 when no such dimer exists, and a value far below the 35 °C limit is still a real structure: this is the number to compare pairs on, because the boolean beside it only reports primer3's design cutoff |
| `primerDimerScore` | number or null |  | PrimerDimer's score for the pair (Johnston et al., Sci Rep 9:209, 2019: one hetero- and both homodimers, the most negative kept, clipped at 0). Lower is more dimer-prone. On 48 gel-tested pairs it separates real primer-dimer bands better than the thal Tm beside it (AUC 0.842 against 0.727), and on the paper's own 319 gel-scored pairs it reads 0.961 against 0.750. Read `primerDimerVerdict` beside it for the published cut-off rather than inventing a threshold. Null when a primer carries a base other than A, C, G or T |
| `primerDimerVerdict` | boolean or null |  | true when `primerDimerScore` falls BELOW PrimerROC's dimer-free cut-off, which is the paper's own verdict rather than primer3's design filter (Johnston et al., Sci Rep 9:209, 2019). The cut-off defaults to the published -4.43 and is the `dimerThreshold` input: the paper fitted it on its own gels and says so, so a lab with its own gel data refits it with `primerRocFit`. Branch on this for the dimer question and on `primerDimerRisk` for the would-primer3-reject-this question — they answer different things. Null when a primer carries a base other than A, C, G or T |
| `primerDimerCutoff` | number or null |  | the dimer-free cut-off `primerDimerVerdict` was read against, so a turn never has to assume which threshold produced the verdict. -4.43 is the published value, fitted on the paper's own PCR conditions |
| `primerDimerRisk` | boolean |  | true when the pair breaks one of primer3's own cross-dimer limits (35 °C at a 3' end, 45 °C anywhere) — branch a workflow on this rather than re-deriving it. FALSE IS NOT 'no dimer': those limits are primer3's design filter, and graded against 48 gel-tested pairs (Johnston et al., Sci Rep 9:209, 2019) they flag none of the 23 that produced a visible primer-primer band. Read `crossDimerTmC` beside it rather than branching on this alone |
| `round1ProductCount` | number or null |  | nested PCR only: how many products the OUTER pair made in round 1 (the first one is re-amplified). Absent for a single-round run |
| `conditions` | any |  | the buffer every temperature here was measured in — salt, magnesium, dNTPs, oligo concentration, the salt-correction method and the NN table — or a note saying pydna's defaults were used |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "pcr_amplify",
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

### plan_master_mix

**Plan master mix**: _How much of each reagent goes into a master mix for this many reactions?_

Scale one PCR reaction into a master mix for N reactions plus overage. Starts from a vendor's own published reaction setup (scaled to any reaction volume in proportion to the vendor's columns, so every final concentration is the vendor's, with water making up the volume and the template added per tube), or from your own component list. Returns each component per reaction and in the mix, the mix to dispense per tube and the total to prepare.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Every reaction gets the same recipe; the overage covers pipetting loss and is a percent of the N-reaction mix.

**Does not:**
- Does not check that a custom recipe's concentrations suit the polymerase: only the vendor setups carry final concentrations.
- A vendor setup is cached from the vendor's document on the date it records; a reformulated product is not seen until the cache is refreshed.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** reaction-setups.json

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `setup` | `"neb-phusion-m0530"` · `"takara-taq-r001a"` · `"takara-ex-taq-rr001a"` · `"takara-la-taq-rr002a"` · `"takara-ex-premier-rr370a"` · `"primestar-gxl-r050a"` · `"primestar-gxl-r050a-rapid"` · `"primestar-hs-r010a"` · `"primestar-max-r045a"` · `"primestar-longseq-r055a"` · `"cloneamp-hifi-639298"` · `"speedstar-hs-rr070a"` · `"terra-direct-639270"` · `"titanium-taq-639208"` · `"advantage-hd-639241"` · `"qiagen-taq-201203"` · `"qiagen-hotstartaq-203203"` |  | `"neb-phusion-m0530"` |  | the vendor reaction setup to scale. Ignored when `components` is given. Values: neb-phusion-m0530 (Phusion High-Fidelity DNA Polymerase (M0530)), takara-taq-r001a (TaKaRa Taq (R001A)), takara-ex-taq-rr001a (TaKaRa Ex Taq (RR001A)), takara-la-taq-rr002a (TaKaRa LA Taq (RR002A)), takara-ex-premier-rr370a (TaKaRa Ex Premier (RR370A)), primestar-gxl-r050a (PrimeSTAR GXL (R050A), standard protocol), primestar-gxl-r050a-rapid (PrimeSTAR GXL (R050A), rapid protocol), primestar-hs-r010a (PrimeSTAR HS (R010A)), primestar-max-r045a (PrimeSTAR Max (R045A)), primestar-longseq-r055a (PrimeSTAR LongSeq (R055S/R055A)), cloneamp-hifi-639298 (CloneAmp HiFi PCR Premix (639298)), speedstar-hs-rr070a (SpeedSTAR HS (RR070A)), terra-direct-639270 (Terra PCR Direct Polymerase Mix (639270)), titanium-taq-639208 (Titanium Taq DNA Polymerase (639208)), advantage-hd-639241 (Advantage HD Polymerase Mix (639241)), qiagen-taq-201203 (QIAGEN Taq DNA Polymerase (201203)), qiagen-hotstartaq-203203 (QIAGEN HotStarTaq DNA Polymerase (203203)). Only applies when components is not given. |
| `reaction_volume` | number |  | `20` | 1–200 | volume of one reaction, µl. Each vendor publishes its setup at one or two volumes (25, 50 or 100 µl; NEB's Phusion at 20 and 50); any volume scales from them. In µl. |
| `template_volume` | number |  | `1` | 0–50 | template DNA per reaction, µl, added to each tube rather than the mix. The vendor states an amount, not a volume (NEB Phusion: < 250 ng), so the volume is yours. In µl. Only applies when components is not given. |
| `primer_final` | number |  |  | ≥ 0 | final concentration of each primer, µM. Most vendors state primers as a range rather than a volume; unset uses the setup's own value (its single stated value, else the low end of its range). In µM. Only applies when setup is takara-taq-r001a or takara-ex-taq-rr001a or takara-la-taq-rr002a or takara-ex-premier-rr370a or primestar-gxl-r050a or primestar-gxl-r050a-rapid or primestar-hs-r010a or primestar-max-r045a or primestar-longseq-r055a or cloneamp-hifi-639298 or speedstar-hs-rr070a or terra-direct-639270 or advantage-hd-639241 or qiagen-taq-201203 or qiagen-hotstartaq-203203. |
| `primer_stock` | number |  | `10` | ≥ 0 | concentration of your primer stock, µM; each primer's volume is its final concentration diluted from this stock. In µM. Only applies when setup is takara-taq-r001a or takara-ex-taq-rr001a or takara-la-taq-rr002a or takara-ex-premier-rr370a or primestar-gxl-r050a or primestar-gxl-r050a-rapid or primestar-hs-r010a or primestar-max-r045a or primestar-longseq-r055a or cloneamp-hifi-639298 or speedstar-hs-rr070a or terra-direct-639270 or advantage-hd-639241 or qiagen-taq-201203 or qiagen-hotstartaq-203203. |
| `mg_final` | number |  |  | ≥ 0 | total Mg²⁺ in the reaction, mM, reached by adding the vendor's 25 mM MgCl2 on top of what the buffer holds. Unset uses the vendor's default. Offered by QIAGEN Taq DNA Polymerase (201203), QIAGEN HotStarTaq DNA Polymerase (203203). In mM. Only applies when setup is qiagen-taq-201203 or qiagen-hotstartaq-203203. |
| `include_dmso` | boolean |  | `false` |  | include the setup's optional DMSO (3% final). Offered by Phusion High-Fidelity DNA Polymerase (M0530); the setup's notes say when to use it. Only applies when setup is neb-phusion-m0530. |
| `include_q_solution` | boolean |  | `false` |  | include the setup's optional Q-Solution (1x (from the 5x stock) final). Offered by QIAGEN Taq DNA Polymerase (201203), QIAGEN HotStarTaq DNA Polymerase (203203); the setup's notes say when to use it. Only applies when setup is qiagen-taq-201203 or qiagen-hotstartaq-203203. |
| `reactions` | number |  | `1` | 1–384 | how many reactions the mix is for. |
| `overage` | number |  | `0` | 0–50 | extra mix for pipetting loss, as a percent of the N-reaction volume. In %. |
| `components` | string[] |  |  |  | your own recipe instead of a vendor setup: objects of { name, perReaction (µl), fill (true on the one component that makes up the volume), perTube (true to add it to each tube instead of the mix) }. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `rows` | any |  | each component: name, µl per reaction, µl in the mix (null when added per tube) |
| `mixTotal` | number or null |  | µl of master mix to prepare |
| `dispensePerTube` | number or null |  | µl of master mix to dispense into each tube |
| `multiplier` | number or null |  | reactions × (1 + overage/100) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "plan_master_mix",
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

### plan_serial_dilution

**Plan serial dilution**: _How do I make a dilution series from this stock?_

Plan a serial dilution: the same fold dilution repeated tube after tube from a stock, each tube made to one volume. Returns the transfer and diluent volumes for every step, each tube's concentration and cumulative dilution, and what each tube holds after giving its transfer to the next.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The solute is conserved and the volumes add.
- Each tube is mixed fully before the next transfer.

**Does not:**
- Pipetting error compounds down the series and is not modelled.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `stock_concentration` | number | **yes** |  | ≥ 0 | concentration of the stock the series starts from. |
| `stock_concentration_unit` | `"M"` · `"mM"` · `"µM"` · `"nM"` · `"pM"` · `"fM"` · `"mg/mL"` · `"µg/µL"` · `"ng/µL"` · `"µg/mL"` · `"ng/mL"` · `"X"` · `"%"` |  | `"mM"` |  | the unit of the stock concentration, which every tube is reported in. |
| `fold` | number |  | `10` | ≥ 1 | the dilution at each step, as a fold (1:10 is 10). |
| `steps` | number |  | `5` | 1–24 | how many dilutions to make. |
| `tube_volume` | number | **yes** |  | ≥ 0 | the volume of each dilution after mixing (transfer plus diluent). |
| `tube_volume_unit` | `"L"` · `"mL"` · `"µL"` · `"nL"` |  | `"µL"` |  | the unit of the tube volume. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `tubes` | any |  | each tube: step, concentration, cumulative fold, volume left after its transfer |
| `transfer` | number or null |  | volume moved into each tube, in the tube volume's unit |
| `diluent` | number or null |  | diluent in each tube, in the tube volume's unit |
| `final` | number or null |  | the last tube's concentration, in the stock's unit |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "plan_serial_dilution",
  "arguments": {
    "stock_concentration": "<number>",
    "tube_volume": "<number>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### primer_check

**Primer check**: _Where does a primer anneal on this molecule, and how well does each site match?_

Where a primer anneals on the open plasmid: 3'-anchored sites with identity % and the ✓/⚠/~/✗ verdict, graded at a bar you can move and that the answer states. The scan is 3'-anchored, so every site it reports matches the oligo's 3' seed exactly and 'no sites' means no seed match rather than a low score.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Annealing needs an exact 3' seed match; identity is scored over the rest.

**Does not:**
- 'No sites' means no 3' seed match, not a low score.
- Melting temperature is SpliceCraft's fallback, not primer3's.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `primer` | string | **yes** |  |  | primer sequence 5'→3'. |
| `thresholds` | object |  |  |  | the identity boundaries the ✓/⚠/~/✗ verdict is cut at. Left unset, the run uses the bar your Primer Library is set to, and with no panel state the upstream SpliceCraft default — either way the bar it used comes back in `thresholds`, because a verdict whose cutoff is not stated cannot be checked. Move it to say what you are asking: screening a pool tolerates a lower `strong` than checking a clone does. Advanced. |
| `thresholds.exact` | number |  | `99.999` | 0–100 | at or above this identity %, a perfect match — distinguished from a merely strong one. It is 99.999 rather than 100 on purpose: identity is computed as 100 × (L − mm) / L and a cut at 100 drops a perfect match to float rounding. In %. |
| `thresholds.strong` | number |  | `90` | 0–100 | at or above: ✓, the primer is expected to bind here. In %. |
| `thresholds.weak` | number |  | `75` | 0–100 | at or above: ⚠, plausible binding worth checking. In %. |
| `thresholds.marginal` | number |  | `60` | 0–100 | at or above: ~, marginal. Below it: ✗, not expected to bind. In %. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sites` | any |  | annealing sites with identity %, mismatches, strand, the 3'-anchored footprint, and each one's tier and what that tier MEANS — read the tier rather than re-deriving it from the percentage, because the bar is a parameter |
| `reading` | string |  | what the scan found, generated from it: how many sites, where the best one sits, its identity and what that tier means. The panel's own sentence, from the builder that sits beside the tier vocabulary both grade with |
| `cautions` | any |  | what would undermine the reading, earned by this run: a second site that is also expected to bind (one primer, more than one product), or a best site that is not a perfect match |
| `siteCount` | number |  | how many sites the seed found at all. Branch on this rather than on the length of `sites`: 0 is a real result and means the oligo's 3' end matches nowhere, not that it binds weakly |
| `bindingCount` | number |  | how many sites are at or above the `strong` boundary — the ones expected to bind. More than one is a different experiment from one: a primer with two real sites gives two products, so a single clean band is not what this predicts |
| `bestIdentityPct` | number | % | identity of the best site, or 0 when nothing was found — a measurement, never a verdict |
| `bestTier` | string |  | the best site's tier: exact · strong · weak · marginal · none, or unknown when nothing was graded |
| `thresholds` | any |  | the four boundaries every verdict above was made against, and whether they came from your panel or from the upstream default — the same shape the `thresholds` parameter takes, so a run can be repeated at the bar it was graded at |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "primer_check",
  "arguments": {
    "primer": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### solve_dilution

**Solve dilution**: _How much stock, diluent or final concentration does a dilution need?_

Solve C₁V₁ = C₂V₂ for whichever of the four quantities is left empty (stock concentration, stock volume, final concentration, final volume), each in its own unit: molar (M to fM), mass per volume (mg/mL to ng/mL), fold (X) or percent. Returns all four, the fold and the diluent volume to add. Refuses a 'dilution' that would raise the concentration, and two concentrations of different dimensions.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The solute is conserved and the volumes add (no contraction on mixing).

**Does not:**
- Cannot convert between molar and mass concentrations: that needs the solute's molar mass.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `stock_concentration` | number |  |  | ≥ 0 | stock concentration (C₁). Leave exactly one of the four quantities empty: that one is calculated. |
| `stock_concentration_unit` | `"M"` · `"mM"` · `"µM"` · `"nM"` · `"pM"` · `"fM"` · `"mg/mL"` · `"µg/µL"` · `"ng/µL"` · `"µg/mL"` · `"ng/mL"` · `"X"` · `"%"` |  | `"mM"` |  | the unit of the stock concentration, given or solved. |
| `stock_volume` | number |  |  | ≥ 0 | stock volume (V₁). Leave exactly one of the four quantities empty: that one is calculated. |
| `stock_volume_unit` | `"L"` · `"mL"` · `"µL"` · `"nL"` |  | `"µL"` |  | the unit of the stock volume, given or solved. |
| `final_concentration` | number |  |  | ≥ 0 | final concentration (C₂). Leave exactly one of the four quantities empty: that one is calculated. |
| `final_concentration_unit` | `"M"` · `"mM"` · `"µM"` · `"nM"` · `"pM"` · `"fM"` · `"mg/mL"` · `"µg/µL"` · `"ng/µL"` · `"µg/mL"` · `"ng/mL"` · `"X"` · `"%"` |  | `"µM"` |  | the unit of the final concentration, given or solved. |
| `final_volume` | number |  |  | ≥ 0 | final volume (V₂). Leave exactly one of the four quantities empty: that one is calculated. |
| `final_volume_unit` | `"L"` · `"mL"` · `"µL"` · `"nL"` |  | `"mL"` |  | the unit of the final volume, given or solved. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `solved` | string |  | which quantity was solved, by its parameter name |
| `value` | number or null |  | the solved quantity, in its own unit |
| `unit` | string |  | the solved quantity's unit |
| `fold` | number or null |  | C₁/C₂, how many times the stock is diluted |
| `diluent` | number or null |  | V₂ − V₁, the diluent to add, in V₂'s unit |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "solve_dilution",
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
