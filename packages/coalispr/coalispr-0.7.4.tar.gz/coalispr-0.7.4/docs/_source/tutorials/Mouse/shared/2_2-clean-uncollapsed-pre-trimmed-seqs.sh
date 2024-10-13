#!/bin/bash

#USE=cutadapt
#USE=flexbar
DATA=${DATA:-SRR64428*}

for i in $DATA
  do
    echo "Processing ${i} .."
  #   if [[ -f "${i}/${i}-collapsed.fasta" ]]; then
  #       mv "${i}/${i}-collapsed.fasta" "${i}/${i}-collapsed_0.fasta"
  #   fi
  #   if [[ "$USE" == "cutadapt" ]]; then
  #       gunzip -c "${i}/${i}-out.fastq.gz" | pyFastqDuplicateRemover.py -o "${i}/${i}-collapsed.fasta"
  #   fi
  #   if [[ "$USE" == "flexbar" ]]; then
    cd "${i}" || exit
    infile="${i}"
    gunzip -c "${infile}.fastq.gz" > tmp.fastq
    python3 ../no_empty_fa.py -f tmp.fastq # output = tmp_ok.fastq
    mv tmp_ok.fastq "${infile}-uncollapsed.fastq"
    gzip -f "${infile}-uncollapsed.fastq"
    rm tmp.fastq
    cd ..
    #fi
  done
