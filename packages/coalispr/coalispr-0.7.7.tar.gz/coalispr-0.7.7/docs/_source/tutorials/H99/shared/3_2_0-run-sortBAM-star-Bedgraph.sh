#!/bin/bash
DATA=${DATA:-SRR[6-8][4-6][6-9][6-7][3-6]*}
#NOTE: No _ in filenames to be parsed in shell scripts (is a 'special character')

# number of threads
n=4

for i in $DATA
  do
    echo "processing ${i}";
    cd "${i}" || exit
    # https://github.com/alexdobin/STAR/issues/510
    #  mkfifo Unmapped.out.mate1 Unmapped.out.mate2
      #cat Unmapped.out.mate1 | gzip > Unmapped.out.mate1.gz &
      #cat Unmapped.out.mate2 | gzip > Unmapped.out.mate2.gz &
    if [[ ! -f samtoolsAligned.sortedByCoord.out.bam ]]; then
     #https://github.com/alexdobin/STAR/issues/465
      #you have to convert SAM into BAM first:
      # samtools view -bS Aligned.out.sam > Aligned.out.bam
      #   samtools sort Aligned.out.bam Aligned.sorted

      #https://github.com/alexdobin/STAR/issues/289
      # error happens when FASTQ files are derived from coordinate-sorted BAM files.
      # This would explain why STAR needs so much RAM for sorting - it decides on the
      # genomic bin size for sorting based on the first 100000 reads.
      # sort it with samtools.
      samtools sort -o samtoolsAligned.sortedByCoord.out.bam -@ "$n" -m 2G -O bam Aligned.out.bam;
      samtools index samtoolsAligned.sortedByCoord.out.bam;
    fi
    if [[ ! -f "${i}-antisense.bedgraph" ]]; then
      BDNAM=temp_
      if [[ !  -d "${BDNAM}" ]]; then
        mkdir "${BDNAM}";
      fi

      cd "$BDNAM" || exit

      STAR \
        --runMode inputAlignmentsFromBAM \
        --inputBAMfile ../samtoolsAligned.sortedByCoord.out.bam \
        --outWigType bedGraph \
        --outWigStrand Stranded

      cd ..
      mv "$BDNAM/Signal.UniqueMultiple.str2.out.bg" "${i}-minus.bedgraph"
      mv "$BDNAM/Signal.UniqueMultiple.str1.out.bg" "${i}-plus.bedgraph"
      mv "$BDNAM/Signal.Unique.str1.out.bg" "${i}-uniq-plus.bedgraph"
      mv "$BDNAM/Signal.Unique.str2.out.bg" "${i}-uniq-minus.bedgraph"

      rm -rf "$BDNAM"
    fi
    cd ..
  done
