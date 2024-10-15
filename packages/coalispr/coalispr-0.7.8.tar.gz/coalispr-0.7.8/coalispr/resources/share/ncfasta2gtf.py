#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ncfasta2gtf.py
#
#  Copyright 2021-2022 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Script to convert home_made fasta to gtf.

From Cryptococcus_neoformans.ASM9104v1.ncrna_db.fa
only use fasta header, get something like this:

::

    14  RWvN    exon    347687  347851  .   -   .   gene_id "boxCDsnorna-116nt";
    transcript_id "boxCDsnorna-116nt"; gene-source "contains box-CD snoRNA; as
    CNAG_12022"; gene_biotype "ncRNA"; transcript_name "boxCDsnorna-116nt";
    transcript_source ""; transcript_biotype "ncRNA"; exon_id "boxCDsnorna-116nt"
"""
import sys

from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from datetime import datetime
from operator import attrgetter
from pathlib import Path


exts = ['.fa', '.fasta']


class Gtfline():
    """Class to deal with a line in a gtf file; all features are named 'exon'.

    Attributes
    ----------
    chrno : str
        Name of chromosome (seqid);
    source: str
        Origin of information for a feature.
    seqstart : int/str
        Start nucleotide featured region
    seqend : int/str
        End nucleotide featured region
    strand : str {'+','-', '.'}
        Strand with feature if applicable
    seqid : str
        Gene-id (also used as 'transcript-id')
    gentype:
        Type of transcript: 'exon', 'tRNA', etc.

    """
    lineobjects = []
    def __init__(self, chrno, source, seqstart, seqend, strand, seqid, gentype):
        self.chrno = chrno
        self.source = source
        self.seqstart = int(seqstart)
        self.seqend = int(seqend)
        self.strand = strand
        self.seqid = seqid
        self.gentype = gentype

    def __str__(self):
        return (f"{self.chrno}, {self.source}, {self.seqstart}, {self.seqend}, "
              f"{self.strand}, {self.seqid}, {self.gentype}")

    def printme(self):
        """Print gtf-line"""
        gtfline = (f"{self.chrno}\t{self.source}\texon\t{self.seqstart}\t"
          f"{self.seqend}\t.\t{self.strand}\t.\tgene_id \"{self.seqid}\"; "
          f"transcript_id \"{self.seqid}\"; gene_source \"\"; gene_biotype "
          f"\"{self.gentype}\"; transcript_name \"{self.seqid}\"; "
          f"transcript_source \"\"; transcript_biotype \"{self.gentype}\"; "
          f"exon_id \"{self.seqid}\";\n")
        return gtfline

    def sort_and_remove_duplicates():
        """Sort gtf and remove duplicate-entries based on feature coordinates"""
        # first sort on coordinates, then on chrno.
        sorted_lineobjects = sorted(Gtfline.lineobjects,
            key=attrgetter('seqstart', 'strand', 'seqend') )
        # chrno is a string but needs to be sorted as a number: lamba creates
        # tuples (length word, word) to sort on; longer names come at the end.
        sorted_lineobjects = sorted(sorted_lineobjects,
            key = lambda x: (len(x.chrno), x.chrno) )
        # skip dup[licates
        sorted_lineobjects = Gtfline.skip_duplicates(sorted_lineobjects)
        return sorted_lineobjects

    def equals(a, b):
        """Compare 2 Gtfline objects with respect to feature coordinates"""
        if (a.chrno, a.seqstart, a.strand, a.seqend) == (b.chrno, b.seqstart,
            b.strand, b.seqend):
            print(f"{a} is a duplicate of {b}")
            return True
        else:
            return False

    def skip_duplicates(lineobjects):
        """Skip duplicate-entries based on feature coordinates"""
        keptlineobjects = [lineobjects[0]]
        for lineobject in lineobjects[1:]:
            if Gtfline.equals(lineobject, keptlineobjects[-1]):
                print(f"Omitting duplicate: {lineobject}")
            else:
                keptlineobjects.append(lineobject)
        return keptlineobjects



def fasta2gtf(infile, gtfout):
    """Create GTF file from fasta-headers

    Parameters
    ----------
    infile : str
        Path to fasta file

    gtfout : str
        Path to gtf file (default: '')

    """
    infilename = Path(infile)
    if infilename.suffix not in exts:
        msg = ("Incorrect filename, expected file with extension "
              f"{', '.join(exts)}")
        raise SystemExit(msg)

    savefile = infilename if gtfout == '' else Path(gtfout)
    savefile = savefile.with_suffix(".gtf")

    with open(infilename, 'r') as filein, open(savefile,'w') as fileout:
        fileout.write("##gff-version 2\n")
        fileout.write(f"# created by {Path(__file__).name} on "
              f"{datetime.now().strftime('%d-%m-%Y')}\n")
        for line in filein:
            if line.startswith("#"):
                continue
            elif not line.startswith('>'):
                continue
            elif line.startswith('>'):
                useline = line[1:]
                _process(useline)

        lines = Gtfline.sort_and_remove_duplicates()
        for gtfline in lines:
            fileout.write(Gtfline.printme(gtfline))



def _process(useline):
    lineobjects = Gtfline.lineobjects

    def get_strand(strd):
        if strd.strip() == "-1":
            return "-"
        elif strd.strip() == "1":
            return "+"
        else:
            return '.'

    def processRWvN(useline):
        """>RWvN_boxCDsnorna-83nt ncrna 1:1859587:1859670:1
        """
        contents = useline.split(" ")
        seqid = contents[0].split('_',1)[1]
        source = contents[0].split('_',1)[0]
        gentype = contents[1]
        coord = contents[2].split(":")
        chrno = coord[0]
        seqstart = coord[1]
        seqend = coord[2]
        strand = get_strand(coord[3])
        return Gtfline(chrno, source, seqstart, seqend, strand, seqid, gentype)


    def processCN(useline):
        """>CNE01750-1 ncrna chromosome:ASM9104v1:5:481873:481955:-1
        gene:CNE01750 gene_biotype:tRNA transcript_biotype:tRNA # removed:
        gene_symbol:CNE01750
        """
        contents = useline.split(" ")
        seqid = contents[3].split(":")[1]
        source = 'rfam'
        gentype = contents[4].split(":")[1]
        coord = contents[2].split(":")
        chrno = coord[2]
        seqstart = coord[3]
        seqend = coord[4]
        strand = get_strand(coord[5])
        return Gtfline(chrno, source, seqstart, seqend, strand, seqid, gentype)

    def processEbfT(useline):
        """>EBT00005237711 ncrna chromosome:ASM9104v1:14:390372:390504:-1
        gene:EBG00005237710 gene_biotype:snRNA transcript_biotype:snRNA #
        removed: gene_symbol:U4
        or
        >EFT00053744263 ncrna chromosome:CNA3:2:279497:279607:-1
        gene:CNAG_10503 gene_biotype:rRNA transcript_biotype:rRNA
        description:5S ribosomal RNA
        """
        contents = useline.split(" ")
        seqid = contents[3].split(":")[1]
        source = 'rfam'
        gentype = contents[4].split(":")[1]
        coord = contents[2].split(":")
        chrno = coord[2]
        seqstart = coord[3]
        seqend = coord[4]
        strand = get_strand(coord[5])
        return Gtfline(chrno, source, seqstart, seqend, strand, seqid, gentype)


    if useline.startswith("RWvN") or useline.startswith("Ensembl"):
        # own annotation
        lineobjects.append(processRWvN(useline))
    elif useline.startswith("CN"):
        #gene-based annotation
        lineobjects.append(processCN(useline))
    elif useline.startswith("vnEB") or useline.startswith("EFT"):
        lineobjects.append(processEbfT(useline))
    else:
        xtra = '; wrong strand given' if useline.startswith("EBT") else ''
        print(f"Not processed: {useline}{xtra}.")



def main(args):
    descrip = "Convert sequence id's from fasta file -f to sorted gtf."
    # Disable default help
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit.')
    required.add_argument('-f','--fasta_file', type=str, required=True,
        help=f"required input file with extension {', '.join(exts)}.")

    optional.add_argument('-o','--output_gtf', type=str, default='',
        help=("name of gtf file to save, default: filename with extension "
              ".gtf."))

    args = parser.parse_args()

    # create gtf
    fasta2gtf(args.fasta_file, args.output_gtf)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
