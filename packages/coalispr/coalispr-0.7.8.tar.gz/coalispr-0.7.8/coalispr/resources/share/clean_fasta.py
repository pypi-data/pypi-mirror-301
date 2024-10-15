#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  clean_fasta.py
#
#  Copyright 2021-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Script to minimize chromosome names in fasta files."""
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from pathlib import Path

def clean_fasta(infile, tag, outname):
    """Simplify chromosome naming to initial number/symbol

    Parameters
    ----------

    infile : str
        path to fasta file with redundant/long/confusing sequence titles.
    tag : str
        Filename-addition (default: '_chr') marking the output fasta file (when
        outname is not given).
    outname
        Name of resulting fasta file to save.

    Returns
    -------
        Fasta file with <outname> or name of <infile> plus <_tag>.

    """

    path = Path(infile)
    if not path.suffix.lower() in ['.fasta', '.fa']:
        msg = "Please choose a file with extension '.fasta' or '.fa'."
        raise SystemExit(msg)

    outfilename = f"{path.stem}_{tag}"

    chroms = ['0','1','2','3','4','5','6','7','8','9']
    if not outname:
        outpath = Path(infile).with_stem(outfilename).with_suffix('.fasta')
    elif outname and Path(outname).suffix != '.fasta':
        outpath = Path(outname).with_suffix('.fasta')
    else:
        outpath = Path(outname)
    print(path, outname)
    with outpath.open("w") as fileout:
        with path.open("r") as filein:
            for line in filein :
                if line.startswith("#"):
                    continue
                #>1 dna_sm:chromosome chromosome:CNA3:1:1:2291499:1 REF
                #>CM008076.1 Cryptococcus neoformans var. neoformans XL280 chromosome 4, whole genome shotgun sequence
                #>1 dna_sm:chromosome chromosome:ASM9104v1:1:1:2300533:1 REF
                if line.startswith(">"):
                    line = line.strip().split(" ")
                    if line[0][1] in chroms:
                        fileout.write(line[0]+"\n")
                    else:
                        i = 0
                        j = 1
                        while j < len(line):
                            if 'chr' in line[i].lower() and line[j][0] in chroms:
                                chr_=''
                                for lett in line[j]:
                                    if lett in chroms:
                                        chr_ += lett
                                fileout.write(f">{chr_}\n")
                                break
                            i += 1
                            j += 1
                else :
                    fileout.write(line)


def main():
    descrip = ("Clean up fasta header to number for each chromosome in fasta "
          "file -f and save output with tag -t or as fasta file -o")
    # Disable default help
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')
    required.add_argument('-f','--fasta_file', type=str, required=True,
        help="required input file with extension '.fasta' or '.fa'.")
    optional.add_argument('-t','--tag', type=str, default='chr',
        help=("resulting fasta file is saved as input extended with '_<tag>', "
              "default tag is 'chr'."))
    optional.add_argument('-o','--output_fasta', type=str, default=None,
        help="name of resulting fasta file to save")

    args = parser.parse_args()

    clean_fasta(args.fasta_file, args.tag, args.output_fasta)


if __name__ == '__main__':
    main()
