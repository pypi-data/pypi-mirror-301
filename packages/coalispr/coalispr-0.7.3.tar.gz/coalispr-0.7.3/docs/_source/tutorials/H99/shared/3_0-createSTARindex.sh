#!/bin/bash
# Create indices for  STAR
# First argument gives name for genome folder, EXP, h99
EXP=$1
#EXP=h99
# Second argument gives fasta file organism;
#DNA=$2
DNA=h99.fasta
# Third argument gives fasta file for extra DNA
# make sure sequence has same name as in the prepared reference GTF, eg. 'extra'
EXT=NAT_G418_HYG.fa #"${3##*.}"
# For reference GTF
GTF=h99.gtf
#--sjdbGTFfile ../${DIR}/${GTF} \
# Bbased on previous STAR runs and the given output
#SJDB=SpliceJunctionDataBase-sorted-uniq.txt
#--sjdbGTFfile ../${DIR}/${SJDB}
#SRC_DIR="$(pwd)"
# for sRNAseq, i.e. short mappable reads expected:
SAdx=11
DIR=source
#--genomeFastaFiles ../${DIR}/${BASE}.${DNA}_r.fasta \
#BASE=Cryptococcus_neoformans_var_grubii_h99.CNA3
#DNA=dna_sm.toplevel
#GTF=H99.10p.aATGcorrected.longestmRNA.2019-05-15.RiboCode.WithStart

# number of threads
n=4

STARDIR="star-${EXP}"
if [[  -d "$STARDIR" ]] ; then rm -r "${STARDIR:?}/"*; fi
if [[ ! -d "${STARDIR}" ]] ; then mkdir "${STARDIR}"; fi

cd "${STARDIR}" || exit

STAR --runThreadN "$n" \
  --runMode genomeGenerate \
  --genomeDir ./ \
  --genomeFastaFiles "../${DIR}/${DNA}" "../${DIR}/${EXT}"\
  --genomeSAindexNbases "${SAdx}" \
  --sjdbGTFfile "../${DIR}/${GTF}" \
  --sjdbOverhang 27
echo " finished STAR-index for small RNAseq of ${EXP}."
cd ..
