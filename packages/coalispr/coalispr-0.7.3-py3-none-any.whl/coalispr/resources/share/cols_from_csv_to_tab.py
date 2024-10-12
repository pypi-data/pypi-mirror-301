#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  col_from_csv_to_tab.py
#
#
#  Copyright 2022 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Script to extract columns from csv for constructing a tabbed tsv file."""
import pandas as pd
from argparse import (
    ArgumentParser,
    SUPPRESS,
    )

mouse = { 'cols': [
            "Run","GEO_Accession (exp)","Experiment","Fraction","Sample Name"],
          'rows': [
            "SRR6442834", "SRR6442835", "SRR6442837", "SRR6442838",
            "SRR6442840", "SRR6442841", "SRR6442843", "SRR6442844", ],
          'outfile' : "GSE108799_Exp.tsv"
          }

yeast = { 'cols' : [
            "Run","GEO_Accession (exp)","Experiment","Sample Name"],
          'rows' : [
            "SRR4305543", "SRR4305544", "SRR14570780", "SRR14570781",
            "SRR4024838", "SRR4024839", "SRR4024840", "SRR4024831",],
          'outfile' : "Kre33Puf6_Exp.tsv"
          }

h99 = {'cols' : [],
       'rows' : [],
       }

jec21 = {'cols' : [],
       'rows' : [],
       }

tutorials = {1: mouse, 2: yeast, 3: h99, 4: jec21}

def load_list(infile,tutorial):
    try:
        infiles = infile.split(',')
        df = pd.read_csv(infiles[0], index_col=0,
            usecols=tutorials[tutorial]['cols'], dtype='object' )
        for filein in infiles[1:]:
            dg = pd.read_csv(filein, index_col=0,
            usecols=tutorials[tutorial]['cols'], dtype='object' )
            df = pd.concat(objs = [df,dg])
        #print(df)
        return df
    except:
        raise SystemExit("Comma-separated string of filenames expected.")

def load_file(infile, tutorial, expandfile):
    """Script to help constructing an EXPFILE for tutorials

    Parameters
    ----------
    file : str
        Input file with extension '.csv', or '.txt' to retrieve columns from.
    tutorial : int
        Option to set tutorial for EXP.
    expandfile : str
        File with extension '.csv', or '.txt' to add retrieved columns to.
    """

    try:
        df = pd.read_csv(infile, index_col=0,
            usecols=tutorials[tutorial]['cols'] )
    except KeyError:
        pass
    except FileNotFoundError:
        df = load_list(infile, tutorial)


    # select only the needed rows
    df1 = df.loc[tutorials[tutorial]['rows']]
    ef = pd.read_csv(expandfile, sep='\t', index_col=0 )
    df2 = pd.merge(ef, df1, left_index=True, right_index=True, how='outer')
    # rename reference run
    isR = df2["Category"] == "R"
    rfx = df2[isR].index
    df2 = df2.rename(index = {rf : 'ref'+rf for rf in rfx})
    print(df2)
    df2.reset_index().to_csv(tutorials[tutorial]['outfile'], sep='\t',
        index=False)
    #print(ef)
    #print(df.index, ef.index)
    #print(df2['Fraction'])
    #print(tutorials[tutorial]['rows'])
    #print(df2.loc["SRR6442835"])
    #print(df2.loc[tutorials[tutorial]['rows']])

def main(args):# Disable default help

    descrip = ("Remove columns from csv file -f")
    parser = ArgumentParser(add_help=False, description=descrip)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-f','--file', type=str, required=True,
        help="required input file(s) with extension '.csv', or '.txt'.")
    required.add_argument('-t','--tutorial',type=int, choices=[1,2,3],
        dest='tutorial', default='',
        help='provide tutorial name: 1: mouse, 2: h99, 3:jec21')
    required.add_argument('-e','--expandfile', type=str, required=True,
        dest='toexpand', default='',
        help=("required file with extension '.csv', or '.txt' to add "
            + "required columns."))
    # Add back help
    optional.add_argument('-h','--help',
        action='help', default=SUPPRESS,
        help='show this help message and exit')

    args = parser.parse_args()

    load_file(args.file, args.tutorial, args.toexpand)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
