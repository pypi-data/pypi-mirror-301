#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sub_gtf.py
#
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""
Script to extract lines from general annotation file for a particular property,
outputting a 'sub'-gtf. Python alternative for below bash script.

.. code-block:: sh

    #! /bin/bash
    inputgz=$1

    if [[ -z $inputgz ]]; then
      echo "Please, provide compressed annotations file (.gtf.gz) as input"
      exit
    fi

    # collect entries for common ncRNAs
    gunzip -cf $inputgz | grep snRNA > tmp
    gunzip -cf $inputgz | grep snoRNA >> tmp
    gunzip -cf $inputgz | grep tRNA >> tmp
    gunzip -cf $inputgz | grep rRNA >> tmp
    sort -k 1.4h,1 -k 4n,4 -k 5nr,5 tmp > mouse_ncRNAs.gtf
    rm tmp
"""
import gzip
import re
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from datetime import datetime
from pathlib import Path
from coalispr.resources.constant import (
    GTFEXON, GTFFEAT,
    )



def create_gtf(kind, get_all, reference, features):
    """Create a kind of GTF file by extracting features from reference gtf.

    Parameters
    ----------
    kind      : str
        Kind of feature for which a GTF is made. Used as output name.
    reference : str
        Filename for annotation reference
    features  : str
        List of features to extract annotations for, recoverable from string.

    Returns
    -------
    GTF file
        An annotation with the following fields:

        ::

            seqname  - The name of the sequence. Must be a chromosome or
                     scaffold.
            source   - The program that generated this feature.
            feature  - The name of this type of feature. Some examples of
                     standard feature types are "CDS", "start_codon",
                     "stop_codon", and "exon".
            start    - The starting position of the feature in the
                     sequence. The first base is numbered 1.
            end      - The ending position of the feature (inclusive).
            score    - A score between 0 and 1000. If the track line
                     useScore attribute is set to 1 for this annotation
                     data set, the score value will determine the level
                     of gray in which this feature is displayed (higher
                     numbers = darker gray). If there is no score value,
                     enter ".".
            strand   - Valid entries include '+', '-', or '.' (for don't
                     know/don't care).
            frame    - If the feature is a coding exon, frame should be a
                     number between 0-2 that represents the reading
                     frame of the first base. If the feature is not a
                     coding exon, the value should be '.'.
            comments - gene_id "Em:U62317.C22.6.mRNA"; transcript_id
                     "Em:U62317.C22.6.mRNA"; exon_number 1
    """

    refpath = Path(__file__).parent.joinpath(reference)
    outpath = Path(__file__).parent.joinpath(f"{kind}.gtf")
    if not refpath.suffixes in [ ['.gtf', '.gz'], ['.GTF', 'gz'] ]:
        msg = (f"Please choose a compressed gtf reference file for {reference}")
        raise SystemExit(msg)

    def can_skip(genid):
        # only collect info what can be displayed
        feature = genid[0].split('\t')[2].strip()
        if not get_all:
            return feature not in [GTFEXON, GTFFEAT]

    def re_id(gtfline, akind):
        delim = '\tgene_id "'
        genid = gtfline.strip().split(delim)
        if can_skip(genid):
            return ''
        gentyp = genid[1].split('gene_type "')[1].split('"; ', 1)[0]
        gennam = genid[1].split('gene_name "')[1].split('"; ', 1)[0]
        is_akind = akind in gentyp or akind in gennam
        use_gentyp = f"{gentyp}_" if gentyp != misc else ''
        to_add = f"{use_gentyp}{gennam}_" if is_akind else ''
        featureline = f"{genid[0]}{delim}{to_add}{genid[1]}\n"
        return featureline

    #features-argument will be seen as one string, never as a list
    features_ = re.split(r',|;|-',features.strip())
    miscfeatures_= []
    for item in features_: #weird resolution when all separators are ','
        #print(item)
        if item.startswith('misc'):
            miscfeatures_.append(item.split('misc')[1])
            features_.remove(item)
    misc = "misc_RNA"

    print(f"Selecting {', '.join(features_)} and {misc}s: "
        f"{', '.join(miscfeatures_)}.")

    gtf = (f"##gff-version 2\n# created by {Path(__file__).name} on "
          f"{datetime.now().strftime('%d-%m-%Y')}\n#\n#\n")
    try:
        with outpath.open('w') as fileout:
            fileout.write(gtf)
            with gzip.open(refpath, 'rb') as refs:
                for byteline in refs:
                    strline = byteline.decode("utf-8")
                    akindline = ''
                    if not strline.strip(): #empty line
                        continue
                    elif strline.startswith('#'): #comments
                        fileout.write(strline)
                    elif misc in strline:
                        for rna in miscfeatures_:
                            if rna in strline:
                                akindline = re_id(strline, rna)
                            if not akindline:
                                continue
                            fileout.write(akindline)
                            break
                    else:
                        for akind in features_:
                            if akind in strline:
                                akindline = re_id(strline, akind)
                            if not akindline:
                                continue
                            fileout.write(akindline)
                            break
                    if not akindline:
                        continue

    except FileNotFoundError as e:
        msg = (f"Please check error message:\n\t '{e}'. \n   Expected is a "
            f"file like '{reference}'")
        raise SystemExit(msg)




def main(args):
    descrip = ("Extract subset of gtf")
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-k','--kind', type=str, required=True,
        dest='kind',
        help=("kind of feature for output (name) gtf file"))
    optional.add_argument('-a','--all', type=int, required=False,
        dest='all', choices=[0,1], default=0,
        help=("return all linked features or only ones that can be shown by "
        "``coalispr showgraphs`` like 'exon'? 0: minimal, 1: all."))
    required.add_argument('-g','--gtf', type=str, required=True,
        dest='reference',
        help=("provide compressed reference file (.gtf.gz)"))
    optional.add_argument('-l','--list', type=str, required=False,
        dest='featurelist',
        default=("snRNA,snoRNA,tRNA,rRNA,scaRNA;misc7SK,miscSRP,miscGm,"
            "Y_RNA,pseudogene"),
        help=("list of features to extract; separate by ',',';' or '-'; no"
            "space(s) or '_'!"))
    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')

    args = parser.parse_args()
    #print(args)
    create_gtf(kind=args.kind, get_all=args.all, reference=args.reference,
        features=args.featurelist)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
