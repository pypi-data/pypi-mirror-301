#!/bin/bash

USE=cutadapt
#USE=flexbar

DATA=${DATA:-SRR64428*}

for i in $DATA
  do
  echo "Processing ${i} .."
    if [[ "$USE" == "cutadapt" ]]; then
      # input files lack adapters but still contain zero-length fasta sequences STAR doesn't like
      cd "${i}" || exit
  #    infile="test"
      infile="${i}"
      gunzip -c "${infile}".fastq.gz | pyFastqDuplicateRemover.py -o tmp.fasta
      python3 ../no_empty_fa.py -f tmp.fasta #output = tmp_ok.fasta
      mv tmp_ok.fasta "${infile}-collapsed.fasta"
      rm tmp.fasta
      cd ..
    fi
  #  if [[ $USE == "flexbar" ]]; then
  #       gunzip -c "${i}/${i}.fastq.gz" | pyFastqDuplicateRemover.py -o "${i}/${i}-collapsed.fasta"
  #  fi
  done

#@SN7001365:465:H5KKCBCX2:1:1107:3039:1981 1:N:0:ANCACG
