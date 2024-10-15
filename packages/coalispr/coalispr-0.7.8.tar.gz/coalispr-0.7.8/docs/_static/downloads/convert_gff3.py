#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  convert_gff3.py
#
#
#  Copyright 2022 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Script for converting gff to gtf files."""
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from datetime import datetime
from pathlib import Path

def convert_gff(infile, delim=None, outname="miRNAs.gtf"):
    """Get gtf2 from gff3, which has different annotation, lacking 'gene_id':

    ``chr1\t.\tmiRNA\tprimary_transcript\t12425986\t12426106\t.\t+\t.\tID=MI0021869;Alias=MI0021869;Name=mmu-mir-6341``

    replace ``ID=`` section with ``gene_id "``.

    Parameters
    ----------
    infile : str
        Name of gff3 file in current directory (where this script resides; has
        been copied to) to be converted to gff2/gtf
    delim : str
        Substring that forms a unique split point sothat given ID forms start of
        second fragment created.
    outname : str
        Name of gtf file created in current directory.
    """
    inpath = Path(__file__).parent.joinpath(infile)
    outpath = Path(__file__).parent.joinpath(outname)
    outpath = outpath.with_stem(f"{outpath.stem}_{inpath.stem}")
    sub = '\tID=' if not delim else delim
    ingff = '##gff-version 3'
    outgff = '##gff-was-version 3'
    gtfid = '\tgene_id "'
    gtf = (f"##gff-version 2\n# created by {Path(__file__).name} on "
          f"{datetime.now().strftime('%d-%m-%Y')}\n# based on {infile}\n#\n")

    try:
        with outpath.open("w") as fileout:
            fileout.write(gtf)
            with inpath.open('r') as filein:
                for line in filein:
                    if not line.strip(): #empty line
                        continue
                    elif line.startswith(ingff):
                        fileout.write(line.replace(ingff, outgff))
                    elif line.startswith('#'): #comments
                        fileout.write(line)
                    # split on common phrase preceding ID.
                    # second chunk needs to be split
                    else:
                        annot = line.strip().split(sub)
                        newannot = annot[1].replace(';', '"; ')
                        newannot = newannot.replace('=', ' "')
                        gtfline = f'{annot[0]}{gtfid}{newannot}";\n'
                        fileout.write(gtfline)
                        continue
    except FileNotFoundError as e:
        msg = (f"Please check error message:\n\t '{e}'. \n   Expected is a "
            f"file like '{infile}'")
        raise SystemExit(msg)


def main(args):
    # Disable default help
    descrip = ("Get useful gene ids")
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-f','--file', type=str, required=True,
        dest='infile',
        help=("gff3 file to create gtf from"))
    optional.add_argument('-d','--delim', type=str,
        default="\tID=",
        help="delimiter to expose start of gene ID")
    optional.add_argument('-o','--out', type=str,
        default="miRNAs.gtf",
        help="name for output file.")
    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')

    args = parser.parse_args()
    #print(args)
    convert_gff(infile=args.infile, delim=args.delim, outname=args.out)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
