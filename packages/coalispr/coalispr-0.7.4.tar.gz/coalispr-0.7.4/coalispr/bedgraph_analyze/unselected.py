#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  unselected.py
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module for dealing with unselected reads retrieved from unspecific data."""
import logging
import pandas as pd
from pathlib import Path
from coalispr.bedgraph_analyze.process_bedgraphs import(
    bin_bedgraphs,
    _get_todo_list,
    )
from coalispr.bedgraph_analyze.genom import chroms
from coalispr.bedgraph_analyze.process_bamdata import (
    bedgraphs_from_xtra_bamdata,
    )
from coalispr.bedgraph_analyze.store import (
    get_unselected_folderpath,
    store_chromosome_data,
    retrieve_merged_unselected,
    retrieve_processed_files,
    )
from coalispr.resources.constant import (
    BEDGRAPH,
    INMAPCOLL, INMAPUNCOLL,
    MINUS,
    PLUS, PRGNAM,
    SAMPLE, SAVETSV, SPECIFIC, STOREPATH,
    TAGCOLL, TOTALS, TOTINPUT, TSV,
    UNSPECIFIC,
    )

from coalispr.resources.utilities import (
    merg,
    thisfunc,
    timer,
    )

logger = logging.getLogger(__name__)

'''
def _get_folderpath(kind,tag):
    """Return path to folder with written bam files for unselected reads.

    Parameters
    ----------
    kind : str (default: **UNSPECIFIC**)
        Flag to indicate kind of specified reads to analyze, either specific or
        unspecific (default) for retrieving reads adhering to characteristics,
        when known, of specific RNAs

    tag : str
        Flag **TAG** to indicate ``kind`` of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**. Comes from counted bam files, which -for efficiency
        reasons- could be expected to be containing collapsed reads
        (**TAGCOLL**).
    """
    kind_ = kind.lower()
    bampath = Path(STOREPATH).joinpath(SAVEBAM)
    overmax_ = 2**LOG2BG
    pattern = (f"{kind_}_{READCOUNTS}_{tag}-bam_*overmax{overmax_}_unspec"
               f"{UNSPECLOG10}_usegaps{UNSPCGAPS}")
    pattern = replace_dot(pattern)
    folderpath = set(bampath.glob(pattern))
    if folderpath == None or len(folderpath) == 0:
        msg=(f"Stopping .. (No bam-files found with:\n  '{pattern}')")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return False
    # take first item as valid path
    folderpath = list(folderpath)[0]
    return  folderpath
'''

def _normalize(frames1, frames2, tag):
    """Create RPM values for raw bedgraph-data based on total mapped reads.

    Normally RPM output is based on total input, which -for unselected reads-
    is fairly low and would produce signals that are too high and not
    providing an indication of the relevance of these reads.

    Parameters
    ----------
    frames1, frames2 : dict, dict
        Dicts with short name as key and as values, a dict with **PLUS** or
        **MINUS** stranded info in dataframes.

    tag : str
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**. Comes from counted bam files, which -for efficiency
        reasons- could be expected to be containing collapsed reads
        (**TAGCOLL**).

    Returns
    -------
    dict1, dict2
        RPM-based frames1, frames2
    """
    # column name to be expected for frame with total input counts
    col = INMAPCOLL if tag == TAGCOLL else INMAPUNCOLL

    def get_inputcounts():
        """Get dataframe with total input counts from file"""
        tsvpath = Path(STOREPATH).joinpath(SAVETSV,TOTINPUT)
        if not tsvpath.is_dir():
            msg=("Make sure total raw-counts (-rc) have been obtained from "
                 "alignment files (see ``countbams -h``); stopping...")
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            raise SystemExit(msg)

        inputtots = tsvpath.joinpath(f"{TOTALS}_{tag}{TSV}")
        try:
            return pd.read_csv(inputtots, sep='\t', usecols=[SAMPLE, col],
            index_col=SAMPLE)
        except:
            msg = f"No correct file found at '{inputtots}'; stopping ..."
            #msg += "\nHave column headers changed since last raw-input-count?"
            logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
            raise SystemExit(msg)

    dftots = get_inputcounts()
    #print(dftots)

    def rpm_dict(dct, tots):
        """Return a dict of chromosome names with dataframes of RPM values

        dct : dict
            Dictionary of chromosomes and counts
        tots : int
            Total counts.
        """
        rpmdict = {}
        for chrnam in chroms():
            df = dct[chrnam]
            rpmdict[chrnam] = df.div(tots, axis=0).mul(1000000, axis=0)
        return rpmdict

    rpmframes1, rpmframes2 = {}, {}
    for frameset in [[frames1,rpmframes1], [frames2,rpmframes2]]:
        #print(frameset[0][0:3])
        for nam in frameset[0].keys():
            #nam = 'u_<key>' or 's_<key>' with <key>:total in dftots frame
            inputtot = dftots.loc[nam[2:]][col]
            msg = nam, nam[2:], inputtot
            #print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            dct = frameset[0][nam]
            frameset[1][nam] = rpm_dict(dct, inputtot)
    #print(rpmframes2)

    return rpmframes1, rpmframes2


def _bin_unsel_bedgraphs(bedgraphdict1, bedgraphdict2, tag, force):
    """Convert bedgraph files to binned and then pickled data with common index.

    Output is stored in folder with **STOREPATH** and **STOREPICKLE**.

    Parameters
    ----------
    bedgraphdict1 : dict
        Dictionary with **PLUS** data.
    bedgraphdict2 : dict
        Dictionary with **MINUS** data.
    tag : **TAGCOLL** or **TAGUNCOLL**
        Type of data to bin.
    """
    saveas = 'unselected_data'
    if force:
        plus_frames, minus_frames = {}, {}
    elif not force:
        plus_frames, minus_frames = retrieve_processed_files(saveas, tag=tag,
            notag=False)

    todo = _get_todo_list(bedgraphdict1.keys(),plus_frames.keys())
    if len(todo) == 0:
        return
    for name in todo:
        msg = f'bin_bedgraphs for {PLUS}-strand {name}'
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        plus_frames[name] = bin_bedgraphs(bedgraphdict1[name],name)
    for name in todo:
        msg = f'bin_bedgraphs for {MINUS}-strand {name}'
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        minus_frames[name] = bin_bedgraphs(bedgraphdict2[name],name)

    # normalize to total input counts (to get 'honest' values for 'unselection')
    plus_frames, minus_frames = _normalize(plus_frames, minus_frames, tag)
    store_chromosome_data(saveas, plus_frames, minus_frames, notag=False,
        tag=tag)


@timer
def merge_unsel(tag, force, tee=False):
    """Unselect bedgraphs are combined but kept separate from the data.

    Parameters
    ----------
    tag : str
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**.
    tee : bool
        Flag defining to return dataframes for immediate use (storing them does
        not allow for this).

    Returns
    -------
    None
        When tee is `False`; print message upon completion of function.
    dict, dict
        When tee is `True`, dicts, one for each strand, with dataframes, one
        for each chromosome, with merged data for reference samples.
    """
    # check whether it has been done before
    unsplus, unsminus = retrieve_merged_unselected()
    if not tee and unsplus != {} and unsminus != {} and not force:
        msg = "Merged unselected dataframes available!"
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return
    if force:
       unsplus, unsminus = {},{}

    # merge unselected data
    mergs1all, mergs2all = {}, {}
    try:
        unsplus_data, unsminus_data = retrieve_processed_files('unselected_data',
            tag=tag, notag=False)
        unskeys = list(unsplus_data.keys())
        for chrnam in chroms():
            mergs1, mergs2 = {}, {}
            mergs1[chrnam] = unsplus_data.get(unskeys[0])[chrnam]
            mergs2[chrnam] = unsminus_data.get(unskeys[0])[chrnam]
            for exp in range(1, len(unskeys)):
                mergs1[chrnam] = merg(
                    mergs1[chrnam],
                    unsplus_data.get(unskeys[exp])[chrnam],
                    )
                mergs2[chrnam] = merg(
                    mergs2[chrnam],
                    unsminus_data.get(unskeys[exp])[chrnam],
                    )
            mergs1all[chrnam] = mergs1[chrnam].fillna(0).round(2)
            mergs2all[chrnam] = mergs2[chrnam].fillna(0).round(2)
        store_chromosome_data('unselected_merged', mergs1all, mergs2all, tag=tag,
            notag=False)
        if tee:
            return mergs1all, mergs2all
    except TypeError as e: # no processed files found
        print(e)
        pass
    except IndexError as i:
        print(i)
        pass


@timer
def process_unselected(kind=UNSPECIFIC, tag=None, force=False):
    """Retrieve extra bamfiles, if any and prepare them for common analysis.

    Parameters
    ----------
    kind : str (default: **UNSPECIFIC**)
        Flag to indicate kind of specified reads to analyze, either specific or
        unspecific (default) for retrieving reads adhering to characteristics,
        when known, of specific RNAs
    tag : str
        Flag **TAG** to indicate ``kind`` of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**. Comes via **TAGBAM** from counted bam files, which -for
        efficiency reasons- is set to collapsed reads (**TAGCOLL**).

    """
    if kind == SPECIFIC:
        msg=(f"{PRGNAM} not set up to process 'unselected' reads from {kind} "
              "data, stopping..")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)

    tag = TAGCOLL if tag == None else tag
    bampath = get_unselected_folderpath(kind, tag)
    if not bampath:
        return False

    #make bedgraphs
    donebefore, bedgraphpath = bedgraphs_from_xtra_bamdata(bampath, force)
    if donebefore:
        print("Bedgraphs will be redone..")
    # sort files by plus vs minus (strands)
    # use strand 2 as this could also be called 'antisense' with 1 'sense'.
    ext2 = MINUS + BEDGRAPH
    #ext1 = PLUS + BEDGRAPH
    bgdict1, bgdict2 = {}, {}
    for bg in bedgraphpath.glob(f"*{BEDGRAPH}"):
        bgkey = bg.name.rsplit(f"_{tag}",1)[0]
        if bg.name.endswith(ext2):
            bgdict2[bgkey] = bg
        else:
            bgdict1[bgkey] = bg

    # input for binning
    _bin_unsel_bedgraphs(bgdict1, bgdict2, tag, force)
    merge_unsel(tag, force, tee=False)
