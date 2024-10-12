#!/bin/bash
startdir="STAR-analysis"
EXP=$1

if (( $# == 2 )); then
    echo "Two parameters given (for name and mismatches)."
    MISM=$2
elif (( $# == 1 )); then
    echo "One parameter given (for experiment name)"
    MISM=0
else
    echo "One or two parameters (for name and, optionally, mismatches) expected."
    exit
fi

if [[ "${MISM}" =~ ^[0-9]$ ]]; then
    echo "Using alignments with ${MISM} mismatches."
else
    echo "Sorry, cannot use input, stopping..."
    exit
fi

targdir="${startdir}${MISM}-${EXP}"
COLL=collapsed
UNCOLL=uncollapsed
if [[ ! -d "${targdir}_${COLL}" ]]; then
    echo "Sorry, no ${targdir}_collapsed, stopping..."
    exit
fi
cd "${targdir}_${COLL}" || exit
#ls
sh ../5_1_0-run-RSeQC-bam_stat-FASTQC.sh "${COLL}"
cd ..
cd "${targdir}_${UNCOLL}" || exit
#ls
sh ../5_1_0-run-RSeQC-bam_stat-FASTQC.sh "${UNCOLL}"
cd ..
