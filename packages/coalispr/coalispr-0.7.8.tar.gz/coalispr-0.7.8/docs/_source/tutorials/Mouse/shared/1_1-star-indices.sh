#!/bin/bash
# Use settings for mouse
# First argument gives name for genome folder
EXP=$1
# Second argument gives fasta file organism
DNA=$2
# Third argument gives fasta file for extra DNA
XDNA=$2

EXT="${XDNA##*.}"

if (( $# == 2 )); then
  echo "Two parameters given (for name and genome)."
elif (( $# == 3 )); then
  echo "Three parameters given (for name, genome and extra DNA)"
else
  echo "Two to three parameters (for name, genome and, optionally, extra DNA) expected."
  exit
fi

STARDIR="star-${EXP}"
SRC_DIR="$(pwd)"

echo "Genome indices will be stored in '${STARDIR}' in the current folder ('${SRC_DIR}')."

if [[ ! -s "${XDNA}"  || "${XDNA}" == '' ]]; then
  echo "No extra DNA input"
elif [[  -s ${XDNA}  && "$EXT" == "fasta" || "$EXT" == "fa" ]]; then
  echo "Extra DNA file, '${XDNA}', found"
else
  echo "Extra DNA file, '${2}', is not a fasta file, stopping .."
  exit
fi

# From STAR manual:
# SAdx=min(14, log2(GenomeLength)/2 - 1);
# Number of references:
# $(grep -e '>' GRCm.genome.fa | wc -l)
# output: 61
# Number of nucleotidelines
# $(wc -l GRCm.genome.fa) - 61 = 45470460-61 = 45470399
# 60 bases per line: 45470399*60 = 2728223940
# python3;
# >>>import numpy as np;
# >>>(np.log2(2728223940)/2)-1
# 14.67
# min(14,14.67)
SAdx=14

# --genomeChrBinNbits=min(18, max(log2[GenomeLength/NumberOfReferences],ReadLength))
# 2728223940/61 = 44724982.62295082
# np.log2(44724982.62295082) = 25.414577585956856
# default --genomeChrBinNbits = 18 seems Ok


# If you generated the genome indexes with annotations, STAR will assume splicing to annotated junctions,
# as --alignIntronMax only controls the annotated junctions. You can either (i) use genome with
# annotations and --alignSJDBoverhangMin 999 (any number > read length) while mapping, or (ii)
# re-generate the genome without annotations.

# To turn off taking splicing into account, you need to use --alignIntronMax 1 during the mapping step
# in addition to not using a GTF at the genome generation step.
#

# When less RAM than 32 GB is available
# add option (see STAR manual)
#--limitGenomeGenerateRAM $int
# with $int maximum available RAM (bytes) for genome generation
# default: 31000000000


if [[  -d "$STARDIR" ]] ; then rm -r "${STARDIR:?}/"*; fi

if [[ ! -d "$STARDIR" ]] ; then mkdir "$STARDIR"; fi

cd "$STARDIR" || exit

STAR --runThreadN 4 \
--runMode genomeGenerate \
--genomeDir ./ \
--genomeFastaFiles "${SRC_DIR}/${DNA}" "${SRC_DIR}/${XDNA}" \
--genomeSAindexNbases ${SAdx} \
echo " finished STAR-index for small RNAseq"
cd ..


# Taken out:
#
#  --sjdbGTFfile ../${GTF} \
#  --sjdbOverhang 27
