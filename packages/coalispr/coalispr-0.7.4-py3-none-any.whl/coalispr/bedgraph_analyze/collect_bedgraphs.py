#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  collect_bedgraphs.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module for collecting data and configured experiment information."""
import logging
import pandas as pd
from pathlib import Path
from coalispr.resources.constant import (
    BASEDIR, BEDGRAPH,
    CAT_D, CAT_R, CATEGORY, CONDITION, CONFPATH,
    EXPFILE, EXPFILNAM,
    FILEKEY, FRACTION,
    GROUP,
    METHOD, MINUS, MINUSIN,
    PLUS,
    REFDIR, REFNDIRLEVEL,
    SHORT, SRCDIR, SRCFLDR, SRCNDIRLEVEL,
    TAG,
    UNIQ,
    )
from coalispr.resources.utilities import (
    joiner,
    thisfunc,
    )


logger = logging.getLogger(__name__)

def checkset(listofexps, omit=None):
    """In order to prevent duplication make sure that all input will be unique.

    Parameters
    ----------

    listofexperiments : list
        A list of experimental samples.

    Returns
    -------
    list
        A non-redundant list of experimental samples.
    """
    non_redundant = set(listofexps)
    if omit:
        non_redundant = set(listofexps).difference(set(omit))
    return list(non_redundant)


def _has_expected_cols(df):
    expected = {"FILEKEY": FILEKEY, "SHORT":SHORT, "CATEGORY":CATEGORY,
                "METHOD":METHOD, "FRACTION":FRACTION, "GROUP": GROUP,
                "CONDITION": CONDITION, }
    for const,col in expected.items():
        if not col in df.columns:
            raise SystemExit(f"\nSorry, program failed. Column '{const}' is "
            " not found in the experiment file (EXPFILE). \nConstants "
            f"{', '.join(expected.keys())} have values: '"
            f"{joiner().join(expected.values())}'. Any of these values is "
            f" expected as a column header in the EXPFILE, '{EXPFILNAM}').\n")
    return df


def label_frame():
    """Dataframe linking files by a filename-derived key to a short name.

    This is the start-dataframe. It defines abbreviated names for display
    (**SHORT**), their **CATEGORY**, etc.. and is built from a tabbed text file
    **EXPFILE** containing all details. Try to correct for errors in **EXPFILE**
    that easily occur, like spaces by themselves as a value in a group column.

    Returns
    -------
    pandas.DataFrame
        Dataframe of **EXPFILE** with **SHORT** as index.
    """
    global _expframe
    # whitespace, to include as non-value (na)
    space = ' '
    msg = f"Check '{EXPFILNAM}' describing samples, categories, groups ..."
    try:
        return _expframe
    except FileNotFoundError:
        raise SystemExit("Cannot load file with experiment description: \n"
            f"`{EXPFILE}`")
    except NameError:
        _expframe = pd.read_csv(EXPFILE, comment='#', sep='\t', dtype=str,
            skipinitialspace=True, na_values=space)
        # remove unwanted spaces, in column headers
        _expframe.columns = _expframe.columns.str.strip()
        # in column-values
        for col in _expframe.columns:
            _expframe[col] = _expframe[col].str.strip()
        # test expected columns
        _expframe = _has_expected_cols(_expframe)
        # use column of SHORT names as index
        _expframe = _expframe.set_index(SHORT, drop=False)
        return label_frame()
    except KeyError:
        msg += ("""

          Extra or missed tabs can interfere with its processing and required
          info is not found.
          """)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)


def get_categories_dict():
    """Returns dict for categories with **SHORT** names as keys."""
    try:
        return label_frame().set_index(SHORT).to_dict()[CATEGORY]
    except KeyError:
        msg = f"No heading '{SHORT}' or '{CATEGORY}' found in '{EXPFILE}'"
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")


def checkSRCDIR(src_dir, tag):
    """Returns path to main folder with folders containing data files."""
    try:
        p = Path(src_dir)
        if tag != None and tag != TAG:
            p = p.parent / (SRCFLDR + tag)
        if p.exists() and p.is_dir():
            return p
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        msg = f"Folder {p} not found"
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)


def get_experiments(category=None, method=None, fraction=None,
    plusdiscards=True):
    """Returns list of short names based on properties of experiments.

    Parameters
    ----------
    category : str or list
        Name or list of category item(s) as present in **EXPFILE**
    method : str or list
        Name or list of method(s) as given in **EXPFILE**
    fraction : str or list
        Name or list of fraction(s) as given in **EXPFILE**
    plusdiscards : bool
        Flag to indicate whether to include samples marked as a discard.

    Returns
    -------
    list
        A list of **SHORT** names representing the samples/experiments requested.
    """
    exps = label_frame()
    try:
        # all experimental files apart from CAT_D to be returned
        if not plusdiscards:
            todiscard = exps[CATEGORY] == CAT_D
            exps = exps[~todiscard]

        if method:
            if isinstance(method, str):
                exps = exps[ exps[METHOD] == method ]
            elif isinstance(method, list):
                exps = exps[ exps[METHOD].isin(method)]

        if fraction:
            if isinstance(fraction, str):
                exps = exps[ exps[FRACTION] == fraction ]
            elif isinstance(fraction, list):
                exps = exps[ exps[FRACTION].isin(fraction)]

        if not category:  # all experimental files to be returned together
            exps = exps[ exps[CATEGORY] != CAT_R ]
        elif category:
            if category and not isinstance(category, list):
                _category = [category]
            else:
                _category = category
            exps = exps[ exps[CATEGORY].isin(_category)]
    except KeyError as e:
        msg = (f"When collecting experiments {e} was not found.\n"
            f"Please check '{EXPFILE}' for expected presence of this category.")
        logging.debug(f"{__name__}.{thisfunc(0)}:{msg}")
        raise SystemExit(msg)
    explist = list(exps.index)
    #logging.debug(f"{__name__}.{thisfunc(1)}:{explist}")

    return explist


def _checkndir(ndirlevels):
    """Simplistic test for expected folder structure: stop proceedings.

    Parameters
    ----------
    ndirlevels : int (default: **SRCNDIRLEVEL** or **REFNDIRLEVEL**)
    """
    #print(f"ndirlevels={ndirlevels, REFNDIRLEVEL}")
    if not ndirlevels >= 0:
        msg = ("Sorry, something went wrong. Check folder structure as "
              f"configured in {CONFPATH}. \nFiles with extension '{BEDGRAPH}' "
               "are expected to be inside a directory corresponding to their "
              f"filename, {ndirlevels} steps below {BASEDIR}.")
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
        raise SystemExit(msg)


# Collect bedgraph files
# ----------------------
def collect_bedgraphs(tag, src_dir=SRCDIR, ndirlevels=SRCNDIRLEVEL,
        category=None):
    """Find file paths to bedgraphs and return as list.

    Parameters
    ----------
    tag : str (default: **TAG**)
    src_dir : str (default: **SRCDIR**)
        File path as string to main folder with folders containing data files.
    ndirlevels : int (default: **SRCNDIRLEVEL**)
        Number of folders in between **SRCDIR** and data files.
    category : str or list
        Name or list of category item(s) as present in **EXPFILE**.

    Returns
    -------
    dict, dict
        A tuple of dictionaries with **FILEKEY** items and paths to separate
        bedgraph files for **PLUS** - and **MINUS** strand data.
    """

    _checkndir(ndirlevels)
    p = checkSRCDIR(src_dir, tag)
    ext = BEDGRAPH
    # repeat /* for number of levels
    pattern = '**' + ndirlevels*'/*' if ndirlevels > 0 else '*'
    # generator; would still contain names with 'uniq'
    # `set` uses up generator
    exppaths = set(p.glob(pattern + ext))
    unqpaths = set(p.glob(pattern + UNIQ + "*" + ext))
    if not exppaths:
        print(src_dir) #SRCDIR)
        _checkndir(-1)
    if not unqpaths:
        usepaths = list(exppaths)
    else:
        if len(unqpaths) < len(exppaths):
            # only take the all-encompassing bedgraphs
            usepaths = list(exppaths-unqpaths)
        elif len(unqpaths) == len(exppaths):
            # possibly only uniq bedgraphs available and intended to be used.
            usepaths = list(unqpaths)
            msg = f"Only {UNIQ} bedgraph files found, {len(usepaths)} of them."
            print(msg)
            logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")

    return _collect_bedgraph_paths(usepaths, category)


def collect_references():
    """Find file paths to bedgraphs for reference data and return as list.

    Parameters
    ----------
    tag : str (default: **TAG**)
    refsdir : str (default: **REFDIR**)
        File path as string to main folder with folders containing reference
        data files.
    ndirlevels : int (default: **REFNDIRLEVEL**)
        Number of folders in between **SRCDIR** and data files.

    Returns
    -------
    dict, dict
        A tuple of dictionaries with **FILEKEY** items and paths to separate
        bedgraph files for the reference with **PLUS** - and **MINUS** strand
        data.
    """
    return collect_bedgraphs(tag=None, src_dir=REFDIR, ndirlevels=REFNDIRLEVEL,
        category=CAT_R)


def _collect_bedgraph_paths(exppaths, category):
    """Retrieve all bedgraphfilenames for use as columns in a DataFrame.

    Notes
    -----
        STAR can output uniq bedgraphs that should be treated separately.
        (not used)

    Parameters
    ----------
    exppaths : list
        A list of strings defining paths to data-files.
    category : str or list
        Name or list of category item(s) as present in **EXPFILE**.

    Returns
    -------
    dict, dict
        A tuple of dictionaries with **FILEKEY** items and paths to sepoarate
        bedgraph files with **PLUS** - and **MINUS** strand data.
    """
    explist = get_experiments(category)
    expfr = label_frame()[[FILEKEY, SHORT]].loc[explist]
    # sort files by plus vs minus (strands)
    # use strand 2 as this could also be called 'antisense' with 1 'sense'
    # allow for possibility that MINUS is not as wished, use given MINUSIN.
    ext2 = MINUSIN + BEDGRAPH
    #ext1 = PLUSIN + BEDGRAPH
    expfilepaths1 = [ path_ for path_ in exppaths
        if path_.name.endswith(BEDGRAPH) and not path_.name.endswith(ext2) ]
    expfilepaths2 = [ path_ for path_ in exppaths if path_.name.endswith(ext2) ]
    # strand-specific bedgraph data should be available:
    if not expfilepaths1 or not expfilepaths2:
        msg = (f"Sorry, no strand-specific '{BEDGRAPH}' files found. "
            "Bedgraph data is expected to be split into separate files for "
            f"{PLUS} and {MINUS} strands.")
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
        raise SystemExit(msg)

    # link filename-key to path/filenamefolder
    def paths1(df, column=FILEKEY):
        for path_ in expfilepaths1:
            if path_.parts[-2].startswith(df[FILEKEY]):
                return path_

    def paths2(df, column=FILEKEY):
        for path_ in expfilepaths2:
            if path_.parts[-2].startswith(df[FILEKEY]):
                return path_

    expfr = expfr.assign(
        graphs1 = expfr.apply(paths1, axis=1),
        graphs2 = expfr.apply(paths2, axis=1)
    )

    bgdict1 = expfr.graphs1.to_dict()
    bgdict2 = expfr.graphs2.to_dict()

    return bgdict1, bgdict2
