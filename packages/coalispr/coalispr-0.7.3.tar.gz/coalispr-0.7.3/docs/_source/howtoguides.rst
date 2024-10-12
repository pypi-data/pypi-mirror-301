.. include:: /properties.rst

How-to guides
=============
The input for |prgnam| are :term:`bedgraph` files. Starting point is to get these. For this, adapters and barcoded linkers have to be removed from raw reads which then need to be mapped to a reference genome. For some data sets the mapping will have to take introns into account; i.e. the possibility that reads have been spliced [#spl]_. From the obtained alignments, :term:`bedgraph` files can be generated [#str]_.

In the |tuts| these preparations have been included. As also shown, before mapping reads, these can be :term:`collapsed` to speed up alignment and, more importantly, the counting of reads. The program selects the sections of the alignment file to count and collapsed reads only need to be counted once to obtain the number of all identical reads present in the library. Together with figures of bedgraph traces, the resultant counts (and linked figures) are the main output of |prgnam|.

Here, how |prgnam| works is explained; how it can help to clean up the data by means of :term:`negative control`\s. The program prepares counted data, which then can be further analyzed. 

|
|

Rationale
---------
The overall idea behind this application is that the output of negative biological controls is common to all samples, and relate to the kind of experimental methods used. These :term:`negative control`\s show which part of the experimental output is not informative. Therefore, removing this :term:`unspecific` output from all samples gives signals that are :term:`specific`, both for the :term:`positive  control` and for mutant or test samples analyzed by the experiment. |prgnam| systemizes this clearing up into a traceable and transparent procedure; it embraces the *bio* in bioinformatics.

.. figure:: /../_static/images/h99-chr8_reads-specification.png
   :name: readspec
   :align: right
   :width: 1491 px
   :height: 1355 px
   :scale: 30%

   Specifying reads by comparing controls.

   | :doc:`Analysis </tutorials/h99>` of *Cryptococcus neoformans* siRNAs (with
   | ``showgraphs -c8`` for chromosome 8). In the top panel 
   | traces for the mutants are set to invisible to show the 
   | overlap between positive and negative controls.

.. with ``coalispr showgraphs -c 8``.

The use of a negative or 'mock' control has been an age-old, systematic approach that enabled (molecular) biologists to account for experimentally relevant observations where the number of parameters affecting an outcome can be baffling. Statistics is only of any help when the signal to noise ratio in the data is much larger than 1. In many cases noise cannot be ignored; for example, data obtained by sequencing small RNAs will not be clean because the available techniques for isolating the input RNA all result in samples containing contaminating RNA, usually RNA that is very abundant in cells, like rRNA or tRNA. In view of their size, small RNAs can be mixed with fragments of broken down larger RNAs which might not be relevant for the biological process under study. Generally, irrelevant molecules can be present because of stickiness to materials during sample preparation. All these can be detected in statistically relevant numbers after the PCR amplification steps used when making the cDNA libraries and during their sequencing. 

Specific and unspecific reads can be distinguished easily for siRNAs. For specific association with Argonaute proteins, i.e. to fit the available RNA binding site on these proteins, siRNAs have to adhere to specific criteria. For example, in `Cryptococcus` the siRNAs are limited in size, being between 20 to 24 nt long, and their starting nucleotide is a U (T in the sequenced cDNA), required for the interaction with a conserved tyrosine residue (Y593 in *C.*\ |nbsp|\ *deneoformans* Ago1).

As mentioned in the :doc:`introduction</README>`, |prgnam| separates out :term:`specific` from :term:`unspecific` reads based on a computational approach by comparing read signals between :term:`bedgraph` files using Python_ and Pandas_. For this the program uses the following parameters: :smc:`UNSPECLOG10`, :smc:`USEGAPS` and :smc:`LOG2BG`, illustrated below, that can be tested (via ``coalispr info -r``\ ; see `info`_) and set in the configuration_ files. In the |tuts|, :smc:`UNSPECLOG10` is used with values of 0.78, 0.905, or 1.3 (setting margins to 10\ :sup:`0.78` = \ :sup:`~`\6, 10\ :sup:`0.905` = \ :sup:`~`\8, or 10\ :sup:`1.3` = \ :sup:`~`\20 fold).


.. figure:: /../_static/images/program_settings_wide_ed.svg
   :name: sttngs
   :align: center
   :figwidth: 100%

In order to enable comparison of bedgraph values of different experiments and for chromosomes with a particular length, the genome gets divided into equally sized :term:`bin`\s. Each read is placed in one bin, the one containing its mid-point. The 1 nt resolution of the RNA sequencing data will thereby change in line with the used bin size, configured  by  the :smc:`BINSTEP` parameter (set to 50) in the `configuration`_ file. For each bin the bedgraph values of reads placed in that bin are summed. The binning approach enables comparison and has another advantage: The :smc:`BINSTEP`-fold decrease in resolution leads to a comparable file-size reduction of stored bedgraph-data which helps to speed up data processing.
  
|
|

Configuration
-------------
|prgnam| relies on a :ref:`configuration file <const>`, ``constant.py``, which is fairly extensive, and a :ref:`file describing the experiment <exp>`. Because bedgraph and alignment data will need to be parsed and compared to annotation files, these files, including the `experiment file`_  need to be found, which is done by describing file-paths in the configuration file. The configuration file further allows for adapting many settings that determine how the data-traces will be presented. Each module of |prgnam| refers to ``constant.py``. Depending on the data set, configurations can vary from simple to complex, as illustrated in the |tuts|.


The configuration file consists of three parts:

- ``1_heading.txt`` to create a python module; this cannot be changed, 
- ``2_shared.txt`` with general defaults, and 
- ``3_EXP.txt`` with settings specific for the data and therefore has to be adapted.

The configuration texts contain explanations for each setting. 
The information provided in ``3_EXP.txt`` needs to be correct for the program to process the data. 
The three text files are combined into the python source-code file ``constant.py`` during ``coalispr setexp`` (see :ref:`below <setxp>`). If problems occur with |prgnam| due to a wrong setting, the program can be reset by:

- ``python3 -m coalispr.resources.constant_in.make_constant``. 

The section :doc:`errors` might be helpful to identify and correct faults, most often linked to a typo, a missing ``tab`` or to quotes or parentheses when only one of an expected pair is present.

|

.. _const:

``constant.py``
```````````````

The configuration in source-code file ``constant.py`` deals with the look and feel of figures, labeling, file naming and experiment descriptors. What follows are notes to give some idea about how this is set up.

.. note::

  | Do not edit the :term:`Python` file ``resources.constant.py``.
    This is a link to a particular file that will be regenerated automatically from text files.
  | Edit the text files (in :smc:`CONFFOLDER`)  instead.
  |
  | Change ``2_shared.txt`` (:smc:`SHARED`) and ``3_EXP.txt`` (:smc:`EXPTXT`) to adapt settings.
  |
  | Look and feel and other default settings are in ``2_shared.txt``.
  | All settings specific for the experiment/session/dataset :smc:`EXP` are in ``3_EXP.txt``

.. sidebar:: Symbols in ``constant.py`` 

   |
   | The configuration texts contain various symbols that, when removed, change functionality.
   |
   | :smc:`#`
   |    The hash symbol marks a comment. A line of words starting with :smc:`#` is ignored by Python. Placing or deleting a :smc:`#` (de)activates that line. 
   |
   | :smc:`NNN`

   .. _`constant`:

   |     A word in capitals, :smc:`NNN`, forms the name for a constant used to refer to a value, which can be a string of text (``NNN = 'a value'``), a number (``NNN = n``), a collection (``NNN = ['a', 'b', 'c']``), etc. . The value of a constant can be set or changed in the text files (see examples). The constant name :smc:`NNN` should remain intact.

   |    
   | :smc:`'  '` or  :smc:`"  "`
   |    A pair of (single or double) quotation marks enclose a string of text in Python, to be used as a label or a name. A starting quotation mark needs a closing one at the end to define a text string; a single quote cannot pair with a double quote.
   |
   | :smc:`/`
   |    A forward slash with surrounding spaces is used in the definition of a path to a file KKK: :literal:`\  NNN / MMM / KKK \ `. The sequence, spacing and slashes should remain intact.
   |
   | :smc:`[,]`  :smc:`{:,}`  :smc:`(,)`
   |     Square or curly brackets and parentheses are used for describing a collection of comma-separated objects in Python. Where present in the configuration text, these should not be removed and should remain paired.
   |
   | :smc:`Path(NNN)`
   |     This is a Python assignment, like in ``BASEDIR = Path(SETBASE)``, which creates file path :smc:`BASEDIR` from a string defined by constant :smc:`SETBASE`.



Communication within the program (and with the data) goes via very short names that are unique and case-sensitive to indicate individual libraries or 'samples' (e.g. ``A1`` for "Ago1", which is different from ``a1``, that could stand for a deletion mutant, "ago1Δ" ). The sample names function as labels in the display of bedgraph traces, or in count diagrams and as headers of columns in countfiles. The short names are of the user's choosing and this information will have to be given in the `Experiment file`_, the other important file |prgnam| depends on.
The experiment file (:smc:`EXPFILE`) can help to keep all relevant information together for separate libraries that form an experiment. More columns can be added as wished as long as the columns required for |prgnam| are present and their headers defined in the ``3_EXP.txt``.
 
Values for constants :smc:`NNN` can be changed to a preferred setting by editing the ``2_shared.txt`` or  ``3_EXP.txt`` configuration pages before running |prgnam| scripts.

The ``2_shared.txt`` and ``3_EXP.txt`` files are originally shipped in ``coalispr/resources/constant_in/`` and copied to the folder set by ``coalispr init`` (:ref:`see below <intt>`), into sub-folders ``config/constant_in/``. The ``constant.py`` that is built from the text files is actually a link pointing to ``constant-EXP.py`` that gets created and then stored in ``coalispr/resources/constant_out/`` when ``coalispr setexp`` is run (:ref:`see below <setxp>`).

For your experiment :smc:`EXP` do (in no particular order):

- Adapt ``config/constant_in/3_EXP.txt`` so that it describes
    - where to find :term:`bedgraph` files,
    - where to find the `Experiment file`_, 
    - what its column with short names would be, 
    - how to group them,
    - set display names for such groups,
    - where to output processed data,
    - where to find :term:`GTF` files,
    - how to account for modified or :term:`extra` sequences,
    - practical thresholds, e.g. :smc:`UNSPECLOG10` (see :ref:`below <unspclg10>`)
    - etc..

- Check (change) ``config/constant_in/2_shared.txt`` that contains settings of 
    - common folder names, 
    - common figure labels and of
    - parameters that control the look and feel of figures.

- Place (links to) references into a sub-folder :smc:`REFS`.

- Assemble a tab delimited `Experiment file`_ (:smc:`EXPFILE`)
    - link data file names to short names, via a column :smc:`SHORT`.
    - link short names to groups of mutants (:smc:`GROUP`), categories (:smc:`CATEGORY`), methods (:smc:`METHOD`), fractions (:smc:`FRACTION`), or conditions (:smc:`CONDITION`).
    
|

Filenaming
''''''''''
In |prgnam|, data-files are treated as input, or source, so that the following path-structure to the :term:`bedgraph` and :term:`bam` files is adhered to::

   BASEDIR / SRCFLDR+TAG / FILEKEY* / FILEKEY*MINUS BEDGRAPH # which is as:
                  SRCDIR / FILEKEY* / FILEKEY*PLUS BEDGRAPH  # and as:
                  SRCDIR / FILEKEY* / SAMBAM   # with SRCDIR = BASEDIR / SRCFLDR+TAG
   BASEDIR / (dir /)n *BEDGRAPH    # n is the number of levels given by NDIRLEVEL

Values for the constants in the paths will be set in ``3_EXP.txt``. This is explained in more detail below.

Bam and bedgraph files need to be stored in the same folder, the name of which will be used to find these files. This is done on the basis of the `Experiment file`_, a tabulated file with descriptors for the experiment. This also holds for reference files. Bedgraph files must be stranded, i.e. for each strand one bedgraph file should be present [#str]_.

.. _filk:

For example, file ``BASEDIR/dir1/dir2/AABB_n34_s5_sequence-run-info_uniq-minus.bedgraph`` will be collected based on the end of its name,".bedgraph", i.e. :smc:`BEDGRAPH` and the identifying start ("AABB_n34"). This start of the original filename is used as the :smc:`FILEKEY` and defined as such in the ``3_EXP.txt``. The file is expected to be in a folder ``dir2`` with a name that also begins with the :smc:`FILEKEY`. Thus, ``dir2`` would in this case have a name "AABB_n34...".  From this folder, the correct bedgraph file is then picked based on the presence of :smc:`MINUSIN` or :smc:`PLUSIN` in the file name [#str]_.

Therefore, the scripts rely on the bedgraph file name endings :smc:`PLUSIN` :smc:`BEDGRAPH` and :smc:`MINUSIN` :smc:`BEDGRAPH`. 

Output stored in the :term:`bam` file, contains information that indicates whether a read is uniquely mapped (vs. a "multimapper") [#cig]_. This information is extracted from the bam file when reads are counted [#unird]_. Bam files to be used are sharing the name given by the constant :smc:`SAMBAM`.

.. note:: 
 - The values for :smc:`SAMBAM`, :smc:`UNIQ`, :smc:`PLUSIN`, :smc:`MINUSIN` and :smc:`BEDGRAPH` in ``3_EXP.txt`` have to be taken from the names of input files created by upstream scripts doing the mapping and conversion to the bedgraph format. These files will be loaded during data collection or for counting. 
 - To enable different nomenclature, :smc:`PLUS` and :smc:`MINUS` will be used by |prgnam| in names for output files and during representation of strand information.
 - :smc:`PL` and :smc:`MI` are used for storage of (binary) data by the program.

|
|

Directory structure
'''''''''''''''''''
The values for :smc:`SRCNDIRLEVEL` or :smc:`REFNDIRLEVEL` determine the :smc:`NDIRLEVEL` for the containing data-files. For example, "dir1/dir2" in the file path above indicates 2 levels of depth in the search tree. By setting the :smc:`NDIRLEVEL` parameter, the search depth can be adapted to your filing structure. :smc:`NDIRLEVEL` needs to be > 0. Default values are according to examples in the |tuts|.

|

.. _exp:

Experiment file
```````````````

The constant :smc:`EXPFILE` defines the path_to :smc:`EXPFILNAM`, the file describing the experimental dataset. This file can be based on a ``SraRunTable`` or put together from scratch, as long as it becomes a tab delimited file (:term:`tsv`). Below, the required and optional fields in :smc:`EXPFILE` are described that are expected and set in ``3_EXP.txt``::

    File           Short       Category     Method      Group      Fraction     Condition etc.         # Header name in EXPFILE
  # FILEKEY        SHORT       CATEGORY     METHOD      GROUP      FRACTION     CONDITION              # Field NNN in "3_EXP.txt"
  #                            CAT_S,CAT_M  TOTAL, RIP1            WCE, NUCL    REPAIR                 # Field NNN in "3_EXP.txt" 
    AABB_n34       wt_1        S            total                  WCE       
    CCDD_n56       rA1_1       M            rip1        rA1        Nuc          rep


.. note::
 - Any white space by itself or as start/ending of a column value are removed, also from column headers.
 - Such spaces are possibly accidental and would interfere with proper running of the program.

|


:smc:`FILEKEY`, :smc:`SHORT`, :smc:`CATEGORY`, :smc:`METHOD`, :smc:`FRACTION`, :smc:`GROUP`, :smc:`CONDITION`
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The key for the file name is read from the :smc:`FILEKEY` column (here "File") of the tabbed :smc:`EXPFILE`. This key helps to link the bedgraph or bam file to a short unique (meaningful) name (:smc:`SHORT`) and other relevant information, such as :smc:`CATEGORY`. Both the :smc:`FILEKEY` and the :smc:`SHORT` name should be unique (with the :smc:`FILEKEY` being the same as the beginning of the name of the containing folder as explained :ref:`above <filk>`). This set-up enables to change the :smc:`SHORT` name (in :smc:`EXPFILE`) to whatever suits best for presentation while the original data file names can be kept.

Thus "AABB_n34" could be used as a :smc:`FILEKEY` that gets linked to the full file-name path when collecting bedgraphs and bam files.

The short name will be extracted from the :smc:`EXPFILE` via the heading :smc:`SHORT` and linked to the data files via a :smc:`FILEKEY` and to a :smc:`CATEGORY` and displayed as such with an associated color (see ``2_shared.txt``) [#col]_.

A third, required, column (:smc:`CATEGORY`) describes which experiments fall in the following categories:

- :smc:`CAT_U` for :term:`Unspecific`, (*Negative*) i.e. this experiment is a :term:`negative control` and not expected to give useful information.

- :smc:`CAT_S` for :term:`Specific`, (*Positive*) i.e. this experiment is a :term:`positive control` and expected to provide "wild-type" information.

- :smc:`CAT_M` for "Mutant", i.e. experiments for which the outcome needs to be assessed by comparison to negative and positive samples.

- :smc:`CAT_R` for :term:`Reference`, bedgraph files the experiments need to be compared to (e.g. RNA sequencing files when checking siRNAs).

- :smc:`CAT_D` for :term:`Discard`, experiments not used in the analysis.

.. note:: Lowercase for :smc:`CAT_U`, :smc:`CAT_S` or :smc:`CAT_M` excludes a sample from usage in discriminating reads as :smc:`SPECIFIC` or :smc:`UNSPECIFIC`.

Use lowercase settings for a category to mark that an experiment should not be part of the default set with which reads are classified as :smc:`SPECIFIC` or :smc:`UNSPECIFIC`. Thus, specifying reads (via ``_specific_and_unspecific_idx`` in module ``begraph_analyze.compare``) will not rely on samples indicated with an undercase ``u`` for :smc:`CAT_U` or ``s,m`` for :smc:`CAT_S` or :smc:`CAT_M`. This is relevant when a large number of almost identical (technical) replicates could create a bias when other samples have less replicates. Also, based on the results, a mutant could be re-evaluated as a negative sample and annotated as such by :smc:`CAT_U`:``u``. For example, when results for a putative 'catalytically dead' mutant (:smc:`CAT_M`:``M``) turn out to be very similar to those of a deletion that functions as a basic negative control (:smc:`CAT_U`: ``U``). 

By default all samples in **EXPFILE** will be counted, also any 'discards' (:smc:`CAT_D`). All negative and positive controls will be included for analysing counts and displays. When some mutants are recognized as 'redundant' (:smc:`CAT_M`:``m``), these are not included for the general data-analysis of ``showcounts``; by default the non-redundant mutant set is loaded. For other commands (``showgraphs`` - :ref:`see below <shwgr>`, ``region``, or ``groupcompare``) redundant mutant samples can be included.

Other fields than :smc:`CATEGORY` are used to differentiate between experiment groups during analysis and in the interactive drawing. Examples are :smc:`METHOD` or :smc:`FRACTION`, that refer to procedures yielding the RNA sample, or :smc:`CONDITION`, that accommodate groupings according to growth or other parameters. The :smc:`GROUP` column helps to separate groups of mutants. Tagged strains when used for RNA immunoprecipitation, can be grouped as 'mutant' but are principally treated as a method. Columns :smc:`METHOD`, :smc:`FRACTION` or :smc:`CONDITION` only need values relating to different methods, fractions or conditions. The value that stands for a common standard ('wildtype') can be omitted. When only one value applies to all samples, the column can be left blank. In the latter case, the group will not be shown in ``coalispr showgraphs``. Thus, if the single method, fraction or condition might be relevant and needs to be visible, its column in the :smc:`EXPFILE` has to be filled with the appropriate value for each sample. A :smc:`READDENS` column can be included to 'normalize' or change the mRNA references so that the traces in the overall display are generally comparable.

.. note::  The program fails, when any of the columns referred to by :smc:`FILEKEY`, :smc:`SHORT`, :smc:`CATEGORY`, :smc:`METHOD`, :smc:`FRACTION`, :smc:`GROUP`, or :smc:`CONDITION` are not in the :smc:`EXPFILE`.

|

Replicates, names, extra DNA  
''''''''''''''''''''''''''''
Indices for replicates of the same experiment should be divided from the short name by means of an underscore (_). This helps to differentiate between :term:`technical replicate`\ s (character) or :term:`biological replicate`\ s (number) of the same experiment, while still seen as one group of samples. Three mutant replicates with :smc:`SHORT` names ``a1_1a``, ``a1_2``, ``a1_1c`` will be grouped by setting ``a1`` in :smc:`GROUP`.


| Some other aspects (for programming use) and entries that need user-input:
| When numbers are used as chromosome names in GTFs and length-files, these names are processed as text strings (thus in |prgnam| source-code files a number ``#`` is referred to as ``'#'`` when it stands for a name).

Bedgraph values for sequences mapping to extrageneous DNA (added to the organism by cloning or transformation) can be incorporated in the analysis by using :smc:`GTFEXTRA`, and is referred to as :smc:`CHRXTRA` with length :smc:`LENXTRA` (set in ``3_EXP.txt`` or loaded via :smc:`LENXTRAFILE`). A combined gtf will be generated for use in the bedgraph browser. For mapping, the genome fasta file has to be enlarged with these extra sequences (under chromosome name :smc:`CHRXTRA`; as done in this :ref:`section<incl45smouse>` of ':doc:`/tutorials/mouse`' in the |tuts|). 

|
|

Output
------
|prgnam| produces various outputs, depending on the command that is run. The :doc:`/tutorials` describe the use of command ``init`` (:ref:`see below <intt>`) to initialize the program after which the :ref:`configuration <const>` can be adapted to the experiment that will be analysed. During this step various folders are created inside the |prgnam| dictionary inside the chosen work environment. Apart from the ``config`` folder with configuration files, there are folders named ``data`` (for :smc:`TSV` files with counts etc.), ``figures`` (where created images are saved), ``logs`` and ``outputs``, each containing subfolders, one for each :smc:`Exp`. For example the path to a count file would be:

``Work-environment / Coalispr / data / EXP / tsvfiles /``

The overall file structure is:

.. code-block:: text

        Work-environment                        (constant name)
        ├── Coalispr
        │   ├── config                           CONFBASE
        |   |   └── constant_in                  CONFFOLDER
        |   |       ├── 2_shared.txt             SHARED
        |   |       └── 3_EXP.txt                EXPTXT
        |   |   
        │   ├── data                             DATA
        |   |   └── EXP                          EXP
        |   |       ├── tsvfiles                 SAVETSV
        |   |       ├── pickled                  STOREPICKLE
        |   |       ├── backup_from_pickled      PKLTSV
        |   |       └── bamfiles                 SAVEBAM
        |   |
        │   ├── downloads                        DWNLDS
        |   |
        │   ├── figures                          FIGS
        │   |   └── EXP                          EXP
            |       ├── jpgfigures               SAVEJPG
            |       ├── pdfs                     SAVEPDF
            |       ├── pngfigures               SAVEPNG
            |       └── svgfigures               SAVESVG
            | 
            ├── logs                             LOGS
            |   └── EXP                          EXP
            |       └── run-log.txt              LOGFILNAM
            |
            └── outputs                          OUTPUTS
                └── EXP                          EXP

Like the name for :smc:`EXP`, all folder names can be reconfigured via constants in ``2_shared.txt``.

|
|

Commands
--------
|prgnam| runs with various, more or less sequential, commands: ``init``, ``setexp``, ``storedata``, ``showgraphs``, ``countbams``, ``showcounts`` ``annotate``, ``groupcompare``, ``info`` and ``test``. Each command comes with a set of options, some of which, like ``-g`` (to split samples according to a *group*\ ing) or ``-x`` (for *excluded* :smc:`CAT_D` samples) will only be available when these are in the :smc:`EXPFILE`. Use the help option ``-h`` to get direct information how to generate a valid command [#coal]_. For example ``coalispr info -h`` provides:

.. code-block:: text

        usage: coalispr info [-i{1,2} -p{1,2} -r{1,2,3} -h]

        Show experiment name, file paths, number of regions, or memory-usage

        optional arguments:
          -h, --help  show this help message and exit
          -i {1,2}    Show 1: current experiment, 2: memory-usage.
          -p {1,2}    Show path to: 1: configuration file '3_EXP.txt'; 2: file
                      describing sequencing data 'EXPFILE'.
          -r {1,2,3}  Regions found depending on settings for parameters
                      'UNSPECLOG10', from (0.61, 0.78, 0.905, 1.0, 1.3), 'USEGAPS',
                      from (50, 100, 150, 200, 300), and 'LOG2BG', from (4, 5, 6, 7,
                      8, 9, 10); 1:collect data, 2:show 'uncollapsed' data; 3:show
                      'collapsed' data. Note that 1 creates input for 2 or 3; run 1
                      first.
          -nt {0,1}   Omit figure title from graph; 0: Keep, 1: Omit.
 
(Each name in ``capitals`` is a constant_ as described in ``constant.py``, :ref:`see above <const>`)

.. note:: 

  |prgnam| is not intended to be run in a web-environment (like a jupyter notebook\ [#jnsht]_ or jupyterlab); it has been developed and tested for the command line interface of a Unix-like console/terminal.

|

.. _intt:

``init``
````````
Command ``coalispr init`` requests input from the user in two steps: First, to give the name for their session/experiment (i.e. the value for :smc:`EXP`) and, 
second, to chose a work-directory to place a ``config`` folder with configuration input files ``2_shared.txt`` and ``3_EXP.txt``. 

The provided name ("ExpSessionName") in the first step will replace "EXP" in ``3_EXP.txt`` when setting up the work-environment for |prgnam|. During the second step, the user is presented with three choices where the ``config`` folder should be placed:

- ``1: home``, in their home folder (within a new directory ``Coalispr``), 
- ``2: current``, in the current directory (within a new folder ``Coalispr``), 
- ``3: source``, in the |prgnam| installation folder next to ``coalispr`` (with  python source-code) and ``docs`` (with documentation).

Option ``2: current`` helps to choose another folder, say nearby the data-files: in the terminal change directory to this location before running ``init``.

A ``Coalispr`` work-folder with the ``config`` directory will be created [#pwd]_ when chosing either ``1: home`` or ``2: current``. 

The chosen work-folder will also be set in in the ``3_ExpSessionName.txt`` as :smc:`SAVEIN`.

Experiment/session-linked configuration also allows to define a separate look and feel by changing ``2_shared.txt``.

The generated ``config`` folder contains files for editing, while the `Experiment file`_ could be put there by the user. Other folders are created next to ``config`` for storing output from the program, like ``figures`` and ``logs``. In ``data`` processed :term:`bedgraph` and :term:`tsv` files will be placed.

Before attempting to run the next |prgnam| command, ``coalispr setexp``, make sure that the ``3_ExpSessionName.txt`` has been edited so that the bedgraph data of interest can be found as well as the associated `Experiment file`_ (:smc:`EXPFILE`) and that the latter contains the expected :smc:`FILEKEY`, :smc:`SHORT`, :smc:`CATEGORY` and, depending on the dataset, :smc:`GROUP`, :smc:`METHOD` or :smc:`CONDITION` columns.

|

.. _setxp:

``setexp``
``````````
The ``coalispr setexp -e EXP`` command defines the *experiment/session* (``-e``) 'EXP' for which subsequent commands will be valid. In this step the ``coalipr.py`` configuration file gets set, which will be used from then on. That can be for a coalispr command in the same or another terminal. Thus, if in one terminal |prgnam| for a "Jec21" experiment is run and in another terminal for "H99" data, each session will follow the latest ``setexp`` setting.  Thus, when multiple sessions are open, make sure to _`reset the experiment`: run ``setexp`` for each session before any other command in that session.

When an extra session will be opened with ``setexp``, the ``-p2`` (*path*) option will help to find the required configuration files in the associated working directory. This uses the same method as for ``coalispr init``: Change directory before running the ``setexp`` command to use this option [#pwd]_. 

After making a change in a configuration file, the ``coalispr.resources.constant.py`` has to be regenerated to incorporate the new setting. In that case, include the path to the configuration files as well; for example: ``coalispr setexp -e H99 -p2``.

|

``storedata``
`````````````
The ``coalispr storedata`` processes the bedgraph data for analysis using Python_ Pandas_. Check the ``-h`` *help* option to see what options are available. There will be the possibility to select the kind of bedgraph data (for experiments or references). Further, this command needs to be run twice for each data set when files are assembled for both :term:`uncollapsed` (default) and :term:`collapsed` reads (for the latter *type*, add the ``-t`` option for this). The collapsed data-set is smaller and will create output faster (Maybe useful for a test run?). 

During this step also :term:`tsv` files (in the ``data`` folder) describing the peak sections with relevant, :term:`specific` sequences vs. peaks with the :term:`unspecific` background are generated. This is based on the settings for :smc:`UNSPECLOG10` (see :ref:`below <unspclg10>`), :smc:`USEGAPS` and :smc:`LOG2BG` defined in the ``3_ExpSessionName.txt``. To find useful values for these parameters, diagrams can be consulted that are created with ``coalispr info -r1`` (this takes a while!) followed by ``coalispr info -r2`` (see :ref:`below figure <rdssttngs>`, info_). To keep unspecific signals as tight as possible, the default is to keep their peaks to :smc:`BINSTEP` and not to fuse them by bridging gaps; this can be changed via :smc:`UNSPCGAPS`.

If one likes to see the difference of one setting to another with respect to ``coalispr showgraphs`` or other functions, change the parameter itself in the configuration file, `reset the experiment`_ to rebuild ``constant.py``, and rerun ``coalispr storedata`` to save the relevant region definitions.

.. sidebar:: ``coalispr showgraphs -c1 -t2 -w2``

   .. image:: /../_static/images/Coalispr_H99_bedgraphs_for_Chromosome_1_w2.png
      :name: bfgrphsw2
      :align: center
      :width: 1000 px
      :height: 800 px
      :scale: 30%
   
   All reads for chromosome 1, for :term:`positive <positive control>` (blue) and :term:`negative control`\ s (red) [#sirns]_.

The used settings  are incorporated in the names of the :term:`tsv` files with regions (stored in folder :smc:`SAVETSV` in :smc:`DATA` \ :smc:`EXP`). The regions stored in these files are used for retrieving reads to count from the :term:`bam` files, with ``coalispr countbams`` (see :ref:`below <cntbms>`).

.. _bckpbd:

Other functions allow to :ref:`back up binary data <bckpbd>` as text and rebuild binary data files from this backup. These steps facilitate the update of binary data-files (the :term:`pickle <pkl>` format can change between Python versions), thereby bypassing the time-consuming step of re-loading bedgraph data (``coalispr storedata -d{1-2}``). This involves the following steps:

  - Create a text backup of binary data (``coalispr storedata -d3``). The binary data are kept in ``data/pickled/`` (:smc:`STOREPATH` / :smc:`STOREPICKLE` /) as ``*data*.pkl`` files. The backup is stored in ``data/backup_from_pickled/`` (:smc:`STOREPATH` / :smc:`PKL2TSV` /). The original datastructures (sets of dictionaries with ``pandas.DataFrames``)  are saved as folders with :term:`tsv` text files.
  - Recreate binary files from backup (``coalispr storedata -d4``), which will be placed in ``data/pickled_from_backup``  (:smc:`STOREPATH` / :smc:`TSV2PKL` /).
  - After completion the folder ``data/pickled/`` (with the original binary files) has been moved to ``data/pickled.bak/`` (so that its contents will be kept but not found anymore by |prgnam|). Instead, folder ``data/pickled_from_backup`` with the recreated binary files will be linked  to ``data/pickled``. 
  - ``coalispr showgraphs`` should work again.
  - The data have been merged again and regions with (un)specific reads have been regenerated; this reproduction can be (slightly) different and thereby the numbers obtainable with ``coalispr countbams``.
  - If all is well, the backups can be deleted.

The same procedures are applied when a sample name needs to be altered after loading and counting the data. Renaming is done interactively with ``coalispr storedata -d5`` allowing to do this for one group of samples in one go. In all :smc:`TSV` text files within ``data``, that is in the data an count files, the sample names will be changed, including in the :smc:`EXPFILE` describing the experiment. Existent data will be backed up. Advised is to check whether the recreated files are comparable in size (e.g. in the case of the experiment file, see :ref:`storedata <strdatsiz>` in :doc:`errors`).

|

.. _shwgr:

``showgraphs``
``````````````
One of the major outputs of |prgnam| is the visualization of bedgraph traces without limiting their numbers. The produced figures are interactive [#scrpt]_: one can turn groups of traces off, highlight particular traces, show annotations (if loaded) and traces for mRNA transcripts (if available) as reference. Displays can be saved in various formats, say as :term:`png` or as vector-graphics (:term:`svg`), directly (by setting *write-graph* option ``-wg``) or from the menu. Below an overview of available interactivity (this message gets displayed in the terminal from which ``python3 coalispr showgraphs -c`` is run).

.. sidebar:: ``coalispr showgraphs -c1 -t2 -w4``

   .. image:: /../_static/images/Coalispr_H99_bedgraphs_for_Chromosome_1_.png
      :name: bfgrphs
      :align: center
      :width: 1000 px
      :height: 800 px
      :scale: 30%

   .. image:: /../_static/images/Coalispr_H99_bedgraphs_for_Chromosome_1_sel.png
      :name: bfgrphsrd
      :align: center
      :width: 1000 px
      :height: 800 px
      :scale: 30%

   :term:`Specific` reads for the :term:`positive control`\ s and mutants [#sirns]_. Three rde mutants produce reduced amounts of siRNAs.

.. code-block:: text


    Coalispr display of bedgraph traces is interactive via the:
    a. menu bar options: see tooltips; keybindings:
          Home/Reset         h, r, home
          Back               left, c, backspace
          Forward            right, v
          Pan/Zoom           p
          Zoom-to-rect       o
          Save               s, ctrl+s
          Toggle fullscreen  f, ctrl+f
          Close Figure       ctrl+w, cmd+w, q
       hold x or y to constrain pan/zoom to that axis
    b. y-axis: toggle scale between log2 and linear
          (reset y-scale after Back/Forward between log2/linear)
    c. x-axis: print crude region coordinates
          (after Zoom, copy for `showgraphs -r1`)
    d. bedgraph trace: annotate and highlight
    e. gtf, segment bars: annotate
    f. legend and side panel patches: toggle traces as a group
          (legend overrules side panel)
    g. legend: can be dragged around
    h. title: toggle legend
    i. y-axis label: toggle title
    j. x-axis label: reset toggled traces
    k. tracks label: reset track annotations            


This command can be set to show :term:`uncollapsed` (default) or :term:`collapsed` data (with *type* option ``-t2``), and with ``-r`` for a chromosomal *region* defined by two coordinates. A particular display *window* can be chosen (option ``-w``), but normally the default sequence is shown: first a display of all reads, then of discarded, :term:`unspecific` reads and last, a third window with the remaining, :term:`specific` reads. Option ``-s`` can be used to select a particular *set of samples*.

Below is illustrated how bedgraph representations differ between a genome browser like IGB_ (left) and |prgnam| (four panels on the right, the top two from a run with command ``showgraphs -c1 -w4`` and the bottom two from a run in a separate terminal with options ``-c1 -t2 -w4``). They provide complementary insights. The 1 nt resolution of IGB allows detection of precise boundaries, while |prgnam| provides the ability to quickly load all samples and compare them in one go. For example, it is easy to enlarge the genomic context of the transposon with the CNAG_00814 transcript (with the 'Zoom rectangle' tool draw a box inside the middle ``segm.`` bar spanning the region of interest around 2,500,000) [#xaxisact]_. In the upper section :term:`uncollapsed` data traces with predominant anti-sense peaks in comparison to the :term:`collapsed` data below [#cllps]_ are shown.  From one |prgnam| display, different images can be output, depending on which highlights and traces have been toggled to be shown: both kinds of representation reveal a difference between various mutants, with rde1, rde3 and rde5 signals matching those of the :term:`negative control` background (red); the rde2 signals are halfway the background and those for the wild type (blue), while the rrp6 profile deviates in both signal height and coverage. Sharp troughs in traces displayed by |prgnam| match introns in the genome browser, showing that RNAi is mostly directed at spliced RNA transcripts, contrary to the model proposed by [Dumesic-2013]_ et al. [#dumes]_.

.. figure:: /../_stat ic/images/CNAG_00814.png
   :name: cng00814
   :align: center
   :width: 4560 px
   :height: 1800 px
   :scale: 20%

   Intron skipping siRNAs against CNAG_00814 at resolution 1:1 (IGB_ image, left) vs 1:50 (right) [#sirns]_.

|

.. _cntbms:

``countbams``
`````````````
Without extra options, the ``coalispr countbams`` command only count reads in segments determined as :term:`specific` for :term:`uncollapsed` data (default, set by :smc:`TAGSEG`). The actual counting is done using :term:`bam`-alignments created with :term:`collapsed` data (default, set by :smc:`TAGBAM`). This is only possible when both kinds of data sets have been prepared. Time used for preparation of the collapsed data-set will be regained at this counting stage: counting proceeds line by line, but in the case of collapsing, all identical reads will be counted in one go instead of one-by-one [#tagbam]_.

*Binning of counts.* Distribution of reads over the counted segment can be determined by splitting the segments into sections, or :term:`bin`\s for which counts are summed as well as for the whole region. This is determined by :smc:`BINS` in the ``3_ExpSessionName.txt``. Setting this higher than 1 or overruling this with *bins* parameter ``-b``, coverage patterns can become visible in the registered counts.

*Input counts.* Other options can be used, like to pick the _`kind` of reads (:smc:`SPECIFIC`, default; :smc:`UNSPECIFIC`) to count, say for :term:`unspecific` reads (*kind* option ``-k2``), which will be used for creating diagrams to check libraries. If such diagrams are needed, the unspecific counts need to be obtained (see also below section on *Unselected reads*). With option *raw counts* (``-rc``) the total numbers of input reads are counted, providing strand-specific numbers for aligned reads. Numbers for unmapped reads when available are also determined. With command ``coalispr showcounts -rc`` the input counts can be visualized (see below, e.g. for :ref:`uncollapsed reads <inptcnts>`).

*Unselected reads.* Some reads in :term:`positive control` or mutant samples could represent genuine :term:`specific` RNAs while they have been specified as :term:`unspecific` due to overlap with reads of :term:`negative control`\s. This happens when the thresholds are not met. At the moment it is possible to recover putative fungal siRNAs from unspecific data using their start-nucleotide ``T`` (:smc:`BAMSTART`) and a length of 19-25 nt (:smc:`BAMLOW`\ -\ :smc:`BAMHIGH`) as definable characteristics [#char]_. During counting of unspecific reads, these :term:`unselected` reads can be copied to a separate alignment file by adding the *unselected* option ``-u 1``. Conversion of these :term:`bam` files to bedgraphs (with ``raw`` counts, not ``RPM`` as output values) can be done using STAR_ if that aligner is available [#b2bg]_. In that case, bedgraphs will be created, processed and included in collapsed data (``-t2```; by default used for counting as set by :smc:`TAGBAM`). When including the ``-u`` option with the ``showgraph`` command, :term:`unselected` traces for reads with the given characteristics in negative control data can be visualized with ``coalispr showgraphs -t2 -w3 -u1``  [#xbam]_. For this to work the total mapped input numbers for collapsed reads (obtained with ``countbams -rc 2``) has to be collected beforehand; these will be used to calculate ``RPM`` values in line with the original bedgraph traces.

.. Note:: 

   Run both ``coalispr countbams`` (for :smc:`SPECIFIC` reads) as well as ``coalispr countbams -k2 {wb 1 -u1}`` (for :smc:`UNSPECIFIC` data) to be able to create (most) diagrams with ``coalispr showcounts``.


Visual inspection of traces of unselected-reads - when combined with length-distributions - shows that some, as hoped, coincide with reads specified as :term:`specific` sense and anti-sense siRNAs. Many unselected reads, however, overlap sense transcripts. This might just be the result of chance, namely when fragments of degraded mRNAs, rRNAs, tRNAs or sn(o)RNAs happen to adhere to siRNA characteristics. It might be tempting to assume that these sense RNAs form a resource for the production of siRNAs, but the overlap with similar RNAs in negative control samples argues against such an interpretation. Surprising though, is the observation that after restoring RNAi, both sense and anti-sense versions of siRNAs can be found targeting tRNAs and especially the large rRNAs. Would this imply that production of genuine siRNAs, i.e. not against useful transcripts, has to be 'learned'? Or is the RNAi response somehow linked to translation, which directly involves the large rRNAs and tRNAs?

.. figure:: /../_static/images/input_counts_h99.png
   :name: inptcnts
   :align: right
   :width: 706 px
   :height: 361 px
   :scale: 50%

   Input counts [#sirns]_ by ``coalispr showcounts -rc 1``.

|

.. _shwcnt:

``showcounts``
``````````````
Information obtained by counting reads, can be visualized using scripts [#scrpt]_ shipped with |prgnam| and called by the ``coalispr showcounts`` command. The scripts provide a quick insight in the properties of the sequenced libraries:

*Input counts.* With parameter ``-rc`` *raw* input *counts* will be displayed, split over strands (:smc:`PLUS`, :smc:`MINUS`) while unmapped reads are shown [#avail]_. This gives a :ref:`quick overview <inptcnts>` of differences between the libraries analyzed.  The type of reads shown (:smc:`TAGCOLL` or :smc:`TAGUNCOLL`) can be chosen as well as the _`grouping` of libraries (*group* option ``-g``) according to either :smc:`CATEGORY`  (:smc:`UNSPECIFIC`, :smc:`SPECIFIC`, :smc:`MUTANT`; default) or the :smc:`METHOD` used to prepare the sequenced RNA [#meth]_. Grouping per category will, for input counts, also show :term:`unused <discard>` :smc:`DISCARD` samples; these can be omitted by including the *exclude* option ``-x 1``.

The abundance of reads mapped to the minus strand in especially unspecific or total sRNA preps of *Cryptococcus (de)neoformans* is very noticable: their rDNA is encoded on a negative strand (that of Chromosome 2) [#ripin]_.

.. figure:: /../_static/images/h99_libcounts_all.png
   :name: h99libcnts
   :align: right
   :width: 718 px
   :height: 369 px
   :scale: 50%

   Library counts [#sirns]_ by ``coalispr showcounts -lc 1``.

*Library counts.* Total *library counts*, for :term:`specific` vs. :term:`unspecific` reads can be diagrammed using parameter ``-lc``, and :ref:`grouped <grouping>` via option ``-g``. Data per _`strand` can be shown with *stranded* option ``-st`` (:smc:`COMBI`, default; :smc:`MUNR`, :smc:`CORB`). Based on the :term:`cigar` string, alignments can be evaluated; only fully matching sequences (with or without one intron-like gap) are counted; all other alignments are skipped (:smc:`SKIP`), but their number logged to a separate file. Change scales of count numbers or show difference with unspecific reads based on *log2* values with option ``-lg``.

These figures highlight the variability between libraries and reveal the over-representation of :term:`unspecific` reads in samples where production of expected siRNAs has been affected: compare :term:`mutant`  (category :smc:`MUTANT`)  libraries with those of the :term:`negative <negative control>` (:smc:`UNSPECIFIC`) and :term:`positive control`\s (:smc:`SPECIFIC`). This suggests that not many genuine siRNAs are present in mutants :ref:`rde1, rde4, or rde5 <h99libcnts>`. 

*Length distributions.* In fungi like *Cryptococcus*, :term:`siRNA`\s range from 20-24 :term:`nt` and tend to have a U (T in cDNAs) as the 5' nt. The *length-distribution* option ``-lo`` forms an overview of the total of all library-reads split according to length of the reads and their starting nucleotide. :term:`Specific <specific>` reads are compared to :term:`unspecific` reads. One can choose to get information for all library (:smc:`LIBR`) reads, cDNAs (:smc:`COLLR`), for reads mapping to unannotated sequences [#mmu45s]_ or :term:`when used to genetically manipulate the strains <extra>` (:smc:`CHRXTRA`) [#avail]_. Reads that map to a unique (:smc:`UNIQ` [#unird]_) locus, or those that can be aligned at multiple loci (:smc:`MULMAP`), can be selected by means of an extra option ``-ma``.

The spread of intron lengths (number of mismatching *N*\s skipped to align a read conforming to intron definitions in STAR_; :smc:`INTR`) in :smc:`LIBR` or :smc:`COLLR` can be displayed. For this, limits on the x-axis can be set via :smc:`MINGAP`, :smc:`MAXGAP`, :smc:`INTSKIP`, with labels shown after each :smc:`INTGAP`. Use option ``-ld`` to display the *length-distributions of separate libraries* for the set :ref:`kind <kind>` of reads (change with ``-k``). :ref:`Group <grouping>` libraries with ``-g``, select mapping type with ``-ma``, or show :ref:`stranded <strand>` data with ``-st`` in combination with ``-ld`` or ``-lo``. 

.. figure:: /../_static/images/h99_readlengths_all.png
   :name: h99rdlngs
   :align: right
   :width: 1866 px
   :height: 939 px
   :scale: 25%

   Overview of length distribution of specified reads.

   | Counts for reads from all libraries [#sirns]_, sorted by start nucleotide 
   | and length, were summed and converted to percentages.  
   | Output from ``coalispr showcounts -lo 1``.
   |


By default, figure titles are turned off with the *notitles* option ``-nt 1``; the relevant information is retained in the window title and included in the filename suggested when saving an image. Use ``-nt 0`` to display figure titles.

As expected, unspecific reads are characterized by an almost homogeneous distribution of fragment lengths, while specific reads peak around 21-23 nt for cDNAs beginning with a T. These are also slightly enriched in the unspecific reads, maybe due to being :term:`unselected`.  

Diagrams of reads mapping to :term:`extra`\neous sequences [#backgr]_ demonstrate that RNAi in strains is triggered upon introduction of foreign nucleic acids: siRNAs are formed against transcripts from bacterial origin of replication, *cas9* and especially target CRISPR/Cas guide RNAs transcribed by means of an U6 promoter [Wang-2016]_.

|

.. _regi:


``region``
``````````
The script called with ``coalispr region`` provides an insight into the length distribution and number of reads that are found in a particular region of the genome (say rDNA). After entering the chromosome name (with option ``-c``), a dialog asks for inputting the region coordinates or these can be given directly with option ``-r`` (like with ``coalispr showgraphs -r``). Option ``-st`` controls whether reads aligning to the :smc:`PLUS` or :smc:`MINUS` strand are analysed (default is both, :smc:`COMBI`). The samples to be counted can be set with option ``-s`` (by default the controls). The terminal provides :ref:`feedback <regrunexampl>` and count results are saved to :smc:`TSV` files and displayed as bar diagrams, which are automatically saved. For proper parsing of all options, place the ``-r`` option plus coordinates at the end of the command.

.. tip:: 
   The ``-r`` and ``-c`` options work in an identical manner in ``coalispr showgraphs`` and ``coalispr region``.

   - Facilitate region analysis for chromosome ``K`` by: 
      - Run in a terminal ``coalispr showgraphs -c K -w2``.
      - Zoom into the region of interest. 
      - Register chromosome coordinates by clicking the x-axis. 
      - The output is shown in the terminal as ``K:<region>``. 
      - Highlight ``<region>`` and copy with ``Shift+Ctrl+C``.

   - Open another terminal for running ``coalispr region -c K -s1 -st 1 -r <region>``
      - Paste ``<region>`` with ``Shift+Ctrl+V``.
  
   - Retrieve a display of the same chromosomal locus with ``coalispr showgraphs -c K -w2 -r <region>``.

To reduce counting time, a limited number of categories are compared, which is set by option ``-cf``. By default libary reads (:smc:`LIBR`) and collapsed, i.e. cDNA, reads (:smc:`COLLR`) are counted. The number of reads that were skipped because of mismatches or point-deletions are reported too. The collection of counters used for this function is defined by the constant :smc:`REGCNTRS` in the ``2_shared.txt`` configuration file. 

.. figure:: /../_static/images/h99-rDNA-minus-counts.png
   :name: regcnt_h99-rDNAhw2
   :align: left
   :width: 1111 px
   :height: 275 px
   :scale: 50%
   :figwidth: 100%
   
   Minus strand counts for the *C.*\ |nbsp|\ *neoformans* rDNA unit on chromosome 2.
    
   | Output from ``coalispr region -c2 -r 271985-279663 -st 3 -s2``. 
   |

This region analysis demonstrates that no reads are specially enriched among :term:`rRFs` in *Cryptococcus* that would fit the siRNA binding pocket on Argonaute. Here, rRFs form a large but biologically uninformative background signal. When there is a large variability between libraries, this would undermine the possibility to normalize against rRNA background or the number of total mapped reads which contains :ref:`a large but inconsistent fraction <h99libcnts>` of :term:`unspecific` reads that are mostly rRFs.

Other options are available, such as for inclusion of any unused (``-x``) or redundant mutant (``-rm``) samples as well as figure titles (``-nt``).

|

.. _annota:


``annotate``
````````````
Count files generated with ``coalispr countbams`` can be compared to reference files and annotated with available gene information. For this, the annotation files :smc:`GTFSPECNAM` for :term:`specific` reads and :smc:`GTFUNSPNAM` for :term:`unspecific` reads are used according to the values for above constants in the :ref:`experiment file <exp>` (:smc:`EXPFILE`). With option ``-rf 1`` annotations in :smc:`GTFREFNAM` for :smc:`REFERENCE` reads can be included as well, extending the processing time. The annotation files are the same as used in the displays created with ``coalispr showgraphs``.

By default a count file for specific :term:`uncollapsed` library reads (:smc:`LIBR`, :smc:`ALL`) is annotated; with *library-choice* option ``-lc 2``, the input will be a count file for cDNAs (:term:`collapsed` reads, :smc:`COLLR`). 

Annotated files are saved to :smc:`OUTPATH` (that is :smc:`SAVEIN / OUTPUTS / EXP`, normally the experiment folder in ``Coalispr/outputs/`` in the work directory) and sorted on value in descending order. To keep annotated files organised according to genome position, turn the *sort-value* option off: ``-sv 0``. 

Other options are: ``-k2`` to change the kind of reads to unspecific; ``-st {1,2,3}`` to define strand-specificity for :smc:`COMBINED` (default), :smc:`MUNR` (``-st 2``) or :smc:`CORB` (``-st 3``); ``-ma {1,2}`` to select count files for :smc:`UNIQ` reads or multimappers (:smc:`MULMAP`). Count numbers can be formatted to their *log2* value with option ``-lg 1`` and output files can include unused samples by setting option ``-x 0``.  

For examples see the :ref:`annotate-section <ms45_annot>` in the tutorial ':doc:`/tutorials/mouse`' or :ref:`this paragraph <annot_h99>` in the tutorial ':doc:`/tutorials/h99`'.

|

``groupcompare``
````````````````

Described above, the command ``coalispr showcounts -ld`` produces an overview of detected readlengths for mapped RNAs for each sample. By including option ``-g`` the grouping of samples can be set. With this command, all samples will be included separately in the figure. 

To compare only a selection of samples according to a particular type (say, method, fraction, condition or mutation) the command ``coalispr groupcompare -g`` might provide a cleaner view. This command generates a grouped bardiagram showing the *average* (:smc:`MEAN` or :smc:`MEDIAN` with option ``-av``) with error bars for the standard deviation between the values for the samples in each group. After setting the major type for the comparison with the required *group* option ``-g``, samples are selected according to the setting for *trim selection* ``-ts``. With option ``-5e`` the start-nucleotide of reads to be examined can be chosen, while *read length* option ``-rl`` sets the minial and maximal lengths of reads to be displayed. As for the ``coalispr showcounts`` command, specific views for *strand*\ s (``-st``), uniq - or multimappers (``-ma``), or the *kind* of read (``-k``, :smc:`SPECIFIC` or :smc:`UNSPECIFIC`) can be generated; any unused (``-x``) or redundant mutant (``-rm``) samples could be included as well as figure titles (``-nt``).

|

``info``
````````

.. figure:: ../_static/images/reads_vs_settings.png
   :name: rdssttngs
   :align: right
   :width: 1346 px
   :height: 732 px
   :scale: 35%

   Settings vs. number of contiguous regions [#sirns]_ 

   | Effect of thresholds on the number of regions with specific (top) or 
   | unspecific (bottom) uncollapsed reads detected in the data; dotted 
   | line indicate configured settings (with ``coalispr info -r2``)
   |
   
This command provides information on the current session, like the setting for ``setexp`` (by default), memory-usage of the data in Pandas_, the path to configuration files or `Experiment file`_.

The *regions* option ``-r`` helps to assess which parameter settings fit the quality of the data. Check the logs for messages ``empty array, no data, thresholds too high? No specific hits?`` after running this option [#empdat]_. For some chromosomes high thresholds can prevent detection of :term:`specific` signals so that no regions are found. Such ``empty`` chromosomes cannot be displayed with ``coalispr showgraphs`` by lack of bins with data.

.. _unspclg10:

*UNSPECLOG10.* High signal-to-noise ratios allow for stringent separation of :term:`specific` from :term:`unspecific` reads. For this, use a large value for :smc:`UNSPECLOG10`. This parameter sets the exponent for the 10\ :sup:`UNSPECLOG10`-fold difference that defines the threshold when positive and negative reads overlap (see :ref:`explanatory figure <sttngs>`). With stringencies set too high, no :term:`specific` peaks can be specified for a chromosome. Such a combination of settings can not be used. In the :ref:`settings figure <rdssttngs>`, this is shown by an absence of region numbers [#opts]_ (see panels with :smc:`UNSPECLOG10` >= 1.0) [#sirns]_. 

:smc:`UNSPECLOG10` values have not a big influence on the number of regions with :term:`unspecific` reads. That many more regions with :term:`collapsed` reads are found relates to the leveling up, whereby single reads in a library gain more visibility (visualize with ``coalispr info -r3``) [#cllps]_.

.. _usgps:

*USEGAPS, UNSPCGAPS.* Stringent thresholds can lead to gaps between peaks when 'lower' regions drop out. With :smc:`USEGAPS` a tolerance is set that creates a contiguous region of reads when its peaks are closer together than the gap-setting [#bnsstp]_. A low :smc:`USEGAPS` reduces the number of peaks that are taken together and results in a high number of regions with specified reads. When :smc:`USEGAPS` is set too high, sections are fused that could represent separate regions when these are relatively close together [#opts]_. For defining segments used in the counting of :term:`unspecific` reads, peaks are not fused; by default the gap (:smc:`UNSPCGAPS`) is kept minimal, i.e. equal to :smc:`BINSTEP`.

.. _lg2bg:

*LOG2BG.* To minimize the number of regions with very low level of specified reads, the signals need to be higher than a threshold of 2\ :sup:`LOG2BG` [#opts]_.
|

``test``
````````
To get an idea of how various sections of |prgnam| perform, ``coalispr test -tp`` saves test profiling information to the logs for the commands ``showgraphs``, ``countbams``, ``region`` and ``annotate``. Number of lines from the report (``-no``) can be set and - for some commands - the kind (``-k``) of reads to be analysed.



|
|

Troubleshooting
---------------

|prgnam| has been developed and tested on a computer operating with Slackware_ linux. Hiccups in other environments can be expected. The program is run from the command-line which can also show errors or warnings which interfere with the feedback provided by |prgnam|. Some of the messages are not from the program but relate to the context of running Python_ and Matplotlib_ and can be removed by changing a :ref:`configuration <const>` setting. 

When the program is not behaving, please consider:

|

Log files
`````````
To help solve problems, error messages generated by Python_ are logged, including some feedback on commands and their parameters. The log files (``run-log.txt``, :smc:`LOGFILNAM`) are stored here:

``Work-environment / Coalispr / logs / :smc:`EXP` / run-log.txt``

that is, in the ``logs`` (:smc:`LOGS`) directory in the |prgnam| folder that was set up in the work environment by  ``coalispr init``, and placed in a sub-folder with the name of the current experiment (:smc:`EXP`, chosen via ``coalispr setexp``).

Maybe the log files can give an idea where the error comes from and how it can be solved. Please, include the relevant section of the ``run-log.txt`` when reporting an issue_ at the |prgnam| repository.

|

.. _ice32:

Backends
````````

:smc:`BACKEND`\s are the programs matplotlib uses to present a graphical users' interface (GUI). You will see that this setting determines the look and feel of displayed graphs (with ``showgraphs``, ``shocounts``, ``region`` or ``info``. A nice backend is "QtAgg", but when many samples are analyzed some ``showcount`` options can lead to a crash with:

.. code-block:: text

     ICE default IO error handler doing an exit(), .. errno = 32

Errors or warnings with "GTK4Agg" can also occur, like:

.. code-block:: text

     Warning: Attempting to freeze the notification queue for object 
     GtkImage[0x5e7f690]; 
     Property  notification does not work during instance finalization.
     lambda event: self.remove_toolitem(event.tool.name))


In such cases change :smc:`BACKEND` in the :smc:`EXPTXT` to, say, "TkAgg" or "GTK3Agg".

|

.. _pnds2:

Pandas-2.x
``````````

For some reason ``python.shelve`` that is at the heart of storing all dataframes with bedgraph values in a ``.pkl`` format, requires a particular file not present in ``pandas-2.x``. This leads to:

.. code-block:: text

     ModuleNotFoundError: No module named 'pandas.core.indexes.numeric'

Place a link/copy of ``coalispr.resources.numeric.py`` in ``python3/site_packages/pandas/core/indexes/`` (see :ref:`here <bckpbd>` in :doc:`/errors`).


|
|

     
=====

Notes
'''''


.. [#spl] For example, spliced transcripts can be expected in the case of *Cryptococcus (de)neoformans* species, with a very high density of introns (>5 per gene; see [Loftus-2005]_, [Janbon-2014]_, [Janbon-2018]_)
.. [#str] An aligner as STAR_ comes with commands to create bedgraphs from bam-alignments (see |tuts|). Note that strand-specific information has to be separated over two files, one for plus-strand data, the other for minus-strand data (see :term:`bedgraph` in the :doc:`glossary`). 

   Bedgrapgh files that cover both strands by using positive and negative values in the 3rd column need to be split into two files with positive values. This can be done as exemplified with ``coalispr.resources.share.convert_plusmin_bedgraph_to_plusplus.py``.
.. [#cig] The uniq vs. multimap information is embedded in the socalled ``CIGAR`` string, which can be defined in an aligner as STAR_. Note that for alignment (and therefore the counting) of :term:`uncollapsed` and :term:`collapsed` reads, different aligner settings for multimappers might be needed (like with STAR_) to get the correct information. The constants :smc:`MULMAPCOLL` and :smc:`MULMAPUNCOLL` in ``3_EXP.txt`` are a reminder of this.
.. [#unird] Finding uniq reads in the bam files directly, bypasses the need to assess :smc:`UNIQ` bedgraphs by themselves. These files, when output by, say, STAR_, have to be recognized though: The label :smc:`UNIQ` used in names of bedgraph files of unique read-mappings should be defined in ``3_EXP.txt``. These files will be ignored unless they are the only ones available.
.. [#col] Color-choices hopefully accommodate for (some) color-vision differences; graphs have been tested on https://asada.website/webCVS/. Green has not been used and although red might be a poor choice too, its association with 'stop', and 'no' made it the preferred candidate for referring to :term:`negative control` or :term:`unspecific` data. Color definitions can be changed easily in ``2_shared.txt``.
.. [#jnsht] ``coalispr showgraphs`` in tested versions of jupyter notebook only showed png images; all interactive features were gone. It seemed better to focus development of |prgnam| on the command line interface. This also evades the complexity and overhead to maintain code in response to development of these notebooks.
.. [#coal] For ``coalispr -h`` an option list with details as described in the text is shown:

   .. code-block:: text

        usage: coalispr init | setexp | storedata | showgraphs | countbams | showcounts | region | annotate | groupcompare | info | test
                [-v,--version  -h,--help]

        Coalispr: 'COunt ALIgned SPecified Reads'

        options:
          -v, --version  show program's version number and exit
          -h, --help     Show this help message and exit.

        commands:
          
            init         Provide a name for session/experiment; set path to folder for Coalispr output
                         and configuration files. Before continuation, adapt the configuration files.
            setexp       Set experiment/session to -e with path -p to its configuration file.
            storedata    Process bedgraph files for aligned-reads, make or restore backups, and rename
                         samples.
            showgraphs   Compare series of bedgraphs -w for chromosome -c using samples -s for aligned
                         reads of type -t . Show side panel with sub-legends (-sp). Start with region
                         (-r), show or write to file (-wg)
            countbams    Count bam alignment files with 'collapsed' reads using segments found in
                         'uncollapsed' bedgraphs; divide segments in -b bins; select for kind -k; and
                         include unselected alignments -u for Unspecific reads (with -k2). Tolerate
                         point-deletions (-pd) or mismatches (-mm). Force counting (-f).
            showcounts   Display total raw counts (-rc) for mapped and unmapped reads, or total
                         library counts (-lc), on log2 (-lg) scale and bin (-bd) or length (-ld)
                         distributions for separate 'Specific' or 'Unspecific' libraries (-k) or an
                         overview (-lo); select only reads mapping to strand -st; group libraries (-g)
                         by 'Category', 'Method' or 'Fraction'; select mapper type (-ma) to 'uniq' or
                         'multimapper' or check hit-number distributions for 'multimappers' or those
                         with introns (-md, -mo).
            region       For region -r on chromosome -c, check counts and distribution of read-lengths
                         for controls (-s1), including mutants (-s2) or a sample selection (-s3).
                         Compare different counts (-cf), tolerate point-deletions (-pd) or mismatches
                         (-mm). Plot on normal or log2 scale (-lg).
            annotate     For reads -lc annotate counts for kind -k, mapper -ma and strand -st; include
                         ref -rf, order libraries by values (-sv) and use log2 scale for counts (-lg).
            groupcompare
                         Groupwise (-g) comparison of length distributions (-ld) for reads with 5' end
                         -5e and readlengths -rl, showing standard deviations with respect to average
                         -av for selected samples (-ts) with mapping frequency -ma and of kind -k for
                         strand -st.
            info         Describe file paths (-p); show detected number of regions with 'specific'
                         reads as a result of parameter settings (-r); give experiment name or
                         calculate memory-usage of Coalispr data in Pandas (-i).
            test         Test or profile (-tp) commands of Coalispr with -no lines of report output.
        
                                      
                    
.. [#pwd]  Note that when the path to the directory containing the ``Coalispr`` work folder has to be set (when asked for in a command), this path does not contain the '``Coalispr``' bit.
.. [#scrpt]  Scripts for making the plots invoke Pandas_, Matplotlib_, Numpy_ or Seaborn_ modules.
.. [#sirns]  Shown are traces for *C.*\ |nbsp|\ *neoformans* H99 based on published siRNA libraries ([Dumesic-2013]_, [Burke-2019]_); for figures based on ``showgraphs`` and ``showcounts`` siRNA reads were specified with a :smc:`UNSPCLOG10` setting of 0.78 giving a ~6-fold difference. The figures are prepared in the tutorial ':doc:`/tutorials/h99`'.
.. [#cllps]  The leveling-up by collapsing the data is because only coverage is taken into account, not the number of siRNA molecules of same length and nucleotide sequence. It is not only noteworthy that collapsing still enables isolation of siRNA targeted regions of transcripts, but that the anti-sense siRNA levels are not exceeding those of the sense siRNAs so much as observed for :term:`uncollapsed` data. This suggests that the anti-sense siRNAs are preferentially amplified, presumably during the RNAi response in the cell (rather than in the PCR reactions during library preparation).
.. [#xaxisact] After zooming, coordinates spanning the view-window can be printed to the terminal (and the log file) by clicking the x-axis. 
.. [#dumes] This observation has been discussed with Hiten Madhani, when he visited the University of Edinburgh in 2017. The GTF they had used could no longer be found and might have been premature, with many wrong exon and intron annotations; the *C.*\ |nbsp|\ *neoformans* H99 genome sequence was published a year later [Janbon-2014]_ and annotations given therein (and released since by EnsemblFungi_ or [Wallace-2020]_)  do not yield intron-siRNA overlaps as reported by [Dumesic-2013]_). See also the tutorial ':doc:`/tutorials/h99`'.
.. [#tagbam] By changing :smc:`TAGSEG` or :smc:`TAGBAM` :term:`constant`\ s in the configuration file the input for ``countbams`` can be adapted to the kind of available data.
.. [#char] Different values for siRNA characteristics :smc:`BAMSTART` and :smc:`BAMPEAK` can be set in ``3_ExpSessionName.txt``.
.. [#b2bg] Or when an alternative script that can extract raw bedgraph values from bam alignment files (:smc:`BAM2BG`) has been set in ``3_ExpSessionName.txt``.
.. [#xbam] This would be the case when default settings were used during the counting of :term:`unspecific` reads (with *kind* option ``-k2``) and :term:`collapsed` unselected reads were written to the extra alignment files, i.e. with command ``countbams -k2 -wb 1``. Note that traces of unselected reads can only be displayed alongside the same type of bedgraph data (here 'collapsed'; so use *type* option ``-t2`` with the command ``showgraphs``)
.. [#mmu45s] For example the mouse 45S rDNA gene of which only the 18S section has been incorporated in the annotations despite sequences for the complete rDNA unit have been published (see the :doc:`mouse tutorial </tutorials/mouse>`).
.. [#avail]  When available. In the |tuts| programs are used that make this possible.
.. [#meth] To group by method makes sense when more than one RNA-isolation procedure has been used to obtain the input material for library preparations. This is set in ``3_ExpSessionName.txt`` using the :smc:`METHODS` entry. 
.. [#ripin] RNA released from immunoprecipitated proteins tends to have less carry-over of rRNA fragments in the sample, when the tagged protein is abundant.
.. [#uniq]  Omitted are the multimappers, i.e. the reads that align to tRNA, rRNA, some transposons and other repeated sequences.
.. [#backgr] These observations relate to *C.*\ |nbsp|\ *deneoformans* (see :doc:`\background`).
.. [#empdat] At :smc:`UNSPECLOG10` value of ``1.3`` no specific data was found for mitochondrial DNA (chromosome``MT``) at values of :smc:`LOG2BG` >= 9.
.. [#opts]  In ``3_ExpSessionName.txt``, the range of options for :smc:`UNSPECLOG10` are defined in a list, :smc:`UNSPECTST`; those for :smc:`USEGAPS` in :smc:`UGAPSTST` and for :smc:`LOG2BG` in :smc:`LOG2BGTST`. Trying out other options is easy: change the list values and rerun ``coalispr setexp`` for the session before running ``coalispr info -r 1``.
.. [#bnsstp] Its value is a multitude of the :smc:`BINSTEP` parameter that defines the length of sections the genome is split into for comparing bedgraph values (which reduces the 1nt resolution of the sequencing data to the value of :smc:`BINSTEP`).



