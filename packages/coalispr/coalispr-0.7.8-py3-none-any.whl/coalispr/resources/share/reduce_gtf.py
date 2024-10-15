#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  reduce_gtf.py
#
#
#  Copyright 2023 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Script for reducing gtf files."""
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from datetime import datetime
from pathlib import Path

def reduce_gtf(infile, outname=None, genbank=False):
    """Omit lines with CDS and start or stop codons from GTF:

    Parameters
    ----------
    infile : str
        Name of gtf file in current directory (where this script resides; has
        been copied to) to be converted
    outname : str
        Name of gtf file created in current directory.
    """
    inpath = Path(__file__).parent.joinpath(infile)
    outpath = Path(__file__).parent.joinpath(outname)
    outpath = inpath.with_stem(f"{inpath.stem}_")
    droppath = inpath.with_stem(f"{inpath.stem}_out")
    try:
        with outpath.open("w") as fileout:
            with droppath.open("w") as dropout:
                with inpath.open('r') as filein:
                    for line in filein:
                        if not line.strip(): #empty line
                            continue
                        elif line.startswith('#'): #comments
                            fileout.write(line)
                        elif 'CDS' in line or '_codon' in line:
                           dropout.write(line)
                        elif genbank and 'GenBank' in line:
                           dropout.write(line)
                        else:
                           fileout.write(line)
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
        help=("gtf file to reduce"))
    optional.add_argument('-o','--out', type=str,
        default="",
        help="name for output file.")
    optional.add_argument('-g','--genbank', type=bool,
        default=False,
        help="Remove lines with GenBank (as source)")
    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')

    args = parser.parse_args()
    #print(args)
    reduce_gtf(infile=args.infile, outname=args.out, genbank=args.genbank)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
