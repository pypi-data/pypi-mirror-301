#!/bin/bash
REF=$1

for i in $REF
  do
    echo "Processing $i .."
    cd "$i"|| exit
    fasterq-dump --split-files "$i".sra
    cd ..
  done
