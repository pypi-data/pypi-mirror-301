.. role::  raw-html(raw)
   :format: html

.. |Dbox|  replace::  :raw-html:`<span class="mononorm">caga</span>`
.. .. |Cbox|  replace::  :raw-html:`<span class="mononorm">rugauga</span>`
.. |nbsp| replace:: :raw-html:`&#x00A0;`

.. .. |extrBP|  replace:: ..S rRNA 
.. |extr|  replace::  :raw-html:`<span class="mononorm">TACATTAC</span>`
.. |targetRNA-1|  replace:: 5.8S rRNA
.. |target-1| replace:: :raw-html:`<span class="mononorm">(gtaatgtg)[a]att<a href="../18s-tab.html#SNORD96_5.8S" title="5.8S target">G</a>cagaat</span>`
.. |ortholog-1| replace:: :raw-html:`human <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300555">SNOR96A</a>, <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300461">SNOR96B</a>`
.. |targetRNA-2|  replace:: 25S rRNA
.. |target-2| replace:: :raw-html:`<span class="mononorm">ctg<a href="../18s-tab.html#SnoR29_25S" title="25S target">T</a>tgagcttg</span>`
.. |ortholog-2| replace:: :raw-html:`plant <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Arabidopsis_thaliana300058">SnoR29-1</a>, <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Arabidopsis_thaliana300057">SnoR29-2</a>, <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Aegilops_tauschii300644">snoZ107_R87</a> or fission yeast <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Schizosaccharomyces_pombe300057">snR88</a> (D' guide)`


In *C.*\ |nbsp|\ *neoformans* and *C.*\ |nbsp|\ *deneoformans*, the gene for UTP17 harbors two box C/D snoRNAs, orthologues of human SNORD96 and plant SnoR29 (snoZ107_R87).

.. figure:: /../_static/images/snoRNAs/utp17_h99_igb.png
   :name: utp17_h99_igb
   :align: left
   :width: 1389 px
   :height: 646 px
   :scale: 40%
   :figwidth: 100%

SNORD96
=======

- SNORD96_intronic-boxCDsnoRNA-97nt-in-UTP17-CNB01450
- Within  5\ :sup:`th` intron of CNB01450 (CNAG_03645) for UTP17
- Predicted target in |targetRNA-1|\ : |target-1|
- Extension of base pair interaction (within brackets) is supported by an accessory guide |extr|
- Orthologue of |ortholog-1|
- In *C.*\ |nbsp|\ *amylolentus*, C.*\ |nbsp|\ *wingfieldii*, or *C.*\ |nbsp|\ *floricola* two versions of SNORD96 were found.
- Assignment of D' box was not attempted by lack of phylogenetic support


.. figure:: /../_static/images/snoRNAs/SNORD96-align.png
   :name: snord96-align
   :align: left
   :width: 1131 px
   :height: 255 px
   :scale: 40%
   :figwidth: 100%


.. rst-class:: mononote

> AE017342.1:436588-436684 Cryptococcus neoformans var. neoformans JEC21 chromosome 2 sequence :raw-html:`</br>`
TTCTCGGATGAGAACTTCTTATACATTACTGTCATCCTTATTCGTACTCCTTTTTCATCGGAGGAATGTG :raw-html:`</br>`
GCGACTTCATTCTGCAATCCTGATCCT

|
|

.. _snor29a:
   
SnoR29
======


- SnoR29_intronic-boxCDsnoRNA-nt-in-UTP17-CNB01450
- Within  6\ :sup:`th` intron of CNB01450 (CNAG_03645) for UTP17
- Predicted target in |targetRNA-2|\ : |target-2|
- Orthologue of |ortholog-2|
- Duplicate (snoZ107-SnoR29b) is present in JEC21 at 2:1309857-1309770:-1 in :doc:`intron CNB04560 for F-actin capping protein <cnag03967_z107>`, but snoRNA from this locus seems poorly expressed.
- In other *Cryptococcus* species multiple versions of this snoRNA are found as well.
- Predicted modification as in fission yeast snR88 (see also snR88 :ref:`D-box orthologue <snr88dbox>`), but is shifted four nucleotides from that in plant, which uses a different D' box (\ |Dbox| \).

.. figure:: /../_static/images/snoRNAs/SnoR29-align.png
   :name: snor29-align
   :align: left
   :width: 1208 px
   :height: 606 px
   :scale: 40%
   :figwidth: 100%


.. rst-class:: mononote

>AE017342.1:436831-436916 Cryptococcus neoformans var. neoformans JEC21 chromosome 2 sequence :raw-html:`</br>`
TTCCTATGATGAGCAACTTTTTTCAAGCTCAACAGTCCTACTATTACTGAGGATACCCCTCTTCTTCTTT :raw-html:`</br>`
ATCTCTGAGGATGTTT


|
|
|
|
|
|

=======

- Image source SNORD96:
  
.. rst-class:: asfootnote

::

        # STOCKHOLM 1.0
        #=GF RW van Nues, July 2023
        #=GF https://coalispr.codeberg.page/paper
        Annnot/1-41                 ----------RTGATGA----------GUGUAAUG-------------------------------------------RTGATGA-----UAAGACGUUA-CTGA-------
        #=GS SNORD96/1-97 DE intronic-boxCDsnoRNA-97nt-in-UTP17-CNB01450 ncrna 2:436588:436684:1 AE017342.1:436588-436684 Cryptococcus neoformans var. neoformans JEC21 chromosome 2 sequence
        SNORD96/1-97                ------TTCTCGGATGAGAACTTCTTATACATTAC-----TGTCATCCTTATTCGTACTCCTTTTTCATCGGAGGAATGTGGCGACTT-CATTCTGCAATCCTGATCCT---
        #=GS H99/1-95 DE CP003821.1:428365-428459 Cryptococcus neoformans var. grubii H99 chromosome 2, complete sequence
        H99/1-95                    ------TTCTCGGATGAGAACTTCTTATACATTAC-----TGTCATCCTTATTCGTACTCCTTTTTCATCGGAGGAATGTGGCGACTT-TATTCTGCAATCCTGATC-----
        #=GS R265/1-98 DE CP025762.1:c1334432-1334335 Cryptococcus gattii VGII R265 chromosome 4
        R265/1-98                   -----TACCTCGGATGAGAACTTCTTATACATTAC-----TGTCATCCTTATTCGTACTCCTTTTTCATCGGAGGAATATGGCGACTT-CATTCTGCAATACTGATTCT---
        #=GS WM276/1-98 DE CP000287.1:c1375604-1375507 Cryptococcus gattii WM276 chromosome B, complete sequence
        WM276/1-98                  -----CACCTCGGATGAGAACTTCTTATACATTAC-----TGTCATCCTTATTCGTACTCCTTTTTCATCGGAGGAATATGGCGACTT-CATTCTGCAATACTGATTCT---
        #=GS KwoMan/1-90 DE ASQF01000041.1:c321699-321610 Kwoniella mangroviensis CBS 8886 cont1.41, whole genome shotgun sequence
        KwoMan/1-90                 -------GAAAAGATGAACAA-CTTTTCACATTCAC----TGTCATCCTTATACGGATACC-----CTTCGGGGTG--GTGGCGACTAACATTCTGCAATCCTGATTTA---
        #=GS KwoHev/1-96 DE ASQC01000125.1:c86192-86097 Kwoniella heveanensis CBS 569 cont2.125, whole genome shotgun sequence
        KwoHev/1-96                 -------TCTCGGATGAGTCA-TTTTTCACATTCAC---TAGTCATCCTTATACGGACCAA--CCTCCTCGGAGGA-CATGGCGACTAACATTCTGCAATACTGAACAAT--
        #=GS KwoSha/1-101 DE NQVO01000042.1:c130415-130315 Kwoniella shandongensis strain CBS 12478 scaffold00042, whole genome shotgun sequence
        KwoSha/1-101                -------TTCCTGATGAGCATTCATAACACATTACATTACTGTCATCCTTTTTCGGTAA---TTCTCCTCGGAGAG-TATGTCGACCAACATTCTGCAATCCTGATCTTTTC
        #=GS CryAmy/1-94 DE MEKH01000001.1:520809-520892 Cryptococcus amylolentus CBS 6273 supercont2.1, whole genome shotgun sequence
        CryAmy/1-94                 -------ATTCGGATGAGACT-CTTTATACATTACA------TCATCCTTATTCGTACCCC-TTTTCTTCGGGACATAATGGCGACT-ACATTCTGCAATACTGAAATCA--
        #=GS CryWin/1-92 DE AWGH01000005.1:c417549-417458 Cryptococcus wingfieldii CBS 7118 supercont1.5, whole genome shotgun sequence
        CryWin/1-92                 -------ATTCGGATGAGACT-CTTTATACATTACA------TCATCCTTATTCGTACCCC-TTTTCTTCGGGACATAATGGCGACT-ACATTCTGCAATACTGAAAC----
        #=GS CryFlo/1-91 DE RRZH01000002.1:559607-559697 Cryptococcus floricola strain DSM 27421 chromosome 2, whole genome shotgun sequence
        CryFlo/1-91                 -------ATTCGGATGAGACT-CTTTATACATTACA----TATCATCCTTATTCGTACCCC-----TATCGGGACATAATGGCGACT-ACATTCTGCAATACTGAAACC---
        #=GS CryFlo/1-89 DE RRZH01000002.1:783770-783858 Cryptococcus floricola strain DSM 27421 chromosome 2, whole genome shotgun sequence
        CryFlo/1-89                 ------TCTTCGGATGATACA-CTATAAACATTACA----------AACATTTCGTACCCC--TTTCTTCGGGACATCATGGCGACC-ACATTCTGCAATACTGAAACC---
        #=GS CryAmy/1-96 DE MEKH01000001.1:743681-743776 Cryptococcus amylolentus CBS 6273 supercont2.1, whole genome shotgun sequence
        CryAmy/1-96                 GTGACTTCTTCGGATGATACT-CTTTATACATTACA----------AAATTTTCGTACCCC--TTTCTTCGGGACATCATGGCGACC-ACATTCTGCAATACTGAAACCC--
        #=GS CryWin/1-78 DE AWGH01000005.1:c198489-198412 Cryptococcus wingfieldii CBS 7118 supercont1.5, whole genome shotgun sequence
        CryWin/1-78                 ----------------ATACT-CCATATACATTACA----------AAATCCTCGTACCCC--TTTCTTCGGGACATCATGGCGACC-ACATTCTGCAATACTGAAAC----
        #=GS AegTau-SNORD96/1-83 DE http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Aegilops_tauschii300594
        AegTau-SNORD96/1-83         ----TGTCCGGTGATGAAAAAGCTGTTAATCATACC------ATCTTTCGGGACTGAT-----TGGTTGC--------TATGTGT----CATTCTGCAATCCTGAGTACA--
        #=GS SNORD96B/1-79 DE H_sapiens300641 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300641
        SNORD96B/1-79               ---GATCCTGGTGATGACA--------------------GACGACATTGTCAGCCAATCCCC-ATGTGGTA-------GTGAGGAC--ATGTCCTGCAGTTCTGAAGGGATT
        #=GS SNORD96A/1-72 DE H_sapiens300555  5.8S rRNA http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300555
        SNORD96A/1-72               ------CCTGGTGATGACA--------------------GATGGCATTGTCAGCCAATCCCC-AAGTG-GGA------GTGAGGAC--ATGTCCTGCAATTCTGAAGG----
        //




- Image source SnoR29:
  
.. rst-class:: asfootnote

::

        # STOCKHOLM 1.0
        #=GF RW van Nues, July 2023
        #=GF https://coalispr.codeberg.page/paper
        Annot/1-34                       -----------RTGATGA---------------GUUCGAGUUGUC-CTGA---------------------RTGATGA--------------------------------CTGA----------
        #=GS SnoR29/1-86 DE intronic-boxCDsnoRNA-86nt-in-CNB01450 ncrna 2:436830:436916:1 AE017342.1:436831-436916 Cryptococcus neoformans var. neoformans JEC21 chromosome 2 sequence
        SnoR29/1-86                      ------TTCCTATGATGAGCAACTT----TTTTCAAGCTCAACAGTCCTACTAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGATGTTT--
        #=GS SnoR29-b/1-87 DE AE017342.1:c1309857-1309770 Cryptococcus neoformans var. neoformans JEC21 chromosome 2 sequence
        SnoR29-b/1-87                    ----ATGTCCGAATATGAGCAAATC----TTTTCAAGCTCAACAGTCCTACCAT--------------AAGCTGAGGACAATT-A-----------C-TCTTCTATTTCTCTGAGGATTATT--
        #=GS H99/1-82 DE CP003821.1:428606-428687 Cryptococcus neoformans var. grubii H99 chromosome 2, complete sequence
        H99/1-82                         ------TTCCTATGATGAGCAATT-----TTTTCAAGCTCAACAGTCCTACTAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGATT-----
        #=GS R265/1-85 DE CP025762.1:c1334185-1334101 Cryptococcus gattii VGII R265 chromosome 4
        R265/1-85                        ------TTCCTATGATGAGCAACT-----TTTTCAAGCTCAACAGTCCTATTAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGATTTTT--
        #=GS WM276/1-85 DE CP000287.1:c1375357-1375273 Cryptococcus gattii WM276 chromosome B, complete sequence
        WM276/1-85                       ------TTCCTATGATGAGCAACT-----TTTTCAAGCTCAACAGTCCTAATAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGATTTTT--
        #=GS CryWin-1/1-82 DE CP034261.1:470536-470617 Cryptococcus wingfieldii strain CBS7118 chromosome 1, complete sequence
        CryWin-1/1-82                    ------TTCCTATGATGAGCAATC----TTTTACAAGCTCAACAGTCCTACTAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAT------
        #=GS CryWin-2/1-82 DE CP034261.1:470894-470975 Cryptococcus wingfieldii strain CBS7118 chromosome 1, complete sequence
        CryWin-2/1-82                    ------TTCCTATGATGAGCAATTC----TTTACAAGCTCAACAGTCCTACCAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAT------
        #=GS CryAmy/1-82 DE XM_019134412.1:129-210 Cryptococcus amylolentus CBS 6039 hypothetical protein (L202_01103), partial mRNA
        CryAmy/1-82                      ------TTCCTATGATGAGCAATC----TTTTACAAGCTCAACAGTCCTACTAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAT------
        #=GS CryAmy-1/1-82 DE MEKH01000002.1:442845-442926 Cryptococcus amylolentus CBS 6273 supercont2.2, whole genome shotgun sequence
        CryAmy-1/1-82                    ------TTCCTATGATGAGCAATC----TTTTACAAGCTCAACAGTCCTACTAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAT------
        #=GS CryAmy-2/1-82 DE MEKH01000002.1:443234-443315 Cryptococcus amylolentus CBS 6273 supercont2.2, whole genome shotgun sequence
        CryAmy-2/1-82                    ------TTCCTATGATGAGCAATTC----TTTACAAGCTCAACAGTCCTACCTT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAT------
        #=GS CryAmy-3/1-80 DE MEKH01000001.1:521026-521105 Cryptococcus amylolentus CBS 6273 supercont2.1, whole genome shotgun sequence
        CryAmy-3/1-80                    -------TCCTATGATGAGCAATC-----TTTACAAGCTCAACAGTCCTAATAT---------------TACTGAGGATACCCCT-----------TTTCTTCTTTATCTCTGAGGAC------
        #=GS CryWin-3/1-82 DE CP034262.1:c1713976-1713895 Cryptococcus wingfieldii strain CBS7118 chromosome 2, complete sequence
        CryWin-3/1-82                    ------GTCCTATGATGAGCAATC-----TTTACAAGCTCAACAGTCCTAATAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGACT-----
        #=GS CryFlo-1/1-82 DE RRZH01000001.1:c1888851-1888770 Cryptococcus floricola strain DSM 27421 chromosome 1, whole genome shotgun sequence
        CryFlo-1/1-82                    ------TTCCTATGATGAGCAATC----TTTTACAAGCTCAACAGTCCTACTAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAT------
        #=GS CryFlo-2/1-82 DE RRZH01000001.1:c1888463-1888382 Cryptococcus floricola strain DSM 27421 chromosome 1, whole genome shotgun sequence
        CryFlo-2/1-82                    ------TTCCTATGATGAGCAATTC----TTTACAAGCTCAACAGTCCTACCAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAT------
        #=GS CryFlo-3/1-80 DE RRZH01000002.1:559832-559911 Cryptococcus floricola strain DSM 27421 chromosome 2, whole genome shotgun sequence
        CryFlo-3/1-80                    -------TCCTATGATGAGCAATC-----TTTACAAGCTCAACAGTCCTAATAT---------------TACTGAGGATACCCCT-----------CTTCTTCTTTATCTCTGAGGAC------
        #=GS CryGC4/1-86 DE JALPCA010000381.1:2282-2367 Cryptococcus sp. GC_Crypt_4 iso00_46_414, whole genome shotgun sequence
        CryGC4/1-86                      ---GGTTCCCAAAGATGATCAAA------TTTTCAAGCTCAACAGTCCTATGTT---------------TACTGAGGACAAACTT---------TTTTTCTTCT-TTTGACTGAGGGATC----
        #=GS TriCor-1/1-82 DE JXYL01000003.1:c1091174-1091093 Trichosporon coremiiforme strain JCM 2938 scaffold_0003, whole genome shotgun sequence
        TriCor-1/1-82                    -----GATTCGATGATGAGTAAAATCAAATTATCAAGCTCAACAGTCCTAACAT---------------TATTGCGGATACCCTA--------------CTTCTA--TTTCTGAGGCA------
        #=GS TriOvo-1/1-84 DE WEIQ01000026.1:c613946-613863 Trichosporon ovoides strain 2NF903A scaffold26-size649502, whole genome shotgun sequence
        TriOvo-1/1-84                    -------ATCAATGATGAGTACAATCATTTTATCAAGCTCAACAGTCCTAACCAA-------------ATGTTGCGGATACCCCA--------------CTTCTACC-TTCTGAGACAG-----
        #=GS TriOvo-2/1-81 DE WEIQ01000021.1:75646-75726 Trichosporon ovoides strain 2NF903A scaffold21-size709057, whole genome shotgun sequence
        TriOvo-2/1-81                    -----GATTCAATGATGAGTAAAATCAAATTATCAAGCTCAACAGTCCTATACAT---------------ACTGCGGACACCCTA--------------CTTC-AAA--TCTGAGGCA------
        #=GS TriCor-2/1-85 DE JXYL01000014.1:c22119-22035 Trichosporon coremiiforme strain JCM 2938 scaffold_0014, whole genome shotgun sequence
        TriCor-2/1-85                    ----GGAATCAATGATGAGTAAAATCAA-TTATCAAGCTCAACAGTCCTAACAA---------------TCTTGCGGACACCCTA--------------CTTCTA--TTTCTGAGGCATTC---
        #=GS TriAsa/1-82 DE BCLT01000005.1:561033-561114 Trichosporon asahii DNA, scaffold: scaffold_5, strain: JCM 2466, whole genome shotgun sequence
        TriAsa/1-82                      ------ATTCAATGATGAGTAAATCAA-TATATCAAGCTCAACAGTCCTAACA---------------ATTTTGCGGACACCCTA--------------CTTCTA--TTTCTGAGGCAAT----
        #=GS CrySki/1-90 DE BCHT01000011.1:c521819-521730 Cryptococcus skinneri DNA, scaffold: scaffold_10, strain: JCM 9039, whole genome shotgun sequence
        CrySki/1-90                      -----TCCCCGGTGATGAACAAA-----TTTTACAAGCTCAACAGTCTCAATATC--TTCG-----GATATATGTGGATTACACC------------TTCTTCT-TTTTTCTGAGGGGAT----
        #=GS KocImp/1-83 DE NBSH01000002.1:480232-480314 Kockovaella imperatae strain NRRL Y-17943 BD324scaffold_2, whole genome shotgun sequence
        KocImp/1-83                      -----CGCCCTATGATGATCAA-----TTATTTCAAGCTCAACAATCTGAACTC-----------------CTGTTGATTCATAC-------TCTTCTTCT-ATTTCT-TCTGAGGGCA-----
        #=GS KwoMan-1/1-101 DE ASQF01000019.1:1003545-1003645 Kwoniella mangroviensis CBS 8886 cont1.19, whole genome shotgun sequence
        KwoMan-1/1-101                   --TCCTACTCTATGATGAATAAAC---TTTTAACAAGCTCAACAGTCTCACTTTT-ACAGA----AAAGGAATGATGACTTT-AT-------TCTTCTTCTTCTTTATTTCTGAGAAAC-----
        #=GS KwoHev/1-93 DE ASQC01000125.1:c85910-85818 Kwoniella heveanensis CBS 569 cont2.125, whole genome shotgun sequence
        KwoHev/1-93                      ----ATCCCTTATGATGAACAAA-----TTTTACAAGCTCAACAGTCCAACATC---TTCG-----GATGCATGAGGATACTC-T-------TCTTCTTCTTCAACC-CTCTGAGGGGT-----
        #=GS KwoSha-1/1-90 DE NQVO01000042.1:c130149-130060 Kwoniella shandongensis strain CBS 12478 scaffold00042, whole genome shotgun sequence
        KwoSha-1/1-90                    -------TTCTATGATGAACAA-----TTTTTACAAGCTCAACAGTCCAACATC--TTAATT----GATGCATGAGGATACTC----------CTTCTTCTTCAACC-CTCTGACGGAT-----
        #=GS KwoMan-2/1-96 DE ASQF01000041.1:c321435-321340 Kwoniella mangroviensis CBS 8886 cont1.41, whole genome shotgun sequence
        KwoMan-2/1-96                    ---GCACCCCAAGGATGAACAAA-----TTTAACAAGCTCAACAGTCCTATATC---TTCG------GATAATGAGGATACTA-T-------TCTTCTTCTTCAACC-CTCTGAGGGGTCTG--
        #=GS KwoSha-2/1-98 DE NQVO01000005.1:228713-228811 Kwoniella shandongensis strain CBS 12478 scaffold00005, whole genome shotgun sequence
        KwoSha-2/1-98                    ----ATCCCCTACGATGAACAAC-----TTTTACAAGCTCAACAGTCCAATCATTCTACA----AGAATGGATGCGGATACTCC-----------TCTTCTTCAACC-CTCTGAGGGATCATC-
        #=GS CryFla/1-85 DE CAUG01000432.1:59250-59334 Cryptococcus flavescens NRRL Y-50378 WGS project CAUG00000000 data, contig NODE_883_length_201895_cov_45_838108, whole genome shotgun sequence
        CryFla/1-85                      -----GTATTCATGATGAACAAA---TTTTTATCAAGCTCAACAGTCCGAATACAA-------------GACTGTGGACAACC------------TTTTCTTCAACC-CTCTGATCCGA-----
        #=GS TreMes/1-80 DE SDIL01000049.1:c131059-130980 Tremella mesenterica strain ATCC 28783 supercont1.49, whole genome shotgun sequence
        TreMes/1-80                      ----GTGCCCCAAGATGAGACAAAA-----TATCAAGCTCAACAGTCCTACTAT---------------TGCTGCGGATACCC-------------TTTCTTCAACC-CTCTGAGGGC------
        #=GS PapLau/1-86 DE JAAZPX010000029.1:c470304-470219 Papiliotrema laurentii strain IF7SW-F4 scaffold52_cov208, whole genome shotgun sequence
        PapLau/1-86                      ------TTTCTATGATGAATAAAC--TTTTATTCAAGCTCAACAGTCCGAATACA-------------AAACTGTGGACACCC------------TTTTCTTCAACC-CTCTGAGATCAT----
        #=GS PapTer/1-87 DE JAHXHD010000720.1:c42181-42095 Papiliotrema terrestris strain LS28 scaffold-719, whole genome shotgun sequence
        PapTer/1-87                      ----AGTATCTATGATGAGCAAACA--TTTTATCAAGCTCAACAGTCCGAATACA-------------AGACTGTGGACAACC-----------TCTTTCTTCAACC-CTCTGAATCC------
        #=GS TreFuc/1-86 DE BRDD01000112.1:257719-257804 Tremella fuciformis NBRC 9317 DNA, KCNB80TF.112, whole genome shotgun sequence
        TreFuc/1-86                      ------GCCCGAAGATGAGCAAAACC---TTTTCAAGCTCAACAGTCTTACCCTA------------TGGGATGCTGACACCC------------TTTTCTTCAACC-CTCTGAGGGCTT----
        #=GS TreYok/1-87 DE BRDC01000028.1:390580-390666 Tremella yokohamensis NBRC 100148 DNA, KCNB35TY.28, whole genome shotgun sequence
        TreYok/1-87                      -----CGCCCGAAGATGAGCAAAACC---TTTTCAAGCTCAACAGTCTTACCCTA------------TGGGATGCTGACACCC------------TTTTCTTCAACC-CTCTGAGGGCTT----
        #=GS NaeEnc/1-87 DE MCFC01000088.1:c28242-28156 Naematelia encephala strain 68-887.2 BCR39scaffold_88, whole genome shotgun sequence
        NaeEnc/1-87                      ------GTTCAAAGATGAGCAAAAC---TTTATCAAGCTCAACAGTCCGAACACTA----------TGTGACTGTGGACACCC-------------TTTCTTCAACC-CTCTGAGAACAT----
        #=GS NaeAur/1-85 DE JAKFAO010000001.1:1991768-1991852 Naematelia aurantialba strain NX-20 Contig1, whole genome shotgun sequence
        NaeAur/1-85                      -------TTCAAAGATGAGCAAAAC---TTTATCAAGCTCAACAGTCCGAACACTA----------TGTGGCTGTGGACACCC-------------ATTCTTCAACC-CTCTGAGAACA-----
        #=GS SchPom-snR88/1-84 DE Schizosaccharomyces_pombe snR88 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Schizosaccharomyces_pombe300057
        SchPom-snR88/1-84                ------TATCGAGGAGGATAAAAA-TGACATGTCAAGCTCAACAATATGAAAAA------------------TTATGATTT--------TTTTCTATTTCTTCACTT--TCTGAGATGT-----
        #=GS AraTha_SnoR29-1/1-106 DE Arabidopsis_thaliana SnoR29-1 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Arabidopsis_thaliana300058
        AraTha_SnoR29-1/1-106            -------GGCAGTGATGACTCGGAAA----TTTCAAGCTCAACAGACCGGAATTAGGCGTTTCTTCCAATTTATTGGTTGAGTCGTTTCTGTGTCGATAACCCCGCTGATCTGAGCC-------
        #=GS AraTha_SnoR29-2/1-115 DE Arabidopsis_thaliana SnoR29-2 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Arabidopsis_thaliana300057
        AraTha_SnoR29-2/1-115            GAGAAATCGTGGTGATGACTTGGAAA---TATTCAAGCTCAACAGACCGTAATGTAGGATTTTTCCT--AGTGGAAAGT----CTTGCGTGTGTCGATAATCCCGCTGAACTGAGCGATTTCTC
        #=GS AegTau-snoZ107_R87/1-104 DE Aegilops_tauschii snoZ107_R87 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Aegilops_tauschii300644
        AegTau-snoZ107_R87/1-104         ----GATGGCAGTGACGATTTGCAAA---TATTCAAGCTCAACAGACCAAATCACA-GGTTTTCTCTC-AGGAGTTGATTT-------GTATGCCGATTATCCCGCTGAACCGAGCCATC----
        #=GS TriDic-snoZ107_R87/1-104 DE Triticum_dicoccoides snoZ107_R87 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Triticum_dicoccoides300966
        TriDic-snoZ107_R87/1-104         ----GATGGCAGTGACGATTTGCAAA---TATTCAAGCTCAACAGACCAAATCACA-GGTTTTCTCTC-AAGAGTTGATTT-------GTATGCCGATTATCCCGCTGAACTGAGCCATC----
        #=GS TriAes-snoZ107_R87/1-104 DE Triticum_aestivum snoZ107_R87 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Triticum_aestivum301324
        TriAes-snoZ107_R87/1-104         ----GATGGCAGTGACGATTTGCAAA---TATTCAAGCTCAACAGACCAAATCACA-GGTTTTCTCTC-AAGAGTTGATTT-------GTATGCCGATTATCCCGCTGAACTGAGCCATC----
        #=GC SS                          ----((((----------------------------------------------------------------------------------------------------------))))------
        //
