#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  annot.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module for annotating counted segments with gen_id's from GTFs"""
import csv
import logging
import numpy as np
import pandas as pd

from coalispr.bedgraph_analyze.experiment import (
    discarded,
    drop_discarded,
    get_positive,
    )
from coalispr.bedgraph_analyze.genom import (
    ref_in_segment,
    )
from coalispr.count_analyze.countfile_plots import (
    load_count_table,
    )
from coalispr.resources.constant import (
    #CHRXTRA,CNTLABELS,
    COU,
    #EXP,
    #LIBR, #LOG2BG,
    MINUS,
    OUTPATH,
    #PLOTLIB,
    PLUS,
    REGI,
    SHOWDISC,
    SPECIFIC,
    TSV,
    #UNSEL,
    UNSPCGAPS, UNSPECIFIC,
    )
from coalispr.resources.utilities import (
    thisfunc
    )

logger=logging.getLogger(__name__)


def _formatref(ref1, ref2):
    """Return formatted annotation.

    Parameters
    ----------
    ref1 : list
        List of strings for references overlapping sample coordinate on
        **PLUS** strand.
    ref2 : list
        List of strings for references overlapping sample coordinate on
        **MINUS** strand.
    maxl  : int
        Maximum length accepted for reference.
    """
    ref1_ = ", ".join(ref1) if ref1 else "-"
    ref2_ = ", ".join(ref2) if ref2 else "-"
    mid = ' : '
    stri = f"{ref1_}{mid}{ref2_}"
    return stri


def _annotate_loc(row, kind, ref):
    """Return formmatted annotation for a region used as index

    Parameters
    ----------
    row : dataframe with regions as index
    kind : str
        Kind of data, **SPECIFIC** (default) or **UNSPECIFIC**.
    ref : bool
        Include general **REFERENCE** annotations.
    """
    #segm = "2:127675-129525"
    try:
        segm = row[REGI]
    except KeyError:
        segm = row.name
    segmchr = segm.split(':')[0]
    segmedges = segm.split(':')[1].split('-')
    segm = (int(segmedges[0]), int(segmedges[1]))
    ref1, ref2 = ref_in_segment(segmchr, segm, kind, ref)
    return _formatref(ref1, ref2)


def annotate_clust_file(path, kind, ref, heading):
    """Return dataframe with annotated clusters read from file.

    Parameters
    ----------
    path : str
        Path to count file with segments and counts (after clustering).
    kind : str
        Kind of data, **SPECIFIC** (default) or **UNSPECIFIC**.
    ref : bool
        Include general **REFERENCE** annotations.
    heading : str
        Name of dataframe column with annotations.
    """
    heading = '' if not heading else heading
    df = pd.read_csv(path, sep='\t', header=None )
    df = df.rename(columns={0: REGI, 1: 'cluster'})
    df[heading] = df.copy().apply(
        lambda x: _annotate_loc(x, kind, ref), axis=1)
    #print(df.sort_values(by=['cluster','segm']))
    return df.sort_values(by=[REGI])


def annotate_count_frame(df, kind, ref, heading):
    """Return dataframe with annotations for counts in the input frame.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with segments and counts.
    kind : str
        Kind of data, **SPECIFIC** or **UNSPECIFIC**.
    ref : bool
        Include general **REFERENCE** annotations.
    heading : str
        Name of dataframe column with annotations.
    """
    df.insert(0,heading, df.copy().apply(
        lambda x: _annotate_loc(x,kind,ref), axis=1))
    return df


def annotate_libtotals(rdkind, strand, kind, ref, showdiscards, log2, sortval):
    """Annotate library counts

    Relevant file-titles: "{kind}{COU}_{strand}{TSV}".

    Parameters
    ----------
    rdkind : str
        One of **LIBR**, **UNIQ**, **COLLR**. Choose all (**LIBR**), only
        uniquely-mapped reads (**UNIQ**, leaving out repetitive sequences,
        **MULMAP**, like tRNA, rRNA or common transposons).
    strand: str
        One of {**ALL_COMBI**, **COMBI**, **MUNR**, **CORB**}
    kind: str
        Name determining kind of reads, **SPECIFIC** or **UNSPECIFIC**
        or **FRACTION**
    ref : bool
        Include general **REFERENCE** GTF for annotations (slow) if True.
    showdiscards : bool
        Include discarded samples.
    log2 : bool
        Use log2 scale if True.
    sortval : bool
        Sort table with respect to values, descending from highest if True.
    """
    nam = f"{rdkind}{COU}_{strand}"

    skipstrand = f"{strand} strands"
    xtr = '' if not showdiscards else ", plus unused samples"

    #reads = _get_labels()
    msg = (f"\nAnnotating {'log2 ' if (log2) else ''}total library "
        f"counts for {kind.lower()} {rdkind} reads for {skipstrand}{xtr}. ")
    if ref:
        msg += "General reference gtf is included for mRNA annotations (slow). "
    if sortval:
        msg += "Output is sorted for highest values... "
    print(msg)

    sep_ = " : "
    heading = f"{PLUS}{sep_}{MINUS}"

    if kind == SPECIFIC:
        df = load_count_table(nam, debug=0)
    elif kind == UNSPECIFIC:
        df = load_count_table(nam, use=UNSPECIFIC, usegaps=UNSPCGAPS, debug=0)
    # take log2 after adding 1 where sum is zero (log2 of 1 is 0)
    if log2:
        df = np.log2(df.where(df>0, 1)).round(3)
        nam += "_log2"
    nam += f"_annot_{kind.lower()}"
    if len(discarded()) > 0 or not showdiscards:
        df = drop_discarded(df)
    else:
        nam += f"_{SHOWDISC}"
    if ref:
        nam += "_ref"
    # add column with annotations and break apart for either strand
    df.insert(0,heading, df.copy().apply(
        lambda x: _annotate_loc(x, kind, ref), axis=1))
    df[[PLUS, MINUS]] = df[heading].str.split(pat=sep_, n=1, expand=True)
    df = df.drop(heading, axis=1)
    # sort on values
    if sortval:
        df = df.sort_values(by = get_positive(df), ascending=False)
        nam += "_sorted"

    opath = OUTPATH.joinpath(f"{nam}{TSV}")
    msg = f"\tTable saved as '{opath}'."
    print(msg)
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    df.to_csv(opath, sep="\t",
        quoting=csv.QUOTE_NONE, quotechar='"',escapechar='\\')
