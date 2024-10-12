.. include:: /properties.rst

.. |highl| replace:: As a major part of negative control data, rRFs do not bind specifically to Argonaute proteins

.. meta::
   :description: With Coalispr, a Python program to count aligned specified reads, it is shown that, as a major part of negative control data, rRFs do not bind specifically to Argonaute proteins (Ago). Various ncRNAs like U1, or box C/D and H/ACA snoRNAs could be identified for Cryptococcus, which was supported by phylogenetic comparison. 
   :keywords: Bioinformatics, RNA-Seq, rRFs, Ago, Argonaute, Control data, snoRNAs, Cryptococcus, Mouse, H99, JEC21, miRNA, siRNA, Coalispr, Pandas, Matplotlib, Box C/D, HACA

..   |codebergicon| replace:: :raw-html:`<a class="svglink" href="https://codeberg.org/coalispr/" aria-label="Codeberg" target="_blank"><svg width="48" height="48"<svg width="4em" height="4em" viewBox="0 0 4.233 4.233"><path fill="#aaa" d="M46.984 76.122a2.117 2.117 0 0 0-1.793 3.242l1.764-2.282c.013-.016.045-.016.058 0l.736.953h-.527l.011.042h.55l.155.2h-.648l.018.067h.68l.138.177h-.769l.024.085h.81l.123.158h-.889l.03.103h.939l.107.139h-1.008l.032.115h1.065l.099.128H47.56l.033.115h1.184a2.117 2.117 0 0 0-1.793-3.242zm.645 3.37.032.114h.94a2.24 2.24 0 0 0 .09-.114zm.068.243.031.114h.629a2.54 2.54 0 0 0 .125-.114zm.067.242.032.115h.212c.063-.036.121-.073.184-.115z" style="paint-order:markers fill stroke" transform="translate(-44.867 -75.991)"/><desc>"Codeberg icon adapted by brobr,see https://codeberg.org/Codeberg/Community/issues/976"</desc></svg></a>`


|papertitl|
===========

|

:raw-html:`<a href="&#109;&#097;&#105;&#108;&#116;&#111;:&#115;&#098;&#111;&#114;&#103;&#054;&#051;&#064;&#100;&#105;&#115;&#114;&#111;&#111;&#116;&#046;&#111;&#114;&#103;">&#082;&#111;&#098;&#032;&#118;&#097;&#110;&#032;&#078;&#117;&#101;&#115;</a>`\ |nbsp|\ |orcidicon|


Current day bioinformatics provides mainly solutions and tools to analyze data obtained by high-throughput sequencing of protein-gene transcripts with statistical underpinning. Based on experience with small non-coding RNAs, we propose an alternative heuristic, which demands standard inclusion of negative control data in initial bioinformatics analysis. This approach facilitates a read-counting method that relies only on genomic coordinates and bypasses the need for an overlap with an annotated feature in a reference file. 

This heuristic can help to understand other difficulties in the analysis and comparison of read-count data. It can be argued that all RNA is a product of gene-transcription and falls therefore into the same category, thereby posing the same problems to solve. This turns out to be, at least practically, too simplistic a view of the plethora of high-throughput data that can be generated. For example, selective [#sele]_ RNA sequencing raises problems that require solutions different to those commonly applied. One of the difficulties relates to how relative changes between independent libraries can be quantified. The prevalent practice centers on applications designed to measure differential gene-expression, like Deseq2_ or EdgeR_. The internal standards required for normalization by these tools go missing when sequencing data do not directly represent transcription. The link with transcription is severed when the biological process generating the RNA follows a different route like occurs during amplification of siRNA [#siamp]_ or after the pool of unrelated, unchanged transcripts that form the internal standard is lost by selective enrichment of the input RNA.

The method we propose deals with an ongoing problem in bioinformatics analysis of high-throughput data, that of distinguishing meaningful information against a backdrop of noise and accidental peaks which, by their omnipresence in repeats of experiments with various substrates, appear to be linked to methodology rather than inputs. This problem further extends to meta-analysis of various independent datasets [#geofish]_ if this complication is not recognized. We show, using ribosomal RNA fragments (:term:`rRFs`) as an example, that novel insights cannot solely be based on large numbers that appear to promise statistical significance: 

.. highlights::

  |highl|



We have developed a Python_ application  [#amat]_ to systematically clean up datasets before their further analysis. This step happens normally 'behind the scenes' but we think that making this explicit serves reproducibility, accessibility of the 'real' information in a dataset, and trustworthiness of derived conclusions. Despite the blatantly obvious we state for many colleagues, we hope our approach will be useful in general and inform people less familiar with experimentation. The crux is this: bring essential biological methodology, the `Bio`, into bioinformatics; integrate experimental control data into the mathematical analysis. Experimenters do not just generate data, they produce data and control data; the latter are key to draw valid conclusions from the former. What is meant by control data?

|

Control data
------------

Biological experiments encompass approaches that historically precede but are conceptually similar to machine-learning methods when training is done on 'bad' vs 'good' examples in the data.

Experimental success lies in the pragmatic possibility to make a proper assessment. That is, from the output of the experiment a conclusion concerning some hypothesis on a biological system can be drawn. Experimental results come in various shapes and forms, from a gel-image to a long list of nucleotide sequences in high-throughput RNA sequencing (RNA-Seq). These results can only be meaningful if standards are present within the experiment to evaluate the overall output against. This because a biological experiment involves components that are not fail-safe. Reagents can expire and no longer be active [#offs]_. Other problems relate to methodology. For example, in small RNA sequencing the short molecules isolated are always mixed with remnants of longer molecules. A size-selection step during the RNA and/or cDNA library preparation will not resolve this difficulty. In general, RNA-Seq libraries will contain contaminants because of electrostatic interactions between nucleophylic molecules in the starting input or when these molecules have some affinity to materials used during the preparative steps. To address such issues biological experiments contain internal tests for proving that outcomes obtained with the followed procedures would have been valid. This also holds for high-throughput sequencing techniques [Esteban-Serna_].

The standards that render the internal tests are called the :term:`positive <positive control>` and :term:`negative control`\s. The :term:`negative control` is a sample that is not expected to provide an informative answer; a negative control, also called 'mock' control, shows the noise in the experiment. In contrast, a :term:`positive control` should give output that is specific, i.e. adheres to the current knowledge available for the biological system under study. It tells that the experimental conditions produced a useful answer. To assess the effect of a mutation (or another condition) is to check what happens to the specific output relative to that of the controls. 

.. figure:: /../_static/images/Sarshad-Fig3D.png
   :name: sarshad3dpap
   :align: right
   :width: 318 px
   :height: 478 px
   :scale: 40%

   **Figure 1.** Input RNA. 

   | Sarshad-2018 [`Figure 3`_\ D];
   | see text for details.
   | |copy| *cell.com; elsevier.com*
   |


The noise of the negative control, the meaningless signals that are also expected for other samples in the same experiment, can be seen as the 'bad' examples in a machine-learning training set. Such noise is visible as a diffuse smear in a biochemical analysis of RNA used for the construction of cDNA libraries in :term:`RNA-Seq`. For example, in a study of :term:`microRNAs <miRNA>` by Sarshad et al. [Sarshad-2018_] the gel-image of :ref:`Figure 1 <sarshad3dpap>` (taken from their `Figure 3`_\ D) shows radioactively labeled RNA that is representative for RNA-Seq input. The RNA was purified from cells that only produce one functional :term:`Argonaute <Ago>` protein (``AGO2``) after induction of the gene expressing an :term:`epitope`-tagged variant (``+ Dox``). The protein was isolated by :term:`immunoprecipitation` (``IP:Flag``) from two cellular fractions (cytoplasmic, ``C`` and nuclear, ``N``). The same procedure was done with cells that were not induced (``- Dox``) and therefore not expected to make AGO2. In this experiment, the ``- Dox`` samples are the :term:`negative control` to ensure that output obtained for the samples of real interest (``+ Dox``) can be trusted. The latter samples could be dubbed the :term:`positive control` because the experimental outcome showed the co-purification of AGO2  with a size-restricted population of RNA molecules (the fat black band at the level of ``:F`` in the label ``IP:Flag``). This was in agreement with the methodology and published findings that :term:`miRNA`\s of ~22 nt bind to Argonaute proteins in mammals. Other controls in this example are for correct fractionation into cytoplasmic components (``CALR``) and nuclei (``LMNA``).

.. _vissub:

The absence of tagged protein in the ``- Dox`` samples demonstrated that the gene was not expressed and indicated properly working induction and immunoprecipitation procedures. Visual subtraction guides the researcher to the conclusion that only the fat band in the lanes of the positive samples represents the meaningful outcome of the experiment: the signals common to all lanes, the :term:`background` :term:`smear`\ s, can be ignored. But not for the follow-up experiment. The RNA smear, visible in the ``- Dox`` lanes, is still present in the positive samples and will be part of the input for RNA-Seq, which was subsequently done on all four samples to enable a similar comparison with respect to the sequencing results. 

In the discussion of their results, Sarshad et al. [Sarshad-2018_] only mention the relevant data, the :term:`miRNA`\s isolated from the ``+ Dox`` samples. Still, the ``- Dox`` dataset would have been used to determine which sequencing reads could be ignored in the ``+ Dox`` data, enabling identification of sequences that specifically associate to AGO2. This filtering is common practice and hardly mentioned or properly explained in publications, which impacts reproducibility. In other words, this essential step can easily be overlooked, especially by non-experimenters, and is possibly the reason negative data sets are not taken into account by at least some meta-studies. This is one of the problems we discuss in this paper, and which we have addressed by developing a Python_ application to systematically clean up and count (small) RNA sequencing results.


.. highlights::

   High-throughput datasets can be full of noise. 

The strategy of ruling out 'bad' examples as in a machine-learning training set is evident when experimenters remark that some particular hits were not used or filtered from the dataset [#massspec]_. Statements concerning omitted reads are indicative for the fact that high-throughput data always contain sequences different from those that are of interest or relevant for the system under study.

When purifying reagents, which determines the success of an experiment, irrelevant molecules can be fished out from the input-sample. This will minimize contaminating signals in the eventual output. :term:`Depletion kits` make the RNA-Seq more efficient by improving the coverage for data the researchers are interested in. Other experimental approaches are abound with a similar aim of improving the signal to noise ratio. For example, as described above, selective purification of an RNA-binding protein and then sequencing the associated RNA helps to narrow down the population of RNA molecules the protein interacts with [#alt]_. Cross-linking techniques have been developed to enrich even more for biologically-relevant over spurious molecular interactions, be it between proteins and RNA [#cracclip]_ or between RNA-molecules bound to a protein of interest [#clash]_. 

The words 'narrow down' and 'enrich' are necessary: noise, although reduced, will :term:`remain <smear>`. Both cDNA library construction and the sequencing reaction involve PCR amplification steps. This means that the noise will be increased along with the signals. Therefore, as illustrated below, the noise can form a more substantial portion of the RNA-Seq output than expected with input of good quality as exemplified by :ref:`Figure 1 <sarshad3dpap>`. Such background corresponds to the category of 'unlikely' reads that have significant overlap with peaks in samples extracted from a 'blank' control in `Figure 2 <https://doi.org/10.1111/mmi.15073#mmi15073-fig-0002>`_ of [Esteban-Serna_].

The take-home message here is that RNA-Seq data are not 'clean'; they are messy and not usable as is. To draw reliable conclusions from the data, the irrelevant noise has to be put aside. We propose to make this taken-for-granted aspect of the data analysis explicit and to systematically remove the noise by following common biologists' practice of using negative controls. We demonstrate how this essence of experimentation can translate to a bioinformatics approach.

|

bioinformatics\ |nbsp|\ use of negative\ |nbsp|\ controls   
---------------------------------------------------------

.. figure:: /../_static/images/specific_light_ed.svg
   :name: trac_smu
   :align: left
   :width: 270
   :height: 132
   :scale: 70 %
   :class: clear-left


   **Figure 2.** :term:`Specifying <specified>` bedgraph signals

   | :term:`Specific` (left) and  :term:`Unspecific` (right) 
   | signals in :term:`negative <negative control>` (``U``), or :term:`positive <positive control>`  (``S``) 
   | controls and :term:`mutant` (``M``) samples. 
   | more precise version is in the notes [#settgs]_.
   |



|prgnam| (*CO*\unt *ALI*\gned *SP*\ecified *R*\eads) [#src]_ consists of a collection of Python_ scripts for quick, selective comparison and visualization of high throughput sequencing data. The program dissects the data per chromosome using bedgraphs for input and helps to retrieve read counts from associated bam files. For relatively small fungal genomes, it can display over 100 bedgraphs in one panel.

.. figure:: /../_static/images/h99-chr8_reads-specification.png
   :name: readspecpap
   :align: right
   :width: 1491 px
   :height: 1355 px
   :scale: 30%

   **Figure 3.** :term:`Specifying <specified>` reads by comparing controls [#sirns]_.

   | In the top panel traces for the mutants are 
   | set to invisible to show the overlap between 
   | positive and negative controls.
   |


The program mimics the :ref:`visual subtraction <vissub>` between positive and negative samples referred to above, but acts on bedgraph traces, as illustrated in the schematic of :ref:`Figure 2 <trac_smu>`. For each sample, stranded bedgraph data are tabulated per chromosome [#chrdiff]_ by splitting and summing over bins [#bins]_. Tabulated bin values are then compared between negative and positive samples. When a bin contains hits in a :term:`negative control`, while comparable values are found for other samples, the reads in that bin are taken to represent a background signal. These reads are dubbed ':term:`unspecific`' (``U``) and can build a low signal, but when they derive from very abundant molecules like :term:`tRNA` or :term:`rRNA`, they accumulate and form substantial peaks in the bedgraph traces. Therefore, in order to distinguish such high levels of noise linked to the applied methods from signals specifically detected by the experiment, comparison with :term:`negative control` data is key. 

:term:`Specific` signals (``S``) are marked by bins that mainly contain reads in the case of the :term:`positive control`\s or :term:`mutant` samples.  These bins show coverage for reads representing RNAs that can be linked to a condition under study or the protein they have been co-purified with. These reads are (mostly) absent from :term:`negative control`\s, so that the difference in coverage rather than signal intensities is used as the leading parameter to :term:`specify <specified>` reads as specific or unspecific. While the difference in coverage is the major determinant, various configuration settings [#settgs]_ help to define segments with :term:`specific` signals (the remainder being :term:`unspecific`). A base level is set below which signals are not taken into account. The second parameter sets a threshold as the fold-difference between specific and unspecific signals in the case reads of :term:`positive control`\s and those in :term:`negative control`\s overlap. Then, to account for missed or dismissed data, the tolerated gap between genomic peak coordinates can be set to define a contiguous segment for counting reads. 

Comparison of read signals collected in bins, instead of directly per nucleotide, is a pragmatic decision. It enables tabulation of all data and thereby the application of vectorization [#vect]_ techniques to process all samples in one go (here with the Python_ module Pandas_). Re-organizing bedgraph signals to a common index (bin-related coordinates) reduces the resolution [#genbr]_ but is the pivot of the approach. Binning concentrates reads which better defines difference-trends when read coverage is variable between samples. The reduction in resolution helps to distinguish genome regions with specific signals from those with unspecific, background peaks. This sorting, preceding subsequent counting and other analysis steps, is the main, novel contribution of |prgnam| to current bioinformatics and highly relevant when size-selection steps cannot reduce contaminating signals, as is the case for small RNA-Seq. An example of peak-sorting into the two categories by |prgnam| is shown in :ref:`Figure 3 <readspecpap>`.

|

Counting\ |nbsp|\ reads
.......................

.. highlights::

   ... without reference to an annotations file. 

Apart from visual comparison of data-traces, the program has been developed to obtain count-data [#serds]_ for small non-coding RNAs. Genome annotation files for most organisms lack information on such RNAs, while programs like HTSeq_ [Putri-2022_] or pyCRAC_ [Webb-2014_] base counts on annotated features. Thus, to count small RNAs with these programs, an annotation file has to be prepared from scratch [#htsq]_. This is laborious, error-prone and not very scalable to other organisms or when a major update of the genome is published. By incorporating :term:`negative control` data in the analysis, the bin-comparison helps to distinguish meaningful reads. With this approach, applied by |prgnam|, it is possible to systematically obtain read counts for various kinds of data. 


.. figure:: /../_static/images/library_counts_combined_strands_by_category_mouse.png
   :name: mmu-totlibs
   :align: right
   :width: 729 px
   :height: 313 px
   :scale: 60%
   
   **Figure 4.** Counts for :term:`specified` reads.

   | Reads in miRNA libraries of [Sarshad-2018_]. 
   | Large fractions of :term:`positive control` reads are
   | :term:`unspecific` and shared with the :term:`negative control`\s [#libcnts]_.
   |

The separation of reads into those that fit the :term:`positive control`\s  and those that are common to all samples (i.e overlap with :term:`negative control`\s), categorizes reads as :term:`specific` or :term:`unspecific`. By this process also the chromosomal regions are defined that link to these categories. Counting of reads can thus be based solely on genomic coordinates in sorted :term:`bam` alignment files the bedgraphs derive from, not requiring an overlap with an annotation reference [#htsq]_. The program implements this principle and supports fast counting of reads when these have been collapsed prior to the mapping. Such collapsing takes all identical sequences as one, but tracks the total number that represent a cDNA [#collps]_.

Dividing reads into specific signals and unspecific noise, shows that a large fraction of the :term:`positive control` reads overlaps with those of the :term:`negative control` (:ref:`Fig. 4 <mmu-totlibs>`). This was to be expected because of the :ref:`background smear <sarshad3dpap>` being part of the input for the RNA-Seq libraries. The characteristics of the grouped reads are very different. The majority of AGO2-associated RNAs are 22-23 nt, conforming to expected lengths of miRNAs, and have an A as the 5' nt. Unspecific RNAs are more diverse in length, with RNAs of 31-33 nt starting with a G most prominent (:ref:`Fig. 5 <mmu-totlengs>`).


.. figure:: /../_static/images/library_lengths_mouse_8_combined_log2bg4_skip20.png
   :name: mmu-totlengs
   :figwidth: 98%
   :align: right
   :width: 1120 px
   :height: 563 px
   :scale: 70%
   
   **Figure 5.** Lengths and 5' nt of :term:`specified` reads  [#lencnts]_.


   | The majority of AGO2-associated RNAs in miRNA-seq libraries of [Sarshad-2018_] are 22-23 nt with an A as the 5' nt; very different from RNAs shared with the :term:`negative control`\s. The unspecific reads of about 32 nt with a G as 5' end do not fit the miRNA binding pocket on Argonaute nor stand out among rRFs (see :ref:`Fig. 7 <mmu18s45sunsel2>`).
   |


| 
|

Ribosomal\ |nbsp|\ RNA\ |nbsp|\ hits 
------------------------------------

.. .. sidebar:: ``coalispr showgraphs -c chr17 -w1``

.. figure:: /../_static/images/miRNAs-vs-18S-chr17-mouse.png
   :name: mmu18Schr17-18s
   :align: right 
   :width: 900 px
   :height: 2887 px
   :scale: 24%

   **Figure 6.** Trace analysis for chr. 17

   | From top (1) to bottom (4):
   | 1: 18S :term:`rRNA` reads are common,
   | 2: Specific to AGO2 are :term:`miRNA`\s.
   | 3: An unspecific hit for a putative
   | miRNA target [#mirtrg]_. 
   | 4: All reads for chromosome 17 [#mirns]_.
   |



Very abundant cellular complexes like translating ribosomes are a source for fragments (rRNA, tRNA, or highly expressed mRNA) that create unwanted :term:`background` signals in RNA-Seq data. Most ribosomal fragments (:term:`rRFs`) originate from very long (precursor) molecules. This section describes the analysis of rRFs in datasets by means of |prgnam|.

|

Mouse\ |nbsp|\ miRNA\ |nbsp|\ data
..................................

Mammalian ribosomal DNA repeats encode 45S pre-ribosomal precursors. Of these rDNA repeats, an 18S unit on chromosome 17 [#rrn]_ is annotated for the reference genome used by Sarshad et al. [Sarshad-2018_]. The display of :ref:`Figure 6 <mmu18Schr17-18s>`, generated with the command ``coalispr showgraphs -c chr17``, shows traces for nuclear and cytoplasmic negative controls (red) that are indistinguishable from those for the AGO2 IPs (blue) in the case of sequences mapping to rDNA (top). Compare this to loci for miRNA genes, expected to be covered by reads associated with AGO2 rather than those isolated from the uninduced samples. This can be seen in the range (18050000, 18052000) on chromosome 17: there is an miRNA cluster of Mir99b, Mirlet7e, and  Mir125a (while ENSMUSG0000207560 was not detected). When the complete 45S rDNA unit is included in the genome for mapping the sequenced RNAs against, no major change was observed for AGO2-specific reads, while cDNAs derived from :term:`rRFs` were comparable for all samples for covering the 45S rDNA region (:ref:`Fig. 7 <mmu18s45sunsel2>`, top). No group of rRFs or rRFs-derived cDNAs could be discerned, incl. those that adhered to the characteristics of miRNAs, that stood out in positive samples compared to the negative controls with respect to length and 5' nucleotide (:ref:`Fig. 7 <mmu18s45sunsel2>`, bottom). These observations indicate that, despite being among the most abundant reads in this dataset [#annot]_, rRFs cannot be proven to be specifically associated with AGO2. This outcome undermines published meta-analyses claiming such a role for rRFs, a suggestion that originated from the over-optimistic assumptions that input RNA had been sufficiently pure and that background in the form of a :term:`smear` on :ref:`gel <sarshad3dpap>` would not produce relevant count numbers in RNA-Seq. This would all have been preventable had their bioinformatics analysis incorporated available :term:`negative control` data; rRFs are not co-purified with mouse AGO2 because of a biologically meaningful interaction.

.. figure:: /../_static/images/rRFs-45S-mouse_rRFcounts.png
   :name: mmu18s45sunsel2
   :align: left
   :width: 1898 px
   :height: 1337 px
   :scale: 24%

   **Figure 7.** Mouse 45S derived rRF-cDNAs and rRFs. 

   | Comparable coverage (top left) of 45S rDNA for cDNA's 
   | incl. miRNA-like sequences (orange) and no specific 
   | enrichment of a class of rRFs in positive samples on 
   | the basis of counts (top right) or length-distributions 
   | (bottom) in comparison to negative controls.
   |


|
|

Yeast\ |nbsp|\ pre\ |nbh|\ rRNA\ |nbsp|\ processing\ |nbsp|\ factors
....................................................................

The finding that rRFs are common to all samples does not mean they cannot represent specific interactions between rRNA and proteins.  Techniques based around UV crosslinking of RNA to the proteins of interest before purification [#cracclip]_ have been developed for exactly this purpose, identifying binding regions for processing factors involved in ribosome assembly and rRNA maturation [Granneman-2009_, Granneman-2010_, Granneman-2011_]. Despite the stringent and harsh purification procedures applied in these approaches, background signals from abundant molecules cannot be evaded. Samples that have not been irradiated can be taken as negative controls but in the case of tight complexes or strong interactions this is not ideal. An alternative way to assess noise is by comparing crosslink data for different, unrelated RNA-binding proteins [#mucontr]_. 

.. figure:: /../_static/images/rDNA-Puf6-Kre33_yeast_chr_xii_all_reads__collapsed.png 
   :name: craclibs
   :align: right
   :width: 900 px
   :height: 1458 px
   :scale: 24%

   **Figure 8.** rRF reads 
   
   | Kre33 crosslinks specifically 
   | to 18S rRNA regions (top);
   | Puf6 binds helices in 25S
   | rRNA (bottom) [#crosscon]_. Nab3
   | is the negative control.
   |

To illustrate how noise can be filtered by using data-sets as mutual controls, various CRAC-samples [#cracclip]_ obtained for processing factors Kre33 [Sharma-2017_], Puf6 [Gerhardy-2021_], or termination factor Nab3 [van.Nues-2017_] were compared (:ref:`Fig. 8 <craclibs>`). Kre33 directs acetylation of cytosine residues in helices 34, and 45 in the 18S rRNA (within the 90S pre-ribosomal particle) and associates with helices 8-10 [Sharma-2017_]. Especially the latter region stands out from the non-Kre33 traces. Similarly for Puf6, which crosslinks to helices 67-68 of 25S rRNA in the large subunit precursor [Gerhardy-2021_]. The more detailed pyCRAC_ [Webb-2014_] analyses published [Sharma-2017_, Gerhardy-2021_] back the specific association of rRFs with Kre33 or Puf6 by the presence of point-deletions of uracil residues in reads that result from UV-crosslinking of the RNA to either protein [#mutsev]_.

These results underline the experiential fact that abundant, spurious rRFs are identified in RNA-Seq libraries despite the stringent purification procedures applied. Any assessment whether rRFs in RNA-Seq data can be linked to a biological role requires proper controls and independent experimental evidence supporting such a function.

|

Fungal\ |nbsp|\ siRNAs\ |nbsp|\ target\ |nbsp|\ rRNA
.......................................................
Most high-throughput analyses catered for by bioinformaticians deal with data obtained for :term:`mRNA` or RNA fragments that are co-purified with proteins they bind to (with or without cross-linking) and rely on extensive gene-annotation files [#htsq]_. With |prgnam| an alternative way for obtaining count-data has been implemented, which is based on genomic coordinates identified by aligning reads to a reference genome. This is the only feasible approach to interpret RNA-Seq data for classes of short RNAs, like :term:`siRNA`\s that have not (or poorly) been annotated.

.. highlights::

   In *Cryptococcus*, RNAi acts downstream of splicing.

The development and testing of |prgnam| has relied on comparison to count-data obtained with HTSeq_ using manually accumulated reference files for siRNAs of *Cryptococcus* [Dumesic-2013_, Burke-2019_] [#h99tut]_. Compilation of complimentary genomic regions provides the insight that siRNAs, contrary to what has been published [Dumesic-2013_], are raised mostly against transcripts that have undergone splicing. Naturally, the possibility that splicing was not entirely complete remains [#splic]_, so that retained introns could be one of many causes for translation failure [#ribfail]_. Such faults, which would be encountered during interaction of spliced transcripts with ribosomes, could turn these transcripts into targets of the RNAi-machinery.

.. figure:: /../_static/images/h99-rDNA-minus-counts.png
   :name: regcnt_h99-rDNAp
   :align: left
   :width: 1111 px
   :height: 275 px
   :scale: 40%

   **Figure 9.** Minus strand counts for *C.*\ |nbsp|\ *neoformans* rDNA.


In this respect note-worthy, is the finding of siRNAs associated with Argonaute proteins that are directed against mature rRNA. This is seen for *C.*\ |nbsp|\ *neoformans* [#rDNAcneo]_ as well as *C.*\ |nbsp|\ *deneoformans*, but, in the case of the latter, especially after the RNAi response has been restored in cells that did not express their main Argonaute protein, Ago1 [Janbon-2010_], or Rdp1 [:ref:`van.Nues-202? <vnues202x-publ>`]. Another ncRNA associated with ribosomes, SRP RNA, can be targeted by siRNAs (:ref:`Fig. 10 <srprna_hits>`).

Comparable to the mouse miRNA datasets, large amounts of rRFs were detected in cryptococcal siRNA libraries [#h99tut]_ [#rDNAcneo]_. The RNAs derived from the rDNA unit, however, cannot provide any information because no reads are specially enriched among rRFs in *Cryptococcus* that would fit the siRNA binding pocket on Argonaute (:ref:`Fig. 9 <regcnt_h99-rDNAp>`). 

|
|

Small\ |nbsp|\ RNA\ |nbsp|\ count\ |nbsp|\ data\ |nbsp|\ are\ |nbsp|\ problematic
---------------------------------------------------------------------------------

.. highlights::

   ... by lack of an internal control as available for differentially transcribed protein genes.

The main aim of |prgnam| is to sort signals from noise. Peaks in bedgraph traces (loaded with ``coalispr storedata``) are specified as :term:`specific` and :term:`unspecific` and this process can be followed by comparing the output visually, using ``coalispr showgraphs`` (see Figures  :ref:`3 <readspecpap>`, 6-8). The specified reads are then counted (with ``coalispr countbams``) and these counts, stored in :term:`tsv` files, can be used for further analyses. Read-counts can be indicative for the quality of libraries and general experimental outcomes, which can be visualized with ``coalispr showcounts`` (see: :ref:`Figure 4 <mmu-totlibs>` or :ref:`Figure 5 <mmu-totlengs>`). The main interest, however, will be in comparing the counts between samples for the same RNA in order to understand the biological effect of a specific condition or mutation. For this, read counts need to be normalized, which is problematic for small RNA sequencing data. Why?

Because of the variability in library depth, often related to practical difficulties during preparation and recovery of the cDNA sequencing input [#cdnalib]_, an internal normalization standard is required. In the case of :term:`mRNA` sequencing, transcripts from genes are followed and thereby the output of active gene expression. Transcription of genes is highly regulated by transcription factors and depends on the modification status of the C-terminal domains of histones and RNA polymerases and, in many organisms, by chemical modification of the DNA. Gene expression as measured by the levels of mRNA can respond quickly to stress caused by a sudden change in environmental conditions because of RNA-degradation and RNA-RNA interactions [van.Nues-2017_, McKellar-2022_, Iosub-2020_]. In these cases, only gene transcripts involved in biological functions affected by the environmental change under study are supposed to alter while the majority of gene-expression will not be interfered with. This observation is used by many bioinformatics tools (like DESeq2_ or EdgeR_) to detect relative changes in protein-gene expression. The large set of unaffected, apparent constant transcripts forms an internal standard allowing comparison of RNA-Seq data for cells before and after exposure to an environmental or genetic change.

Quantification approaches of differential gene-expression (DE) by programs like DESeq2_ or EdgeR_ are, however, not applicable to assess changes in read-numbers between libraries that cannot represent the transcriptome. Such libraries are those that have been created after enrichment of RNAs by size or by their association to a particular protein. Small RNA libraries of siRNAs also have this characteristic. Formation of siRNAs, other than miRNAs that are controlled by gene-expression, appears to occur as a response to some change in cellular exposure to harmful nucleic-acids, like invasive viral RNA or transcripts from transposons. Therefore, it can be assumed that a change in siRNA levels could be the result of a stochastic or immediate reaction triggered by conditions peculiar to a specific strain or a group of cells. Observed differences in siRNA populations between biological replicates might be an indication for this [:ref:`van.Nues-202? <vnues202x-publ>`]. By lack of evidence that siRNA levels are controlled by a well-regulated process like gene-expression, there is no internal reference, a base-line, that can be decided on. Even if that would be the case, DE-analysis of siRNAs is hampered by, compared to the number of mRNA genes, a relative low frequency of unique loci siRNAs can be mapped to and thus a low number of molecules that might be taken as 'constant'.

Some approaches in assessing small RNA-Seq signals take as a base line the total mapped reads in a library and reads per million (RPM) of these are compared. Bedgraphs, used as input for |prgnam| [#bdgr]_, are based on RPM values. Quantitative comparison between bedgraph signals from different experiments is, however, not always possible. When libraries differ significantly in their number of reads or in the case of considerable differences in the amount of background reads, numerical comparison does not seem to be reliable or trustworthy. Size selection of siRNAs cannot evade contamination by equally-sized break-down products of larger molecules like rRNA or tRNA which, due to their abundance, can be responsible for large (but not necessarily equally large) fractions of total read counts. Different RNA isolation methods, like size-selection of small RNAs from total RNA vs. RNA-IP with Argonaute proteins, can lead to incomparable differences in co-purified background. This makes it difficult to quantify siRNA read-counts by normalization to mapped library sizes, especially when yields of library preparations vary [#cdnalib]_. 

Experimental design decisions (inclusion of a spike-in RNA, or combining samples during cDNA synthesis) will contribute to obtain data that will be better comparable but will not address the above sketched difficulty in quantitative comparison posed by the low number of siRNA loci. Some bioinformaticians argue that the compositional (or relative) nature of count data requires that counts need to be assessed in relation to the mixture of reads in a sample. This aspect, the proportionality of counts, is inherent to the methods by which RNA-Seq libraries are generated [Quinn-2018_, Quinn-2019_]. Still, looking proportionally at RNA sequencing data by compositional data analysis [CoDa_] is not generally done [#prop]_; most methods take the read counts as is and try to normalize these to some standard. To turn this into a valid approach for siRNAs is not straightforward.

|

Sourcing\ |nbsp|\ ncRNAs
------------------------

.. highlights::

   Identified in *Cryptococcus*: RNase P, U1 snRNA, 37 H/ACA and 63 Box C/D snoRNAs.


Many abundant RNA molecules, like rRNAs and small ncRNAs, form common background signals in :term:`RNA-Seq` experiments. Given that most of such molecules are not or only poorly annotated, one can treat the negative control data as a resource to get an impression of the population of ncRNAs in these cells. In the case of the *Cryptococcus* samples, we have been able to identify the full extent of the genes for :doc:`35S pre-rRNA </supplemental/18s-tab>`, a series of tRNAs, some of which had not been annotated, :doc:`SRP RNA </supplemental/otherRNA/srp>` [Dumesic-2015_] (:ref:`Fig. 10 <srprna_hits>`) and - previously unidentified [#idncrna]_ - :doc:`U1 snRNA </supplemental/otherRNA/u1snrna>` (:ref:`Fig. 11 <u1rna_hits>`), and other biologically important molecules like :doc:`RNase P </supplemental/otherRNA/rnasep>`, or :doc:`H/ACA </supplemental/snoRNAs/haca_list>` and :doc:`box C/D </supplemental/snoRNAs/boxcd>` snoRNAs, for example :doc:`U14 </supplemental/snoRNAs/u14>` or snR190, both important for processing of pre-rRNA (:ref:`Fig. 12 <u14_hits>`).

.. figure:: /../_static/images/SRP-RNA_coalispr_h99_bedgraphs_chr_1_all_reads__uncollapsed__23_libs.png
   :name: srprna_hits
   :align: left
   :width: 1200 px
   :height: 900 px
   :scale: 30%
   :figwidth: 50%

   **Figure 10** Hits at the :doc:`SRP RNA </supplemental/otherRNA/srp>` locus in *C.*\ |nbsp|\ *neoformans* H99.


.. figure:: /../_static/images/U1-snRNA_coalispr_h99_bedgraphs_chr_1_all_reads__uncollapsed__23_libs.png
   :name: u1rna_hits
   :align: left
   :width: 1200 px
   :height: 900 px
   :scale: 30%
   :figwidth: 50%

   **Figure 11** Hits at the CNAG_12993 locus for :doc:`U1 snRNA </supplemental/otherRNA/u1snrna>` in *C.*\ |nbsp|\ *neoformans* H99.



Like in other eukaryotes, cryptococcal snoRNAs are formed by transcription of snoRNA genes or are processed from introns that have been removed by splicing from precursors of protein-coding messages [Kufel-2019_]. For example, U14 is encoded by the 2\ :sup:`nd` intron, snR190 by the 1\ :sup:`rst` intron in *Argininosuccinate synthase* genes of *Cryptococcus* (:ref:`Fig.12 <u14_hits>`) which seems conserved in related *Tremellales* (jelly fungi). Both snoRNAs are linked to different genes in more distant  *Tremellomycetes* but appear in the same 5' to 3' order as first found in *S.*\ |nbsp|\ *cerevisiae* [Zagorski-1988_], where it is encoded on a bicistronic transcript. In some fungal species each snoRNA is expressed from a different locus.

Genomic organization has diverged in evolution for other box C/D snoRNAs [van.Nues-2011_], like for snR51, snR41 and snR70. In *Saccharomyces* these snoRNAs are expressed as part of a cluster that is processed (snR41-snR70-snR51). While the homologous guides for snR51 were found in separate snoRNAs, in *Tremellomycetes* snR41 and snR70 derive from introns of a non-coding transcript that in the first intron expresses another snoRNA.

Thus, in *Cryptococcus*, another source for snoRNAs is formed by non-coding transcripts that are spliced and where the sole conserved section is the intron containing the snoRNA. As a corollary, many ncRNAs for *C.*\ |nbsp|\ *neoformans* have been annotated with respect to their exons, while only the precursor would have been functional by providing a (conserved) snoRNA; the spliced exons do not contain conserved sequences that could point to some biological function. Of course, versatile as this organism is, also transcripts for snoRNAs are seen where one snoRNA is intronic and the other derives from an exon, e.g. in the case of :doc:`CNAG_12256 </../supplemental/snoRNAs/snr13>` with snR13 (intron) and snR45-U13/U3 (exon). Further, snoRNAs can be split by introns, even when encoded in an intron of a pre-mRNA, for example :doc:`snR50-snR40l </../supplemental/snoRNAs/cnag00458>`.


 
.. figure:: /../_static/images/U14_coalispr_h99_bedgraphs_chr_5_all_reads__uncollapsed__23_libs.png
   :name: u14_hits
   :align: left
   :width: 1200 px
   :height: 900 px
   :scale: 30%
   :figwidth: 50%
   
   **Figure 12** snR190 and U14 derive from introns of *Argininosuccinate synthase* in *Cryptococcus*.



In yeast and higher eukaryotes, acetylation of rRNA nucleotides by Kre33 (NAT10) is guided by box C/D snoRNAs, snR4, or snR45 (U13) [Sharma-2017_]. In *Tremellomycetes*, the role of snR45 could be regulated or implemented by two different snoRNAs (:ref:`snr45u13` and :doc:`supplemental/snoRNAs/ascnag12486`), each providing a separate guide region for attachment to the substrate. The first snoRNA, (:ref:`snr45u13`) has a homologue (:doc:`supplemental/snoRNAs/u3`) and both snoRNAs fit the Rfam signature for U3, despite a major variation in the secondary structure: the 5' leader sequences upstream of the C-box in these snoRNAs from *Tremellomycetes* are quite different from U3 in baker's yeast and its homologues where a well-conserved helical region confers a base-pair interaction with 18S rRNA. Maybe in *Tremellomycetes* the roles for snR45 and U3 have been divided over the U3-like molecules and :doc:`supplemental/snoRNAs/ascnag12486`.

For some snoRNAs, for which no counterparts in other organisms were identified, no obvious base-pairing target could be identified. For example :doc:`supplemental/snoRNAs/cnag12093` is well-conserved among *Tremellomycetes* [#kwo]_ but putative targets did not reflect this conservation at the level of base pairing to the snoRNA guide. Methylation involves dynamic, short-lived base-pair interactions which might be hampered by stretches of sizable complementarity. As only relatively long guides (>13 bp) were checked for homology, it is possible that biological partners have been missed. For some loci, association of the snoRNA with pre-mRNA was possible nearby splice junctions or a branch-point. Provided these RNAs are able to interact, this could imply a side effect of the presence of this snoRNA on storage or processing of splicing intermediates in *Cryptococcus* (e.g. for :ref:`L30e <cna02220-align>`).


|

Conclusion
----------

By incorporating negative controls in bioinformatics analysis of high-throughput datasets we could easily identify meaningful signals and obtain count data without relying on a reference with annotated regions. By doing so, it was possible to assess the variability between libraries, which exemplified difficulties inherent to common practices when applied for the comparison of small RNA-seq data. We demonstrated that coverage and abundance of ribosomal RNA fragments (rRFs) and other abundant ncRNAs are comparable between negative and positive datasets to such an extent that no biological meaning can be assigned to their co-purification with Argonaute proteins. In general, because the amplification steps during high-throughput sequencing elevate the levels of non-specific RNAs and intensify the background signals, the occurrence of rRFs or other abundant RNAs in co-purification studies require careful evaluation with respect to their biological significance; such observations might actually be highly 'unlikely' [Esteban-Serna_] and should be checked against sequencing data obtained for appropriate negative controls (especially when the RNA-input appears to be 'clean') as shown here.


Although not providing information relevant for the biological system under study, negative datasets can help to annotate highly abundant RNAs and assess their roles. The RNA-Seq results for *Cryptococcus* species, combined with phylogenetic comparison, guided identification of a large number of snoRNAs and other ncRNAs present in these and related fungi. Many of these RNA molecules are processed from intronic sequences spliced from protein-coding pre-mRNA transcripts as found in higher eukaryotes. Novel is that some snoRNAs are derived from non-coding transcripts that are spliced but only carry sequences with significant evolutionary conservation within their introns. In these cases the precursor is functional, not the annotated spliced transcript. 

At the basis for these insights was the Python application |prgnam| we developed to process small RNA-Seq data for various organisms. By means of negative control data, the program provides a systematic approach to separate reads of putative biological relevance from those that form unspecific background. The program makes explicit what mostly remains hidden in experimental practicalities, the biologists' technique to remove noise from signals.

|

.. figure:: /../_static/images/overview_ed.svg
   :name: summaryfig
   :align: center
   :width: 1522 px
   :height: 411 px
   :scale: 60%


|
|
   
.. toctree::
   :maxdepth: 1

   supplemental/otherRNA/srp
   supplemental/otherRNA/u1snrna
   supplemental/otherRNA/rnasep
   supplemental/snoRNAs/boxcd
   supplemental/snoRNAs/u14
   supplemental/18s-tab
   supplemental/snoRNAs/haca_list

|
|

.. figure:: /../_static/images/qr_img.png
   :name: bioRxiv-access
   :align: right
   :width: 284 px
   :height: 324 px
   :scale: 40%

Download essay
--------------

The essay including supporting materials can be found as a paper at bioR\ |chi|\ iv `https://doi.org/10.1101/2024.10.08.617225 <https://doi.org/10.1101/2024.10.08.617225>`_

|
|

=====

Notes
-----


.. [#sele] 'Selective' will be understood to be any method, like size-selection, :term:`RIP` or its crosslinking variants [#cracclip]_, that enriches a particular subset of all the RNA available in a cell. Because of the selection, information with respect to a possible 'constant', unaltered population of transcripts can be lost. If this is the case, normalization becomes difficult.
.. [#siamp] Amplification of siRNAs in fungi involves reverse transcription of the target RNA by RNA-dependent RNA-polymerase (RDP), followed by dicing the double-stranded product and the final association of single-stranded small RNAs with Argonaute proteins. 
.. [#geofish] Experimental, high-throughput sequencing data is commonly published by molecular biologists in a processed form within research articles describing their topic of interest. The raw data is often deposited in public repositories like the Gene Expression Omnibus (`GEO <https://www.ncbi.nlm.nih.gov/geo/>`_) database, which enables re-analysis or meta-analysis, when novel insights derived from the overlap between various independent data-sets are sought for.
.. [#amat] Being self-taught programmers, this analysis serves as an illustration and proof of principle. Mathematicians and more experienced programmers can easily extend and improve the program.
.. [#offs] For example enzymes driving biochemical reactions can lose their activity when these are subjected to too many freeze-thaw cycles. Long-time storage of RNA dissolved in water at -20 :sup:`o`\C will lead to degradation of the molecules, and makes them unsuitable input for RNA-Seq. RNA is ideally kept in 70% ethanol or at -80 :sup:`o`\C.
.. [#src] The program is published at `codeberg.org/coalispr <https://codeberg.org/coalispr/coalispr>`_. All figures are from the documentation for |prgnam|, especially the :doc:`/howtoguides` and :doc:`/tutorials`.

   ..   Github: `github.com/brobr/coalispr <https://github.com/brobr/coalispr>`_. `pypi.org <https://pypi.org>`_ and 

.. [#massspec] Sequential mapping of libraries to sequences known for rRNA, tRNA, other structural RNAs, etc. can remove reads that are not of interest. In a kind of analogous way, common contaminants of mass spectrometry are `filtered from results <https://doi.org/10.1016/j.jprot.2013.02.023>`_, like `keratin <https://www.alphalyse.com/proteinanalysisblog/2016/06/03/protein-contaminant-mass-spec/>`_. 
.. [#alt] Another common approach, especially for biological systems that are hard to genetically manipulate, is to compare data from RNA seq between wild-type cells and cells where the RNA-binding protein of interest has been knocked down or deleted. Absence of coverage in the data for the knock-down cells point to RNAs specifically binding to the deleted protein. The dataset of the mutant defines the negative control, while the positive dataset is linked to the wild-type condition.
.. [#cracclip] In the CLIP_ [Ule-2005_] and CRAC [Granneman-2009_] protocols UV crosslinking is used to create permanent chemical bonds between interacting protein and RNA molecules allowing for very stringent protein purification under denaturing conditions (see also [Hafner-2021_]).
.. [#clash] CLASH [Kudla-2011_] is a comparable approach to CLIP_ [Ule-2005_] and CRAC [Granneman-2009_] but aims to identify RNA-RNA interactions that occur via the RNA crosslinked to the protein of interest. For this, CLASH includes a ligation step in which base-paired or nearby RNA molecules are enzymatically connected. After linkage, the isolated RNA molecules will form 'hybrids': one half mapping to another genomic location than the other half.
.. [#chrdiff] There are pragmatic reasons for this. Only bedgraph data per chromosome can be displayed to keep zooming in/out to a minimum. Chromosomes will differ in length. Bins have a defined size and if chromosomes are not kept apart, some bins relate to sequences from different chromosomes, which interferes with keeping their data apart for display.
.. [#bins] Bin size can be set in configuration files of the program to, say, 50 bp. The nucleotide-resolution of the input data will thereby reduce but this is compensated for by an improvement in speed due to a decrease in memory usage. The binning and comparisons are done with Pandas_, a Python_ module. Note that |prgnam| complements genome browsers that allow zooming to 1-nt resolution by the ability to display, with ``coalisprs showgraphs``, a much larger number of 'tracks'.
.. [#vect] Converting an algorithm from operating on a single value at a time to operating on a set of values at one time.
.. [#genbr] |prgnam| is not intended to replace a genome browser as IGB_ or IGV_; it works and is used in parallel (see :doc:`tutorials`).
.. [#sirns] Shown are traces for chromosome 8 of *Cryptococcus neoformans* H99 based on published siRNA libraries ([Dumesic-2013_], [Burke-2019_]); a ~6-fold difference was set as the threshold between specific and unspecific reads. The negative controls are mutants carrying a deletion for the sole Argonaute gene (*AGO1*) or the gene for RNA-dependent RNA polymerase (*RDP1*).
.. [#settgs] Parameters that can be checked (by ``coalispr info``) and altered (by changing configuration files and ``coalispr setexp``) to determine sensitivity in what is called :term:`specific` or :term:`unspecific`. On the right, illustration of regions observed in the case of siRNAs in *Cryptococcus*.

   .. figure:: /../_static/images/program_settings_wide_ed.svg
           :name: sttngspap
           :align: left
           :width: 3200 px
           :height: 1593 px
           :scale: 20%
           :figwidth: 100%


.. [#serds] Currently, only the counting of single ended (SE) reads has been implemented.
.. [#htsq] For example, counting with HTSEQ_ [Putri-2022_] goes via 'features' described in annotation files. In absence of such a file, these can be prepared by manually scanning bedgraph traces in a genome browser like IGB_ and copying genome coordinates over to a text file and name these regions. From this file a GTF can be constructed with a feature useful for counting (see tutorial for :doc:`/tutorials/h99`).
.. [#collps] The ``pyFastqDuplicateRemover.py`` script in the pyCRAC_ package [Webb-2014_] is used for read-collapsing in the tutorials that come with the |prgnam| documentation. Mapping of the cDNA-sequences in the resulting fasta files can be done with the STAR_ aligner [Dobin-2013_].
.. [#mmusttg] An ~8-fold difference was set as the threshold between specific and unspecific reads. Traces for all 8 samples are shown. 
.. [#libcnts] Library counts by ``coalispr showcounts -lc 1`` [#mmusttg]_.
.. [#lencnts] Length counts by ``coalispr showcounts -lo 1`` [#mmusttg]_.
.. [#mirtrg] According to the miRDB_ [Chen-2020_], 'Wtap' is predicted to be targeted by 154 miRNAs in mouse.
.. [#mirns] Bedgraph traces by ``coalispr showgraphs -c chr17 -w2`` [#mmusttg]_. Gene annotations illustrated in the tracks in between the panes for reads mapping to the plus strand (top panel) or minus strand (bottom panel) by coloured bars are from GTFs extracted from the general annotation file for common non-coding RNA (red), miRNAs, that may bind to AGO2 (amber) or putative miRNA-targets [#mirtrg]_ (black). The grey-blue bars in the middle track ('segm') indicate regions that have been counted. The base-line (2\ :sup:`4`\) reflects the base-level above which signals are considered. 
.. [#rrn] The annotation (`gencode.vM30 <https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M30/gencode.vM30.chr_patch_hapl_scaff.annotation.gtf.gz>`_) seems incomplete: chromosome 17 (40157244-40159092) shows up as the one with the 18S rRNA region. No results for 28S or the precursor 45S. While 5.8S is normally fused within the 45S pre-rRNA in between 18S and 28S, it is annotated on chromosomes 6 (94803762-94803904) and 18 (73666474-73666621).
.. [#annot] Outputs of ``coalispr annotate``  (left) for specific reads (top) and unspecific reads (bottom) compared to diagrams obtained with ``coalispr showgraphs -c chr7 -r 3268365-3270435`` or ``coalispr showgraphs -c  chr14 -r 115280625-115282725`` (right). Note that rRFs form the majority of counted reads in the unspecific dataset (bottom left, row 1), on a par with the specific counts for a miRNA cluster on chromosome 7; only the top section of the tables are shown.

   .. figure:: /../_static/images/annots_mouse.png
      :name: mmu_annots
      :align: left 
      :width: 2706 px
      :height: 1160 px
      :scale: 24%
      :figwidth: 100%

      Mouse count data annotated and compared to traces for miRNA clusters on chromosomes 7 or 14.
   
.. [#mucontr]  Especially when crosslink samples have been processed in parallel and the cDNAs were amplified and sequenced under identical reaction conditions, the resulting datasets can function as negative controls for each other. Identical reaction conditions can be achieved when cDNAs are made in the same reverse-transcription reaction (with differentiating, 5' bar-coded adapters ligated to the RNAs) and form one mix that is submitted for sequencing. Because of high sensitivity of RNA-Seq, cross-contamination can occur [#crosscon]_.
.. [#crosscon] The relative increases of Puf6-signals for the Kre33-specific 18S segment (and vice versa for the Kre33 trace over the Puf6-region in 25S) is probably due to cross-contamination when these samples were prepared in parallel and processed within the same RT and sequencing reactions. For other preps, in which Kre33 and Puf6 crosslinks were separatedly assessed, these overlaps were not observed.
.. [#mutsev] A kind of positive control for monitoring crosslinked RNA fragments are single nt deletions (for CRAC) or mutations (for CLIP) that will be common for crosslinked uracil residues. These mutations reflect reverse trancription mistakes caused by remnants of amino acid adducts on a crosslinked residue.
.. [#h99tut] See also the tutorial ':doc:`/tutorials/h99`'. 
.. [#splic] In their seminal paper of 2013, `Dumesic et al.`_ proposed that in *C.*\ |nbsp|\ *neoformans* H99 a pre-mRNA was either spliced or redirected to the RNAi machinery, which was based on the observation that many siRNAs mapped to introns. The annotation file they had used must have been a premature version, as almost all siRNAs actually align to exon sequences described in GTFs published since, including those (`H99-2014 genes`_) for the original genomic sequence of this fungus [Janbon-2014_]. For example, one of the signature genes in [Dumesic-2013_], CNAG_07721, has been :ref:`re-annotated <cnag7721to03231>`, with this chromosome 8 locus [#locus]_ renamed to CNAG_03231. In *C.*\ |nbsp|\ *deneoformans* JEC21, siRNAs also align to exons [:ref:`van.Nues-202? <vnues202x-publ>`] and for both fungi siRNAs crossing splice junctions (retrieved after STAR_ mapping) were identified as shown in the section on :doc:`/tutorials/H99/rde1-6xN_rde2-7xN` as part of the :doc:`tutorial </tutorials/h99>` for *C.*\ |nbsp|\ *neoformans*. These findings demonstrate that RNAi acts on spliced transcripts and thus downstream of (instead of parallel to) splicing. Of course, retained introns might trigger RNAi against transcripts, but most likely not in the sense described by [Dumesic-2013_].

   .. figure:: /../_static/images/dumesicCNAG_03231.png
      :name: cnag7721to03231
      :align: left
      :width: 2179 px
      :height: 1509 px
      :scale: 18%
      :figwidth: 100%


           
      *C.*\ |nbsp|\ *neoformans* siRNAs target exons, not introns.

      | Left: Comparison of Fig. 1E from `Dumesic et al.`_ to STAR_-aligned data from [Dumesic-2013_] and [Burke-2019_] and GTF annotations from [Janbon-2014_] and [Wallace-2020_].
      | Right: Chromosme 8 context of CNAG_03231 and RNA-Seq by [Wallace-2020_] for wild type (H99) and strains with an *AGO1* deletion (:raw-html:`&#x0394;`\ Ago1; Top). Skipped introns have canonical splice site sequences (*GU..AG*; Bottom).
      |

.. [#ribfail] Intron retainment is often treated as alternative splicing, that can result in messages with premature stop-codons. Other characteristics of mRNAs could affect translation and instigate stalling and breakdown of ribosomes, like rare codons, particular secondary structures, or stop-codon readthrough.
.. [#locus] The assessment that CNAG_03231 was previously called CNAG_07721, is based on genome coordinates provided for RNAs that mapped to CNAG_07721 by Kim et al. [Kim-2014_] in their supplementary `Table S4`_ (sheet 3, entry 123):

  .. table::

        +-----+-------------+------+------------+--------+--------+--------+--------------------------------+
        | no  | Feature ID  | DMSO | Chromosome | Strand | Start  | End    | Function                       |
        +=====+=============+======+============+========+========+========+================================+
        | 123 | CNAG_07721  | 1.20 |          8 | plus   | 399834 | 400159 | conserved hypothetical protein |
        +-----+-------------+------+------------+--------+--------+--------+--------------------------------+

.. [#rDNAcneo] In *Cryptococcus* the rDNA is on chromosome 2, on the minus strand. As shown below, :term:`rRFs` are common to all samples. In some strains, including the wild type (from [Dumesic-2013_]), reads are mapped that are antisense to the rRNA. Can these be the result of an RNAi response? Or are they generated by another, possibly artefactual mechanism?


        
   .. figure:: /../_static/images/rDNA-H99.png
      :name: rdn_h99pap
      :align: left
      :width: 2285 px
      :height: 1216 px
      :scale: 30%
      :figwidth: 100%
   
      *C.*\ |nbsp|\ *neoformans* rDNA locus.


      Reads representing :term:`rRFs` are abundant in all samples of [Burke-2019_; Dumesic-2013_] and cover the complete rDNA to a comparable extent in the controls (top left) and mutants. In some clones, but not all, reads complementary to rRNA are formed. For the rde1Δ (top mid) and rde2Δ (top right) strains these reads counter LSU (5.8S and 25S) rRNA regions, while in wild type (top left) or rrp6Δ (bottom mid) the SSU (18S) rRNA region and flanking transcribed spacers are targeted. No effect is visible for strains without Rde3, Rde4 or Rde5 (bottom left) or in strains lacking DNA or histone methylation activity (bottom right). Although a contamination with rDNA might have caused this, the signals are typical for the various strains and could have another source of origin. Note the rRNA peaks of the reference RNA-Seq libraries that run off the scale (black). Traces for all reads are shown (with: ``coalispr showgraphs -c2 -w2`` ).
.. [#bdgr] Note that in |prgnam| bedgraph traces are compared primarily for genome coverage (reads that overlap a :term:`nt` position in the reference genome) and that signal height is taken as a secondary parameter [#settgs]_.

.. [#cdnalib] Efficient synthesis of cDNA depends on a couple of factors. The amount of substrate for the reverse transcription tends to determine how well the reaction proceeds. Specific RNAs (i.e. binding to the protein of interest with which the RNA has been co-purified or in the exact range of the sizes isolated from gel) can be in low abundance. In that case, the concentration of attached adapters priming cDNA synthesis will also be low, leading to reduced yields of specific cDNAs and enhanced amplification of contaminating molecules during the subsequent PCR step and sequencing. A way to improve on this is by increasing specific RNA input. This can be achieved by mixing various RNA isolates after linking the adapters so that more substrate is available in the reaction. Another advantage of this approach is that purification of the cDNA libraries will represent a single event rather than a number of independent events (in the case of separate cDNA reactions) that could proceed with variable efficiencies. Such an approach depends on the incorporation of barcoded 5' end adapters and is used during prepartion of CRAC libraries [van.Nues-2017_, McKellar-2020_]. In the case of independent libaries, made from independent reverse transcription reactions [Dumesic-2013_, Burke-2019_], a large variability is observed:

   .. figure:: /../_static/images/input-counts-H99-all.png
      :name: input_h99_libspap
      :align: left
      :width: 2399 px
      :height: 627 px
      :scale: 30%
      :figwidth: 100%
   
      *C.*\ |nbsp|\ *neoformans* libraries, mapped (stranded) vs. unmapped reads.
    
      | Uncollapsed read data on the left, collapsed data (cDNAs) on the right.
      | (with ``coalispr showcounts -rc``)
      |

.. [#prop]  Maybe because the mathematicians involved cannot explain the method to the lay audience of molecular biologists? The available literature does not provide an easy way in, nor are major proponents able to offer more insightful advice than to 'reach out to a bioinformatics core research group at your university'.
.. [#idncrna] The sequences of non-coding transcripts were copied and analyzed as described in :doc:`/supplemental/snoRNAs/boxcd`. 
.. [#kwo] For example, this snoRNA was not found in *Cryptococcus Skinneri*, or most *Kwoniella* species despite homologues for other snoRNAs were identified in their sequenced genomes.

|
|
   

