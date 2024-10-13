#!/bin/bash

# Copyright Rob van Nues 2022 sborg63@disroot.org
# using STAR for conversion from bam to bedgraph (RPM)
# Script is called by Coalispr function
# `bedgraphs_from_xtra_bamdata(bampath)` from 
# `python3 -m coalispr.bedgraph_analyze.process_bamdata`

# The following arguments (preformed filenames) come in;

# bamfile   = $1
# plusbg    = $2
# minbg     = $3

star=$(which STAR)

if [[ -x $star ]]; then
  $star \
    --runMode inputAlignmentsFromBAM \
    --inputBAMfile "$1" \
    --outWigType bedGraph \
    --outWigStrand Stranded \
    --outWigNorm None
    #--outWigNorm RPM # is the default 
    # but gives exaggerated signals
    # normalize the counts to total mapped reads
    # as given by the aligner
else
  echo "No STAR aligner available, stopping.."
  exit 1
fi

mv Signal.UniqueMultiple.str1.out.bg "${2}"
mv Signal.UniqueMultiple.str2.out.bg "${3}"
rm Signal.Unique.str1.out.bg
rm Signal.Unique.str2.out.bg
rm Log.out