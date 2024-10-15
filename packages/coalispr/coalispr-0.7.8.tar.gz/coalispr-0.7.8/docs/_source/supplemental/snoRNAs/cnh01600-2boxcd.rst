.. role::  raw-html(raw)
   :format: html

.. |Dbox|  replace::  :raw-html:`<span class="mononorm">cuga</span>`
.. .. |Cbox|  replace::  :raw-html:`<span class="mononorm">rugauga</span>`
.. .. |nbsp| replace:: :raw-html:`&#x00A0;`

.. .. |extrBP|  replace:: ..S rRNA 
.. |extr|  replace::  :raw-html:`<span class="mononorm">(t)gacat</span>`
.. |targetRNA|  replace:: 18S rRNA
.. |target| replace:: :raw-html:`<span class="mononorm">aacg<a href="../18s-tab.html#snR88_18S" title="18S target">A</a>aggt</span>`
.. |ortholog| replace:: :raw-html:`yeast <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Saccharomyces_cerevisiae300071">snR54</a>, or human <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300691">SNORD59</a>`
.. |targetRNA-0|  replace:: 25S rRNA
.. |target-0| replace:: :raw-html:`<span class="mononorm">ggcg<a href="../18s-tab.html#snR88_25S_0" title="25S target?">G</a>gggt</span>`
.. |targetRNA-1|  replace:: 25S rRNA
.. |target-1| replace:: :raw-html:`<span class="mononorm">gaag<a href="../18s-tab.html#snR88_25S" title="25S target">T</a>ggagaaa</span>`
.. |target-1b| replace:: :raw-html:`<span class="mononorm">(atgtc)aaag<a href="../18s-tab.html#snR88_25S_2" title="25S target">T</a>ggagaaa</span>`
.. |ortholog-1| replace:: :raw-html:`fission yeast <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Schizosaccharomyces_pombe300057">snR88</a>`

.. |targetRNA-2|  replace:: 25S rRNA
.. |target-2| replace:: :raw-html:`<span class="mononorm">aag<a href="../18s-tab.html#snRcnh01600_25S" title="25S target?">A</a>ctaatcg</span>`

- Within intron of CNH01600 (CNAG_07884) for mitochondrial 37S ribosomal protein S35


.. figure:: /../_static/images/snoRNAs/snR88_h99_igb.png
   :name: snr88_h99_igb
   :align: left
   :width: 1389 px
   :height: 646 px
   :scale: 40%
   :figwidth: 100%

.. _snr88dbox:

snR88
=====


- snR88_intronic-boxCDsnoRNA-84nt-in-CNH01600


.. figure:: /../_static/images/snoRNAs/snR88-align.png
   :name: snr88-align
   :align: left
   :width: 1118 px
   :height: 411 px
   :scale: 40%
   :figwidth: 100%


- Predicted target D' guide in |targetRNA|\ : |target| 
- Targeted nt is in a *Cryptococcus* specific 18S rRNA sequence and close to that of a conserved A modified by |ortholog| (with an overlapping guide).
- D' guide is controlled by a canonical |Dbox| motif, which makes it unlikely that actually the same nt is methylated as in yeast, human or plant.
- An alternative target for the D' guide is in |targetRNA-0|\ : |target-0| but this relies on weaker G-U base pairs.
- Predicted target D guide in |targetRNA-1|\ : |target-1| and |target-1b|
- Orthologue of |ortholog-1|  (D guide).
- Accessory guide |extr| could extend base pairing of the D-guide with the second |targetRNA-1|\ target |target-1b|
- SnoR29 (see :ref:`SnoR29 in UTP17 <snor29a>` or :doc:`snoZ107-SnoR29b <cnag03967_z107>`) is the orthologue in *Tremellomycetes* with |ortholog-1| D'-guide.


.. rst-class:: mononote

>AE017348.1:681933-682016 Cryptococcus neoformans var. neoformans JEC21 chromosome 8 sequence :raw-html:`</br>`
CACTCGGATGAAAAAACCTATGACATAACCTTCGTTCTGAAGACTCAAACATATGGTTACTCTTTTTTCT :raw-html:`</br>`
TCACTTTCTGAAAA


|
|
|



snRcnh01600
===========

- snRcnh01600_intronic-boxCDsnoRNA-70nt-in-CNH01600
- Predicted target in |targetRNA-2|\ : |target-2|
- Requires experimental verification as D' and C' motifs are not obvious.
- Nucleotide to be modified appears unique for *Tremellomycetes*

.. figure:: /../_static/images/snoRNAs/snRcnh01600-align.png
   :name: snrcnh01600-align
   :align: left
   :width: 984 px
   :height: 307 px
   :scale: 40%
   :figwidth: 100%


.. rst-class:: mononote

>AE017348.1:682139-682208 Cryptococcus neoformans var. neoformans JEC21 chromosome 8 sequence :raw-html:`</br>`
ACAGATGATTTATTACGATTAGTCTTTAAGACACCTACATGGTTCCAACTTGCTTTATTTTGCTGATACT :raw-html:`</br>`

|
|
|
|
|
|

=======

- Image source snR88:
  
.. rst-class:: asfootnote

::

        # STOCKHOLM 1.0
        #=GF RW van Nues, July 2023
        #=GF https://coalispr.codeberg.page/paper
        Annot/1-49                   -------RTGATGA---------------------aCUGUA--UGGAAGCAACTGA-------------------RTGATGA----------AAAGAGGUGAARCTGA-----
        #=GS snR88/1-84 DE intronic-boxCDsnoRNA-84nt_in-CNH01600 ncrna 8:681932:682016:1
        snR88/1-84                   ---CACTCGGATGAAA------------AAACCTATGACAT-AACCTTCGTTCTGAAGACTCAAAC-------ATATGGTTACTCTT----TTTTCTTCACTTTCTGAAAA--
        #=GS H99/1-83 DE CP003833.2:c501869-501787 Cryptococcus neoformans var. grubii H99 chromosome 14, complete sequence
        H99/1-83                     ---TACTCGGATGAAA------------AAACCTATGACAT-AACCTTCGTTCTGAAGACCCAAAC-------ATATGGTTACTCTT----TTTTCTTCACTTTCTGAAA---
        #=GS R265/1-83 DE CP025768.1:c394331-394249 Cryptococcus gattii VGII R265 chromosome 10, complete sequence
        R265/1-83                    ---TACTCGGATGAAA------------CAACCTATGACAT-AACCTTCGTTCTGAAGACTCAAA-------CATATGGTTACTCTT----TTTTCTTCACTTTCTGAAA---
        #=GS WM276/1-84 DE CP000297.1:c394321-394238 Cryptococcus gattii WM276 chromosome L, complete sequence
        WM276/1-84                   ---TACTCGGATGAAA------------CAACCTATGACAT-AACCTTCGTTCTGAAGACTCAAA-------CATATGGTTACTCTT----TTTTCTTCACTTTCTGAAAA--
        #=GS KwoSha/1-86 DE NQVO01000031.1:63608-63693 Kwoniella shandongensis strain CBS 12478 scaffold00031, whole genome shotgun sequence
        KwoSha/1-86                  --TATCCCGGATGATA------------AAAAATATGACAT-AACCTTCGTTCTGAAGACATAAA-------CACATGGTTATCCTT-ATA-TTTCTTCACTTTCTGAAA---
        #=GS NaeEnc/1-81 DE MCFC01000037.1:c161464-161384 Naematelia encephala strain 68-887.2 BCR39scaffold_37, whole genome shotgun sequence
        NaeEnc/1-81                  --TCTCCCGGATGAAA------------CAAACTATGACATT-ACCTTCGTTCTGAAGACTA--T-------CCCATGGTTACACT-----TTTTCTTCACTTTCTGAAA---
        #=GS NaeAur/1-81 DE JAKFAO010000004.1:1532558-1532638 Naematelia aurantialba strain NX-20 Contig4, whole genome shotgun sequence
        NaeAur/1-81                  --TTTCCGGGATGAGA------------CAAC-TATGACATT-ACCTTCGTTCTGAAGACTCC---------TACATGGTTATCCT-----TTTTCTTCACTTTCTGAAAA--
        #=GS CryFlo/1-86 DE RRZH01000015.1:c317652-317567 Cryptococcus floricola strain DSM 27421 chromosome 14, whole genome shotgun sequence
        CryFlo/1-86                  --TACCCCTGATGAGA------------AAAAATATGACAT-AACCTTCGTTCTGAAGACTAATT-------CCCATGGTTACCAT--CTATTTTCTTCACTTTCTGAAA---
        #=GS CryAmy/1-87 DE MEKH01000013.1:c322436-322350 Cryptococcus amylolentus CBS 6273 supercont2.13, whole genome shotgun sequence
        CryAmy/1-87                  --TACCCCTGATGAGA------------AAAAATATGACAT-AACCTTCGTTCTGAAGACTAATT-------CCCATGGTTACCAT--CTATTTTCTTCACTTTCTGAAAT--
        #=GS KwoMan/1-86 DE ASQF01000001.1:c790611-790526 Kwoniella mangroviensis CBS 8886 cont1.1, whole genome shotgun sequence
        KwoMan/1-86                  ---TACTCGGATGAAA------------CAAAATATGACAT-AACCTTCGTTCTGAAGACATAAA-------ATCATGGTTATTATT-ATA-TTTCTTCACTTTCTGAACC--
        #=GS KwoHev/1-89 DE ASQB01000033.1:49862-49950 Kwoniella heveanensis BCC8398 cont1.33, whole genome shotgun sequence
        KwoHev/1-89                  -CCTTCCCTGATGAAA------------CAAATTATGACATTAACCTTCGTTCTGAAGACACA-A-------CACATGGTTATCACTCATA-TTTCTTCACTTTCTGAAAA--
        #=GS BulAlb/1-84 DE CAMYTR010000041.1:c218016-217933 Bullera alba genome assembly, contig: jcf7180000012134, whole genome shotgun sequence
        BulAlb/1-84                  --CATCTCGGATGATA------------CAAAATATGACAT-AACCTTCGTTCTTAAGACTAT---------TACATGGTTACATT--ATA-TTTCTTCACTTTCTGAAAC--
        #=GS CrySki/1-88 DE BCHT01000004.1:298391-298478 Cryptococcus skinneri DNA, scaffold: scaffold_3, strain: JCM 9039, whole genome shotgun sequence
        CrySki/1-88                  CTTATCTATGATGATA------------CAAA-TATGACAT-AACCTTCGTTCTGAAGACATA---------CCCATGGTTATTCTT-ATA-TTTCTTCACTTTCTGAAATAC
        #=GS PapTer/1-83 DE JAHXHD010000043.1:c4188-4106 Papiliotrema terrestris strain LS28 scaffold-42, whole genome shotgun sequence
        PapTer/1-83                  --CGTCTCTGATGAAA------------CAAACT-TGACAT-AACCTTCGTTCTTAAGACACC---------CACATGGTTACGATT--CA-TTTCTTCACTTTCTGAAAC--
        #=GS PapLau/1-84 DE JAAZPX010000001.1:341195-341278 Papiliotrema laurentii strain IF7SW-F4 scaffold1_cov209, whole genome shotgun sequence
        PapLau/1-84                  --TTTCTGGGATGAGA------------AAAAT--TGACATTAACCTTCGTTCTTAAGACACC---------TACATGGTTATCCTTT-CA-TTTCTTCACTTTCTGAAAA--
        #=GS CryGC4/1-83 DE JALPCA010000504.1:9806-9888 Cryptococcus sp. GC_Crypt_4 iso00_46_537, whole genome shotgun sequence
        CryGC4/1-83                  --CATCTCGGATGAAA------------CAAACT-TGACAT-AACCTTCGTTCTTAAGACAAAC--------CCCATGGTTACGATA--CA-TTTCTTCACTTTCTGAAA---
        #=GS TreTag/1-89 DE CAJHEQ010000942.1:2058-2146 MAG: Tremellales sp. Tagirdzhanova-0007 genome assembly, contig: TREM_942, whole genome shotgun sequence
        TreTag/1-89                  --TTTTTGGGATGAGA------------CAACA-ATGACATTAACCTTCGTTCTGAAGACTTTAAAA-----AACATGGTTACGCT---CATTTTCTTCACTTTCTGAAGCG-
        #=GS TreYok/1-82 DE BRDC01000026.1:153136-153217 Tremella yokohamensis NBRC 100148 DNA, KCNB35TY.26, whole genome shotgun sequence
        TreYok/1-82                  -----CCCTGATGAAA------------CAAACT-TGACATTAACCTTCGTTCTGAAGACATTC--------ACCCTGGTTACTCT---CATTTTCTTCACTTTCTGAAGC--
        #=GS TreMes/1-89 DE SDIL01000126.1:8155-8243 Tremella mesenterica strain ATCC 28783 supercont1.126, whole genome shotgun sequence
        TreMes/1-89                  CTCTCCTCTGATGATA------------CCAA-TATGACATTAACCTTCGTTCTGAAGACTAT---------CACATGGTTACGCTCG-TA-TTTCTTCACTTCCTGACTACT
        #=GS CryFla/1-83 DE CAUG01000211.1:c64505-64423 Cryptococcus flavescens NRRL Y-50378 WGS project CAUG00000000 data, contig NODE_284_length_200747_cov_45_572124, whole genome shotgun sequence
        CryFla/1-83                  ---TACTCTGATGAAA------------CAAACT-TGACAT-AACCTTCGTTCTTAAGACATC---------CACATGGTTACGATA--CA-TTTCTTCACTTTCTGAAACT-
        #=GS TriOvo/1-100 DE JAMFRG010000016.1:c290339-290240 Trichosporon ovoides strain Y9002B ctg_16, whole genome shotgun sequence
        TriOvo/1-100                 -----TCCTGATGAGAAACATGACACGACATTCTTTAATTTAAGACTCACAAATCGGGACT-TTGTC-----CCAATGGTTACTCAAA-CA-TTTCTTCACTTTCTGATCCGA
        #=GS TriInk/1-104 DE JXYM01000003.1:2528582-2528685 Trichosporon inkin strain JCM 9195 scaffold_0003, whole genome shotgun sequence
        TriInk/1-104                 TCTCTCCCTGATGAGAAACATGACACGACATTCTTTACCTAAAGACGCACAA-TCGGGACTCTCGTC-----CCAATGGTTACTCAAA-CA-TTTCTTCACTTTCTGATCCA-
        #=GS SchPom-snR88/1-84 DE Schizosaccharomyces_pombe snR88 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Schizosaccharomyces_pombe300057
        SchPom-snR88/1-84            -----TATCGAGGAGG------------ATAAAAATGACATGTCAAGCTCAACAATATGAAAAATTATGATTTTTTT------------CTATTTCTTCACTTTCTGAGATGT
        Annot-SacCer/1-46            -------RTGATGA---------------------------AUUGAAAGCAAGA-CTGA----------------RTGATGA----------------------CTGA-----
        #=GS SacCer-snR54/1-86 DE 18S:A974 Saccharomyces_cerevisiae snR54 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Saccharomyces_cerevisiae300071
        SacCer-snR54/1-86            ---TAAGATGATGATCAA----------CTTTTTATATCAATAACTTTCGTTCTACTGACTGTGATCAAACGATCTTGTAGAG-----------AACTTTTACTCTGAAT---
        #=GS HomSap-SNORD59A/1-75 DE 18S:A1031 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300691
        HomSap-SNORD59A/1-75         -CCTTCTATGATGAT----------------TTTATCAAAATGACTTTCGTTCTTCTGAGTT-----------TGCTGAAGCCA----------CATTTAGGTACTGAGAAGG
        #=GS HomSap-SNORD59B/1-71 DE 18S:A1031 http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Homo_sapiens300690
        HomSap-SNORD59B/1-71         --CCTCACTGATGAGT-------------------ACGTTCTGACTTTCGTTCTTCTGAGTT-----------TGCTGAAGCCA----------GATGCAATTTCTGAGAAGG
        #=GS AraTha-SnoR59a/1-76 DE 18S:A975,25S:G1845  Arabidopsis_thaliana
        AraTha-SnoR59a/1-76          --CTCTTATGATGTCAA-------------------------AACTTTCGTTCTCCTGAGATTTC----AATATGCTGAAAAAAA------TTGGAGACCTGAACTGAAAGAG
        // 




- Image source snRcnh01600:
  
.. rst-class:: asfootnote

::

        # STOCKHOLM 1.0
        #=GF RW van Nues, July 2023
        #=GF https://coalispr.codeberg.page/paper
        Annot/1-33               ---RTGATGA----------GCUAAUCAGAA-CTGA---------------RTGATGA--------------------------CTGA--------
        #=GS snRcnh01600/1-70 DE intronic-boxCDsnoRNA-70nt-in-CNH01600 ncrna 8:682138:682266:1
        snRcnh01600/1-70         --ACAGATGATTTATTA---CGATTAGTCTTTAAGACACCTA--------CATGGTTCCAACT---------TGCTTTATTTTGCTGATACT----
        #=GS H99/1-70 DE CP003833.2:c501664-501595 Cryptococcus neoformans var. grubii H99 chromosome 14, complete sequence
        H99/1-70                 --ACAGATGATTTATTA---CGATTAGTCTTTAAGACACCTA--------CATGGTTCCAACT---------TGCTTTATTTTGCTGATACT----
        #=GS R265/1-70 DE CP025768.1:c394125-394056 Cryptococcus gattii VGII R265 chromosome 10, complete sequence
        R265/1-70                --ACAAATGATTTATTA---CGATTAGTCTTTAAGACACCTA--------CATGGTTCCAACT---------TGCTTTATTTTGCTGATATT----
        #=GS WM276/1-70 DE CP000297.1:c394114-394045 Cryptococcus gattii WM276 chromosome L, complete sequence
        WM276/1-70               --ACAGATGATTTATTA---CGATTAGTCTTTAAGACACCTA--------CATGGTTCCAACT---------TGCTTTATTTTGCTGATACT----
        #=GS CryFlo/1-68 DE RRZH01000015.1:c317441-317374 Cryptococcus floricola strain DSM 27421 chromosome 14, whole genome shotgun sequence
        CryFlo/1-68              --TATGATGTTTAA------CGATTAGTCTTTAAGACAACTA--------CATGGTTCCAACTT-------ACGCTTTACCT-GCTGAACCT----
        #=GS CryAmy/1-72 DE MEKH01000013.1:c322224-322153 Cryptococcus amylolentus CBS 6273 supercont2.13, whole genome shotgun sequence
        CryAmy/1-72              --TATGATGTTGAA------CGATTAGTCTTTAAGACAACTA--------CATGGTTCCTACTT-------ACGCTTTACCT-GCTGAACCTTCTT
        #=GS NaeEnc/2-72 DE MCFC01000037.1:c161299-161228 Naematelia encephala strain 68-887.2 BCR39scaffold_37, whole genome shotgun sequence
        NaeEnc/2-72              TTTATGATGAGTATA-----CGATTAGTCTTTAAGACTTCTA--------CATGGTTCCTAACA-------ATGCATGGCTTT-CTGATCCT----
        #=GS NaeAur/1-72 DE JAKFAO010000004.1:1532730-1532801 Naematelia aurantialba strain NX-20 Contig4, whole genome shotgun sequence
        NaeAur/1-72              TCTATGATGAGTATA-----CGATTAGTCTTTAAGACTTCTA--------CATGGTTCCTACCA-------ATGCATGGCTTT-CTGACACAC---
        #=GS KwoMan/1-80 DE ASQF01000001.1:c790356-790277 Kwoniella mangroviensis CBS 8886 cont1.1, whole genome shotgun sequence
        KwoMan/1-80              --AATGATGACTACT-----TGATTAGTCTTTAAGACTTCACAGTAAACTTATGGTTATAAACC-------ATGCATGGCTTT-CTGATACTCTT-
        #=GS BulAlb/1-73 DE CAMYTR010000041.1:c217802-217730 Bullera alba genome assembly, contig: jcf7180000012134, whole genome shotgun sequence
        BulAlb/1-73              -CAGTGATGAGTAAC-----CGATTAGTCTTTAAGACACATA--------CGTGGTTCCAAACTCCA----ATGCATGGCTTT-CTGATCAT----
        #=GS CrySki/1-82 DE BCHT01000004.1:298637-298718 Cryptococcus skinneri DNA, scaffold: scaffold_3, strain: JCM 9039, whole genome shotgun sequence
        CrySki/1-82              TCTATGATGAATTCAAAAATCGATTAGTCTTGAAGACACCTT--------CATGGTTACAAAAATTTAC-AATGCATGGCTTT-CTGATCTT----
        #=GS PapTer/2-75 DE JAHXHD010000043.1:c3988-3914 Papiliotrema terrestris strain LS28 scaffold-42, whole genome shotgun sequence
        PapTer/2-75              ACAGTGATGATCAAC-----CGATTAGTCTTGAAGACACCTA--------CATGGTTTCAAACTCCA----ATGCATGGCTTT-CTGACCTT----
        #=GS PapLau/3-73 DE JAAZPX010000001.1:341412-341484 Papiliotrema laurentii strain IF7SW-F4 scaffold1_cov209, whole genome shotgun sequence
        PapLau/3-73              TCAATGATGAGCAC------CGATTAGTCTTTAAGACATCTA--------CATGGTTCCAAACTC------ATGCATGGCTTA-CTGATCCT----
        #=GS CryGC4/2-71 DE JALPCA010000504.1:10035-10105 Cryptococcus sp. GC_Crypt_4 iso00_46_537, whole genome shotgun sequence
        CryGC4/2-71              TTCATGATGATCAA------CGATTAGTCTTTAAGACTTACA--------CATGGTTCCAAACA-------ATGCATGGCTTT-CTGATACT----
        #=GS TreTag/2-82 DE CAJHEQ010000942.1:2280-2361 MAG: Tremellales sp. Tagirdzhanova-0007 genome assembly, contig: TREM_942, whole genome shotgun sequence
        TreTag/2-82              TTCGTGATGATCGCAA----CGATTAGTCTTGAAGACATATACT------CATGGTTTCACATTCTGTCA-ATGCATGGCTTT-CTGATACCA---
        #=GS TreYok/2-74 DE BRDC01000026.1:153357-153430 Tremella yokohamensis NBRC 100148 DNA, KCNB35TY.26, whole genome shotgun sequence
        TreYok/2-74              TCTATGATGAGCACA-----CGATTAGTCTTTAAGACACCCA--------CATGGTTTCAAACAAC-----ATGCATGGCTTT-CTGACCCT----
        #=GS TreMes/2-70 DE SDIL01000126.1:8434-8507 Tremella mesenterica strain ATCC 28783 supercont1.126, whole genome shotgun sequence
        TreMes/2-70              TTTATGATGAGCAA------CGATTAGTCTTTAAGACTCACA--------CATGGTTCCAAAACTC-----ATGCATGGCTTA-CTGAA-------
        #=GS KocImp/4-73 DE NBSH01000008.1:c624743-624671 Kockovaella imperatae strain NRRL Y-17943 BD324scaffold_8, whole genome shotgun sequence
        KocImp/4-73              TTCATGATGAGCAA------CGATTAGTCTTTAAGACTTCTA--------CATGGTTCCAAATC-------ATGCATGGCTTA-CTGATTCA----
        #=GS VanFra/2-80 DE BEDY01000002.1:2380378-2380457 Vanrija fragicola DNA, scaffold: scaffold_2, strain: JCM 1530, whole genome shotgun sequence
        VanFra/2-80              ACAGTGATGATTGAGAT---CGATTAGTCTTGAAGACTCCAAA-------CATGGTTAAACAACCTCCA--ATGCATGGCTTT-CTGACCCT----
        #=GS TriOvo/1-85 DE JAMFRG010000016.1:c290086-290006 Trichosporon ovoides strain Y9002B ctg_16, whole genome shotgun sequence
        TriOvo/1-85              TTCATGATGAGCGAGAT---CGATTAGTCTTGAAGACCCTAAA-------CGTGGTTAAACAACCCCTCTTATGCATGGCTTT-CTGATTCCACCT
        //
