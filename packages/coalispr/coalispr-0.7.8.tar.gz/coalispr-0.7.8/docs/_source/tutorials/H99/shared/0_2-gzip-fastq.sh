#!/bin/bash

DATA=${DATA:-SRR[68][46][69]*}

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
