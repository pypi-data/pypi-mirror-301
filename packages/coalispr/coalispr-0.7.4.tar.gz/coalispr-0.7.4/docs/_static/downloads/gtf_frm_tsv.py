#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  gtf_frm_tsv.py
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Create a gtf for counting reads as reference using 'features', from a
tabulated file with self-annotated siRNA-segments. The tsv file was built
by copying locations straight from the IGB browser to create an index
of chr:[start-stop](size).
"""

import csv
import pandas as pd
import re
import sys
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from datetime import datetime
from pathlib import Path

exts = ['.tsv','.tab','.csv']
prefix = '@'
headers = { 1: 'JEC21', 2:'H99', }
#useheaders = ''

def clean_igb(row): #,index_string):
    """Function to convert genome coordinates copy-pasted from IGB to a tsv file,
    loaded into dataframe that needs cleaning up; use via apply.
    """
    #https://stackoverflow.com/questions/43483365/use-pandas-groupby-apply-with-arguments
    #in apply 2nd argument needs put in 'args='
    #                   Segment <chr:[start-stop](size)>
    #index_string = row #['Segment <chr:[start-stop](size)>']
    #1: [24,645 - 24,799] (+154)
    #'1: [1,122 - 1,740] (+618)'
    sub1 = re.sub("[\[,\] \n\+\<\>\)]",'',row)
    #gives: 1:24645-24799(154
    #then to: 1_24645_24799_154
    return re.sub(':|\(|\-','_',sub1)


def create_siRNA_GTF_line(row):
    """Function to create GTF from self-annotated file with peak regions."""
    #global prefix
    segment=str(row["segm"]).strip().split("_")
    #1_24645_24799_154_sRNA
    #[1,24645,24799,154,sRNA]
    seqname=segment[0]
    source="srnaseq"
    feature="sirnasegment"
    start=segment[1]
    end=segment[2]
    #if upper strand is target; siRNAs are on lower strand
    if row['Fragment'] == "target":
        strand = "-"
        #prefix = "_"
    elif row['Fragment'] == "siRNA":
        strand = "+"
        #prefix = '@'
    else:
        strand="."
    genid = row["gene_id"]
    annot = row["Annotation"]
    if useheaders == 'JEC21':
        loc = row["locs"]
        peak = row["Peak"]
        hom = row["Homology"]
        gtfline = (f"{seqname}\t{source}\t{feature}\t{start}\t{end}\t."
            f"\t{strand}\t.\tgene_id \"{prefix}{genid}\"; peak \"{peak}\"; locus "
            f"\"{loc}\"; annotation \"{annot}\"; homology \"{hom}\";")
    elif useheaders == 'H99':
        K9 = row["K9"]
        K27 = row["K27"]
        CpG = row["CpG"]
        gtfline=(f"{seqname}\t{source}\t{feature}\t{start}\t{end}\t."
            f"\t{strand}\t.\tgene_id \"{prefix}{genid}\"; K9 \"{K9}\"; K27 \"{K27}\"; "
            f"CpG \"{CpG}\"; annotation \"{annot}\"; ")
    return gtfline


def get_GTF_comment():
    if useheaders == 'JEC21':
        comment = (
            "# Gene-ids needed to be both unique and informative; and \n"
            "# might look a bit cryptic but convey some simple information \n"
            "# using qualifiers seperated by underscores. \n"
            "# For example: '@1_use_3endCNA03010_harbidom_822':\n"
            "# \t prefix ('@'): symbol indicative for 'anti' or 'targeting'.\n"
            "# \t number ('1'): chromosome where segment has been mapped. \n"
            "# \t qualifier ('use'): \n"
            "# \t\t u/mu/nu: \n"
            "# \t\t\t u : by STAR mapping criteria this section is unique. \n"
            "# \t\t\t nu: not unique \n"
            "# \t\t\t mu: mostly unique \n"
            "# \t\t\t s: transcript has been spliced before siRNAs are made. \n"
            "# \t\t\t   Sometimes splicing can seem incomplete.\n"
            "# \t\t\t   Intron prediction can be inaccurate because:\n"
            "# \t\t\t   a) no reads in RNAseq data to confirm the prediction.\n"
            "# \t\t\t   b) it could be wrong; for example when siRNA reads \n"
            "# \t\t\t   were found against the putative intron section.\n"
            "# \t\t\t   c) STAR-mapping by breaking reads where the gap could \n"
            "# \t\t\t   align to an actual but not predicted intron; covered \n"
            "# \t\t\t   by many different reads; with acceptable splice sites \n"
            "# \t\t\t   and recognizable branchpoint.\n"
            "# \t\t\t c: segment maps to a centromeric region or to its edges; \n"
            "# \t\t\t   mostly observed in samples obtained from strains that \n"
            "# \t\t\t   cannot methylate histones (c4/clr4 deletion) or DNA \n"
            "# \t\t\t   (d5/dnmt5 deletion).\n"
            "# \t\t\t e: target transcript is expressed under conditions \n"
            "# \t\t\t   Wallace-2020 (https://doi.org/10.1093/nar/gkaa060)\n"
            "# \t\t\t   isolated RNA for generating their data. Sometimes \n"
            "# \t\t\t   the target transcript  is realtively more expressed \n"
            "# \t\t\t   in the absence of Ago1 (used as a 'duplicate').\n"
            "# \t label ('3endCNA03010_harbidom'): short acronym for locus \n"
            "# \t       (if known, then in  CAPITALS) or homologous element \n"
            "# \t       (in undercase) from JEC21, B-3501 (crynb) or H99 (cnag_) \n"
            "# \t       followed by underscore and extra info ('harbidom').\n"
            "# Prefixes are:\n"
            "# \t ups:  upstream of\n"
            "# \t dwn:  downstream of\n"
            "# \t 3end: 3' end region of\n"
            "# nt-length ('822'): length of segment with siRNA reads, which \n"
            "#       is often over 3'end part of a target transcript or at a \n"
            "#       site of double-stranded RNA in case of a nearby gene on \n"
            "#       the opposite strand.\n")
    elif useheaders == 'H99':
        comment = (
            "# K9 (from Dumesic 2015; doi:10.1016/j.cell.2014.11.039)\n"
            "#\tK9-methylation   over region with siRNA peaks\n"
            "#\t-\tnot present (equal to deletion of clr4)\n"
            "#\t+\tpresent (absent in deletion of clr4)\n"
            "# K27 (from Dumesic 2015; doi:10.1016/j.cell.2014.11.039)\n"
            "#\t-\tnot present (equal to deletion of ezh2)\n"
            "#\t+\tpresent (absent in deletion of ezh2)\n"
            "# CpG (from Huff 2014; doi:10.1016/j.cell.2014.01.029)\n"
            "#\t-\tnot present (equal to deletion of dnmt5)\n"
            "#\t+\tpresent (absent in deletion of dnmt5)\n")
    return comment


def tsv2gtf(file_name, prefix, cryp, gtf_name):
    """Function to convert tsv input to gtf output

    file_name : str
        Name input file
    prefix : str (default: '@')
        Prefix for gene_id to express 'anti'
    cryp : int (default: 1)
        Use headers for 1: JEC21; 2: H99
    gtf_name : str
        Output filename
    """
    global useheaders
    useheaders = headers[cryp]
    def validate(df):
        check = df.isna().any().any().sum()
        if check !=0:
            missingdata_list = df.columns[df.isnull().any()].tolist()
            msg = (f"Empty cells in {', '.join(missingdata_list)} of the input;"
                  ", please check, stopping...")
            raise SystemExit(msg)
        elif df[df.duplicated()].empty == False:
            msg = "The input file has duplicates, please check, stopping..."
            raise SystemExit(msg)
        else:
            msg = "The input file seems workable, ..."
            #print(msg)
            pass

    filepath = Path(file_name)
    if not filepath.suffix in exts:
        raise SystemExit("Please use expected fileformat ({', '.join(exts)}).")
    output = Path(gtf_name) if gtf_name else filepath
    output = output.with_suffix('.gtf')

    try:
        df=pd.read_csv(filepath, sep="\t", comment='#')
    except FileNotFoundError:
        msg = (f"{file_name} not found, stopping..")
        raise SystemExit(msg)

    validate(df)
    #df['agenid'] = prefix + df["gene_id"]
    #df = df.drop("gene_id", axis=1)
    #df = df.rename(columns = {'agenid':"gene_id"})
    rownam = 'Segment <chr:[start-stop](size)>'
    #print(df['Segment <chr:[start-stop](size)>'])
    #return
    df["segm"] = df.apply(lambda row : clean_igb(row[rownam]), axis=1)
    if useheaders == 'JEC21':
       df["locs"] = df.apply(lambda row : clean_igb(row['Locus']), axis=1)
    df["gtfline"] = df.apply(lambda row : create_siRNA_GTF_line(row), axis=1);

    with open(output,"w") as seq_id:
        seq_id.write("##gff-version 2 \n# created on: "
            f"{datetime.now().strftime('%d-%m-%Y')}\n# by 'python3 "
            f"gtf_frm_tsv.py -f {file_name} -c {cryp}'.\n{get_GTF_comment()}")
        df.gtfline.to_csv(seq_id,index=False,header=False,
            quoting=csv.QUOTE_NONE, quotechar='"',escapechar='\\')
    #    df.agenid.to_csv(seq_id,index=False,header=False,
    #        quoting=csv.QUOTE_NONE, quotechar='"',escapechar='\\')


def main(args):

    descrip = ("Translate tabbed siRNA features file -f for Cryptococcus -c to "
               ".gtf and output as -o; include prefix -p in gene-id.")

    # Disable default help
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit.')
    required.add_argument('-f','--tsv_file', type=str, required=True,
        help=f"required input file with extension {', '.join(exts)}.")
    optional.add_argument('-p','--prefix', type=str, default=prefix,
        help=f"prefix for gene-id to express 'targeting', default: {prefix}.")
    optional.add_argument('-c','--cryp', type=int, choices=[1,2],
        default=1,
        help=("which Cryptococcus the annotation is done for, 1: 'JEC21', "
            "2: 'H99'; 'default: 1 ('JEC21')."))
    optional.add_argument('-o','--output_gtf', type=str, default='',
        help=("name of gtf file to save, default: filename with extension "
              ".gtf."))

    args = parser.parse_args()

    # create gtf
    tsv2gtf(file_name=args.tsv_file, prefix=args.prefix, cryp=args.cryp,
        gtf_name=args.output_gtf)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
