#!/bin/bash
# number of threads
n=4

DATA1=${DATA1:-SRR8697*}
ADAP1="TGGAATTCTCGGGTGCC"
QUAL1=i1.8

DATA2=${DATA2:-SRR64663*}
ADAP2="TCGTATGCCGTCTTCTGC"
QUAL2=solexa

FB=FlexbarLogs
if [[ ! -d $FB ]] ; then mkdir $FB; fi

for i in $DATA1
  do
    echo "Processing ${i} .."
    if [[ -f "$i/$i-trimmed.fastq.gz" ]]; then
      echo "Found ${i}-trimmed.fastq.gz, skipping ..";
      continue
    fi
    flexbar \
      -r "${i}/${i}.fastq.gz" \
      -qf $QUAL1 \
      -t "${i}/${i}-trimmed" \
      -as $ADAP1 \
      -z  GZ -n  10 -ao 6 -m 12 -n "$n"
    mv "${i}/${i}-trimmed.log" $FB/
  done

for i in $DATA2
  do
    echo "Processing ${i} .."
    if [[ -f "$i/$i-trimmed.fastq.gz" ]]; then
      echo "Found ${i}-trimmed.fastq.gz, skipping ..";
      continue
    fi
    flexbar \
      -r "${i}/${i}.fastq.gz" \
      -qf $QUAL2 \
      -t "${i}/${i}-trimmed" \
      -as $ADAP2 \
      -z  GZ -n  10 -ao 6 -m 12 -n "$n"
    mv "${i}/${i}-trimmed.log" $FB/
  done

#--pre-trim-phred 30

# nebnext adapter      AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
# standard SE adapter: TGGAATTCTCGGGTGCCAAGGC
# Minimum quality as threshold for trimming was the Default: 20.
