.. role::  raw-html(raw)
   :format: html

.. |prgnam| replace:: :program:`Coalispr`
.. |tuts| replace:: :doc:`tutorials </tutorials>`   
.. |37C| replace:: 37\ :sup:`o`\ C 
.. .. |del| replace:: :raw-html:`&#x0394;`

Multimapping 21-mers in rde1Δ
=============================

In the tutorial ':doc:`/tutorials/h99`' it was observed that in the strain lacking Rde1 most multimappers had a length of 21 nt, rather than 22 nt as normally found. Appearance of 21-mer multimappers can be checked a bit further:

.. table::
   :name: rde1mm
   :align: left



   +-------------+-------------+----------+----------+-----------+----------+----------+------------+-------------+----------+
   | Sample                    | cDNA counts  (collapsed)                   |  Multimapper read counts (uncollapsed)         |
   +=============+=============+==========+==========+===========+==========+==========+============+=============+==========+
   | *Name*      | *SRA*       | *20-mer* | *21-mer* | *22-mer*  | *23-mer* | *20-mer* | *21-mer*   |  *22-mer*   | *23-mer* |
   +-------------+-------------+----------+----------+-----------+----------+----------+------------+-------------+----------+
   | rde1Δ       | SRR8697586  |  9973    |  12924   | **15972** |  12859   |  375990  | **723258** |  550248     |  446487  |
   +-------------+-------------+----------+----------+-----------+----------+----------+------------+-------------+----------+
   |             | SRR8697587  |  9627    |  13294   | **16094** |  13380   |  309394  | **594001** |  451775     |  403168  |
   +-------------+-------------+----------+----------+-----------+----------+----------+------------+-------------+----------+
   | wild type   | SRR646636   | 32990    |  45271   | **53001** |  42888   |  322177  | 741118     | **1557249** | 1177401  |
   +-------------+-------------+----------+----------+-----------+----------+----------+------------+-------------+----------+



To find counts for reads with matches from 20 to 23 nucleotides in the alignments, as shown in this :ref:`table <rde1mm>`, the following approach can be taken. As a control, cDNAs and wild type multimappers are counted. 

First, change directory, for the cDNAs:

- ``cd STAR-analysis0-h99_collapsed/SRR8697586_collapsed_0mismatch-h99/``

Then, get multimapper counts (for above table) with ``samtools`` and ``grep``.

| (``-v`` for *take the inverse*, ``-c`` for *count* and ``-w`` for *search whole word*):

- ``samtools view samtoolsAligned.sortedByCoord.out.bam | grep -v "NH:i:1" | grep -cw "20M"``

- ``samtools view samtoolsAligned.sortedByCoord.out.bam | grep -v "NH:i:1" | grep -cw "21M"``

- ``samtools view samtoolsAligned.sortedByCoord.out.bam | grep -v "NH:i:1" | grep -cw "22M"``

- ``samtools view samtoolsAligned.sortedByCoord.out.bam | grep -v "NH:i:1" | grep -cw "23M"``


Repeat these commands for the replicate:

- ``cd ../../STAR-analysis0-h99_collapsed/SRR8697587_collapsed_0mismatch-h99/``

And for the multimapping reads:

- ``cd ../../STAR-analysis0-h99_uncollapsed/SRR8697586_uncollapsed_0mismatch-h99/``
- ``cd ../../STAR-analysis0-h99_uncollapsed/SRR8697587_uncollapsed_0mismatch-h99/``

and for a wild-type control too:

- ``cd ../../STAR-analysis0-h99_collapsed/SRR646636_collapsed_0mismatch-h99/``
- ``cd ../../STAR-analysis0-h99_uncollapsed/SRR646636_uncollapsed_0mismatch-h99/``

To get the numbers for reads of interest - the 21-mers - for each chromosome do (before changing directory):

- ``for i in {1..14}; do echo "$i: $(samtools view samtoolsAligned.sortedByCoord.out.bam | grep -v "NH:i:1" | awk "\$3==$i" | grep -cw "21M" )"; done``

| (``awk '$3=1'`` will select lines when the third field - the chromosome name - is ``1``; in the full command the chromosome names are passed in as ``$i``, a bash-variable; because ``bash`` has to process the awk command as text, the awk-qualifier ``$3`` needs escaping and the whole is in between double quotes to allow interpretation of ``$i``.)


This table collects the results:


.. table::
   :name: rde1mmschr
   :align: left



   +----------------+-------------+-------------+----------------------+
   | Sample         |  rde1Δ                    |  wildtype            |
   +================+=============+=============+======================+
   | *SRA*          |  SRR8697586 |  SRR8697587 |  SRR646636           | 
   +----------------+-------------+-------------+----------------------+
   | *Chromosome*   | *Multimapper read counts 21-mer*                 | 
   +----------------+-------------+-------------+----------------------+
   |  1             |   11036     |   11510     |    99094             | 
   +----------------+-------------+-------------+----------------------+
   |  2             |  687782     |  558693     |   130603             |
   +----------------+-------------+-------------+----------------------+
   |  3             |    2594     |    2666     |    59705             |  
   +----------------+-------------+-------------+----------------------+
   |  4             |    1271     |    1312     |    28507             |
   +----------------+-------------+-------------+----------------------+
   |  5             |    1087     |    1072     |    69644             |
   +----------------+-------------+-------------+----------------------+
   |  6             |     896     |     850     |    63315             |
   +----------------+-------------+-------------+----------------------+
   |  7             |    3873     |    4045     |    26985             |
   +----------------+-------------+-------------+----------------------+
   |  8             |     777     |     869     |    28801             |
   +----------------+-------------+-------------+----------------------+
   |  9             |    7885     |    7442     |    67859             |
   +----------------+-------------+-------------+----------------------+
   | 10             |     527     |     566     |    16059             |
   +----------------+-------------+-------------+----------------------+
   | 11             |    1460     |    1415     |    72215             |
   +----------------+-------------+-------------+----------------------+
   | 12             |     987     |     828     |    14030             |
   +----------------+-------------+-------------+----------------------+
   | 13             |    1261     |    1299     |    50498             |
   +----------------+-------------+-------------+----------------------+
   | 14             |     521     |     442     |    11100             |
   +----------------+-------------+-------------+----------------------+


With the exception of chromosome 2, to all chromosomes of the wild type 8 to 30-fold more reads are mapped than in the rde1Δ strain. In the mutant, the vast majority of reads map to chromosome 2. Because the counted reads represent a mix of specific and unspecific reads of 21 nt, hits can come from unspecific regions. Given that rRNA reads are multimappers on chromosome 2, these numbers point to this chromosome.

With the following commands we can narrow this down; run in each folder ``SRR..._uncollapsed_0mismatch-h99/`` a command to find the number of reads that map to chromosme 2:

- ``samtools view samtoolsAligned.sortedByCoord.out.bam | grep -v "NH:i:1" | awk "\$3==2" | grep -cw "21M"``

and then one that retrieves the counts of reads that align within the rDNA locus between ``2:270000-284000``:

- ``samtools view samtoolsAligned.sortedByCoord.out.bam | grep -v "NH:i:1" | awk "\$3==2" | awk '$4 > 270000 && $4 < 284000' | grep -cw "21M"``

This gives :

.. table::
   :name: rde1mmschr2rdna
   :align: left
 
   +----------------+-------------+-------------+----------------------+
   | Sample         |  rde1Δ                    |  wildtype            |
   +================+=============+=============+======================+
   | *SRA*          |  SRR8697586 |  SRR8697587 |  SRR646636           |
   +----------------+-------------+-------------+----------------------+
   | *Chromosome*   |  *Multimapper read counts 21-mer*                |
   +----------------+-------------+-------------+----------------------+
   |  Total         |  723258     |  594001     |   741118             |
   +----------------+-------------+-------------+----------------------+
   |  2             |  687782     |  558693     |   130603             |
   +----------------+-------------+-------------+----------------------+
   |  270000-284000 |  684218     |  555291     |    32328             |
   +----------------+-------------+-------------+----------------------+


This approach points out that most 21-mers in rde1Δ are linked to the rDNA. Whether these represent siRNAs or rRFs is not clear. An analysis with ``coalispr region``, however, revealed that siRNAs antisense to rRNA can be generated which were highly abundant in rde1Δ (see :ref:`Figure 13 <regcnt_h99rdna>` in the :doc:`tutorial </tutorials/h99>`).


After these tests return to ``Burke-2019/``:

- ``cd ../../``


