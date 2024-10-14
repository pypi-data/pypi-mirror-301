#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  load_countfile.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module to obtain dataframes from count files."""
import logging
import pandas as pd

from coalispr.bedgraph_analyze.process_bamdata import (
    count_folder,
    )
from coalispr.resources.constant import (
    ALL,
    BCO,
    LIBR, LOG2BG,
    MULMAP,
    PLOTINTRLEN, PLOTLEN, PLOTPERC, PLOTSTRT,
    SPECIFIC,
    TAGCOLL, TAGUNCOLL, TSV,
    UNIQ, UNSPECIFIC, UNSPCGAPS, UNSPECLOG10, USEGAPS,
    )
from coalispr.resources.utilities import (
    get_string_info,
    get_tsvpath,
    percentaged,
    thisfunc,
    )

logger = logging.getLogger(__name__)


def _multimap_table(name, use, bam, segments, overmax, maincut, usegaps,
    index_col, debug):
    """Get subset of counts for **MULMAP** reads as library, introns or cDNAs.
    Subtract **UNIQ** frame from frame with total values.

    .. table::

    +----+-------------------+------------+-----------------+-----------+
    | lx | Start name        | Total.sub( | Uniq )          | replace   |
    +====+===================+============+=================+===========+
    | 1. | MULMAP+LIBR       | LIBR       | UNIQ            | len(LIBR) |
    +----+-------------------+------------+-----------------+-----------+
    | 2. | MULMAP+COLLR      | COLLR      | UNIQ+COLLR      | 0         |
    +----+-------------------+------------+-----------------+-----------+
    | 4. | MULMAP+INTR       | INTR       | UNIQ+INTR       | 0         |
    +----+-------------------+------------+-----------------+-----------+
    | 5. | MULMAP+INTR+COLLR | INTR+COLLR | UNIQ+INTR+COLLR | 0         |
    +----+-------------------+------------+-----------------+-----------+

    """
    debug += debug
    totnam = name[len(MULMAP):]
    # total counts for reads/cDNAs with multimappers have fractions
    # only unique reads will be Int64
    rnd = 2
    typ = float
    if name.startswith(MULMAP+LIBR): # create appropriate filename
        namuniq = UNIQ+totnam[len(LIBR):]
    else:
        namuniq = UNIQ+totnam

    logging.debug(f"{__name__}.{thisfunc(debug)}:\n'{totnam}' sub "
        f"'{namuniq}'.")

    dftot = load_count_table(totnam, use, bam, segments, overmax, maincut,
                usegaps, index_col, debug)
    dfuniq = load_count_table(namuniq, use, bam, segments, overmax, maincut,
                usegaps, index_col, debug)
    df = dftot.sub(dfuniq, fill_value=0 ).round(rnd).astype(typ)
    logging.debug(f"{__name__}.{thisfunc(debug)}:\n{get_string_info(df)}")
    return df


def load_count_table(name, use=SPECIFIC, bam=TAGCOLL, segments=TAGUNCOLL,
    overmax=LOG2BG, maincut=UNSPECLOG10, usegaps=USEGAPS, index_col=0, debug=0):
    """Retrieve count tables with given keywords in the folder/filename.

    The count files come from ``coalispr.bedgraph_analyze.process_bamdata``.

    Parameters
    ----------
    name : str
        Name of particular count file to retrieve.
    use : str (default: **SPECIFIC**)
        What type of counted reads to use, i.e. **SPECIFIC** or **UNSPECIFIC**.
    bam : str (default: **TAGCOLL**)
        Flag to indicate sort of aligned-reads, **TAGCOLL** or **TAGUNCOLL**,
        used to obtain bam-alignments.
    segments : str (default: **TAGUNCOLL**)
        Flag to indicate sort of aligned-reads, **TAGCOLL** or **TAGUNCOLL**,
        used to obtain segment definitions.
    overmax : int (default: **LOG2BG**)
        Exponent to set threshold above which read signals are considered;
        part of folder name with stored count files.
    maincut : float (default: **UNSPECLOG10**)
        Exponent to set difference between **SPECIFIC** and **UNSPECIFIC**
        reads; part of folder name with stored count files.
    usegaps : int (default: **USEGAPS**)
        Region tolerated between peaks of mapped reads to form a contiguous
        segment; part of folder name with stored count files.
    indexcol : int
        Number of index-column in table loaded from csv file.
    debug : int
        Level to obtain relevant function calling this support function.

    Returns
    -------
        pandas.DataFrame

    """
    name = name.lower()
    # check mappers; only MULMAP needs to be dealt with = ALL-UNIQ
    if name.startswith(MULMAP):
        return _multimap_table(name, use, bam, segments, overmax, maincut,
            usegaps, index_col, debug)
    if name.startswith(UNIQ+LIBR):
        name = UNIQ + name[len(UNIQ+LIBR): ]

    use_folder = count_folder(use, bam, segments, overmax, maincut, usegaps)
    p = get_tsvpath()

    try:
        pexp = p.joinpath(use_folder, name+TSV)
        n=debug + 1
        logging.debug(f"Called by (level = {n}) {__name__}.{thisfunc(n)}")
        logging.debug(f"{__name__}.{thisfunc()}:\nCount file name: {pexp}")
        return pd.read_csv(pexp, comment="#",sep="\t",index_col=index_col)
    except IndexError as e:
        msg = ("Sorry, no count files found; \n (figures can rely on both "
              f"{SPECIFIC} and {UNSPECIFIC} count-files).")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}\n{e}")
        raise SystemExit(msg)
    except FileNotFoundError:
        msg = (f"Sorry, no such file '{name+TSV}' or no storage folder "
            f"\n\t'{use_folder}'.")
        raise SystemExit(msg)


def load_lengths_table_perc(name, use, debug):
    """Retrieve lengthcounts from ``coalispr.bedgraph_analyze.process_bamdata``
    as percentages for given kind of reads.

    Parameters
    ----------
    name : str
        Name of particular count file to retrieve.
    use : str (default: **SPECIFIC**)
        What type of counted reads to use, i.e. **SPECIFIC** or **UNSPECIFIC**.
    debug : int
        Level to obtain relevant function calling this support function.

    Returns
    -------
    pandas.DataFrame
        Dataframe with percentaged counts for read-lengths.

    """
    debug += 1
    if use==UNSPECIFIC:
        leng_df = load_count_table(name, use=UNSPECIFIC, usegaps=UNSPCGAPS,
            debug=debug)
    else:
        leng_df = load_count_table(name, use=SPECIFIC, debug=debug)
    return percentaged(leng_df)


def load_bin_table_perc(name, use, debug):
    """Retrieve bin-counts from ``coalispr.bedgraph_analyze.process_bamdata``
    as percentages for given kind of reads.
    """
    debug += 1
    if not BCO in name:
        raise SystemExit("Not a bin-count file")
    if use==UNSPECIFIC:
        bin_df = load_count_table(name, use=UNSPECIFIC, usegaps=UNSPCGAPS,
            index_col=[0,1,2], debug=debug)
    else:
        bin_df = load_count_table(name, use=SPECIFIC, index_col=[0,1,2],
            debug=debug)
    return percentaged(bin_df)


def get_freq_frame(name, use, debug, idx=PLOTINTRLEN, allc=PLOTPERC):
    """Get frame with distribution for index ``idx`` and column ``allc``.

    Parameters
    ----------
    name : str
        Name of particular count file to retrieve.
    use : str
        What type of counted reads to use, i.e. **SPECIFIC** or **UNSPECIFIC**.
    idx : str
        Name of index column, **PLOTINTRLEN** for lengths (introns) or
        **PLOTFREQ** for number of hits (multimappers).
    allc : str
        Name of column with values to be shown, **PLOTINTR** for lengths or
        **PLOTMMAP** for multimappers

    Returns
    -------
    pandas.DataFrame
        Dataframe with frequencies for lengths or multimappers.

    """
    debug += 1
    df = load_lengths_table_perc(name,  use=use, debug=debug)
    # set index name; get column from index
    df.index.names = [idx]
    df.reset_index(inplace=True)
    try:
        for i in df.columns:
            if ALL in i:
                df = df.rename(columns={i: allc})
    except KeyError:
        pass
    return df


def split_readlengths_index(df):
    df[PLOTSTRT] = df.index.str.split(pat='_').str.get(0)
    df[PLOTLEN] = df.index.str.split(pat='_').str.get(1)
    df.reset_index(drop=True, inplace=True)
    try:
        for i in df.columns:
            if ALL in i:
                df = df.rename(columns={i: PLOTPERC})
    except KeyError:
        pass
    return df


def get_readlengths_frame(name, use, debug):
    """Add columns **PLOTSTRT**, **PLOTLEN** to frame with read lengths.

    Parameters:
    name : str
        Name of file to load.
    use : str
        Which kind of reads to use, **SPECIFIC** or **UNSPECIFIC**.
    debug : int
        For debugging: the number of levels calling function is separated.
    """
    debug += 1
    df = load_lengths_table_perc(name, use=use, debug=debug)
    return split_readlengths_index(df)
