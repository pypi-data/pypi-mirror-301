#!/bin/bash
# Requires the programmes fastqc and rseqc.
# Run from a folder within a normal work-directory
SRCDIR=$(pwd)/../
#echo "$SRCDIR"
DATA=${DATA:-SRR[6-8][4-6][6-9][6-7][3-6][0-9]*}

FQC="$SRCDIR/fastqc_settings/"
settings="${FQC}fastqc_limits_collapsed.txt"
#adapters="${FQC}fastqc_adapters.txt"
unplacable="${FQC}fastqc_contaminants.txt"
TARG=$1

for i in $DATA
  do
    echo "generating reports for ${i}"
    cd "${i}" || exit
    #if [[ -s "${i}_bam_stat.out" ]]; then
    #     mv "${i}_bam_stat.out" "${i}_bam_stat0.out"
    #fi
    if [[ -s samtoolsAligned.sortedByCoord.out.bam ]]; then
      bam_stat.py -i samtoolsAligned.sortedByCoord.out.bam > "${i}_bam_stat.out"
       # samtools view -H samtoolsAligned.sortedByCoord.out.bam > 1mismatched.sam ;
       # samtools view samtoolsAligned.sortedByCoord.out.bam | grep 'nM:i:1'>> 1mismatched.sam
       # samtools view -b 1mismatched.sam -o 1mismatched.bam
       # rm 1mismatched.sam
      unset _JAVA_OPTIONS
      fastqc samtoolsAligned.sortedByCoord.out.bam \
        --noextract -l "$settings" \
        --contaminants "$unplacable" ;
      #-a "$adapters"
    fi
    #collapsed Unmapped is fasta file; not suitabnle for fastqc
    if [[ -z "${TARG}" ]]; then
      continue;
    elif [[ "${TARG}" =~ 'uncollapsed' ]]; then
      if [[ -s Unmapped.out.mate1.gz ]]; then
        gunzip -k Unmapped.out.mate1.gz
        fastqc Unmapped.out.mate1 \
          --noextract -l "$settings" \
          --contaminants "$unplacable" ;
        rm Unmapped.out.mate1
      fi
    fi
    cd ..
  done
