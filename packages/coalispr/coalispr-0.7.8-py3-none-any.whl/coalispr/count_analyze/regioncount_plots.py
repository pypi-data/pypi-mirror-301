#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  regioncount_plots.py
#
#  Copyright 2023-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module to plot count comparisons for a given region.

   Relevant folders:

   ``tsvpath/{REGI}_{READCOUNTS}_{TAGBAM}-bam/{REGI}_chrnam_nt1-nt2/``

"""
import logging
import matplotlib as mpl

from coalispr.bedgraph_analyze.experiment import (
    for_group,
    )
from coalispr.count_analyze.load_countfile import (
    split_readlengths_index,
    )
from coalispr.count_analyze.panel_plotters import (
    LengthPanelPlotter,
    Log2RegionCountPanelPlotter,
    RegionCountPanelPlotter,
    )
from coalispr.resources.constant import (
    COLLR,
    EXP,
    LIBR, LOG2BG,
    MINUS, MULMAP,
    PERC, PLOTLEN, PLOTLIB, PLOTSTRT, PLUS,
    REGI,
    SAMPLE, SHOWDISC,
    UNIQ,
    )
from coalispr.resources.plot_utilities import (
    capit_label,
    get_context,
    init_sns,
    no_titles,
    )
from coalispr.resources.utilities import (
    doneon,
    get_skip,
    get_ylabel,
    percentaged,
    remove_odds,
    thisfunc,
    )

logger = logging.getLogger(__name__)


init_sns()

posslabels = {
        LIBR            : capit_label(LIBR),
        UNIQ            : capit_label(UNIQ),
        MULMAP + LIBR   : capit_label(MULMAP),
        COLLR           : COLLR,
        UNIQ + COLLR    : f"{capit_label(UNIQ)} {COLLR}",
        MULMAP + COLLR  : f"{capit_label(MULMAP)} {COLLR}",
        }

def _strd(strand):
        if strand == PLUS: return ":1"
        elif strand == MINUS: return ":-1"
        else: return ""


@mpl.rc_context(get_context()) #-cf; see countfile_plots.compare_libtotals; -lc
def plot_regioncounts(cntregion, countfram, group, strand, notitles, log2,
    showdiscards):
    """Compare counts for **LIB**, cDNA (**COLLR**) and associated
    **UNIQ** and **MULMAP** reads for a region in given samples.

    Relevant file-titles:

    ``{LIBR | UNIQ | COLLR | UNIQ+COLLR}{COU}{_chrnam_nt1-nt2}TSV``.

    But not read from file; direct input as dataframe for processing.

    .. table::

       +------------------------------------+------------+------+----------+
       | label                              |     a1_1   | ...  |    wt_2  |
       +====================================+============+======+==========+
       | library                            |   3006.92  | ...  |   984.49 |
       +------------------------------------+------------+------+----------+
       | uniq                               |   2990.0   | ...  |   820.0  |
       +------------------------------------+------------+------+----------+
       | cDNA                               |   1868.74  | ...  |   632.32 |
       +------------------------------------+------------+------+----------+
       | uniqcDNA                           |   1857.0   | ...  |   619.0  |
       +------------------------------------+------------+------+----------+
       | multimapperlibrary                 |  49720.16  | ...  | 25251.54 |
       +------------------------------------+------------+------+----------+
       | multimappercDNA                    |   1399.52  | ...  |   539.77 |
       +------------------------------------+------------+------+----------+

    Parameters
    ----------
    cntregion : str
        String describing counted region, e.g. "6:56000-78900".
    countfram : pd.DataFrame
        Dataframe with samples in columns and counts in rows with indices like
        "library".
    group : str
        Name determining grouping of samples, either **CATEGORY**, **METHOD** or
        **FRACTION**
    strand : str
        Strand(s) with the counted reads.
    notitles : bool
        Flag to set display of figure title on graph.
    log2 : bool
        Use log2 scale if True.
    showdiscards : bool
        Show numbers for unused samples.

    """
    labl = SAMPLE  #countfram.index.name #.split('_',1)[0]
    countframlabls = list( countfram.index)
    countfram[labl] = [ posslabels[x] for x in countframlabls ]
    cntfram = countfram.set_index(labl, drop=True).T


    #print(cntregion)
    print(cntfram)
    #return
    numbers = list(cntfram.columns)
    #print(numbers)
    explan = (f"{', '.join(numbers)}")
    fcie = RegionCountPanelPlotter if not log2 else Log2RegionCountPanelPlotter

    rlessx = 1 # reduction factor for setting labels in less_xlabel; default
    cols = list(cntfram.index)

    msg = (f"\nShowing {'log2' if (log2) else ''} "
        f"counts of {explan} reads for {strand} strand(s) of {cntregion} "
        f"{len(cols)} samples, grouped by {group.lower()}. ")
    if showdiscards:
        msg += "Discards are included."

    print(msg)
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    nams, lens, sampls = for_group(group, showdiscards, cols)

    #print(nams, lens, sampls)


    xlabel = PLOTLIB
    legtitl = f"For region {cntregion}{_strd(strand)}"
    ylabel = "Sample libraries"

    suptitl = (f"Counts for {cntregion}.")
    suptitl = no_titles(suptitl, notitles)
    wintitl = (f"{'' if not showdiscards else SHOWDISC+' '}counts for {strand}"
        f" strands over region {cntregion} {len(cols)} samples by {group} {EXP}"
        f" log2bg{LOG2BG} skip{get_skip()}"
        f"{' notitles ' if notitles else ' '}{doneon()}")
    wintitl = remove_odds(wintitl).lower()
    ftitles = {'legtitl':legtitl,'suptitl':suptitl, 'wintitl':wintitl,
        'xlabel':xlabel,'ylabel':ylabel, 'rlessx':rlessx}

    fcie(group, nams, lens, sampls, cntfram, numbers, ftitles,
            ).plot_panels()


@mpl.rc_context(get_context()) #see countfile_plots.compare_exp_lengths; -ld
def plot_regionlengths(cntregion, lengthframs, group, readlen, strand, notitles,
    showdiscards):
    """Obtain read-length distribution for a region in separate library samples.

    Relevant file-titles:

    ``{LIBR | UNIQ | COLLR | UNIQ+COLLR}_[RLENCOUNTS}{_chrnam_nt1-nt2}TSV``.

    But not read from file; direct input as dict of dataframes for processing.

    Parameters
    ----------
    cntregion : str
        String describing counted region, e.g. "6:56000-78900".
    lengthframs : dict
        Dictionary of ``label: counter.get_lencount_frame()``\ s with label in
        [ **LIBR, UNIQ, COLLR, UNIQ+COLLR** ] depending on calling function.
    group : str
        Name determining grouping of samples, **CATEGORY**, **METHOD** or
        **FRACTION**
    readlen : tuple
        Limits for read lengths to include.
    strand : str
        Strand(s) with the counted reads.
    notitles : bool
        Flag to set display of figure title on graph.
    showdiscards : bool
        Show discarded samples.

    """
    numbers = [PLOTLEN, PLOTSTRT]
    ltitl = f"{PLOTSTRT} (for {cntregion}{_strd(strand)})"
    fcie = LengthPanelPlotter
    rlessx =1 #factor to reduce label no (see plot_utilities.less_xlabels)
    xtr = '' if not showdiscards else " plus unused samples"

    for nam, df in lengthframs.items():
        ylabel = f"{PERC} {get_ylabel(nam, strand=strand, spaces=4)}"
        #print(nam)
        df = percentaged(df)
        df = split_readlengths_index(df)
        df = df[ (df[PLOTLEN].astype(int) >= readlen[0])
               & (df[PLOTLEN].astype(int) <= readlen[1]) ]
        #print(df)

        cols = list(df.columns)
        cols.remove(PLOTLEN)
        cols.remove(PLOTSTRT)

        msg = (f"\nShowing {nam} length distributions for {strand} strands of "
            f"{REGI.lower()} {cntregion} as bar graphs for {len(cols)} "
            f"separate libraries, grouped by {group.lower()}{xtr}.")
        print(msg)
        #msg += f"\n{get_string_info(df)}"
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

        nams, lens, sampls = for_group(group, showdiscards, cols)
        #print(nams, lens, sampls)

        suptitl = (f"Separate {nam} length distributions for {cntregion}:"
            f"\ngrouped by {group.lower()}.")
        suptitl = no_titles(suptitl, notitles)
        wintitl = (f"{'' if not showdiscards else f'{SHOWDISC} '}"
            f"separate {nam} lengths for {strand} strands {cntregion} of "
            f"{len(cols)} samples by {group} log2bg{LOG2BG} skip{get_skip()}"
            f"{' notitles ' if notitles else ' '}{doneon()}")
        wintitl = remove_odds(wintitl).lower()

        ftitles = {'legtitl': ltitl, 'suptitl':suptitl, 'wintitl':wintitl,
                   'xlabel':numbers[0],'ylabel':ylabel, 'rlessx':rlessx,
                    }
        fcie(group, nams, lens, sampls, df, numbers, ftitles).plot_panels()
