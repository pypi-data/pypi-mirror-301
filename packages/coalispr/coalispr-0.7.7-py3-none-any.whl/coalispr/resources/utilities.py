#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  utilities.py
#
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
import pandas as pd
import io
import logging
import time
import functools
import string
import sys

from datetime import date
from pathlib import Path
from coalispr.resources.constant import (
    BINN,
    BINSTEP,
    CHRXTRA, CNTLABELS, COMBI,
    MINUS, MIRNAPKBUF,
    PLUS,
    SAVETSV,
    STOREPATH,
    )

"""Functions used in many other modules."""
logger=logging.getLogger(__name__)


def bins_sum(df, level=BINN):
    """Sum bin-values to get bin totals.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with bins that constitute a ``level`` to be converted.
    level : str
        Column header with indices to be grouped (default=**BINN**).

    Returns
    -------
    pandas.DataFrame
    """
    return df.groupby(level=level, sort=False).sum(numeric_only=True)


def chrom_region(chrnam, region):
    """Create label for chromosome region.

    Parameters
    ----------
    chrnam: str
        Chromosome name.
    region: tuple
        Tuple of coordinates.
    """
    return f"{chrnam}:{region[0]}-{region[1]}"


def chrxtra():
    """Check for presence extra DNA and annotations."""
    if CHRXTRA:
        return CHRXTRA
    else:
        return "(No extra data to display; unused)"


def clean_dict(adict):
    """Remove empty items from a dictionary.

    Parameters
    ----------
    adict : dict
       Dictionary
    """
    return {k:v for k,v in adict.items() if v}


def doneon():
    """Return date of function called (for saving files)."""
    return date.today()


def get_skip():
    """Provide a value of fragment size skipped during counting,
    which depends on **BINSTEP** and **MIRNAPKBUF**.

    Returns
    -------
    int
        A value representing an extra margin to expand read segment with a
        single peak beyond 0.
    """
    return int(2*BINSTEP*MIRNAPKBUF) if MIRNAPKBUF else BINSTEP


def get_string_info(df):
    """Return a string for logging info, bypassing standard out.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to get info for.
    """
    buff = io.StringIO()
    df.info(buf=buff)
    return buff.getvalue()


def get_tsvpath():
    """Return location of folder with **TSV** files"""
    tsvpath = Path(STOREPATH).joinpath(SAVETSV)
    return tsvpath


def get_ylabel(label, strand=COMBI, spaces=0):
    """Return formatted label for y-axis of count plots.

    Parameters
    ----------
    label : str
        Read kind name to retrieve a label for configured in **CNTLABELS**.
    strand : str
        One of **COMBI**, **MUNR** or **CORB** to indicate strand counted
        reads map to.
    spaces : int
        Number of spaces to start second line with.
    """
    spac =  spaces*' '
    strd = "strand" if strand in [MINUS,PLUS] else "strands"
    return f"{CNTLABELS[label]}\n{spac}({strand.lower()} {strd})"


def is_all_zero(df):
    """Is this a dataframe with only 0 values?

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to get info for.

    Returns
    -------
    bool
        Flag to indicate whether all values are 0.
    """
    return (df[df.columns].sum()==0).all()

def joinall(labels, conn = "', '"):
    """Return string of words from list or dict of labels.

    Parameters
    ----------
    labels : list or dict
        List/Dictionary of lists of words to be joined.
    conn : str
        Connector linking the words from labels.
    """

    def listlabels(labls,conn):
        return conn.join( [ labl for labl in labls ] )


    if isinstance(labels, list):
        return listlabels(labels,conn)
    elif isinstance(labels, dict):
        return conn.join( [ f"{labl}: {listlabels(val, ', ')}"
            for labl, val in labels.items() ] )


def joiner(symb=None):
    """Quote list-items when joined to string. Add start and end ' to calling
    format function {no control of '/" when using 'repr' by including !r}."""
    joiner = f"', {symb} '" if symb else "', '"
    return joiner


def merg(df1, df2):
    """Merge bedgraphs for each chr on intervals with hits.

    All rows/columns need to be combined; this creates duplicate columns with
    adapted names when non-unique columns are merged.

    Parameters
    ----------
    df1, df2 : pandas.DataFrame
        Dataframes to merge

    Returns
    -------
    pandas.DataFrame
        Merged dataframe.
    """
    try:
        df3= pd.merge(df1,df2, left_index=True, right_index=True, how='outer')
        return df3
    except TypeError as e:
        logger.debug(f"{__name__}.{thisfunc(1)}:\n{e}")
        raise SystemExit("Dataframe merge impossible \n"
            "(for details see the log).")


def percentaged(df):
    """Turn dataframe values into percentages of column totals.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with raw counts

    Returns
    -------
    pandas.DataFrame
    """
    sumcols = df.sum(axis=0)
    df2 = 100*(df.div(sumcols))
    return df2


def remove_odds(termodds):
    """Prevent spaces or odd symbols in filename string.

    Parameters
    ----------
    termodds : str
        String with possibly symbols or spaces in filename.

    Returns
    -------
    str
        Lower case name without odds; not to be confused with extension.
    """
    accepted = string.ascii_letters + string.digits + '_-'
    term = termodds.lower()
    for odd in term:
      if odd not in accepted:
          term = term.replace(odd,'_')
    return term


def replace_dot(termdot):
    """Remove dots from file name.

    Parameters
    ----------
    termdot : str
        String with possibly dots ('.') in filename (excluding extension).

    Returns
    -------
    str
        Name without dot(s); not to be confused with extension.
    """
    return termdot.replace(".","-") if "." in termdot else termdot


def replacelist(linestring, names_old_new):
    """Replace sections in a string, pathname, print line etc.

    Parameters
    ----------
    linestring : str
        String with particular sections to be replaced.

    names_old_new : list of tuples
        Contents of listed tuples: (search-string, replacement).

    Returns
    -------
    str
        String after replacement.
    """
    for item in names_old_new:
        # this is for text; when bytes would be required use:
        #linestring = linestring.replace(item[0].encode(), item[1].encode())
        linestring = linestring.replace(item[0], item[1])
    return linestring


def replacelist_list(listofitems, names_old_new):
    """Replace items in a list.

    Parameters
    ----------
    listofitems : list
        List with particular items to be changed.

    names_old_new : list of tuples
        Contents of listed tuples: (search-string, replacement).

    Returns
    -------
    list
        List with items including those that have been replaced.
    """
    dictnams = {item[0]: item[1] for item in names_old_new}
    for k,v in dictnams.items():
        idx = listofitems.index(k)
        listofitems[idx] = v
    return listofitems


def thisfunc(n=0):
    """Return name of current or calling function for logging.

    from:
    https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback

    https://docs.quantifiedcode.com/python-anti-patterns/correctness/assigning_a_lambda_to_a_variable.html

    https://docs.quantifiedcode.com/python-anti-patterns/correctness/accessing_a_protected_member_from_outside_the_class.html

    Parameters
    ----------
    n : int
        For current func name, specify 0 or no argument.
        For name of caller of current func, specify 1.
        For name of caller of caller of current func, specify 2. etc.

    Returns
    -------
    str
        Name of function containing call.
    """
    return sys._getframe(n + 1).f_code.co_name


def timer(func):
    """Print the time needed to run the decorated function.
    from: https://realpython.com/primer-on-python-decorators/
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        showtime = ""
        if run_time > 3600:
            showtime = f"{run_time/3600:.2f} hrs"
        elif run_time < 60:
            showtime = f"{run_time:.2f} secs"
        else:
            showtime = f"{run_time/60:.2f} min"

        msg = f"Finished {func.__name__!r} in {showtime}\n"
        logging.debug(msg)
        return value

    return wrapper_timer
