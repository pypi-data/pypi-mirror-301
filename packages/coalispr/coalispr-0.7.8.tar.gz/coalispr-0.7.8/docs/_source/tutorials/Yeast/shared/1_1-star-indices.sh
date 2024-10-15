#!/bin/bash
#use settings for yeast
# first argument gives name for genome folder
EXP=$1
# second argument gives fasta file organism
DNA=$2
# third argument gives fasta file for extra DNA or for reference GTF
EXT="${3##*.}"
SRC_DIR="$(pwd)"


if (( $# == 2 )); then
  echo "Two parameters given (for name and genome)."
  DNAIN="${SRC_DIR}/${DNA}"
  RFGTF=""
elif (( $# == 3 )); then
  echo -e "Three parameters given:\n\tname:\t'${1}'\n\tgenome:\t'${2}' \
  and\n\t'${3}'."
  if [[ "$EXT" == "fasta" || "$EXT" == "fa" || "$EXT" == "fsa" ]]; then
    echo -e "Extra DNA file, '${3}', found."
    DNAIN="${SRC_DIR}/${DNA} ${SRC_DIR}/${3}"
    RFGTF=""
  elif [[ "$EXT" == "gtf" || "$EXT" == "GTF" ]]; then
    echo -e "Reference GTf file, '${3}', found."
    DNAIN="${SRC_DIR}/${DNA}"
    RFGTF=$3
  else
    echo -e "Extra file, '${3}', is not a fasta ('.fa', '.fsa', '.fasta') \
    or gtf ('.gtf', '.GTF') file, stopping .."
    exit
  fi
else
  echo -e "Two to three parameters (for name, genome and, \
  optionally, extra DNA or reference GTF) expected."
  exit
fi

STARDIR="star-${EXP}"

if [[ ! -s "${DNAIN}" ]]; then
  echo -e "Cannot find fasta file(s)\n '${DNAIN}', stopping.."
  exit
fi

echo "Genome indices will be stored in '${STARDIR}' in the current folder ('${SRC_DIR}')."

#from STAR manual:
# SAdx=min(14, log2(GenomeLength)/2 - 1);
# number of references:
#grep -e '>' GRCm.genome.fa | wc -l
#61

# wc -l GRCm.genome.fa - 61: 45470460-61 = 45470399
# 60 bases per line: 45470399*60 = 2728223940
# python3;
# >>>import numpy as np;
# >>>(np.log2(2728223940)/2)-1
# 14.67
# min(14,14.67)

# https://stackoverflow.com/questions/3096259/bash-command-to-sum-a-column-of-numbers
# use: awk '{s+=$1} END {print s}' filename
# or: command | paste -sd+ - | bc
#cut Saccharomyces_cerevisiae.R64-1-1.75_chromosome_lengths.txt -f 2 | paste -sd+ - | bc
#12157105
# >>> (np.log2(12157105)/2)-1
#10.767648190764776
#do not use 11, gives a STAR error

SAdx=10

# --genomeChrBinNbits=min(18, log2[max(GenomeLength/NumberOfReferences,ReadLength)])
# wc -l Saccharomyces_cerevisiae.R64-1-1.75_chromosome_lengths.txt
#17
# >>> np.divide(12157105,17)
#715123.8235294118 <- max vs ReadLength ~75
# >>> np.log2(715123.8235294118)
#19.447833540279213
# default --genomeChrBinNbits = 18 seems Ok


# if you generated the genome indexes with annotations, STAR will assume splicing to annotated junctions,
# as --alignIntronMax only controls the annotated junctions. You can either (i) use genome with
# annotations and --alignSJDBoverhangMin 999 (any number > read length) while mapping, or (ii)
# re-generate the genome without annotations.

# to turn off taking splicing into account, you need to use --alignIntronMax 1 during the mapping step
# in addition to not using a GTF at the genome generation step.
#

# add option (see STAR manual)
#--limitGenomeGenerateRAM
#default: 31000000000
#int>0: maximum available RAM (bytes) for genome generation
# if less RAM is available

if [[  -d "${STARDIR}" ]] ; then rm -r "${STARDIR:?}/"*; fi

if [[ ! -d "${STARDIR}" ]] ; then mkdir "${STARDIR}"; fi

cd "${STARDIR}" || exit

STAR \
  --runThreadN 4 \
  --runMode genomeGenerate \
  --genomeDir ./ \
  --genomeSAindexNbases "${SAdx}" \
  --genomeFastaFiles "${DNAIN}" \
  --sjdbGTFfile "${SRC_DIR}/${RFGTF}" \
  --sjdbOverhang 27
cd ..
echo -e "\nfinished STAR-index for ${EXP} genome.\n"
exit
