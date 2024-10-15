#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  references.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module for dealing with reference data."""
import logging
from coalispr.resources.constant import (
    EXPFILE,
    READDENS, REFERENCE,
    UNSPECLOG10,
    )
from coalispr.bedgraph_analyze.collect_bedgraphs import label_frame
from coalispr.bedgraph_analyze.store import retrieve_processed_files
from coalispr.resources.utilities import thisfunc

logger = logging.getLogger(__name__)

def retrieve_merged_reference():
    """Return merged reference data, organized per binned chromosome."""
    global _ref1, _ref2
    try:
        return _ref1, _ref2
    except NameError:
        _ref1, _ref2 = retrieve_processed_files('reference_merged',
            tag=None, notag=True)
    return _ref1, _ref2


def _corray():
    """Return density factors to correct corresponding reference signal."""
    if not READDENS:
        msg = (f"No correction of reference signals done by lack of factors."
               f"If needed, include a column READDENS (now: {READDENS}) in "
               f"the experiment file, '{EXPFILE}'."
               f"Values in this column are factors, of which one is set to 1, "
               "to 'normalize' signals of various references.")
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return 1
    exps = label_frame()[READDENS].dropna().astype(float)
    # max(dens, key = dens.get)
    refkey = exps.max()
    try:
        # [dens[refkey]/val for val in dens.values()]
        dens = refkey / exps
        return dens
    except ZeroDivisionError:
        msg = (f"Please correct experiment file\n'{EXPFILE}';\nrelative "
               f"'{READDENS}' cannot be 0.")
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return


def _equalize_references(ref1chr, ref2chr):
    """Correct for global differences in read density between samples.

    This is done by using the numbers provided in the experiment file, which
    have been determined by trial and error (say in a genome browser).

    Parameters
    ----------
    ref1chr, ref2chr : pandas.DataFrame, pandas.DataFrame
        **PLUS** and **MINUS** strand dataframes with raw RNA-seq signals for a
        chromosome.

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        Tuple of dataframes, for **PLUS** and **MINUS** strand of chromosome
        ``chrnam``, with transposed RNA-seq signals.
    """
    try:
        corr = _corray()
        return ref1chr.mul(corr), ref2chr.mul(corr)
    except AttributeError:
        pass
    except KeyError:
        return ref1chr, ref2chr
    except ValueError:
        msg = (f"Please correct experiment file\n'{EXPFILE}';\nrelative "
               f"'{READDENS}' only valid for '{REFERENCE}' entries.")
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")


def referencetrack(chrnam):
    """Return references separately to allow transposition.

    Parameters
    ----------
    chrnam : str
        Name of chromosome for which RNA-seq data to return.

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        Tuple of dataframes, for **PLUS** and **MINUS** strand of chromosome
        ``chrnam``, with transposed RNA-seq signals.
    """
    plus_ref, minus_ref = retrieve_merged_reference()
    ref1chr, ref2chr = _equalize_references(plus_ref.get(chrnam),
        minus_ref.get(chrnam))
    logging.debug(f"{__name__}.{thisfunc()}:\n equalized reference values for "
        f"chromosome: {chrnam}\n")
    return ref1chr, ref2chr


def filtered_referencetrack(chrnam, tag, specific=True):
    """Return transposed references linked to specified reads.

    Parameters
    ----------
    chrnam : str
        Name of chromosome for which filtered, transposed RNA-seq data to
        return.
    tag : str
        Flag **TAG** to indicate kind of aligned-reads to filter with,
        **TAGUNCOLL** or **TAGCOLL**.
    specific : bool
        Flag to indicate what kind of reads to return data for; when `True`,
        for **SPECIFIC** reads, when `False`, for **UNSPECIFIC** reads.

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        Tuple of dataframes, for **PLUS** and **MINUS** strand of chromosome
        ``chrnam``, with filtered and transposed RNA-seq signals.

    """
    if specific:
        plus_ref, minus_ref = retrieve_processed_files(
            f"reference_specific_{UNSPECLOG10}", tag)
        return  _equalize_references(plus_ref.get(chrnam),
                    minus_ref.get(chrnam))
    else:
        not_plus, not_minus = retrieve_processed_files(
            f"reference_unspecific_{UNSPECLOG10}", tag)
        return  _equalize_references(not_plus.get(chrnam),
                    not_minus.get(chrnam))
