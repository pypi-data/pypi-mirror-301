#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  no_empty_fa.py
#
#
#  Copyright 2022 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""
Below set of shell commands work on a small file but which uses too much RAM
in the case of a very long file with sequencing data in fastq.

.. code-block:: sh

    #for i in SRR644*; do
    #  echo "Processing ${i} .."
    #    infile="${i}/${i}"
    #    declare -a LINNUM
    #    # Gather line numbers for empty reads in reverse order to allow for sequential deletion
    #    # Line  numbers begin with @:
    #    # @SN7001365:465:H5KKCBCX2:1:1107:3039:1981 1:N:0:ANCACG
    #    LINNUM+=($(gunzip -c ${infile}.fastq.gz | grep -nB 1 '^ *$' | grep '@'| cut -d '-' -f 1 | sort -nr ))
    #    gunzip -c ${infile}.fastq.gz > tmp
    #    for lino in "${LINNUM[@]}"; do
    #      #echo "Line number $lino will be deleted"
    #      range="${lino}, $((lino +3))"
    #      sed -i "$range d" tmp;
    #    done
    #    cp tmp ${infile}-uncollapsed.fastq
    #    gzip ${infile}-uncollapsed.fastq
    #    rm tmp
    #done

For fasta files it is easier, and the files are smaller: all empty reads are
collapsed into one.

.. code-block:: sh

    #for i in SRR644*; do
    #  echo "Processing ${i} .."
    #    infile="${i}/${i}"
    #    gunzip -c ${infile}.fastq.gz | pyFastqDuplicateRemover.py -o tmp.fasta
    #    # there will be only one unique fasta read without any length; find its name
    #    LINNAM=$(grep -B1 '^ *$' tmp.fasta)
    #    # use double quote to expand variable in sed command
    #    sed "/$LINNAM/,+1 d" tmp.fasta > ${infile}-collapsed.fasta
    #    rm tmp.fasta
    #done

This python script covers both kind of sequencing files; it directly copies the
non-empty sequences (in fasta or fastq format) to a new file without a need to
store the information into RAM for filtering and sorting.
"""
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from itertools import islice
from pathlib import Path



def clean_file(infile):
    """Take out empty sequences left after adapter removal.

    Parameters
    ----------
    infile : str
       Filename of fasta file to be corrected
    """
    path = Path(infile)
    if not path.suffix in ['.fasta', '.fa', '.fastq']:
        msg = ("Please choose a file with extension '.fastq', '.fasta', "
            + "or '.fa'.")
        raise SystemExit(msg)

    outpath = path.with_stem(f"{path.stem}_ok")

    with outpath.open("w") as fileout:
        with path.open("r") as filein:
            if path.suffix in ['.fa', '.fasta']:
                #titlestart='>'
                slicestep = 2
            elif path.suffix in ['.fastq']:
                #titlestart='@'
                slicestep = 4
            while True:
                # islice returns an iterator, get the contents as list
                lines = list(islice(filein, slicestep))
                if lines :
                    if not lines[1].strip(): #empty line
                        continue
                    else:
                        for line in lines:
                            fileout.write(line)
                else:
                    break


def main(args):# Disable default help
    descrip = ("Filter empty sequence lines from fast[a|q] file -f")
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')
    required.add_argument('-f','--file', type=str, required=True,
        help="required input file with extension '.fastq', '.fasta' or '.fa'.")

    args = parser.parse_args()

    clean_file(args.file)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
