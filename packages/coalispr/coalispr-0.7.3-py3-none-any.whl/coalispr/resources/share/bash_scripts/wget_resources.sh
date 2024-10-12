#!/bin/bash
# simple script to access resources
# relies on the program wget
FUNGIFTP=ftp://ftp.ensemblgenomes.org/pub/fungi/release
NCBIGB=ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/fungi/Cryptococcus_neoformans/latest_assembly_versions

read -r -e -p "Enter strain: H99 or JEC21 > "
STRAIN=$REPLY
if [[ "$STRAIN" = "JEC21" ]]; then
  ORGANISM=cryptococcus_neoformans
  RESOURCE=Cryptococcus_neoformans.ASM9104v1
  GFF=JEC21.10p.aATGcorrected.longestmRNA.2018-12-03.RiboCode.WithStart
  GB=GCA_000091045.1_ASM9104v1/GCA_000091045.1_ASM9104v1_genomic.gbff.gz
  ABBR=cneoDgenom
  XTRAFILE="../constant_in/3_JEC21.txt"

elif [[ "$STRAIN" = "H99" ]]; then
  ORGANISM=fungi_basidiomycota1_collection/cryptococcus_neoformans_var_grubii_h99_gca_000149245
  RESOURCE=Cryptococcus_neoformans_var_grubii_h99_gca_000149245.CNA3
  GFF=H99.10p.aATGcorrected.longestmRNA.2019-05-15.RiboCode.WithStart
  GB=GCA_000149245.3_CNA3/GCA_000149245.3_CNA3_genomic.gbff.gz
  ABBR=cneoAgenom
  XTRAFILE=""
fi

read -r -e -p "Enter release no. [NUMBER] or 1 for latest genbank gbff, or 0 for Wallace-2020 gff> "
RELEASE=$REPLY #38
# echo "Release is ${RELEASE}"


DNA=${RESOURCE}.dna_sm.toplevel.fa
WALL=https://github.com/ewallace/CryptoTranscriptome2018/raw/master/CnGFF/


GTF=${RESOURCE}.${RELEASE}.gtf
TMP=${ABBR}_${RELEASE}

PATTERN1="DNAXTRA  "
PATTERN2="CHRXTRA  "
#GTFRES="../resources/gtfs"
DWNLD="../../../../downloads"
TDIR=${DWNLD}release${RELEASE}
DNAXTRA=$(cat $XTRAFILE | grep -e "${PATTERN1}" | cut -d "'" -f 4)
XTRAHEAD=$(cat $XTRAFILE | grep -e "${PATTERN2}" | cut -d "'" -f 2)
echo "${DNAXTRA}, ${DNAXTRA%%.*},>${XTRAHEAD}"

if [[ $RELEASE == 0 ]]; then
  echo -e "\nDownloading gff Wallace annotation..."
  wget -cN --show-progress -P "${DWNLD}" "${WALL}${GFF}.gff3"
  ##downloaded 'gff3' is in gtf format
  mv ${DWNLD}/${GFF}.gff3 ${DWNLD}/${GFF}.gtf
  gzip ${DWNLD}/${GFF}.gtf
elif [[ $RELEASE == 1 ]]; then
  echo -e "\nDownloading NCBI complete genbank source...\n"
  wget -cNrnd --show-progress --timestamping -P "${DWNLD}/genbank" "${NCBIGB}/${GB}"
else
  echo -e "\nDownload what kind of file for release ${RELEASE}?"
  read -r -e -p "1: genbank, 2: fasta, 3: gtf [NUMBER] > "
  TYPE=$REPLY

  if [[ $TYPE == 1 ]]; then
    echo -e "\nDownloading genbank source..."
    wget -cNrnd --show-progress --timestamping -P "${TDIR}/genbank" "${FUNGIFTP}-${RELEASE}/genbank/$ORGANISM/"
  elif [[ $TYPE == 2 ]]; then
    echo -e "\nDownloading data source..."
    wget -cN --show-progress -P "${TDIR}/fasta" "${FUNGIFTP}-${RELEASE}/fasta/$ORGANISM/dna/${DNA}.gz"
    gunzip "${TDIR}/fasta/${DNA}.gz"
    echo -e "\nCleaning up fasta headers"
    python3 clean_fasta.py -f "$TDIR/fasta/${DNA}" -o "${DWNLD}/${TMP}.fasta"
    # allow for absence xtra stuff
    # echo -e "\n${DNAXTRA:=None}"
    if [[ ${DNAXTRA:=None} != None ]]; then
    echo -e "\nAdd extra data source..."
    XTRAIN=../fasta/${DNAXTRA}
    cat "${DWNLD}/${TMP}.fasta" $XTRAIN > "${DWNLD}/${TMP}.1.fasta"
    mv "${DWNLD}/${TMP}.1.fasta" "${DWNLD}/${TMP}.fasta"
    echo -e "\nFile concatenated with ${XTRAIN} and saved as '${DWNLD}/${TMP}'"
    echo -e "\nAdjusting fasta header '${DNAXTRA%%.*}' to '$XTRAHEAD'"
    replace "${DNAXTRA%%.*}" "${XTRAHEAD}" -- "${DWNLD}/${TMP}.fasta"
    fi
    echo -e "\nProcessed fasta download to '${DWNLD}/${TMP}.fasta'"
    rm "${TDIR}/fasta/${DNA}"
    rmdir "$TDIR/fasta"
    rmdir "${TDIR}"
    echo -e "\nRemoved downloaded '${TDIR}/fasta/${DNA}'"
  elif [[ ${TYPE} == 3 ]]; then
    echo -e "\nDownloading gtf annotation..."
    wget -cN --show-progress -P "${TDIR}/gtf" "${FUNGIFTP}-${RELEASE}/gtf/$ORGANISM/${GTF}.gz"
    #gunzip $TDIR/gtf/${GTF}.gz
    #python3 clean_gtf.py $TDIR/gtf/${GTF} ${DWNLD}/${TMP}.gtf
    echo -e "\nProcessed gtf download to '${DWNLD}/${TMP}.gtf'"
  else
    echo -e "\nNo working choice made"
  fi
fi
