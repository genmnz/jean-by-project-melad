# 🧩 Proteins, domains & proteomics

_Domains and motifs, residue sites, protein properties and peptide evidence._

26 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`antibody_antigen_contacts`](#antibody_antigen_contacts) | Which antibody residues touch which antigen residues in this complex, how close, and what kind of interaction is each? |
| [`antibody_canonical_classes`](#antibody_canonical_classes) | Which known loop conformation does each CDR of this antibody's variable domain most likely adopt? |
| [`antibody_isotype`](#antibody_isotype) | Which immunoglobulin gene and allele is this chain's constant region, and where does each IMGT domain sit on it? |
| [`antibody_liabilities`](#antibody_liabilities) | Which sequence liabilities does this variable domain carry, and in which IMGT region does each sit? |
| [`antibody_molecule`](#antibody_molecule) | What are an assembled Fab's or IgG's mass, isoelectric point, charge at a pH, and extinction coefficient reduced and oxidised? |
| [`antibody_position_frequencies`](#antibody_position_frequencies) | Which residues of this variable domain are unusual at their IMGT position, measured against the species' germline alleles or an expressed repertoire? |
| [`bayesian_protein_inference`](#bayesian_protein_inference) | What is the posterior probability that each protein, group and match is present? |
| [`delta_blast_smart`](#delta_blast_smart) | Which of these subject proteins resemble this one, by a profile built from its SMART domains? |
| [`find_linear_motifs`](#find_linear_motifs) | Which short linear motifs from ELM does this protein carry, after ELM's own filters? |
| [`graft_antibody_cdrs`](#graft_antibody_cdrs) | Which human germline framework accepts this domain's CDRs, and what is the grafted sequence? |
| [`humanize_antibody`](#humanize_antibody) | Which framework mutations does Sapiens make to humanize this variable domain, keeping the parental CDRs? |
| [`infer_proteins`](#infer_proteins) | Which proteins do these peptide-spectrum matches support, and which cannot be told apart? |
| [`lookup_protein`](#lookup_protein) | What does the authority named return for this protein? |
| [`lookup_residue_sites`](#lookup_residue_sites) | Which catalytic, binding and interface residues do member databases annotate in this protein's domains? |
| [`number_antibody`](#number_antibody) | Which antibody or TCR variable domains does this protein carry, how are they numbered, and which germlines are closest? |
| [`protein_disorder`](#protein_disorder) | Which stretches of this protein does FoldIndex predict unfolded? |
| [`protein_disorder_metapredict`](#protein_disorder_metapredict) | What is this protein's per-residue disorder score, and which regions are IDRs, by metapredict? |
| [`protein_membrane_profile`](#protein_membrane_profile) | Which windows of this protein look transmembrane, globular or surface-seeking on an Eisenberg hydrophobic-moment plot? |
| [`protein_profile`](#protein_profile) | How does a chosen physicochemical scale vary along this protein? |
| [`protein_properties`](#protein_properties) | What are this protein's mass, formula, isoelectric point, instability index and amphipathicity? |
| [`protein_topology`](#protein_topology) | Which residues of this protein are inside, in a transmembrane helix, or outside, by the HMM-TM model? |
| [`rps_blast_cdd`](#rps_blast_cdd) | Which conserved domains does NCBI's CD-Search find in this protein? |
| [`rps_blast_smart`](#rps_blast_smart) | Which SMART domain models does this protein hit? |
| [`rpstblastn_smart`](#rpstblastn_smart) | Which SMART domains does this DNA encode in any of its six frames? |
| [`scan_motif_sites`](#scan_motif_sites) | Where does a transcription-factor matrix match this sequence, on either strand, at a threshold set as a fraction of that matrix's own score range? |
| [`scan_protein_domains`](#scan_protein_domains) | Which domains and families does InterProScan find in this protein? |

---

### antibody_antigen_contacts

**Antibody antigen contacts**: _Which antibody residues touch which antigen residues in this complex, how close, and what kind of interaction is each?_

Type the ANTIBODY-ANTIGEN INTERFACE of a deposited complex: which residue of each antibody chain touches which residue of the antigen, how close, and what kind of interaction each pair makes - ionic, polar, weak polar, hydrophobic, aromatic, carbonyl, or a disulfide. The antigen is found rather than named: a protein chain with no immunoglobulin variable domain is the thing being bound. Geometric definitions are CREDO's as Arpeggio implements them, graded contact-for-contact against pdbe-arpeggio. `polar` is the hydrogen-bond criterion WITHOUT the donor angle, because a crystal structure carries no hydrogens; it is the superset an angle test would filter, and no angle-checked hydrogen bond is claimed.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- CREDO's geometric interaction definitions.
- The antigen is the protein chain with no immunoglobulin variable domain.

**Does not:**
- Geometry in one deposited model: it is not an energy or a measured contribution to binding.
- Alternate conformations and missing atoms limit what can be typed.

**Not read from this result:** The answer is the residue-pair contact table, which the outputs carry; the structure tab colours the interface from it and writes no reading over it.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `text` | string | **yes** |  |  | the coordinate file's contents - a PDB flat file or a PDBx/mmCIF; the format is read from the bytes, not from a name. |
| `model` | number |  | `1` | ≥ 1 | which model of an ensemble to type, 1-based: conformers touch in different places, so one is typed rather than all. |
| `antibodyChain` | string |  |  |  | type only this chain against the antigen. Left out, every chain carrying a variable domain is typed. |
| `antigenChains` | string |  |  |  | comma-separated chain ids to treat as the antigen. Left out, every protein chain with no variable domain is the antigen. |
| `interactingCutoff` | number |  | `5` | ≥ 1 | atom pairs further apart than this (Å) are not reported at all; Arpeggio's own default is 5. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `antibodyChains` | any |  | the chains typed, each with its variable-domain chain types |
| `antigenChains` | any |  | the chain ids treated as the antigen |
| `contacts` | any |  | one row per residue pair: the antibody residue (chain, author number, name, and its scheme position where it sits in a variable domain), the antigen residue, the closest atom distance, the atom-pair count, and the interaction types |
| `byType` | any |  | atom pairs carrying each type over the whole interface, distance bands included |
| `residues` | any |  | how many residues each side contributes, per antibody chain |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "antibody_antigen_contacts",
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

### antibody_canonical_classes

**Antibody canonical classes**: _Which known loop conformation does each CDR of this antibody's variable domain most likely adopt?_

Assign each CDR of an antibody heavy, kappa or lambda variable domain to its canonical structure class: SCALOP's length-independent clusters of known loop conformations (CDR-H1, H2, L1, L2, L3; H3 has no canonical classes). Each loop is scored against every cluster of its length by the cluster's position-specific log-odds; the best score above SCALOP's threshold names the class and its median structure (a PDB chain). Graded against the real SCALOP on every heavy, kappa and lambda chain of ANARCI's PDB benchmark.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- SCALOP's v2019-10 clusters and PSSMs, as published in its repository.
- The CDR is cut by SCALOP's own region tables in the chosen scheme and definition, which for North are not abnumber's.

**Does not:**
- A class is a sequence-based prediction of a conformation, not a structure; a loop below the threshold, or of a length no cluster holds, gets no class.
- CDR-H3 is not classified. T-cell receptor chains are refused.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (one-letter amino acids); every heavy, kappa and lambda variable domain in it is classified. |
| `scheme` | `"imgt"` · `"chothia"` |  | `"imgt"` |  | the numbering the clusters are read in. Values: imgt (IMGT), chothia (Chothia). |
| `definition` | `"imgt"` · `"chothia"` · `"north"` |  | `"north"` |  | where each CDR begins and ends, by SCALOP's own tables. Values: imgt (IMGT), chothia (Chothia), north (North). |
| `species` | (`"human"` · `"mouse"` · `"rat"` · `"rabbit"` · `"rhesus"` · `"pig"` · `"alpaca"` · `"cow"`)[] |  | `["human", "mouse"]` |  | species whose HMMs are preferred when numbering (ANARCI's default: human and mouse). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `domains` | any |  | per heavy, kappa or lambda domain: chain type, span, and per CDR the loop sequence, its class (cluster id), the median structure, the cluster's size, the outcome, SCALOP's threshold, every candidate cluster's score, and each residue's position, 0-based sequence index and log-odds in the assigned cluster |
| `classes` | any |  | one `CDR: class` string per CDR, in sequence order (`H1: H1-13-A`, `None` where no class fits) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "antibody_canonical_classes",
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

### antibody_isotype

**Antibody isotype**: _Which immunoglobulin gene and allele is this chain's constant region, and where does each IMGT domain sit on it?_

Name the CONSTANT region of an antibody chain: which immunoglobulin gene and allele it carries (IGHG1, IGHA2, IGKC, IGLC2 …), and where each IMGT domain sits on it — CH1, the hinge, CH2, CH3, the secretory tail and the membrane exons, or the single C region of a light chain. A domain search says 'a C1-set immunoglobulin domain'; this says which isotype it is. Reads IMGT/GENE-DB's own per-label translations for every species, and is graded against UniProtKB's curated human constant chains and their CH1/hinge/CH2/CH3 regions.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- IMGT/GENE-DB's own per-label translations define the domains.

**Does not:**
- Names the isotype from sequence; it does not infer effector function.

**Not read from this result:** The answer is the best-matching IMGT constant gene and allele with its identity and domain placements, which the outputs carry; the Antibody panel shows them on the chain diagram and writes no reading over them.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the chain (one-letter amino acids); the constant region in it is found, so a whole heavy chain is fine. |
| `species` | string |  |  |  | only consider genes of this species, spelled as IMGT spells it (Homo sapiens, Mus musculus). Left out, every species in the catalogue competes and the answer says which won. |
| `minIdentity` | number |  | `0.6` |  | a domain matching less of its reference than this is not reported. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `gene` | string |  | the IMGT gene the constant region matches (IGHG1) |
| `allele` | string |  | the allele, as IMGT numbers them (01) |
| `species` | string |  | the species whose gene answered |
| `identity` | number |  | identical residues over every aligned column, 0 to 1 |
| `domains` | any |  | each IMGT label placed on the chain: label, start, end (1-based inclusive), identity, coverage |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "antibody_isotype",
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

### antibody_liabilities

**Antibody liabilities**: _Which sequence liabilities does this variable domain carry, and in which IMGT region does each sit?_

Scan antibody and TCR variable domains for sequence liabilities (Asn deamidation, Asp isomerization, N-glycosylation sequons, Asp-Pro cleavage, Met and Trp oxidation, unpaired or missing conserved cysteines), each placed in its IMGT region so CDR hits can be told from framework ones. Every motif is cited to its source.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Each motif is the published one, cited at its declaration.

**Does not:**
- No risk score: the sources name motifs, not rates, so a hit is a flag to check rather than a predicted failure.
- Sequence motifs only: structure and formulation decide whether one matters.

**Not read from this result:** The answer is the list of motif hits with their rule, region and source, which the outputs carry; the Antibody panel counts them inside the numbering sentence, which needs number_antibody's germline too.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (one-letter amino acids). |
| `rules` | (`"deamidation"` · `"isomerization"` · `"n-glycosylation"` · `"asp-pro-cleavage"` · `"met-oxidation"` · `"trp-oxidation"` · `"unpaired-cys"` · `"missing-conserved-cys"`)[] |  |  |  | which liabilities to report (default: all). |
| `cdrOnly` | boolean |  | `false` |  | report only liabilities that start inside a CDR. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `liabilities` | any |  | each hit: rule, motif, 0-based start and end, IMGT positions, region, whether in a CDR, source |
| `count` | number |  | number of liabilities reported |
| `cdrCount` | number |  | number of reported liabilities inside a CDR |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "antibody_liabilities",
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

### antibody_molecule

**Antibody molecule**: _What are an assembled Fab's or IgG's mass, isoelectric point, charge at a pH, and extinction coefficient reduced and oxidised?_

Properties of an assembled antibody from its heavy and light chains: molecular weight, isoelectric point, net charge at a pH, and the extinction coefficient and A280 with cysteines reduced and with every pair formed into a cystine, for a Fab (1 heavy + 1 light) or an IgG (2 + 2). Each chain keeps its own termini, so this is not the same as pasting the chains end to end. Graded against Biopython ProtParam over every heavy/light pair of ANARCI's PDB benchmark.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The stoichiometry chosen (1+1 Fab, 2+2 IgG); each chain keeps its own termini.

**Does not:**
- Sequence-derived: glycosylation, which dominates a real antibody's mass, is not included.
- Not the same as concatenating the chains, which is why the assembly is explicit.

**Not read from this result:** The answer is the whole molecule's computed properties (mass, pI, charge, extinction), which the outputs carry; the Antibody panel shows them as readouts and writes no reading over them.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `heavy` | string | **yes** |  |  | the heavy chain (one-letter amino acids), as much of it as the molecule carries. |
| `light` | string | **yes** |  |  | the light chain (kappa or lambda, one-letter amino acids). |
| `format` | `"fab"` · `"igg"` |  | `"igg"` |  | how many copies of each chain the molecule holds. Values: fab (Fab (1 heavy + 1 light)), igg (IgG (2 heavy + 2 light)). |
| `pH` | number |  | `7.4` |  | the pH the net charge is reported at. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `molecularWeight` | number |  | average mass of the whole molecule, Da (chains reduced) |
| `isoelectricPoint` | number |  | isoelectric point of the whole molecule (Bjellqvist pKs, each chain with its own termini) |
| `chargeAtPH` | number |  | net charge at the requested pH |
| `extinction` | any |  | ε280 in M⁻¹ cm⁻¹, `reduced` and `cystines` |
| `absorbance` | any |  | A280 of a 1 g/L solution, `reduced` and `cystines` |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "antibody_molecule",
  "arguments": {
    "heavy": "<string>",
    "light": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### antibody_position_frequencies

**Antibody position frequencies**: _Which residues of this variable domain are unusual at their IMGT position, measured against the species' germline alleles or an expressed repertoire?_

How common each residue of an antibody variable domain is at its IMGT position, and which residues are rarer there than a cut (abYsis's 1% "unusual residue" by default). Two distributions: IMGT's own germline V and J alleles of a species (one count per reference allele), or a bundled Observed Antibody Space repertoire subset (one count per unique expressed sequence; human naive B cells, Jaffe et al. 2022). Graded against independent pandas counts of ANARCI's germline alignments and of every OAS data unit of the subset.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- germline: IMGT/GENE-DB V and J alleles as ANARCI ships them, aligned to the 128 IMGT states.
- repertoire: OAS unpaired · Jaffe_2022 (doi:10.1038/s41586-022-05371-z) · human · PBMC · naive B cells · disease None · vaccine None · every unit the search returned (47 heavy, 10 light), numbered by OAS with ANARCI under IMGT, counted once per unique sequence (retrieved 2026-10-21).
- Each residue is read at its own IMGT state; an insertion (111A) has no column in either table and gets no frequency.

**Does not:**
- A germline distribution is not a repertoire: somatic mutation and selection are not counted, so a residue rare in germlines can be common in expressed antibodies.
- The repertoire is one named OAS subset (human naive B cells from healthy donors), not all of OAS: naive repertoires carry little somatic mutation, and other species or T-cell receptors are refused.
- abYsis's 1% cut was defined on a repertoire; on the germline distribution it is applied to alleles.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (one-letter amino acids); every antibody and T-cell-receptor variable domain in it is read. |
| `distribution` | `"germline"` · `"repertoire"` |  | `"germline"` |  | what each position is counted over: `germline` (IMGT's V and J alleles of `germline_species`) or `repertoire` (the bundled human OAS subset of expressed sequences). |
| `germline_species` | string |  | `"human"` |  | the species whose IMGT germline alleles each position is counted over (germline distribution only; the repertoire is human). |
| `rare_below` | number |  | `0.01` | 0–1 | a residue is rare where its share of the alleles or sequences is below this fraction (abYsis's unusual-residue cut is 0.01). |
| `species` | (`"human"` · `"mouse"` · `"rat"` · `"rabbit"` · `"rhesus"` · `"pig"` · `"alpaca"` · `"cow"`)[] |  | `["human", "mouse"]` |  | species whose HMMs are preferred when numbering (ANARCI's default: human and mouse). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `domains` | any |  | per domain: chain type, span, what the table counted (germline allele counts, or the repertoire's sequence count and subset), and per residue its IMGT position, 0-based sequence index, count, denominator, frequency, the commonest residue there and whether it is rare |
| `rare` | any |  | one `IMGT position residue (count of n)` string per rare residue, in sequence order |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "antibody_position_frequencies",
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

### bayesian_protein_inference

**Bayesian protein inference**: _What is the posterior probability that each protein, group and match is present?_

Bayesian protein inference, Epifany (validated against OpenMS BayesianProteinInferenceAlgorithm on PXD000001): the posterior probability that each protein, each indistinguishable group and each peptide-spectrum match is present, from the matches' posterior error probabilities under a network in which present proteins emit their peptides. Shared peptides are weighed between their proteins instead of being counted for each.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Epifany's network model, with the posterior error probabilities given as input.
- The alpha, beta and gamma parameters chosen, or the grid search's.

**Does not:**
- A posterior under this model: it moves with the parameters, which the answer reports.
- Garbage posterior error probabilities in, garbage posteriors out.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `psms` | string | **yes** |  |  | the matches as a table with a header row naming spectrum, peptide, charge and a posterior error probability column (tab- or comma-separated); peptides are ProForma. |
| `database` | string | **yes** |  |  | the protein database searched, as FASTA; the accession is the header up to the first space. |
| `scoreColumn` | string |  | `"pep"` |  | the column holding each match's posterior error probability (PEP, 0 to 1). |
| `alpha` | number |  | `0.1` |  | peptide emission probability α: the chance a present protein yields a given one of its peptides. |
| `beta` | number |  | `0.01` |  | spurious emission probability β: the chance a peptide is reported with none of its proteins present. |
| `gamma` | number |  | `0.5` |  | protein prior γ: the chance a protein is present before any evidence. |
| `peptidePrior` | number |  | `0.1` |  | peptide prior π, dividing each match's probability back out of its evidence. |
| `psmCutoff` | number |  | `0.001` |  | drop matches whose probability (1 − PEP) is below this. |
| `gridSearch` | boolean |  | `false` |  | choose α, β and γ instead: run OpenMS's grid (α 0.1–0.8 × β 0.01–0.4 × γ 0.2–0.7) and keep the combination whose protein posteriors best agree with target-decoy FDR and separate targets from decoys; needs decoy proteins. |
| `decoyPrefix` | string |  | `"DECOY_"` |  | accession prefix marking a decoy protein, for the grid search. |
| `appendReversedDecoys` | boolean |  | `false` |  | add the reversed sequence of every database protein as a decoy (accession decoyPrefix + accession), for a database searched with reversed decoys that holds only targets. |
| `maxAmbiguousResidues` | number |  | `3` |  | how many ambiguous database residues (B, J, Z, X) one peptide match may resolve. |
| `ilEquivalent` | boolean |  | `false` |  | treat isoleucine and leucine (and a database J) as the same residue when mapping peptides. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `proteins` | any |  | one row per protein: accession, posterior probability, matches counted, sequence coverage (%) |
| `groups` | any |  | indistinguishable protein groups, most probable first: probability that at least one member is present, and accessions |
| `psmPosteriors` | any |  | the matches inference used (the best per peptide): spectrum, peptide, prior (1 − PEP) and posterior |
| `grid` | any |  | with the grid search: every α, β, γ tried, with its FDR-curve difference, ROC-100 and objective (skipped when improbable) |
| `count` | number |  | proteins reported |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "bayesian_protein_inference",
  "arguments": {
    "psms": "<string>",
    "database": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### delta_blast_smart

**DELTA BLAST SMART**: _Which of these subject proteins resemble this one, by a profile built from its SMART domains?_

DELTA-BLAST, run on this machine: build a position-specific profile for a protein from the SMART conserved domains it contains, then search other proteins with it (one PSI-BLAST iteration) — more sensitive than BLASTP for distant homologs. Searches the open record's coding sequences unless `subjects` gives FASTA. NCBI BLAST+ 2.17.0's algorithms, checked against the deltablast program on every bundled protein. Nothing is sent anywhere.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- NCBI BLAST+ 2.17.0's deltablast against the bundled SMART PSSMs.

**Does not:**
- Searches the subjects given, not a public database.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** smart

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein, one-letter codes; wire it from translate_sequence or read it off a CDS. |
| `subjects` | string |  |  |  | the proteins to search, as FASTA; leave empty to search the open record's coding sequences. |
| `domain_inclusion_evalue` | number |  | `0.05` | ≥ 0 | conserved-domain hits with E below this build the profile (`-domain_inclusion_ethresh`). |
| `threshold` | number |  | `11` | ≥ 1 | lowest profile word score seeded in the lookup table (`-threshold`). Advanced. |
| `evalue` | number |  | `10` | ≥ 0 | report alignments with E at most this (`-evalue`); BLAST's default is 10. |
| `max_target_seqs` | number |  | `500` | ≥ 1 | most proteins reported (`-max_target_seqs`). |
| `source` | `"bundled"` · `"ncbi"` |  | `"bundled"` |  | where the SMART database is read from: 'bundled' (a byte-identical copy of NCBI's file) or 'ncbi' (NCBI's FTP site, now). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `proteins` | any |  | every protein hit, best first: id, title, length, and each HSP with query and subject coordinates, score, bits, E-value, identities, positives, gaps and aligned strings |
| `count` | number |  | proteins reported |
| `domains` | any |  | the conserved-domain alignments DELTA-BLAST built its profile from (rpsblast at the domain inclusion E-value): accession, shortName, title, and each HSP's query and model coordinates, score, bits, E-value, identities and aligned strings |
| `profile` | any |  | how the profile was built: domainsUsed, columnsCovered, meanObservations, and the profile's gapped lambda and kappa |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "delta_blast_smart",
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

### find_linear_motifs

**Find linear motifs**: _Which short linear motifs from ELM does this protein carry, after ELM's own filters?_

Short linear motifs in a protein: degrons, docking sites, targeting signals, cleavage and modification sites — the three-to-eleven-residue functional sites a profile-HMM domain scan cannot see. Runs ELM's own class patterns ON THIS MACHINE; only the class table is fetched. Applies ELM's context filters: the chance-probability cutoff, family selection, and the globular-domain filter when you pass domains. It does NOT scan for DOMAINS — for those call scan_protein_domains, which submits to EMBL-EBI InterProScan and returns `domains` in exactly the form this tool's `domains` parameter takes.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- ELM's class regular expressions and filters as bundled.

**Does not:**
- A regex match is a candidate, not an annotated instance.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence, one-letter codes; wire it from translate_sequence or read it off a CDS. |
| `expectCutoff` | number |  | `0.01` | 0–1 | ELM's class gate: classes whose chance probability per residue exceeds this are not scanned at all. ELM's own default is 0.01; 0 scans every class, which is the resource's “all found (before filtering)” listing. |
| `families` | string |  | `""` |  | restrict to these ELM families, comma-separated, from CLV, DEG, DOC, LIG, MOD, TRG. Empty is no restriction and scans every family; the literal "none" is a restriction to no family and scans nothing, which is what the panel does when every family is unticked. |
| `filterInDomains` | boolean |  | `false` |  | apply ELM's globular-domain filter, dropping motifs buried inside a folded domain. Takes the domains from `domains` when you pass them, and otherwise from the scan the Protein domains panel currently holds; with neither, the call refuses rather than silently not filtering. |
| `domains` | string |  | `""` |  | the globular domains to bury motifs in, as `start-end` residue ranges (1-based, inclusive), comma-separated, each optionally labeled `start-end@label` so a dropped hit can say what buried it — e.g. `20-153@G3DSA:3.90.180.10, 296-341@G3DSA:3.90.180.10`. Pass the FRAGMENTS of an InterProScan domain match, not its outer span. Empty falls back to the scan the Protein domains panel holds, which is the only source the in-browser doors need. Only applies when filterInDomains is true. |
| `compartments` | string |  | `""` |  | restrict to motifs whose class is annotated for these cell compartments, as GO ids, comma-separated (e.g. GO:0005634 for nucleus). Empty runs no compartment filter, which is ELM's own default. |
| `species` | string |  | `""` |  | the species the protein comes from, as an NCBI Taxonomy id (e.g. 4932) or a scientific name (e.g. Saccharomyces cerevisiae), for ELM's taxonomic range filter: a motif whose class ELM does not place in that species' lineage is dropped, with its range. Empty runs no taxon filter, which is ELM's own default. |
| `structuralContext` | string |  | `""` |  | score each motif's structural context, as ELM's structure filter does. Empty applies nothing, which is the panel's own default. `alphafold` uses the predicted model and yields Q_acc only. A four-character PDB id (e.g. `1crn`) uses that experimental entry and yields Q_acc, Q_sse and ELM's three-way verdict, because only a real entry has a DSSP file. Either way the protein is resolved to its UniProt entry by sequence checksum first, and the call refuses if it is not an exact match. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | each surviving motif, in the engine’s own field names: identifier, accession, functionalSiteName, description, 1-based start/end, the residues that matched, the class chance probability, and how many experimentally annotated instances ELM holds |
| `accounting` | any |  | what the scan was actually run against — classes scanned, classes skipped by the cutoff, classes skipped by the family selection — so a hit count can be read against its denominator rather than on its own |
| `count` | number |  | surviving motifs, after every filter that ran |
| `provenance` | any |  | the ELM release and date the scan ran against, and the filters that ran |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "find_linear_motifs",
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

### graft_antibody_cdrs

**Graft antibody CDRs**: _Which human germline framework accepts this domain's CDRs, and what is the grafted sequence?_

Humanize an antibody variable domain by CDR grafting: find the closest human germline V and J, merge them into an acceptor framework, and put the parental CDRs onto it. The classical humanization route, and the counterpart to humanize_antibody's language model. Reproduces abnumber 0.4.4 over every antibody chain of ANARCI's PDB benchmark.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The closest human V and J by identity are a suitable acceptor.

**Does not:**
- The classical route: it does not predict whether binding survives the graft.
- Back-mutations are not proposed here.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (one-letter amino acids); the variable domains in it are found and numbered first. |
| `domain` | number |  | `0` |  | which variable domain to graft when the sequence holds several (0-based, in sequence order). |
| `cdrDefinition` | `"imgt"` · `"kabat"` · `"chothia"` · `"north"` |  | `"imgt"` |  | which CDR definition decides what is grafted from the parental antibody. Values: imgt (IMGT), kabat (Kabat), chothia (Chothia), north (North). |
| `vGene` | string |  |  |  | use this human V germline instead of the closest one (a family, gene or allele: IGHV1, IGHV1-18, IGHV1-18*01). |
| `jGene` | string |  |  |  | use this human J germline instead of the closest one. |
| `top` | number |  | `0` |  | graft onto the n-th closest germline instead of the closest (0-based). |
| `backmutateVernier` | boolean |  | `false` |  | keep the parental residues at the Kabat Vernier positions, the framework residues that support the CDR loops. |
| `rankByFrameworks` | boolean |  | `false` |  | rank germlines on framework identity alone, ignoring the CDRs. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `grafted` | string |  | the grafted variable domain sequence |
| `germline` | string |  | the V and J alleles the frameworks came from |
| `identity` | number | % | percent identity of the grafted domain to the parental one |
| `candidates` | any |  | the closest human V and J germlines, best first |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "graft_antibody_cdrs",
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

### humanize_antibody

**Humanize antibody**: _Which framework mutations does Sapiens make to humanize this variable domain, keeping the parental CDRs?_

Humanize an antibody variable domain with Sapiens, the antibody language model behind BioPhi: score every position against human repertoires, take the highest-scoring residue in the frameworks, and keep the parental CDRs (and optionally the Kabat Vernier zone). Reports every mutation, and what the model would change next. Validated against the published PyTorch model on every chain of ANARCI's PDB benchmark.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Sapiens' language model, scored against human repertoires; the CDRs (and optionally the Vernier zone) are kept.

**Does not:**
- A humanness score is not an immunogenicity measurement.
- Mutations are proposed; binding must be re-measured.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (one-letter amino acids); the variable domains in it are found and numbered first. |
| `domain` | number |  | `0` |  | which variable domain to humanize when the sequence holds several (0-based, in sequence order). |
| `iterations` | number |  | `1` |  | Sapiens passes, each re-scoring the previous output (BioPhi's default 1). |
| `cdrDefinition` | `"imgt"` · `"kabat"` · `"chothia"` · `"north"` |  | `"imgt"` |  | which CDR definition marks the residues kept from the parental antibody. Values: imgt (IMGT), kabat (Kabat), chothia (Chothia), north (North). |
| `humanizeCdrs` | boolean |  | `false` |  | humanize the CDRs too instead of grafting the parental ones back (raises the risk of losing binding). |
| `backmutateVernier` | boolean |  | `false` |  | also keep the parental residues at the Kabat Vernier positions, which support the CDR loops. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `humanized` | string |  | the humanized variable domain sequence |
| `mutations` | any |  | each change: 0-based index in the domain, IMGT position, region, parental and humanized residue, and the model's probability for each |
| `mutationCount` | number |  | number of positions changed |
| `identity` | number | % | percent identity of the humanized domain to the parental one |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "humanize_antibody",
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

### infer_proteins

**Infer proteins**: _Which proteins do these peptide-spectrum matches support, and which cannot be told apart?_

Protein inference from peptide-spectrum matches (validated against OpenMS BasicProteinInferenceAlgorithm on PXD000001): maps each peptide to the protein database, keeps the best match per spectrum, scores each protein by aggregating its peptides' best scores, reports the proteins its evidence cannot tell apart as indistinguishable groups, and the percent of each sequence the matches cover.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The database searched is the one the matches came from; the best match per spectrum is kept.

**Does not:**
- Indistinguishable proteins are reported as a group rather than one being chosen.
- A protein score aggregates peptide scores; it is not a probability (bayesian_protein_inference is that).

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `psms` | string | **yes** |  |  | the matches as a table with a header row naming spectrum, peptide, charge and score (tab- or comma-separated); peptides are ProForma. |
| `database` | string | **yes** |  |  | the protein database searched, as FASTA; the accession is the header up to the first space. |
| `scoreColumn` | string |  | `"score"` |  | which column holds the score inference uses, when the table carries several (OpenMS score_type); a column named pep or q-value sets its own direction. |
| `higherIsBetter` | boolean |  | `true` |  | true for scores like HyperScore; false for e-values, q-values and PEPs. |
| `scoresArePep` | boolean |  | `false` |  | the scores are posterior error probabilities: matches compete lowest first, and each protein combines 1 − PEP into a posterior probability (higher is better); implies higherIsBetter false. |
| `aggregation` | `"best"` · `"sum"` · `"product"` |  | `"best"` |  | how a protein's peptide scores combine: best one, mean (sum over count), or product. |
| `chargeVariantsSeparate` | boolean |  | `true` |  | count each charge state of a peptide as its own evidence. |
| `modificationVariantsSeparate` | boolean |  | `true` |  | count each modified form of a peptide as its own evidence. |
| `useSharedPeptides` | boolean |  | `true` |  | let a peptide that maps to several proteins count for each of them. |
| `minPeptides` | number |  | `1` |  | report only proteins with at least this many evidences (0 reports every matched protein). |
| `greedyGroupResolution` | boolean |  | `false` |  | razor peptides: give each shared peptide only to its best-scoring protein or group (ties to the one with more matches) and drop proteins left with no peptide of their own. |
| `peptideProteinResolution` | boolean |  | `false` |  | resolve shared peptides between indistinguishable groups: in each connected set of groups the highest-probability group (then the one with more peptides) takes its peptides from the rest, and each set is reported as an ambiguity group; not combined with greedyGroupResolution. |
| `maxAmbiguousResidues` | number |  | `3` |  | how many ambiguous database residues (B, J, Z, X) one peptide match may resolve. |
| `ilEquivalent` | boolean |  | `false` |  | treat isoleucine and leucine (and a database J) as the same residue when mapping peptides. |
| `coverageOf` | string |  | `""` |  | the accession whose sequence coverage is drawn; empty draws the first protein of the best group, as the Coverage tab opens on. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `proteins` | any |  | one row per protein: accession, score, evidences counted, sequence coverage (%) |
| `groups` | any |  | indistinguishable protein groups, best first: probability (the best member score) and accessions |
| `ambiguityGroups` | any |  | with peptide–protein resolution: one group per connected set of groups, best group first, with the best probability. Null when that resolution was not asked for, because an empty list would read as a dataset with no ambiguity in it |
| `count` | number |  | proteins reported |
| `scoreColumn` | string or null |  | the column the match scores were read from, which decides whether higher or lower is better |
| `method` | string or null |  | the inference algorithm and mapping that produced these proteins, named |
| `coverageMap` | string or null |  | one protein's sequence with the peptides that identified it laid under the residues they cover, unique in blue and shared in orange: the Coverage tab's picture of `coverageOf` |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "infer_proteins",
  "arguments": {
    "psms": "<string>",
    "database": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### lookup_protein

**Lookup protein**: _What does the authority named return for this protein?_

Look up a protein: UniProt records, InterPro/Pfam domain architecture, STRING interaction networks, Human Protein Atlas expression, or a predicted/experimental structure from AlphaFold, PDB or EMDB.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"uniprot"` · `"interpro"` · `"string"` · `"proteinatlas"` · `"alphafold"` · `"pdb"` · `"emdb"` · `"complexportal"` · `"intact"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | an accession or gene symbol, or a command such as "get_domain_architecture:P04637" or "get_string_network:TP53,BRCA1 species=9606". A PLAIN UniProt search returns metadata only and never the residues (its field projection has no sequence field), so to get the SEQUENCE ask for the entry by accession: "get_uniprot_entries:P60568" (FASTA, residues included), or add "format=tsv fields=accession,sequence" for a table. |
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
  "name": "lookup_protein",
  "arguments": {
    "source": "uniprot",
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

### lookup_residue_sites

**Lookup residue sites**: _Which catalytic, binding and interface residues do member databases annotate in this protein's domains?_

The individual catalytic, substrate-binding, metal-binding and interface residues a member database annotates INSIDE a domain, for a known protein. Takes a UniProt accession. This is what InterProScan itself does not return — its per-location site array comes back empty — so it is a separate lookup against InterPro, keyed to an entry whose sequence the residue numbers belong to.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network; known UniProt accessions only.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `accession` | string | **yes** |  |  | UniProt accession, e.g. P00330. It must be the entry whose CURRENT sequence you mean: residues are numbered against it, so an accession for a protein that merely resembles yours puts a catalytic residue on the wrong amino acid. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `signatures` | any |  | per member-database signature: its accession, the database, its name, and each named site with every annotated residue and 1-based position |
| `residueCount` | number |  | total annotated residues across every signature |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "lookup_residue_sites",
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

### number_antibody

**Number antibody**: _Which antibody or TCR variable domains does this protein carry, how are they numbered, and which germlines are closest?_

Find antibody and T-cell-receptor variable domains in a protein sequence, number them under IMGT, Kabat, Chothia, Martin, AHo or Wolfguy, call chain type and species, and assign the closest V and J germline with percent identity. Validated against ANARCI 2026.2.13.2 on every chain of its PDB benchmark.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The numbering scheme chosen; ANARCI's HMMs identify the domains and species.

**Does not:**
- Numbering and germline assignment, not a structure or an affinity.
- A germline identity is against the reference set we ship.

**Not read from this result:** The answer is the numbering, regions and germlines, which the outputs carry; the Antibody panel's sentence joins them with antibody_liabilities' count, so neither door alone holds that reading.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (one-letter amino acids); may hold several domains, e.g. an scFv. |
| `scheme` | `"imgt"` · `"kabat"` · `"chothia"` · `"martin"` · `"aho"` · `"wolfguy"` |  | `"imgt"` |  | numbering scheme. Values: imgt (IMGT), kabat (Kabat), chothia (Chothia), martin (Martin (enhanced Chothia)), aho (AHo), wolfguy (Wolfguy). |
| `cdrDefinition` | `"imgt"` · `"kabat"` · `"chothia"` · `"north"` |  | `"imgt"` |  | where CDR1-3 begin and end (abnumber's borders; North is read in Chothia numbering). Kabat, Chothia and North define H, K and L chains only; TCR domains keep IMGT's. Values: imgt (IMGT), kabat (Kabat), chothia (Chothia), north (North). |
| `species` | (`"human"` · `"mouse"` · `"rat"` · `"rabbit"` · `"rhesus"` · `"pig"` · `"alpaca"` · `"cow"`)[] |  | `["human", "mouse"]` |  | species whose HMMs are preferred for the hit and whose germlines are searched (ANARCI's default: human and mouse). |
| `chainTypes` | (`"H"` · `"K"` · `"L"` · `"A"` · `"B"` · `"G"` · `"D"`)[] |  | `["H", "K", "L", "A", "B", "G", "D"]` |  | chain types to number: H, K, L (antibody); A, B, G, D (TCR). Others are still listed in the hit table. |
| `assignGermline` | boolean |  | `true` |  | assign the closest V and J germline genes. |
| `bitScoreThreshold` | number |  | `80` |  | minimum HMMER bit score for a domain to count (ANARCI's default 80). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `domains` | any |  | one entry per domain: chain type, species, sequence span, numbering as [position, residue] pairs, framework and CDR regions (0-based residue spans) under cdrDefinition, germlines |
| `chainTypes` | any |  | the chain type of each domain, in sequence order |
| `hits` | any |  | every HMM hit over the threshold: id, E-value, bit score, start, end |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "number_antibody",
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

### protein_disorder

**Protein disorder**: _Which stretches of this protein does FoldIndex predict unfolded?_

Intrinsic disorder along a protein by FoldIndex (Prilusky 2005): I_F = 2.785·⟨H⟩ − |⟨R⟩| − 1.151 over a sliding window, where ⟨H⟩ is mean normalized Kyte-Doolittle hydropathy and ⟨R⟩ the mean net charge per residue. Negative means predicted unfolded. Reports the whole-protein score, the per-window series, the runs below zero, and the Uversky charge-hydropathy point with the boundary it was judged against.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- FoldIndex's published formula over normalised Kyte-Doolittle hydropathy and net charge, at the window given.

**Does not:**
- A 2005 two-term predictor: it sees charge and hydropathy only.
- Negative means predicted unfolded, which is not evidence of disorder in the cell.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (unambiguous one-letter codes); wire it from translate_sequence. |
| `window` | number |  | `51` |  | sliding window in residues, odd so a window has a centre residue to report at (default 51, the size the FoldIndex paper uses). Short windows expose single loops; long ones report whole domains. |
| `chargeModel` | `"net"` · `"henderson-hasselbalch"` |  | `"net"` |  | 'net' counts whole charges K+R−D−E, which is what the paper does; 'henderson-hasselbalch' uses fractional charges at `pH`. They answer different questions and only the first is settled by the paper. |
| `pH` | number |  | `7` |  | pH for the Henderson-Hasselbalch model, ignored by 'net' (default 7.0, the pH the paper's ⟨R⟩ is defined at). Only applies when chargeModel is henderson-hasselbalch. |
| `pKaSet` | `"EMBOSS"` · `"DTASelect"` · `"Solomons"` · `"Sillero"` · `"Rodwell"` · `"Lehninger"` · `"Toseland"` · `"Thurlkill"` · `"Nozaki"` · `"Dawson"` · `"Bjellqvist"` · `"ProMoST"` · `"IPC_protein"` · `"IPC_peptide"` · `"Vollhardt"` |  | `"IPC_protein"` |  | named pKa set for the Henderson-Hasselbalch model (default IPC_protein, which is idpr's). Values: EMBOSS (EMBOSS (Rice 2000)), DTASelect (DTASelect (Tabb 2002)), Solomons (Solomons (Solomons 1992)), Sillero (Sillero (Sillero 1989)), Rodwell (Rodwell (Rodwell 1982)), Lehninger (Lehninger (Nelson 2017)), Toseland (Toseland (Toseland 2006)), Thurlkill (Thurlkill (Thurlkill 2006)), Nozaki (Nozaki (Nozaki 1971)), Dawson (Dawson (Dawson 1989)), Bjellqvist (Bjellqvist (Bjellqvist 1994)), ProMoST (ProMoST (Halligan 2004)), IPC_protein (IPC_protein (Kozlowski 2016)), IPC_peptide (IPC_peptide (Kozlowski 2016)), Vollhardt (Vollhardt (Vollhardt 2014)). |
| `countHistidine` | boolean |  | `false` |  | count histidine as positive in the 'net' model. False by default: the paper says charged residues at pH 7.0, and His (pKa ~6) is ~9% protonated there, so Uversky's set is K,R vs D,E — exposed because some FoldIndex descendants do count it. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `overall` | number |  | whole-protein FoldIndex from the global means — the number the 2005 paper's abstract reports. Below zero = predicted unfolded |
| `disorderedWindows` | number |  | how many windows score below zero |
| `disorderedFraction` | number |  | that count as a fraction of all windows |
| `windowCount` | number |  | how many windows were scored — the series length, so a fraction can be read back |
| `segments` | any |  | runs of consecutive negative windows as 1-based inclusive residue spans, with each run's mean and minimum I_F |
| `windows` | any |  | every window: { position, centerResidue, hydropathy, charge, score } — the series a plot draws |
| `scores` | any |  | just the I_F value per window, parallel to `positions` |
| `positions` | any |  | 1-based centre residue of each window, parallel to `scores` |
| `plot` | object or null |  | the FoldIndex profile as a plot; below zero is predicted disordered |
| `plot.x` | number[] |  |  |
| `plot.series` | object[] |  |  |
| `plot.series[].name` | string |  |  |
| `plot.series[].y` | (number or null)[] |  |  |
| `plot.xLabel` | string |  |  |
| `plot.yLabel` | string |  |  |
| `plot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `plot.title` | string |  |  |
| `plot.rules` | object[] |  |  |
| `plot.rules[].y` | number |  |  |
| `plot.rules[].label` | string |  |  |
| `meanHydropathy` | number |  | ⟨H⟩ over the whole chain — the x of the Uversky charge-hydropathy point |
| `meanNetCharge` | number |  | \|⟨R⟩\| over the whole chain — the y of the Uversky point |
| `boundary` | number |  | the Uversky 2000 boundary \|⟨R⟩\| = 2.785·⟨H⟩ − 1.151 evaluated at this protein's ⟨H⟩ — what `meanNetCharge` is above or below |
| `unfolded` | boolean |  | whether the whole-protein point sits above that boundary, i.e. predicted natively unfolded |
| `window` | number |  | the window actually used |
| `chargeModel` | string |  | the charge model actually used |
| `pKaSetName` | string |  | the pKa set actually used, or '' for the 'net' model which needs none |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_disorder",
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

### protein_disorder_metapredict

**Protein disorder metapredict**: _What is this protein's per-residue disorder score, and which regions are IDRs, by metapredict?_

Per-residue intrinsic disorder by metapredict (Emenecker, Griffith & Holehouse, Biophys J 2021; V2/V3 the lab's successors), a bidirectional LSTM trained to reproduce a consensus of disorder predictors, run locally. Reports a 0–1 score per residue, the IDRs and folded domains its domain caller draws from the smoothed profile, and the percentage of residues at or above the network's threshold. A different question from protein_disorder's FoldIndex, which reads composition alone.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- The metapredict version chosen; its network reproduces a consensus of other predictors, not an experiment.

**Does not:**
- A consensus-trained prediction: it inherits the biases of the predictors it was trained to reproduce.
- Domain boundaries come from the smoothed profile and move with the smoothing.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence; wire it from translate_sequence. |
| `version` | `"V3"` · `"V2"` · `"V1"` |  | `"V3"` |  | which trained network: V3 (the package default), V2, or V1 (the published 2021 network). Values: V3 (V3 (default)), V2 (V2), V1 (V1 (published, legacy)). |
| `threshold` | number |  |  |  | smoothed score above which a residue can seed an IDR, and per-residue score at or above which it counts as disordered. Omit for the network's own: V1 0.42, V2 and V3 0.5. |
| `minimumIdrSize` | number |  | `12` |  | the shortest IDR the domain caller reports, in residues; also sets the smoothing window (twice this, made odd). Default 12. Advanced. |
| `minimumFoldedDomain` | number |  | `50` |  | gaps between IDRs shorter than this are re-tested at 0.75× the threshold, so short ordered stretches inside an IDR are absorbed. Default 50. Advanced. |
| `gapClosure` | number |  | `10` |  | the longest run of sub-threshold residues closed when flanked by disordered runs of the same length. Default 10. Advanced. |
| `convert` | boolean |  | `true` |  | read B as N, U as C, X as G and Z as Q, as metapredict's FASTA readers do; off refuses them. Default true. Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `scores` | any |  | the per-residue disorder score, 0–1, residue 1 first |
| `idrs` | any |  | intrinsically disordered regions as 1-based inclusive spans with their length and mean score |
| `foldedDomains` | any |  | the complementary folded domains, same shape |
| `percentDisordered` | number | % | percentage of residues scoring at or above the threshold, to 3 dp |
| `disorderedResidues` | number |  | how many residues score at or above the threshold |
| `idrResidues` | number |  | how many residues the IDRs cover |
| `threshold` | number |  | the threshold actually used |
| `version` | string |  | the network actually used |
| `converted` | number |  | how many B/U/X/Z residues were read as N/C/G/Q |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_disorder_metapredict",
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

### protein_membrane_profile

**Protein membrane profile**: _Which windows of this protein look transmembrane, globular or surface-seeking on an Eisenberg hydrophobic-moment plot?_

Eisenberg hydrophobic-moment plot along a protein: per-window mean hydrophobicity and moment, each classified Globular / Transmembrane / Surface-seeking, plus those windows collapsed into residue spans. A hydrophobicity-based prediction, NOT a trained topology model.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- Eisenberg's consensus scale and his plot's class boundaries.

**Does not:**
- A hydrophobicity-based prediction, not a trained topology model: protein_topology is that.
- Spans come from collapsing windows, so their ends are window-resolution.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (unambiguous one-letter codes); wire it from translate_sequence. |
| `window` | number |  | `11` |  | sliding window in residues (default 11). |
| `angle` | number |  | `100` |  | rotational angle per residue in degrees: 100 for an alpha-helix (default), 160 for a beta-sheet. |
| `minWindows` | number |  | `2` |  | shortest run of same-class windows reported as a segment (default 2; a one-window run is usually noise). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `moment` | any |  | hydrophobic moment uH per window |
| `hydrophobicity` | any |  | mean Eisenberg hydrophobicity H per window |
| `plot` | object or null |  | the Eisenberg profile as a plot: moment and mean hydrophobicity per window |
| `plot.x` | number[] |  |  |
| `plot.series` | object[] |  |  |
| `plot.series[].name` | string |  |  |
| `plot.series[].y` | (number or null)[] |  |  |
| `plot.xLabel` | string |  |  |
| `plot.yLabel` | string |  |  |
| `plot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `plot.title` | string |  |  |
| `plot.rules` | object[] |  |  |
| `plot.rules[].y` | number |  |  |
| `plot.rules[].label` | string |  |  |
| `position` | any |  | per-window class: G globular, T transmembrane, S surface-seeking |
| `segments` | any |  | runs of one class as 1-based inclusive residue spans, with their mean/peak moment |
| `transmembrane` | number |  | how many segments are classified transmembrane |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_membrane_profile",
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

### protein_profile

**Protein profile**: _How does a chosen physicochemical scale vary along this protein?_

Windowed physicochemical profile along a protein (ExPASy ProtScale). Pass `scaleId` for any of the 57 scales ProtScale publishes plus the 14 Biopython tables it does not, with optional 0-1 normalisation; or pass `kind` for the five ProtParam profiles (hydropathy over the 28 GRAVY scales, Vihinen flexibility, Hopp & Woods hydrophilicity, Emini surface accessibility, Janin interior-to-surface transfer). Returns one value per window with the residue it centres on.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The scale is the published one named, applied over the window and normalisation stated.

**Does not:**
- A scale is a propensity, not a structural prediction.
- Different scales are not comparable, which is why the scale is named in the answer.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (unambiguous one-letter codes); wire it from translate_sequence. |
| `kind` | `"hydropathy"` · `"flexibility"` · `"hydrophilicity"` · `"accessibility"` · `"interior"` |  | `"hydropathy"` |  | which profile to compute. Ignore this and pass `scaleId` to reach the full ProtScale catalogue. |
| `scale` | `"KyteDoolitle"` · `"Aboderin"` · `"AbrahamLeo"` · `"Argos"` · `"BlackMould"` · `"BullBreese"` · `"Casari"` · `"Cid"` · `"Cowan3.4"` · `"Cowan7.5"` · `"Eisenberg"` · `"Engelman"` · `"Fasman"` · `"Fauchere"` · `"GoldSack"` · `"Guy"` · `"Jones"` · `"Juretic"` · `"Kidera"` · `"Miyazawa"` · `"Parker"` · `"Ponnuswamy"` · `"Rose"` · `"Roseman"` · `"Sweet"` · `"Tanford"` · `"Wilson"` · `"Zimmerman"` |  | `"KyteDoolitle"` |  | hydropathy scale. Values: KyteDoolitle (Kyte & Doolittle (1982)), Aboderin (Aboderin (Int J Biochem 2:537)), AbrahamLeo (Abraham & Leo (1987)), Argos (Argos (Eur J Biochem 128:565)), BlackMould (Black & Mould (1991)), BullBreese (Bull & Breese (1974)), Casari (Casari & Sippl, hydrophobic potential (JMB 224:725)), Cid (Cid (Protein Eng 5:373)), Cowan3.4 (Cowan at pH 3.4 (1990)), Cowan7.5 (Cowan at pH 7.5 (1990)), Eisenberg (Eisenberg, normalized consensus (1984)), Engelman (Engelman, transfer free energy (Annu Rev Biophys 15:321)), Fasman (Fasman (1989)), Fauchere (Fauchere (1983)), GoldSack (Goldsack & Chalifoux, free energy of mixing (J Theor Biol 39:645)), Guy (Guy, transfer free energy kcal/mol (1985)), Jones (Jones (J Theor Biol 50:167)), Juretic (Juretic (Theor Comput Chem 5:405)), Kidera (Kidera factors (J Protein Chem 4:23)), Miyazawa (Miyazawa, contact energy from 3D structures (1985)), Parker (Parker, HYDROPHILICITY from HPLC retention (1986)), Ponnuswamy (Ponnuswamy, folded-protein character (Prog Biophys Mol Biol 59:57)), Rose (Rose (1985)), Roseman (Roseman (1988)), Sweet (Sweet, optimized matching OMH (1983)), Tanford (Tanford (1962)), Wilson (Wilson, hydrophobic constants from HPLC retention (1981)), Zimmerman (Zimmerman (J Theor Biol 21:170)). Only applies when kind is hydropathy. |
| `scaleId` | `"molecularweight"` · `"numbercodons"` · `"bulkiness"` · `"polarityzimmerman"` · `"polaritygrantham"` · `"refractivity"` · `"recognitionfactors"` · `"hphob-eisenberg"` · `"hphob-sweet"` · `"hphob-woods"` · `"hydropath-doolittle"` · `"hphob-manavalan"` · `"hphob-leo"` · `"hphob-black"` · `"hphob-breese"` · `"hphob-fauchere"` · `"hphob-guy"` · `"hphob-janin"` · `"hphob-miyazawa"` · `"hphob-argos"` · `"hphob-roseman"` · `"hphob-tanford"` · `"hphob-wolfenden"` · `"hphob-welling"` · `"hphob-wilson"` · `"hphob-parker"` · `"hphob-ph3-4"` · `"hphob-ph7-5"` · `"hphob-mobility"` · `"hplchfba"` · `"hplctfa"` · `"transmembranetendency"` · `"hplc2-1"` · `"hplc7-4"` · `"buriedresidues"` · `"accessibleresidues"` · `"hphob-chothia"` · `"hphob-rose"` · `"ratioside"` · `"averageburied"` · `"averageflexibility"` · `"alpha-helixfasman"` · `"beta-sheetfasman"` · `"beta-turnfasman"` · `"alpha-helixroux"` · `"beta-sheetroux"` · `"beta-turnroux"` · `"coilroux"` · `"alpha-helixlevitt"` · `"beta-sheetlevitt"` · `"beta-turnlevitt"` · `"totalbeta-strand"` · `"antiparallelbeta-strand"` · `"parallelbeta-strand"` · `"a-a-composition"` · `"a-a-swiss-prot"` · `"relativemutability"` · `"biopython-argos"` · `"biopython-casari"` · `"biopython-cid"` · `"biopython-engelman"` · `"biopython-fasman"` · `"biopython-goldsack"` · `"biopython-jones"` · `"biopython-juretic"` · `"biopython-kidera"` · `"biopython-ponnuswamy"` · `"biopython-zimmerman"` · `"biopython-flex"` · `"biopython-surface-accessibility"` · `"biopython-janin"` |  |  |  | any of the 57 ExPASy ProtScale scales, or the 14 Biopython tables ProtScale does not publish. Pass this INSTEAD of `kind` and `scale`, never alongside them: sending `scaleId` together with `kind` is refused by name rather than one silently winning. The panel opens on `scaleId: hydropath-doolittle`, which computes the same curve as the `kind`/`scale` defaults. Values: molecularweight (Molecular weight), numbercodons (Number of codon(s)), bulkiness (Bulkiness), polarityzimmerman (Polarity / Zimmerman), polaritygrantham (Polarity / Grantham), refractivity (Refractivity), recognitionfactors (Recognition factors), hphob-eisenberg (Hphob. / Eisenberg et al.), hphob-sweet (Hphob. OMH / Sweet et al.), hphob-woods (Hphob. / Hopp & Woods), hydropath-doolittle (Hydropath. / Kyte & Doolittle), hphob-manavalan (Hphob. / Manavalan et al.), hphob-leo (Hphob. / Abraham & Leo), hphob-black (Hphob. / Black), hphob-breese (Hphob. / Bull & Breese), hphob-fauchere (Hphob. / Fauchere et al.), hphob-guy (Hphob. / Guy), hphob-janin (Hphob. / Janin), hphob-miyazawa (Hphob. / Miyazawa et al.), hphob-argos (Hphob. / Rao & Argos), hphob-roseman (Hphob. / Roseman), hphob-tanford (Hphob. / Tanford), hphob-wolfenden (Hphob. / Wolfenden et al.), hphob-welling (Hphob. / Welling & al), hphob-wilson (Hphob. HPLC / Wilson & al), hphob-parker (Hphob. HPLC / Parker & al), hphob-ph3-4 (Hphob. HPLC pH3.4 / Cowan), hphob-ph7-5 (Hphob. HPLC pH7.5 / Cowan), hphob-mobility (Hphob. / Rf mobility), hplchfba (HPLC / HFBA retention), hplctfa (HPLC / TFA retention), transmembranetendency (Transmembrane tendency), hplc2-1 (HPLC / retention pH 2.1), hplc7-4 (HPLC / retention pH 7.4), buriedresidues (% buried residues), accessibleresidues (% accessible residues), hphob-chothia (Hphob. / Chothia), hphob-rose (Hphob. / Rose & al), ratioside (Ratio hetero end/side), averageburied (Average area buried), averageflexibility (Average flexibility), alpha-helixfasman (alpha-helix / Chou & Fasman), beta-sheetfasman (beta-sheet / Chou & Fasman), beta-turnfasman (beta-turn / Chou & Fasman), alpha-helixroux (alpha-helix / Deleage & Roux), beta-sheetroux (beta-sheet / Deleage & Roux), beta-turnroux (beta-turn / Deleage & Roux), coilroux (Coil / Deleage & Roux), alpha-helixlevitt (alpha-helix / Levitt), beta-sheetlevitt (beta-sheet / Levitt), beta-turnlevitt (beta-turn / Levitt), totalbeta-strand (Total beta-strand), antiparallelbeta-strand (Antiparallel beta-strand), parallelbeta-strand (Parallel beta-strand), a-a-composition (A.A. composition), a-a-swiss-prot (A.A. comp. in Swiss-Prot), relativemutability (Relative mutability), biopython-argos (Argos), biopython-casari (Casari & Sippl), biopython-cid (Cid et al.), biopython-engelman (Engelman (GES)), biopython-fasman (Fasman), biopython-goldsack (Gold Sack & Chalifoux), biopython-jones (Jones), biopython-juretic (Juretic et al.), biopython-kidera (Kidera et al.), biopython-ponnuswamy (Ponnuswamy), biopython-zimmerman (Zimmerman (hydrophobicity)), biopython-flex (Flexibility (Vihinen)), biopython-surface-accessibility (Surface accessibility (Emini)), biopython-janin (Janin (Biopython rounding)). |
| `normalize` | boolean |  | `false` |  | ProtScale's 'normalize the scale from 0 to 1' — rescales the twenty scale values before windowing, so profiles from different scales are comparable. Requires `scaleId`. |
| `window` | number |  | `9` |  | ProtScale window in residues, odd (default 9). IGNORED for 'flexibility', whose Vihinen parameters are only defined at 9. Only applies when kind is hydropathy or hydrophilicity or accessibility or interior. |
| `edge` | number |  | `1` |  | ProtScale relative weight of the window's edge residues, 0-1 (default 1 = unweighted). |
| `weightVariation` | `"linear"` · `"exponential"` |  | `"linear"` |  | ProtScale's weight model between the centre and the edge weight: 'linear' steps down evenly, 'exponential' decays steeply near the centre. Requires `scaleId`; identical at edge 1. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `values` | any |  | one profile value per window |
| `centres` | any |  | 0-based residue index each window centres on, parallel to `values` |
| `label` | string |  | the profile's cited name, e.g. 'Hydropathy (KyteDoolitle)' |
| `plot` | object or null |  | the profile as a plot along the chain |
| `plot.x` | number[] |  |  |
| `plot.series` | object[] |  |  |
| `plot.series[].name` | string |  |  |
| `plot.series[].y` | (number or null)[] |  |  |
| `plot.xLabel` | string |  |  |
| `plot.yLabel` | string |  |  |
| `plot.mark` | `"line"` · `"bar"` · `"point"` |  |  |
| `plot.title` | string |  |  |
| `plot.rules` | object[] |  |  |
| `plot.rules[].y` | number |  |  |
| `plot.rules[].label` | string |  |  |
| `window` | number |  | window actually used (flexibility forces 9) |
| `normalized` | boolean |  | whether the scale was rescaled to 0-1 before windowing. False for the five ProtParam kinds, which are never rescaled |
| `weightVariation` | string |  | the ProtScale weight model the values were computed under, 'linear' or 'exponential' ('linear' for the five ProtParam kinds) |
| `reference` | string |  | the scale's primary citation, when it came from the ProtScale catalogue. Empty for the five ProtParam kinds |
| `peak` | number |  | index into `values` of the LARGEST value. Large is not a synonym for hydrophobic: on a transfer free energy or a hydrophilicity scale the largest window is the most hydrophilic one, and on a flexibility or accessibility profile it is neither. `label` names the scale; `protein_properties.gravyHydrophobicEnd` answers the direction for the 28 hydropathy tables |
| `peakResidue` | number |  | 1-based residue the peak window centres on |
| `trough` | number |  | index into `values` of the SMALLEST value — the other extreme, which is the hydrophobic one on an inverted scale |
| `troughResidue` | number |  | 1-based residue the trough window centres on |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_profile",
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

### protein_properties

**Protein properties**: _What are this protein's mass, formula, isoelectric point, instability index and amphipathicity?_

Molecular weight (average + monoisotopic), molecular formula, isoelectric point, instability index and amphipathicity (Boman index, Eisenberg hydrophobic moment) of a protein sequence (Biopython ProtParam + `peptides` + `pyteomics`).

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- ProtParam's tables and pKa sets, with `peptides` and `pyteomics` for the rest.

**Does not:**
- Sequence-derived properties: post-translational modifications, folding and complexes are not in them.
- An instability index is a published heuristic, not a measured half-life.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (unambiguous one-letter codes); wire it from translate_sequence. |
| `momentWindow` | number |  | `11` |  | sliding window for the hydrophobic moment, in residues (default 11; clamped to the sequence length). |
| `cystineConvention` | `"cystine"` · `"perCysteine"` |  | `"cystine"` |  | how the oxidised e280 counts cysteines: 'cystine' = 125 per disulfide (ProtParam, default) or 'perCysteine' = 62.5 per residue (SnapGene). They differ only on an ODD cysteine count. |
| `gravyScale` | `"KyteDoolitle"` · `"Aboderin"` · `"AbrahamLeo"` · `"Argos"` · `"BlackMould"` · `"BullBreese"` · `"Casari"` · `"Cid"` · `"Cowan3.4"` · `"Cowan7.5"` · `"Eisenberg"` · `"Engelman"` · `"Fasman"` · `"Fauchere"` · `"GoldSack"` · `"Guy"` · `"Jones"` · `"Juretic"` · `"Kidera"` · `"Miyazawa"` · `"Parker"` · `"Ponnuswamy"` · `"Rose"` · `"Roseman"` · `"Sweet"` · `"Tanford"` · `"Wilson"` · `"Zimmerman"` |  | `"KyteDoolitle"` |  | hydropathy scale GRAVY is averaged over (all 28 ProtParam/ProtScale scales; default Kyte & Doolittle). Values: KyteDoolitle (Kyte & Doolittle (1982)), Aboderin (Aboderin (Int J Biochem 2:537)), AbrahamLeo (Abraham & Leo (1987)), Argos (Argos (Eur J Biochem 128:565)), BlackMould (Black & Mould (1991)), BullBreese (Bull & Breese (1974)), Casari (Casari & Sippl, hydrophobic potential (JMB 224:725)), Cid (Cid (Protein Eng 5:373)), Cowan3.4 (Cowan at pH 3.4 (1990)), Cowan7.5 (Cowan at pH 7.5 (1990)), Eisenberg (Eisenberg, normalized consensus (1984)), Engelman (Engelman, transfer free energy (Annu Rev Biophys 15:321)), Fasman (Fasman (1989)), Fauchere (Fauchere (1983)), GoldSack (Goldsack & Chalifoux, free energy of mixing (J Theor Biol 39:645)), Guy (Guy, transfer free energy kcal/mol (1985)), Jones (Jones (J Theor Biol 50:167)), Juretic (Juretic (Theor Comput Chem 5:405)), Kidera (Kidera factors (J Protein Chem 4:23)), Miyazawa (Miyazawa, contact energy from 3D structures (1985)), Parker (Parker, HYDROPHILICITY from HPLC retention (1986)), Ponnuswamy (Ponnuswamy, folded-protein character (Prog Biophys Mol Biol 59:57)), Rose (Rose (1985)), Roseman (Roseman (1988)), Sweet (Sweet, optimized matching OMH (1983)), Tanford (Tanford (1962)), Wilson (Wilson, hydrophobic constants from HPLC retention (1981)), Zimmerman (Zimmerman (J Theor Biol 21:170)). |
| `pH` | number |  | `7` |  | pH the net charge is reported at (default 7.0). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `mw` | number or null | Da | molecular weight [Da] — a FLOOR when `nonStandard` is non-empty, because ProtParam has no mass for those letters and still counts them in the length |
| `length` | number or null |  | residues analysed, including any the mass tables have no row for |
| `nonStandard` | any |  | residues with no mass at all (X, B, Z, gaps, *), with their positions: excluded from `mw`, `monoisotopicMw`, `formula` and `elements`, still counted in `length`. Empty on a clean chain |
| `scaleNonStandard` | any |  | residues that ARE weighed but have no per-residue scale value (U, O). They are why `gravy` and `instability` can come back null on a sequence whose mass is exact |
| `pI` | number or null |  | isoelectric point |
| `instability` | number or null |  | instability index (>40 = unstable in vivo), or null when a residue the Guruprasad table has no row for makes it undefined — refused rather than computed on a spliced sequence |
| `stable` | boolean or null |  | ProtParam's own reading of the index: at or below 40. Null exactly when `instability` is — there is no verdict without a value |
| `boman` | number or null | kcal/mol | Boman potential protein-interaction index [kcal/mol] (>2.48 = protein-binding) |
| `momentHelix` | number or null |  | max Eisenberg hydrophobic moment at the α-helix periodicity (100°) |
| `momentSheet` | number or null |  | max Eisenberg hydrophobic moment at the β-sheet periodicity (160°) |
| `momentWindow` | number or null |  | the window the two moments were measured over, after the clamp to the sequence length — a short peptide is not measured over 11 residues it does not have |
| `monoisotopicMw` | number or null | Da | monoisotopic molecular weight [Da] — what mass spectrometry reports. Null when a residue has no mass, rather than a mass for a different molecule |
| `formula` | string |  | molecular formula, ProtParam style (e.g. C1755H2634N466O557S5); empty when a residue has no formula |
| `atoms` | number or null |  | total number of atoms in the molecule, or null when a residue has no formula |
| `extinctionReduced` | number or null | M⁻¹ cm⁻¹ | molar extinction coefficient at 280 nm [M-1 cm-1], all cysteines reduced |
| `extinctionCystines` | number or null | M⁻¹ cm⁻¹ | molar extinction coefficient at 280 nm [M-1 cm-1], cystines formed (per `cystineConvention`) |
| `a280` | number or null |  | A280 of a 1 g/L solution (cystines form) — divide a spectrophotometer reading by this |
| `nTerminal` | string |  | the N-terminal residue the N-end rule half-lives below are read from |
| `halfLifeMammalian` | string |  | estimated in-vivo half-life, mammalian reticulocytes (N-end rule); '—' when the N-terminus has no entry |
| `halfLifeYeast` | string |  | estimated in-vivo half-life, yeast (N-end rule) |
| `halfLifeEcoli` | string |  | estimated in-vivo half-life, E. coli (N-end rule) |
| `gravy` | number or null |  | grand average of hydropathicity over `gravyScale`, or null when a residue has no value on it |
| `gravyScale` | string or null |  | which hydropathy scale `gravy` was averaged over |
| `gravyHydrophobicEnd` | string or null |  | which end of `gravyScale` is the hydrophobic one: 'higher' (Kyte & Doolittle and most others) or 'lower' (a transfer free energy or a hydrophilicity scale). Read `gravy` against this, never against zero alone |
| `gravyZeroIsMeaningful` | boolean or null |  | whether `gravyScale` takes both signs. False on the eight one-sided tables (Rose, Miyazawa, Argos, …), where the sign of `gravy` is a property of the scale and says nothing about this protein |
| `aliphatic` | number or null |  | aliphatic index (Ikai 1980) — higher suggests greater thermostability |
| `aromaticity` | number or null |  | aromaticity (Lobry 1994): the F+W+Y frequency, as a fraction |
| `helix` | number or null |  | fraction of residues favouring an alpha-helix |
| `turn` | number or null |  | fraction of residues favouring a turn |
| `sheet` | number or null |  | fraction of residues favouring a beta-sheet |
| `charge` | number or null |  | net charge at `pH` |
| `composition` | any |  | residue counts, one entry per standard amino acid (ProtParam's composition table) |
| `compositionPercent` | any |  | the same table as mole percent of the chain |
| `elements` | any |  | atom counts per element (C, H, N, O, S) behind the formula, or null when a residue has no formula |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_properties",
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

### protein_topology

**Protein topology**: _Which residues of this protein are inside, in a transmembrane helix, or outside, by the HMM-TM model?_

Transmembrane topology of a protein by the HMM-TM 114-state hidden Markov model (JUCHMME, Bagos et al.), decoded residue by residue into inside / transmembrane-helix / outside runs. Reports the labelled path, the runs as residue spans, and the per-residue posterior. Needs the trained model, which the host loads once per session — this refuses by name when it has not been.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- JUCHMME's trained 114-state model applies to this protein's family.
- The host has loaded the trained model; without it the tool says so.

**Does not:**
- A posterior per residue is the model's confidence, not an experimental topology.
- Signal peptides can be mistaken for helices, which the labelled path shows.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence (unambiguous one-letter codes); wire it from translate_sequence. |
| `decoding` | `"viterbi"` · `"posterior-viterbi"` · `"optimal-accuracy"` · `"n-best"` |  | `"viterbi"` |  | which decoder: 'viterbi' the single most probable state path (default, and the fast one); 'posterior-viterbi' and 'optimal-accuracy' re-decode over the posterior; 'n-best' beams over label SEQUENCES rather than states and is a genuinely different algorithm — and much slower on a long chain. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `path` | string |  | one label per residue, in sequence order |
| `segments` | any |  | runs of one label as 1-based inclusive residue spans |
| `helices` | number |  | how many runs are transmembrane helices — 0 means no helix was predicted, which for a cytosolic protein is the right answer and not a failure |
| `summary` | string |  | the topology in words — how many helices and which side the N-terminus is on, or that none was predicted |
| `logProb` | number |  | log probability of the decoded path, in nats |
| `decoding` | string |  | which decoder produced this path |
| `posterior` | any |  | per-residue posterior probability of each label — the confidence behind the path |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "protein_topology",
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

### rps_blast_cdd

**RPS BLAST CDD**: _Which conserved domains does NCBI's CD-Search find in this protein?_

RPS-BLAST a protein against NCBI's Conserved Domain Database (CDD) or one of its member collections (Pfam, SMART, COG, KOG, PRK, TIGR, NCBI-curated), through NCBI Batch CD-Search. Returns every domain hit with its hit type (specific, non-specific, superfamily, multi-domain), residue span, E-value, bit score, CDD accession, superfamily cluster and whether the alignment stops short of either end of the model. This is the rpsblast program. Give `protein`, or give `dna` to send its six reading frames as six proteins (per-frame CD-Search: each E-value is for its own frame, which is not rpstblastn; rpstblastn_smart runs rpstblastn itself on this machine). The query leaves the machine for NCBI.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network; the protein leaves the machine.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string |  |  |  | the protein sequence, one-letter codes; wire it from translate_sequence or read it off a CDS. |
| `dna` | string |  |  |  | instead of `protein`: DNA whose six reading frames are sent as six proteins, labeled frame +1 … frame -3; each hit names its frame in queryLabel. |
| `smode` | `"auto"` · `"prec"` · `"live"` |  | `"auto"` |  | NCBI's search mode: automatic uses precomputed results where they exist, precomputed never runs a search, live always runs one. Only live honours db, evalue and maxhit. Values: auto (automatic), prec (precomputed only), live (live search). |
| `db` | string |  | `"cdd"` |  | the PSSM collection, as the live Batch CD-Search form names it (cdd, cdd_ncbi, oasis_pfam, oasis_smart …); live mode only. Only applies when smode is live. |
| `evalue` | number |  | `0.01` | ≥ 0 | E-value cutoff; live mode only (automatic and precomputed apply 0.01). Only applies when smode is live. |
| `maxhit` | number |  | `500` | ≥ 1 | most hits per protein; live mode only (automatic and precomputed apply 500). Only applies when smode is live. |
| `compbasedadj` | `0` · `1` · `2` · `3` |  | `1` |  | 0 no composition-based statistics · 1 composition-based statistics · 2 composition matrix adjust · 3 forced full matrix adjust. |
| `filter` | boolean |  | `false` |  | mask low-complexity regions of the query before searching. |
| `dmode` | `"rep"` · `"std"` · `"full"` |  | `"std"` |  | which hits come back: concise (the best hit per region), standard (the best per source database per region) or full (every hit). Values: rep (concise), std (standard), full (full). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `hits` | any |  | every domain hit: queryLabel (the frame, for a `dna` query), hitType, pssmId, from, to (1-based residues), evalue, bitscore, accession, shortName, incompleteN, incompleteC, superfamily, definition |
| `count` | number |  | domain hits returned |
| `cdsid` | string |  | NCBI's search id, re-openable in CD-Search's own viewer for two days |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "rps_blast_cdd",
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

### rps_blast_smart

**RPS BLAST SMART**: _Which SMART domain models does this protein hit?_

rpsblast, run on this machine: find conserved domains in a protein against NCBI's SMART domain models (1,011 PSSMs from CDD). NCBI BLAST+ 2.17.0's algorithms, checked against the rpsblast program on every bundled protein. Nothing is sent anywhere; for all of CDD use rps_blast_cdd, which goes to NCBI.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- NCBI BLAST+ 2.17.0's rpsblast against the bundled SMART PSSMs.

**Does not:**
- SMART's 1,011 models only; all of CDD is rps_blast_cdd.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** smart

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein, one-letter codes; wire it from translate_sequence or read it off a CDS. |
| `evalue` | number |  | `10` | ≥ 0 | report alignments with E at most this (`-evalue`); BLAST's default is 10. |
| `max_target_seqs` | number |  | `500` | ≥ 1 | most domain models reported (`-max_target_seqs`). |
| `source` | `"bundled"` · `"ncbi"` |  | `"bundled"` |  | where the SMART database is read from: 'bundled' (a byte-identical copy of NCBI's file) or 'ncbi' (NCBI's FTP site, now). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `domains` | any |  | every SMART domain hit, best first: accession, shortName, title, profileLength and each HSP's residue coordinates, model coordinates, score, bits, E-value, identities, positives, gaps and aligned strings |
| `count` | number |  | domain models hit |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "rps_blast_smart",
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

### rpstblastn_smart

**RPSTBLASTN SMART**: _Which SMART domains does this DNA encode in any of its six frames?_

rpstblastn, run on this machine: find conserved domains in DNA by searching all six reading frames against NCBI's SMART domain models (1,011 PSSMs from CDD). Leave `sequence` empty to search the open record. NCBI BLAST+ 2.17.0's algorithms, checked against the rpstblastn program on every bundled GenBank record. Nothing is sent anywhere; for all of CDD use rps_blast_cdd on a translated protein.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- NCBI BLAST+ 2.17.0's rpstblastn against the bundled SMART PSSMs, with the genetic code given.

**Does not:**
- SMART's 1,011 models only; all of CDD is rps_blast_cdd.

**Validated:** against the reference implementation by 1 golden suite.

**Reads bundled data:** smart

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the DNA to search, 5′→3′; leave empty to search the open record. Both strands are searched. |
| `evalue` | number |  | `10` | ≥ 0 | report alignments with E at most this (`-evalue`); BLAST's default is 10. |
| `max_target_seqs` | number |  | `500` | ≥ 1 | most domain models reported (`-max_target_seqs`). |
| `comp_based_stats` | `0` · `1` |  | `1` |  | composition-based statistics: 1 on (the default, Schäffer et al. 2001), 0 off. |
| `genetic_code` | number |  | `1` | 1–33 | NCBI genetic code used to translate the six frames (`-query_gencode`). |
| `source` | `"bundled"` · `"ncbi"` |  | `"bundled"` |  | where the SMART database is read from: 'bundled' (a byte-identical copy of NCBI's file) or 'ncbi' (NCBI's FTP site, now). Advanced. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `domains` | any |  | every SMART domain hit, best first: accession, shortName, title, profileLength and each HSP's nucleotide coordinates (1-based, to < from on the minus strand) and frame, model coordinates, score, bits, E-value, identities, positives, gaps and aligned strings |
| `count` | number |  | domain models hit |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "rpstblastn_smart",
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

### scan_motif_sites

**Scan motif sites**: _Where does a transcription-factor matrix match this sequence, on either strand, at a threshold set as a fraction of that matrix's own score range?_

Find every place a transcription-factor binding motif (a position-frequency matrix, such as a JASPAR matrix's counts) matches a DNA sequence, on both strands, at a threshold set per motif as a fraction of that matrix's own score range. It is the scan the optimizer's avoid-motif specification counts, so the sites it lists are the ones an optimisation with that motif would remove. Each site carries its log-odds score and where that score falls in the matrix's range. A match is a sequence resemblance to the matrix, not evidence of binding.

<sub>read-only · runs locally on the engine</sub>

**Assumes:**
- The matrix is a position-frequency matrix with the pseudocount and background the scan states.

**Does not:**
- A matrix match is a sequence-level prediction, not evidence of binding in a cell.
- The threshold is relative to this matrix's range, so it is not comparable between matrices.

**Not read from this result:** The matrix hits on both strands with their scores; the Optimize panel lists them per motif and writes no sentence over them.

**Validated:** against the reference implementation by 2 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `sequence` | string |  |  |  | the DNA to scan - leave unset to use the open record. |
| `motifs` | object[] | **yes** |  |  | the matrices, each {name, counts: {A, C, G, T} per position, relativeThreshold (0-1 of the matrix's score range) or threshold (absolute log-odds)}. Pseudocounts are JASPAR's sqrt(N) by default. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `sites` | any |  | every match, by position: motif name, start and end (0-based, end exclusive), strand, log-odds score and its fraction of the matrix's range |
| `count` | number |  | how many matches in total |
| `perMotif` | any |  | the number of matches for each motif, by name |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "scan_motif_sites",
  "arguments": {
    "motifs": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### scan_protein_domains

**Scan protein domains**: _Which domains and families does InterProScan find in this protein?_

De-novo protein domain and family annotation: submits a protein to EMBL-EBI InterProScan and returns every member-database signature that matches it — Pfam, CATH-Gene3D, SUPERFAMILY, PANTHER, PROSITE, SMART, CDD and the rest — with its InterPro entry, its GO terms, its coordinates and its E-value. This is the DOMAIN half of the Protein domains panel; for the short linear motifs a profile scan cannot see, use find_linear_motifs, which takes the `domains` this tool emits. The scan runs at EBI, takes minutes, and needs a contact address because EBI requires one.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network; the protein leaves the machine.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `protein` | string | **yes** |  |  | the protein sequence, one-letter codes; wire it from translate_sequence or read it off a CDS. |
| `applications` | string |  | `""` |  | member databases to run, comma-separated, using InterProScan's own ids (Pfam, Gene3D, SUPERFAMILY, PANTHER, PROSITE …). Empty runs the service's own default set, which is every database it has enabled. An id the live service does not advertise is refused by name rather than dropped. |
| `goTerms` | boolean |  | `true` |  | ask InterPro to attach Gene Ontology terms to the integrated entries, so a match carries its function rather than only its accession. |
| `pathways` | boolean |  | `true` |  | ask InterPro to attach pathway cross-references (Reactome, KEGG, MetaCyc) to the integrated entries. |
| `representativeOnly` | boolean |  | `false` |  | keep only the matches InterProScan itself marks representative — its own answer to “which of these overlapping signatures describes this region best”. |
| `integratedOnly` | boolean |  | `false` |  | keep only signatures integrated into an InterPro entry, dropping member-database hits InterPro has not curated into one. |
| `maxEvalue` | number |  | `0` | ≥ 0 | drop matches whose E-value is worse than this. 0 applies no threshold. A match the member database scores no E-value for (Coils, MobiDB-lite, Phobius) is KEPT either way — it has not failed the threshold, it was never scored against one. |
| `email` | string |  |  |  | EBI requires a contact address on every submission (their abuse contact, not a login). Left empty, the one saved in any EMBL-EBI panel is used, which only the in-browser doors can read. It is sent to EBI with the job and stored nowhere by this tool. |
| `visibleLibraries` | string |  | `""` |  | keep only matches from these member databases, comma-separated, as the RESULT document spells them (PFAM, GENE3D, SUPERFAMILY, CDD, PANTHER, MOBIDB_LITE …). This narrows what comes back; `applications` narrows what is RUN, and they are not the same question — a caller reading one library out of the service's default set wants this one. Empty keeps every database that answered. |
| `sortBy` | `"length"` · `"position"` · `"evalue"` · `"library"` |  | `"length"` |  | row order of the returned matches. Values: length (longest first), position (position along the protein), evalue (best E-value first), library (by member database). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `matches` | any |  | every signature that matched, after the reading knobs: member database, signature accession and name, the InterPro entry it is integrated into, its kind (domain, family, site, repeat, homologous superfamily…), 1-based inclusive aaStart/aaEnd, the fragments a discontinuous domain is made of, the E-value and the GO and pathway cross-references |
| `count` | number |  | matches returned, after the reading knobs |
| `domains` | string |  | the FOLDED regions only — domains, as `start-end@label` residue ranges — ready to wire straight into find_linear_motifs.domains so its globular-domain filter can bury motifs in them. Families, signal peptides, transmembrane helices, coiled coils and disordered spans are excluded: those are not folds a motif can hide inside, and disorder is where linear motifs live |
| `jobId` | string |  | EBI's own job id, which is re-fetchable at their dispatcher for as long as they keep it — the provenance of this result, not an internal handle |
| `provenance` | any |  | the InterProScan version that ran, the MD5 the service computed over the sequence it analyzed, the member databases asked for, how many matches the scan returned before the reading knobs, and which of those knobs ran |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "scan_protein_domains",
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
