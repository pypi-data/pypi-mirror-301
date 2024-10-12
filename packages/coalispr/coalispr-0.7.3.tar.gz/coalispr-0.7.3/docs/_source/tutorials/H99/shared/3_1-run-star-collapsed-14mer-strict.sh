#!/bin/bash

# number of threads
n=4

DATA=${DATA:-SRR[6-8][4-6][6-9][6-7][3-6]*}

# Get the EXP name for picking correct reference
EXP=$1
# Store required maximum number of mismatches in second argument
MISM=$2
# Redo splice junctions
REDOSJ=$3

# NOTE: Use full path for STAR:
SRC_DIR="$(pwd)"
REF_DIR="${SRC_DIR}/star-${EXP}"
# Speed up mapping by using references for splice junctions from previous mappings; or a gtf
# Based on previous STAR runs and their SJ.out.tab output, which was cat-ed, sorted with -u.
SJDB="${SRC_DIR}/source/SpliceJunctionDataBase-sorted-uniq.txt"
#--sjdbGTFfile ../${DIR}/${SJDB}CRYPr_GTF="/home/working/DATA_ANALYSIS_2/dataOtherLabs/Burke-2019/source/H99.10p.aATGcorrected.longestmRNA.2019-05-15.RiboCode.WithStart.gtf"

if (( $# == 2 )); then
  echo "Two parameters given (for experiment name and mismatches); using existing splice junction database."
  REDOSJ=0
elif (( $# == 3 )); then
  echo "Three parameters given (for name, mismatches, redo splice junctions)."
  REDOSJ=$3
else
  echo "Two or three parameters (for name, mismatches, redo splice junctions) expected; stopping.."
  exit
fi

if [[ "${MISM}" =~ ^[0-9]$ ]]; then
  echo "Using alignments with ${MISM} mismatches."
else
  echo "Sorry, cannot use input, stopping..."
  exit
fi

if [[ ${REDOSJ} == 1 ]]; then
  echo "Collecting splice junction data, while making alignments.."
  TPMODE=Basic
  DOSJ=""
else
  echo "Skip collecting splice junction data.. using provided.."
  TPMODE=None
  DOSJ=${DOSJ:---sjdbFileChrStartEnd $SJDB}
  #echo "${DOSJ}"
fi

REF_DIR="${SRC_DIR}/star-${EXP}"

if [[ ! -d ${REF_DIR} ]]; then
  echo "'${REF_DIR}' not found; Do you need to add the EXP parameter?"
  exit
fi

# See: https://github.com/alexdobin/STAR/issues/604
# On a computer cluster use
#MEM=NoSharedMemory #default
# On a single computer with over 30 Gb memory
#MEM=LoadAndKeep
# When including a splice-junction file, LoadAndKeep cannot be used.
MEM=NoSharedMemory

startdir="STAR-analysis"
workdir="${startdir}${MISM}-${EXP}_collapsed/"
tag="_collapsed_${MISM}mismatch-${EXP}"

if [[ ! -d "$workdir" ]] ; then mkdir "$workdir"; fi

for i in $DATA
  do
    echo "Checking STAR-folder for ${i} .."
    # check of old alignment folders are there; these need to be renamed
    olddir="${workdir}${i}${tag}"
    _olddir="${workdir}_${i}${tag}"
    if [[ -d ${olddir} ]]; then
        echo "Previous alignments found; these will be renamed."
        mv -f "${olddir}" "${_olddir}"
        echo "${i} renamed to _${i} in ${workdir}"
    fi
    if [[ !  -d "${workdir}${i}${tag}" ]]; then
      mkdir  -m a=rwx "${workdir}${i}${tag}";
    fi
done

for i in $DATA
  do
    cd "${workdir}${i}${tag}" || exit
    echo "mapping ${i}"
    STAR \
    --runThreadN "$n" \
    --genomeLoad "${MEM}" \
    --genomeDir "$REF_DIR" \
    --readFilesIn "${SRC_DIR}/${i}/${i}-collapsed.fasta" \
    "${DOSJ}" \
    --outFilterType BySJout \
    --outSAMprimaryFlag AllBestScore \
    --outReadsUnmapped Fastx \
    --outMultimapperOrder Random \
    --outSAMtype BAM Unsorted \
    --outFilterMismatchNmax 0 \
    --outFilterMatchNmin 14 \
    --outFilterScoreMinOverLread 0 \
    --outFilterMatchNminOverLread 0 \
    --outSJfilterOverhangMin  6 4 4 4 \
    --outFilterMultimapNmax 50 \
    --seedSearchLmax 28 \
    --seedSplitMin 9 \
    --alignIntronMin 20 \
    --alignIntronMax 150 \
    --alignSJoverhangMin 3 \
    --alignSJDBoverhangMin 2 \
    --alignEndsType EndToEnd \
    --twopassMode "${TPMODE}";
    gzip -f Unmapped.out.mate1
    cd ../../;
  done

exit 1

#for collapsed reads quality score could be omitted but this would change column order
#--outSAMmode NoQS \
#
#--sjdbFileChrStartEnd "${SJDB}" \
#--sjdbGTFfile
#--twopassMode Basic;
#for collapsed reads in case of multimappers
#--outSAMmultNmax 1 \
#might have caused the loss of T3 peaks
#prohibit splicing with --alignIntronMax 1
#If you do not need counting over genes in the GTF file, you can omit the --sjdbGTFfile and --sjdbOverhang parameters altogether.

# --outFilterMismatchNmax 0
# --outSAMattributes NH HI AS nM MD \
# get info where mismatch could be
# --outSAMattributes NH HI AS nM MD \
# with spjdb no need to do
#   --twopassMode Basic;
#also reduce --alignIntronMax 1000000 \
#this default takes 35 min vs 8.5 for 4000-1_n4
#take out --seedSearchStartLmax
#slows mapping to 13 min.
#it does determine seed-length, but
#hom many nt are skipped before mapping starts
#had this at 10 (blocks to seed alignment from)
#As determined with Jellyfish
#for each 10-mer ~ 11-12 start sites possible;
#at 12 mostly 1x
#
#also do not clip reads; they are either correct or
#should be thrown out: changed
#--alignEndsType Extend5pOfRead1
#taken out
# --seedMultimapNmax 10000 \
# --winAnchorMultimapNmax 1000 \
#crypto introns are short ~50-60 nt, so max 200 might speed up alignment
###FOR STRICT
# used here: --outFilterMismatchNmax 0  instead of normally:
# --outFilterMismatchNoverReadLmax 0.05  would allow for 0.05x20=~1 per read

#also taken out looking for chimeric reads; only useful for CRAC I think
#--chimOutType WithinBAM \
# --chimSegmentMin 10 \
# --chimJunctionOverhangMin 10 \
# --chimSegmentReadGapMax 6 \

# option --outFilterMatchNmin 14 \
# is for matches between paired reads
# NOT minimal mapped length
# BUT is advised with
# --outFilterScoreMinOverLread 0 \
# --outFilterMatchNminOverLread 0 \
# use flexbar for setting minimal readlengths
# --outFilterMatchNmin 16 limits the mapped length to 16b
# --outFilterScoreMinOverLread  0
# --outFilterMatchNminOverLread 0

#If you are willing to work with multimappers mapping to >20 loci, increase
# --outFilterMultimapNmax
# increase --winAnchorMultimapNmax from the default 50 to reduce remaining unmapped reads

# reduce  --seedSearchStartLmax to 10 (or even less) to allow for shorter seeds.
