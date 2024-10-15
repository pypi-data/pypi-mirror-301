#!/bin/bash
#NOTE: Use full path for STAR:
SRC_DIR="$(pwd)"
# speed up mapping by using references for splice junctions from previous mappings; or a gtf
#YEAST_GTF="${SRC_DIR}/Saccharomyces_cerevisiae.R64-1-1.75_1.2.gtf" #gunzip the archive

# to turn off splicing, you need to use --alignIntronMax 1 in addition to not using GTF at the
# genome generation step.
# Get the EXP name for picking correct reference
EXP=$1
# store required maximum number of mismatches in second argument
MISM=$2
#files to align dependent on $3 input
#DATA="SRR[1-4][0-4][0-5][4-7]" # raises SC2125 warning
# PE, paired end. Strands defined as
j=1
k=2

if (( $# == 1 )); then
  echo "One parameter given (for experiment name); no mismatches."
elif (( $# == 2 )); then
  echo "Two parameters given (for name and mismatches)."
elif (( $# == 3 )); then
  echo "Three parameters given (for name, mismatches, and input data)."
else
  echo "One or two parameters (for name and mismatches) expected."
  exit
fi

if [[ -z "$MISM" ]]; then
  echo "Using alignments with no mismatches"
  MISM=0
elif [[ "${MISM}" =~ ^[0-9]$ ]]; then
  echo "Using alignments with ${MISM} mismatches."
else
  echo "Sorry, cannot use input, stopping..."
  exit
fi

#https://github.com/alexdobin/STAR/issues/604
# on a computer cluster use
#MEM=NoSharedMemory
# on a single computer with over 30 Gb memory (the mouse genome size is ~27 Gb)
#MEM=LoadAndKeep

# EndToEend:
#   most stringent;
#   no soft-clipping of adapter remnants or chimer-portions or poly-A tails (can be found easily in Unmapped)
#   used by https://groups.google.com/g/rna-star/c/IFj3fHG_Ysc for yeast
#   also with --seedSplitMin, --clip5pNbases (most adapters came with random N; maybe on reverse read this is still hanging on)
# Extend5pOfRead1
#   softclipping 3end read1 (5end read2)
# Extend5pOfReads12
#   like EndToEnd but allows softclipping not mapping 3end bits
#   but only for long read-sections

if [[ -z $3 ]]; then
  echo -e "No SRR accession given; aligning hardcoded GEO numbers\n \
using pre-loaded memory.."
  # prevents SC2125 warning
  DATA=${DATA:-SRR[1-4][0-4][0-5][4-7]*}
  MEM=LoadAndKeep
  ENDTYPE=EndToEnd
elif [[ -s $3 ]]; then
  echo "SRR accession given for reference; aligning ${3}.."
  DATA=${DATA:-$3}
  MEM=NoSharedMemory
  ENDTYPE=Local
fi

REF_DIR="${SRC_DIR}/star-${EXP}"

if [[ ! -d "${REF_DIR}" ]]; then
  echo "'${REF_DIR}' not found; Do you need to add the EXP parameter?"
  exit
fi

startdir="STAR-analysis"
workdir="${startdir}${MISM}-${EXP}_collapsed/"
tag="_collapsed_${MISM}mismatch-${EXP}"

if [[ ! -d "$workdir" ]] ; then mkdir "$workdir"; fi

for i in $DATA;
  do
    echo "Checking STAR-folder for ${i} .."

    # check of old alignment folders are there; these need to be renamed
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


#CLIP-reactions will have 1 nt mismatches;
#normal miRNA seq is just IP, without croslink-induced mutations.
#ignore chimers; mostly duplicates on trial run;
#use another program to find CLASH hybrids
for i in $DATA
  do
    read1="${SRC_DIR}/${i}/${i}-collapsed_${j}.fasta"
    read2="${SRC_DIR}/${i}/${i}-collapsed_${k}.fasta"
    cd "${workdir}${i}${tag}" || exit
    echo "PE mapping ${i}"

    STAR \
      --runThreadN 4 \
      --genomeLoad "${MEM}" \
      --genomeDir "$REF_DIR" \
      --readFilesIn "$read1" "$read2" \
      --outSAMprimaryFlag AllBestScore \
      --outReadsUnmapped Fastx \
      --outMultimapperOrder Random \
      --outSAMtype BAM Unsorted \
      --outSAMattributes NH HI AS nM MD \
      --outFilterMismatchNmax "${MISM}" \
      --outFilterMultimapNmax 100 \
      --outFilterIntronMotifs RemoveNoncanonicalUnannotated \
      --seedSearchLmax 28 \
      --seedSplitMin 11 \
      --alignEndsType "$ENDTYPE" \
      --twopassMode None;
    gzip -f Unmapped.out.mate1
    gzip -f Unmapped.out.mate2

    cd ../../;
  done

exit 1

#
# taken out:

# --outFilterScoreMinOverLread 0.33 \
# --outFilterMatchNminOverLread 0.33 \
# --outFilterMatchNmin 14 \
# --sjdbGTFfile "$YEAST_GTF" \
#
# --outSJfilterOverhangMin  6 4 4 4 \
#
#--sjdbFileChrStartEnd "${SJDB}" \
#
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

#do not soft-clip reads; they are either correct or
#should be thrown out: changed
#--alignEndsType Extend5pOfRead1

#crypto introns are short ~50-60 nt, so max 200 might speed up alignment
###FOR STRICT
# used here: --outFilterMismatchNmax 1  instead of normally:
# --outFilterMismatchNoverReadLmax 0.05  would allow for 0.05x~70 = 3.5 per read

#also taken out looking for chimeric reads; not useful; too many repeats
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
