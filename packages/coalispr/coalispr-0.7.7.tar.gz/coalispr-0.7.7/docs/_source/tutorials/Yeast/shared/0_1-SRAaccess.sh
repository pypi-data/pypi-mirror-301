#! /bin/bash
# https://github.com/ncbi/sra-tools/wiki/08.-prefetch-and-fasterq-dump
# https://github.com/ncbi/sra-tools/wiki/HowTo:-fasterq-dump
DATA=${DATA:-SRR[1-4][0-4][0-5]*}

for i in $DATA
  do
    echo "Processing ${i} .."
    FQ=$(ls ${i}/ | grep -c 'fastq')
    if (( ${FQ}!=0 )); then
      echo "Found ${FQ} (gzipped) fastq file(s), skipping.."
      continue
    fi
    #cd "$i" || exit
    fasterq-dump --split-files "${i}" --outdir "./${i}" -p
    #cd ..
  done
