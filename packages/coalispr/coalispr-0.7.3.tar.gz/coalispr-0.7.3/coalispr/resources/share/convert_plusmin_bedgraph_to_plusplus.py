#!/usr/bin/env python3
#
#  convert_plusmin_bedgraph_to_plusplus.py
#
#  Copyright 2024 Rob van Nues <sborg63@disroot.org>
#
#
#  "Licensed under the EUPL-1.2 or later"
#
#


import sys

from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from pathlib import Path
import pandas as pd




def bgconvert_file(infile, delim, header):
    """Bedgraph converter that splits ENSEMBL-bedgraphs with +/- values, see
    https://www.ensembl.org/info/website/upload/bed.html#bedGraph
    into stranded bedgraph files as is the output by STAR or PyCRAC

    track type=bedGraph name="BedGraph Format" description="BedGraph format" priority=20
    chr1 59302000 59302300 -1.0
    chr1 59302300 59302600 -0.75
    chr1 59302600 59302900 -0.50
    chr1 59302900 59303200 -0.25
    chr1 59303200 59303500 0.0
    chr1 59303500 59303800 0.25
    chr1 59303800 59304100 0.50
    chr1 59304100 59304400 0.75
    """
    pfile = Path(infile)
    if pfile.suffix.lower() not in [".bedgraph", ".bg"]:
        raise SystemExit(f"Extension '{pfile.suffix}' not recognized.")

    sepin = { 1: r'\s+', 2: ',', 3: '\t'}[delim]
    skipin = [ n for n in range(header)]
    inframe = pd.read_csv(pfile, sep=sepin, skiprows=skipin, header=None)

    pfileplus = Path(f"{pfile.stem}_plus.bedgraph")
    plusframe = inframe[inframe[3] >= 0]
    plusframe.to_csv(pfileplus, sep="\t", header=False)

    pfileminus = Path(f"{pfile.stem}_minus.bedgraph")
    minframe = inframe[inframe[3] < 0 ]
    minframe.loc[:,3] = minframe.loc[:,3].abs()
    minframe.to_csv(pfileminus, sep="\t", header=False)

def main(args):
    descrip = ("Split single plus-minus bedgraph into stranded bedgraph files")
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-f','--file', type=str, required=True,
        help="Input file with extension '.bedgraph', or '.bg'.")

    optional.add_argument('-d','--delimiter', type=int, choices=[1,2,3],
        default=1,
        help=("Give number for the type of column delimiter in bedgraph file: "
        "1: space; 2: comma; 3: tab "))
    optional.add_argument('-t','--typeheader', type=int,
        choices=[0,1,2,3,4,5,6,7,8,9], default=1,
        help=("Give number of lines that form header of file. 0: no header, "
        "1: 'track type=bedGraph ..' only; 2: two lines, 3: etc."))

    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')

    args = parser.parse_args()

    bgconvert_file(args.file, args.delimiter, args.typeheader)

    return 0



if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
