#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  genbank2gtf.py
#
#  Copyright 2021 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Script to enerate gtf from genbank file."""
import gzip
from Bio     import SeqIO  #required package Biopython not needed for Coalispr
from pathlib import Path
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )
from datetime import datetime

exts = ['.dat', '.gbff', '.gbk', '.gb', '.gz', ]
convtab = '_conv.tab'


def genbank2gtf(file_name, conversion_table, otherpath, selected_features,
    gtf_name, include_lengths):
    """Generate gtf from genbank file for chosen features. Requires biopython.

    Parameters
    ----------
    file_name: str
        Full/relative path to (compressed, 'gz') genbank file ('.gbff', '.gbk',
        '.gb').
    conversion_table: str
        Start of name of conversion table (.tab file) to simplify chromosome
        names (these should be the same as used in the fasta file; see
        `clean_fasta.py`)
    otherpath : str
        Path to conversion table if not in default folder.
    selected_features : int
        Number for list of scanned features/types
    gtf_name : str
        Filename for output gtf.
    include_lengths : int {0.1}
        Flag to indicate whether to create a file with chromosome lengths;
        0: No; 1: Yes

    Returns
    -------
        Downloaded genbank file information translated to GTF.

    """

    path = Path(file_name)
    #print(path.suffixes)
    table = _get_table(Path(otherpath).joinpath(f"{conversion_table}{convtab}"))

    features = {
        0: ['pseudo','gene'],
        1: ['noncoding','ncRNA','tRNA', 'rRNA', 'snRNA', 'snoRNA',
           'trna', 'rrna', 'ncrna', 'snrna', 'snorna',],
        2: ['coding','gene','exon','cds'],
        3: ['MT','mito', 'gene','exon','CDS', 'cds', 'mt'],
        4: ['pseudo_noncoding','gene', 'tRNA', 'rRNA','snRNA', 'snoRNA',
            'trna', 'rrna','ncRNA', 'ncrna','snrna', 'snorna',],
        }

    gtf = (f"##gff-version 2\n# created by {Path(__file__).name} on "
          f"{datetime.now().strftime('%d-%m-%Y')}\n")
    lengths = 0
    lengthsrecord =''
    skipped = 0
    skippedtypes = set()
    foundtypes = set()

    def run_handle(handle):
        nonlocal lengths, lengthsrecord, gtf, skipped, skippedtypes

        for gb in SeqIO.parse(handle, "genbank"):
            acc = gb.id #gb.name #gb.description
            print("id: ",gb.id, "\nname: ",gb.name, "\ndescr: ",gb.description)
            acc = acc.split('.')[0] #if not "CN" in acc else acc[0:2]
            print("acc: ", acc)
            lengths = len(gb)
            lengthsrecord += f"{table[acc]}\t{lengths}\n"
            #print(f"SeqIO.parse gave acc {acc}, length {lengths} and "
            #     f"{len(gb.features)} features ")
            if (selected_features == 3 and
                table[acc] != features[selected_features][0]):
                print(f"Skipped {table[acc]}")
                continue

            for f in gb.features:
                if f.type.lower() not in features[selected_features]:
                    skipped += 1
                    skippedtypes.add( f.type )
                    continue
                elif f.type.lower() in features[selected_features]:
                    #print(f)
                    if (f.type.lower() == 'gene' and 'pseudo' in f.qualifiers
                        and 'locus_tag' in f.qualifiers):
                        #use locus tag as gene_id/transcript_id
                        gene_id = transcript_id = (
                            f"{f.qualifiers['locus_tag'][0]}-pseudo")
                        feat = 'exon'
                        foundtypes.add( f.type )
                    elif (f.type in ['tRNA','ncRNA','rRNA', 'snRNA', 'snoRNA',
                          ] and 'locus_tag' in f.qualifiers):
                        gene_id = transcript_id = (
                            f"{f.qualifiers['locus_tag'][0]}-{f.type}")
                        feat = 'exon'
                        foundtypes.add( f.type )
                    #elif f.type == 'ncRNA'
                    elif f.type.lower() == 'exon' and 'label' in f.qualifiers:
                        # in exported genebank
                        gene_id = transcript_id = f.qualifiers['label'][0]
                        feat = f.type
                        foundtypes.add( f.type )
                    elif 'gene' in f.qualifiers:
                        gene_id = transcript_id = f.qualifiers['gene'][0]
                        feat = f.type
                        foundtypes.add( f.type )
                    elif (f.type.lower() == 'cds' and 'locus_tag'
                            in f.qualifiers):
                        # catch MT non-tRNA genes
                        gene_id = transcript_id = f.qualifiers['locus_tag'][0]
                        feat = 'exon'
                        foundtypes.add( f.type )
                    else:
                        #sys.stderr.write( "Skipped entry: "
                        #     f"{'; '.join( str(f).split(nl) )}\n")
                        skipped += 1
                        skippedtypes.add( f.type )
                        continue

                comments = (f'gene_id "{gene_id}"; transcript_id '
                            f'"{transcript_id}"')

                #code strand as +/- (in genbank 1 or -1)
                strand = '+' if int(f.location.strand) > 0 else '-'

                #define gb
                """
                  seqname  - The name of the sequence. Must be a chromosome or
                             scaffold.
                  source   - The program that generated this feature.
                  feature  - The name of this type of feature. Some examples of
                             standard feature types are "CDS", "start_codon",
                             "stop_codon", and "exon".
                  start    - The starting position of the feature in the
                             sequence. The first base is numbered 1.
                  end      - The ending position of the feature (inclusive).
                  score    - A score between 0 and 1000. If the track line
                             useScore attribute is set to 1 for this annotation
                             data set, the score value will determine the level
                             of gray in which this feature is displayed (higher
                             numbers = darker gray). If there is no score value,
                             enter ".".
                  strand   - Valid entries include '+', '-', or '.' (for don't
                             know/don't care).
                  frame    - If the feature is a coding exon, frame should be a
                             number between 0-2 that represents the reading
                             frame of the first base. If the feature is not a
                             coding exon, the value should be '.'.
                  comments - gene_id "Em:U62317.C22.6.mRNA"; transcript_id
                             "Em:U62317.C22.6.mRNA"; exon_number 1
                """

                gtf += (f"{table[acc]}\t{acc}\t{feat}\t"
                        f"{f.location.start+1}\t"
                        f"{f.location.end}\t.\t{strand}\t."
                        f"\t{comments};\n")

    #print(f"Output gtf:\n{gtf}")
    if path.suffix in exts:
        path2 = path.with_suffix('')
        try:
            if path2.suffix in exts:
                handle = gzip.open(path, 'rt')
            elif path2.suffix not in exts:
                handle = path.open()
            run_handle(handle)
        except FileNotFoundError:
            raise SystemExit("File not found")
        finally:
            handle.close()
    else:
        print(f"Please choose a file with extension {exts}")
        return


    if not gtf_name:
        outputname = (f"{path.stem}-{features[selected_features][0]}")
        gtf_name = path.with_stem(outputname).with_suffix('.gtf')
    else:
        gtf_name = Path(gtf_name).with_suffix('.gtf')

    msg = f"Saved gtf as:\n '{gtf_name}'\n"



    with gtf_name.open('w') as output:
        output.write(gtf)

    if include_lengths == 1:
        lengths_name = path.with_stem(
            f"{path.stem}-lengths").with_suffix('.txt')
        msg = f"and a file with lengths as:\n '{lengths_name}'\n"
        with lengths_name.open('w') as output:
            output.write(lengthsrecord)

    sys.stderr.write( f"\nDuring conversion {skipped} entries were skipped of "
          f"type: {', '.join(skippedtypes)}.\n")
    sys.stderr.write( "Searched types: "
          f"{', '.join(sorted(features[selected_features][1:]))};\nFound types: "
          f"{', '.join(sorted(foundtypes))}. If overlap is not complete, you "
           "may need to download separate gtf files for these.\n\n")

    print(msg)




def _get_table(table_path):
    """Read conversion table, a tabulated file with on each line:

     'Accession' \t 'Chromosome name to be used'

     Accession numbers are without version number (i.e. '.1');
     use, for example,  'AE017342' instead of 'AE017342.1'

    Parameters
    ----------
    table_path : Path

    Returns
    -------
    dict of accession number (key) with short name (value)
    """
    #print(f"For chromosome conversion, using {table_path}")
    table={}
    with table_path.open() as tp:
        for line in tp:
            #print(line)
            if line.startswith("#"):
                continue
            lineparts = line.strip().split(sep="\t")
            #print(lineparts)
            try:
                table[lineparts[0]] = lineparts[1]
            except IndexError:
                pass
    return table



def main(args):

    descrip = ("Obtain lengths and gtf with kind of feature -k from genbank "
          "file -f and output as -o. Provide label -c for chromosome-conversion "
         f"table '<label>{convtab}' on path -p")
    p = Path(__file__).parent.joinpath('conversion_tables/')
    # Disable default help
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='Show this help message and exit')
    required.add_argument('-f','--genbank_file', type=str, required=True,
        help=f"Required input file with extension {exts}")
    required.add_argument('-c','--chromosome_conversion', type=str,
        required=True, help=("Label for chromosome conversion table "
           "'<label>_{convtab}', for example 'H99' or 'JEC21'"))

    optional.add_argument('-k','--feature_kind', type=int, choices=[0,1,2,3,4],
        default=2, help=("Kind of feature to extract:  0:'pseudo'; 1:'ncRNA'; "
          "2:'all coding'; 3:'MT'; 4: combine 0 and 1"))
    optional.add_argument('-p','--conversion_table_path', type=str, default=p,
        help=f"Path to tabbed file '<label>_{convtab}'; default={p}")
    optional.add_argument('-o','--output_gtf', type=str, default=None,
        help="Name of gtf file to save")
    optional.add_argument('-l','--lengths_file', type=int, choices=[0,1],
        default=0,
        help="Save a file with chromosome lengths; 0: No; 1: Yes")

    args = parser.parse_args()

    # create gtf
    genbank2gtf(
        file_name=args.genbank_file,
        conversion_table=args.chromosome_conversion,
        otherpath=args.conversion_table_path,
        selected_features=args.feature_kind,
        gtf_name=args.output_gtf,
        include_lengths=args.lengths_file,
        )

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
