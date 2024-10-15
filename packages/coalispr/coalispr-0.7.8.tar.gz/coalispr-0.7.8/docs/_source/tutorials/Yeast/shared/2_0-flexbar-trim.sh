#!/bin/bash
if [[ -z $1 ]]; then
  echo -e "No SRR accession given; processing hardcoded GEO numbers.."
  DATA=${DATA:-SRR[1-4][0-4][0-5][4-7]*}
elif [[ -s $1 ]]; then
  echo "SRR accession given; aligning ${*}.."
  DATA=${DATA:-$*}
fi

# number of threads
n=4


# PE reads
j=1
k=2

# Clear possible App_PE still there in read1 or read2:-n 10 -ao 6 -as "NAGATCGGAAGAGCACACGTCTG"
APPPE1="NAGATCGGAAGAGCACACGTCTG"
APPPE2="CAGACGTGTGCTCTTCCGATCTN"

for i in $DATA
  do
    if   [[ $i == SRR4305543  ]]; then NADAP1="ACACGACGCTCTTCCGATCTNNNCACTAGCN";  NADAP2="NGCTAGTGNNNAGATCGGAAGAGCGTCGTGT" # L5Bc; Kre33-data-I (exp73);
    elif [[ $i == SRR4305544  ]]; then NADAP1="ACACGACGCTCTTCCGATCTNNNGCACTAN";   NADAP2="NTAGTGCNNNAGATCGGAAGAGCGTCGTGT"  # L5Db; Kre33-data-II (exp72);
    elif [[ $i == SRR14570780 ]]; then NADAP1="ACACGACGCTCTTCCGATCTNNNGTGAGCN";   NADAP2="NGCTCACNNNAGATCGGAAGAGCGTCGTGT"  # L5Bb; Puf6 (exp73);
    elif [[ $i == SRR14570781 ]]; then NADAP1="ACACGACGCTCTTCCGATCTNNNCGTGATN";   NADAP2="NATCACGNNNAGATCGGAAGAGCGTCGTGT"  # L5Da; Puf6 (exp72);
    elif [[ $i == SRR4024838  ]]; then NADAP1="ACACGACGCTCTTCCGATCTNNNGTGAGCN";   NADAP2="NGCTCACNNNAGATCGGAAGAGCGTCGTGT"  # L5Bb; Nab3 (exp72);
    elif [[ $i == SRR4024839  ]]; then NADAP1="ACACGACGCTCTTCCGATCTNNNCGCTTAGC";  NADAP2="GCTAAGCGNNNAGATCGGAAGAGCGTCGTGT" # L5Ad; Nab3m (exp11B);
    elif [[ $i == SRR4024840  ]]; then NADAP1="ACACGACGCTCTTCCGATCTNNNGCGCAGC";   NADAP2="GCTGCGCNNNAGATCGGAAGAGCGTCGTGT"  # L5Ac; Nab3m (exp10B);
    fi

    echo "Processing ${i} clean 3' end.."
    flexbar -r "${i}/${i}_${j}.fastq.gz" -qf i1.8 -t "${i}/${i}-trim3_${j}"  -z GZ -n "$n" -ao 6 -as $APPPE1 -m 12;
    flexbar -r "${i}/${i}_${k}.fastq.gz" -qf i1.8 -t "${i}/${i}-trim3_${k}"  -z GZ -n "$n" -ao 6 -as $APPPE2 -m 12 -at LEFT;
    #flexbar -r "${i}/${i}_${j}.fastq.gz" -p "${i}/${i}_${k}.fastq.gz" -qf i1.8 -t "${i}/${i}-trim3"  -z GZ -n 10 -ao 6 -as "NAGATCGGAAGAGCACACGTCTG" -m 12;
    echo "Processing ${i} clean 5' end.."
    #5'linker: trim left; keep right sense/read1; inverse sequence is like 3end adapter for read2
    flexbar -r "${i}/${i}-trim3_${j}.fastq.gz" -qf i1.8 -t "${i}/${i}-trim35_${j}"  -z GZ -n "$n" -ao 6 -as $NADAP1 -m 12 -at LEFT;
    flexbar -r "${i}/${i}-trim3_${k}.fastq.gz" -qf i1.8 -t "${i}/${i}-trim35_${k}"  -z GZ -n "$n" -ao 6 -as $NADAP2 -m 12;
    #flexbar -r "${i}/${i}-trim3_${j}.fastq.gz" -p "${i}/${i}-trim3_${k}.fastq.gz" -qf i1.8 -t "${i}/${i}-trim35"  -z GZ -n 10 -ao 6 -as $NADAP -m 12 -at LEFT -ac ON;
    #echo "Trimming short overhangs.."
    # throws "ERROR: Read without counterpart in paired input mode."
    #flexbar -r "${i}/${i}-trim35_${j}.fastq.gz" -p "${i}/${i}-trim35_${k}.fastq.gz" -qf i1.8 -t "${i}/${i}-trim35t"  -z GZ -ap ON -av 25 -m 12
    echo "Cleaning up.."
    rm "${i}/${i}-trim3_${j}.fastq.gz" "${i}/${i}-trim3_${k}.fastq.gz"
  done


#--pre-trim-phred 30

# nebnext adapter      AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
# standard SE adapter: TGGAATTCTCGGGTGCCAAGGC
# Minimum quality as threshold for trimming was the Default: 20.
