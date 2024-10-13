#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  compare.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#

"""Module with functions used to compare bedgraph-data."""
import logging
import numpy as np
import pandas as pd

from pathlib import Path

from coalispr.bedgraph_analyze.experiment import (
    all_exps,
    get_mutant,
    get_negative,
    get_positive,
    get_reference,
    )
from coalispr.bedgraph_analyze.genom import (
    chroms,
    )
from coalispr.bedgraph_analyze.store import (
    retrieve_merged,
    retrieve_processed_files,
    store_processed_chrindexes,
    store_chromosome_data_as_tsv,
    )
from coalispr.resources.constant import (
    BINSTEP,
    LOG2BG, LOG2BGTST, LOWR,
    MIRNAPKBUF,
    REGS,
    SAVETSV, SEGSUM, SPAN, SPECIFIC, STOREPATH,
    TAGCOLL, TAGUNCOLL, TRSHLD, TSV,
    UGAPSTST, UNSPCGAPS, UNSPECIFIC, UNSPECLOG10, UNSPECTST, USEGAPS, UPPR,
    )
from coalispr.resources.utilities import (
    merg,
    replace_dot,
    thisfunc,
    timer,
    )

encoding='utf-8'
logger=logging.getLogger(__name__)


def get_indexes(df, keep='exps'):
    """Provide indexes for specific and unspecific data sets.

    Parameters
    ----------
    df : pandas.DataFrame
        The pandas dataframe from which read-indexes are retrieved.
    keep : str (default: 'exps')
        Indicates the group of reads (experiments or references) for which
        indexes need to be returned.

    Returns
    -------
    pandas.Index, pandas.Index
        Tuple of pandas indexes for specific resp. unspecific reads present in
        input dataframe.
    """
    logging.debug(f"\n{__name__}.{thisfunc()}:")
    return _specific_and_unspecific_idx(df=df, keep=keep)


def specific(chrnam, tag, setlist, maincut=UNSPECLOG10, keep='exps'):
    """Get merged dataframes with specific reads for a chromosome.

    Returned are data for both chromosomes for a list of given samples.

    Parameters
    ----------
    chrnam : str
        Name of chromosome to return data for.
    tag : str
        Type of reads, **TAG** (default) or **TAGCOLL** ('collapsed') or
        **TAGUNCOLL** ('uncollapsed').
    setlist : list
        Group of samples for which data is returned.
    maincut : float
        Exponent for log10-difference between specific and non-specific reads.

    Returns
    -------
    list of pd.DataFrames
        List with two dataframes with specific reads from merged samples for
        **PLUS** resp. **MINUS** strands.
    """
    logging.debug(f"\n{__name__}.{thisfunc()} running for chromosome {chrnam}")
    msg = (f"No chromosome {chrnam} found; no {len(setlist)} {tag} samples in "
           f"the merged dataset or maincut {maincut} is not yielding results")

    _chr1, _chr2 = {}, {}
    try:
        plus_merg, minus_merg = retrieve_merged(tag=tag)
        _idx1, _idx2 = _specific_and_unspecific(chrnam, tag, maincut=maincut,
            keep=keep, specific=True)
        _chr1 = plus_merg.get(chrnam)
        _chr2 = minus_merg.get(chrnam)

        return [ _chr1.reindex(_idx1)[setlist],
                 _chr2.reindex(_idx2)[setlist]]
    except KeyError:
        logging.debug(f"{__name__}.{thisfunc()}:KeyError\n{msg}")
        return _chr1, _chr2
    except AttributeError:
        logging.debug(f"{__name__}.{thisfunc()}:AttributeError\n{msg}")
        return _chr1, _chr2


def unspecific(chrnam, tag, setlist, maincut=UNSPECLOG10, keep='exps'):
    """Get merged dataframes with unspecific reads for a chromosome.

    Returned are data for both chromosomes for a list of given samples.

    Parameters
    ----------
    chrnam : str
        Name of chromosome to return data for.
    tag : str
        Type of reads, **TAG** (default) or **TAGCOLL** ('collapsed') or
        **TAGUNCOLL** ('uncollapsed').
    setlist : list
        Group of samples for which data is returned.
    maincut : float
        Exponent for log10-difference between specific and non-specific reads.

    Returns
    -------
    list
        List of dataframes with unspecific reads from merged samples for
        **PLUS** resp. **MINUS** strands.
    """
    logging.debug(f"\n{__name__}.{thisfunc()} running for chromosome {chrnam}")
    msg = (f"No chromosome {chrnam} found; no {len(setlist)} {tag} samples in "
           f"the merged dataset or maincut {maincut} is not yielding results")
    _chr1, _chr2 ={}, {}
    try:
        plus_merg, minus_merg = retrieve_merged(tag)
        _notidx1, _notidx2 = _specific_and_unspecific(chrnam, tag,
            maincut=maincut, keep=keep, specific=False)
        _chr1 = plus_merg.get(chrnam)
        _chr2 = minus_merg.get(chrnam)
        return [ _chr1.reindex(_notidx1)[setlist],
                 _chr2.reindex(_notidx2)[setlist]]
    except KeyError:
        logging.debug(f"{__name__}.{thisfunc()}:KeyError\n{msg} ")
        return _chr1, _chr2
    except AttributeError:
        logging.debug(f"{__name__}.{thisfunc()}:AttributeError\n{msg}")
        return _chr1, _chr2


def gather_all_specific_regions(tag, dowhat='tsv', cutoff=LOG2BG,
    maincut=UNSPECLOG10, gaps=USEGAPS, plusdiscards=False):
    """Get specific regions for a dataset.

    The output are (**TSV**) text files with tab-separated values defining
    regions with specified reads that help to speed up counting.

    Parameters
    ----------
    tag : str
        Type of reads, **TAG** (default) or **TAGCOLL** ('collapsed') or
        **TAGUNCOLL** ('uncollapsed').
    dowhat : str
        Instruction how to output data; 'tsv': write tabbed separated values
        to a text file; 'test': print total number of regions found to
        test_intervals.tsv.
    cutoff : float
        Threshold (2\ :sup:`cutoff`) for read-signals above which reads are
        considered (default: **LOG2BG**).
    maincut: float
        Threshold (10^maincut) for difference between read-signals from
        aligned-reads in wild type or mutant samples and those of unspecific
        (negative control) samples above which reads are considered 'specific'.
        (default: **UNSPECLOG10**).
    gaps: int
        Length of tolerated sections without reads separating peak-regions that
        form a contiguous segment of specified reads (default: **USEGAPS**).
    plusdiscards : bool
        If 'False' use all experimental files but omit **CAT_D**, the discards.
    """
    _gather_regions(kind=SPECIFIC, tag=tag, dowhat=dowhat, cutoff=cutoff,
        maincut=maincut, gaps=gaps, plusdiscards=plusdiscards)


def gather_all_unspecific_regions(tag, dowhat='tsv', cutoff=LOG2BG,
    maincut=UNSPECLOG10, gaps=UNSPCGAPS, plusdiscards=False):
    """Get unspecific regions.

    Output are text files with tab-separated values (**TSV**) defining regions
    with unspecific reads for samples prepared with given method.

    Parameters
    ----------
    tag : str
        Type of reads, **TAG** (default) or **TAGCOLL** ('collapsed') or
        **TAGUNCOLL** ('uncollapsed').
    dowhat : str
        Instruction how to output data; 'tsv': write tabbed separated values
        to a text file; 'test': print total number of regions found to
        test_intervals.tsv.
    cutoff : float
        Threshold (2\ :sup:`cutoff`) for read-signals above which reads are
        considered (default: **LOG2BG**).
    maincut: float
        Threshold (10\ :sup:`maincut`) for difference between read-signals from
        aligned-reads in wild type or mutant samples and those of unspecific
        (negative control) samples above which reads are considered 'specific'.
        (default: **UNSPECLOG10**).
    gaps: int
        Length of tolerated sections without reads separating peak-regions that
        form a contiguous segment of specified reads; for **UNSPECIFIC** reads
        the gap is set to **UNSPCGAPS** (best as low as **BINSTEP** to keep
        peaks tight). (default: **UNSPCGAPS**).
    plusdiscards : bool
        If 'False' use all experimental files but omit **CAT_D**, the discards.
    """
    _gather_regions(kind=UNSPECIFIC, tag=tag, dowhat=dowhat, cutoff=cutoff,
        maincut=maincut, gaps=gaps, plusdiscards=plusdiscards)


@timer
def test_intervals(logs10=None, gaps=None, thresh=None):
    """Try out various settings for UNSPECLOG10, USEGAPS and LOG2BG.

    Output are **TSV** text files with tab-separated values for **TAG**, 'KIND',
    **UNSPECLOG10**, **LOG2BG**, **USEGAPS**, **TRSHLD** in relation to the
    number of independent regions (**REGS**) of specified reads that are
    picked up with combinations of these settings.
    Produces input for `show_regions_vs_settings`.

    Parameters
    ----------
    logs10 : list
        List of possible settings for `UNSPECLOG10`, set to `UNSPECTST`.
    gaps : list
        List of possible settings for `USEGAPS`, set to `UGAPSTST`.
    thresh : tuple
        Defines the range for checking `LOG2BG` values: (start, end, step),
        set to LOG2BGTST.
    """
    def _check_merged():
        tags = []
        for tag_ in [TAGUNCOLL, TAGCOLL]:
            try1, try2 = retrieve_merged(tag_)
            if len(try1) == 0:
                print(f"\tNo {tag_} data, will be skipped")
            elif len(try1) > 0:
                print(f"\tFound {tag_} data; these will be used")
                tags.append(tag_)
        return tags

    print("\nCounting regions for various parameter settings; this will take "
          "(quite) a while;")


    _logs10 = list(UNSPECTST) if logs10 == None else logs10
    _gaps = list(UGAPSTST) if gaps == None else gaps
    _thresh = list(LOG2BGTST) if thresh == None else thresh

    tsvpath = Path(STOREPATH).joinpath(SAVETSV)
    convert_dict = { # let pandas figure out best dtype (np.float64 etc.)
        'TAG': 'str',
        'KIND': 'str',
        'UNSPECLOG10': 'float',
        'LOG2BG': 'int',
        'USEGAPS': 'int',
        REGS: 'int',
        TRSHLD: 'int',
        }
    testintervals = pd.DataFrame({'TAG': [],'KIND': [],'UNSPECLOG10': [],
            'LOG2BG': [],'USEGAPS': [], REGS: [], TRSHLD: []}, index=None)
    testintervals = testintervals.astype(convert_dict)

    i = 0
    for tag_ in _check_merged(): #[TAGUNCOLL, TAGCOLL]:
        for kind in [SPECIFIC, UNSPECIFIC]:
            for cut_ in _logs10:
                for gap_ in _gaps:
                    for log2bg_ in _thresh:
                        testintervals.loc[i] = _gather_regions(kind=kind,
                            tag=tag_, cutoff=log2bg_, maincut=cut_, gaps=gap_,
                            dowhat='test', discard=True)
                        i += 1

    # remove rows with empty values due to too stringent settings
    testintervals = testintervals.dropna()
    testintervals.to_csv(tsvpath.joinpath(f"test_intervals{TSV}"),
        sep="\t")
    print("Finished counting regions; input for plotting is ready")



def _specific_and_unspecific(chrnam, tag, maincut, keep, specific=True):
    """Return indexes for specific and unspecific lanes.

    Parameters
    ----------
    chrnam : str
        Name of chromosome for which indexes to return.
    tag : str.
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**.
    maincut : float
        Exponent describing accepted difference (10^maincut) between signals
        specified as **UNSPECIFIC** vs. **SPECIFIC**; default: **UNSPECLOG10**.
    specific : bool
        Flag to indicate what kind of read indexes to return for; when `True`,
        for **SPECIFIC** reads, when `False`, for **UNSPECIFIC** reads.

    Returns
    -------
    pandas.Index, pandas.Index
        A tuple of indexes, one for each strand, for a type of read:
        either **PLUS** and **MINUS** **SPECIFIC** indexes,
        or **PLUS** and **MINUS** **UNSPECIFIC** indexes.
    """
    # maybe a previous run created index files
    _idx1data, _idx2data = retrieve_processed_files(
        replace_dot(f"idx_{SPECIFIC.lower()}_{maincut}"), tag=tag
        )
    _notidx1data, _notidx2data = retrieve_processed_files(
        replace_dot(f"idx_{UNSPECIFIC.lower()}_{maincut}"), tag=tag
        )
    try:
        _idx1, _idx2 = _idx1data[chrnam], _idx2data[chrnam]
        _notidx1, _notidx2 = _notidx1data[chrnam], _notidx2data[chrnam]
        logging.debug(f"{__name__}.{thisfunc()}: indexes reused ")
    except KeyError:
        # if not, run on merged files to create index-files
        plus_merg, minus_merg = retrieve_merged(tag=tag)
        _idx1, _notidx1 = _specific_and_unspecific_idx(plus_merg[chrnam],
            maincut=maincut, keep=keep)
        _idx2, _notidx2 = _specific_and_unspecific_idx(minus_merg[chrnam],
            maincut=maincut, keep=keep)
        store_processed_chrindexes(replace_dot(
            f"idx_{SPECIFIC.lower()}_{maincut}"),
            chrnam, _idx1, _idx2, tag)
        store_processed_chrindexes(replace_dot(
            f"idx_{UNSPECIFIC.lower()}_{maincut}"),
            chrnam, _notidx1, _notidx2, tag)
        logging.debug(f"{__name__}.{thisfunc()}: indexes made and saved ")

    if specific == True:
        return _idx1, _idx2
    else:
        return _notidx1, _notidx2




#@timer
def _specific_and_unspecific_idx(df, maincut=UNSPECLOG10, keep = "exps"):
    """Return indices for specific and unspecific reads.

    Find row-indices for regions to be considered as background and
    those considered specific; return both sets.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with merged and binned data for mutual comparison.
    maincut : float
        Exponent describing accepted difference (10:\ :sup:`maincut`) between
        signals specified as **UNSPECIFIC** vs. **SPECIFIC**;
        (default: **UNSPECLOG10**).
    keep : str
        Describing which kind of data in df to select, either 'exps' (sample
        data) or `reference' (RNA-seq data).

    Returns
    -------
    pandas.Index, pandas.Index
        A tuple of indexes, one for each type of read: **SPECIFIC** index,
        **UNSPECIFIC** index.
    """
    # make sure that all values are a number
    df.fillna(0, inplace=True)
    # we only need the indexes for specific vs unspecific lanes
    if keep == "exps":
        # list of experiments
        to_keep = get_positive(df, allpos=False) + get_mutant(df, allmut=False)
    elif keep == "refs":
        # when using merged df of negative and reference as input
        to_keep = get_reference(df)
    #print(f"Using {keep}: {to_keep}")
    # Transposition (.T) could speed up mean calculations. Any NaN in a cell
    # will indicate the presence of a value somewhere else in the
    # row/transposed column. NaN's will be ignored in the calculations, so
    # the obtained outcome for the negative samples would give all the required
    # information, that is: the indices to drop.
    # Before taking log10, add 1 only where values are 0 (to keep them 0).
    dfu = df[ get_negative(df, allneg=False) ]
    uval = np.log10( dfu.where(dfu > 0, 1).T.mean(axis = 0))
    dfs = df[ to_keep ]
    sval = np.log10( dfs.where(dfs > 0, 1).T.mean(axis = 0))
    #msg = (f"uval: {type(uval)},\n {uval}\n")
    #msg += (f"sval: {type(sval)},\n {sval}\n")
    # Check difference, assuming more specific reads than in negative;
    # Note, that unfiltered reference seq will keep rRNA when present in
    # much higher numbers than in our negatives:
    # increasing log10 cutoff from 1.2 to say 3 partially addresses this.
    uidx = df[ sval - uval < maincut ].index
    sidx = df.drop(uidx).index
    # Show specific hits in dataframe
    msg = ""#( f"df.loc[sidx]:\n{df.loc[sidx]}\n")
    # Also check equivalence (all lengths should be the same)
    msg += (f"There were {len(df[ sval - uval >= maincut ].index ) } "
             "bins with some slight overlap with negative reads; \n "
            f"Reads in {len(uidx)} bins were not ~{10**maincut:.0f}-fold more "
             "abundant than those of the negative-controls and omitted.\n "
            f"Overall, {len(sidx)} bins with specific reads were identified.\n "
             "Is the input index of the same length as that of combined outputs"
            f"? {'Yes' if len(df.index) == len(uidx.union(sidx)) else 'No'}!"
           )
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    #print(msg)
    # sidx is specific; uidx is unspecific
    return sidx, uidx


def _group_indices(df1, df2, gaps): #, log2cutoff):
    """Get the boundaries of contiguous rows that form a sRNA segment.

    By default the minimal length of a segment is 1 bin (**BINSTEP**)
    df input columns are [samples]
    df output has columns **LOWR**, **UPPR**, **SPAN**, *[samples], **SEGSUM**.

    Parameters
    ----------
    df1 : pandas.DataFrame
        Dataframe with plus-strand information.
    df2 : pandas.DataFrame
        Dataframe with minus-strand information.
    gaps : int
        Should be multitude of **BINSTEP**, defines tolerated length of sequence
        without reads between regions with reads to treat these regions as one
        peak-region.
    #log2cutoff : int
    #    Treshold of minimum value in a region; is by default 2\ :sup:`LOG2BG`,
    #    but can vary when doing test-runs.

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        A tuple of dataframes with definitions of read-segments.
    """
    # check for no data
    NODATA = True if df1.empty and df2.empty else False

    if gaps < BINSTEP:
        msg = (f"Increase the USEGAPS-setting; {gaps} is too small, needs to "
               f"be at least {BINSTEP}, i.e. as large as the BINSTEP")
        logging.debug(f"{__name__}.{thisfunc()}:{msg}")
        print(msg)
        return

    # combine indices of both strands to obtain comparable view
    idx = df1.index.union(df2.index)
    df1 = df1.reindex(idx)
    df2 = df2.reindex(idx)

    def get_segments():
        # create pandas/numpy.array
        npidx = idx.array
        #print("npidx", npidx)
        # allow gaps within a contiguous segment: keep indices that cross gaps
        breakidx  = np.where(np.diff(npidx) > gaps)
        #print("breakidx", breakidx)
        # number of upperbound row-name in npidx is given as element of breakidx
        upbounds  = npidx[ breakidx ]
        #print("upbounds",upbounds)
        # +1 index in npidx is starting index of next contiguous segment
        lowbounds = npidx[np.add(breakidx,1).flatten()]
        #print("lowbounds",lowbounds)
        # get end index and start index of the segments
        #raise SystemExit()
        try:
            # add the last value of npidx as end of last segment
            upbounds  = np.append(upbounds,npidx[-1])
            # add start of first segment (npidx[0])
            lowbounds = np.insert(lowbounds, 0, npidx[0], axis=0)
        except IndexError:
            nonlocal NODATA
            NODATA = True
            pass
        return lowbounds, upbounds

    def dataframes_with_segmented_data():
        lowbounds, upbounds = get_segments()
        # create interval index based on the segments
        boundsidx = pd.IntervalIndex.from_arrays(lowbounds,upbounds,
            closed='both')

        #print("boundsidx",boundsidx, boundsidx.hasnans)
        # create bins
        df1['segments'], df2['segments'] = (
            pd.cut(idx, boundsidx), pd.cut(idx, boundsidx)
            # boundsidx.left, boundsidx.right
            )

        df1_2, df2_2 = (
            # sum the peak values for each segment
            df1.groupby('segments', sort=False).sum(numeric_only=True).round(2).
                reset_index(drop=True),
            df2.groupby('segments', sort=False).sum(numeric_only=True).round(2).
                reset_index(drop=True)
            )
        df1_2[SEGSUM], df2_2[SEGSUM] = (
            df1_2.sum(axis=1).round(2),
            df2_2.sum(axis=1).round(2)
            )

        df = pd.DataFrame({LOWR:lowbounds, UPPR:upbounds}).astype(int)
        df[SPAN] = df[UPPR]-df[LOWR]
        # as above, remove non-segments, get clean index
        #df = df[df[SPAN] > BINSTEP].reset_index(drop=True)
        df1_3, df2_3 = merg(df, df1_2),  merg(df, df2_2)

        msg = (f"...from {len(df1)} indices to {len(df1_3)} segments; ")
        logging.debug(f"{__name__}.{thisfunc()}_for_{thisfunc(1)}:\n{msg}\n")
        #print(msg)
        return df1_3, df2_3

    def dataframes_with_mirnabuffer():
        '''The fusing of peaks into contiguous segments of a minimal number of
        bins could throw out single peaks not overlapping more than one bin.
        These reads are relevant, for unspecific or miRNA data, but lost by::

            if not MIRNAPKBUF:
                # remove non-regions/singlepeaks
                boundsidx = boundsidx.drop(
                                    boundsidx[ boundsidx.length < BINSTEP ])

        Single peaks formed by reads mapping to only one bin would 'collapse' as
        a 'zero-length' hit on a bin edge (seen with ``coalispr showgraphs``).
        Such peaks were missed during counting. As a solution, keep all single
        peaks and add a margin (**MIRNAPKBUF**) when they have zero spans.
        '''
        allplus, allminus = dataframes_with_segmented_data()

        offset = int(BINSTEP*MIRNAPKBUF)
        zerospan = allplus[ allplus[SPAN] == 0 ].index
        for df in [allplus, allminus]:
            df.loc[zerospan, LOWR] -= offset
            df.loc[zerospan, UPPR] += offset
            df.loc[zerospan, SPAN] = 2*offset
        return allplus, allminus

    if NODATA:
        msg = (
        "i.e. empty array, no data, thresholds too high? No specific hits?")
        logging.debug(f"{__name__}.{thisfunc()}:{msg}\n")
        samples = df1.columns
        # use 'columns 'lower', 'upper', 'span', *[samples], 'segmentsum'.
        # unpack 'samples'; otherwise "NameError: name '_idx' is not defined`";
        #    this happens with e.g. countbams on empty XTRA segments.
        dfout = pd.DataFrame(columns=[LOWR, UPPR, SPAN, *samples, SEGSUM])
        # return empty dataframe
        return dfout, dfout.copy()
    else:
        return dataframes_with_mirnabuffer()


def _gather_regions(kind, tag, dowhat, cutoff, maincut, gaps, plusdiscards):
    """Obtain dataframes with all (un)specific read-regions.

    Cater for the possibility that specific mutant reads are not in the positive
    controls; use the minimum of 2**cutoff in a sample of a row to filter low
    level peaks.


    Parameters
    ----------
    kind : str
        Kind of aligned-reads (**SPECIFIC** or **UNSPECIFIC**) for which
        chromosome regions are returned. Mostly informative for specific reads
        (default).
    tag : str.
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**.
    dowhat : str
        Instruction what to return as output from this function
    cutoff : float
        Exponent describing threshold (2^cutoff) above which signals are
        considered.
    maincut : float
        Exponent describing accepted difference (10^maincut) between signals
        specified as **UNSPECIFIC** vs. **SPECIFIC**; default: **UNSPECLOG10**.
    gaps : int
        Length of tolerated sections without reads separating peak-regions that
        form a contiguous segment of specified reads (default: **USEGAPS**).
    plusdiscards : bool
        If 'False' use all experimental files but omit **CAT_D**, the discards.

    Returns
    -------
        Tuple or **TSV** files of dataframes with info on regions retrieved
        based on the parameters (cutoff, maincut, gaps) set.
    """
    kind_ = kind.lower()
    inputs = (f"{__name__}.{thisfunc()} called by {thisfunc(2)}, inputs:\n "
              f"Kind: '{kind_}', tag: '{tag}', dowhat: '{dowhat}', "
              f"cutoff: 2^'{cutoff}', maincut: 10^'{maincut}', "
              f"gaps: '{gaps}', keep discards: '{plusdiscards}' (determines "
              "sample size)")
    logging.debug(inputs)
    # omit discarded samples, they are rejected for a reason.
    explist = all_exps(plusdiscards)

    log2cutoff = 2**abs(cutoff)
    plus_regions = {}
    minus_regions = {}

    total_no_regions = 0

    for chrnam in chroms():
        if kind == SPECIFIC:
            # get dataframes with specific reads
            plus_chr, minus_chr = specific(chrnam, tag, explist,
                maincut=maincut)

        elif kind == UNSPECIFIC:
            # get dataframes with unspecific reads
            plus_chr, minus_chr = unspecific(chrnam, tag, explist,
                maincut=maincut)

        # find the regions; use max value in a row as threshold value
        df1 = plus_chr[ plus_chr.max(axis=1) > log2cutoff ].copy()
        df2 = minus_chr[ minus_chr.max(axis=1) > log2cutoff ].copy()

        # organise regions into separate segments
        try:
            input_={'TAG': tag, 'KIND': kind_, 'UNSPECLOG10': maincut,
                'LOG2BG': cutoff, 'USEGAPS': gaps, REGS: np.nan,
                TRSHLD: log2cutoff}
            msg = f"Chromosome '{chrnam}'.."
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            #print(msg)
            plus_regions[chrnam], minus_regions[chrnam] = (
                _group_indices(df1, df2, gaps)#, log2cutoff)
                )
            total_no_regions += plus_regions[chrnam].index.size
        except TypeError as e:
            msg = (f"These settings do not work for {kind_} reads of chr. "
                   f"'{chrnam}':\nLOG2BG={cutoff}, UNSPECLOG10={ maincut}.")
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}\n{e}")
            return input_ if dowhat=='test' else None

    # outputs
    if dowhat=='tsv':
        nam = replace_dot(f"{total_no_regions}_{kind_}_segments_"
            f"overmax{log2cutoff}_unspec{maincut}_usegaps{gaps}")
        store_chromosome_data_as_tsv(nam, plus_regions, minus_regions, tag)
    elif dowhat=='test':
        output={'TAG': tag, 'KIND': kind_, 'UNSPECLOG10': maincut,
            'LOG2BG': cutoff, 'USEGAPS': gaps, REGS: total_no_regions,
            TRSHLD: log2cutoff}
        logging.debug(f"{__name__}.{thisfunc()}:\n{output}")
        print(f"\n{tag} {kind_}, UNSPECLOG10: {maincut}, "
            f"USEGAPS: {gaps} LOG2BG:{cutoff}: {total_no_regions}")
        return output
