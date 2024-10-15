#!/bin/bash

#USE=cutadapt
USE=flexbar

DATA=${DATA:-SRR[68][46][69]*}


for i in $DATA
  do
    echo "Processing ${i} .."
    if [[ -s ${i}/${i}-collapsed.fasta ]]; then
      echo "Skipped; found collapsed data file: ${i}-collapsed.fasta."
      #mv "${i}/${i}-collapsed.fasta" "${i}/${i}-collapsed_0.fasta"
      continue
    fi
    if [[ $USE == "flexbar" ]]; then
      gunzip -c "${i}/${i}-trimmed.fastq.gz" | \
      pyFastqDuplicateRemover.py -o "${i}/${i}-collapsed.fasta"
    elif [[ $USE == "cutadapt" ]]; then
      gunzip -c "${i}/${i}-out.fastq.gz" | \
      pyFastqDuplicateRemover.py -o "${i}/${i}-collapsed.fasta"
    fi
  done
