.. role::  raw-html(raw)
   :format: html
   
.. |targetRNA-1|  replace:: 25S rRNA
.. |target-1| replace:: :raw-html:`<span class="mononorm">gag<a href="../18s-tab.html#snord79_25S" title="25S target">A</a>ttcccact</span>`
.. |ortholog-1| replace:: :raw-html:`human <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300200">SNORD79</a>`

.. |targetRNA-2|  replace:: 18S rRNA
.. |target-2| replace:: :raw-html:`<span class="mononorm">gtg<a href="../18s-tab.html#snr40_18S" title="18S target">G</a>tgcatgg</span>`
.. |ortholog-2| replace:: :raw-html:`yeast <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Saccharomyces_cerevisiae300055">snR40</a> (D' guide)`

.. :raw-html:`<a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Saccharomyces_cerevisiae300026>yeast snR55</a>, <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300564">human SNORD33 (U33)</a>`

.. |targetRNA-3|  replace:: 18S rRNA
.. |target-3| replace:: :raw-html:`<span class="mononorm">ca<a href="../18s-tab.html#snr56_18S" title="18S target">G</a>gtctgtga</span>`
.. |ortholog-3| replace:: :raw-html:`yeast <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Saccharomyces_cerevisiae300046">snR56</a> (D' guide), human <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300169">SNORD25</a>`


SNORD79
=======

- SNORD79_intronic-boxCDsnoRNA-83nt
- within 1\ :sup:`st` intron of CNC00470 (CNAG_03038)

  .. :raw-html:`<table><tr><th>&nbsp;<i>C.&nbsp;neoformans</i></th><th>&nbsp;</th><th><i>&nbsp;C. deneoformans</i></th></tr>`

:raw-html:`<table><tr><th>&nbsp;<i>C.&nbsp;neoformans</i></th><th colspan="2">&nbsp;</th>`
:raw-html:`<tr><td>`

.. figure:: /../_static/images/snoRNAs/snord79_h99_igb.png
   :name: snord79-cnag03838
   :align: left
   :width: 1389 px
   :height: 646 px
   :scale: 40%

:raw-html:`</td><td colspan="2">&nbsp;</td></tr></table>`


- Predicted target in |targetRNA-1|\ : |target-1|
- Orthologue of |ortholog-1|

.. figure:: /../_static/images/snoRNAs/snord79-aligned.png
   :name: snord79-align
   :align: left
   :width: 978 px
   :height: 697 px
   :scale: 40%
   :figwidth: 100%


.. rst-class:: mononote

>AE017343.1:c133672-133591 Cryptococcus neoformans var. neoformans JEC21 chromosome 3 sequence :raw-html:`</br>`
TCTAAGATGAGACCTATAACTGCAAGTGGGAATCTCTCCTAAAACAATTGAGGACACAATATTTACTTAG :raw-html:`</br>`
CACCTCTGATCC


snR40_snR56
===========

- snR40_snR56_intronic-boxCDsnoRNA-96nt
- Within 2\ :sup:`nd` intron of CNC00470 (CNAG_03038)
- Predicted target D' guide in |targetRNA-2|\ : |target-2|
- Like |ortholog-2| 
- Predicted target D guide in |targetRNA-3|\ : |target-3|
- Like |ortholog-3| (but guide on different D/D' box)
- In *Tremellomycetes* two separate snoRNAs are present with specificities like yeast snR40, which modifies two sites in 18S rRNA [Yang-2015_]. Possibly the yeast function has been divided over snR40_snR56, to modify h34, and :doc:`snR40-like <snr40like>` to methylate the second site found for yeast snR40.

..  Alternatively, one of the two snoRNAs takes on a putative role of displacing snR4, which in yeast/human could be done by snR55/SNORD33.


.. figure:: /../_static/images/snoRNAs/yeast-snR4-snR40-snR55-overlap.png
   :name: snr40overlap_Sharma2017_again
   :align: left
   :width: 623 px
   :height: 588 px
   :scale: 40%
   :figwidth: 100%

   Overlapping basepair interactions between h34 in 18S rRNA and snR40, snR4 and snR55 in yeast [from Sharma-2017_]


.. figure:: /../_static/images/snoRNAs/snR40_snR56-aligned.png
   :name: snr40_snr56-align
   :align: left
   :width: 3351 px
   :height: 469 px
   :scale: 30%
   :figwidth: 100%

.. rst-class:: mononote

>AE017343.1:c133288-133194 Cryptococcus neoformans var. neoformans JEC21 chromosome 3 sequence :raw-html:`</br>`
ACCCCAATGATATAAACAATCATGCACCACGCTTAGCCAGCCATACGGCGCGGCCATGCGGAAAAAACTG :raw-html:`</br>`
ATTCACAGACCTGATATGAGGGGTC

|
|
|
|
|
|

=======

- Image source SNORD79:
  
.. rst-class:: asfootnote

::

        # STOCKHOLM 1.0
        #=GF RW van Nues, June 2023
        #=GF https://coalispr.codeberg.page/paper
        SNORD79/1-86                ---TCTCTAAGATGAGACCTATAAC---TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACAA--TATTTACTTAGCACCTCTGATCCTT-
        #=GS H99/1-83 DE CP003822.1:c142621-142539 Cryptococcus neoformans var. grubii H99 chromosome 3, complete sequence
        H99/1-83                    -----TCTAAGATGAGACCTATAAA---TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACAA--TATTTGCTTAGCACCTCTGACCCT--
        #=GS WM276/1-85 DE CP000288.1:1836161-1836245 Cryptococcus gattii WM276 chromosome C, complete sequence
        WM276/1-85                  ----TTCTAAGATGAGACCTATAAA---TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACAA--TATTTACTTAGCACCTCTGATCCTT-
        #=GS EN28/1-81 DE CP025719.1:c142688-142608 Cryptococcus neoformans strain EN28 chromosome 3, complete sequence
        EN28/1-81                   -------TAAGATGAGACCTATAAA---TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACAA--TATTTGCTTAGCACCTCTGACCTT--
        #=GS R265/1-84 DE CP025759.1:2078805-2078888 Cryptococcus gattii VGII R265 chromosome 1, complete sequence
        R265/1-84                   -----TTCAAGATGAGATCTATAAA---TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACAA--TATTTACTTAGCACCTCTGATCCTT-
        #=GS PasPL2/1-84 DE JAMFRE010000023.1:c187681-187598 Pascua sp. PL2904B ctg_23, whole genome shotgun sequence
        PasPL2/1-84                 ----TTTCAAGATGAGACCATCTAT---TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACCACAA--TTACTTAGCACCTCTGATTCC--
        #=GS TriGue/1-84 DE BCJX01000004.1:817277-817360 Trichosporon guehoae DNA, scaffold: scaffold_3, strain: JCM 10690, whole genome shotgun sequence
        TriGue/1-84                 ----TTTCAAGATGAGACCATCTAT---TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACCACAA--TTACTTAGCACCTCTGATTCC--
        #=GS TriGam/1-83 DE BCJN01000004.1:c1372052-1371970 Trichosporon gamsii DNA, scaffold: scaffold_3, strain: JCM 9941, whole genome shotgun sequence
        TriGam/1-83                 ----TTTCAAGATGAGACTCAA------TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACCCAAC-TATAC-TAGCATCTCTGAACCATC
        #=GS VanPse/1-82 DE CP086720.1:958324-958405 Vanrija pseudolonga isolate DUCC4014 chromosome 7
        VanPse/1-82                 ----TTTCAAGATGAGATTAAT------TGCAAGTGGGAATCTCTCCTAA-TACAC--TTGAGGACACCC--TTTTTACTTTGCGCTTCTGATACTT-
        #=GS VanHum/1-81 DE BFAH01000024.1:338700-338780 Vanrija humicola UJ1 DNA, scaffold25, whole genome shotgun sequence
        VanHum/1-81                 -----TTCAAGATGAGATAAAT------TGCAAGTGGGAATCTCTCCTAA-TACAC--TTGAGGACACCC--TTTTTACTTTGCGCTTCTGATCCTT-
        #=GS KwoHev/1-86 DE ASQC01000046.1:c85899-85814 Kwoniella heveanensis CBS 569 cont2.46, whole genome shotgun sequence
        KwoHev/1-86                 -----TCTAAGATGAGAAACTATAAT--TGCAAGTGGGAATCTCTCCTAAA-TCAC--TTGAGGACATAAAA-CAATACTTAGCACCTCTGATCATT-
        #=GS KwoSha/1-85 DE NQVO01000028.1:c189078-188994 Kwoniella shandongensis strain CBS 12478 scaffold00028, whole genome shotgun sequence
        KwoSha/1-85                 -----TTGAAGATGAGACTTTACAAT--TGCAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGATATA--TTATATACTTAGCACCTCTGAACCTC-
        #=GS CryDep/1-82 DE AWGL01000002.1:c1393767-1393686 Cryptococcus depauperatus CBS 7855 supercont2.2, whole genome shotgun sequence
        CryDep/1-82                 ----TATTAAGATGAGATATTTCAAT--TGCAAGTGGGAATCTCTCCTAAT-TCAA--TTGAGGAAACC----TTTTGCTTTGCACCTCTGAACC---
        #=GS KwoDej/1-85 DE ASCJ01000023.1:c1158231-1158147 Kwoniella dejecticola CBS 10117 cont1.23, whole genome shotgun sequence
        KwoDej/1-85                 -----TCTATGATGAGACCAAATATAAATGCAAGTGGGAATCTCTCCTAAA-CCAA--TTGAGGAAACA--TAAAATACTTAGCACCTCTGATCC---
        #=GS KwoPin/1-86 DE ASCL01000037.1:35372-35457 Kwoniella pini CBS 10737 cont1.37, whole genome shotgun sequence
        KwoPin/1-86                 -----TTTATGATGAGACTAAATATAA-TGCAAGTGGGAATCTCTCCTAAAA-TAA--TTGAGGAAA--TATAAAATACTTAGCGACTCTGACTCGT-
        #=GS TriVee/1-82 DE BCKJ01000002.1:c3164935-3164854 Trichosporon veenhuisii DNA, scaffold: scaffold_1, strain: JCM 10691, whole genome shotgun sequence
        TriVee/1-82                 -----TTCAGGATGAGATCAAT------TGCAAGTGGGAATCTCTCCTAA-TACAC--TTGAGGACACCC-TACTATACTTAGCATCTCTGATCCTC-
        #=GS KocImp/1-86 DE NBSH01000011.1:c578577-578492 Kockovaella imperatae strain NRRL Y-17943 BD324scaffold_11, whole genome shotgun sequence
        KocImp/1-86                 -----TTCCGGATGAGACTATCATTT--TGCAAGTGGGAATCTCTCCTAATATCAC--TTGAGGATCACA--TTTATACTTAGCACCTCTGATCATC-
        #=GS PapTer/1-80 DE JAHXHD010000182.1:c3579-3500 Papiliotrema terrestris strain LS28 scaffold-181, whole genome shotgun sequence
        PapTer/1-80                 ------TCCGGATGAGACTATAT-----TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACAACCA--TAAATACTAGCACCTCTGATCAT--
        #=GS PapTre/1-81 DE JDSR01000634.1:c9628-9548 Papiliotrema laurentii RY1 contig_655, whole genome shotgun sequence
        PapTre/1-81                 -----TTCCGGATGAGACATCTTT----TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACAACCAC--TATACTTAGCACCTCTGACCC---
        #=GS BulAlb/1-85 DE CAMYTR010000136.1:317050-317134 Bullera alba genome assembly, contig: jcf7180000012237, whole genome shotgun sequence
        BulAlb/1-85                 ----TTTCCGGATGAAACTCTATT----TGCAAGTGGGAATCTCTCCTAAA-TCAT--TTGAGGATACAAAAC-TATACTTAGCACCTCTGAACATC-
        #=GS CryFla/1-80 DE CAUG01000390.1:24627-24706 Cryptococcus flavescens NRRL Y-50378 WGS project CAUG00000000 data, contig NODE_746_length_79055_cov_47_112000, whole genome shotgun sequence
        CryFla/1-80                 ------TCCGGATGAGACTATAT-----TGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACAATTATAAA-TAC-TAGCAACTCTGATCAT--
        #=GS CryGC_1/1-82 DE JALPCD010000078.1:c15459-15378 Cryptococcus sp. GC_Crypt_1 78, whole genome shotgun sequence
        CryGC_1/1-82                -----TTCCGGATGAGACATACT-----TGCAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGACAACCAAC-TATAC-TAGCACCTCTGATCTCT-
        #=GS TakKor/1-84 DE BCKT01000006.1:118638-118721 Takashimella koratensis DNA, scaffold: scaffold_5, strain: JCM 12878, whole genome shotgun sequence
        TakKor/1-84                 -----TTCCGGATGAGACATCTTTT---TGCAAGTGGGAATCTCTCCTAAA-TACA--CTGAGGACAACC-TCTTATACTTAGCACCTCTGAACCT--
        #=GS TriFae/1-81 DE JXYK01000006.1:c872741-872661 Trichosporon faecale strain JCM 2941 scaffold_0006, whole genome shotgun sequence
        TriFae/1-81                 ----TTCTCGGATGAGACACAAAC----TGCAAGTGGGAATCTCTCCTAAA-TCAT--TTGAGGACACCC--TTAATAT-TTGCACCTCTGAACA---
        #=GS TriCor/1-80 DE JXYL01000002.1:1636090-1636169 Trichosporon coremiiforme strain JCM 2938 scaffold_0002, whole genome shotgun sequence
        TriCor/1-80                 -----TCCTGGATGAGACACAATC----TGCAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGACACCC--TTTATAT-TTGCACCTCTGATAT---
        #=GS SaiJCM/1-78 DE BCLC01000002.1:c945392-945315 Saitozyma sp. JCM 24511 DNA, scaffold_1, whole genome shotgun sequence
        SaiJCM/1-78                 -----TTTCGGATGAGACAATT------TGCGAGTGGGAATCTCTCCTAAA-TCAC--TTGAGGACAACC---TTTTACTTTGCACCTCTGATCC---
        #=GS SaiPod/1-80 DE CABVUB010000001.1:104143-104222 Saitozyma podzolica genome assembly, contig: NODE_1_length_1044407_cov_28.3483, whole genome shotgun sequence
        SaiPod/1-80                 ------TTCGGATGAGACAATC------TGCGAGTGGGAATCTCTCCTAAA-TCAC--TTGAGGACAACCTTCTTTTACTTTGCACCTCTGATCC---
        #=GS CryGC_2/1-80 DE JALPCC010000014.1:c7039-6960 Cryptococcus sp. GC_Crypt_2 iso00_70_14, whole genome shotgun sequence
        CryGC_2/1-80                -----TTCCGGATGAGTTTTAAAT----AGCAAGTGGGAATCTCTCCTAAA-TCAA--TTGAGGACACCATAA--TTACT-AGCACCTCTGAATT---
        #=GS TriGra/1-84 DE BCJO01000004.1:1024371-1024454 Trichosporon gracile DNA, scaffold: scaffold_3, strain: JCM 10018, whole genome shotgun sequence
        TriGra/1-84                 ----TTCAAGGATGATACCTAAAT----AGCAAGTGGGAATCTCTCCTAAA-TCAA--TTGAGGACACCCAAA--TTACTTAGCAGCTCTGATCTAC-
        #=GS ApiAki/1-81 DE PQXP01000086.1:c40341-40261 Apiotrichum akiyoshidainum strain HP2023 Contig1069, whole genome shotgun sequence
        ApiAki/1-81                 ----TTCAAGGATGATATCTAAAT----AGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACATAAA--TTACT-CGCATCTCTGATCC---
        #=GS CutCya/1-83 DE BEDZ01000004.1:c861795-861713 Cutaneotrichosporon cyanovorans DNA, scaffold: scaffold_4, strain: JCM_31833, whole genome shotgun sequence
        CutCya/1-83                 -----TCTCGGATGATACTCTACA----AGCAAGTGGGAATCTCTCCTAAA-TCAT--TTGAGGACAACC--TATATACT-CGCACCTCTGATCCCAT
        #=GS TriLai/1-81 DE BCKV01000013.1:119279-119359 Trichosporon laibachii DNA, scaffold: scaffold_12, strain: JCM 2947, whole genome shotgun sequence
        TriLai/1-81                 ----TTTAAGGATGATATTTAAAT----AGCAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGACACCTAAA--TTACT-AGCATCTCTGATCT---
        #=GS TriMon/1-82 DE BCFV01000002.1:435168-435249 Trichosporon montevideense DNA, scaffold: scaffold_1, strain: JCM 9937, whole genome shotgun sequence
        TriMon/1-82                 -----TTCAGGATGAGATTTATAA----AGCAAGTGGGAATCTCTCCTAA-TACTT--TTGAGGACACCCGA--TTTACTTAGCATCTCTGACTCT--
        #=GS ApiDom/1-82 DE BCFW01000002.1:c888523-888442 Apiotrichum domesticum DNA, scaffold: scaffold_1, strain: JCM 9580, whole genome shotgun sequence
        ApiDom/1-82                 -----TTCAGGATGAGATTTATAA----AGCAAGTGGGAATCTCTCCTAA-TATCT--TTGAGGACACCCAA--TTTACTTAGCATCTCTGACTCT--
        #=GS ApiMyc/1-79 DE CP049823.1:2525998-2526083 Apiotrichum mycotoxinovorans strain GMU1709 chromosome III
        ApiMyc/1-79                 -----TTAAGGATGAGATCAAT------CGCAAGTGGGAATCTCTCCGAA-CACAC--TTGAGGACACCCAA--TTTACTTAGCATCTCTGATCC---
        #=GS CutCut/1-79 DE LTAL01000631.1:25954-26032 Cutaneotrichosporon cutaneum strain ACCC 20271 contig631, whole genome shotgun sequence
        CutCut/1-79                 -----TTAAGGATGAGATCAAT------CGCAAGTGGGAATCTCTCCGAA-CACAC--TTGAGGACACCCAA--TTTACTTAGCATCTCTGATCC---
        #=GS NaeEnc/1-78 DE MCFC01000074.1:c79798-79721 Naematelia encephala strain 68-887.2 BCR39scaffold_74, whole genome shotgun sequence
        NaeEnc/1-78                 -----TTTCGGATGAGACCAAT------CGCAAGTGGGAATCTCTCCTAAAA-CCA--TTGAGGACACCACA---TTACTTAGCGTTTCTGAATT---
        #=GS TriPor/1-83 DE BCJG01000001.1:c3687752-3687670 Trichosporon porosum DNA, scaffold: scaffold_0, strain: JCM 1458, whole genome shotgun sequence
        TriPor/1-83                 -----TTCAAGATGATACACAAAA----CGCAAGTGGGAATCTCTCCTAAAA-TAA--TTGAGGACAACCTAC-TATACTTAGCACCTCTGAACTA--
        #=GS KwoBes/1-87 DE ASCK01000005.1:c581033-580947 Kwoniella bestiolae CBS 10118 cont1.5, whole genome shotgun sequence
        KwoBes/1-87                 -----TCCCTGATGAGACTAAATATAATGCAAAGTGGGAATCTCTCCTAAAA-CAA--TTGAGGATATATAAAA--TACTTAGCACCTCTGATCTAT-
        #=GS XanDen/1-85 DE LN483332.1:152375-152460 Xanthophyllomyces dendrorhous genome assembly Xden1, scaffold Scaffold_249
        XanDen/1-85                 ---CTTGAATGATGATACTTTAT----TGCAAAGTGGGAATCTCTCCTAAA-TCAA--TTGAGGACAACC-TTTTTTACTTTTGCTCTCTGACCTC--
        #=GS KwoMan/1-84 DE ASQE01000056.1:52877-52960 Kwoniella mangroviensis CBS 8507 cont2.55, whole genome shotgun sequence
        KwoMan/1-84                 -----TCTCTGATGAGACTAAATATAATGCAAAGTGGGAATCTCTCCTAAA-TCAA--TTGAGGAAATATAAAA--TACTTAGCACCTCTGATC----
        #=GS CryGC_5/1-85 DE JALPBZ010000094.1:29765-29849 Cryptococcus sp. GC_Crypt_5 iso00_58_94, whole genome shotgun sequence
        CryGC_5/1-85                -------TAAGATGAGTCACTTGTAATTGCAAAGTGGGAATCTCTCCTAAA-TCAT--TTGAGGATACATAAGA--TACTTAGCACCTCTGATCTTT-
        #=GS CryGC_3/1-85 DE JALPCB010000026.1:87930-88014 Cryptococcus sp. GC_Crypt_3 iso00_45_26, whole genome shotgun sequence
        CryGC_3/1-85                ------TTAAGATGAGTCACTTGTAATTGCAAAGTGGGAATCTCTCCTAAA-TCAT--TTGAGGATACATAAGA--TACTTAGCACCTCTGATCTT--
        #=GS CryFlo/1-87 DE NIDF01000082.1:67961-68047 Cryptococcus floricola strain DSM 27421 scaffold6.82, whole genome shotgun sequence
        CryFlo/1-87                 -----TCAAAGATGAGACTTTATCAAACGCAAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGATACTTTATA--TACTTAGCACCTCTGAACCTT-
        #=GS CryWin/1-87 DE AWGH01000002.1:c1136453-1136367 Cryptococcus wingfieldii CBS 7118 supercont1.2, whole genome shotgun sequence
        CryWin/1-87                 -----TCAAAGATGAGACTCTATCAAACGCAAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGAAACTTTATA--TACTTAGCACCTCTGAACCTT-
        #=GS CryAmy/1-87 DE MEKH01000001.1:c2109042-2108956 Cryptococcus amylolentus CBS 6273 supercont2.1, whole genome shotgun sequence
        CryAmy/1-87                 -----TCAAAGATGAGACTTTATTAAATGCAAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGATACTTTATA--TACTTAGCACCTCTGAACCTT-
        #=GS CryGC_6/1-84 DE JALPBY010000032.1:112830-112913 Cryptococcus sp. GC_Crypt_6 iso00_61_32, whole genome shotgun sequence
        CryGC_6/1-84                -----TCTACGATGAGACTCTTTTAATTGCAAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGATACATAAGA--TACTTAGCACCTCTGATC----
        #=GS CryGC_7/1-86 DE JALPBX010000030.1:112831-112916 Cryptococcus sp. GC_Crypt_7 iso00_79_30, whole genome shotgun sequence
        CryGC_7/1-86                -----TCTACGATGAGACTCTTTTAATTGCAAAGTGGGAATCTCTCCTAAA-CCAT--TTGAGGATACATAAGA--TACTTAGCACCTCTGATCTT--
        Annot/1-34                  --------RTGATGA----------------tcacccttagag-CTGA---------RTGATGA-----------------------CTGA------
        RatRat-SNORD79/1-75         -----TTAGTGATGATCAATTAAGTTAAAACAGATGGGAATCTCTCTGAACAACAT--TGGAGATTGA------------TTGTTAAGCTGAAA----
        #=GS HomSap-SNORD79/1-85 DE Homo_sapiens SNORD79
        HomSap-SNORD79/1-85         TACTGTTAGTGATGATTTTAAAA-TTAAAGCAGATGGGAATCTCTCTGAGAAAGAAAATGGAGATTAATC-------------TTAAACTGAAACAGTA
        //

- Image source snR40_snR56:
  
.. rst-class:: asfootnote

::

        # STOCKHOLM 1.0
        #=GF RW van Nues, June 2023
        #=GF https://coalispr.codeberg.page/paper
        Annot/1-52                        ---------------------------------------------------------------RTGA--TGA----------gGUACGUGGUG-CTGA---------------------------RTGATGA--------------aGUGUCUGGACa-CTGA------------------------------------------------------------------------------------CTGA---------------------------------YAG----------------------------------------------------------------------
        #=GS snR40_snR56/1-96 DE intronic-boxCDsnoRNA-96nt-in-CNC00470 ncrna 3:133192:133288:-1 
        snR40_snR56/1-96                  ---------------------------------------------------------ACCCCAATGATATAAA------CAATCATGCACCACGCTTAGCCAGCC--ATAC--GGCGCGGCC---ATGCGGAAA-AAACTGAT---TCACAGACCTGATATGAGGGGTCC-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS intron-in-CNC00470/49-250 DE intron-with-boxCDsnoRNA-145nt-in-CNC00470 ncrna 3:133143-133288:-1
        intron-in-CNC00470/49-250         TGATCCGGAGGTGAGCCGCATTTCTTACCTCATTTTTCTTCATTTTCGTTTCATGGGACCCCAATGATATAAA------CAATCATGCACCACGCTTAGCCAGCC--ATAC--GGCGCGGCC---ATGCGGAAA-AAACTGAT---TCACAGACCTGATATGAGGGGTCCCTTACTTTTTCATCATTTTATATCTCT-----------------------------------GACGATGATCAT-CGCTGACTTA------------------------------------------------------------------------------------------------------
        #=GS H99/1-149 DE CP003822.1:c142238-142090 Cryptococcus neoformans var. grubii H99 chromosome 3, complete sequence
        H99/1-149                         ---------------------------------------------------------ACCCCAATGATATAAA------CAATCATGCACCACGCTTAGCCAGCC--ATAC--GGCGCGGCC---ATGCGGAAA-AAACTGAT---TCACAGACCTGATATGAGGGGTCCCTTTTTTTTCATCATTATTTTATCATCTCC--------------------------------GACGATGATCATCCGCTGACTTG------------------------------------------------------------------------------------------------------
        #=GS CryWin/1-159 DE CP034262.1:111800-111958 Cryptococcus wingfieldii strain CBS7118 chromosome 2, complete sequence
        CryWin/1-159                      ---------------------------------------------------------ATCCCAATGATTCAAC------AAATCATGCACCACGCTTAGCCAGGC--AATT--GTCGCGGCC---ATGCTGAAACAA-CCGAT---TCACAGACCTGATATGAGGGATCCCTTTTTTTCATTTATTTTATTTGTCTGATTGT-----------------------------GACTAGTGAGCTCTTGCTGACTCGTATAATC-----------------------------------------------------------------------------------------------
        #=GS R265/1-148 DE CP025759.1:2079187-2079334 Cryptococcus gattii VGII R265 chromosome 1, complete sequence
        R265/1-148                        ---------------------------------------------------------ACCCCAATGATATAAA------CAATCATGCACCACGCTTAGCCAGCC--ATAC--GGCGCGGCC---ATGCGGAAA-AAACTGAT---TCACAGACCTGATATGAGGGGTCCCTTTTATTTATTACTTTTGTAATATCT-----------------------------------GATGAAGATCGCCCGCTGACTTAAT----------------------------------------------------------------------------------------------------
        #=GS WM276/1-148 DE CP000288.1:1836547-1836694 Cryptococcus gattii WM276 chromosome C, complete sequence
        WM276/1-148                       ---------------------------------------------------------ACCCCAATGATATAAA------CAATCATGCACCACGCTTAGCCAGCC--ATAC--GGCGCGGCC---ATGCGGAAA-AAACTGAT---TCACAGACCTGATATGAGGGGTCCCTTTTTATTTTTTACTTTTATAATCTCC----------------------------------GATGATGATCATCCGCTGACTTGA-----------------------------------------------------------------------------------------------------
        #=GS PapLau/2-147 DE JDSR01000634.1:c9270-9124 Papiliotrema laurentii RY1 contig_655, whole genome shotgun sequence
        PapLau/2-147                      ---------------------------------------------------------GCCCCAAGGATATAAA------ACATCATGCACCACGCTTAGCCAGCC--ATAC--GGCGCGGCC---ATGCGGAAA-AACCTGAT---TCACAGACCTGATATGAGGGGCCCTCTTCTCTTGACGAGATTTTGTATAT------------------------------------------GGACATTTGCTGACGCAAAGATCC-----------------------------------------------------------------------------------------------
        #=GS KwoSha/1-169 DE NQVO01000028.1:c188668-188500 Kwoniella shandongensis strain CBS 12478 scaffold00028, whole genome shotgun sequence
        KwoSha/1-169                      ---------------------------------------------------------ACCCCAAAGAT-TAAA------CAATCATGCACCACGCTTAGCCAGCC--TTAC--GGCGTGGCC---ATGCGGAAACAACCTGAT---TCACAGACCTGATATGAGGGGCCCTCCATATTCCATCGTTTTCTCATTCCTTCAACCATTCT-------------GCAGCACTCCATTGAGAAATATCATACTGACACAC-----------------------------------------------------------------------------------------------------
        #=GS KwoHev/1-225 DE ASQC01000046.1:c85393-85169 Kwoniella heveanensis CBS 569 cont2.46, whole genome shotgun sequence
        KwoHev/1-225                      ---------------------------------------------------------ACCCCAATGATATGAA------ACATCATGCACCACGCTTAGCCAGCCT-TAGC-GGGCGCGGCC---ATGCGGAAACAA-CTGAT---TCACAGACCTGATATGAGGGGCCACCATATACCACAATTTTCCCCAGAGTCTATCTGAAATCCTCTTTTTGGAGTGTATTGCCGAAGCGAAGAGCTGTGTGCTGACGATGCCGTGTCACGCCCTCTCTTG--------TAGATCCTCGACACTAATGCG----------------------------------------------------
        #=GS KwoMan/1-169 DE ASQF01000020.1:240129-240297 Kwoniella mangroviensis CBS 8886 cont1.20, whole genome shotgun sequence
        KwoMan/1-169                      ---------------------------------------------------------ACCCCAAGGATTTAAA------CCATCATGCACCACGCTTAGCCAGCTC-ACA--GAGCGCGGCC---ATGCGGAAGCAA-CTGATAC-TCACAGACCTGATATGAGGGGCATTCGTGTATTCATATTTTTTGTTTGCATCT---------------AGTCAGACATCGTAATATATACGAGATGAATCACTGACAAC------------------------------------------------------------------------------------------------------
        #=GS TreYok/2-216 DE BRDC01000026.1:1115831-1116046 Tremella yokohamensis NBRC 100148 DNA, KCNB35TY.26, whole genome shotgun sequence
        TreYok/2-216                      ---------------------------------------------------------TCCCCAAAGAT-TCAA------CATTCATGCACCACGCTTAGCCAGCC--TTAC--GGCGCGGCC---ATGCGGAAACAA-ATGAACA--CACAGACCTGTTATGAGGGGACCCTATCGAAACTTTTCTCTCACT-------------------------------GCTCCGAATATTGGCTCGTCATAGACGATAGCTTATCGT----------------------CAGATCCTCGACAACAACCCACCTCTCCTCTTCCACCTTCACCTTCTCCGACTGATCG---------------
        #=GS PapTer/2-195 DE JAHXHD010000182.1:c3229-3035 Papiliotrema terrestris strain LS28 scaffold-181, whole genome shotgun sequence
        PapTer/2-195                      ---------------------------------------------------------TCCCCGAGGATTTTAA------ACATCATGCACCACGCTTAGCCAGCT---TC---GGCGCGGCC---ATGCGGAAATA-CCTGATAA--CACAGACCTGATATGAGGGGTCGCGCACACTGCAACGTTTCCTTT-------------------------------------------------GTCAGGCTGAGCGCTGACATT----------------------CAGATCCTTGACACGAACCCGCCGCTTCTGTTCCACCTGCACCTACTGCGCCTGGT-----------------
        #=GS CryFag/2-192 DE BCHU01000014.1:814669-814860 Cryptococcus fagi DNA, scaffold: scaffold_13, strain: JCM 13614, whole genome shotgun sequence
        CryFag/2-192                      ---------------------------------------------------------TCCC-AATGAT-TCAAC-----ACATCATGCACCACGCTTAGCCAGCT---TC---GGCGTGGCC---ATGCGGAAACAA-CCGATTT-TCACAGACCTGATATGAGGGACCATCTTGCGGCTATCTGTTTT------------------------------GAGATTGAATAGTTATTTGAGCCTTGGACTGATCCATTCAACTT---------------------TAGATCCTTGACACGAATCCCCCATTACTTTTT----------------------------------------
        #=GS BulALb/2-170 DE CAMYTR010000136.1:317430-317599 Bullera alba genome assembly, contig: jcf7180000012237, whole genome shotgun sequence
        BulALb/2-170                      ---------------------------------------------------------TCCCCAAGGATATGAA------CCATCATGCACCACGCTTAGCCAGC---TTAAT--GCTTGGCC---ATGCTGAAG-AAAATGATC--TCACAGACCTGATATGAGGGGTATACAATCCTCCTCTTTCTCTC------------------------------ACGTGGAAGGCTAGGAGAAGTATCAAGCTGATCTCGTGCTCA----------------------TAGATTCTCGA--------------------------------------------------------------
        #=GS KwoPin/1-284 DE ASCL01000037.1:35847-36130 Kwoniella pini CBS 10737 cont1.37, whole genome shotgun sequence
        KwoPin/1-284                      ---------------------------------------------------------ACCCCAAGGATTTAAC------AAATCATGCACCACGCTTAGCCAGCTC-AAA--GAGCGCGGCC---ATGCTGAAACA--ACGATC--TCACAGACCTGATATGAGGGGCATCCATCTATCTTATTTCATTCTTTTTATCATTTGGAAATACATCGTGGTTGATTGAAAATATTGAGAAGTATAAAAAGCTAATCTGCTATTTATATTTACTTTTGGAAATAATTATAGATACTAGATACCAATCCACCATTATTATTTCATCTTCACTTATTAAGACTTATTGAATTAATTAGATCAG
        #=GS NaeAur/1-171 DE JAKFAO010000003.1:c144643-144473 Naematelia aurantialba strain NX-20 Contig3, whole genome shotgun sequence
        NaeAur/1-171                      ---------------------------------------------------------TCCCCGATGAAAAGA-------CAATCATGCACCACGCTTAGCCCGCT---TC---GGCGTGGCC---ATGCGGAAACAC-CTGATT--TTACAGACCTGATATGAGGGGACTCAACCC-AACGCTAGATTTCTCTT-----------------GCCACTGCATACTTGTCCTGTCCTGGATGCAAAAAGCTGATACCGGC--------------------------TAGATTC------------------------------------------------------------------
        #=GS SaiPod/6-207 DE RSCD01000010.1:130393-130599 Saitozyma podzolica strain DSM 27192 scaffold_10, whole genome shotgun sequence
        SaiPod/6-207                      ---------------------------------------------------------ACCCCG-AGATTAGATC-----GTATCATGCACCACGCTTAGCCGGCTC-TTAC-GAGCAAGGCC---ATGCTGAAATACCACGAC---TCACAGACCTGATATGAGGGGTCCCTACCTTTCTGCCGATTGCTGCTC------------------------------GGCGATACGACGAG-CGGCTCCGCTGACGCAGAGTA------------------------CAGATCCTCGACACGAACCCACCCCTGCTTTTCCATCTCCACCT-----------------------------
        #=GS TreMes/2-203 DE AFVY01000063.1:c129062-128860 Tremella mesenterica DSM 1558 strain Fries TREMEscaffold_1_Cont63, whole genome shotgun sequence
        TreMes/2-203                      ---------------------------------------------------------TCCCCAAAGATTTAAC------AAA-CATGCACCACGCTTAGCCGGCT---TC---GGCAAGGCC---ATGCTGAAATAC-CTGTTA---CACAGACCTGATATGAGGGGTCATCTACAATCTATCCTTTCCTTGTCTTCTGTCTC----------------------------------ACGGACAATGCTGACATGA----------------------------GAGATATTGGACAACAACCCTCCCCTTCTTTTCCACCTTCACCTACTCCGTCTCATC----------------
        #=GS VanFra/2-212 DE BEDY01000006.1:520349-520560 Vanrija fragicola DNA, scaffold: scaffold_6, strain: JCM 1530, whole genome shotgun sequence
        VanFra/2-212                      ---------------------------------------------------------GCCCCAAGGATATGAA------ACATCATGCACCACGCTTAGCCGCCC---TC---GGGAAGGCC---ATGCTGAAACAC-CTGAT---TCACAGACCTGATATGAGGGGCCCTTCTATCTTCATCCTTTATTGTT--------------------------------------------AGAATACTGGCTGACAGAAAA--------------------------CAGATTCTTGATACCAAGACGGATATCCTCTTCCATCTTTTCCTCCTGCGGCTCATCGAGCTCATTCGCGAGG
        #=GS VanHum/1-202 DE BCJF01000007.1:946262-946463 Vanrija humicola DNA, scaffold: scaffold_6, strain: JCM 1457, whole genome shotgun sequence
        VanHum/1-202                      ---------------------------------------------------------GCCCCAATGATATGAA------CCATCATGCACCACTCTCAGCCGGCT---TC---GGCAAGGCC---ATGCGGAAATAC-CTGATT--TCACAGACCTGATATGAGGGGCCATTATATTTCTCTGCTTTCAGCGATTCGTTT-----------------------------------------CAGGCGCTAACAATGG---------------------------CAGATACTCGACACCAACCCTCCGCTCCTCTTCCACCTGTTCCTATTGCGATTGATCGAGC------------
        #=GS ApiMyc/6-173 DE CP053622.1:c2380376-2380204 Apiotrichum mycotoxinovorans strain CICC 1454 chromosome 3
        ApiMyc/6-173                      ---------------------------------------------------------GCCCCAAGGATATGAA------CCATCATGCACCACTCTCAGCCGGC---TTCGT--GCAAGGCC---ATGCGGAAACAC-CTGATTTATCACAGACCTGATATGAGGGGCCCAACCAAGTCTTTTTTTTTTGTTTCT-------------------------------------------------CAACTGACACAT----------------------------CAGATCCTCGATACCAACCCTACGCTTTTGTTC----------------------------------------
        #=GS VanPse/1-202 DE CP086720.1:958693-958894 Vanrija pseudolonga isolate DUCC4014 chromosome 7
        VanPse/1-202                      ---------------------------------------------------------GCCCCAATGATATGAA------CCATCATGCACCACTCTCAGCCGGC---TTCG---GCAAGGCC---ATGCGGAAATA-CCTGATT--TCACAGACCTGATATGAGGGGCCATCATCTTTCACTGCTTTTAGTGTTTGCTCC----------------------------------------AGAGAAGCTAACGAGAG---------------------------CAGATTCTGGACACCGACTCTACGCTACTCTTCCACCTGTTTCTCCTGCGATTGATCGAG-------------
        SacCer-snR56/1-86                 --------------------------------------------------------------------------------------------------------------------------AACATGATGAAAAAA--TATATTAACACAGACCTGTACTGAACTTTTCGAAGTTTTGCAGATAACAATATTGCTTTTTTTCTCTGACT---------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS HomSap-SNORD25/1-67 DE Homo Sapiens U25                   
        HomSap-SNORD25/1-67               ------------------------------------------------------------------------------------------------------------------------TTCCTATGATGAGGACC------TTTTCACAGACCTGTACTGAGCTC--------CGTGAGGATAAATAACT------------CTGAGGAGA------------------------------------------------------------------------------------------------------------------------------------------------
        Annot-snR40/12-61                 ---------------------------------------------------------------RTGA--TGA---------CGGUACGUGGU--CTGA----------------GUGGGU-----RTGATGA---------------------------CTGA--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        SacCer-snR40/1-95                 ------------------------------------------------------------TAAATGACGAGAAAA----AAGCTGTGCACCAGTCTGAACATGGATGCCACAAGTACTCAGGTGTCCTATGAAGCATT-----AAGTATACCCAAATTTCTGAT-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        SchPom-snR40/1-81                 ------------------------------------------------------------TTAATGA--TGATACACTGTCTTCATGCACCAGTCTGA-------GACA----TTTATT-TGTCAGTGAAGAGG---------AACAGACCCTTTATTTCTGAA-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Annot-snR55-snR56/7-63            ----RTGATGA-------------------------------CTGA-----------------RTGA--TGA-----------GUACGUGGUGGUGCTGA-------------------------RTGATGA---------------------------CTGA-------------RTGATGA---------------------CTGA-----------------------------------------------------------------------------------------------------------------------------------------------------
        SacCer-snR55/1-98                 TTATTTGATGAATAGACACCACAATCGTCTTTTTTTTATCCGGCGATGATTCCTTTGGAATATGTGCCATGGATT----ACATCATGCATCACCATCTGATT---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS HomSap-SNORD33/1-78 DE Homo Sapiens U33                   
        HomSap-SNORD33/1-78               GCCGGTGATGAGAACTTCTCCCACTCA------------CATTCGAGTT------TCCCGACCATGAGATGAC------TCCACATGCACTACCATCTGAGG---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GC SS_cons                      ----------------------------------------------------------((((-----------....--------------------(((-(((((-....-))))))))-------------------------------------------))))----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        //

.. _Sharma-2017: https://doi.org/10.1371/journal.pgen.1006804
.. _Yang-2015: https://doi.org/10.1093/nar/gkv058

