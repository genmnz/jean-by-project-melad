# Tool reference

Every tool on `https://jeanpm.vercel.app/mcp`: **358** in all. Generated from the live server by `scripts/catalogue.py`; do not edit by hand. Read [the protocol guide](../protocol.md) first: it explains the arguments every tool shares.

## Sections

| Section | Tools | Covers |
|---|---|---|
| [🧬 Cloning & assembly](cloning.md) | 37 | Digests, ligations, Gibson, Golden Gate, Gateway-style recombination, part grammars and assembly planning. |
| [🔥 PCR, primers & thermocycling](amplify.md) | 15 | Primer design for every kind of PCR, melting temperatures and reaction simulation. |
| [✂️ CRISPR & genome editing](crispr.md) | 20 | Guide design and scoring, off-targets, screens, and editing outcomes measured from traces. |
| [📈 Sanger, sequencing & verification](sequencing.md) | 18 | Trace reading, base calling, construct verification, read QC and alignment to a reference. |
| [🧪 qPCR & digital PCR](qpcr.md) | 13 | Amplification and melt curves, RDML runs, droplet gating, uncertainty and relative quantification. |
| [🎛️ Design & expression](design.md) | 42 | Codon optimisation, RBS and operons, probes, barcodes, genetic circuits and annotation. |
| [🌳 Alignment & phylogenetics](phylo.md) | 20 | Pairwise and multiple alignment, dot plots, model selection, trees and tree comparison. |
| [🧫 Genomics, variants & copy number](variants.md) | 23 | Variant calls, copy-number segmentation, LOH and mosaicism, genome regions. |
| [🧩 Proteins, domains & proteomics](protein.md) | 26 | Domains and motifs, residue sites, protein properties and peptide evidence. |
| [⚗️ Cheminformatics](chem.md) | 16 | Molecules, conformers, scaffolds, reactions, chemical space and library screening. |
| [🔬 Expression & hypothesis testing](discovery.md) | 14 | Differential expression, gene-set enrichment and falsification-tested discovery programmes. |
| [🗄️ Public databases & records](data.md) | 21 | Search and fetch from NCBI, EMBL-EBI, UCSC, UniProt and more, then hand the record to any tool. |
| [📊 Sequence analysis](analyze.md) | 67 | Everything else a bench scientist asks of a sequence. |
| [🔗 Pipelines & lab records](pipelines.md) | 14 | Chain tools into reproducible workflows, export records, keep lab notes. |
| [🖥️ Workbench state](workspace.md) | 12 | Tools that read or write the open project inside the Jean workbench. Over this stateless endpoint there is no open project, so they matter only to the in-app assistant. |

## A–Z

| Tool | Title | Section |
|---|---|---|
| [`activity_cliffs`](chem.md#activity_cliffs) | Activity cliffs | ⚗️ Cheminformatics |
| [`add_notebook_figure`](workspace.md#add_notebook_figure) | Add notebook figure | 🖥️ Workbench state |
| [`adopt_trace_calls`](sequencing.md#adopt_trace_calls) | Adopt trace calls | 📈 Sanger, sequencing & verification |
| [`align_pair`](phylo.md#align_pair) | Align pair | 🌳 Alignment & phylogenetics |
| [`align_read`](phylo.md#align_read) | Align read | 🌳 Alignment & phylogenetics |
| [`align_sequences`](phylo.md#align_sequences) | Align sequences | 🌳 Alignment & phylogenetics |
| [`alignment_agreement`](phylo.md#alignment_agreement) | Alignment agreement | 🌳 Alignment & phylogenetics |
| [`alignment_pca`](phylo.md#alignment_pca) | Alignment PCA | 🌳 Alignment & phylogenetics |
| [`alignment_redundancy`](phylo.md#alignment_redundancy) | Alignment redundancy | 🌳 Alignment & phylogenetics |
| [`alignment_window`](phylo.md#alignment_window) | Alignment window | 🌳 Alignment & phylogenetics |
| [`analyze_flow_cytometry`](analyze.md#analyze_flow_cytometry) | Analyze flow cytometry | 📊 Sequence analysis |
| [`analyze_flow_cytometry_ploidy`](analyze.md#analyze_flow_cytometry_ploidy) | Analyze flow cytometry ploidy | 📊 Sequence analysis |
| [`analyze_melt_curves`](qpcr.md#analyze_melt_curves) | Analyze melt curves | 🧪 qPCR & digital PCR |
| [`analyze_rt_pcr`](analyze.md#analyze_rt_pcr) | Analyze rt PCR | 📊 Sequence analysis |
| [`annotate_region`](design.md#annotate_region) | Annotate region | 🎛️ Design & expression |
| [`antibody_antigen_contacts`](protein.md#antibody_antigen_contacts) | Antibody antigen contacts | 🧩 Proteins, domains & proteomics |
| [`antibody_canonical_classes`](protein.md#antibody_canonical_classes) | Antibody canonical classes | 🧩 Proteins, domains & proteomics |
| [`antibody_isotype`](protein.md#antibody_isotype) | Antibody isotype | 🧩 Proteins, domains & proteomics |
| [`antibody_liabilities`](protein.md#antibody_liabilities) | Antibody liabilities | 🧩 Proteins, domains & proteomics |
| [`antibody_molecule`](protein.md#antibody_molecule) | Antibody molecule | 🧩 Proteins, domains & proteomics |
| [`antibody_position_frequencies`](protein.md#antibody_position_frequencies) | Antibody position frequencies | 🧩 Proteins, domains & proteomics |
| [`apply_feature_file`](data.md#apply_feature_file) | Apply feature file | 🗄️ Public databases & records |
| [`apply_variant_call`](variants.md#apply_variant_call) | Apply variant call | 🧫 Genomics, variants & copy number |
| [`assemble_index_oligos`](cloning.md#assemble_index_oligos) | Assemble index oligos | 🧬 Cloning & assembly |
| [`assemble_multiple_inserts`](cloning.md#assemble_multiple_inserts) | Assemble multiple inserts | 🧬 Cloning & assembly |
| [`assemble_operon`](cloning.md#assemble_operon) | Assemble operon | 🧬 Cloning & assembly |
| [`assembly_plan_simulate`](cloning.md#assembly_plan_simulate) | Assembly plan simulate | 🧬 Cloning & assembly |
| [`assess_small_molecule`](chem.md#assess_small_molecule) | Assess small molecule | ⚗️ Cheminformatics |
| [`audit_barcodes`](design.md#audit_barcodes) | Audit barcodes | 🎛️ Design & expression |
| [`audit_cds_annotations`](design.md#audit_cds_annotations) | Audit CDS annotations | 🎛️ Design & expression |
| [`auto_annotate`](design.md#auto_annotate) | Auto annotate | 🎛️ Design & expression |
| [`auto_gate_flow_cytometry`](analyze.md#auto_gate_flow_cytometry) | Auto Gate flow cytometry | 📊 Sequence analysis |
| [`back_translate`](design.md#back_translate) | Back translate | 🎛️ Design & expression |
| [`batch_flow_cytometry`](analyze.md#batch_flow_cytometry) | Batch flow cytometry | 📊 Sequence analysis |
| [`bayesian_protein_inference`](protein.md#bayesian_protein_inference) | Bayesian protein inference | 🧩 Proteins, domains & proteomics |
| [`blast_project_sequences`](analyze.md#blast_project_sequences) | BLAST project sequences | 📊 Sequence analysis |
| [`blast_search`](analyze.md#blast_search) | BLAST search | 📊 Sequence analysis |
| [`bootstrap_cq`](qpcr.md#bootstrap_cq) | Bootstrap Cq | 🧪 qPCR & digital PCR |
| [`browse_region`](variants.md#browse_region) | Browse region | 🧫 Genomics, variants & copy number |
| [`build_addgene_deposit`](pipelines.md#build_addgene_deposit) | Build addgene deposit | 🔗 Pipelines & lab records |
| [`build_assembly_report`](cloning.md#build_assembly_report) | Build assembly report | 🧬 Cloning & assembly |
| [`build_codon_table_from_cds`](design.md#build_codon_table_from_cds) | Build codon table from CDS | 🎛️ Design & expression |
| [`build_ena_submission`](design.md#build_ena_submission) | Build ENA submission | 🎛️ Design & expression |
| [`build_genbank_submission`](design.md#build_genbank_submission) | Build GenBank submission | 🎛️ Design & expression |
| [`build_tree`](phylo.md#build_tree) | Build tree | 🌳 Alignment & phylogenetics |
| [`calculate_power`](design.md#calculate_power) | Calculate power | 🎛️ Design & expression |
| [`calculate_rnaseq_power`](design.md#calculate_rnaseq_power) | Calculate rnaseq power | 🎛️ Design & expression |
| [`calibrate_flow_cytometry_beads`](analyze.md#calibrate_flow_cytometry_beads) | Calibrate flow cytometry beads | 📊 Sequence analysis |
| [`call_bases_from_trace`](sequencing.md#call_bases_from_trace) | Call bases from trace | 📈 Sanger, sequencing & verification |
| [`call_cq`](qpcr.md#call_cq) | Call Cq | 🧪 qPCR & digital PCR |
| [`call_mixed_bases_from_trace`](sequencing.md#call_mixed_bases_from_trace) | Call mixed bases from trace | 📈 Sanger, sequencing & verification |
| [`cancel_research_run`](data.md#cancel_research_run) | Cancel research run | 🗄️ Public databases & records |
| [`canonical_tautomer`](chem.md#canonical_tautomer) | Canonical tautomer | ⚗️ Cheminformatics |
| [`check_assay_decay`](analyze.md#check_assay_decay) | Check assay decay | 📊 Sequence analysis |
| [`check_color_balance`](design.md#check_color_balance) | Check color balance | 🎛️ Design & expression |
| [`check_flow_cytometry_quality`](analyze.md#check_flow_cytometry_quality) | Check flow cytometry quality | 📊 Sequence analysis |
| [`check_golden_gate_parts`](cloning.md#check_golden_gate_parts) | Check Golden Gate parts | 🧬 Cloning & assembly |
| [`check_index_pool`](design.md#check_index_pool) | Check index pool | 🎛️ Design & expression |
| [`check_invariants`](variants.md#check_invariants) | Check invariants | 🧫 Genomics, variants & copy number |
| [`check_manufacturability`](design.md#check_manufacturability) | Check manufacturability | 🎛️ Design & expression |
| [`check_methylation_block`](cloning.md#check_methylation_block) | Check methylation block | 🧬 Cloning & assembly |
| [`check_primer_specificity`](analyze.md#check_primer_specificity) | Check primer specificity | 📊 Sequence analysis |
| [`check_qpcr_multiplex`](qpcr.md#check_qpcr_multiplex) | Check qPCR multiplex | 🧪 qPCR & digital PCR |
| [`check_rows`](analyze.md#check_rows) | Check rows | 📊 Sequence analysis |
| [`check_scorpion_stem`](design.md#check_scorpion_stem) | Check scorpion stem | 🎛️ Design & expression |
| [`check_value`](workspace.md#check_value) | Check value | 🖥️ Workbench state |
| [`classify_droplets`](qpcr.md#classify_droplets) | Classify droplets | 🧪 qPCR & digital PCR |
| [`classify_flow_cytometry_events`](analyze.md#classify_flow_cytometry_events) | Classify flow cytometry events | 📊 Sequence analysis |
| [`classify_grammar_part`](cloning.md#classify_grammar_part) | Classify grammar part | 🧬 Cloning & assembly |
| [`cluster_flow_cytometry_events`](analyze.md#cluster_flow_cytometry_events) | Cluster flow cytometry events | 📊 Sequence analysis |
| [`cluster_flow_cytometry_flowsom`](analyze.md#cluster_flow_cytometry_flowsom) | Cluster flow cytometry FlowSOM | 📊 Sequence analysis |
| [`cluster_molecules`](chem.md#cluster_molecules) | Cluster molecules | ⚗️ Cheminformatics |
| [`codon_optimality`](design.md#codon_optimality) | Codon optimality | 🎛️ Design & expression |
| [`codon_table_fetch`](design.md#codon_table_fetch) | Codon table fetch | 🎛️ Design & expression |
| [`codon_usage_analysis`](design.md#codon_usage_analysis) | Codon usage analysis | 🎛️ Design & expression |
| [`codon_usage_distance`](design.md#codon_usage_distance) | Codon usage distance | 🎛️ Design & expression |
| [`compare_antibodies`](analyze.md#compare_antibodies) | Compare antibodies | 📊 Sequence analysis |
| [`compare_constructions`](pipelines.md#compare_constructions) | Compare constructions | 🔗 Pipelines & lab records |
| [`compare_flow_cytometry_populations`](variants.md#compare_flow_cytometry_populations) | Compare flow cytometry populations | 🧫 Genomics, variants & copy number |
| [`compare_molecules`](chem.md#compare_molecules) | Compare molecules | ⚗️ Cheminformatics |
| [`compare_reads_to_reference`](sequencing.md#compare_reads_to_reference) | Compare reads to reference | 📈 Sanger, sequencing & verification |
| [`compare_trees`](phylo.md#compare_trees) | Compare trees | 🌳 Alignment & phylogenetics |
| [`confirm_literature_hit`](data.md#confirm_literature_hit) | Confirm literature hit | 🗄️ Public databases & records |
| [`consensus_from_traces`](sequencing.md#consensus_from_traces) | Consensus from traces | 📈 Sanger, sequencing & verification |
| [`convert_mass_moles`](amplify.md#convert_mass_moles) | Convert mass moles | 🔥 PCR, primers & thermocycling |
| [`copy_number_allele_split`](variants.md#copy_number_allele_split) | Copy number allele split | 🧫 Genomics, variants & copy number |
| [`copy_number_compare`](variants.md#copy_number_compare) | Copy number compare | 🧫 Genomics, variants & copy number |
| [`copy_number_findings`](variants.md#copy_number_findings) | Copy number findings | 🧫 Genomics, variants & copy number |
| [`copy_number_loh`](variants.md#copy_number_loh) | Copy number loh | 🧫 Genomics, variants & copy number |
| [`copy_number_mosaicism`](variants.md#copy_number_mosaicism) | Copy number mosaicism | 🧫 Genomics, variants & copy number |
| [`copy_number_read`](variants.md#copy_number_read) | Copy number read | 🧫 Genomics, variants & copy number |
| [`copy_number_regions`](variants.md#copy_number_regions) | Copy number regions | 🧫 Genomics, variants & copy number |
| [`copy_number_segment`](variants.md#copy_number_segment) | Copy number segment | 🧫 Genomics, variants & copy number |
| [`copy_number_somatic`](variants.md#copy_number_somatic) | Copy number somatic | 🧫 Genomics, variants & copy number |
| [`correct_flow_cytometry_batches_cycombine`](analyze.md#correct_flow_cytometry_batches_cycombine) | Correct flow cytometry batches cyCombine | 📊 Sequence analysis |
| [`crispr_analyze_screen`](crispr.md#crispr_analyze_screen) | CRISPR analyze screen | ✂️ CRISPR & genome editing |
| [`crispr_design_guides`](crispr.md#crispr_design_guides) | CRISPR design guides | ✂️ CRISPR & genome editing |
| [`crispr_design_library`](crispr.md#crispr_design_library) | CRISPR design library | ✂️ CRISPR & genome editing |
| [`crispr_quantify_edits`](crispr.md#crispr_quantify_edits) | CRISPR quantify edits | ✂️ CRISPR & genome editing |
| [`crispr_score_deephf`](crispr.md#crispr_score_deephf) | CRISPR score DeepHF | ✂️ CRISPR & genome editing |
| [`crispr_score_deepspcas9`](crispr.md#crispr_score_deepspcas9) | CRISPR score DeepSpCas9 | ✂️ CRISPR & genome editing |
| [`debarcode_mass_cytometry`](design.md#debarcode_mass_cytometry) | Debarcode mass cytometry | 🎛️ Design & expression |
| [`decompose_r_groups`](chem.md#decompose_r_groups) | Decompose r groups | ⚗️ Cheminformatics |
| [`delta_blast_smart`](protein.md#delta_blast_smart) | DELTA BLAST SMART | 🧩 Proteins, domains & proteomics |
| [`demultiplex_reads`](sequencing.md#demultiplex_reads) | Demultiplex reads | 📈 Sanger, sequencing & verification |
| [`describe_discovery_corpus`](discovery.md#describe_discovery_corpus) | Describe discovery corpus | 🔬 Expression & hypothesis testing |
| [`describe_project`](workspace.md#describe_project) | Describe project | 🖥️ Workbench state |
| [`design_barcodes`](design.md#design_barcodes) | Design barcodes | 🎛️ Design & expression |
| [`design_bisulfite_primers`](amplify.md#design_bisulfite_primers) | Design bisulfite primers | 🔥 PCR, primers & thermocycling |
| [`design_codehop`](amplify.md#design_codehop) | Design CODEHOP | 🔥 PCR, primers & thermocycling |
| [`design_codon_tiling_primers`](design.md#design_codon_tiling_primers) | Design codon tiling primers | 🎛️ Design & expression |
| [`design_combinatorial_library`](cloning.md#design_combinatorial_library) | Design combinatorial library | 🧬 Cloning & assembly |
| [`design_degenerate_primers`](amplify.md#design_degenerate_primers) | Design degenerate primers | 🔥 PCR, primers & thermocycling |
| [`design_expression_variants`](variants.md#design_expression_variants) | Design expression variants | 🧫 Genomics, variants & copy number |
| [`design_free_codes`](design.md#design_free_codes) | Design FREE codes | 🎛️ Design & expression |
| [`design_fusion_site_primers`](cloning.md#design_fusion_site_primers) | Design fusion site primers | 🧬 Cloning & assembly |
| [`design_gene_fragment_order`](design.md#design_gene_fragment_order) | Design gene fragment order | 🎛️ Design & expression |
| [`design_genetic_circuit`](design.md#design_genetic_circuit) | Design genetic circuit | 🎛️ Design & expression |
| [`design_gibson_primers`](cloning.md#design_gibson_primers) | Design Gibson primers | 🧬 Cloning & assembly |
| [`design_hcr_probes`](design.md#design_hcr_probes) | Design HCR probes | 🎛️ Design & expression |
| [`design_indel_primers`](crispr.md#design_indel_primers) | Design indel primers | ✂️ CRISPR & genome editing |
| [`design_ish_probes`](design.md#design_ish_probes) | Design ish probes | 🎛️ Design & expression |
| [`design_knockout_package`](design.md#design_knockout_package) | Design knockout package | 🎛️ Design & expression |
| [`design_lamp_primers`](amplify.md#design_lamp_primers) | Design LAMP primers | 🔥 PCR, primers & thermocycling |
| [`design_ligation_independent_primers`](cloning.md#design_ligation_independent_primers) | Design ligation independent primers | 🧬 Cloning & assembly |
| [`design_merfish_probes`](design.md#design_merfish_probes) | Design MERFISH probes | 🎛️ Design & expression |
| [`design_multisite_primers`](cloning.md#design_multisite_primers) | Design multisite primers | 🧬 Cloning & assembly |
| [`design_mutagenesis_primers`](cloning.md#design_mutagenesis_primers) | Design mutagenesis primers | 🧬 Cloning & assembly |
| [`design_oligo_plate_order`](design.md#design_oligo_plate_order) | Design oligo plate order | 🎛️ Design & expression |
| [`design_overhang_set`](cloning.md#design_overhang_set) | Design overhang set | 🧬 Cloning & assembly |
| [`design_padlock_probes`](design.md#design_padlock_probes) | Design padlock probes | 🎛️ Design & expression |
| [`design_primer_pairs`](amplify.md#design_primer_pairs) | Design primer pairs | 🔥 PCR, primers & thermocycling |
| [`design_primers`](amplify.md#design_primers) | Design primers | 🔥 PCR, primers & thermocycling |
| [`design_qpcr_assay`](qpcr.md#design_qpcr_assay) | Design qPCR assay | 🧪 qPCR & digital PCR |
| [`design_rbs`](design.md#design_rbs) | Design RBS | 🎛️ Design & expression |
| [`design_saturation_primers`](cloning.md#design_saturation_primers) | Design saturation primers | 🧬 Cloning & assembly |
| [`design_sequencing_primers`](amplify.md#design_sequencing_primers) | Design sequencing primers | 🔥 PCR, primers & thermocycling |
| [`design_split_sites`](cloning.md#design_split_sites) | Design split sites | 🧬 Cloning & assembly |
| [`design_xenium_probes`](design.md#design_xenium_probes) | Design xenium probes | 🎛️ Design & expression |
| [`detect_trace_indel`](crispr.md#detect_trace_indel) | Detect trace indel | ✂️ CRISPR & genome editing |
| [`differential_abundance_flow_cytometry`](discovery.md#differential_abundance_flow_cytometry) | Differential abundance flow cytometry | 🔬 Expression & hypothesis testing |
| [`differential_expression`](discovery.md#differential_expression) | Differential expression | 🔬 Expression & hypothesis testing |
| [`digest_fragments`](cloning.md#digest_fragments) | Digest fragments | 🧬 Cloning & assembly |
| [`digest_reaction_conditions`](cloning.md#digest_reaction_conditions) | Digest reaction conditions | 🧬 Cloning & assembly |
| [`discover_annotation_contradictions`](design.md#discover_annotation_contradictions) | Discover annotation contradictions | 🎛️ Design & expression |
| [`discover_codon_outliers`](design.md#discover_codon_outliers) | Discover codon outliers | 🎛️ Design & expression |
| [`discover_flag_rates`](discovery.md#discover_flag_rates) | Discover flag rates | 🔬 Expression & hypothesis testing |
| [`discover_gene_tree_discordance`](phylo.md#discover_gene_tree_discordance) | Discover gene tree discordance | 🌳 Alignment & phylogenetics |
| [`discover_reference_concordance`](discovery.md#discover_reference_concordance) | Discover reference concordance | 🔬 Expression & hypothesis testing |
| [`discover_reference_stability`](discovery.md#discover_reference_stability) | Discover reference stability | 🔬 Expression & hypothesis testing |
| [`discover_site_avoidance`](discovery.md#discover_site_avoidance) | Discover site avoidance | 🔬 Expression & hypothesis testing |
| [`discover_target_validation`](discovery.md#discover_target_validation) | Discover target validation | 🔬 Expression & hypothesis testing |
| [`discover_tree_incongruence`](phylo.md#discover_tree_incongruence) | Discover tree incongruence | 🌳 Alignment & phylogenetics |
| [`domesticate_part`](cloning.md#domesticate_part) | Domesticate part | 🧬 Cloning & assembly |
| [`dot_plot`](phylo.md#dot_plot) | Dot plot | 🌳 Alignment & phylogenetics |
| [`dot_plot_grid`](phylo.md#dot_plot_grid) | Dot plot grid | 🌳 Alignment & phylogenetics |
| [`draw_alignment`](phylo.md#draw_alignment) | Draw alignment | 🌳 Alignment & phylogenetics |
| [`draw_gel`](cloning.md#draw_gel) | Draw gel | 🧬 Cloning & assembly |
| [`draw_trace`](sequencing.md#draw_trace) | Draw trace | 📈 Sanger, sequencing & verification |
| [`draw_tree`](phylo.md#draw_tree) | Draw tree | 🌳 Alignment & phylogenetics |
| [`ebi_align`](phylo.md#ebi_align) | EBI align | 🌳 Alignment & phylogenetics |
| [`enumerate_protonation_states`](chem.md#enumerate_protonation_states) | Enumerate protonation states | ⚗️ Cheminformatics |
| [`enumerate_reaction`](chem.md#enumerate_reaction) | Enumerate reaction | ⚗️ Cheminformatics |
| [`enzyme_collection`](pipelines.md#enzyme_collection) | Enzyme collection | 🔗 Pipelines & lab records |
| [`enzyme_cut_counts`](analyze.md#enzyme_cut_counts) | Enzyme cut counts | 📊 Sequence analysis |
| [`estimate_cytof_spillover`](analyze.md#estimate_cytof_spillover) | Estimate cytof spillover | 📊 Sequence analysis |
| [`estimate_effect_size`](design.md#estimate_effect_size) | Estimate effect size | 🎛️ Design & expression |
| [`estimate_flow_cytometry_scale`](analyze.md#estimate_flow_cytometry_scale) | Estimate flow cytometry scale | 📊 Sequence analysis |
| [`estimate_spectra_from_controls`](analyze.md#estimate_spectra_from_controls) | Estimate spectra from controls | 📊 Sequence analysis |
| [`estimate_spillover_from_controls`](analyze.md#estimate_spillover_from_controls) | Estimate spillover from controls | 📊 Sequence analysis |
| [`export_barcodes`](design.md#export_barcodes) | Export barcodes | 🎛️ Design & expression |
| [`export_construction_record`](pipelines.md#export_construction_record) | Export construction record | 🔗 Pipelines & lab records |
| [`export_flow_cytometry_population`](variants.md#export_flow_cytometry_population) | Export flow cytometry population | 🧫 Genomics, variants & copy number |
| [`export_map_svg`](pipelines.md#export_map_svg) | Export map SVG | 🔗 Pipelines & lab records |
| [`export_trace`](pipelines.md#export_trace) | Export trace | 🔗 Pipelines & lab records |
| [`export_tree`](phylo.md#export_tree) | Export tree | 🌳 Alignment & phylogenetics |
| [`fastq_qc`](sequencing.md#fastq_qc) | FASTQ QC | 📈 Sanger, sequencing & verification |
| [`fetch_article`](data.md#fetch_article) | Fetch article | 🗄️ Public databases & records |
| [`fetch_clinvar_vcf`](data.md#fetch_clinvar_vcf) | Fetch ClinVar VCF | 🗄️ Public databases & records |
| [`fetch_record`](data.md#fetch_record) | Fetch record | 🗄️ Public databases & records |
| [`filter_items`](analyze.md#filter_items) | Filter items | 📊 Sequence analysis |
| [`find_accessions`](data.md#find_accessions) | Find accessions | 🗄️ Public databases & records |
| [`find_assemblies`](cloning.md#find_assemblies) | Find assemblies | 🧬 Cloning & assembly |
| [`find_common_substructure`](analyze.md#find_common_substructure) | Find common substructure | 📊 Sequence analysis |
| [`find_linear_motifs`](protein.md#find_linear_motifs) | Find linear motifs | 🧩 Proteins, domains & proteomics |
| [`find_orfs`](analyze.md#find_orfs) | Find ORFs | 📊 Sequence analysis |
| [`find_primer_snps`](analyze.md#find_primer_snps) | Find primer SNPs | 📊 Sequence analysis |
| [`find_restriction_sites`](cloning.md#find_restriction_sites) | Find restriction sites | 🧬 Cloning & assembly |
| [`find_star_sites`](cloning.md#find_star_sites) | Find star sites | 🧬 Cloning & assembly |
| [`fit_flow_cytometry_cell_cycle`](analyze.md#fit_flow_cytometry_cell_cycle) | Fit flow cytometry cell cycle | 📊 Sequence analysis |
| [`fit_flow_cytometry_compass`](analyze.md#fit_flow_cytometry_compass) | Fit flow cytometry COMPASS | 📊 Sequence analysis |
| [`fit_flow_cytometry_proliferation`](analyze.md#fit_flow_cytometry_proliferation) | Fit flow cytometry proliferation | 📊 Sequence analysis |
| [`fit_flow_cytometry_trajectory`](analyze.md#fit_flow_cytometry_trajectory) | Fit flow cytometry trajectory | 📊 Sequence analysis |
| [`flow_cytometry_kinetics`](analyze.md#flow_cytometry_kinetics) | Flow cytometry kinetics | 📊 Sequence analysis |
| [`fold_guide`](crispr.md#fold_guide) | Fold guide | ✂️ CRISPR & genome editing |
| [`fold_rna`](analyze.md#fold_rna) | Fold RNA | 📊 Sequence analysis |
| [`fragment_ions`](analyze.md#fragment_ions) | Fragment ions | 📊 Sequence analysis |
| [`fusion_pcr`](amplify.md#fusion_pcr) | Fusion PCR | 🔥 PCR, primers & thermocycling |
| [`gate_droplets`](qpcr.md#gate_droplets) | Gate droplets | 🧪 qPCR & digital PCR |
| [`gc_content`](analyze.md#gc_content) | GC content | 📊 Sequence analysis |
| [`gene_set_camera`](discovery.md#gene_set_camera) | Gene set camera | 🔬 Expression & hypothesis testing |
| [`gene_set_enrichment`](discovery.md#gene_set_enrichment) | Gene set enrichment | 🔬 Expression & hypothesis testing |
| [`gene_set_overrepresentation`](discovery.md#gene_set_overrepresentation) | Gene set overrepresentation | 🔬 Expression & hypothesis testing |
| [`generate_conformers`](chem.md#generate_conformers) | Generate conformers | ⚗️ Cheminformatics |
| [`genotype_pca`](analyze.md#genotype_pca) | Genotype PCA | 📊 Sequence analysis |
| [`get_construction_history`](pipelines.md#get_construction_history) | Get construction history | 🔗 Pipelines & lab records |
| [`get_open_record`](workspace.md#get_open_record) | Get open record | 🖥️ Workbench state |
| [`get_selection`](workspace.md#get_selection) | Get selection | 🖥️ Workbench state |
| [`gibson_assemble`](cloning.md#gibson_assemble) | Gibson assemble | 🧬 Cloning & assembly |
| [`golden_gate_assemble`](cloning.md#golden_gate_assemble) | Golden Gate assemble | 🧬 Cloning & assembly |
| [`graft_antibody_cdrs`](protein.md#graft_antibody_cdrs) | Graft antibody CDRs | 🧩 Proteins, domains & proteomics |
| [`history_protocol`](data.md#history_protocol) | History protocol | 🗄️ Public databases & records |
| [`hmm_build`](analyze.md#hmm_build) | HMM build | 📊 Sequence analysis |
| [`hmm_search`](analyze.md#hmm_search) | HMM search | 📊 Sequence analysis |
| [`hmmscan`](analyze.md#hmmscan) | Hmmscan | 📊 Sequence analysis |
| [`humanize_antibody`](protein.md#humanize_antibody) | Humanize antibody | 🧩 Proteins, domains & proteomics |
| [`impute_flow_cytometry_infinity`](analyze.md#impute_flow_cytometry_infinity) | Impute flow cytometry infinity | 📊 Sequence analysis |
| [`infer_proteins`](protein.md#infer_proteins) | Infer proteins | 🧩 Proteins, domains & proteomics |
| [`isotope_envelope`](analyze.md#isotope_envelope) | Isotope envelope | 📊 Sequence analysis |
| [`isotopic_composition`](analyze.md#isotopic_composition) | Isotopic composition | 📊 Sequence analysis |
| [`ligate_fragments`](cloning.md#ligate_fragments) | Ligate fragments | 🧬 Cloning & assembly |
| [`ligation_independent_clone`](cloning.md#ligation_independent_clone) | Ligation independent clone | 🧬 Cloning & assembly |
| [`linkage_disequilibrium`](analyze.md#linkage_disequilibrium) | Linkage disequilibrium | 📊 Sequence analysis |
| [`list_databases`](data.md#list_databases) | List databases | 🗄️ Public databases & records |
| [`list_experiments`](workspace.md#list_experiments) | List experiments | 🖥️ Workbench state |
| [`list_library`](workspace.md#list_library) | List library | 🖥️ Workbench state |
| [`list_research_runs`](data.md#list_research_runs) | List research runs | 🗄️ Public databases & records |
| [`list_samples`](data.md#list_samples) | List samples | 🗄️ Public databases & records |
| [`list_sgrna_scaffolds`](crispr.md#list_sgrna_scaffolds) | List sgRNA scaffolds | ✂️ CRISPR & genome editing |
| [`list_traces`](workspace.md#list_traces) | List traces | 🖥️ Workbench state |
| [`list_workflow_templates`](pipelines.md#list_workflow_templates) | List workflow templates | 🔗 Pipelines & lab records |
| [`load_record`](workspace.md#load_record) | Load record | 🖥️ Workbench state |
| [`load_trace`](analyze.md#load_trace) | Load trace | 📊 Sequence analysis |
| [`lookup_clinical`](data.md#lookup_clinical) | Lookup clinical | 🗄️ Public databases & records |
| [`lookup_compound`](chem.md#lookup_compound) | Lookup compound | ⚗️ Cheminformatics |
| [`lookup_gene`](data.md#lookup_gene) | Lookup gene | 🗄️ Public databases & records |
| [`lookup_omics`](data.md#lookup_omics) | Lookup omics | 🗄️ Public databases & records |
| [`lookup_ontology`](data.md#lookup_ontology) | Lookup ontology | 🗄️ Public databases & records |
| [`lookup_protein`](protein.md#lookup_protein) | Lookup protein | 🧩 Proteins, domains & proteomics |
| [`lookup_residue_sites`](protein.md#lookup_residue_sites) | Lookup residue sites | 🧩 Proteins, domains & proteomics |
| [`lookup_variant`](variants.md#lookup_variant) | Lookup variant | 🧫 Genomics, variants & copy number |
| [`map_chemical_space`](chem.md#map_chemical_space) | Map chemical space | ⚗️ Cheminformatics |
| [`map_reaction_atoms`](chem.md#map_reaction_atoms) | Map reaction atoms | ⚗️ Cheminformatics |
| [`map_reads`](sequencing.md#map_reads) | Map reads | 📈 Sanger, sequencing & verification |
| [`mask_sequence`](analyze.md#mask_sequence) | Mask sequence | 📊 Sequence analysis |
| [`match_part_by_sequence`](analyze.md#match_part_by_sequence) | Match part by sequence | 📊 Sequence analysis |
| [`matched_molecular_pairs`](chem.md#matched_molecular_pairs) | Matched molecular pairs | ⚗️ Cheminformatics |
| [`melt_profile`](qpcr.md#melt_profile) | Melt profile | 🧪 qPCR & digital PCR |
| [`melting_temperature`](qpcr.md#melting_temperature) | Melting temperature | 🧪 qPCR & digital PCR |
| [`miqe_checklist`](analyze.md#miqe_checklist) | MIQE checklist | 📊 Sequence analysis |
| [`multiplex_pcr`](amplify.md#multiplex_pcr) | Multiplex PCR | 🔥 PCR, primers & thermocycling |
| [`normalize_cytof_beads`](analyze.md#normalize_cytof_beads) | Normalize cytof beads | 📊 Sequence analysis |
| [`normalize_flow_cytometry_batch`](analyze.md#normalize_flow_cytometry_batch) | Normalize flow cytometry batch | 📊 Sequence analysis |
| [`normalize_flow_cytometry_cytonorm`](analyze.md#normalize_flow_cytometry_cytonorm) | Normalize flow cytometry CytoNorm | 📊 Sequence analysis |
| [`notebook_cross_refs`](data.md#notebook_cross_refs) | Notebook cross refs | 🗄️ Public databases & records |
| [`number_antibody`](protein.md#number_antibody) | Number antibody | 🧩 Proteins, domains & proteomics |
| [`optimize_sequence`](design.md#optimize_sequence) | Optimize sequence | 🎛️ Design & expression |
| [`pcr_amplify`](amplify.md#pcr_amplify) | PCR amplify | 🔥 PCR, primers & thermocycling |
| [`peptide_mass`](crispr.md#peptide_mass) | Peptide mass | ✂️ CRISPR & genome editing |
| [`pick_first`](workspace.md#pick_first) | Pick first | 🖥️ Workbench state |
| [`plan_master_mix`](amplify.md#plan_master_mix) | Plan master mix | 🔥 PCR, primers & thermocycling |
| [`plan_next_tools`](workspace.md#plan_next_tools) | Plan next tools | 🖥️ Workbench state |
| [`plan_rnaseq_experiment`](pipelines.md#plan_rnaseq_experiment) | Plan rnaseq experiment | 🔗 Pipelines & lab records |
| [`plan_serial_dilution`](amplify.md#plan_serial_dilution) | Plan serial dilution | 🔥 PCR, primers & thermocycling |
| [`plan_thermocycler_program`](cloning.md#plan_thermocycler_program) | Plan thermocycler program | 🧬 Cloning & assembly |
| [`population_ancestry`](variants.md#population_ancestry) | Population ancestry | 🧫 Genomics, variants & copy number |
| [`population_fst`](variants.md#population_fst) | Population Fst | 🧫 Genomics, variants & copy number |
| [`population_site_stats`](variants.md#population_site_stats) | Population site stats | 🧫 Genomics, variants & copy number |
| [`primer_check`](amplify.md#primer_check) | Primer check | 🔥 PCR, primers & thermocycling |
| [`propagate_uncertainty`](qpcr.md#propagate_uncertainty) | Propagate uncertainty | 🧪 qPCR & digital PCR |
| [`protein_digest`](cloning.md#protein_digest) | Protein digest | 🧬 Cloning & assembly |
| [`protein_disorder`](protein.md#protein_disorder) | Protein disorder | 🧩 Proteins, domains & proteomics |
| [`protein_disorder_metapredict`](protein.md#protein_disorder_metapredict) | Protein disorder metapredict | 🧩 Proteins, domains & proteomics |
| [`protein_membrane_profile`](protein.md#protein_membrane_profile) | Protein membrane profile | 🧩 Proteins, domains & proteomics |
| [`protein_profile`](protein.md#protein_profile) | Protein profile | 🧩 Proteins, domains & proteomics |
| [`protein_properties`](protein.md#protein_properties) | Protein properties | 🧩 Proteins, domains & proteomics |
| [`protein_signal_peptide`](crispr.md#protein_signal_peptide) | Protein signal peptide | ✂️ CRISPR & genome editing |
| [`protein_topology`](protein.md#protein_topology) | Protein topology | 🧩 Proteins, domains & proteomics |
| [`quantify_base_editing`](crispr.md#quantify_base_editing) | Quantify base editing | ✂️ CRISPR & genome editing |
| [`quantify_dpcr`](qpcr.md#quantify_dpcr) | Quantify dPCR | 🧪 qPCR & digital PCR |
| [`query_database`](data.md#query_database) | Query database | 🗄️ Public databases & records |
| [`rank_next_tests`](design.md#rank_next_tests) | Rank next tests | 🎛️ Design & expression |
| [`rank_reference_genes`](analyze.md#rank_reference_genes) | Rank reference genes | 📊 Sequence analysis |
| [`rank_strategies`](cloning.md#rank_strategies) | Rank strategies | 🧬 Cloning & assembly |
| [`rank_tradeoffs`](design.md#rank_tradeoffs) | Rank tradeoffs | 🎛️ Design & expression |
| [`read_answer_window`](pipelines.md#read_answer_window) | Read answer window | 🔗 Pipelines & lab records |
| [`read_eds_run`](analyze.md#read_eds_run) | Read eds run | 📊 Sequence analysis |
| [`read_mgf`](analyze.md#read_mgf) | Read MGF | 📊 Sequence analysis |
| [`read_mzml`](analyze.md#read_mzml) | Read mzML | 📊 Sequence analysis |
| [`read_rdml_run`](qpcr.md#read_rdml_run) | Read RDML run | 🧪 qPCR & digital PCR |
| [`read_sequencing_qc`](sequencing.md#read_sequencing_qc) | Read sequencing QC | 📈 Sanger, sequencing & verification |
| [`read_structure`](analyze.md#read_structure) | Read structure | 📊 Sequence analysis |
| [`read_structure_consensus`](sequencing.md#read_structure_consensus) | Read structure consensus | 📈 Sanger, sequencing & verification |
| [`read_variant_calls`](variants.md#read_variant_calls) | Read variant calls | 🧫 Genomics, variants & copy number |
| [`recombine`](cloning.md#recombine) | Recombine | 🧬 Cloning & assembly |
| [`recompute_trace_quality`](sequencing.md#recompute_trace_quality) | Recompute trace quality | 📈 Sanger, sequencing & verification |
| [`record_composition`](analyze.md#record_composition) | Record composition | 📊 Sequence analysis |
| [`record_experiment`](workspace.md#record_experiment) | Record experiment | 🖥️ Workbench state |
| [`relative_expression`](analyze.md#relative_expression) | Relative expression | 📊 Sequence analysis |
| [`remember_lab_preference`](pipelines.md#remember_lab_preference) | Remember lab preference | 🔗 Pipelines & lab records |
| [`research_run_status`](data.md#research_run_status) | Research run status | 🗄️ Public databases & records |
| [`resolve_gene_sets`](discovery.md#resolve_gene_sets) | Resolve gene sets | 🔬 Expression & hypothesis testing |
| [`restore_trace_file_calls`](sequencing.md#restore_trace_file_calls) | Restore trace file calls | 📈 Sanger, sequencing & verification |
| [`restriction_ligate`](cloning.md#restriction_ligate) | Restriction ligate | 🧬 Cloning & assembly |
| [`resume_research_run`](data.md#resume_research_run) | Resume research run | 🗄️ Public databases & records |
| [`reverse_complement`](analyze.md#reverse_complement) | Reverse complement | 📊 Sequence analysis |
| [`rps_blast_cdd`](protein.md#rps_blast_cdd) | RPS BLAST CDD | 🧩 Proteins, domains & proteomics |
| [`rps_blast_smart`](protein.md#rps_blast_smart) | RPS BLAST SMART | 🧩 Proteins, domains & proteomics |
| [`rpstblastn_smart`](protein.md#rpstblastn_smart) | RPSTBLASTN SMART | 🧩 Proteins, domains & proteomics |
| [`run_discovery_programme`](discovery.md#run_discovery_programme) | Run discovery programme | 🔬 Expression & hypothesis testing |
| [`run_gel_lane`](cloning.md#run_gel_lane) | Run gel lane | 🧬 Cloning & assembly |
| [`run_gel_plate`](cloning.md#run_gel_plate) | Run gel plate | 🧬 Cloning & assembly |
| [`run_workflow`](pipelines.md#run_workflow) | Run workflow | 🔗 Pipelines & lab records |
| [`save_enzyme_collection`](pipelines.md#save_enzyme_collection) | Save enzyme collection | 🔗 Pipelines & lab records |
| [`scaffold_network`](chem.md#scaffold_network) | Scaffold network | ⚗️ Cheminformatics |
| [`scan_intrinsic_terminators`](analyze.md#scan_intrinsic_terminators) | Scan intrinsic terminators | 📊 Sequence analysis |
| [`scan_motif_sites`](protein.md#scan_motif_sites) | Scan motif sites | 🧩 Proteins, domains & proteomics |
| [`scan_protein_domains`](protein.md#scan_protein_domains) | Scan protein domains | 🧩 Proteins, domains & proteomics |
| [`scan_sigma70_promoters`](analyze.md#scan_sigma70_promoters) | Scan sigma70 promoters | 📊 Sequence analysis |
| [`scan_splice_sites`](analyze.md#scan_splice_sites) | Scan splice sites | 📊 Sequence analysis |
| [`score_overhang_fidelity`](cloning.md#score_overhang_fidelity) | Score overhang fidelity | 🧬 Cloning & assembly |
| [`score_rbs`](design.md#score_rbs) | Score RBS | 🎛️ Design & expression |
| [`score_spectrum`](analyze.md#score_spectrum) | Score spectrum | 📊 Sequence analysis |
| [`score_variant_effect`](variants.md#score_variant_effect) | Score variant effect | 🧫 Genomics, variants & copy number |
| [`screen_contamination`](crispr.md#screen_contamination) | Screen contamination | ✂️ CRISPR & genome editing |
| [`screen_guides`](crispr.md#screen_guides) | Screen guides | ✂️ CRISPR & genome editing |
| [`screen_molecule_library`](crispr.md#screen_molecule_library) | Screen molecule library | ✂️ CRISPR & genome editing |
| [`screen_oligo_structure`](crispr.md#screen_oligo_structure) | Screen oligo structure | ✂️ CRISPR & genome editing |
| [`scrub_restriction_sites`](cloning.md#scrub_restriction_sites) | Scrub restriction sites | 🧬 Cloning & assembly |
| [`search_literature`](data.md#search_literature) | Search literature | 🗄️ Public databases & records |
| [`search_molecule_library`](chem.md#search_molecule_library) | Search molecule library | ⚗️ Cheminformatics |
| [`search_off_targets`](crispr.md#search_off_targets) | Search off targets | ✂️ CRISPR & genome editing |
| [`search_records`](data.md#search_records) | Search records | 🗄️ Public databases & records |
| [`select_substitution_model`](phylo.md#select_substitution_model) | Select substitution model | 🌳 Alignment & phylogenetics |
| [`simulate_rnaseq_power`](design.md#simulate_rnaseq_power) | Simulate rnaseq power | 🎛️ Design & expression |
| [`simulate_taqman_curve`](qpcr.md#simulate_taqman_curve) | Simulate TaqMan curve | 🧪 qPCR & digital PCR |
| [`size_fragments`](analyze.md#size_fragments) | Size fragments | 📊 Sequence analysis |
| [`solve_dilution`](amplify.md#solve_dilution) | Solve dilution | 🔥 PCR, primers & thermocycling |
| [`summarize_rows`](analyze.md#summarize_rows) | Summarize rows | 📊 Sequence analysis |
| [`survey_off_targets`](crispr.md#survey_off_targets) | Survey off targets | ✂️ CRISPR & genome editing |
| [`synthesize_flow_cytometry`](analyze.md#synthesize_flow_cytometry) | Synthesize flow cytometry | 📊 Sequence analysis |
| [`target_decoy_qvalues`](analyze.md#target_decoy_qvalues) | Target decoy qvalues | 📊 Sequence analysis |
| [`test_cytometry_spatial_interactions`](analyze.md#test_cytometry_spatial_interactions) | Test cytometry spatial interactions | 📊 Sequence analysis |
| [`tide_quantify_indels`](crispr.md#tide_quantify_indels) | TIDE quantify indels | ✂️ CRISPR & genome editing |
| [`trace_raw_signal`](sequencing.md#trace_raw_signal) | Trace raw signal | 📈 Sanger, sequencing & verification |
| [`transform_tree`](phylo.md#transform_tree) | Transform tree | 🌳 Alignment & phylogenetics |
| [`translate_sequence`](analyze.md#translate_sequence) | Translate sequence | 📊 Sequence analysis |
| [`tree_statistics`](phylo.md#tree_statistics) | Tree statistics | 🌳 Alignment & phylogenetics |
| [`tree_taxon_annotations`](design.md#tree_taxon_annotations) | Tree taxon annotations | 🎛️ Design & expression |
| [`trim_reads`](sequencing.md#trim_reads) | Trim reads | 📈 Sanger, sequencing & verification |
| [`trim_trace`](sequencing.md#trim_trace) | Trim trace | 📈 Sanger, sequencing & verification |
| [`validate_gene_trait`](discovery.md#validate_gene_trait) | Validate gene trait | 🔬 Expression & hypothesis testing |
| [`validate_workflow`](pipelines.md#validate_workflow) | Validate workflow | 🔗 Pipelines & lab records |
| [`variant_call_summary`](variants.md#variant_call_summary) | Variant call summary | 🧫 Genomics, variants & copy number |
| [`variant_consequences`](variants.md#variant_consequences) | Variant consequences | 🧫 Genomics, variants & copy number |
| [`verify_construct`](sequencing.md#verify_construct) | Verify construct | 📈 Sanger, sequencing & verification |
| [`verify_read`](sequencing.md#verify_read) | Verify read | 📈 Sanger, sequencing & verification |
| [`write_structure_library`](chem.md#write_structure_library) | Write structure library | ⚗️ Cheminformatics |
