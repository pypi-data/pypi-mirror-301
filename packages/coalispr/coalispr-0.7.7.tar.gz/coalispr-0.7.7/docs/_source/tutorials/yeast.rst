.. include:: /properties.rst

Yeast RBPs 
==========

.. toctree::
   :maxdepth: 1

   Yeast/shared_contents_y
..   Yeast/unmap_table

This tutorial compares RNAs UV-crosslinked to RNA-binding proteins (:term:`RBP`\ s) Kre33 [Sharma-2017]_, Puf6 [Gerhardy-2021]_ and Nab3 [van.Nues-2017]_  in yeast *Saccharomyces cerevisiae*. The purpose is to show how similar experiments can be used as mutual controls for detecting :term:`unspecific` background. Important is that the analysis is done with at least one protein known not to be directly involved in binding the same RNA molecules as the other proteins. Here, data for proteins proven to be involved in processing and assembly of pre-rRNA, Kre33 and Puf6, are set against data for the termination factor Nab3 to identify regions of the pre-rRNA that :term:`specific`\ally associate to Kre33 or Puf6. More detailed analysis for these proteins is presented in the referred publications.

First,

- create a work directory (say ``Kre33Puf6/``) 

Then, move some files that have been shipped with the program:

-  copy the contents of this folder in the source ditribution :doc:`coalispr/docs/_source/tutorials/Yeast/shared/ </tutorials/Yeast/shared_contents_y>` to ``Kre33Puf6/``.

In a terminal, change directory to the created work environment (from which all scripts and commands will be run):

- ``cd /<path to>/Kre33Puf6/``


Dataset
-------

The yeast data we are using here have originally been aligned with Novoalign_ and analyzed with scripts from the pyCRAC_ suite [Webb-2014]_. For evaluating the data with |prgnam| we need bedgraph files. We can obtain these after aligning the data to the reference genome. To do this, the raw sequencing data is used and downloaded from the Gene Expression Omnibus (GEO_) database with the relevant accession numbers retrieved from the literature:

.. table::
   :align: left
  
   +---------------+------------------+------------------+------------+ 
   |  CRAC-data    | Reference        |  GEO acc. no.    |  SRA table |
   +===============+==================+==================+============+
   |  Kre33        | [Sharma-2017]_   | ``GSE87480``     | GSE87480_  |
   +---------------+------------------+------------------+------------+
   |  Puf6         | [Gerhardy-2021]_ | ``GSE174587``    | GSE174587_ |
   +---------------+------------------+------------------+------------+
   |  Nab3         | [van.Nues-2017]_ | ``GSE85545``     | GSE85545_  |
   +---------------+------------------+------------------+------------+


- Open the `GEO Accession Display`_ page for each of the experiments.
- Enter the accession no. into the field ``GEO accession`` and press ``GO``. 

For Kre33 and Puf6 all files are collected:

- Access ``SRA Run Selector`` from bottom of the GEO accession display page that has been opened.
- On the SRA Run Selector webpage, click on the ``Accession List`` button in the ``Total`` row of the ``Select`` pane. 
- Save the file to the work directory and, because it will be combined with other data, add a prefix.

  | Save as ``Kre33-SRR_Acc_List.txt`` and  ``Puf6-SRR_Acc_List.txt``.

- For detailed info, click the ``Metadata`` button for a file describing the experiment.

  | Save as ``Kre33-SraRunTable.txt`` and ``Puf6-SraRunTable.txt``

.. Collate the lists and files:

Collate the lists:

- ``cat Kre33-SRR_Acc_List.txt Puf6-SRR_Acc_List.txt > SRR_Acc_List.txt``

.. - ``cat Kre33-SraRunTable.txt Puf6-SraRunTable.txt > SraRunTable.txt``

For Nab3 select the glucose tests on the SRA Run Selector webpage:

- In the ``Found # items`` pane, select ``SRR4024838``, ``SRR4024839``, and ``SRR4024840``.
- In the ``Select`` pane, click on the ``Selected`` button and then the ``Accession List`` button.

  | Save as ``Nab3-SRR_Acc_List.txt``.

- For experiment details, click the ``Metadata`` button.

  | Save as  ``Nab3-SraRunTable.txt``.


.. Collate the lists and tables by:

Collate the lists:

- ``cat Nab3-SRR_Acc_List.txt >> SRR_Acc_List.txt`` [#alt]_
  
.. - ``cat Nab3-SraRunTable.txt >> SraRunTable.txt``

Download, extract :term:`fastq` and compress the data (These steps create a directory structure (see :doc:`/tutorials/mouse`) in the working folder the scripts rely on).

- ``sh 0_0-SRAaccess.sh``

  | This takes awhile [#preftch]_, and so does [#extr]_:

- ``sh 0_1-SRAaccess.sh``
- ``sh 0_2-gzip-fastq.sh``

|

.. _reftracs:

Reference traces
................

Traces for gene-expression in cells grown under the same conditions support analysis. |prgnam| can include these :term:`RNA-seq` mRNA signals as reference traces. We would like to compare CRAC signals to mRNA signals. Although the next step can be included within the Nab3 downloads, often such data have to be downloaded from another GEO experiment, which we simulate here. 

The mRNA reads for parental strain BY4740 linked to the Nab3 dataset will be used [van.Nues-2017]_:

.. table::
   :align: left
  
   +---------------+------------------+------------------+-------------+ 
   |  RNA-Seq      | Reference        |  GEO acc. no.    |  SRA table  |
   +===============+==================+==================+=============+
   |  BY4741       | [van.Nues-2017]_ | ``GSE85545``     | SRR4024831_ |
   +---------------+------------------+------------------+-------------+

- Obtain the metadata as above, save as ``BYRNASEQ-SraRunTable.txt``.

Get the sequencing data (this step is optional; omit if reference traces are not needed) [#optio]_:

- ``prefetch SRR4024831``
- ``sh 0_1_2-SRAaccess_ref.sh SRR4024831``

.. _refnam:
   
We want to align the reference reads independently from the CRAC data [#indepref]_ and for that change all ``SRR4024831`` labels to ``refSRR4024831``. First, ``SRR4024831``-files are renamed and then the folder: 

- ``for i in 1 2; do mv SRR4024831/SRR4024831_$i.fastq SRR4024831/refSRR4024831_$i.fastq; done; mv SRR4024831 refSRR4024831;``

Compress the uncollapsed reads.

- ``sh 0_2-gzip-fastq.sh refSRR4024831``

  
|
|

Alignment
---------

In the other tutorials, sequence alignments were created with STAR_; we will do that here as well. Before the data can be aligned to the yeast genome, we have to obtain reference files. The pyCRAC_ suite comes with reference :term:`fasta` and :term:`gtf` files for yeast, defining many non-coding RNAs [#sacc]_. More up-to-date versions have been used for the referenced papers and included here [#ensem]_. The GTF file should have been copied from the :doc:`shared folder </tutorials/Yeast/shared_contents_y>`. Download an accompanying, sorted fasta genome:
 
- ``wget -O - https://ftp.ensembl.org/pub/release-107/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna_sm.toplevel.fa.gz | gunzip > saccer-R64.fasta``

Then create the indices:

.. 
   - ``sh 1_1-star-indices.sh yeast Saccharomyces_cerevisiae.EF2.59.1.0.fa Saccharomyces_cerevisiae.EF2.59.1.3.gtf``
..
   
- ``sh 1_1-star-indices.sh yeast  saccer-R64.fasta Saccharomyces_cerevisiae.R64-1-1.75_1.2.gtf``

The adapters have been removed from the reads deposited at GEO_; still the 3'adapter (``App_PE``, see ':doc:`/tutorials/oligos_crac`') is found in forward reads in reverse reads, maybe formed as primer-dimer, and some 5' adapters. To remove these:

- ``sh 2_0-flexbar-trim.sh``

Make a dataset of collapsed reads:

- ``sh 2_1-collapse-pre-trimmed-seqs.sh``

The reads can now be aligned to the reference genome [#sharmem]_. Because UV-crosslinking is an inefficient event, compared to normal RNA-IP, low numbers of RNAs are isolated that are specifically bound to the protein of interest. The covalently bonded RNA, after being released from this protein by enzymatic digestion with proteinase K [McKellar-2020]_, can still carry a crosslinked residue that will interfere with cDNA synthesis. These factors lead to reduced yields of specific sequences, enabling amplification of unspecific background. Isolation of cDNAs for specific RNAs is further affected when the RNA-binding protein of interest is low in abundance or its RNA-binding substrate has a strong, higher-order structure. A strategy to reduce the number of background reads in the analysis of crosslinked RNAs is to apply a high stringency at the mapping stage [#end2end]_.

Due to UV-crosslinking, point-deletions and point-mutations are common in CRAC and CLIP-cDNAs. Therefore, such reads will be mapped while allowing at least an 1 nt mismatch;

.. _alignm:

Alignments and subsequent files will be stored in two directories within ``Kre33Puf6/`` that will be created by the scripts, namely ``STAR-analysis1-yeast_collapsed/`` and ``STAR-analysis1-yeast_uncollapsed/``. The folder names contain the :smc:`EXP` parameter (i.e. 'yeast') which is the first argument for the mapping scripts. To align the collapsed reads with one mismatch [#mismy]_ :

- ``sh 3_1-run-starPE-collapsed-14mer.sh yeast 1``

  
Do the same for the uncollapsed reads, run:

- ``sh 4_1-run-starPE-uncollapsed-14mer.sh yeast 1``

Remove the genome from shared memory (if that is used) when all mapping threads (set to 4 in the script) have completely finished:

- ``sh 4_1_2-remove-genome-from-shared-memory.sh yeast``

.. _bdgr:
   
And create bedgraphs for both collapsed and uncollapsed data sets by [#mismy]_:

- ``sh 3_2-run-make-bedgraphs.sh yeast 1``
- ``sh 4_2-run-make-bedgraphs-uncollapsed.sh yeast 1``

Note that the alignments are stored in their own subdirectories and that the filenames (``Aligned.out.bam``, ``Log.final.out`` etc.) are the same for each experiment. Therefore, |prgnam| uses the folder names as a lead for retrieving :term:`bedgraph` and :term:`bam` files.

|

Align reference 
...............
If reference sequences have been downloaded (this was :ref:`optional <reftracs>`), these can be aligned as (un)collapsed reads and converted to bedgraphs after adding a third parameter to instruct the mapping scripts to process the reference data.
Star will not see the readcounts for collapsed reads; if coverage is sufficient:

.. _mapref:
   
- ``sh 2_1-collapse-pre-trimmed-seqs.sh refSRR4024831``
- ``sh 3_1-run-starPE-collapsed-14mer.sh yeast 1 refSRR4024831``
- ``sh 3_2-run-make-bedgraphs.sh yeast 1 refSRR4024831``

For bedgraph values reflecting both coverage and numbers of mapped reads:

- ``sh 4_1-run-starPE-uncollapsed-14mer.sh yeast 1 refSRR4024831``
- ``sh 4_2-run-make-bedgraphs-uncollapsed.sh yeast 1 refSRR4024831``

|
|

|prgnam|
--------
Described in the ':doc:`/howtoguides`' and like in the :doc:`mouse tutorial </tutorials/mouse>` we need to set up working conditions for the program. First a working environment is prepared and then the configuration files.

|

Work folder
...........
Similar to the :doc:`mouse </tutorials/mouse>` tutorial we set up a workfolder for |prgnam| inside ``Kre33Puf6/``. 

.. _wrky:

- In a terminal change directory to ``Kre33Puf6/`` and run:
- ``coalispr init``
- Give 'yeast' as the :smc:`EXP` name for the session, in line with the :ref:`alignments <alignm>` created above and confirm.
- Choose the ``current`` folder for setting up the |prgnam| directory.

Output shows where the configuration files are:

.. code-block:: text

        Configuration files to edit are in: 
        '/<path to>/Kre33Puf6/Coalispr/config/constant_in'
        The path '/<path to>/Kre33Puf6/Coalispr' will be set as 'SAVEIN' in 3_yeast.txt.
        
|
|

Configuration
.............

|

.. _expfil:
   
Experiment file
'''''''''''''''
As described in the :doc:`/howtoguides`, for |prgnam| a file describing the experiments, :smc:`EXPFILE`, has to be created. The fields (columns) required for the program are prepared in the ``XtraColumns.txt`` copied from :doc:`/tutorials/Yeast/shared_contents_y`.

.. Gather all other information from the previously downloaded three ``SraRunTable``\s:

.. - ``cat Kre33-SraRunTable.txt Puf6-SraRunTable.txt Nab3-SraRunTable.txt > SraRunTable.txt``


For an informative overview, not all columns or rows are collected and combined with ``XtraColumns.txt``. Also, the :term:`csv` format has to be changed to that of :term:`tsv`. A separate script takes care of this:

- copy python script :download:`coalispr/coalispr/resources/share/cols_from_csv_to_tab.py </../_static/downloads/cols_from_csv_to_tab.py>` to the work directory ``Kre33Puf6/`` and run:
- ``python3 cols_from_csv_to_tab.py -f "Kre33-SraRunTable.txt,Puf6-SraRunTable.txt,Nab3-SraRunTable.txt,BYRNASEQ-SraRunTable.txt" -t2 -e XtraColumns.txt`` [#refincl]_
   | (``-f`` is input file, ``-t 2`` stands for "tutorial 2", the one for yeast RNA binding proteins; ``-e`` for "expand with")

The resulting file, ``Kre33Puf6_Exp.tsv``, would be:

.. code-block:: text

        Run                Description   Short Category Group Method  Fraction   Experiment GEO_Accession (exp) Sample Name
        SRR4305543         Kre33-data-I  K33_a        S   K33  rip33       WCE   SRX2199807          GSM2332452  GSM2332452
        SRR4305544        Kre33-data-II  K33_b        S   K33  rip33       WCE   SRX2199808          GSM2332453  GSM2332453
        SRR14570780     HTP-tagged Puf6   P6_a        S    P6   rip6       WCE  SRX10913999          GSM5320150  GSM5320150
        SRR14570781     HTP-tagged Puf6   P6_b        S    P6   rip6       WCE  SRX10914000          GSM5320151  GSM5320151
        SRR4024838     Nab3 Vari-X-link   N3_a        U    N3   rip3       WCE   SRX2016899          GSM2276892  GSM2276892
        SRR4024839      Nab3 Megatron 1   N3_b        U    N3   rip3       WCE   SRX2016900          GSM2276893  GSM2276893
        SRR4024840      Nab3 Megatron 2   N3_c        U    N3   rip3       WCE   SRX2016901          GSM2276894  GSM2276894
        refSRR4024831    BY4741-RNA-Seq     BY        R   NaN rnaseq       WCE   SRX2016892          GSM2276885  GSM2276885
        
|

Settings file
'''''''''''''

The next file to prepare is the  ``Coalispr/config/constant_in/3_yeast.txt`` within ``Kre33Puf66/``. This was copied from the ``3_EXP.txt`` during ``coalispr init`` :ref:`above <wrky>`, with some fields adapted to the current analysis. :ref:`Edit <editrs>` this file:

- ``scite Coalispr/config/constant_in/3_yeast.txt``

  | (by setting *Language* in the menu-bar to "Python" the active fields are highlighted compared to the comments)

.. _sttgsy:

Fields to be altered in the template ('#' indicates a comment):

   .. rst-class:: asfootnote

- :smc:`EXP`         : "yeast" [#done]_
- :smc:`CONFNAM`     : "3_yeast.txt"  [#done]_
- :smc:`EXPNAM`      : "Saccharomyces cerevisiae"
- :smc:`BINSTEP`     : 20 [#usgp]_
- :smc:`USEGAPS`     : BINSTEP [#usgp]_
- :smc:`MIRNAPKBUF`  : 1/4 
- :smc:`SETBASE`     : "/*<path to>*/Kre33Puf6/"
- :smc:`MUTNO`       : "1" [#srcf]_ 
- :smc:`REFNAM`      : "refSRR4024831\_"
- :smc:`REFS`        : REFNAM + TAG + "_" + MUTNO + "mismatch-" + EXP [#refs]_ 
- :smc:`EXPFILNAM`   : "Kre33Puf6_Exp.tsv"
- :smc:`TOTAL`       : "rip3" [#ri3]_
- :smc:`RIP1`        : "rip33" [#ri33]_
- :smc:`RIP2`        : "rip6" [#ri6]_
- :smc:`EXPERIMENT`  : "Description"
- :smc:`MUTGROUPS`   : {  
             | "K33" : "Kre33",  
             | "P6" : "Puf6",  
             | "N3" : "Nab3",  
             |  }
- :smc:`METHODS`     : {
             |  TOTAL:"Nab3 crac", 
             |  RIP1:"Kre33 crac", 
             |  RIP2:"Puf6 crac",
             |  }
- :smc:`UNSPECIFICS` : [ "N3", ]
- :smc:`MUTANTS`     :  ""
- :smc:`LENGTHSNAM`  : "Saccharomyces_cerevisiae.R64-1-1.75_chromosome_lengths.txt"
- :smc:`GTFREFNAM`   : "Saccharomyces_cerevisiae.R64-1-1.75_1.2.gtf"
- :smc:`SAVEIN`      : Path("/*<path to>*/Kre33Puf6/Coalispr") [#done]_
- :smc:`LENGTHSFILE` : BASEDIR / LENGTHSNAM [#noquot]_ [#base]_ 
- :smc:`EXPFILE`     : BASEDIR / EXPFILNAM 
- :smc:`REFDIR`      : BASEDIR / SRCFLDR / REFS
- :smc:`GTFREF`      : BASEDIR / GTFREFNAM

|
|

Analysis
--------

After preparing the configuration files, we can process the bedgraphs. 

|

.. figure:: /../_static/images/rDNA-Puf6-Kre33_yeast_chr_xii_all_reads.png
   :name: craclibsy
   :align: right
   :width: 900 px
   :height: 2951 px
   :scale: 24%

   **Figure 1.** rRF cDNAs and reads
   
   | Kre33 crosslinks specifically 
   | to 18S rRNA regions; Puf6  
   | binds 25S rRNA helices [#crosscon]_.
   | Top panel: cDNAs;
   | (collapsed data).
   | Bottom panels: reads;
   | (uncollapsed data).


``setexp``
..........

Begin with activating the new configuration:

- ``cd /<path to>/Kre33Puf6/``
- ``coalispr setexp -e yeast -p2``

  | choose option 2 and confirm.

|

``storedata``
.............

Now the :ref:`bedgraph data <bdgr>` can be loaded into Pandas_ dataframes, saved as :term:`pickle <pkl>` files by |prgnam|: 
When reference bedgraphs are used, these can be stored using option ``-d2``. First, do this for the :term:`uncollapsed` reads (the default type, ``-t1``):

- ``coalispr storedata -d1``
- ``coalispr storedata -d2``


For collapsed reads, getting an idea of the different cDNAs crosslinked to the proteins, do:

- ``coalispr storedata -d1 -t2``
- ``coalispr storedata -d2 -t2``


|

``showgraphs``
..............

Analysis of bedgraph traces for all uncollapsed reads with

- ``coalispr showgraphs -c XII -w2``

or checking traces representing cDNAs with

- ``coalispr showgraphs -c XII -w2 -t2``

shows how specific :term:`rRFs` for Kre33 derive from 18S regions in the rDNA and those for Puf6 from a 25S section (top panels in :ref:`Fig. 1 <craclibsy>`).
Zooming out from the rDNA region (bottom panel in :ref:`Fig. 1 <craclibsy>`) shows how noisy the RNA-seq data from cross-linked samples can be (e.g. for Kre33 or Puf6 [#nb3red]_). Therefore, monitoring single nt deletions (for CRAC) or mutations (for CLIP) that will be common for crosslinked uracil residues in crosslinked RNA fragments is an important measure. The pyCRAC_ software suite [Webb-2014]_ has been specifically developed for such in-depth analysis of RNA-seq data for crosslinked RNA. The referred publications for Kre33 [Sharma-2017]_, Puf6 [Gerhardy-2021]_ and Nab3 [van.Nues-2017]_ describe such an analysis. Here we aimed to illustrate usage of |prgnam| and show how independent experiments can form mutual controls for particular observations, as mentioned in the essay ":doc:`/paper`".

|
|
    
=====

Notes
'''''

.. [#alt] Instead of:

   - In the ``Select`` pane, click on the ``Selected`` button and then the ``Accession List`` button.

     | Save as ``Nab3-SRR_Acc_List.txt``

   - Collate the lists by

     | ``cat Nab3-SRR_Acc_List.txt >> SRR_Acc_List.txt`` 

   One can collate directly:

   - ``for i in SRR4024838 SRR4024839 SRR4024840; do echo $i >> SRR_Acc_List; done``

.. [#preftch] feedback in the terminal is like:
        
   .. code-block:: text

                2022-10-05T10:17:35 prefetch.2.11.0: 1) Downloading 'SRR4305543'...
                2022-10-05T10:17:35 prefetch.2.11.0:  Downloading via HTTPS...
                2022-10-05T10:17:53 prefetch.2.11.0:  HTTPS download succeed
                ..

.. [#extr] feedback is like:

   .. code-block:: text

                spots read      : 2,195,879
                reads read      : 4,391,758
                reads written   : 4,391,758

.. [#sacc] They are in the ``db/`` folder of the pyCRAC_ source package. 
.. [#optio] Although the actual sequences need not be gathered, the metadata is used for creating the :ref:`Experiment file <expfil>` (:smc:`EXPFILE`). Also the renaming and compression of the sequence files can be skipped.
.. [#indepref] RNA-seq reads for mRNA are obtained by a different protocol than those for CRAC samples; the latter being less abundant and with a shorter length need more stringent settings. Compare the STAR_ alignment commands in each mapping script. 
.. [#ensem] These pyCRAC GTFs include additional annotations for ncRNAs. General updates to the reference genome can be found at Ensembl_ or the *Saccharomyces Genome Database* (sgd_) ftp sites. Depending on the source, chromosome names can differ ('chrI' vs 'I' for example); therefore use fasta and gtf files from the same release-source for everything.
.. [#sharmem]  The alignment scripts are set up to load the genome and then keep it in shared memory, which works fine on a single computer. When the mapping is done on a cluster of shared computers, this can cause problems (see `STAR/issues/604`_); edit the bash scripts 3_1 and 4_1 so that the setting ``NoSharedMemory`` is activated.
.. [#end2end] In STAR_ :term:`soft-clipping` is default and will increase mapping scores and speed. Expect fast reductions in the number of mapped reads with the stringent ``alignEndsType --EndToEnd`` setting (compared to ``--Extend5pOfReads12``).
.. [#mismy] Add the number of allowed mismatches in the :ref:`alignment<alignm>` as the second argument for the script: ``sh 3_1-run-starPE-collapsed-14mer.sh yeast 1`` for 1 mismatch with the yeast genome. When mapping is redone with the same number of mismatches existent alignment folders within :smc:`SRCFLDR` [#srcf]_ will be renamed from  ``SRR..`` to ``_SRR..``.
.. [#srcf]  The string :smc:`MUTNO` helps to define :smc:`SRCFLDR` in the configuration file; yielding ``STAR-analysis1-yeast_``, which forms the beginning of the folder names for storing mapping data. These names end in ``collapsed`` or ``uncollapsed`` and are created by running mapping scripts 3_1 or 4_1. The 'yeast' portion relates to the :smc:`EXP` setting, which is :ref:`the first parameter for the scripts <alignm>`. The digit in the name represents the number of mismatches allowed in alignments of reads to the reference genome. The default in the scripts is zero mismatches but this can be set by adding the number as the second argument to the alignment command [#mismy]_. The :smc:`MUTNO` setting has to reflect this new number to work with the correct data set.
.. [#refincl] The called script assumes the reference metadata has been downloaded and is available. Otherwise the ``XtraColumns.txt`` would not fit either.
.. [#done] Done during ``coalispr init`` step.
.. [#usgp] With CRAC [Granneman-2009]_ direct binding contacts between protein and RNA are sought; best to keep peaks as narrow as possible. Most positive peaks are localized hits, so account for small single peaks rather than longer regions. Bacause the yeast genome is small, setting the resolution (which is given by :smc:`BINSTEP`) to 20 is feasible.
.. [#refs] Just uncomment this line in ``3_yeast.txt``. The name is a combination of set constants around the relabelled :ref:`data-id <refnam>`, refSRR4024831 (:smc:`REFNAM`), provided as the third parameter for the :ref:`mapping scripts <mapref>`, placing the outcomes in the :smc:`SETBASE` / :smc:`SRCFLDR`.
.. [#ri3]  For RNA-ip after crosslinking in the Nab3-crac sample instead of "total".
.. [#ri33] For Kre33 crac sample.
.. [#ri6] For  Puf6 crac sample.
.. [#noquot] No quotes (" ") around the text as this is a reference to pre-defined constants; keep spaces around /.
.. [#base] File is placed next to sequence data folders, within the work-directory ``Kre33Puf6/``. 
.. [#crosscon] The relative increases of Puf6-signals for the Kr33-specific 18S segment (and vice versa for the Kre33 trace over the Puf6-region in 25S) is probably due to cross-contamination when these samples were prepared in parallel and processed within the same RT and sequencing reactions. For other preps (``Kre33-a``) these overlaps were not observed.
.. [#nb3red] Termination factor Nab3 (red traces) is involved in the control of many transcripts [van.Nues-2017]_ in line with the red peak signals. Kre33 binds to leucine and serine tRNAs as well as snoRNAs snR4 and snR45 [Sharma-2017]_, while Puf6 predominantly interacts with 25S rRNA sequences [Gerhardy-2021]_ and some snoRNAs in the target domain (RvN; unpublished). The number of these potential targets is far exceeded by the amount of hits indicated by the blue traces. 




..   ad [#sacc] If not easily found, the genome :term:`fasta` file and :term:`gtf` annotations can be downloaded directly by:

   - ``wget https://git.ecdf.ed.ac.uk/sgrannem/pycrac/-/raw/master/pyCRAC/db/Saccharomyces_cerevisiae.EF2.59.1.0.fa``
   - ``wget https://git.ecdf.ed.ac.uk/sgrannem/pycrac/-/raw/master/pyCRAC/db/Saccharomyces_cerevisiae.EF2.59.1.3.gtf`` 
   - ``wget https://git.ecdf.ed.ac.uk/sgrannem/pycrac/-/raw/master/pyCRAC/db/Saccharomyces_cerevisiae.EF2.59.1.0_chr_lengths.txt``
..
..   ad [#ensem]At the illumina site (igenome_) or SGD (sgd-latest_) all relevant files can be obtained in one go . Various compressed files will be present in the extracted folder.

   On the Ensembl site, do a search for the species ('sacc') and pick the file format links to get to the pages with downloadable files. For a higher or different Ensembl release, the number ``107`` has to be replaced with the required version:

   - ``wget -O - https://ftp.ensembl.org/pub/release-107/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna_sm.toplevel.fa.gz | gunzip > saccer-R64.fasta``
   - ``wget -O - https://ftp.ensembl.org/pub/release-107/gtf/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.107.gtf.gz | gunzip > saccer-R64.gtf``

   The original -unsorted- version 75 of R64 can be downloaded as:

   - ``wget -O - https://ftp.ensembl.org/pub/release-75/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.75.dna_sm.toplevel.fa.gz | gunzip > saccer-R64-1-1.75.fasta``

..

.. _GSE87480: https://www.ncbi.nlm.nih.gov/Traces/study/?acc=PRJNA344887
.. _GSE174587: https://www.ncbi.nlm.nih.gov/Traces/study/?acc=PRJNA730580
.. _GSE85545: https://www.ncbi.nlm.nih.gov/Traces/study/?acc=PRJNA338773&o=acc_s%3Aa&s=SRR4024838,SRR4024839,SRR4024840
.. _SRR4024831:   https://www.ncbi.nlm.nih.gov/Traces/study/?acc=PRJNA338773&o=acc_s%3Aa&s=SRR4024831
.. _igenome: http://igenomes.illumina.com.s3-website-us-east-1.amazonaws.com/Saccharomyces_cerevisi.ae/Ensembl/R64-1-1/Saccharomyces_cerevisiae_Ensembl_R64-1-1.tar.gz
.. _Novoalign: https://www.novocraft.com/products/novoalign/
.. _sgd: http://sgd-archive.yeastgenome.org/sequence/S288C_reference/genome_releases/
.. _sgd-latest: http://sgd-archive.yeastgenome.org/sequence/S288C_reference/genome_releases/S288C_reference_genome_Current_Release.tgz



