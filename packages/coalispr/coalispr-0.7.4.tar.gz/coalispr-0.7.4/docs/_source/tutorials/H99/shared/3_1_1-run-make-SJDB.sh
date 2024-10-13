#!/bin/bash
EXP=$1

if (( $# == 1 )); then
    echo "One parameter given (for experiment name);"
    MISM=0
elif (( $# == 2 )); then
    echo "Two parameters given (for name and mismatches)."
    MISM=$2
else
    echo "One or two parameters (for name and mismatches) expected."
    exit
fi

if [[ -z $MISM ]]; then
    echo "Using alignments with no mismatches"
    MISM=0
elif [[ "${MISM}" =~ ^[0-9]$ ]]; then
    echo "Using alignments with ${MISM} mismatches."
else
    echo "Sorry, cannot use input, stopping..."
    exit
fi

USE_DIR="STAR-analysis${MISM}-${EXP}_collapsed"
tag="_collapsed_${MISM}mismatch-${EXP}"
DATA=${DATA:-SRR[6-8][4-6][6-9][6-7][3-6][0-9]*$tag}


# Create splice-juction reference database from previous mapping exercises
SJDB="SpliceJunctionDataBase"

if [[ -s "source/${SJDB}-sorted-uniq.txt" ]]; then
  echo "Found database with splice junctions, '${SJDB}-sorted-uniq.txt'; renaming to ${SJDB}-sorted-uniq.ORIG.txt"
  mv -f "source/${SJDB}-sorted-uniq.txt" "source/${SJDB}-sorted-uniq.ORIG.txt"
elif [[ ! -s "source/${SJDB}-sorted-uniq.txt" ]]; then
  echo "No '${SJDB}-sorted-uniq.txt'; Creating splice junctions data base from SJ.out files in collapsed data.."
fi


# Get first 4 columns from sjdb files and put together
today=$(date +"%d%b%Y")

cd "$USE_DIR" || exit

#echo "$(pwd)"
for k in $DATA
  do
    echo "$k"
    if [[ ! -s "${k}/_STARgenome/sjdbList.out.tab" ]]; then
      echo  "No splice junctions found in ${k}"
      continue
    elif [[ -s "${k}/_STARgenome/sjdbList.out.tab" ]]; then
      echo "Adding info from ${k}"
      #    cut -f 1,2,3,4 $k >> ${SJDB}-$today.txt
      cat "${k}/_STARgenome/sjdbList.out.tab" >> "${SJDB}-${today}.txt"
    fi
done;

echo "Sorting database"

sort -k 1n,1 -k2n "${SJDB}-${today}.txt" > "${SJDB}-${today}-sorted.txt"

echo "Removing duplicates"
uniq "${SJDB}-${today}-sorted.txt" > "${SJDB}-${today}-sorted-uniq.txt"
echo "Copying sorted file with unique splice junctions.."

cp -f "${SJDB}-${today}-sorted-uniq.txt" "../source/${SJDB}-sorted-uniq.txt"

echo "Check duplicates"
uniq -c "${SJDB}-${today}-sorted.txt" > "${SJDB}-${today}-duplicates.txt"

rm "${SJDB}-${today}-sorted.txt"
rm "${SJDB}-${today}.txt"

cd ..

echo "done"
