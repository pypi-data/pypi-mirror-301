#!/bin/bash
startdir="STAR-analysis"
EXP=$1
MISM=$2

if (( $# == 2 )); then
  echo "Two parameters given (for name and mismatches)."
elif (( $# == 3 )); then
  echo "Three parameters given (for name, mismatches and data)."
elif (( $# == 1 )); then
  echo "One parameters given (for experiment name)"
else
  echo "One or two parameters (for name and, optionally, mismatches) expected."
  exit
fi

if [[ -z "$MISM" ]]; then #zero-length parameter
  echo "Using alignments with no mismatches"
  MISM=0
elif [[ "${MISM}" =~ ^[0-9]$ ]]; then
  echo "Using alignments with ${MISM} mismatch(es)."
else
  echo "Sorry, cannot use input, stopping..."
  exit
fi

if [[ -z $3 ]]; then
  echo -e "No SRR accession given; aligning hardcoded GEO numbers.."
  DATA=${DATA:-SRR[1-4][0-4][0-5][4-7]*}
elif [[ -s $3 ]]; then
  echo "SRR accession given; aligning ${3}.."
  DATA=${DATA:-$3}
fi

targdir="${startdir}${MISM}-${EXP}_collapsed"

if [[ ! -d "$targdir" ]]; then
  echo "Sorry, no $targdir, stopping..."
  exit
fi
cd  "$targdir" || exit
echo "In '$targdir'"
#ls
sh ../3_2_0-run-sortBAM-star-Bedgraph.sh "$DATA"
cd ..
