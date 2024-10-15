#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  get_smallRNAs_and_targets.py
#
#
#  Copyright 2022 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Scripts for collecting small RNA info and putative targets from input."""
import gzip
import pandas as pd
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from datetime import datetime
from pathlib import Path
from coalispr.resources.constant import (
    GTFEXON, GTFFEAT,
    )

def _get_match(infile, namelibrary):
    """ Replaces bash script:

    .. code-block:: sh

        REF=$(gunzip -k gene2ensembl.gz)
        INFILE=$(gunzip -k $infile )
        grep 'mmu' $INFILE | cut -f 2 | sort | uniq >> tmp
        MMTARG=$(grep 'mmu' $INFILE | cut -f 2 | sort | uniq)
        ## next step hangs
        #for i in $MMTARG[@]; do
        #  grep $i gene2ensembl | cut -f 3 >> tmp2;
        #done
    """
    INFILEX = 'miRDB.gz'
    LIBEX = 'gene2ensembl.gz'
    inpath = Path(__file__).parent.joinpath(infile)
    # first column of miRBD file with targets has names for miRNAs beginning
    # an abbreviation of the species, for mouse:
    mmu = 'mmu'
    libpath = Path(__file__).parent.joinpath(namelibrary)
    # target name is like ENSMUSG00000059796 in gene2ensembl column [2]
    # input name is like NM_144958.4 in gene2ensembl column [3]
    # but lacks .4 version number in search label of gene2ensembl column [2]
    sortcol = "RNA_nucleotide_accession.version"
    searchcol = "RNA_nucleotide_accession"
    genid = "GeneID"
    # tax id = 10090 gene2ensembl column [0]
    taxid = 10090
    getcol = 'Ensembl_gene_identifier'
    stargets = []
    match = []

    if libpath.suffix != '.gz' or inpath.suffix != '.gz':
        raise SystemExit("Compressed input files expected!")

    try:
        with gzip.open(inpath, 'rb') as targs:
            dftargets = pd.read_csv(targs, sep='\t', usecols=[0,1], header=None,
                index_col=0).sort_index()
            hasmmu = dftargets.index.str.startswith(mmu)
            stargets = dftargets[hasmmu].iloc[:,0].sort_values(
                ignore_index=True).to_list()

        with gzip.open(libpath, 'rb') as ensem:
            dfensembl = pd.read_csv(ensem, sep='\t',na_values='-', index_col=0
                ).loc[taxid].sort_values(by=[sortcol]).drop([genid], axis=1)
            dfensembl[searchcol] = dfensembl[sortcol].str.rsplit(pat='.', n=1
                ).str.get(0)
            dfensembl = dfensembl.drop_duplicates(subset=[sortcol])
            dfensembl = dfensembl.dropna(subset =[sortcol]).set_index(
                searchcol, drop=True)
            #print(dfensembl[getcol]) #Length: 43106
            matchidx = dfensembl.index.intersection(stargets)
            #print(matchidx) #length=24531
            dfmatch = dfensembl.loc[matchidx][getcol]
            #dfmatch.to_csv('miRNA-targets.txt',index=False, columns=[getcol],
            #   header=False)
            match = dfmatch.to_list()
        return match
    except FileNotFoundError as e:
        msg = (f"Please check error message:\n\t '{e}'. \n   Expected are files"
            f" like '{INFILEX}' or '{LIBEX}'")
        raise SystemExit(msg)


def _create_gtfs_from(akind, get_all, idlist, areference, outname):
    """Use ids in idlist to find reference lines for akind output"""
    if not isinstance(idlist, list):
        raise SystemExit("create_gtf_from() failed on wrong input (not a list)")
    # lines with akind of RNA and its putative targets based on idlist are
    # combined into one file
    outkind = Path(__file__).parent.joinpath(f"{akind}s.gtf")
    outpath = Path(__file__).parent.joinpath(outname).with_suffix('.gtf')
    refpath = Path(__file__).parent.joinpath(areference)
    delim = '\tgene_id "'
    gtf = (f"##gff-version 2\n# created by {Path(__file__).name} on "
          f"{datetime.now().strftime('%d-%m-%Y')}\n")
    gtfadd0 = f"# for {akind} molecules. "
    gtfadd1 = f"# for {len(idlist)} putative targets of {akind}s."

    if ','.join(refpath.suffixes).lower().split(',') != ['.gtf', '.gz']:
        raise SystemExit("Compressed reference file (.gtf.gz) expected!")

    def can_skip(genid):
        # only collect info what can be displayed
        feature = genid[0].split('\t')[2].strip()
        if not get_all:
            return feature not in [GTFEXON, GTFFEAT]

    def re_id(gtfline, is_target=False):
        genid = gtfline.strip().split(delim)
        if can_skip(genid):
            return ''
        gentyp = genid[1].split('gene_type "')[1].split('"; ', 1)[0]
        gennam = genid[1].split('gene_name "')[1].split('"; ', 1)[0]
        is_akind = not is_target and (akind in gentyp or akind in gennam)
        to_add = f"{gentyp}_{gennam}_" if is_akind else f"{gennam}_"
        featureline = f"{genid[0]}{delim}{to_add}{genid[1]}\n"
        return featureline

    print("Building gtfs ..")

    try:
        with outpath.open("w") as fileout:
            with outkind.open("w") as kindout:
                kindout.write(f"{gtf}{gtfadd0}\n#\n") #miRNA
                fileout.write(f"{gtf}{gtfadd1}\n#\n") #targets
                # refpath is expected to be compressed
                with gzip.open(refpath, 'rb') as filein:
                    for byteline in filein:
                        strline = byteline.decode("utf-8")
                        ## otherwise add 'b' preceding text because of bytes loaded
                        if not strline.strip(): #empty line
                            continue
                        elif strline.startswith('#'): #comments
                            fileout.write(strline)
                            kindout.write(strline)
                        elif akind in strline: #the RNAs themselves
                            rna_line = re_id(strline)
                            kindout.write(rna_line)
                        else:
                            # get their targets:
                            # split on common phrase preceding gene_id.
                            # second chunk could start with name in ids
                            # stop at '.' before version no
                            genid = strline.split(delim)
                            nam = genid[1].split('.')[0]
                            if not nam in idlist:
                                continue
                            # only collect info what can be displayed
                            if can_skip(genid):
                                continue
                            trg_line = re_id(strline, True)
                            fileout.write(trg_line)
    except FileNotFoundError as e:
        msg = (f"Please check error message:\n\t '{e}'. \n   Expected is "
            f"input like '{areference}'")
        raise SystemExit(msg)




def create_gtfs(kind, get_all, targets, library, reference, outname):
    """Create a GTF file for kind of RNA from infile, using reference if needed

    Parameters
    ----------
    kind      : str
        Kind of RNA the GTF is made for, like 'miRNA'.
    get_all   : int
        Flag to indicate to get 0: minimal (i.e. only displayed by
        ``coalispr showgraphs``) or 1: all annotations for a feature
    targets : str
        Name for input file with ids for genes to be annotated
    library : str
        Name for file with info for gene ID conversions
    reference : str
        Name for gtf with all genome annotations to be mined as reference
    otname : str
        Name for output file

    Returns
    -------
    GTF file

        An annotation file with the following fields:

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
    path = Path(__file__).parent.joinpath(targets)
    if not path: #.suffix in ['.gtf', 'GTF', ]:
        msg = ("Please choose a targets file")
        raise SystemExit(msg)

    #if kind in ["targets", "t", "-t"]:
    ids = _get_match(targets, library)
    print(f"Found {len(ids)} target gene-names.")
    _create_gtfs_from(kind, get_all, ids, reference, outname)
    #elif kind in ["miRNAs", "m", "-m"]:
    #   convert_gff3(infile)
    #else:
    #    raise SystemExit(f"Kind ('-k') '{kind}' not found")




def main(args):
    # Disable default help
    descrip = ("Get useful gene ids")
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-k','--kind', type=str, required=True,
        dest='kind', choices=["m","miRNA", "s", "siRNA"],
        help=("required kind of feature to create gtf for"))
    optional.add_argument('-a','--all', type=int, required=False,
        dest='all', choices=[0,1], default=0,
        help=("return all linked features or only ones that can be shown by "
        "``coalispr showgraphs`` like 'exon'? 0: minimal, 1: all."))
    required.add_argument('-t','--targets', type=str, required=True,
        help="required, compressed file with putative targets as input.")
    required.add_argument('-l','--library', type=str, required=True,
        help="required, compressed library file for conversion IDs as input.")
    required.add_argument('-g','--gtf', type=str, required=True,
        dest='reference',
        help=("provide compressed reference file (.gtf.gz)"))
    required.add_argument('-o','--out', type=str, required=True,
        dest='outname',
        help=("provide name output file (.gtf)"))
    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')

    args = parser.parse_args()
    #print(args)
    create_gtfs(kind=args.kind, get_all=args.all, targets=args.targets,
        library=args.library, reference=args.reference, outname=args.outname)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
