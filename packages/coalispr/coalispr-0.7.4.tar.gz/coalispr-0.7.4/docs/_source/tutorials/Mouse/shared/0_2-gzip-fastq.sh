#!/bin/bash
DATA=${DATA-SRR64428[3-4][0-8]*}

for i in $DATA
  do
    FQZ=$(ls ${i}/ | grep -c 'fastq.gz')
    FQ=$(ls ${i}/ | grep -c 'fastq')
    echo "Processing ${i}"
    if (( ${FQZ} > 0 )); then
        echo "Found $FQ gzipped fastq file(s), skipping.."
      continue
    elif (( ${FQZ} == 0 && ${FQ} > 0 )); then
      echo "GZipping ${FQ} fastq file(s)";
      find ./${i}/ -name "*.fastq" -exec  gzip "{}" +
    else
      echo "Found ${FQ} .fastq(.gz) file(s), skipping.."
      continue
    fi
  done
