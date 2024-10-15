#!/bin/bash
#
# Mouse specific input
KIND='miRNA' # will form output '${KIND}s.gtf'
# -a is all feature lines (1) or only those that can be displayed (0)
ALL=0
LIBR='gene2ensembl.gz'
REFS='mouse_annotation.gtf.gz'
TARG='miRDB.gz'
OUTF='miRNAtargets' # omit extension '.gtf'
# Extra stuff
COMB=$1
# When combining with another file given as input
IN=$2 # no gtf extension

# Mouse-lines in $TARG, linked to miRDB_v[No]_prediction_result.txt.gz begin with 'mmu'.
# Use NM reference in the second column to find ensemble homologous name.
# Use ensembl name to find gtf entries.
if [[ $# == 1 ]] ; then
    # Collect entries for putative miRNA targets
    echo "Building '${KIND}s.gtf' and '${OUTF}.gtf' for ${KIND} and targets using '${LIBR}', '${REFS}' and '$TARG'."

    # Use specific pythonscript to get prediced targets as ensembl IDs.
    # Assemble these with the kind of RNAs that associate with the targets.
    # Output as $OUTF
    python3 get_smallRNAs_and_targets.py -k "$KIND" -a "$ALL" -t "$TARG" -l "$LIBR" -g "$REFS" -o "$OUTF"
    echo "Done"
elif [[ $# == 3 ]]; then #-z $COMB -z $IN ]]; then
    echo "Combining '${IN}' and '${COMB}' to '${IN}_2.gtf'"
    cat "${IN}.gtf" "$COMB" > tmp
    sort -k 1.4h,1 -k 4n,4 -k 5nr,5 tmp > "${IN}_2.gtf"
    rm tmp
else
    echo "Nothing to do."
fi
exit 1
