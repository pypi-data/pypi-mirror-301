#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  process_bamdata.py
#
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module to count bam files based on specification of aligned reads."""
import logging
import numpy as np
import pandas as pd
import pysam
import subprocess
from pathlib import Path

from coalispr.bedgraph_analyze.bam_counters import (
    BamCounterController,
    BamRegionCountController,
    set_cols,
    )
from coalispr.bedgraph_analyze.collect_bedgraphs import (
    checkSRCDIR,
    label_frame,
    )
from coalispr.bedgraph_analyze.experiment import (
    all_exps,
    )
from coalispr.bedgraph_analyze.genom import (
    chroms,
    get_lengths,
    retrieve_chr_regions_from_tsv,
    smallest2chroms,
    )
from coalispr.resources.constant import (
    BAK, BAM2BG, BAMPEAK, BAMSTART, BEDGRAPH, BINS, BINSTEP,
    CHRXTRA, CIGARCHK, CIGFM, CIGPD, COLLR, COMBI, CONFPATH, CORB,
    EXPFILE, EXPTXT,
    FILEKEY,
    HI,
    INMAPCOLL, INMAPUNCOLL, INTR,
    LIBR, LOG2BG, LOWR,
    MININTRON, MINUS, MULMAPCOLL, MULMAPUNCOLL, MUNR,
    NH, NM, NRMISM,
    PLUS,
    READCOUNTS, REGI,
    SAMBAM, SAMPLE, SAVEBAM, SAVETSV, SEGSUM, SHARED, SPAN, SPECIFIC, SRCDIR,
    SRCNDIRLEVEL, STOREPATH,
    TAGBAM, TAGCOLL, TAGSEG, TAGUNCOLL, TOTALS, TOTINPUT, TSV,
    UNIQ, UNMAP, UNMAPCOLLTP, UNMAPPEDFIL, UNMAPTYPE, UNSEL, UNSPCGAPS,
    UNSPECIFIC, UNSPECLOG10, USEGAPS,
    XTRA,
    )
from coalispr.resources.utilities import (
    chrom_region,
    get_skip,
    get_tsvpath,
    joiner,
    merg,
    replace_dot,
    thisfunc, timer,
    )


logger = logging.getLogger(__name__)


def _indexdict_from_segments(tresh, maincut, tag, kind):
    """Retrieve dictionary of chromosome-linked reusable iterators to get
    segments that have to be counted.

    Notes
    -----
    Reusable iterators for segements are needed to count through a series of
    samples, as the same chromosomal regions (retrieved from a datafile via a
    pandas.DataFrame) are thus repeatedly scanned for reads to count.

    Parameters
    ----------
    tresh : int
        Exponent (`LOG2BG`) for treshold level (2^tresh) to ignore background.
    maincut : float
        Exponent (`UNSPECLOG10`) to set fold difference (10^maincut) between
        bedgraph values of reads called `SPECIFIC` vs. `UNSPECIFIC` when these
        overlap.
    tag : str
        Sort of aligned-reads (`TAGCOLL` or `TAGUNCOLL`) used for generating
        alignment files.
    kind : str
        Kind (`SPECIFIC` or `UNSPECIFIC`) of specified aligned reads to be
        counted.

    Returns
    -------
    dict
        Dictionary with chromosome keys and iterators to get lower boundary,
        length of segments, signal-sums for `PLUS` and `MINUS` strands of
        segments.
    """
    global _idx

    class Segments():
        """Inner class to retrieve segments that have to be counted. From:
        Brett Slatkin, Effective Python, Item 17; same on:
        https://dev.to/v_it_aly/python-tips-how-to-reuse-a-generator-within-one-function-a5o


        Attributes
        ----------
        df1, df2 : DataFrame, DataFrame
            Pair of dataframes for `PLUS` and `MINUS` strands

        Parameters
        ----------
        chrnam : str
            Chromosome to yield segments for.
        """
        def __init__(self, chrnam):#, tresh, maincut, tag, kind):
            kind_ = kind.lower()
            self.df1, self.df2 = retrieve_chr_regions_from_tsv(chrnam,
                                    tresh=tresh, maincut=maincut, tag=tag,
                                    kind=kind_, usecols=[LOWR,SPAN,SEGSUM])
            #print(chrnam, self.df1) # check for correct processing

        def __iter__(self):
            df1 = self.df1
            segments = zip(df1[LOWR].astype(int), df1[SPAN].astype(int),
                df1[SEGSUM].astype(float), self.df2[SEGSUM].astype(float))
            yield segments

    try:
        return _idx
    except NameError:
        # store list of region descriptors and values
        _idx = { chrnam : Segments( chrnam ) for chrnam in chroms() }
        return _idx


def _binned_regions(chrnam, start, length, bins):
    """Create list of regions for bins spanning a segment.

    Parameters
    ----------
    chrnam : str
        Name of chromosome for which segments are split.
    start : int
        Lower boundary of segment to be split into bins.
    length : int
        Span of segment to be split into bins.
    bins : int (default: `BINS`)
        Number of bins a segment will be split into.

    Returns
    -------
    dict
        A dictionary of sub-segments for segments to be counted in a chromosome.
    """
    _bins = bins if bins else BINS
    # define some leeway: precede start and add to end of segment because bins
    # contain reads with only their midpoint in the bin
    offset  = int(BINSTEP/2)
    chrlen  = int(get_lengths()[chrnam])
    # Within pysam, coordinates are 0-based, half-open intervals,
    # i.e., the position 10,000 is part of the interval, but 20,000 is not.
    # An exception are samtools compatible region strings such as
    # ‘chr1:10000:20000’, which are closed, i.e., both positions 10,000 and
    # 20,000 are part of the interval.

    # 'add' offset to beginning of region
    #start_  = int(start) - offset  if int(start) > offset else 1 # int(start)
    start_  = start - offset  if start > offset else 1
    # only have integers for chromosome locations
    #range_  = int(start) + int(length) + int(offset)
    range_  = start + length + offset
    # add offset to end of region if possible
    end_    = range_ if range_ <= chrlen else chrlen
    #ref_    = f"{chrnam}:{int(start_)}-{int(end_)}"
    ref_    = f"{chrnam}:{start_}-{end_}"
    regions = {}
    try:
        section = end_-start_
        interval = int(section / _bins)
        extr = section % _bins
        startl = start_ #startl = int(start_)
        bin_ = 1
        for bin_ in range(1, _bins+1):
            endl = startl + interval - 1 if bin_ != (_bins) else end_
            #regions[(ref_, str(bin_))] = f"{chrnam}:{int(startl)}-{int(endl)}"
            regions[(ref_, str(bin_))] = f"{chrnam}:{startl}-{endl}"
            startl = endl + extr + 1 if bin_ == (_bins - 1) else endl + 1
        return regions
    except ZeroDivisionError:
        msg = (f"Check value for BINS -is given as {bins} and set to {BINS}- "
               f"in '{CONFPATH.joinpath(EXPTXT)}'; should not be 0");
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return

'''
def _countindex_from_binned_segments(segs, bins, kind=SPECIFIC):
    """Returns index from binned segments using chained generators.
    (from Dan Bader, Python Tricks, 6.7 Iterator chains).

    Parameters
    ----------
    segs = dict
        Dictionary of generators with segments toi be counted;
    """
    global _binidx

    if not segs:
        segs = _indexdict_from_segments(LOG2BG, UNSPECLOG10, TAGSEG, kind)

    def regionbins_from_segments(segs):
        for chrnam in chroms():
            for start, length, ptotal, mtotal in next(iter(segs[chrnam])):
                regionbins = _binned_regions(chrnam, start, length, bins)
                for regionbin_, region_ in regionbins.items():
                    cntidx = (regionbin_[0], regionbin_[1],  region_)
                    yield cntidx

    try:
        return _binidx
    except NameError:
        _binidx = list(regionbins_from_segments(segs))
        return _binidx
'''

def collect_bamfiles(tag=TAGBAM, src_dir=SRCDIR, ndirlevels=SRCNDIRLEVEL):
    """Retrieve all bam-file names for counting aligned reads.

    These are marked by `SAMBAM`.

    Parameters
    ----------
    tag : str (default: `TAGBAM`)
        Sort of aligned-reads (collapsed or uncollapsed).
    src_dir : Path (default: `SRCDIR`)
        Path to folder with sequencing data incl. bamfiles.
    ndirlevels : int (default: `SRCNDIRLEVEL`)
        Number of subdirectories to traverse from `SRC` directory to get to
        bamfiles.

    Returns
    -------
    dict
        Dictionary of sample (`SHORT`) names and paths to associated
        `SAMBAM`-files.
    """
    global _bamkeys
    global _nodiscards_keys
    # gives path to tag which is set: TAGBAM
    # (so tag to be searched can be ../SRCFLDR_{tag}
    p = checkSRCDIR(src_dir, tag)
    logger.debug(f"{__name__}.{thisfunc()}:\nPath to bamfiles that are "
        f"collected for counting: \n{p}")
    pattern = '**' + ndirlevels*'/*'# same folder as bedgraphs but name given
    # list uses up generator;
    exppaths = list(p.glob(pattern + SAMBAM))
    _bamkeys = all_exps()
    _nodiscards_keys = all_exps(plusdiscards=False)
    # create dict of filename-keys
    def find_filenam(df):
        for bfile in exppaths:
            if bfile.parts[-2].startswith(df[FILEKEY]):
                return bfile

    bexp = label_frame().loc[_bamkeys].apply(find_filenam, axis=1)
    #print(bexp)

    if len(_bamkeys) != len(bexp):
        msg = f"Only {len(bexp)} bam files found out of sought {len(_bamkeys)}"
        msg += f"Bam files not as in Experiment file `{EXPFILE}`; stopping..."
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)
    else:
        msg = f"All expected {len(bexp)} bam files found to count"

    return bexp.to_dict()


def num_counted_libs(plusdiscards=True):
    """Retrieve number of counted libraries from number counted bam-files."""
    global _bamkeys
    global _nodiscards_keys
    try:
        return len(_bamkeys) if plusdiscards else len(_nodiscards_keys)
    except NameError:
        collect_bamfiles()
        return num_counted_libs(plusdiscards)


def keys_counted_libs(plusdiscards=True):
    """Retrieve keys linked to counted bam-files."""
    global _bamkeys
    global _nodiscards_keys

    try:
        return _bamkeys if plusdiscards else _nodiscards_keys
    except NameError:
        collect_bamfiles()
        return keys_counted_libs(plusdiscards)


@timer
def total_raw_counts(tagBam=None, stranded=False, force=False):
    """Obtain total mapped reads and unmapped reads from alignments.

    Returns
    -------
    A **TSV** file
        A text file with tab-separated columns giving total input numbers for
        all  experiments.
    """
    totmap = {}
    totunmap = {}
    totpmap = {}
    totmmap = {}
    tsvpath = Path(STOREPATH).joinpath(SAVETSV,TOTINPUT)
    filepath = tsvpath.joinpath(f"{TOTALS}_{tagBam}{TSV}")
    donebefore = _hasbeendone(filepath, force)
    if donebefore and not force:
        return donebefore

    # obtain dict {short: bamfile}
    bams = collect_bamfiles(tag=tagBam)
    print("\nRetrieving total counts from SAM-header ...")
    pcounts, mcounts = pd.Series(dtype=np.int64), pd.Series(dtype=np.int64)
    if stranded:
        print("Obtaining stranded counts from bam file ...")
    for key in bams.keys():
        inbam = pysam.AlignmentFile(bams.get(key), 'rb')
        totmap[key] = inbam.mapped
        # will be 0 for STAR bam files
        if inbam.unmapped != 0:
            totunmap[key] = inbam.unmapped
        if stranded:
            print(key)
            pcounts, mcounts = 0, 0
            for read in inbam:
                if read.is_reverse:
                    mcounts +=1
                else:
                    pcounts +=1
            totpmap[key] = pcounts
            totmmap[key] = mcounts

    col = INMAPUNCOLL if tagBam == TAGUNCOLL else INMAPCOLL
    if len(totunmap) == 0 and len(totmap) > 0:
        print(f"Counts for mapped reads:\n {totmap}\n")
        print("No counts for unmapped reads found in SAM-header..")
    df = pd. DataFrame.from_dict(totmap, orient='index', columns=[col])
    if len(totpmap) > 0 and len (totmmap) > 0:
        dfp = pd.DataFrame.from_dict(totpmap, orient='index', columns=[PLUS])
        df = merg(df, dfp)
        dfm = pd.DataFrame.from_dict(totmmap, orient='index', columns=[MINUS])
        df = merg(df, dfm)

    def readhere(f):
        if not (UNMAPTYPE == 'fastq' and UNMAPCOLLTP == 'fasta'):
            msg = (f"UNMAPTYPE = {UNMAPTYPE} and UNMAPCOLLTP = {UNMAPCOLLTP}\n"
                   "'fastq' and 'fasta' expected; cannot calculate unmapped "
                   "reads, stopping...")
            print(msg)
            logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
            return 0

        wcl = sum(1 for line in f)
        # fastq (4 lines per read); collapsing gives fasta (2 lines per read)
        return wcl/4 if tagBam == TAGUNCOLL else wcl/2

    try:
        # only collect unmapped data if present or not found
        if UNMAPPEDFIL != '' and len(totunmap) == 0:
            print(f"Counting '{UNMAPPEDFIL}' for...")
            for key in bams.keys():
                print(f"\t{key}")
                # if isinstance(bams.get(key), pathlib.PosixPath)
                unmapfil = bams.get(key).with_name(UNMAPPEDFIL)
                if unmapfil.suffix == ".gz":
                    import gzip
                    with gzip.open(unmapfil, 'rb') as f:
                        totunmap[key] = readhere(f)
                elif unmapfil.suffix == ".bz2":
                    import bz2
                    with bz2.open(unmapfil, 'rb') as f:
                        totunmap[key] = readhere(f)
                elif unmapfil.suffix == ".xz":
                    import lzma
                    with lzma.open(unmapfil, 'rb') as f:
                        totunmap[key] = readhere(f)
                elif unmapfil.suffix == ".zip":
                    import zipfile
                    with zipfile.ZipFile.open(unmapfil, 'rb') as f:
                        totunmap[key] = readhere(f)
                else:
                    with unmapfil.open('r') as f:
                        totunmap[key] = readhere(f)
            #print(totunmap)
    except FileNotFoundError:
        msg = f"No file '{UNMAPPEDFIL}' with unmapped reads found; skipped..\n"
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        pass

    if len(totunmap) > 0:
        dfu = pd. DataFrame.from_dict(totunmap, orient='index', columns=[UNMAP])
        #print(dfu)
        dall = merg(df, dfu)
    else:
        dall = df

    dall.index.names = [SAMPLE]
    #print(dall.index.names)

    if len(dall) > 0:
        dall.to_csv(filepath, sep="\t",
            float_format='%.0f')
        print(f"Total counts saved to '{filepath}'.\n")
    else:
        print("Could not obtain total counts, sorry")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")


def count_folder(kind, bam, segments, overmax, maincut, usegaps):
    """Return folder with stored count files"""
    use_folder = (f"{kind.lower()}_{READCOUNTS.lower()}_{bam}-bam_{segments}-"
     f"segments_overmax{2**overmax}_unspec{maincut}_usegaps{usegaps}")
    return replace_dot(use_folder)


def has_been_counted(typeofcount="", kind=SPECIFIC):
    """Check whether count files have been created.

    Parameters
    ----------
    typeofcount: str
        Pattern to find specific files
    kind: str
        Selct kind of reads that have been counted, either **SPECIFIC** or
        **UNSPECIFIC**

    Returns
    -------
        boolean to indicate count file is present (True) or not (False)
    """
    folder = count_folder(kind, bam=TAGCOLL, segments=TAGUNCOLL, overmax=LOG2BG,
        maincut=UNSPECLOG10, usegaps=USEGAPS)
    p = Path(STOREPATH) / SAVETSV / folder
    files = list(p.glob(f"*{typeofcount}*{TSV}"))
    return False if len(files) == 0 else True


## help functions for counting bam files
def _check_newpath(p):
    if p.suffix not in [TSV, BAK] and not p.is_dir():
        p.mkdir(parents=True)
    elif p.suffix == TSV and not p.parent.is_dir():
        p.parent.mkdir(parents=True)


def _hasbeendone(apath, force):
    """Check whether counting or copying of bamfiles has been done before.

    Parameters
    ----------
    apath : Path
        Path to location where count or bam files would be saved.

    Returns
    -------
    bool
        `True` when count-files are present; `False` when not.
    """
    done = False
    def rename(p):
        bak = f"{p.suffix + BAK}"
        bakpath = p.with_suffix(bak)
        try:
            p.rename(bakpath)
        except FileExistsError:
            p.rename(bakpath)
        except OSError:
            print("A previous backup found ...")

    _check_newpath(apath)

    if apath.suffix != TSV:
        #print("dir ?", apath.is_dir())
        #print("any files ?", any(apath.iterdir()))
        donepaths = sorted(apath.glob(f"*{TSV}"))
        # if list donepaths has folders, process has been started
        if len(donepaths) != 0:
            if force:
                rename(apath)
                _check_newpath(apath)
            else: # not force:
                donefiles = [donefil.name for donefil in donepaths]
                nl = "\n\t"
                done = True
                msg=("\nFolder exist! Command has been run before and created:\n"
                    f"{apath}/{nl}{nl.join(donefiles)};"
                     "\n..remove/rename folders to continue processing, or "
                     "use 'force' option -f1; stopping now.\n")
                print(msg)
                logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
                return done
    msg = f"Results will be saved in '{apath}'"
    print(msg)
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    return done


def _getBamSection():
    bampeak = BAMPEAK
    bampeak = (int(bampeak[0]), int(bampeak[1]))
    if len(bampeak) !=2 and not (bampeak[0] < bampeak[1]):
        msg = (f"BAMPEAK ({BAMPEAK}) should have two integer numbers, the "
               f"first smaller than the second; set to use is {bampeak}.")
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return

    bamstart = [n.upper() for n in BAMSTART if n in "ACGTNacgtn"]
    if not len(bamstart) > 0:
        msg = f"BAMSTART ({bamstart}) does not cover a nucleotide"
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return
    return bamstart, bampeak


def _get_bampath():
    bampath = Path(STOREPATH).joinpath(SAVEBAM)
    return bampath


def _check_mulmap():
    if MULMAPUNCOLL != 1 or MULMAPCOLL != 1:
        msg = ("The counting of multimappers will be wrong if current "
        f"settings for 'MULMAPUNCOLL' ('{MULMAPUNCOLL}') or MULMAPCOLL "
        f"('{MULMAPCOLL}') in the configuration files at \n'{CONFPATH}'\n"
        f"reflect the mapping strategies for {TAGUNCOLL} or {TAGCOLL} reads."
        )
        print(msg)
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
        return


def _hitidx(hit_idx, beancounter):
    msg = (f"Found HI = {hit_idx} (SAM-parameter in counted "
           f"{TAGUNCOLL}  read);, this should be 1.\n(see item"
           f"`MULMAPUNCOLL` in '{SHARED}' or '{EXPFILE}'. "
           "Read will be skipped...")
    print(msg)
    logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
    beancounter.skip_count()


def _format_regn(regn):
    return regn.replace(':','_') if ':' in regn else regn


def _make_cigarcheck(cigchk, nomis):
    """Take cigar items as marked by 'cigartuples; cigarstring; <meaning>':
    0;M <match>,
    1;I <insertion>,
    2;D <deletion>,
    3;N <skipped>,
    which are standard (the other accepted cigar items:  4;S <soft clip>,
    5;H <hard clip>, 6;P <padding>, 7;= <sequence match>, 8;X <sequence
    mismatch, substitution> are indirectly used here.
    Skip if alignment is dubious; for short SE sequences only accept matches
    (0;M) and gaps (3;N); for reads from UV-treated samples accept a
    point-deletion (2;D)

    Parameter
    ---------
    cigchk : str (from **CIGARCHK**, either **CIGPD** or **CIGFM**)
        Defines function to use for checking a read.
    nomis : str (default: **NRMISM**)
    """
    global _unfit_read
    global _nomis
    _nomis = nomis

    if cigchk not in [CIGFM, CIGPD]:
        msg = (f"Cannot check cigar string; `CIGARCHK` ('{cigchk}') not "
            f"expected; should be one of '{CIGFM}' or, '{CIGPD}'.")
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
        raise SystemExit(msg)

    def fullmatch(cigtuples):
        return any(x[0] not in [0,3] for x in cigtuples)

    def pointdel(cigtuples):
        return any(x[0] not in [0,3,2] or (x[0]==2 and x[1] > 1 )
            for x in cigtuples)

    _unfit_read =  {CIGFM : fullmatch, CIGPD : pointdel,}[cigchk]


def _strand(read, strand):
    """Check strand of read for inclusion in counts

    Parameters
    ----------
    read : pysam.AlignedSegment
        Input for obtaining tuples describing the cigar string of an aligned
        read, number of mismatches and introns.
    strand : str
        One of **COMBI**, **PLUS** or **MINUS**; for selecting sense/antisense
        in defined sections (for which the **MUNR** and **CORB** properties
        are neither set nor applicable).

    Returns
    -------
        True or False
    """
    if strand == COMBI:
        return True
    elif strand == PLUS and not read.is_reverse:
        return True
    elif strand == MINUS and read.is_reverse:
        return True
    else:
        return False


def _check_read(read, intronchk=True):
    """Check cigar and number of tolerated mismatches for each read.

    Parameters
    ----------
    read : pysam.AlignedSegment
        Input for obtaining tuples describing the cigar string of an aligned
        read, number of mismatches and introns.
    intronchk : bool
        Check for introns and gather their lengths (or not).

    Returns
    -------
        True or False and sets list of intron-lengths for valid introns
    """
    global _okintrons
    global _nomis
    if read.is_supplementary:
        return False
    # skip non-matching reads.
    try:
        cigt = read.cigartuples        # TypeError
        if _unfit_read(cigt):
            return False
    # skip reads with too many mismatches.
        if read.get_tag(NM) > _nomis:  # KeyError
            return False
    except KeyError:
        pass
    except TypeError:
        msg = f"Cigar string expected in '{read}'."
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
        raise SystemExit(msg)
    # check presence of introns
    if intronchk:
        _okintrons = []                # reset _okintrons
        gaps = [ x[1] for x in cigt if x[0] == 3 ]
        if any(y < MININTRON for y in gaps):
            #msg = (f"Some introns in '{gaps}' < MININTRON f"({MININTRON}).")
            logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
            return False
        else:
            _okintrons = gaps
            #print(f"lengths possible introns: {okintrons}")
            return True
    return True


## count bam files
@timer
def process_bamfiles(tagSeg=TAGSEG, tagBam=TAGBAM, bins=BINS, tresh=LOG2BG,
    maincut=UNSPECLOG10, kind=SPECIFIC, writebam=False, force=False, test=False,
    cigchk=CIGARCHK, nomis=NRMISM):
    """Extract reads from a bamfile using selected_regions and count them.

    Allow for counting Bam-alignment files obtained for **TAGCOLL** reads with
    segments found for **TAGUNCOLL** reads.

    Parameters
    ----------
    tagSeg : str (default: **TAGSEG**)
        Sort of aligned-reads (**TAGCOLL** or **TAGUNCOLL**) used for generating
        segment files.
    tagBam : str (default: **TAGBAM**)
        Sort of aligned-reads (**TAGCOLL** or **TAGUNCOLL**) used for generating
        alignment files.
    bins : int (default: **BINS**)
        The number of sub-segments of equal length a contiguous segment with
        reads needs to be partitioned in for counting. This to assess coverage/
        density of reads dependent of location in the main segment.
    tresh : int (default: **LOG2BG**)
        Treshold level (2^tresh) of accepted background.
    maincut : float (default: **UNSPECLOG10**)
        Fold difference (10^maincut) between bedgraph values of reads called
        'specific' vs. 'unspecific' when these overlap.
    kind : str (default: **SPECIFIC**)
        Kind of specified aligned reads to be counted.
    writebam : bool (default: `False`)
        Do siRNA-like alignments need to be copied to separate bamfiles?
        Can be true when counting unspecific reads to see how many reads that
        fit criteria of genuine siRNAs have been omitted due to set thresholds;
        most will be fragments of abundant transcripts though.
    force : bool (default: `False`)
        Ignore previous counting; go ahead after backing old counts up.
    test : bool (defaul: `False`)
        Count a subset of samples for testing or profiling
    cigchk : str (default: **CIGARCHK**)
        Label to mark function for checking cigar string of a read alignmemnt.
    nomis : int (default: NRMISM)
    Returns
    -------
    A series of **TSV** files with count data
        The **TSV** files are saved to the configured **STOREPATH**.
    """
    # some checks beforehand:
    _check_mulmap()
    # set function for read-checking
    _make_cigarcheck(cigchk, nomis)
    kind_ = kind.lower()
    gap = USEGAPS if kind_ == SPECIFIC.lower() else UNSPCGAPS
    # obtain dict {short: bamfile}
    bams = collect_bamfiles(tag=tagBam)
    # count a few files for testing
    TEST = test
    # structure of name also used for analyzing extra bam files if writebam
    #foldernam = (f"{kind_}_{READCOUNTS}_{tagBam}-bam_{tagSeg}-segments_"
    #             f"overmax{2**tresh}_unspec{maincut}_usegaps{gap}")
    #foldernam = replace_dot(foldernam) if not TEST else (f'tests_{kind_}')
    foldernam = count_folder(kind_, tagBam, tagSeg, tresh, maincut, gap)
    if TEST:
        foldernam = f'tests_{kind_}'
    tsvpath = get_tsvpath().joinpath(foldernam)
    donebefore = _hasbeendone(tsvpath, force)
    if donebefore and not force:
        return
    # set up writebam conditions
    bamstart = None
    bampeak = None
    if writebam:
        bampath = _get_bampath().joinpath(foldernam)
        writtenbefore = _hasbeendone(bampath, force)
        if writtenbefore and not force:
            return
        bamstart, bampeak = _getBamSection()
    # need DataFrames instead of Counters to hold floats derived from
    # multimapped reads; these 'counters' are organized in various classes.
    cols = keys_counted_libs()
    if TEST:
        # test first two and last of all samples
        cols = [*cols[0:2], cols[-1]] if len(cols)>3 else cols
        print("Test: count smallest 2 chromosomes for samples '"
            f"{joiner().join(cols)}'.")
    set_cols(cols)
    # create store of segments to be counted for each sample
    segs = _indexdict_from_segments(tresh, maincut, tagSeg, kind)#, len(cols))
    #set_cntidx(_countindex_from_binned_segments(segs, bins))
    # create bam-file counters with cols and count index
    beancounter = BamCounterController()
    #print(beancounter)
    for key in cols:
        print(f"\n  {key}")
        inbam = pysam.AlignmentFile(bams.get(key), 'rb')
        if inbam.header['HD']['SO'] != 'coordinate':
            msg="Bam file is not usable; has not been sorted on coordinate."
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            raise SystemExit(msg)

        # save selected reads in a bam file of their own if needed
        if writebam:
            outfilename = str(bampath.joinpath(f"{kind_}_{key}_selected_"
                f"{tagBam}.bam"))
            selectbam = pysam.AlignmentFile(outfilename, "wb", template=inbam)
        else:
            selectbam = None

        for chrnam in chroms():
            if TEST and not chrnam in smallest2chroms():
                continue
            print(f"  {chrnam}")
            for start, length, ptotal, mtotal in next(iter(segs[chrnam])):
                # skip unexpected short peaks
                if length < get_skip(): # keep only peaks longer than get_skip
                    beancounter.skip_count()
                    continue
                # set kind of counted region from ptotal vs mtotal
                munroregion = True  if ptotal >= mtotal else False
                #corbettregion = True if mtotal > ptotal else False
                # ptotal/mtotal 0 values inform that bam-file reads on the other
                # strand, opposite to the given sequence, can be dismissed (will
                # be reads of other kind (specific vs unspecific)).
                if munroregion:
                    skipother = True if mtotal == 0 else False
                else: # corbettregion
                    skipother = True if ptotal == 0 else False
                # pysam follows 0-based bam-files; thus chr 1 is denoted as '0'
                # when retrieving as string with str(read); use to_string() for
                # correct representation)
                regionbins = _binned_regions(chrnam, start, length, bins)
                for regionbin_, region_ in regionbins.items():
                    iter1 = inbam.fetch(region=region_)
                    _parse_reads(
                        iter1, munroregion, skipother, tagBam, chrnam,
                        bamstart, bampeak, selectbam, beancounter)
                    cntidx = (regionbin_[0], regionbin_[1],  region_)
                    # finalise counters.addkeycount(cntidx, key, count)
                    beancounter.set_bincounts(cntidx, key)

        beancounter.report_skipped(key)
        if selectbam:
            selectbam.close()
        inbam.close()
        beancounter.merge_lencounters(key)

    beancounter.save_to_tsv(tsvpath, bins)


def _parse_reads(iterator, munroregion, skipother, tag, chrnam, bamstart,
    bampeak, selectbam, beancounter):
    """Process the read using pysam commands and references;

    Distinguish between anti-target sRNAs (**MUNR**, munro; in excess) and
    those derived from target strand (**CORB**, corbett, less abundant). This
    may not work for loci with transcripts from opposite strands; ``tag``
    refers to the kind of Bam-file that is used for counting.
    """
    for read in iterator:
        global okintrons
        # STAR is set to omit unmapped reads from the bam alignment but
        # maybe other aligners don't..
        if read.is_unmapped:
            continue
        # get strand to count
        if read.is_reverse:
            if munroregion and skipother:
                continue
            strand = CORB if munroregion else MUNR
        else: # not read.is_reverse:
            if skipother and not munroregion:
                continue
            strand = MUNR if munroregion else CORB

        if not _check_read(read):
            beancounter.skip_count()
            continue

        intronsize = 0
        count = 0
        cdna_count = 0
        #assert(chrnam == read.reference_name)
        nr_hits = int(read.get_tag(NH)) # > 1 for multimapping collapsed reads
        hit_idx = int(read.get_tag(HI)) # always 1 for uncollapsed reads
        seq     = read.get_forward_sequence()
        N_start = seq[0].upper()
        length  = len(seq)
        lenreadidx = f"{N_start}_{length}_mer"
        # each multimapper should have been mapped to each locus once, leading
        # to nr_hits identical entries for the same alignment; thus:
        cdna_count = 1/nr_hits
        # register multimappers and their frequency
        # (mappings that will not be counted are outwith count regions or kind)
        if nr_hits > 1: # use cdna_count for adding repeated locus "nr_hits"
            #print(nr_hits,cdna_count,strand,hit_idx )
            beancounter.update_multimap_count(LIBR, cdna_count, strand,
                nr_hits)
        # tag is set to TAGBAM in EXPFILE for `collapsed` data by default;
        if tag == TAGCOLL:
            # query_name (QN) as 'numberAsCdnaReadName_countOfCollapsedReads'
            origreadno = int(read.query_name.split('_')[-1])
            # each multimapper should have been mapped to each locus once,
            # leading to nr_hits identical entries for the same alignment.
            count = origreadno/nr_hits
            if nr_hits == 1:
                beancounter.update_strand_count(UNIQ, origreadno, strand,
                    lenreadidx)
                beancounter.update_strand_count(UNIQ+COLLR, 1, strand,
                    lenreadidx)
        # `uncollapsed` data is set to be counted; this is slow: read by read
        elif tag == TAGUNCOLL:
            count = 1
            if nr_hits == 1:
                beancounter.update_strand_count(UNIQ, 1, strand, lenreadidx)
                beancounter.update_strand_count(UNIQ+COLLR, 1, strand,
                    lenreadidx)
            if hit_idx > 1:
                _hitidx(hit_idx, beancounter)
                continue
        beancounter.update_strand_count(LIBR, count, strand, lenreadidx)
        beancounter.update_strand_count(COLLR, cdna_count, strand, lenreadidx)
        # check introns (set via global _okintrons in _check_read)
        if _okintrons:
            for intronsize in _okintrons:
                beancounter.update_strand_count(INTR, count, strand, intronsize)
                beancounter.update_strand_count(INTR+COLLR, cdna_count,
                    strand, intronsize)
                if nr_hits == 1:
                    beancounter.update_strand_count(UNIQ+INTR, origreadno,
                        strand, intronsize)
                    beancounter.update_strand_count(UNIQ+INTR+COLLR, 1, strand,
                        intronsize)
                elif nr_hits > 1:
                    beancounter.update_multimap_count(INTR, cdna_count, strand,
                        nr_hits)
        if chrnam == CHRXTRA:
            beancounter.update_strand_count(XTRA, count, strand, lenreadidx)
        if selectbam:
            if (N_start in bamstart) and (bampeak[0] <= length <= bampeak[1]):
                beancounter.update_strand_count(UNSEL, count, strand,
                    lenreadidx)
                selectbam.write(read)


def process_reads_for_region(samples, chrnam, region, strand, comparereads,
    cigchk=CIGARCHK, nomis=NRMISM, tagBam=TAGBAM):
    """Obtain read-length data for a particular region on chromosome chrnam for
    given samples.

    Parameters
    ----------
    samples : list
        List of short names to retrieve bamfiles with alignment data for.
    chrnam : str
        Name of chromosome to retrieve region from.
    region : tuple
        Tuple with coordinates for chromosomal region to retrieve counts for.
    strand : str
        One of **COMBI**, **PLUS** or **MINUS**; for selecting sense/antisense
        in defined sections (for which the **MUNR** and **CORB** properties
        are neither set nor applicable).
    comparereads: list
        List of reads to count for comparison.
    tagBam : str (default: **TAGBAM**)
        Sort of aligned-reads (**TAGCOLL** or **TAGUNCOLL**) used for generating
        alignment files.
    """
    _check_mulmap()
    _make_cigarcheck(cigchk, nomis)
    region_ = chrom_region(chrnam,region)
    region__ =_format_regn(region_)
    # keep peaks longer than get_skip
    if abs(region[1] - region[0]) < get_skip():
        msg = f"Region '{region_}' is too short to assess."
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)
    # path to save files to
    foldernam = f"{REGI}_{READCOUNTS}_{tagBam}-bam".lower()
    regionfoldernam = f"{REGI}_{region__}".lower()
    tsvpath = get_tsvpath().joinpath(foldernam,regionfoldernam)
    _check_newpath(tsvpath)
    bams = collect_bamfiles()
    beancounter = BamRegionCountController(region_, comparereads, strand)
    #read_lengths = pd.DataFrame
    set_cols(samples)

    for key in samples:
        print(f"\n  {key}")
        inbam = pysam.AlignmentFile(bams.get(key), 'rb')
        if inbam.header['HD']['SO'] != 'coordinate':
            msg="Bam file is not usable; has not been sorted on coordinate."
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            raise SystemExit(msg)

        iter1 = inbam.fetch(region=region_)
        _parse_regionreads(iter1, strand, tagBam, beancounter)
        cntidx = (region_, 1,  region_)
        beancounter.set_bincounts(cntidx, key)
        beancounter.report_skipped(key)
        inbam.close()
        beancounter.merge_lencounters(key)
    beancounter.save_to_tsv(tsvpath, region__, strand)
    return  beancounter.get_lencount_frames(), beancounter.get_count_frames()


def _parse_regionreads(iterator, strand, tag, beancounter):
    """Process the read using pysam commands and references;

    The ``tag`` refers to the kind of Bam-file that is used for counting;
    ``strand`` directs what read will be counted.
    """
    for read in iterator:
        # STAR is set to omit unmapped reads from the bam alignment but
        # maybe other aligners don't..
        if read.is_unmapped:
            continue

        if not _strand(read, strand):
            #print(read.is_reverse, strand)
            continue

        if not _check_read(read, False):
            beancounter.skip_count()
            continue

        count = 0
        cdna_count = 0
        strnd = None # for keyword argument 'strand' in update_strand_count()
        nr_hits = int(read.get_tag(NH)) # > 1 for multimapping collapsed reads
        hit_idx = int(read.get_tag(HI)) # always 1 for uncollapsed reads
        seq     = read.get_forward_sequence()
        N_start = seq[0].upper()
        length  = len(seq)
        lenreadidx = f"{N_start}_{length}_mer"

        # each multimapper should have been mapped to each locus once, leading
        # to nr_hits identical entries for the same alignment; thus:
        cdna_count = 1/nr_hits
        # tag is set to TAGBAM in EXPFILE for `collapsed` data by default;
        if tag == TAGCOLL:
            # query_name (QN) as 'numberAsCdnaReadName_countOfCollapsedReads'
            origreadno = int(read.query_name.split('_')[-1])
            # each multimapper should have been mapped to each locus once,
            # leading to nr_hits identical entries for the same alignment.
            count = origreadno/nr_hits
            if nr_hits == 1:
                beancounter.update_strand_count(UNIQ, origreadno, strnd,
                    lenreadidx)
                beancounter.update_strand_count(UNIQ+COLLR, 1, strnd,
                    lenreadidx)
        # `uncollapsed` data is set to be counted; this is slow: read by read
        elif tag == TAGUNCOLL:
            count = 1
            if nr_hits == 1:
                beancounter.update_strand_count(UNIQ, 1, strnd, lenreadidx)
                beancounter.update_strand_count(UNIQ+COLLR, 1, strnd,
                    lenreadidx)
            if hit_idx > 1:
                _hitidx(hit_idx,beancounter)
                continue
        beancounter.update_strand_count(COLLR, cdna_count, strnd, lenreadidx)
        beancounter.update_strand_count(LIBR, count, strnd, lenreadidx)


def bedgraphs_from_xtra_bamdata(bampath, force=False):
    """Create bedgraph files from selected bamdata.

    During specification of reads, genuine siRNAs can be thrown out due to
    overlap with unspecific reads even if these would not be siRNAs. Thus, based
    on start-nucleotide and length range, siRNAs can be retrieved during
    counting of unspecified reads and copied to new bam files. Here, extract
    and process these reads.

    Bam files need to be sorted and indexed before they can be converted to
    bedgraphs
    """
    if not bampath.is_dir():
        print(f"Bam-files folder '{bampath}' not present)")
        return

    bamstart, bampeak = _getBamSection()
    # set up names for paths
    namestart = bampath.stem.split("_")[0]
    outbase = (f"{namestart}_{''.join(bamstart)}_{bampeak[0]}-{bampeak[1]}mers")
    # set up path to bedgraph folder
    bedgraphpath = bampath.joinpath(f"bedgraphs_{outbase}")
    donebefore = _hasbeendone(bedgraphpath, force)
    if donebefore and not force:
        return donebefore, bedgraphpath
    # set up paths to scripts
    shscrpt = Path(BAM2BG)
    shlink = bampath.joinpath(shscrpt.name)
    if not shlink.is_symlink():
        shlink.symlink_to(shscrpt)

    def sortindex():
        msg = f"Sorting and indexing {UNSEL} bam files..."
        if bam.with_suffix(".bam.bai").exists():
            print("Indexing has been done before")
            msg += ", done before."
        else:
            print("Let's sort, then make an index")
            pysam.sort("-o", str(bam), str(bam))
            pysam.index(str(bam))
            msg += ", done."
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")

    def getkeysource():
        if bam.stem.startswith(UNSPECIFIC.lower()):
            src = UNSPECIFIC.lower()
        elif bam.stem.startswith(SPECIFIC.lower()):
            msg = f"No {SPECIFIC} bam-files generated for unselected reads."
            logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
            #src = SPECIFIC.lower() # unselected is per definition UNSPECIFIC
        else:
            msg = f"Wrong start for filename; cannot proceed '{src}'; stopping"
            logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
            return
        tag = bam.stem.rsplit("_", 1)[-1]
        if tag not in [TAGUNCOLL,TAGCOLL]:
            msg = (f"Bam file has no {', '.join([TAGUNCOLL,TAGCOLL])} at "
                   f"expected place, instead {tag} will be in bedgraph names.")
            print(msg)
            logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
        key = bam.stem.replace(src,"")
        key = key.split("_selected")[0]
        return f"{src[0]}{key}_{tag}_"

    for bam in bampath.glob("*.bam"):
        # index available ?
        sortindex()
        # bedgraph name
        bgnam = getkeysource()
        print(f"Bedgraphs for {bgnam}")
        # make bedgraphs
        plusbg = str(bedgraphpath.joinpath(f"{bgnam}{PLUS}{BEDGRAPH}"))
        minbg = str(bedgraphpath.joinpath(f"{bgnam}{MINUS}{BEDGRAPH}"))
        subprocess.run([str(shscrpt), str(bam), plusbg, minbg])

    return donebefore, bedgraphpath
