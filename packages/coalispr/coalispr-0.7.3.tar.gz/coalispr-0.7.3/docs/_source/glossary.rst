.. include:: /properties.rst

.. _glossar:

Glossary
========

.. glossary::
   :sorted:

   **Ago**
       'Ago' or 'AGO' are abbreviations for Argonaute proteins involved in RNA silencing (:term:`RNAi`). By complementarity of the small guide RNA (:term:`siRNA`, :term:`miRNA` or piRNA) they are complexed with, Argonaute-like proteins can find and bind to target RNA molecules.

   **background**
       What is background or noise in an (:term:`immunoprecipitation`) experiment? Why does this form a smear on an image showing molecules according to length? Protein and associated RNAs are isolated from extracts, which are soups remaining after clearing cellular debris from smashed-up tissue or whole cells. Conditions are chosen that keep most molecules intact, but cannot prevent that extracts contain fragments of large complexes or very long molecules that get broken in the process. 

       The immunoprecipitation procedure can be compared to fishing with a worm on a hook. This activity can pull out objects that, in contrast to fish, do not go after the worm but just get hooked (like seaweed, twigs, fishing gear, shopping bags or bicycles thrown into a canal). Similarly, molecules can hold onto reagents (like the beads antibodies are linked to) or materials (plastic tubes and pipette tips) they come into contact with during the preparation. Despite steps to wash away ingredients of the extract that do not have specific affinity to the antibody, the clean-up will never be complete and some of the ‘sticky’ molecules will be part of the immunoprecipitate from which the RNA is purified. 

       RNAs in the background, due to the chance-event they originate from, are of undefined length, yielding the :term:`smear`. Especially when such fragments are derived from very abundant cellular complexes like translating ribosomes, sequencing reads representing genomic regions of rRNA, tRNA, or highly expressed mRNA will form peak signals in mapped sequencing data.
   
   **bam**
       Bam files are sequence alignments using the SAM_ format and are readable by Samtools_ or Pysam_ when they have been sorted and indexed (in a ``.bai`` file). They are compressed binary versions of Sam files and the primary output of read mappers like STAR_. Bam files are the kind of alignments countable by |prgnam| and form the input for generating :term:`bedgraph` files. A SAM alignment contains 11 required fields, and can have extra SAM-tags (or 'SAM-attributes'), like ``NH``, ``HI`` and ``nM``, which are used during read counting. If Samtools has been installed, Bam-alignments  (as produced in the :doc:`/tutorials`) can be checked on the command line by ``samtools view samtoolsAligned.sortedByCoord.out.bam | less``. Field ``6.``, the :term:`CIGAR <cigar>` string, is used for counting intron-like gaps and to skip imperfect alignments (like the last one with a deletion ``12M1D11M``) when reads are not derived after RNA_IP of UV-irradiated samples::

        # SAM-tags 1.           2.      3.      4.      5.      6.        7.      8.      9.      10.                      11.                       Optional
        # QNAME (query name)    FLAG  RefNAME   POS     MAPQ    CIGAR     Mate    MPos    TLen    SEQ                      QUAL                      Number    Hit      Alignm.   number of
        #                                                                                                                                            of Hits   Index    Score     Mismatches  

        SRR646636.10466082      0       1       972     255     23M       *       0       0       TGTTATTCTTCGACATTGTTTGT  GGGGGGGGGGGGGFGGGGGGGGF   NH:i:1    HI:i:1   AS:i:22   nM:i:0
        SRR646636.20241186      0       1       972     255     23M       *       0       0       TGTTATTCTTCGACATTGTTTGT  E?DEEEE?EEEDDED>CAAAC6C   NH:i:1    HI:i:1   AS:i:22   nM:i:0
        SRR646636.1090240       16      1       1186    3       17M       *       0       0       CCAGCTCCCAATCCAGA        GGGGGGGGGGGFGGGGG         NH:i:2    HI:i:1   AS:i:16   nM:i:0
        SRR646636.1992179       16      1       1186    3       23M       *       0       0       CCAGCTCCCAATCCAGAGGTGCA  D=D6D:D=@@>@>=B?C=DD?DD   NH:i:2    HI:i:1   AS:i:22   nM:i:0
        SRR646636.18847562      16      1       1186    3       23M       *       0       0       CCAGCTCCCAATCCAGAGGTGCA  ==C<BA5::ACA5B?=DC?D?5D   NH:i:2    HI:i:1   AS:i:22   nM:i:0
        SRR646636.458491        0       1       1187    3       22M       *       0       0       CAGCTCCCAATCCAGAGGTGCA   DDDD=B=DDD=BE=E?DDA?5A    NH:i:2    HI:i:1   AS:i:21   nM:i:0
        SRR646636.18048023      0       1       1218    255     22M       *       0       0       TGCTTTTCCTCCAGAATCTGGA   CCCA?ADB=ADDDDCAEDEEED    NH:i:1    HI:i:1   AS:i:21   nM:i:0
        SRR646636.20947570      0       1       1218    255     22M       *       0       0       TGCTTTTCCTCCAGAATCTGGA   GFEGGGGFGGFGDEGGGFGGGF    NH:i:1    HI:i:1   AS:i:21   nM:i:0
        SRR646636.20414571      0       1       1218    3       12M1D11M  *       0       0       TGCTTTTCCTCCGAATCTGGAGC  DD:DD=?C:CC;>4:4.@/?A::   NH:i:2    HI:i:1   AS:i:18   nM:i:0

       STAR alignment runs can exclude column 11 with quality information from the output by including option ``--outSAMmode NoQS \``, while inclusion of information from SAM tags (``NH HI AS nM`` (Standard) or, ``NM MD jM jI MC ch``) can be specified by the user with ``--outSAMattributes A1 A2 A3 ...`` (see the `STAR manual`_). Note, |prgnam| will not differentiate reads from chimers (supplementary reads).

   **barcode**
       To reduce sequencing costs and enhance efficiency, cDNA-libraries are commonly pooled. This is possible when each library has been synthesized with primers that are identical but for a different sequence at a particular position. This signature is referred to as the *barcode*. Sometimes, primers are synrthesized that contain signatures that are *random*\ nized, facilitating detection of different cDNAs when these were made from separate RNA molecules of identical length and sequence.

   **bedgraph**
       Bedgraphs are tabbed text files with chromosome nucleotide numbers (:term:`seq_id`, *start*, *end*) and a mapped-read value that provides a measure of abundance. Mostly a normalized value (abundance relative to the total input) is given::

        # seq_id  start      end         value

          1	 1185	    1198	0.07742 
          1	 1207	    1229	0.15483
          1	 1577	    1589	0.07742
          ..
          7	 1032652    1032656	0.23225
          7	 1032656    1032688	0.15483
          7	 1032688    1032691	0.30967


       Some aligners, like STAR_, can be instructed to output 'raw' abundance values (without normalization). This is helpful (and relevant in the case for :term:`unselected` reads) when numbers independent of the bam-input need to be used for the calculation.

       The STAR sequence aligner or the pyCRAC_ script ``pyGTF2bedGraph.py`` produce two bedgraph files, one per strand, for each alignment. |prgnam| relies on such stranded bedgraph files as input. Thus, bedgraphs with negative values as described by USCS_ or ENSEMBL_ need to be split over two files, one with all positive values (strand 1, or :smc:`PLUSIN`) and one containing all negative values (strand 2, or :smc:`MINUSIN`) with the sign omitted (see :download:`convert_plusmin_bedgraph_to_plusplus.py</../static/downloads/convert_plusmin_bedgraph_to_plusplus.py>` in ``coalispr/resources/share/``). Parameters in :term:`constant` can be set to the strandedness (:smc:`PLUSIN` or :smc:`MINUSIN`), and the extension (:smc:`BEDGRAPH`) of analyzed bedgraph files. Constants :smc:`PLUS` and :smc:`MINUS` refer to values used by the program to indicate strandedness in processing, representation and names of output files.

   **bin**
       Term to indicate one of the parts a series or length has been divided into. A bin can be of a given length, so that a series has been split in equal segments. This kind of *binning* is used for creating an index for gathering bedgraph data for each chromosome, by splitting the chromosome in sections of equal lengths (:smc:`BINSTEP`). Alternatively, a bin can represent a logical section, say when fragmenting all regions covered by reads in three parts. This will yield sections of inequal lengths between these but representing comparable classes: *start*, *middle*, *end*. Such information might point to preferential coverage of reads, when reads are relatively more or less concentrated in one of these classes.

   **binary numbers**

       Repeating the clear explaination by `Steve Summit <https://www.eskimo.com/~scs/cclass/mathintro/sx3.html>`_:

       .. rst-class:: asfootnote


        The familiar decimal number system is based on powers of 10. The number 123 is actually 100 + 20 + 3  or  1 x 10\ :sup:`2` + 2 x 10\ :sup:`1` + 3 x 10\ :sup:`0`.
 
        The binary number system is based on powers of 2. The number 100101\ :sub:`2` (that is, 100101 base two) is 1 x 2\ :sup:`5` + 0 x 2\ :sup:`4` + 0 x 2\ :sup:`3` + 1 x 2\ :sup:`2` + 0 x 2\ :sup:`1` + 1 x 2\ :sup:`0`  or  32 + 4 + 1  or  37.

        We usually speak of the individual numerals in a decimal number as digits, while the *digits* of a binary number are usually called *bits*.

        Besides decimal and binary, we also occasionally speak of octal (base 8) and hexadecimal (base 16) numbers. These work similarly: The number 45\ :sub:`8` is 4 x 8\ :sup:`1` + 5 x 8\ :sup:`0`  or  32 + 5  or  37. The number 25\ :sub:`16` is 2 x 16\ :sup:`1` + 5 x 16\ :sup:`0`  or  32 + 5  or  37. 

        So 37\ :sub:`10`,  100101\ :sub:`2`,  45\ :sub:`8`, and  25\ :sub:`16` are all the same number.

   **biological experiment**
       An experiment to test a biological system. These experiments rely on (other) biological systems or procedures to function properly. In order to test this, each biological experiment would have a :term:`positive control` (should give an expected result) and a :term:`negative control` (should not give a significant result) to which the outcomes of the actual test-samples (the :term:`mutant`\s) will be compared.

   **biological replicate**
       A sample obtained from a different strain, tested under the same conditions as another sample. During configuration (see :doc:`tutorials`) the naming of samples in the *Experiment file* (:smc:`EXPFILE`) could help to differentiate biological from technical replicates. A `technical replicate` is a repeat of an experiment under the same conditions for the same strain; when using ``wt_1`` and ``wt_2`` for biological replicates, names as ``wt_1a`` and ``wt_1b`` could express that these are technical replicates.

   **cDNA**
       Single stranded, complimentary DNA synthesized from RNA by a reverse transriptase. After :term:`PCR` amplification a *cDNA library* is obtained that forms the input for the next-generation sequencing reactions in :term:`RNA-Seq`. After :term:`collapsing <collapsed>` identical sequencing reads an idea of the number of cDNAs in this library can be obtained. An exact estimation requires random :term:`barcode`\ s to be present in the 5' adaptor that has been fused to the RNA/cDNA during library preparation. 

   **cigar**
       The *cigar string* is the 6th field in each alignment line of a :term:`bam` file. For example the annotation ``2S12M1D5M56N14M``, describes an alignment, after :term:`soft-clipping` a 2 nt overhang (``S``), with 12, 5 and 14 matches (``M``), broken with a large gap of 56 nt (``N``) while one point-deletion (``D``) is needed to get the given sequence aligned against the reference genome. For short siRNAs only a complete match with or without an intron-like gap (i.e. only ``M`` and ``N`` in the cigar of an alignment) are tolerated by |prgnam|. Alignments should be created with sequences from which the adapters have been trimmed and based on an end-to-end mapping instruction (as is possible in STAR_). Then, trimmed overhangs (by soft-clipping), deletions or insertions (``I``) can be taken as indicative for a poor alignment. Note that point-mutations and point-deletions are expected to occur in sequences derived from crosslinked RNA. Further, a mismatch can be present within the stretch that 'matches'. A 'match' (``M``) means that each nucleotide in the aligned section faces a nucleotide in the reference (without skipping or deletion). Thus, ``M`` can cover a mismatch (substitution) which can also be symbolized with ``X`` (with ``=`` for an identical match). STAR handles mismatches by means of ``M`` and SAM-tags ``nM`` (number of mismatches), ``NM`` (number of mismatched + inserted + deleted bases), and ``MD`` (string encoding mismatched and deleted reference bases). Of these tags, ``nM`` is part of the default output and checked during counting by |prgnam|. Which SAM-tag is checked can be changed with :term:`parameter <constant>` :smc:`NM`, while acceptance of point-deletions versus an alignment that fully matches is defined with :smc:`CIGARCHK`, :smc:`CIGPD` and :smc:`CIGFM`; the number of tolerated mismatches can be configured with :smc:`NRMISM`.

   **constant**
       The configuration file for |prgnam| is ``resources.constant.py``, which gets built from text files. A word in capitals in the configuration texts, :smc:`NNN`, forms the name for a constant used to refer to a value, which can be a string of text (``NNN = 'a value'``), a number (``NNN = n``), or a collection (``NNN = ['a', 'b', 'c']``). The value of a constant can be set or changed in the text files (see :doc:`tutorials`). The constant name :smc:`NNN` should remain intact. In this documentation, an inline capitalized word in bold refers to a constant.

   **collapsed**
       Reads that are identical in sequence can be sorted into one, collapsed read with the read-count stored in the read-identifier. The program ``pyFastqDuplicateRemover.py`` from pyCRAC_ can be used for this; its output are :term:`fasta`-files that work as input for a sequence aligner like STAR_. This appoach results in small :term:`bam` files. Collapsing reads speeds up counting enormously. (The 'collapsing' type of bam-files to be counted is set via parameter :smc:`TAGBAM` in :term:`constant`). Note that by collapsing single-read sequences become relatively overrepresented when sequences are counted (say when generating :term:`bedgraph` files from bam alignments); this, however, does not affect the identification of :term:`siRNA` targets (although the anti-sense siRNA peak -with respect to the target strand- becomes less tall relative to the sense siRNA population).

   **corbett**
       In |prgnam| source and configuration files, :term:`siRNA` reads that align to the same locus on the genome but with opposite strandedness are distinguished as *corbett* (:smc:`CORB`) or *munro* (:smc:`MUNR`). In *Cryptococcus*, the most abundant population of siRNAs are antisense to a transcript (the expression of which can become elevated in the absence of RNAi, say in deletion mutants for *AGO1*). These antisense reads, forming the larger peaks, are the *munro* siRNAs. The smaller population of siRNAs, sense to the same transcript, are the *corbett* siRNAs. On a log2 scale, the bedgraph signal representing the number of :term:`uncollapsed` *munro* reads exceeds by far the signals for *corbett* reads, while in the case of cDNAs (:term:`collapsed` reads), the bedgraph signals are far less disparate and on a comparable scale. The large difference between uncollapsed *munro* and *corbett* reads might reflect an amplification of the difference between their :term:`cDNA` populations by the :term:`PCR`-steps during preparation of the cDNA libraries and the sequencing. On the other hand - when no random-:term:`barcode`\ s are available to distinguish otherwise identical cDNAs - it could be possible that more *munro* siRNA molecules represented by the same cDNA were present in the cellular RNA pool, compared to the *corbett* siRNAs. This would mean that a cellular amplification step led to the observed difference between the numbers of uncollapsed *munro* and *corbett* reads.

   **coverage**
       The number of different reads that overlap a :term:`nt` position in the genome. Coverage is directly related to the complexity of a library.

   **csv**
       Common format for text-only data files without any mark-up. In these file the values are separated by commas. For use with |prgnam|, such files will be converted to :term`tsv`.

   **depletion kits**
       Various products to fish out ribosomal RNA (:term:`rRNA`) from RNA input for :term:`cDNA` library construction are evaluated in `articles <https://bmcgenomics.biomedcentral.com/articles/9.1186/s12864-018-4585-1>`_ or `blog-posts <https://www.rna-seqblog.com/ribo-depletion-in-rna-seq-which-ribosomal-rna-depletion-method-works-best/>`_. An on-line search for 'rRNA depletion kits' yields many hits, listing companies like `NEB <https://www.neb-online.de/en/next-generation-sequencing/nebnext-rrna-depletion-kit/>`_, `Illumina <https://www.illumina.com/products/selection-tools/rrna-depletion-selection-guide.html>`_, `PerkinElmer <https://perkinelmer-appliedgenomics.com/home/products/library-preparation-kits/illumina-rna-library-prep-kits/ribonaut-rrna-depletion-kit/>`_, `ThermoFisher <https://www.thermofisher.com/uk/en/home/life-science/dna-rna-purification-analysis/rna-extraction/rna-applications/ribosomal-rna-depletion.html>`_, `Biorad <https://www.bio-rad.com/en-uk/product/sequoia-ribodepletion-kit?ID=QP2V53RT8IG9>`_, `Mgi-tech <https://en.mgi-tech.com/products/reagents_info/15/>`_, etc. Telzrow-2021_ describes methods specially tested for *C.*\ |nbsp|\ *neoformans*.


   **discard**
       Sequence data not used in the overall analysis. Such reads were obtained from experiments that were controls, say an untagged control in a FLAG-\ :term:`IP` or a control for completeness of a biochemical reaction. In spite that input sRNAs (as could have been detected by staining or gamma-labeling and autoradiography) were almost absent, when compared to the other samples, the cDNA libraries for these controls have yielded far more reads than expected. Because of the ambiguity in their origin (contamination, carry-over, a result from :term:`PCR` amplification steps), these libraries have not been used and labeled as :smc:`DISCARD` (:smc:`CAT_D`). A proper :term:`negative control` was a library from a strain in which the biological process under study had been completely inactivated. 

   **epitope**
       A short peptide that is specifically recognized by an antibody during purification of a protein containing or tagged with that epitope. For tagging, the coding sequence for the protein is extended (either at the start or the end) with :term:`codons <mRNA>` that specify a flexible linker and then the epitope. Although short, epitope-tags can be found to interfere with protein function. This happens when their presence blocks residue interactions needed for structural stability, complex formation, or catalytic activity. 

   **extra**
       Sometimes genome features, like the complete 45S rDNA unit for mouse (see :doc:`/tutorials/mouse`), have not (yet) been incorporated in the used references. Other examples where reads can map to regions not present in the genome relate to modification of strains by site-directed mutagenesis. The  high-throughput sequencing libraries analyzed by |prgnam| can be based on RNAs co-immuniprecipated with :term:`epitope`-tagged proteins or isolated from strains carrying disrupted genes. Genetic manipulation of fungi like *Cryptococcus* relies on the introduction of extra-genomic DNA(s) that (can) end up in the genome. The program allows for analyzing reads that map to such extra DNA, when these sequences have been included in :term:`GTF` and :term:`fasta` files used for mapping reads. Such extra sequences are put in an additional chromosome, named :smc:`CHRXTRA` (defined in the :term:`constant` file). This is not a spurious excercise: CRISPR/CAS manipulation of *C.*\ |nbsp|\ *deneoformans* leads to an :term:`RNAi` response targeting the *CAS*-gene, the bacterial-plasmid origin of replication and, especially, the guide RNA defining the recombination target in many of the modified strains!

   **fasta**
       Text file format for storing/reading/saving nucleotide sequences. For DNA, only one strand is shown::

        >seqid
        GATCCCCGATTTGCATGCATGCAGTAGCAGTAGACTAGATCTAGCTGGATCGATGACAGTCGATGACAGTSAGCATCGACAGCTGACAGCTGAGTACAGGAGAGAGATTT

       The output-format of :term:`collapsing<collapsed>` identical sequences in :term:`fastq` files is fasta; the read count is shown after the underscore in the :term:`seq_id` (">SequenceNumber_Counts")::

        >5495_1
        TTGTCGGTTCACATCGGAAGCGCACACGTCTGAACTCCAGTCACAGTTCCAGGGCGGTTTGCGTGTTGTGGTTGCT
        >5496_42
        TTAAGCTGAAGAGCGCTCGGTT
        >5497_17
        TCCACTTCTCGTCTGGGTCTCCC
        >5498_861
        TAAAGTCGATCTGGAACTCTCT
        >5499_1
        CCGAAATCGATGCCTGTAATTTTACCTTGAAAAAATTAGAGT
        >5500_1
        ATACACTCATAGCACAGAACGT
        >5501_6
        TGCGACAGCGAATGAACTGA

   **fastq**
       Text file format for storing/reading/saving nucleotide sequences including quality scores, barcodes. These are generated during high throughput sequencing::

        @NB551016:239:H77GGBGX7:3:11401:13758:1020 1:N:0:TTAGGC
        CACTGGTTGGGACTGAGATCGGAAGAGCACACGTCTGAACTCCAGTCACTTAGGCATCTCGTATGCCGTCTTCTGC
        +
        AAAAAEEEEEEE6EEEEEEEEE66EE/EEEEEAEEEEEEEEAEEEEE/AEEEEEAEE/<AEAEEEEAAEAAA/E<<
        @NB551016:239:H77GGBGX7:3:11401:7589:1021 1:N:0:TTAGGC
        AAGTCGGAATCCGCTAAGGAGTGTAGATCGGAAGAGCACACGTCTGAACTCCAGTCACTTAGGCATCTCGTATGCC
        +
        /AAAAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE/EAEEEEEEAE
      
   **GTF**
       Genome annotation file. A GTF_ consists of a tabbed file with 9 fields::

        # gff-version 2.2
        # seq_id source    feature      start   end     score   strand  frame   annotation

        1	 GenBank   transcript	50077	54254	.	+	.	gene_id "CNA00170"; gene_name "CNA00170"; transcript_id "CNA00170.t03";
        1	 GenBank   gene         50077	54254	.	+	.	gene_id "CNA00170"; gene_name "CNA00170";
        1	 GenBank   exon    	50482	51090	.	+	.	gene_id "CNA00170"; gene_name "CNA00170"; transcript_id "CNA00170.t03";
        1	 GenBank   start_codon	50923	50925	.	+	.	gene_id "CNA00170"; gene_name "CNA00170";
        ..
        7	 GIRI	   gene    	903570	903732	.	-	.	gene_id "LTR11_cn7_903570";
        7	 GIRI	   exon    	903570	903732	.	-	.	gene_id "LTR11_cn7_903570"; transcript_id "LTR11_cn7_903570"; exon_number "1"; gene_source "homology: 163 overlap, 224 score, 0 e-val and 91.411 percent identity";transcript_name "LTR11_cn7_903570"; 
        7	 Wallace   transcript	960561	965976	.	-	.	gene_id "CNG03420-pseu"; transcript_id "CNG03420-pseu"; 
        7	 AE017347  gene  	960561	965976	.	-	.	gene_id "CNG03420-pseu"; 

   **immunoprecipitation**
        IP is a form of affinity purification whereby an antibody bound to inert material (often agarose beads) and specific for an :term:`epitope` tag is mixed with the extract after which the beads are collected, washed and the bound protein or associated RNA are eluted. The protein or RNA are then isolated from the eluate by further biochemical treatments and prepared as inputs for the actual experiments. When specifically the RNA is isolated by means of co-purification with an epitope-tagged protein, this is called RNA immunoprecipitation or :term:`RIP` (RNA IP).

   **IP**
        :term:`Immunoprecipitation` of proteins using antibodies.


   **miRNA**
        A microRNA or miRNA is a single stranded RNA molecule that like a :term:`siRNA` is bound to Argonaute proteins (Ago) and functions as a guide. In contrast to :term:`siRNA`\ s, miRNAs derive from hairpin-like precursors that result from gene-expression and mature in various, well-defined steps to the RNA that is bound by Ago. They are implicated in the regulation of :term:`mRNA` translation and can function as bio-markers (i.e. molecules that are detectable in blood sera) for particular cancers.

   **mRNA**
        Messenger RNA, or mRNA, is a class of RNA molecules that are transcripts from protein-coding genes. They contain an *Open reading frame (ORF)* with the protein-code. In nascent transcripts, ORFs are often interrupted by *introns* that are removed by the *splicing* machinery. Spliced transcripts consist of *codons*, triplets of nucleotides that 'define' the amino acids and their sequence in the protein. Mature mRNAs are scanned by *ribosomes* that combine amino acids brought in by :term:`tRNA`\ s. These transport RNAs recognize the triplets defining the order of amino-acids via complimentarity to their *anti-codons*. Ribosomes 'translate' the message encoded in the mRNA to the chain of amino acids that build a protein.
        
        Many things can go wrong during this process; any splicing mistake interrupts the coding frame and can lead to truncation of the synthesized protein. Incorporation of the wrong amino acid can cause misfolding or different activity of the resulting protein. Such a mutation can occur when the coding/anti-codon complimentarity is close but only partial in the case a shortage of the appropriate tRNA-amino acid allows other tRNAs to occupy the active center on the ribosome. This can also lead to a premature stop of the process. Mis-spliced mRNA and wrongly synthesized proteins can be deleterious to cells and will be degraded in most cases. Mutant proteins that fold into a stable structure or still participate in the cellular biology could disrupt vital processes and trigger aging and disease.

   **multimapper**
       Sequencing reads, especially short ones, can often be aligned to a reference genome more than once. This depends not only on the stringency settings for the mapping. Repeats in the genome occur, like that of telomeres (the protective end-sections of linear chromosomes), or genes for ribosomal RNA (rDNA), :term:`tRNA`\ s, or transposons. When studying :term:`siRNA`\ s, which often are directed against transcripts derived from transposons, multimappers need to be taken into account. For |prgnam| to do so, it is expected that during the alignment (:term:`uncollapsed`) multimapping reads are randomly mapped to the possible loci, and will be counted as 1. :term:`Collapsed` reads are aligned at each possible position (to keep these hits visible in the :term:`bedgraph`\ s) but are counted as ``1/NH`` (with ``NH`` the Number of Hits found in the :term:`bam` alignment line). 

       Thus, multimappers for collapsed and uncollapsed reads are counted differently. The configuration file ``2_shared.txt`` contains fields :smc:`MULMAPCOLL` and :smc:`MULMAPUNCOL` which serve to remind that particular alignment settings are expected by the ``countbams`` scripts. When mapping collapsed reads, find an alignment parameter that does the following: each multimapping read will be mapped to each locus as 1 read (setting ``--outSAMprimaryFlag AllBestScore`` in STAR_ that fits ``MULMAPCOLL = 1``).  During alignment of uncollapsed reads each multimapping read is counted once and randomly divided over loci (setting ``--outSAMmultNmax 0`` in STAR to meet ``MULMAPUNCOLL = 1``).

   **munro**
       Qualification of :term:`siRNA`\ s that are antisense to a transcript targeted by :term:`RNAi` and far more abundant than siRNAs sense to that transcript (:smc:`MUNR`); see :term:`corbett` (:smc:`CORB`).


   **mutant**
       A strain that has been changed genetically, either accidentally or in order to test an effect or role of the modified gene. The experimental test of these changes always include a :term:`negative control` and a  :term:`positive control` for comparison as these form a :term:`required reference or standard <biological experiment>`. To set up experiments, strains will be genetically modified for technical reasons (e.g. introducing epitope tags or deletions that enable future strain construction) and such a strain can be used as a negative or positive control. The :term:`mutant` bears an alteration in the genetic background of a control strain. Heuristically, a mutant in one experiment can be a negative or positive control for another. 

   **negative control**
       A sample, sometimes called 'mock' control, in a :term:`biological experiment` that is not expected to give a meaningful outcome because the biological system under study is inactive in the sample. The mock experiment will show no or a very low background signal, dependent on experimental conditions. When such a sample provides input for high-throughput sequencing, however, the output can still be significant in size due to amplification steps (:term:`PCR`\ ) in the procedure. Despite high count numbers, reads of a negative control do not provide any relevant information and are thought of as :term:`unspecific` :term:`background` or noise.
       
   **NMD**
       Nonsense-mediated decay of :term:`mRNA` harboring premature termination :term:`codons <mRNA>` (PTCs). In mammalian cells NMD is detected in separate, nuclear export linked translation complexes of newly synthesized, spliced mRNA with CBP80 binding to the cap and associated with EJC (exon-junction complex) proteins. These complexes differ from cytoplasmic ribosomes translating eIF4E capped mRNA [Maquat-2010]_. In yeast NMD in pioneer rounds of translation is observed on both kinds of translation complexes [Gao-2005]_.
   
   **noise**
       :term:`Background` signals in experimental results.

   **nt**
       Nucleotide, one bead in the RNA string; for DNA that would be one base pair (bp).
 
   **PCR**
       Polymerase chain reaction is a technique to obtain sufficient material for further biochemical analysis from traces of input DNA. This enlargement, or 'amplification', of the amount of DNA molecules of interest results from multiple rounds of resynthesizing copies of the same DNA fragment.

   **PE**
       Abbreviation for paired-end sequencing data. Both strands of each cDNA are sequenced, giving a forward *read1* and reverse *read2*. The forward strand, reflecting the RNA sequence, is distinguished by strand-specific library construction; for example when different adapters are ligated to the 5' and 3' ends of the RNA-molecules or when first-strand cDNA synthesis is initiated by priming characteristic regions near the 3' end (such as polyA-tails of mRNAs with oligo-dT). Paired reads in PE-bam files have particular values for SAM-fields :smc:`RNEXT` (``=``), :smc:`PNEXT` and :smc:`TLEN' ::

        # SAM-tags 1.           2.      3.      4.      5.      6.        7.      8.         9.              10.       11.      Optional
        # QNAME (query name)    FLAG  RefNAME   POS     MAPQ    CIGAR     Mate    MPos       TLen            SEQ       QUAL     Number    Hit      Alignm.   number of
        #             
          <read1>                              <num1>                     =       [num2]     [num2]-<num1>
          [read2]                              [num2]                     =      -<nnum1>  -([num2]-<num1>)

       PE bam alignements need to be preprocessed to obtain SE versions before reads can be counted with |prgnam|; this is attempted by converting PE to SE but need to omit counting gaps.


   **png**
       Image file format, editable in programs like Gimp_; output is in pixels (see also :term:`svg`).

   **pkl**
       Extension used by |prgnam| for files created by ``python.shelve``. These files consist of dictionary-like objects with strings as keys while the values are binary Python_ objects handled by the ``python.pickle`` module. Text versions of the binary files (and vice versa) can be made with ``coalispr storedata`` to obtain a permanent (and transparent) backup and to accommodate changes in the Python_ environment (the pickle format is tightly linked to the Python_ version used for generating the binary data).

   **positive control**
       A sample in a :term:`biological experiment` that is expected to provide a positive result (meaningful outcome), demonstrating that the biological system under study is functional under the experimental conditions. In a biochemical experiment, this is shown by an obvious signal that conforms to expectations based on the current biological knowledge. In the case of high-throughput sequencing, this sample results in :term:`specific` (as well as :term:`unspecific`) reads.

   **Python**
      |prgnam| is written with the programming language Python_ and makes use of additional libraries Pandas_, Matplotlib_, Seaborn_ and thereby Numpy_ and Numexpr_. Some steps rely on pyCRAC_ and Pysam_. Python source files have the extension ``.py``.

   **RBP**
       RNA-binding protein. Many proteins have been found to be able to associate with RNA, mainly by :term:`RIP`. Aspecific interactions of RBPs with :term:`rRFs` and :term:`tRNA` is often observed and identified by means of :term:`negative control` experiments.
       
   **reference**
       Small RNAs like siRNAs are often targeting transcripts that form messenger RNAs (mRNAs). For evaluative purposes of siRNA signals it is helpful when mRNA sequencing results (when available) can be loaded as a reference (\ **R** in the |prgnam| logo).

   **repair**
       A biological process can be halted by disruption of a protein gene sustaining this process. Rebuilding the open reading frame (ORF) of the disrupted gene via site-directed mutagenesis can in theory restore the biological function. Mutant strains constructed by this approach are here called 'repair mutants'. These strains can provide information about how the biological process is established if this depends on some 'memory' effect.

   **RIP**
       The isolation of RNA molecules by immunoprecipitation of proteins that bind to these RNAs. UV-cross linking is often applied to make permanent bonds that allow for very stringent isolation procedures (in that case mostly referred to as CLIP_ or variants thereof, like CRAC [Granneman-2009]_).

   **RNA-seq**
       Abbreviation of high-throughput RNA sequencing done by next-generation sequencing (NGS) of :term:`cDNA` libraries.

   **RNAi**
       RNA interference of gene expression. Associated :term:`miRNA`\ s or :term:`siRNA`\ s guide Argonautes to transcripts that then get inactivated ('silenced') by :term:`Ago` and complexed proteins.

   **RPM**
       Reads per million (mapped reads).

   **rRFs**
       Ribosomal RNA (:term:`rRNA`) fragments. In some publications proposed to form a biologically relevant population of small RNAs associated with Argonautes. Because of their common co-purification with RNA-binding proteins (RBP), incl. :term:`Ago`\s, this association is mostly not :term:`specific` for the RBP but a by-catch linked to the experimental procedure. They are shared with the :term:`negative control`.

   **rRNA**
       Ribosomal RNA or rRNA. Ribosomes are the protein factories in living cells; they scan :term:`mRNA` molecules and link amino acids brought in by :term:`tRNA` molecules into a peptide chain. Ribosomes are present in all cells and similar between organisms. They are very abundant and necessary for all cellular processes as these rely on proteins produced by ribosomes. Ribosomes consist of two sub-units assembled from a large number of proteins and three to four RNA molecules, two of which are very long and derived from an even longer precursor RNA. Most energy of fast growing cells goes to the production of ribosomes.

   **SE**
       Abbreviation for single-end sequencing data. This kind of data is counted by |prgnam|; SAM-fields :smc:`RNEXT` (column 7) ``= *`` :smc:`PNEXT` (column 8) ``= 0`` and column 9 :smc:`TLEN` ``= 0``; instead of zero Pysam_ uses ``-1``. Also see :term:`PE` and :term:`bam`.
       
   **seq_id**
       Sequence-identifier, should be the same for :term:`GTF` and :term:`bedgraph` files.

   **siRNA**
       Short interfering RNA molecules, between 20-24 nt (nucleotides) in length. These RNAs are bound by Argonaute (-like) proteins and guide these to their targets (with a complimentary sequence).

   **smear**
       A continuum of :term:`background` bands, present in each lane, on images of experiments where purified molecules are visualized after being separated on size, i.e. according to their length. In contrast to a :term:`negative control`, discrete, obvious bands in lanes representing a :term:`positive control` will stand out and represent an expected outcome. Depending on the chosen stain or labeling technique, background signals might not get beyond the threshold of detectability, so that 'dirty' results can appear as 'clean'. :term:`PCR` amplification steps in high-throughput sequencing can, however, lead to a significant number of reads that derive from such 'invisible' background, as discussed by [Esteban-Serna-2023]_.

   **soft-clipping**
       Strategy to increase mapping of reads. Short 5' or 3' overhangs that are not aligned to the reference genome are removed from the alignment. This is annotated in the :term:`cigar` string with ``S``. This the default ``alignEndsType`` in STAR_. Soft-clipping can be restricted to 3' ends of the forward read (``--Extend5pOfRead1``) or both reads (``--Extend5pOfReads12``) in paired-end (:term:`PE`) data. With ``alignEndsType --EndToEnd`` no mismatching overhangs are allowed; the read has to map from start to finish.

   **specific**
       Specific reads - from the :term:`positive control` (blue **S** trace in the |prgnam| logo) or mutants under study (olive **M** signal) - are not present in :term:`negative control` experiments where no meaningful outcome is expected. Specific reads come from RNA molecules that are formed by the biological system under study (say the :term:`RNAi`-machinery) and associate with proteins constituting the activity of that biological system (e.g. Argonaute (Ago), Dicer (Dcr), RNA-dependent RNA polymerase (Rdp)), which is testable by (crosslinking plus) immunoprecipitation experiments.

       Think of fish caught with a worm. This set-up also brings up :term:`unspecific` material as the by-catch (because of the line and hook, not the hooked worm). 

   **specified**
       Reads are sorted by  |prgnam| into two groups, :term:`specific` or :term:`unspecific` reads. Reads, after this grouping, are specified.

   **svg**
       Scalable vector graphics, an image file format editable in programs like Inkscape_. SVG files can be displayed in web pages. Set as the default saving option in |prgnam|, which can be changed in ``2_shared.txt``. An image format can also be selected from the drop-down 'save' menu of displays generated with |prgnam|. SVG files with bedgraph traces can be very large; as an alternative choose :term:`PNG` or JPG formats. 

   **technical replicate**
       See :term:`biological replicate`.

   **tRNA**
       Transport RNA, required for translation of mRNAs into proteins by ribosomes (See :term:`mRNA`).

   **tsv**
       Unformatted, tab delimited text file with extension :smc:`TSV` (\ *.tsv* or *.tab*); contains tab separated values (cf. *.csv*, comma separated values). The tab-symbols (``\t``) guide loading and saving of the file contents with Pandas_.

   **uncollapsed**
       Reads as present in the :term:`fastq`/:term:`fasta` files after adapter removal; many identical reads, possibly :term:`PCR`-duplicates derived from one :term:`cDNA`, will be present in the data. :term:`Collapsing<collapsed>` removes this redundancy.

   **unique**
       Reads or cDNAs that are referred to as 'unique' map to a single locus on the reference genome, in contrast to :term:`multimapper`/ s. Maybe 'monomapper' would have been a better name.

   **unselected**
       Reads are dubbed *unselected* when they have been specified as :term:`unspecific` while adhering to characteristics of sought small RNAs (defined in the ``3_EXP.txt`` configuration file). They might have not been classified as :term:`specific` because these reads did not pass the set thresholds (10\ :sup:`UNSPECLOG10`, 2\ :sup:`LOG2BG`). On the other hand, a fraction of reads will always meet the set characteristics by chance, especially when the libraries have been size-selected. 

       After counting :term:`unspecific` reads (``countbams -k2``), the occurrence of unselected RNAs can be checked by analyzing the length distributions with ``showgraphs [-ld, -lo]`` (or checked in files with counts for read lengths as well as that of the 5' nt). The unselected reads are also written to separate bam files when counting the unspecific reads (by default from collapsed bam-files) and then can be visualized with ``showgraphs -c CHROM -u1 -t2``. The unselected bedgraph traces for :term:`collapsed` data are calculated on the basis of :term:`raw bedgraph <bedgraph>` output from the STAR_ aligner in the script set by :smc:`BAM2BG`. (A similar script for another program could be used as long as files with raw bedgraph values are produced). Reads with small-RNA characteristics (if expected) will form the majority among :term:`specific` sequences; these can be saved to separate bam-files as well (but cannot be displayed together with the specified reads they derive from).

   **unspecific**
       Unspecific reads are found by overlap with :term:`negative control` data (red **U** trace in the :ref:`logo <logo_smu>`), that is under conditions when the biological system under study is not active, for example because proteins essential for this system are absent or inactivated. These reads come from RNA that could fortuitously be present in the same size-fraction as :term:`specific` RNA molecules or stick to matrix-material used for purifying the RNA. 

       Think of the bycatch: twigs, plastic bags, nylon nets, bicycle wheels, tires and shopping trolleys pulled out of the water with a line and hook (not dependent on the worm).




