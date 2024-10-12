#!/bin/bash
# Uses pyCRAC script pyCalculateChromosomeLengths.py
inputfasta=$1

if [[ -z "$inputfasta" ]]; then
  echo "Please, provide input fasta"
  exit
fi

# Get fasta-names with lengths; store
pyCalculateChromosomeLengths.py -f "$inputfasta"  > 2coltabcol.txt
# Get first section of name (to first space), store as column 1
cut -d ' ' -f1 2coltabcol.txt > 1col.txt
# Get last section, the lengths, after the tab; store as column 2
cut -f2 2coltabcol.txt > 2col.txt
# Fuse columns
paste 1col.txt 2col.txt > "${inputfasta//./_}-chrlengths.tsv"
# Clean up
rm 2coltabcol.txt 1col.txt 2col.txt
