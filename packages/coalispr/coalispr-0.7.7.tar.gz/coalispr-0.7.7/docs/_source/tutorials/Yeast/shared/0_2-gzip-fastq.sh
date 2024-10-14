#!/bin/bash

if [[ -z $1 ]]; then
  echo -e "No SRR accession given; aligning hardcoded GEO numbers.."
  DATA=${DATA:-SRR[1-4][0-4][0-5][4-7]*}
elif [[ -s $1 ]]; then
  echo "SRR accession given; aligning ${*}.."
  DATA=${DATA: $*}
fi

for i in $DATA
  do
  echo -e "\nProcessing $i";
  for j in 1 2;
    do
    #echo "$j";
    if [[ -f "${i}/${i}_${j}.fastq" ]]; then
      echo "GZipping ${i}_${j}.fastq";
      gzip "${i}/${i}_${j}.fastq";
    elif [[ -f "${i}/${i}_${j}.fastq.gz" ]]; then
      echo "${i}_${j}.fastq.gz found; nothing to do ..";
    fi
    done
  done
