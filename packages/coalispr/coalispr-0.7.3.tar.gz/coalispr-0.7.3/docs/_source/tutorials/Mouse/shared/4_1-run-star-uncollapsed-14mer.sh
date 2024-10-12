#!/bin/bash
# NOTE USE full path for STAR:
#SRC_DIR="/<path-to>/Sarshad-2018"
SRC_DIR="$(pwd)"
DATA=${DATA:-SRR64428[0-9][0-9]*}
# speed up mapping by using references for splice junctions from previous mappings; or a gtf
#MOUSE_GTF="/<path-to>/Sarshad-2018/mouse_annotation.gtf" #gunzip the archive

# Get the EXP name for picking correct reference
EXP=$1
# Store required maximum number of mismatches in second argument
#MISM=$2

if (( $# == 1 )); then
    echo "One parameter given (for experiment name); no mismatches."
    MISM=0
elif (( $# == 2 )); then
    echo "Two parameters given (for name and mismatches)."
    MISM=$2
else
    echo "One or two parameters (for name and mismatches) expected."
    exit
fi

if [[ "${MISM}" =~ ^[0-9]$ ]]; then
    echo "Using alignments with ${MISM} mismatches."
else
    echo "Sorry, cannot use input, stopping..."
    exit
fi

REF_DIR="${SRC_DIR}/star-${EXP}"

if [[ ! -d "${REF_DIR}" ]]; then
  echo "'${REF_DIR}' not found; Do you need to add the EXP parameter?"
  exit
fi

#https://github.com/alexdobin/STAR/issues/604
# On a computer cluster use:
#MEM=NoSharedMemory
# On a single computer with over 30 Gb memory (the mouse genome size is ~27 Gb):
MEM=LoadAndKeep
startdir="STAR-analysis"
workdir="${startdir}${MISM}-${EXP}_uncollapsed/"
tag="_uncollapsed_${MISM}mismatch-${EXP}"

if [[ ! -d "$workdir" ]] ; then mkdir "$workdir"; fi

for i in $DATA
  do
    echo "Checking STAR-folder for ${i} .."
    # Check for the presence of old alignment folders; these need to be renamed
    olddir="${workdir}${i}${tag}"
    _olddir="${workdir}_${i}${tag}"
    if [[ -d "${olddir}" ]]; then
        echo "Previous alignments found; these will be renamed."
        mv -f "${olddir}" "${_olddir}"
        echo "${i} renamed to _${i} in ${workdir}"
    fi
    if [[ !  -d "${workdir}${i}${tag}" ]]; then
      mkdir  -m a=rwx "${workdir}${i}${tag}";
    fi
done

# CLIP-reactions will have 1 nt mismatches;
# Normal miRNA seq is just IP, without croslink-induced mutations.
# Sequencess from SRR6442834-SRR6442845 in:
for i in $DATA
  do
    cd "${workdir}${i}${tag}" || exit
    echo "mapping ${i}"
    STAR \
      --runThreadN 4 \
      --genomeLoad "${MEM}" \
      --genomeDir "$REF_DIR" \
      --readFilesCommand gunzip -c \
      --readFilesIn "${SRC_DIR}/${i}/${i}-uncollapsed.fastq.gz" \
      --outSAMprimaryFlag OneBestScore \
      --outReadsUnmapped Fastx \
      --outMultimapperOrder Random \
      --outSAMtype BAM Unsorted \
      --outSAMmultNmax 1 \
      --outFilterMismatchNmax "${MISM}" \
      --outFilterMatchNmin 14 \
      --outFilterScoreMinOverLread 0 \
      --outFilterMatchNminOverLread 0 \
      --outFilterMultimapNmax 1000 \
      --seedSearchLmax 28 \
      --seedSplitMin 12 \
      --alignIntronMax 1 \
      --alignEndsType EndToEnd \
      --twopassMode None;
    gzip -f Unmapped.out.mate1
    cd ../../;
  done

exit 1

#
#
#
#for collapsed reads in case of multimappers
#--outSAMmultNmax 1 \
#might have caused the loss of T3 peaks
#prohibit splicing with --alignIntronMax 1
#do not check introns
# taken out:
#   --sjdbGTFfile "$MOUSE_GTF" \
#   --alignIntronMin 20 \
#   --alignIntronMax 150 \ -> set to 1
#   --alignSJoverhangMin 3 \
#   --alignSJDBoverhangMin 2 \
#

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
#   --seedMultimapNmax 10000 \
#   --winAnchorMultimapNmax 1000 \
#crypto introns are short ~50-60 nt, so max 200 might speed up alignment
###FOR STRICT
# used here: --outFilterMismatchNmax 0  instead of normally:
# --outFilterMismatchNoverReadLmax 0.05  would allow for 0.05x20=~1 per read

#also taken out looking for chimeric reads; only useful for CRAC I think
#--chimOutType WithinBAM \
#   --chimSegmentMin 10 \
#   --chimJunctionOverhangMin 10 \
#   --chimSegmentReadGapMax 6 \

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
