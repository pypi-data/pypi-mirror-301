#!/bin/bash
# -k is kind/output name
kind='common_ncRNAs'
# -a is all feature lines (1) or only those that can be displayed (0)
all=0
# -g is compressed reference gtf
refs='mouse_annotation.gtf.gz'
# -l is list of features to be selected
feats="snRNA,snoRNA,tRNA,miscGm;rRNA,misc7SK;scaRNA,miscSRP;Y_RNA;pseudogene"
python3 sub_gtf.py -k "$kind" -a "$all" -g "$refs" -l "$feats"

#inputgz=$1
#
#if [[ -z $inputgz ]]; then
#  echo "Please, provide compressed annotations file (.gtf.gz) as input"
#  exit
#fi
#
#input=$(gunzip -cf $inputgz)
## collect entries for common ncRNAs
#cat $input | grep snRNA > tmp
#cat $input | grep snoRNA >> tmp
#cat $input | grep tRNA >> tmp
#cat $input | grep rRNA >> tmp
#sort -k 1.4h,1 -k 4n,4 -k 5nr,5 tmp > mouse_ncRNAs.gtf
#rm tmp $inputgtf
