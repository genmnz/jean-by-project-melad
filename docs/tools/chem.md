# ⚗️ Cheminformatics

_Molecules, conformers, scaffolds, reactions, chemical space and library screening._

16 tools. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. How to call any of them: [protocol](../protocol.md). All sections: [index](README.md).

## Contents

| Tool | What it answers |
|---|---|
| [`activity_cliffs`](#activity_cliffs) | Which pairs of similar molecules differ most in activity (SALI)? |
| [`assess_small_molecule`](#assess_small_molecule) | What are this molecule's RDKit descriptors, drug-likeness rule results and structural alerts? |
| [`canonical_tautomer`](#canonical_tautomer) | Which tautomers does this molecule have, and which is canonical? |
| [`cluster_molecules`](#cluster_molecules) | How do these molecules cluster, or which are most diverse, on Morgan fingerprints? |
| [`compare_molecules`](#compare_molecules) | How similar are these two molecules under each fingerprint? |
| [`decompose_r_groups`](#decompose_r_groups) | What R-groups does each molecule carry on this core? |
| [`enumerate_protonation_states`](#enumerate_protonation_states) | Which protonation states does this molecule take across this pH window? |
| [`enumerate_reaction`](#enumerate_reaction) | What products does this reaction SMARTS give over these reactants? |
| [`generate_conformers`](#generate_conformers) | What 3D conformers does this molecule take, and how is each scored? |
| [`lookup_compound`](#lookup_compound) | What does the authority named return for this compound or drug? |
| [`map_chemical_space`](#map_chemical_space) | Where does each molecule sit on the principal components of the property table or fingerprint bits? |
| [`map_reaction_atoms`](#map_reaction_atoms) | Which reactant atom does each product atom come from? |
| [`matched_molecular_pairs`](#matched_molecular_pairs) | Which pairs of these molecules differ by one small change? |
| [`scaffold_network`](#scaffold_network) | What is the scaffold network of these molecules? |
| [`search_molecule_library`](#search_molecule_library) | Which of these molecules contain this SMARTS substructure? |
| [`write_structure_library`](#write_structure_library) | Write these molecules as one structure file. |

---

### activity_cliffs

**Activity cliffs**: _Which pairs of similar molecules differ most in activity (SALI)?_

SALI activity cliffs (Guha & Van Drie 2008) in a list of small molecules with one activity each: every pair scored as the activity difference over one minus the Tanimoto similarity of RDKit path fingerprints, steepest first; identical fingerprints with different activities score Infinity. Indices are 0-based.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- SALI (Guha & Van Drie 2008) on the similarity and scale given.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `activities` | number[] | **yes** |  |  | one number per structure, in the same order; a non-number leaves it out. |
| `scale` | `"pIc50Um"` · `"asGiven"` |  | `"pIc50Um"` |  | how the activities are read. Values: pIc50Um (pIC50 from a µM IC50), asGiven (As given). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the cliffs in words, generated from this run |
| `pairs` | any |  | every pair, highest SALI first: i the more active, j, similarity, SALI |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "activity_cliffs",
  "arguments": {
    "molecules": [],
    "activities": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### assess_small_molecule

**Assess small molecule**: _What are this molecule's RDKit descriptors, drug-likeness rule results and structural alerts?_

Assess a small molecule given as SMILES or a molfile: RDKit's descriptors, medchem's drug-likeness rules (Lipinski, Veber, Ghose, Egan, REOS, rule of three, CNS and more) and the papers' own readings where medchem departs from them, with every bound and this molecule's value, a structural-alert screen (PAINS, Brenk, NIH, ZINC and ChEMBL's seven curated sets) with the matched atoms, the molecular formula with its masses and natural-abundance isotope pattern, QED drug-likeness under all three weightings, ESOL aqueous solubility, synthetic accessibility and natural-product likeness, the Bemis–Murcko scaffold and generic framework, the BOILED-Egg's gut-absorption and brain-penetration verdicts, and per-atom logP, polar-surface and charge contributions. Readings are taken with hydrogens implicit, the form the descriptors and the rules' papers assume. An alert flags a nuisance or reactive substructure; it is not a verdict on activity or toxicity.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's descriptors and medchem's rule and alert definitions.

**Does not:**
- Rules flag; they do not predict activity.

**Validated:** against the reference implementation by 3 golden suites.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecule` | string | **yes** |  |  | the structure: a SMILES string or an MDL molfile (V2000 or V3000). One molecule; for an SDF, pass one record. |
| `rules` | (`"rule_of_five"` · `"rule_of_five_beyond"` · `"rule_of_four"` · `"rule_of_three"` · `"rule_of_three_extended"` · `"rule_of_two"` · `"rule_of_ghose"` · `"rule_of_veber"` · `"rule_of_reos"` · `"rule_of_chemaxon_druglikeness"` · `"rule_of_egan"` · `"rule_of_pfizer_3_75"` · `"rule_of_gsk_4_400"` · `"rule_of_oprea"` · `"rule_of_xu"` · `"rule_of_cns"` · `"rule_of_respiratory"` · `"rule_of_five_paper"` · `"rule_of_ghose_paper"` · `"rule_of_reos_paper"`)[] |  | `["rule_of_five", "rule_of_five_beyond", "rule_of_four", "rule_of_three", "rule_of_three_extended", "rule_of_two", "rule_of_ghose", "rule_of_veber", "rule_of_reos", "rule_of_chemaxon_druglikeness", "rule_of_egan", "rule_of_pfizer_3_75", "rule_of_gsk_4_400", "rule_of_oprea", "rule_of_xu", "rule_of_cns", "rule_of_respiratory", "rule_of_five_paper", "rule_of_ghose_paper", "rule_of_reos_paper"]` |  | which drug-likeness rules to evaluate, by id: medchem's 17, plus the papers' own readings of Lipinski, Ghose and REOS (ids ending _paper). Every rule by default. |
| `alert_sets` | (`"PAINS_A"` · `"PAINS_B"` · `"PAINS_C"` · `"BRENK"` · `"NIH"` · `"ZINC"` · `"CHEMBL_Glaxo"` · `"CHEMBL_Dundee"` · `"CHEMBL_BMS"` · `"CHEMBL_MLSMR"` · `"CHEMBL_Inpharmatica"` · `"CHEMBL_LINT"` · `"CHEMBL_SureChEMBL"`)[] |  | `["PAINS_A", "PAINS_B", "PAINS_C", "BRENK", "NIH", "ZINC", "CHEMBL_Glaxo", "CHEMBL_Dundee", "CHEMBL_BMS", "CHEMBL_MLSMR", "CHEMBL_Inpharmatica", "CHEMBL_LINT", "CHEMBL_SureChEMBL"]` |  | which structural-alert catalogs to screen against. Empty screens nothing, which is not a clean result. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the assessment in one sentence, generated from this run |
| `canonical_smiles` | string |  | RDKit's canonical SMILES of the molecule every reading was taken on |
| `structure` | string or null |  | the 2D structure every reading was taken on, drawn by RDKit with implicit hydrogens as the chemistry tab opens it |
| `descriptors` | any |  | RDKit's descriptors under RDKit's own keys (exactmw, CrippenClogP, tpsa, NumHBD …) |
| `rules` | any |  | one entry per rule evaluated: id, label, passes, citation, and every clause with its property, bound and this molecule’s value. A rule with anyClauses passes when at least one of those holds |
| `alerts` | any |  | every alert matched: its set, name, SMARTS and the atom indices of the first match, numbered on the implicit-hydrogen molecule |
| `boiled_egg` | any |  | the BOILED-Egg placement (Daina & Zoete 2016) of the neutral, unsalted ChEMBL parent as the paper places it (`placed` says whether that is the parent or, when the pipeline refuses one or it is the molecule itself, the record as drawn; `asDrawn` and `parent` carry both): tPSA counting S and P, RDKit's Crippen logP standing in for WLOGP, and for the gut-absorption (hia) and brain-penetration (bbb) ellipses whether the point is inside, its summed focal distance and the ellipse's major axis; region is yolk, white or outside |
| `formula` | any |  | RDKit's molecular formula (every hydrogen, isotope labels merged, charge suffixed) with its element counts and charge, the monoisotopic and average masses in Da, and OpenMS's coarse natural-abundance isotope envelope (isotope index, mass, share of molecules), or the reason there is none (an isotope-labeled structure, or an element OpenMS has no isotope data for) |
| `synthetic_accessibility` | any |  | Ertl & Schuffenhauer 2009 synthetic accessibility, 1 (easy) to 10 (hard), with its fragment score, complexity penalty, symmetry correction, the counts they read and how many fragments the table did not know; null only if the fragment table could not be loaded |
| `np_likeness` | any |  | Ertl et al. 2008 natural-product likeness, about -5 (synthetic-like) to 5 (natural-product-like), and the confidence: the share of the molecule's fragments the model knows |
| `solubility` | any |  | ESOL (Delaney 2004) log S in mol/L under two coefficient sets, rdkitRefit (Walters' refit to RDKit descriptors) and delaney2004 (the paper's, with Crippen logP for Daylight CLOGP), and the four inputs: Crippen logP, average mass, rotatable bonds, aromatic proportion |
| `bioavailability_radar` | any |  | SwissADME's Bioavailability Radar (Daina 2017): six axes (lipo, size, polar, insolu, insatu, flex) with this molecule's value, the inclusive window, whether it is inside, and drugLike when all six are; read with Crippen logP for XLOGP3 and the XLOGP3 window's figure bound of 5.0 |
| `scaffold` | any |  | the Bemis–Murcko scaffold (ring systems and linkers, side chains removed) as canonical SMILES, empty for a molecule with no ring; the generic framework (every atom carbon, every bond single), null where an atom has more bonds than carbon allows; and the indices of the atoms the scaffold keeps, on the implicit-hydrogen molecule |
| `qed` | any |  | QED (Bickerton 2012) with mean weights, maximum weights and unweighted; the eight inputs (MW average mass, ALOGP Crippen, HBA, HBD, PSA, ROTB, AROM, ALERTS) and each input's desirability; and the SMARTS of every unwanted group QED counted |
| `atom_contributions` | any |  | per-atom weights on the implicit-hydrogen molecule: logp (Crippen, heavy atoms), tpsa (Ertl, N and O), tpsaSP (Ertl with S and P) and charge (Gasteiger–Marsili; not a number around an element RDKit has no parameters for) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "assess_small_molecule",
  "arguments": {
    "molecule": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### canonical_tautomer

**Canonical tautomer**: _Which tautomers does this molecule have, and which is canonical?_

A small molecule's tautomers and the canonical one, as RDKit's TautomerEnumerator finds and scores them: 37 hydrogen-shift transforms (after MolVS and Sitzmann 2010), scored by aromatic rings, twelve weighted groups and hydrogens on P, S, Se and Te, ties to the smaller SMILES. Returns every tautomer, the canonical SMILES, the score and the 0-based atoms (implicit hydrogens, molfile order) a hydrogen moved between.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's TautomerEnumerator transforms and scoring.

**Does not:**
- Capped at the tautomer and transform limits given.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecule` | string | **yes** |  |  | the structure: SMILES or a molfile. |
| `max_tautomers` | number |  | `1000` | ≥ 1 | stop the enumeration at this many tautomers. |
| `max_transforms` | number |  | `1000` | ≥ 1 | stop after this many transform applications. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the enumeration in words, with the cap when one was reached |
| `canonical` | string |  | RDKit's canonical tautomer, as canonical SMILES |
| `tautomers` | any |  | every tautomer enumerated, as canonical SMILES, sorted |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "canonical_tautomer",
  "arguments": {
    "molecule": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### cluster_molecules

**Cluster molecules**: _How do these molecules cluster, or which are most diverse, on Morgan fingerprints?_

Cluster or diversity-pick a list of small molecules on 1 − Tanimoto of Morgan radius-2 fingerprints: Butina sphere exclusion (RDKit ClusterData, optional reordering), MaxMin diversity picking (RDKit MaxMinPicker, seeded), or average linkage (UPGMA) cut into k clusters. Indices are 0-based.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- 1 − Tanimoto on Morgan radius-2 bits; the method and threshold given; the `seed` fixes a random pick.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `method` | `"butina"` · `"maxmin"` · `"average"` |  | `"butina"` |  | the clustering method. Values: butina (Butina (sphere exclusion)), maxmin (MaxMin diversity pick), average (Average linkage (UPGMA)). |
| `threshold` | number |  | `0.4` | 0–1 | Butina: neighbors within this distance (1 − Tanimoto), 0–1. |
| `reordering` | boolean |  | `false` |  | Butina: recount unassigned neighbors after each cluster. |
| `picks` | number |  | `10` | ≥ 1 | MaxMin: how many structures to pick. |
| `seed` | number |  | `0` | ≥ 0 | MaxMin: seed of the first pick, as RDKit's seed. |
| `clusters` | number |  | `5` | ≥ 1 | average linkage: how many clusters to cut the tree into. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the clustering in words, generated from this run |
| `groups` | any |  | Butina and average linkage: clusters of input indices (Butina: centroid first) |
| `picks` | any |  | MaxMin: input indices in pick order |
| `unread` | any |  | input indices RDKit could not read, left out |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "cluster_molecules",
  "arguments": {
    "molecules": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### compare_molecules

**Compare molecules**: _How similar are these two molecules under each fingerprint?_

How similar two small molecules are: Tanimoto under six RDKit fingerprints (Morgan/ECFP4, atom pair, topological torsion, RDKit path, pattern, MACCS), every DataStructs metric (Tanimoto, Dice, cosine, Sokal, Russell, Rogot-Goldberg, all-bit, Kulczynski, McConnaughey, asymmetric, Braun-Blanquet, on-bit, Tversky) on the chosen one, and count-based Tanimoto, Dice and Tversky on Morgan counts. The first molecule is the query.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's fingerprints and similarity metrics.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecule` | string | **yes** |  |  | the query structure: SMILES or a molfile. |
| `other` | string | **yes** |  |  | the structure to compare it with: SMILES or a molfile. |
| `fingerprint` | `"morgan"` · `"atomPair"` · `"torsion"` · `"path"` · `"pattern"` · `"maccs"` |  | `"morgan"` |  | the fingerprint every metric is read on. Values: morgan (Morgan (ECFP4)), atomPair (Atom pair), torsion (Topological torsion), path (RDKit path), pattern (Pattern), maccs (MACCS keys). |
| `tversky_a` | number |  | `0.9` | 0–1 | Tversky's weight on bits only the query has, 0–1. |
| `tversky_b` | number |  | `0.1` | 0–1 | Tversky's weight on bits only the other has, 0–1. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the comparison in words, generated from this run |
| `tanimoto_by_fingerprint` | any |  | per fingerprint: kind, length, bits set in each molecule, bits in common, Tanimoto |
| `metrics` | any |  | every metric on the chosen fingerprint, keyed Tanimoto, Dice, Cosine, Sokal, Russel, RogotGoldberg, AllBit, Kulczynski, McConnaughey, Asymmetric, BraunBlanquet, OnBit, Tversky |
| `count_similarity` | any |  | Tanimoto, Dice and Tversky on unfolded Morgan radius-2 counts |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "compare_molecules",
  "arguments": {
    "molecule": "<string>",
    "other": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### decompose_r_groups

**Decompose r groups**: _What R-groups does each molecule carry on this core?_

RDKit's R-group decomposition of a list of small molecules on a core given as SMARTS (default RGroupDecomposition parameters): per matched structure its core and substituents R1, R2 …, and the structures the core does not match. Indices are 0-based.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's RGroupDecomposition defaults.

**Does not:**
- Molecules that do not match the core are reported.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `core` | string | **yes** |  |  | the core, as SMARTS. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the decomposition in words, generated from this run |
| `rows` | any |  | per matched structure: its index and its groups (Core, R1, R2 …) as SMILES |
| `unmatched` | any |  | input indices the core does not match |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "decompose_r_groups",
  "arguments": {
    "molecules": [],
    "core": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### enumerate_protonation_states

**Enumerate protonation states**: _Which protonation states does this molecule take across this pH window?_

Enumerate a small molecule's protonation states across a pH window with Dimorphite-DL (Ropp et al. 2019): each ionisable group it recognizes (substructures with pKa means and spreads taken from measured pKa values) is kept protonated, deprotonated or both, and every combination is returned as SMILES. Reproduces Dimorphite-DL 2.1.0, including that it neutralizes charged groups first and keeps only the part it neutralized.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- Dimorphite-DL's (Ropp et al. 2019) site library and pKa ranges.

**Does not:**
- Groups outside the library are left as drawn.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecule` | string | **yes** |  |  | the structure: SMILES or a molfile. |
| `ph_min` | number |  | `6.4` | 0–14 | lower end of the pH window. |
| `ph_max` | number |  | `8.4` | 0–14 | upper end of the pH window. |
| `precision` | number |  | `1` | 0–10 | how many standard deviations of each group's pKa widen its window, 0–10. |
| `max_variants` | number |  | `128` | 1–10000 | stop enumerating past this many states (later groups are then not visited). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the enumeration in words, generated from this run, with its caveats |
| `states` | any |  | every protonation state as canonical SMILES, sorted |
| `sites` | any |  | per ionisable site: Dimorphite name, SMARTS, each pKa (mean, stdev, state) and its atoms on the input (0-based, implicit hydrogens), or null when they do not map |
| `capped` | boolean |  | true when the enumeration stopped at max_variants |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "enumerate_protonation_states",
  "arguments": {
    "molecule": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### enumerate_reaction

**Enumerate reaction**: _What products does this reaction SMARTS give over these reactants?_

Run a reaction SMARTS over lists of reactants, every combination, with RDKit's reaction engine: one list per reactant template, in template order. Pick one of 94 library reactions (the 58 robust organic reactions of Hartenfeller et al. 2011 and 36 click-chemistry reactions, as AutoGrow4 encodes them) or pass your own SMARTS. Each product is sanitised; a product set is kept only when every product in it sanitises. Indices are 0-based.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's reaction engine.

**Does not:**
- Capped at the combination limit given.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `template` | `"1_Epoxide_and_Alcohol"` · `"2_Epoxide_and_Thiol"` · `"3_Alkene_Oxidized_To_Epoxide"` · `"4_Sulfonyl_Azide_and_Thio_Acid"` · `"5_Alkyne_and_Azide"` · `"6_Alcohol_To_Azide"` · `"7_Alcohol_To_Cyanide"` · `"8_Primary_Amine_Oxidized_To_an_Azide"` · `"9_Primary_Amine_Oxidized_To_an_Isocyanate"` · `"10_Primary_Amine_Oxidized_To_an_Isothiocyanate"` · `"11_Azide_Reduced_To_Amine"` · `"12_Carbonochloridate_and_Amine"` · `"13_Carboxylate_and_Amine"` · `"14_Carboxylate_and_Alcohol"` · `"15_Carboxylate_and_Thiol"` · `"16_Carboxylate_To_Cyanide"` · `"17_Carboxylate_To_Azide"` · `"18_Halide_and_Amine"` · `"19_Halide_and_Alcohol"` · `"20_Halide_and_Thiol"` · `"21_Halide_To_Cyanide"` · `"22_Halide_To_Azide"` · `"23_Ester_and_Amine"` · `"24_Ester_and_Alcohol"` · `"25_Ester_and_Thiol"` · `"26_Acid_Anhydride_Noncyclic_and_Amine"` · `"27_Acid_Anhydride_Noncyclic_and_Alcohol"` · `"28_Acid_Anhydride_Noncyclic_and_Thiol"` · `"29_Acid_Anhydride_Noncyclic_To_Cyanide"` · `"30_Acid_Anhydride_Noncyclic_To_Azide"` · `"31_Isocyanate_and_Amine"` · `"32_Isothiocyanate_and_Amine"` · `"33_Isocyanate_and_Thiol"` · `"34_Isothiocyanate_and_Thiol"` · `"35_Isocyanate_and_Alcohol"` · `"36_Isothiocyanate_and_Alcohol"` · `"37_Pictet_Spengler"` · `"38_benzimidazole_derivatives_carboxylic_acid_ester"` · `"39_benzimidazole_derivatives_aldehyde"` · `"40_benzothiazole"` · `"41_benzoxazole_arom_aldehyde"` · `"42_benzoxazole_carboxylic_acid"` · `"43_thiazole"` · `"44_Niementowski_quinazoline"` · `"45_tetrazole_terminal"` · `"46_tetrazole_connect_regioisomere_1"` · `"47_tetrazole_connect_regioisomere_2"` · `"48_Huisgen_Cu_catalyzed_1_4_subst"` · `"49_Huisgen_Ru_catalyzed_1_5_subst"` · `"50_Huisgen_disubst_alkyne"` · `"51_1_2_4_triazole_acetohydrazide"` · `"52_1_2_4_triazole_carboxylic_acid_ester"` · `"53_3_nitrile_pyridine"` · `"54_spiro_chromanone"` · `"55_pyrazole"` · `"56_phthalazinone"` · `"57_Paal_Knorr_pyrrole"` · `"58_triaryl_imidazole"` · `"59_Fischer_indole"` · `"60_Friedlaender_chinoline"` · `"61_benzofuran"` · `"62_benzothiophene"` · `"63_indole"` · `"64_oxadiazole"` · `"65_Williamson_ether"` · `"66_reductive_amination"` · `"67_Suzuki"` · `"68_piperidine_indole"` · `"69_Negishi"` · `"70_Mitsunobu_imide"` · `"71_Mitsunobu_phenole"` · `"72_Mitsunobu_sulfonamide"` · `"73_Mitsunobu_tetrazole_1"` · `"74_Mitsunobu_tetrazole_2"` · `"75_Mitsunobu_tetrazole_3"` · `"76_Mitsunobu_tetrazole_4"` · `"77_Heck_terminal_vinyl"` · `"78_Heck_non_terminal_vinyl"` · `"79_Stille"` · `"80_Grignard_carbonyl"` · `"81_Grignard_alcohol"` · `"82_Sonogashira"` · `"83_Schotten_Baumann_amide"` · `"84_sulfon_amide"` · `"85_N_arylation_heterocycles"` · `"86_Wittig"` · `"87_Buchwald_Hartwig"` · `"88_imidazole"` · `"89_decarboxylative_coupling"` · `"90_heteroaromatic_nuc_sub"` · `"91_nucl_sub_aromatic_ortho_nitro"` · `"92_nucl_sub_aromatic_para_nitro"` · `"93_urea"` · `"94_thiourea"` · `"custom"` |  | `"83_Schotten_Baumann_amide"` |  | the library reaction to run, or custom for your own SMARTS. |
| `smarts` | string |  |  |  | your own reaction SMARTS, reactants>>products. Only applies when template is custom. |
| `reactants` | any[][] | **yes** |  |  | one list of SMILES or molfiles per reactant template, in template order. |
| `max_combinations` | number |  | `2500` | ≥ 1 | stop after this many reactant combinations. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the run in words: products, combinations, and what was dropped or capped |
| `products` | any |  | every product set as SMILES with the 0-based index of each reactant that made it |
| `capped` | boolean |  | true when the run stopped at max_combinations |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "enumerate_reaction",
  "arguments": {
    "reactants": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### generate_conformers

**Generate conformers**: _What 3D conformers does this molecule take, and how is each scored?_

3D conformers of a small molecule by OpenChemLib's torsion-library generator, each scored and optionally minimized under MMFF94, MMFF94s or MMFF94s+ (whose MMFF94 equals Halgren's OPTIMOL on all 761 validation-suite structures), lowest energy first, as molfiles with every hydrogen; for a 3D molfile also the energy of its own geometry. Energies in kcal/mol.

<sub>read-only · runs locally on the engine · randomised, reproducible with its seed · long-running</sub>

**Assumes:**
- OpenChemLib's torsion-library generator; the force field named; the `seed` fixes the draws.

**Does not:**
- A sample of conformers, not an exhaustive search.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecule` | string | **yes** |  |  | the structure: SMILES or a molfile. |
| `count` | number |  | `10` | 1–100 | at most this many conformers. |
| `seed` | number |  | `1` | ≥ 0 | random seed. |
| `strategy` | `"likelyRandom"` · `"adaptiveRandom"` · `"likelySystematic"` · `"pureRandom"` |  | `"likelyRandom"` |  | how torsion sets are chosen. |
| `max_torsion_sets` | number |  | `100000` | ≥ 1 | distinct torsion sets to try before stopping. |
| `sixty_degree_steps` | boolean |  | `false` |  | every rotatable bond in 60° steps instead of the torsion library's angles. |
| `force_field` | `"MMFF94"` · `"MMFF94s"` · `"MMFF94s+"` |  | `"MMFF94"` |  | the MMFF94 variant. |
| `minimise` | boolean |  | `true` |  | minimize each conformer. |
| `max_iterations` | number |  | `4000` | ≥ 1 | minimiser iterations, at most. |
| `gradient_tolerance` | number |  | `0.0001` | ≥ 0 | minimiser gradient tolerance. |
| `energy_tolerance` | number |  | `1e-06` | ≥ 0 | minimiser energy tolerance. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the ensemble in words, generated from this run |
| `conformers` | any |  | each conformer: molfile, energy as generated and minimized (kcal/mol) |
| `file_energy` | any |  | a 3D molfile's own MMFF94 energy, or why it could not be computed |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "generate_conformers",
  "arguments": {
    "molecule": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### lookup_compound

**Lookup compound**: _What does the authority named return for this compound or drug?_

Look up a chemical compound or drug: ChEMBL molecules, mechanisms of action and bioactivity, PubChem properties, ChEBI ontology, Rhea reactions, or purchasable ZINC compounds.

<sub>read-only · calls a public database or service · open-world (reaches outside services) · long-running</sub>

**Does not:**
- Needs the network.

**No scientific claim:** Relays the remote service's own result unchanged; it computes no number of its own, so the service is the authority for what comes back.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `source` | `"chembl"` · `"pubchem"` · `"chebi"` · `"rhea"` · `"zinc"` · `"bindingdb"` | **yes** |  |  | which authority to ask. |
| `query` | string | **yes** |  |  | a compound name, SMILES or identifier, or a command such as "mechanism:CHEMBL941" or "admet:CHEMBL941". |
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
  "name": "lookup_compound",
  "arguments": {
    "source": "chembl",
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

### map_chemical_space

**Map chemical space**: _Where does each molecule sit on the principal components of the property table or fingerprint bits?_

Principal components of a list of small molecules, computed as R's prcomp computes them, on the scaled property table or on Morgan radius-2 bits: each structure's scores on PC1 and PC2, every component's standard deviation and variance share, the property loadings, and constant properties left out. Indices are 0-based.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- R's prcomp on the scaled table.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `space` | `"descriptors"` · `"morgan"` |  | `"descriptors"` |  | what the components are taken over. Values: descriptors (Properties (scaled)), morgan (Morgan bits (ECFP4)). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the map in words, generated from this run |
| `points` | any |  | per mapped structure: its index and its PC1 and PC2 scores |
| `explained` | any |  | the share of the total variance each component carries |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "map_chemical_space",
  "arguments": {
    "molecules": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### map_reaction_atoms

**Map reaction atoms**: _Which reactant atom does each product atom come from?_

Predict which reactant atom each product atom came from (atom-to-atom mapping) with RXNMapper (Schwaller et al., Sci. Adv. 2021), the most accurate mapper in Lin et al.'s 2022 benchmark of 1,851 curated reactions. Agents join the reactants, each compound is canonicalised and each side sorted before mapping, as RXNMapper does. Returns the reaction SMILES with atom maps and a confidence (the product of each product atom's attention score). A prediction, not a measurement.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RXNMapper (Schwaller et al. 2021).

**Does not:**
- A prediction; balanced reactions map best.

**Not read from this result:** The answer is the atom-mapped reaction and the model's confidence, which the outputs carry; the Chemistry panel colors atoms by it and writes no reading over it.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `reaction` | string | **yes** |  |  | reaction SMILES, reactants>agents>products; existing atom maps are ignored. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `mapped` | string |  | the canonicalised reaction SMILES with atom maps |
| `confidence` | number |  | the product of the per-atom confidences, 0 to 1 |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "map_reaction_atoms",
  "arguments": {
    "reaction": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### matched_molecular_pairs

**Matched molecular pairs**: _Which pairs of these molecules differ by one small change?_

Matched molecular pairs (Hussain & Rea 2010) in a list of small molecules, as mmpdb finds them: pairs that differ by one change no larger than a heavy-atom limit, grouped by the change as a reaction SMIRKS, most pairs first. Indices are 0-based.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- mmpdb's fragmentation, up to the size given.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `max_size` | number |  | `10` | 1–50 | largest changed part, in heavy atoms. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the pairs in words, generated from this run |
| `transformations` | any |  | each change as SMIRKS with its pairs (left, right, shared context) |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "matched_molecular_pairs",
  "arguments": {
    "molecules": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### scaffold_network

**Scaffold network**: _What is the scaffold network of these molecules?_

The scaffold network (Kruger et al. 2020) of a list of small molecules, as RDKit's CreateScaffoldNetwork builds it, under RDKit's default ring-side cuts or the 46 BRICS bond types (Degen 2008). Every node with the structures that contain it and how many times the network made it, and every edge with RDKit's type. Structures over the cut limit are named and left out. Indices are 0-based.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's CreateScaffoldNetwork with its default ring-side cuts.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `rules` | `"rings"` · `"brics"` |  | `"rings"` |  | which bonds are cut. Values: rings (Ring side of each cut), brics (BRICS, both sides). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | the network in words, generated from this run |
| `nodes` | any |  | every node: SMILES, the input indices containing it, times made |
| `edges` | any |  | every edge: from and to node indices and its RDKit type |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "scaffold_network",
  "arguments": {
    "molecules": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### search_molecule_library

**Search molecule library**: _Which of these molecules contain this SMARTS substructure?_

Which of a list of small molecules contain a SMARTS substructure, with RDKit's substructure library (pattern-fingerprint screen, then atom matching). Returns the 0-based indices of the hits and of any structure RDKit could not read.

<sub>read-only · runs locally on the engine · long-running</sub>

**Assumes:**
- RDKit's substructure matching.

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the library: one SMILES or molfile per entry. |
| `smarts` | string | **yes** |  |  | the substructure, as SMARTS (a plain SMILES reads as one). |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many structures contain the pattern, of how many searched |
| `hits` | any |  | 0-based indices of the molecules that contain the pattern, ascending |
| `unread` | any |  | 0-based indices of the entries RDKit could not read, never searched |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "search_molecule_library",
  "arguments": {
    "molecules": [],
    "smarts": "<string>",
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---

### write_structure_library

**Write structure library**: _Write these molecules as one structure file._

Write a list of small molecules as one file: SDF (V2000 or V3000), each record named and, optionally, carrying its canonical SMILES and RDKit descriptors as data fields; or SMILES or CXSMILES, one record a line followed by its name. Written as RDKit's SDWriter, MolToSmiles and MolToCXSmiles write it; a structure RDKit cannot read is left out and its index returned.

<sub>read-only · runs locally on the engine · long-running</sub>

**Validated:** against the reference implementation by 1 golden suite.

**Arguments**

| Argument | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `molecules` | string[] | **yes** |  |  | the structures: one SMILES or molfile per entry. |
| `names` | string[] |  |  |  | a name per structure, in the same order (the SDF title line, the SMILES second column). |
| `format` | `"sdf"` · `"sdf-v3000"` · `"smiles"` · `"cxsmiles"` |  | `"sdf"` |  | the file format. Values: sdf (SDF), sdf-v3000 (SDF V3000), smiles (SMILES), cxsmiles (CXSMILES). |
| `with_properties` | boolean |  | `true` |  | SDF only: add canonical_smiles and the RDKit descriptors to each record as data fields. |

Plus [`_subject` and `_files`](../protocol.md#naming-the-molecule-_subject), shared by every tool that acts on a record.

<details><summary><b>Output</b> (<code>structuredContent</code>)</summary>

| Field | Type | Unit | Description |
|---|---|---|---|
| `summary` | string |  | how many structures were written, of how many given, and which were left out |
| `text` | string |  | the file |
| `unread` | any |  | 0-based indices of the entries RDKit could not read, left out of the file |

</details>

<details><summary><b>Minimal call</b></summary>

```json
{
  "name": "write_structure_library",
  "arguments": {
    "molecules": [],
    "_subject": {
      "sequence": "<bases, or use accession / sample / file>"
    }
  }
}
```

</details>

[↑ top](#contents)

---
