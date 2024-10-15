.. role::  raw-html(raw)
   :format: html
   
.. |targetRNA|  replace:: 25S rRNA
.. |target| replace:: :raw-html:`<span class="mononorm">(ctgttg)agct<a href="../18s-tab.html#snr66_25Sm" title="25S target">T</a>gactcta</span>`
.. |ortholog| replace:: :raw-html:`yeast <a href="http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Saccharomyces_cerevisiae300061">snR66</a>`
.. |extrBP-1|  replace:: 18S rRNA 
.. |extr-1|  replace::  :raw-html:`<span class="mononorm">ttgccaac</span>`
.. |extr-2|  replace::  :raw-html:`<span class="mononorm">tggcctgtt</span>`
.. |extr-3|  replace::  :raw-html:`<span class="mononorm">tgacag</span>`
.. |extrBPtarget-1|  replace:: :raw-html:`<span class="mononorm"><a href="../18s-tab.html#snr66_18Sxtr1" title="18S extra base-pairiong?">gttggtgg</a></span>`
.. |extrBP-2|  replace:: 25S rRNA 
.. |extrBPtarget-2a|  replace:: :raw-html:`<span class="mononorm"><a href="../18s-tab.html#snr66_25Sxtr2a" title="18S extra base-pairing?, Cryptococcus">gacgggtca</a></span>`
.. |extrBPtarget-2b|  replace:: :raw-html:`<span class="mononorm"><a href="../18s-tab.html#snr66_25Sxtr2b" title="25S extra base-pairing?, conserved">gacaggtta</a></span>`



.. upstream snR66 target: aagaccctgttgagct
..  extrBP-3 rYTGTYR:         CTGTTG
.. Crypto-ETS1  3a GCTGTTG, 3b ACTGTCA
.. 18S 3c GTTGTTG, 3d ACTGTCG
.. 25S 3e ATTGTTG, 3f ATTGTCA
   <a id="snr66_25Sxtr3e" href="snoRNAs/snr66.html" title="snR66 accessory base-pairing?">attgttg</a>


snR66
=====

.. figure:: /../_static/images/snoRNAs/snr66_h99_igb.png
   :name: snr66_h99_igb
   :align: left
   :width: 1389 px
   :height: 646 px
   :scale: 40%
   :figwidth: 100%


- snR66_processed-boxCDsnoRNA-118nt-as-`URS000035E911_235443 <https://rnacentral.org/rna/URS000035E911/235443>`_
- Processed from dedicated transcript (as CNAG_12022)
- Predicted target in |targetRNA|\ : |target|
- Orthologue of |ortholog|
- Various conserved segments could be accessory guides [van.Nues-2011_], with |extr-3| just upstream of the D-box extending the modification guide (brackets).
- These sections could determine different snoRNA conformations or interact in trans with (pre-)rRNA; complimentary regions are: 

  - motif |extr-1|, possible target: |extrBP-1|, |extrBPtarget-1| 
  - motif |extr-2|, possible target: |extrBP-2|, |extrBPtarget-2a| or |extrBPtarget-2b|


.. figure:: /../_static/images/snoRNAs/snR66-trimmed.png
   :name: snR66-trimmed-align
   :align: left
   :width: 1456 px
   :height: 268 px
   :scale: 40%
   :figwidth: 100%


.. rst-class:: mononote

>AE017341.1:c347820-347703 Cryptococcus neoformans var. neoformans JEC21 chromosome 1, complete sequence :raw-html:`</br>`
CGCCCAGTGATGAGAATTGCCAACACAATAGAGTCAAGCTCGGAGACCCTAGTCGCCTCTTCGGATGGTG :raw-html:`</br>`
CTGGTCTATGTCGAGCACTGGCCTGTTTGACAGTTACTGAGGGTTCAT



|
|
|
|
|
|

=======

- Image source:
  
.. rst-class:: asfootnote

::

        # STOCKHOLM 1.0
        #=GF RW van Nues, June 2023
        #=GF https://coalispr.codeberg.page/paper
        Annot/1-58                ---------------------------------------------------------------------------------------------------------------------------------------------------------RTGATGA---GGUGGUUG-----AUCUCAGUUCGACTGA-------------------------------------------RTGATGA-aCUGGGCAG-GTTGTC-----CTGA--------------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS snR66/6-123 DE processed boxCDsnoRNA-120nt-as-URS000035E911_235443 ncrna 1:347702:347818:-1
        snR66/6-123               ---------------------------------------------------------------------------------------------------------------------------------------------------CGCCCAGTGATGAGAATTGCCAACACA-ATAGAGTCAAGCTCGGAGACCCTAGTCGCCTCT----TC---GGATGGTGCTGGTCTATGTCGAGCACTGGCCTGTT-TGACAGTT--ACTGAGGGTTCAT------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS H99/1-414 DE CNAG_12022 ENA|CP003820.1:382584..382997:ncRNA|CP003820.1:382584..382997:ncRNA.1 Cryptococcus neoformans var. grubii H99 hypothetical RNA
        H99/1-414                 AAACATCTCTATTTTACAAGTTAGAGACGAATCAACAGGGCTACAGGACACAGCAAGCCAGGTGGCACATCATGTGGCGCAAGGTCGGTCGTGTCTTGTATTCTTGTTGCTCTTCATCTACCTTTCCTTTTCGTCTTTTTTCTTTCACGCCCGGTGATGAGAATTGCCAACACA-ATAGAGTCAAGCTCGGAGACCCTAGTCGCCTCT----TC---GGATGGTGCTGGTCTATGTCGAGCACTGGCCTGTT-TGACAGTT--ACTGAGGGTTCATCTTTTTCGTGTCTTTCATCATGTCGCTCCTTATCTTGGATCCATCAAACAACCTGTCAACATTTTGGTTCCAAGGTCTCATTTATTATGAAAATATATGCATGTATTGCAGATCAACTGAACAT-GTTTCTGCCAATCAATCCCAAATAG
        #=GS H99-snR66/148-263 DE CNAG_12022 ENA|CP003820.1:382584..382997:ncRNA|CP003820.1:382584..382997:ncRNA.1 Cryptococcus neoformans var. grubii H99 hypothetical RNA
        H99-snR66/148-263         ---------------------------------------------------------------------------------------------------------------------------------------------------CGCCCGGTGATGAGAATTGCCAACACA-ATAGAGTCAAGCTCGGAGACCCTAGTCGCCTCT----TC---GGATGGTGCTGGTCTATGTCGAGCACTGGCCTGTT-TGACAGTT--ACTGAGGGTTC--------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS R265/1-393 DE ENA|CP025762.1:341899..342291:ncRNA|CP025762.1:341899..342291:ncRNA.1 Cryptococcus gattii VGII R265 hypothetical RNA
        R265/1-393                -TCACAAGTCACAACACAGATCGGCGATCAACCAACTGGACTACAGGACACAGCAAGCTAGGTGGCACTTTATGTGGCGCAAAGCCGGTTGTGTCTTGTATTCTTGTTGCTCTTCATCTACTCTTTTTTTTTATCTTTTTATTTTTATGCCCAGTGATGAGAATTGCCAACACA-ATAGAGTCAAGCTCGGAGACCCTAGTCGCCTCT----TC---GGATGGTGCTGGTCTATGTCGAGCACTGGCCTGTT-TGACAGTT--ACTGAGGGTTCATCTTTTTCGTGTCTTTTT--ATGTC-TTCCT------TTGTCTAGCATCCACCAAACAAGCTGCCAAAGTTCGAGGTCATTTATC--ATGAACACCTATGCATGTATTGCAAATCAACTGAACATTGATTCTGCCAATCAA----------
        #=GS CutCut/1-119 DE LTAL01000688.1:c26738-26620 Cutaneotrichosporon cutaneum strain ACCC 20271 contig688, whole genome shotgun sequence
        CutCut/1-119              ------------------------------------------------------------------------------------------------------------------------------------------------CTCCACCCTATGATGAGAATTGCCAACAAAT-TAGAGTCAAGCTCGGAGACCCTAGTCGCGACCT---TC----GGGCGTGCTGGTTAATGCCGAGTGTCGGCCTGTC-TGACAGTT-CGCTGAGGGCT---------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS Nae/1-116 DE MCFC01000009.1:c77628-77513 Naematelia encephala strain 68-887.2 BCR39scaffold_9, whole genome shotgun sequence
        Nae/1-116                 -------------------------------------------------------------------------------------------------------------------------------------------------TTCACCCAGTGATGAGACTTGCCAACACA-ATAGAGTCAAGCTCTTAGACCCTAGTCGCCTT-----TT-------GGTGCTGGTCAGAGACGAGCACTGGCCTGTTTTGACAGTT-TACTGAGGGATAT-------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS CryWin/1-121 DE AWGH01000001.1:c1175943-1175823 Cryptococcus wingfieldii CBS 7118 supercont1.1, whole genome shotgun sequence
        CryWin/1-121              --------------------------------------------------------------------------------------------------------------------------------------------------ACGCCCTATGATGAGAGTTGCCAACAC--ATAGAGTCAAGCTCGGAGACCCTAGTCGCTTTCT---TC---GGATCGTGCTGGTCATTGTCGAGTGTCGGCCTGTT-TGACAGTAAAACTGAGGGCTCAT------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS CrySki/1-121 DE BCHT01000002.1:c1897-1777 Cryptococcus skinneri DNA, scaffold: scaffold_1, strain: JCM 9039, whole genome shotgun sequence
        CrySki/1-121              ------------------------------------------------------------------------------------------------------------------------------------------------ATATCCCCTATGATGAGAATTGCCAACAC--ATAGAGTCAAGCTCGGAGACCCTAGTCGCCCGTT---TC--GACGGTGTGCTGGTCCATGTCGAGGTCTGGCCTGTT-TGACAGTT-TACTGAGGGTCT--------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS CryFagi/1-114 DE BCHU01000002.1:574810-574923 Cryptococcus fagi DNA, scaffold: scaffold_1, strain: JCM 13614, whole genome shotgun sequence
        CryFagi/1-114             -----------------------------------------------------------------------------------------------------------------------------------------------------CCCAGTGATGAGAATTGCCAACAA--ATAGAGTCAAGCTCGGAGACCCTAGTCGCATCCT---TC--GGGATTGTGCTGGTCATTGTCGAGGTCTGGCCTGTC-TGACAGTT-TACTGAGGGT----------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS KwoShan/1-123 DE NQVO01000063.1:c20954-20832 Kwoniella shandongensis strain CBS 12478 scaffold00063, whole genome shotgun sequence
        KwoShan/1-123             ---------------------------------------------------------------------------------------------------------------------------------------------------CGCCCAACGATGAGAATTGCCAACAAA-ATAGAGTCAAGCTCGGAGACCCTAGTCGCCTTTCCT-TC-GGGGGAGGTGCTGGTTAATGTCGAGCACTGGCCTGTTATGACAGTT-TACTGAGGGTTC--------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS TakKor/2-415 DE BCKT01000006.1:c1137184-1136770 Takashimella koratensis DNA, scaffold: scaffold_5, strain: JCM 12878, whole genome shotgun sequence
        TakKor/2-415              CTCATGCAGCAGTATCCCCTTCACCCGTGTTAGCTTCTGGCGGTTTTTAGCATCTACTCATGTCCTCTCTCAACATTGACGTCTGCCCCGACCGCCTCCCAACCCTCCCCCCTTCTAACCCCTGTCCCCCTACCCCCCTCCCCTCCTCCCCCTGTGATGAGAATTGCCAACACATATAGAGTCAAGCTCGTAGACCCTAGTCGCCCT-----TC-----GGGGTGCTGGTCTATGCCGAGCACTGGCCTGTTTTGACAGTT-TACTGAGGGCTCAACTACCTAGTCTCCCAATGCACCCATTACTGTTATGTCCCTGCTGCATGATGCCGGATCCCTTTCACGGCAGTATCCCTGATAGGTATAAAGGTATAAAAGATAGAAAGACCAAAGATGAAAGTAATAGGAAGAGCCAATGTTCGTTTTG-
        #=GS VanHum/7-421 DE QKWK01000001.1:457854-458274 Vanrija humicola strain CBS 4282 CBS4282_scaffold01, whole genome shotgun sequence
        VanHum/7-421              TGCCAGGCGATACTCACCGCGGCCTACGCACACCTTCCTCCCCAGCTCCACACCGCTCCCCTCCCCTCCCCTCCCCTCCCCTCCCCTCCTCGTCCCAGTCCCGTCCTTCTTCCGCCTCTCCTCCTCTCCCCATCCCATCCCCTTCCCTACCCGATGATGAGAGTTGCCAACACAA-TAGAGTCAAGCTCGGAGACCCTAGTCGCTACCT---TC---GGGA-GTGCTGGTTAATGCCGAGTGTCGGCCTGTT-TGACAGTAACACTGAGGGCTCTTCTTTCTCCATTCTTTCCTATCTTCCAGCTATCTCCTCCCCTGTGCGGGCGCGGTGTTCGTAGCATATCTCATTACTTGACATGCACATGGTGTTTGGGCGTTTTTGGGTGCTTTATGGTGTTCTACACAGAAACAGGAAGATGACGCG--
        #=GS TriGue/1-409 DE BCJX01000001.1:3202421-3202835 Trichosporon guehoae DNA, scaffold: scaffold_0, strain: JCM 10690, whole genome shotgun sequence
        TriGue/1-409              ----AAAGATGCTGGCCCTAACACTCCCCGCATCTTTTCACCACCAACCGTCCGCGACAGTGCCGGCGCGATGAGGCGGCGCAAACCCGTCCCCTCGTCGTCTGGCCAAGTGTCTCTCTTCCCCTCATCTCCCCTCCTTTCCCCATCCACCTCATGATGAGAATTGCCAACAAAT-TAGAGTCAAGCTCGGAGACCCTAGTCGCCGC-----TT-----GCGGTGCTGGTTAATGCCGAGTGTCGGCCTGTC-TGACAGTT-CACTGAAGGTCTTTCATCCTTGTCCTTTTCCGTTGTCTACTAGTGTTTTGTCCCTTGTCCTGCTATGAATATTATGGAAATCGAAAGCGAAAAGGAGATGGAGTTGCATTACACTTACGACGATGGAGGCTGACTGGCAAATTGAAGTGACCAAGGGCAAGGGC
        #=GR SS                   ---------------------------------------------------------------------------------------------------------------------------------------------------------------------<<<---------------------------------((((((------------))))))------------------->>>((((----))))-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GR SS                   ------------------------------------------------------------------------------------------------------------------------------------------------------------------<<<<-<<--------------------------------((((((------------))))))---------------------------->>->>>>----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GC SS                   -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------<<<<-<<---------------((((((------------))))))------------------------>>-->>>>-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #=GS SacCer-snR66/1-85 DE http://snoopy.med.miyazaki-u.ac.jp/snorna_db.cgi?mode=sno_info&id=Saccharomyces_cerevisiae300061
        SacCer-snR66/1-85         -----------------------------------------------------------------------------------------------------------------------------------------------------TCAAATGATGAAATACCAATGCAA---CAGAGTCAAGCTCTGA----------GTTTC---AAAAA----GAAAC----------ATGGACGAGA---TTGCTT-TTTT--ATTACTGACC------------------------------------------------------------------------------------------------------------------------------------------------------------
        // 


.. _van.Nues-2011: https://doi.org/10.1038/emboj.2011.148


