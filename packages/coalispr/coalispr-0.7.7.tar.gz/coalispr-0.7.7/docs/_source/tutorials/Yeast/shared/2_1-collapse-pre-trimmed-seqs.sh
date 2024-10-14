#!/bin/bash
if [[ -z $1 ]]; then
  echo -e "No SRR accession given; aligning hardcoded GEO numbers.."
  DATA=${DATA:-SRR[1-4][0-4][0-5][4-7]*}
  # Found still many 3'linker (AppPE) in Unmapped.out.mate12;
  # removed these with 2_1_0-flexbar-trim.sh
  TRIM="-trim35"
elif [[ -s $1 ]]; then
  echo "SRR accession given; aligning ${*}.."
  DATA=${DATA:-$*}
  TRIM=""
fi

USE="PE"

j=1
k=2

for i in $DATA
  do
    if [[ $USE == "PE" ]]; then
      echo "Processing ${USE} data for ${i} .."

      cd "${i}" || exit
      gunzip -c "${i}${TRIM}_${j}.fastq.gz" > read1
      gunzip -c "${i}${TRIM}_${k}.fastq.gz" > read2
      pyFastqDuplicateRemover.py -f read1 -r read2 -o "${i}-collapsed"
      rm read1 read2
      cd ..
    fi
  done

#@SN7001365:465:H5KKCBCX2:1:1107:3039:1981 1:N:0:ANCACG
