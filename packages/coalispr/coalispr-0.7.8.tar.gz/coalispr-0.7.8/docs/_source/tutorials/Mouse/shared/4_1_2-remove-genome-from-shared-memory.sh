#!/bin/bash
# NOTE USE full path for STAR:
SRC_DIR="$(pwd)"
EXP=$1
REF_DIR="${SRC_DIR}/star-${EXP}"

if [[ ! -d "${REF_DIR}" ]]; then
  echo "'${REF_DIR}' not found; Do you need to add the EXP parameter?"
  exit
fi

# Make sure no STAR is running:
if [[ $(pidof STAR) ]]; then
  echo "STAR process still running; stopping it.."
  pkill STAR
fi
# Remove a pre-loaded genome from memory
# see: https://github.com/alexdobin/STAR/issues/604

STAR \
    --genomeDir "$REF_DIR" \
    --genomeLoad Remove \
    --outSAMtype None ;
# Remove local stuff left by STAR
#rm -r _STARtmp
rm Log.*

exit

# If still memory occupied after closing it all; try closing the terminal you were working in.

# this generated the following at my end:
#
# bash-5.1$ sh 4_1_2-remove-genome-from-shared-memory.sh
#                STAR --genomeDir /<path to>/Sarshad-2018/star-mouse --genomeLoad Remove --outSAMtype None
#                STAR version: 2.7.10a   compiled: 2022-01-31T21:02:42+00:00 /tmp/SBo/STAR-2.7.10a/source
#        Sep 02 01:24:03 ..... started STAR run
#        Sep 02 01:24:03 ..... loading genome
#
#        Shared memory error: 11, errno: Operation not permitted(1)
#        EXITING because of FATAL ERROR: There was an issue with the shared memory allocation. Try running STAR with --genomeLoad NoSharedMemory to avoid using shared memory.
#        Sep 02 01:24:06 ...... FATAL ERROR, exiting
#

# Another way was to find the stuck memory blocks with:
# (from: https://www.systutorials.com/how-to-list-and-delete-shared-memory-in-linux/)
# List all shared memories in your Linux Systems
#
#  $ ipcs -m
#
# Delete specific one
#
#  $ ipcrm -M 0x0001869c
#
