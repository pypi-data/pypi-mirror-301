.. meta::
   :keywords: pyCRAC, CRAC, kinetic CRAC

.. include:: /properties.rst
   
About
=====

Analysis of small RNA-sequencing data
.....................................

Having mostly spent research time at the bench doing experiments with baker's yeast and the lower-intestine bacterium *Escherichia coli*, the author gained experience with high-throughput sequencing when working with Sander Granneman. They produced cDNA libraries from RNA that could be covalently bound to a protein of interest by irradiating growing cells with UV. To facilitate bioinformatics analysis of the results, Sander had put together the pyCRAC_ suite. Often they liked to know what portions of pre-ribosomal RNA was bound to ribosomal processing factors, for which the cross-linking technique [Ule-2005]_ had been initially designed [Granneman-2009]_. To follow the rapid cellular RNA-response to sudden environmental changes, the Vari-X-linker_ was developed in collaboration with UVO3_. This machine and protocol made it possible to perform cross-linking during a defined time series [van.Nues-2017]_ [McKellar-2020]_. The technique was applied for compiling various data collections, some as part of a collaboration, [Lemay-2016]_, [Gerhardy-2021]_ and [Sharma-2017]_. Many of the datasets had been prepared simultaneously, which facilitated to observe variations in RNA populations specific for the bait protein despite a fair level of background, especially when hits for rRNAs, tRNAs and snoRNAs were compared.

Funding ran out and the author went on to establish the opportunistic pathogen *Cryptococcus deneoformans* as an alternative model organism in the fission-yeast lab of Liz Bayne. The research was funded by grants from The University of Edinburgh and the Wellcome Trust [Bayne-2016]_. The initial aim was to set up genetic analysis and to delineate the workings of the RNAi machinery in *C.*\ |nbsp|\ *deneoformans*. RNAi is complicated in this fungus by the presence of two Argonautes (Ago1, Ago2) and two Dicers (Dcr1, Dcr2), begging the question whether these proteins have redundant or differentiated roles. There was no experience in the lab (or department at that time, April 2016) with this organism and many techniques applicable to budding or fission yeast were inadequate to genetically modify *C.*\ |nbsp|\ *deneoformans*. Eventually, being able to transform cells thanks to the advice of Brian Wickes and Xudong Zhu and by combining their split-marker approach [Fu-2012]_ and CRISPR/CAS system [Wang-2016]_, the author managed to obtain epitope-tagged strains that allowed analysis of siRNAs associated with either Argonaute. The tagged strains also facilitated the identification of two other proteins not previously known to participate in fungal RNAi. Biochemical analyses of purified RNAs and proteins, a plate-based transposon-trapping assay [#trap]_ and high-throughput sequencing of siRNAs [#scoy]_ for many [#libsno]_ deletion and reconstitution mutants provided evidence for various findings that were summarized in a manuscript [:ref:`van.Nues-202? <vnues202x-publ>`], and have been presented on a poster at the annual meeting of the `RNA society <RNAsoc>`_ [#onl]_. Results of the work helped to obtain grants *Understanding mechanisms of small RNA mediated silencing* [Bayne-2016]_, *Mechanisms and roles of RNA interference in Cryptococcus neoformans* [Bayne-2017]_, *Mechanisms of Argonaute function in the human fungal pathogen Cryptococcus* [Bayne-2023]_. 
Count numbers had been generated in a traditional manner with HTSEQ_ but could in principle be obtained by very crude scripts the author had been trying out at the time. Development of |prgnam| was seriously taken on by the author together with writing the documentation after his research contract ended in May 2021.


|prgnam| was initially developed in spare time as a proof of principle; it is good to have a hobby not immediately addressing daily work practice. Having tried programming in Java (around 2000) and being involved with Linux [#linx]_, the author picked up on the enthusiasm of Sander Granneman for Python as a tool for data analysis. Learning pyCRAC_ and a course on *Python for Biologists* by `Martin Jones <py4bio_>`_ introduced the author to Pandas_. But to learn programming one needs a topic and sufficient motivation. Since the days of analyzing CRAC-libraries the dream was to have a tool that would filter out background by mimicking a kind of 'visual subtraction' of noise from signals as happens when wet-scientists assess their experimental results by means of controls. The tabular nature of bedgraph data forged the idea that Pandas_ could be used to implement this comparison. The motivation to actually try this came from typical difficulties associated with the analysis of siRNA libraries. First, in the work on *Cryptococcus*, a time-consuming complication of counting reads was that the available methods, apart from being slow when processing a large number of bam-files, relied on a GTF with annotations for transcripts to be counted. For siRNAs these GTFs were not available and had to be compiled manually. This involved careful inspection of bedgraphs in a genome browser and copy-pasting genome coordinates of regions covered by :term:`specific` reads. The second challenge to develop this application stemmed from the practical problem posed by degradation products that tend to contaminate small RNA-Seq datasets. Despite the misleading outcomes that can be generated when this experiential fact is ignored, its relevance is not always appreciated. This became clear after a request, in 2020, to review a manuscript for a high-impact journal. The authors of the report presented a bioinformatics meta-analysis of miRNA-Seq data which felt incomplete because they had not used all available controls [#pap]_. 

Apparently, there could be use for a tool that separates specific from :term:`unspecific` reads. Incorporation of control data formed the starting point of developing this application, which led to a counting method that was not dependent on annotations. Hopefully, the insights |prgnam| can provide (see the :doc:`essay <paper>`: '\ |papertitl|'), makes it worth to have it in the public domain.

.. _siquant:
   
Quantification
..............

Quantification of RNA sequencing data is difficult. At the heart of this problem lies the compositional (or relative) nature of the count data: counts need to be treated in relation to the mixture of reads in a sample [Quinn-2018]_. This is inherent to the method by which libraries are generated and equal for small and mRNA-sequencing approaches. This implies that variation in read signals need to be taken as variation in proportions. Looking proportionally at RNA sequencing data by compositional data analysis (CoDa_, [Quinn-2018]_, [Quinn-2019]_) is, however, not generally done. Most methods take read counts as they are and try to normalize these to some standard.

Many bioinformatics tools are directed at detecting relative changes in protein-gene expression, that is of :term:`mRNA` levels. Synthesis of mRNA depends on which genes are actively transcribed. The actual expression profile reflects a response to environmental conditions, like neighbouring cells, exposure to particular chemicals, hormones, intruders like viruses, or when parameters fluctuate, like temperature, acidity, or intracellular energy or nutrient levels. Upon a change in condition some sets of genes are turned off, others activated, while expression of a large set remains relatively constant. Any change in gene-expression is accompanied by chemical modification of the DNA or of histone proteins covering the region.

Differential expression (DE) of genes seems measurable in mRNA seq data because of a large set of apparent constant transcripts. That a group of transcripts can be taken to form a base-line relies on the finding that the particular differences in experimental conditions did not affect the relative level of these transcripts. The group of 'constant' transcripts is thus dependent on context and will have other members when cells respond to other changes in the environment. For example, nitrogen starvation hugely affects processes (ribosome biogenesis; ribosome degradation) involving transcripts (mRNAs for r-proteins) that could be forming the standard under other conditions. 

Some popular quantification methods (like DESeq2_ or EdgeR_) rely on such a base-line. Further, for dealing with large variations that can be present in RNA sequencing data, these tools demand a sometimes practically unrealistic [#rpts]_ number of biological repeats (over 5 per sample) to gain statistical relevance.

Approaches developed to quantify differential gene-expression are not suitable to assess relative changes in siRNA read-numbers between RNA-Seq libraries. Formation of siRNAs, other than miRNAs that are controlled by gene-expression, seems to occur in response to some change in cellular exposure to harmful nucleic-acids, like invasive viral RNA or transcripts from transposons. Therefore, there is no internal reference, a base-line, that can be decided on. By lack of evidence that siRNA levels are reflecting a regulated process like gene-expression, it can be assumed that a change in siRNA levels could be the result of a stochastic event specific for a group of cells. A change in siRNA levels could reflect an immediate response triggered by conditions peculiar to the (history of a) strain. Observed differences between biological replicates might be an indication for this ([:ref:`van.Nues-202? <vnues202x-publ>`]). The relatively low number of unique siRNA (target) loci further hampers the evaluation of relevant changes in siRNA levels by DE-analysis, since the strength of the method relies on the large number of genes that are not up- or downregulated after an environmental change. 

Some approaches in assessing small RNA-seq signals take as a base-line the total mapped reads in a library and reads per million (RPM) of these are compared. Bedgraphs, used as input for |prgnam|, are based on such an approach. Direct comparison between bedgraph signals from different experiments is, however, not always possible. When libraries differ significantly in their :term:`coverage` or when differences in the amount of background reads are big, numerical comparison does not seem to be applicable. Size selection of siRNAs cannot evade contamination by equally-sized break-down products of larger molecules like rRNA or tRNA which, due to their abundance, can be responsible for large (but not necessarily equally large) fractions of total read counts (see :doc:`/tutorials`). This makes it difficult to quantify siRNA read-counts by normalization to library sizes, especially when yields of library preparations vary.

|prgnam| does not immediately compare the height of signals - only to meet a particular threshold, 2\ :sup:`LOG2BG`; see :ref:`here<lg2bg>`, above which a signal is taken into account. Instead, mainly the coverage is evaluated, the presence of a mapped read at a genomic locus.  For specific signals the coverage is concentrated and forms a peak, especially in comparison to smeared out coverage of random background signals. However, for abundant contaminants, concentrated coverage peaks will be present. Only when such peaks overlap with peaks in the :term:`specific` samples, the height of the signal is taken into account and then in the sense that the signal has to be much larger (10\ :sup:`UNSPECLOG10`; see :ref:`here<unspclg10>`) in the specific sample to be counted (Not being a trained mathematician, the manner in which such peak-differences are assessed is open for improvement). 

The main aim of |prgnam| is to sort signals from noise (reads that can be seen as contaminants/background). Peaks are specified as :term:`specific` and :term:`unspecific` and this process can be followed by comparing output :term:`tsv` files or visually, using ``coalispr showgraphs`` (see :ref:`here<shwgr>`). The specified reads are then counted and these counts can be used for further analyses. Read-counts can be indicative for the quality of libraries and general experimental outcomes, which can be visualized with ``coalispr showcounts`` (see :ref:`here<shwcnt>`), while specific genomic sections can be assessed with ``coalispr region`` (see :ref:`here<regi>`). Examples are shown for assessing length distributions of siRNAs in the :doc:`/tutorials`. 

|
|
     
=====

Notes
'''''
.. [#trap] In order to better identify separate transposition events, the author developed a plate-based version of the approach with liquid cultures by [Gusa-2020]_.
.. [#scoy] Some of these sequencing results were used in [Scoynes-2022]_ but without a source reference while GEO accession numbers had been available under GSE178393_ since June 2021.
.. [#libsno] More than 100 siRNA manylibraries were sequenced and deposited at GEO.
.. [#onl] This conference was completely online in 2021 due to the Covid pandemic. 
.. [#linx] All files of the project have been produced with open source applications. Figures were made with Inkscape_ and GIMP_; code was written with Geany_, SciTE_, or Mousepad_; the documentation with GVim_ (in Restructured Text using Sphinx_ and the Furo_ theme). Software development was on a Clevo_ N750HU (from `PC Specialist`_) with an Intel_ Core i7-7700HQ CPU @ 2.80GHza and 32 GB RAM, running Slackware_ linux 64bit with a.o. Python_, Numpy_, Pandas_, Matplotlib_, Pysam_, and other software obtained via slackbuilds.org_.
.. [#pap] The authors argued that biochemical data for the **input** RNA samples provided sufficient evidence for reliability of the used sequencing information, thereby overlooking the possibility that background in biochemical data can end up with relevant count numbers after RNA-Seq (also see :doc:`/tutorials`).
.. [#rpts] Smaller groups with restricted financial resources, man-power or available time can often not afford this number of repeat experiments.


|
|
|
|
|

.. _`vnues202x-publ`:

.. rst-class:: asfootnote

van.Nues-202?
'''''''''''''
.. rst-class:: asfootnote

This reference relates to experimental data, summarized in a poster and an unpublished manuscript by van Nues RW, Scoynes C, Mukherjee A, Henry S, Spanos C, and Bayne EH. 

.. rst-class:: asfootnote

All remarks referring to the author's experience with studying RNAi in *C.*\ |nbsp|\ *deneoformans* JEC21 have to be treated as 'personal communication' and 'data not shown'. 




