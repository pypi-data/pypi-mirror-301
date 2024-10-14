#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  genom.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#

"""This module produces genome descriptors used for parsing and imaging."""
import logging
import pandas as pd
from pathlib import Path

from coalispr.resources.constant import (
    BINSTEP,
    CHRXTRA,
    DATASTOR,
    GTFEXON, GTFFEAT, GTFREF, GTFSPEC, GTFUNSP, GTFUNXTR, GTFXTRA,
    LENGTHSFILE, LENXTRA, LENXTRAFILE, LOG2BG, LOWR,
    MINUS,
    PLUS,
    REFERENCE,
    SAVETSV, SPAN, SPECIFIC, STOREPATH,
    TAG, TSV,
    UNSPCGAPS, UNSPECIFIC, UNSPECLOG10, UPPR, USEGAPS,
    )
from coalispr.resources.utilities import (
    replace_dot,
    thisfunc,
    )

logger=logging.getLogger(__name__)


def chroms():
    """Lists chromosome names.

    Returns
    -------
    list
        A list of strings referring to numbers/names of all chromosomes that
        form the reference genome used for mapping cDNA reads.

        The returned list is created by ``create_genom_indexes``.
    """
    global _genom
    try:
        return _genom
    except NameError:
        create_genom_indexes()
    return _genom


def get_lengths():
    """Gives a dict of chromosome lengths.

    Notes
    -----
    For example, this dict of chromosome names vs. their lengths is returned
    for **EXP** ``jec21``.

    .. code-block:: python

        {
        '1': 2300533, '2': 1632307, '3': 2105742, '4': 1783081, '5': 1507550,
        '6': 1438950, '7': 1347793, '8': 1194300, '9': 1178688, '10': 1085720,
        '11': 1019846, '12': 906719, '13': 787999, '14': 762694,
        **CHRXTRA**: int(length chrxtra),
        }


    The lengths file can be extended with an artifical chromosome (**CHRXTRA**)
    collating features (possibly) added by gene modification like the sequences
    of selectable markers, plasmids, promoters, terminators, CRISPR/Cas
    components or cleavage-guides. Also it could comprise known features not
    incorporated (yet) in the reference genome annotatotion.

    Returns
    -------
    dict : {str: int}
        A dict with lengths of chromosomes after parsing lengths files.
    """
    lengthsfile = LENGTHSFILE
    xtrafile = LENXTRAFILE
    chrxtra = 0
    chrlengths = {}

    if CHRXTRA and LENXTRA: #and LENXTRA != '':
        chrxtra = int(LENXTRA)

    if xtrafile:
        #logging.debug('using file with extra-DNA length')
        with open(xtrafile,"r") as chrlens:
            for line in chrlens:
                chrnam = str(line.strip().split("\t")[0])
                # use the configured chromosome name
                msg = f"Extra DNA in {chrnam} is used as chromosome '{CHRXTRA}'."
                if not chrnam == CHRXTRA:
                    print(msg)
                chrxtra= int(line.strip().split("\t")[1])

    if lengthsfile:
        #logging.debug('using chromosomal lengths file')
        with open(lengthsfile,"r") as chrlens:
            for line in chrlens:
                chrnam= str(line.strip().split("\t")[0])
                chrlengths[chrnam] = int(line.strip().split("\t")[1])
        if CHRXTRA and chrxtra > 0:
            chrlengths[CHRXTRA] = chrxtra
    else:
        msg = 'No chromosome lengths found.'
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    return chrlengths


def smallest2chroms():
    dictl = get_lengths()
    return [k for k,v in dictl.items() if v in sorted(dictl.values())[:2] ]


def create_genom_indexes(do_interval=False):
    """Generates range or interval indexes and a chromosome list.

    Notes
    -----
    For peak comparisons all reads documented in a bedgraph as fragments
    (via `start`, `end`) are gathered in bins of size **BINSTEP**.

    Binning relies on an existing index. Bedgraph files only come with
    fragment entries. For comparison, they need to have a common interval index.

    This function generates this common index; it creates an interval index
    for each chromosome from ``pd.interval_range``. It splits up the whole g
    enome into bins of size **BINSTEP**.

    Then, bedgraph files are reindexed on this common index, which is
    frequently used, so that a copy is stored in memory.

    Idea from  https://pbpython.com/pandas-qcut-cut.html

    Parameters
    ----------
    do_interval : bool  (default: `False`)
        If `True`, create interval index (needed for binning bedgraphs).
        If `False`, create range indexes for chromosomes.
    """
    global _chrranges
    global _chridx
    global _genom

    chrlengths = get_lengths()

    _genom = chrlengths.keys()

    if do_interval:
        # intervalindexes only needed for binning bedgraphs
        _chrranges = {
            chrnam: pd.interval_range(start=0, freq=BINSTEP, end=chrlen,
                                    closed='left')
            for chrnam, chrlen in chrlengths.items()
        }
    else:
        # bin-edges for indexing
        _chridx = {
            chrnam: pd.RangeIndex(start=0, stop=chrlen, step=BINSTEP)
            for chrnam, chrlen in chrlengths.items()
        }


def get_genom_indexes(do_interval=False):
    """Return indexes to use. With a **BINSTEP** of 50, a genome of ~19 Mbp
    (millions of base pairs, 19051922 bp) is checked in the case of **EXP**
    ``jec21``, yielding an index of 381031 lines:



    .. table:: interval ranges
       :name: dointrvl

       +--------+-------+---------------------+---------------------------+
       |        | chr   | range               |                           |
       +========+=======+=====================+===========================+
       | 0      | 1     | [0, 50)             |  <---- start interval     |
       +--------+-------+---------------------+---------------------------+
       | 1      | 1     | [50, 100)           |                           |
       +--------+-------+---------------------+---------------------------+
       | 2      | 1     | [100, 150)          |                           |
       +--------+-------+---------------------+---------------------------+
       | ...                                                              |
       +--------+-------+---------------------+---------------------------+
       | 46008  | 1     | [2300400, 2300450)  |                           |
       +--------+-------+---------------------+---------------------------+
       | 46009  | 1     | [2300450, 2300500)  |  <---- end chromosome 1   |
       +--------+-------+---------------------+---------------------------+
       | 46010  | 2     | [0, 50)             |  <---- start interval     |
       +--------+-------+---------------------+---------------------------+
       | 46011  | 2     | [50, 100)           |                           |
       +--------+-------+---------------------+---------------------------+
       | ...                                                              |
       +--------+-------+---------------------+---------------------------+
       | ...                                                              |
       +--------+-------+---------------------+---------------------------+
       | 365776 | 13    | [787850, 787900)    |                           |
       +--------+-------+---------------------+---------------------------+
       | 365777 | 13    | [787900, 787950)    |  <---- end chromosome 13  |
       +--------+-------+---------------------+---------------------------+
       | 365778 | 14    | [0, 50)             |  <---- start interval     |
       +--------+-------+---------------------+---------------------------+
       | 365779 | 14    | [50, 100)           |                           |
       +--------+-------+---------------------+---------------------------+
       | ...                                                              |
       +--------+-------+---------------------+---------------------------+
       | 381029 | 14    | [762550, 762600)    |                           |
       +--------+-------+---------------------+---------------------------+
       | 381030 | 14    | [762600, 762650)    |  <---- end chromosome 14  |
       +--------+-------+---------------------+---------------------------+


    Parameters
    ----------
    do_interval : bool     (default: `False`)
        If `True`, return interval ranges (needed for binning bedgraphs).
        The default returns range indexes for chromosomes (chromosome name
        linked to the section of the third column covering that chromosome,
        with only the start value of each interval: 0, 50, 100,..).

    Returns
    -------
    dict
        A dict of chromosome names with range indexes or interval ranges.
    """
    try:
        return _chrranges if do_interval else _chridx
    except NameError:
       #logging.debug('set_genom_indexes')
       create_genom_indexes(do_interval)
    return _chrranges if do_interval else _chridx


def chr_test():
    """Get a chromosome name as found in original gtf/bedgraphs.

    Returns
    -------
    str
        Name of first chromosome in the genome.
    """
    return next(iter(chroms()))


def retrieve_chr_regions_from_tsv(chrnam, tresh=LOG2BG, maincut=UNSPECLOG10,
    tag=TAG, kind=SPECIFIC, usecols=[LOWR,UPPR,SPAN]):
    """Read specified regions for a chromosome from tsv.

    Get stored information on `upper` and 'lower' boundaries for regions of
    contiguous reads. These have previously been obtained by assessing bedgraph
    data and saved as **TSV** files by ``gather_regions`` functions in module
    ``coalispr.bedgraph_analyze.compare``.

    Parameters
    ----------
    chrnam : str
        Name of the chromosome for which the information has been stored.
    tresh : int     (default: **LOG2B**)
        Applied treshold above which values have been taken into account.
    maincut : float    (default: **UNSPECLOG10**)
        Used minimal log10 difference between specific and unspecific values.
    tag : str       (default: **TAG**)
        Tag to indicate kind of mapped reads analysed: collapsed or uncollapsed
    kind : str      (default: **SPECIFIC**)
        The kind of specified reads stored: specific, unspecific or both.
    usecols : list
        Columns to keep in returned dataframes

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        A tuple of pandas dataframes, one for each strand of chromosome
        ``chrnam``.
    """
    kind_ = kind.lower()
    gap = USEGAPS if kind_ == SPECIFIC.lower() else UNSPCGAPS
    nam = f"_{kind_}_segments_overmax{2**tresh}_unspec{maincut}_usegaps{gap}"
    nam += f"_{tag}"
    nam = replace_dot(nam)
    path_ = Path(STOREPATH).joinpath(SAVETSV)
    fullnam = None
    try:
        for filenam in path_.iterdir():
            if filenam.name.endswith(nam):
                fullnam = filenam
                #logging.debug(f"{__name__}.{thisfunc()}:\ntry {fullnam}")
                continue
        if not fullnam:
            raise FileNotFoundError
        fullpath_ = fullnam.joinpath(f"{chrnam}_{fullnam.name}")
        ## do not use joinpath, it introduces path-separators
        #logging.debug(f"{fullpath_}_{PLUS}{TSV}")
        df1 = pd.read_csv(
            f"{fullpath_}_{PLUS}{TSV}",comment="#",sep="\t", #index_col=0,
            usecols=usecols)
        df2 = pd.read_csv(
            f"{fullpath_}_{MINUS}{TSV}",comment="#",sep="\t", #index_col=0,
            usecols=usecols)
        return df1, df2
    except FileNotFoundError:
        msg = (f"No {TSV} found with '{nam}' in {path_}; \nplease (re-) run "
               f"the '{DATASTOR}' command.")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)


def retrieve_all_chr_regions_from_tsv(chrnam, tresh=LOG2BG, maincut=UNSPECLOG10,
    tag=TAG):
    """Read all specified regions for a chromosome from tsv files.

    Get stored information on `upper` and 'lower' boundaries for all regions of
    contiguous reads (Previously obtained by assessing bedgraphs and saved as
    **TSV** by ``gather*regions`` of ``coalispr.bedgraph_analyze.compare``).

    Parameters
    ----------
    chrnam : str
        Name of the chromosome for which the information has been stored.
    tresh : int     (default: **LOG2B**)
        Applied treshold above which values have been taken into account.
    maincut : float    (default: **UNSPECLOG10**)
        Used minimal log10 difference between specific and unspecific values.
    tag : str       (default: **TAG**)
        Tag to indicate kind of mapped reads analysed: collapsed or uncollapsed

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        A tuple of pandas dataframes, one for each strand of chromosome
        ``chrnam``.
    """
    df1u, df2u = retrieve_chr_regions_from_tsv(chrnam, tresh, maincut, tag,
        kind=UNSPECIFIC)
    df1s, df2s = retrieve_chr_regions_from_tsv(chrnam, tresh, maincut, tag,
        kind=SPECIFIC)
    # merge on all columns by setting on to 'None'
    df1 = df1u.merge( df1s, on=None, how = 'outer')
    df2 = df2u.merge( df2s, on=None, how = 'outer')
    return df1, df2


class Track():
    """A class to represent a track of segments.

    A track provides input for a ``matplotlib.collections.BrokenBarHCollection``
    used in ``coalispr.bedgraph_analyze.bedgraph_plotting``.

    Attributes
    ----------
    chrnam : str
        The name of the chromosome for which the track is made
    df1, df2 : pandas.DataFrame, pandas.DataFrame
        Tuple of pandas dataframes, for strand 1 (**PLUS**) and strand 2
        (**MINUS**).
    df : pandas.DataFrame
        Pandas dataframe, used for obtaining segment information.

    """
    def __init__(self, chrnam):
        self.chrnam = chrnam
        self.df1, self.df2 = None, None
        self.df = None

    def textlist(self, clickp):
        """Show list of information for regions under the cursor.

        Parameters
        ----------
        clickp : int
            X-coordinate of point under cursor; registered after mouse-click.

        Returns
        -------
        list
            List of information associated with segments under the cursor.
        """
        return None

    def get_segments(self, df):
        """Return list of segments with information that form the track.

        Parameters
        ----------
        df : pandas.DataFrame
            A pandas dataframe with segment information

        Returns
        -------
        list
            List of lower boundaries and length of segments, parseable
            by ``matplotlib.collections.BrokenBarHCollection``.
        """
        return list(zip(self.df[LOWR],self.df[SPAN]))

    def get_ctext(self, clickp):
        """Decribe (first) region under the cursor after clicking (if any).

        Parameters
        ----------
        clickp : int
            X-coordinate of point under cursor; registered after mouse-click.

        Returns
        -------
        str
            Text associated with first entry of listed regions under cursor.
        """
        try:
            textlist = self.textlist(clickp)
            if len(textlist) > 0:
                shwtxt = "\n".join(textlist) #[0] # keep all possible info for
                logging.debug(shwtxt)
                print(shwtxt)
                return shwtxt
            return
        except ValueError as e:
            msg = f"ValueError {e}"
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            pass
        except IndexError: # empty list (nothing hit)
            msg = "IndexError: empty list (nothing hit)"
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            pass
        except TypeError: # empty track
            msg = "TypeError: empty track"
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            pass


class SegmentTrack(Track):
    """A class to represent a track of countable segments.

    Attributes
    ----------
    chrnam : str
        The name of the chromosome for which the track is made
    dfs, dfa : pandas.DataFrame, pandas.DataFrame
        Tuple of pandas dataframes, for strand 1 (plus) and strand 2 (minus).
    df : pandas.DataFrame
        Pandas dataframe, used for obtaining segment information.

    """
    def __init__(self, chrnam):
        self.chrnam = chrnam
        self.df1, self.df2 = retrieve_all_chr_regions_from_tsv(chrnam)
        self.df = self.df1
        #print(len(self.df))

    def textlist(self, clickp):
        """Show list of information for regions under the cursor.

        Parameters
        ----------
        clickp : int
            X-coordinate of point under cursor; registered after mouse-click.

        Returns
        -------
        list
            List of information associated with segments under the cursor.
        """
        return _segm_at_clickpoint(self.chrnam, clickp)


class GTFtrack(Track):
    """A Track class to represent a track with annotation info from a GTF file.

    Attributes
    ----------
    kind : str
        The kind of GTF information, for `reference`, or regions with
        **SPECIFIC** or **UNSPECIFIC** reads.
    strand: str
        The strand with the segment the annotation refers to.
    """
    def __init__(self, chrnam, kind, strand):
        super().__init__(chrnam)
        self.kind = kind
        self.strand = strand
        # gtf might not be available; catch error, but ignore it
        # (just do not show all track functionality)
        try:
            self.df = _gtf_frames(self.chrnam, self.kind, self.strand)
        except TypeError:
            pass

    def textlist(self, clickp):
        """Get list of information for regions under the cursor.

        Method overwrites that of parent, using another function.


        Parameters
        ----------
        clickp : int
            X-coordinate of point under cursor; registered after mouse-click.

        Returns
        -------
        list
            List of information associated with segments under the cursor.
        """
        if self.df.empty:
            return
        return _ref_at_clickpoint_strand(self.chrnam, clickp, self.strand,
            self.kind)


def ref_at_clickpoint(chrnam, clickp, kind):
    """Get reference label for segment with clickpoint.

    Parameters
    ----------
    chrnam : str
        The name of the chromosome for which GTF info is retrieved.
    clickp : int
        The click point of the segment under the cursor.
    kind : str
        The kind of specified reads for which a GTF could be prepared:
        (**SPECIFIC**, **UNSPECIFIC**, **REFERENCE**)

    Returns
    -------
    tuple of lists
        Lists with gene_id's from the GTF described by ``kind``; one list for
        each strand of chromosome ``chrnam``,
    """
    kind_ = kind.lower()
    gtf1, gtf2 = _retrieve_gtf(kind_)
    chr1 = gtf1[ gtf1['chrnam'] == chrnam ]
    chr1loc = (chr1[LOWR] < clickp ) & (clickp < chr1[UPPR])
    id1 = chr1[chr1loc]['gene_id'].to_list()
    chr2 = gtf2[ gtf2['chrnam'] == chrnam ]
    chr2loc = (chr2[LOWR] < clickp ) & (clickp < chr2[UPPR])
    id2 = chr2[chr2loc]['gene_id'].to_list()
    return id1, id2


def ref_in_segment(chrnam, segm, kind, ref):
    """Get reference labels for segment.

    Parameters
    ----------
    chrnam : str
        The name of the chromosome for which GTF info is retrieved.
    segm : (int,int)
        The segment to check.
    kind : str
        The kind of specified reads for which a GTF could be prepared:
        (**SPECIFIC**, **UNSPECIFIC**)
    ref : bool
        Include general **REFERENCE** GTF for annotations (slow). 0: No; 1: Yes.

    Returns
    -------
    tuple of lists
        Lists with gene_id's from the GTF described by ``kind``; one list for
        each strand of chromosome ``chrnam``.
    """
    kind_ = kind.lower()
    segmid = segm[0] + int(segm[1]-segm[0])/2

    try:
        gtf1, gtf2 = _retrieve_gtf(kind_)

        if ref:
            rgtf1, rgtf2 = _retrieve_gtf(REFERENCE)

        chr1 = pd.concat([ gtf1[  gtf1['chrnam'] == chrnam ],
                          rgtf1[ rgtf1['chrnam'] == chrnam ] ])
        chr2 = pd.concat([ gtf2[  gtf2['chrnam'] == chrnam ],
                          rgtf2[ rgtf2['chrnam'] == chrnam ] ])


        chr1['mid'] = (chr1[LOWR]+(chr1[UPPR]-chr1[LOWR])/2).astype(int)
        chr2['mid'] = (chr2[LOWR]+(chr2[UPPR]-chr2[LOWR])/2).astype(int)

    except TypeError:
        raise SystemExit("No references.")
    except KeyError:
        raise SystemExit(f"No references for {chrnam}.")
    except ValueError:
        raise SystemExit("No references.")

    chr1loc = ((segm[0] <= chr1['mid']) & (chr1['mid'] <= segm[1])) | (
       (chr1[LOWR] < segmid ) & (segmid < chr1[UPPR]))
    id1 = chr1[chr1loc]['gene_id'].unique()
    id1 = list(id1)

    chr2loc = ((segm[0] <= chr2['mid']) & (chr2['mid'] <= segm[1])) | (
       (chr2[LOWR] < segmid ) & (segmid < chr2[UPPR]))
    id2 = chr2[chr2loc]['gene_id'].unique()
    id2 = list(id2)
    return id1, id2


def _gtf_frames(chrnam, kind, strand):
    """Produce a dataframe set with annotation info from a GTF file.

    Parameters
    ----------
    chrnam : str
        The name of the chromosome for which GTF info is retrieved.
    kind : str
        The kind of specified reads for which a GTF could be prepared
        (**SPECIFIC**, **UNSPECIFIC**, or **REFERENCE**).
    strand : str
        Strand (**PLUS** or **MINUS**) to retrieve information for.

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        Tuple of dataframes, one for each strand, with information on annotated
        regions for chromosome chrnam; the field for chrnam itself has been
        omitted.
    """
    kind_ = kind.lower()
    try:
        gtf1, gtf2 = _retrieve_gtf(kind_)
        gtf = gtf1 if strand == PLUS else gtf2
        chrom = gtf[ gtf['chrnam'] == chrnam ].drop('chrnam', axis=1)
        #print( kind, strand, chrnam, "\n", chrom)
        if chrom.empty:
            msg = f"No '{kind_}' annotations for '{chrnam}, {strand}'."
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return chrom
    except TypeError:
        return


def _segm_at_clickpoint(chrnam, clickp):
    """Get segment with click point under mouse pointer.

    Parameters
    ----------
    chrnam : str
        The name of the chromosome for which GTF info is retrieved.
    clickp : int
        The click point of the segment under the cursor.

    Returns
    -------
    str
        String with lower and upper bounds of the segment under the cursor.
    """
    df1, df2 = retrieve_all_chr_regions_from_tsv(chrnam)
    # same location-segments for each frame; one will do
    try:
        chr1loc = (df1[LOWR] <= clickp) & (clickp < df1[UPPR])
    except TypeError:
        return ''
    dwn = df1[chr1loc][LOWR].to_list()
    up = df1[chr1loc][UPPR].to_list()
    try:
        return [f"{dwn[0]}-{up[0]}"]
    except IndexError:
        return ''


def _ref_at_clickpoint_strand(chrnam, clickp, strand, kind=SPECIFIC):
    """Get strand-specific annotation for region with clickpoint.

    Parameters
    ----------
    chrnam : str
        The name of the chromosome for which GTF info is retrieved.
    clickp : int
        The click point of the segment under the cursor.
    strand : str
        String to describe relevant strand, either **PLUS** or **MINUS**.
    kind : str
        The kind of specified reads for which a GTF could be prepared:
        (**SPECIFIC**, **UNSPECIFIC**, **REFERENCE**)

    Returns
    -------
    str
        Name of reference on the relevant strand.
    """
    id1, id2 = ref_at_clickpoint(chrnam=chrnam, clickp=clickp, kind=kind)
    idst = id1 if strand == PLUS else id2
    return list(set(idst)) # remove possible redundancies


def _retrieve_gtf(kind):
    """Store and return strand-specific exon positions and gene_id's.

    This information is retrieved from GTF files and stored into pandas
    dataframes.

    Parameters
    ----------
    kind : str
        Sets the sort annotatation file based on configuration:
        **REFERENCE** for genes etc. as often published; **SPECIFIC** and
        **UNSPECIFIC** for (self-)annotated sections with specified reads.

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        A tuple of pandas dataframes, one with details for upper (**PLUS**)
        strand and  one with information for lower (**MINUS**) strand.
    """
    global SPEC_PLUS, UNSP_PLUS, REF_PLUS
    global SPEC_MINUS, UNSP_MINUS, REF_MINUS
    kind_ = kind.lower()
    try:
        if kind_ == SPECIFIC.lower():
            gtf = GTFSPEC
            return SPEC_PLUS, SPEC_MINUS
        elif kind_ == UNSPECIFIC.lower():
            gtf = GTFUNSP
            return UNSP_PLUS, UNSP_MINUS
        elif kind_ == REFERENCE.lower():
            gtf = GTFREF
            return REF_PLUS, REF_MINUS
    except NameError:
        try:
            if gtf == '':
                msg = f"No gtf file ('{gtf}') for kind {kind_} available."
                logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
                return None
            #logging.debug(f"{__name__}.{thisfunc()}:\n{gtf} loaded")
            dfgtf = pd.read_csv(gtf, comment="#", sep="\t", header=None,
                dtype={0: str, 3:int, 4:int})
            # incorporate XTRA chromosome data, for references or non-coding
            #if CHRXTRA and gtf != GTFSPEC:
            #if gtf != GTFSPEC:
            msg = ""
            if (gtf == GTFREF and GTFXTRA != ''):
                dfextra = pd.read_csv(GTFXTRA, comment="#", sep="\t",
                    header=None, dtype={0: str, 3:int, 4:int})
                #dfextra[0] = CHRXTRA
                dfgtf = pd.concat([dfgtf, dfextra])
                logging.debug(f"{__name__}.{thisfunc()}: with XTRA protein "
                f"gene references from '{Path(GTFXTRA).name}'.")
            elif (gtf == GTFUNSP and GTFUNXTR != ''):
                dfextra = pd.read_csv(GTFUNXTR, comment="#", sep="\t",
                    header=None, dtype={0: str, 3:int, 4:int})
                #dfextra[0] = CHRXTRA
                dfgtf = pd.concat([dfgtf, dfextra])
                logging.debug(f"{__name__}.{thisfunc()}: with XTRA unspecific "
                f"references from '{Path(GTFUNXTR).name}'.")
                #print(dfgtf.tail())

            # only keep lines needed, that is, with configured features.
            lines_with_feature = (
                (dfgtf[2].str.strip().str.lower() == GTFEXON.lower()) |
                (dfgtf[2].str.strip().str.lower() == GTFFEAT.lower()) |
                (dfgtf[2].str.strip().str.lower() == "intron")
                )
            df = dfgtf[lines_with_feature]

            # use .assign to chain (or .copy() for no SettingWithCopyWarning)
            # omit 'gene_id "' from field, to get gene_id itself
            #assert len('gene_id "') == 9
            # use dict-expansion for 'span' column to allow another string
            df = df.assign(
                gene_id = df[8].str[9:].str.split(pat='";',n=1).str.get(0),
                **{SPAN:(df[4]-df[3])},
                )
            # split df into plus and minus frames
            df1 = df[ df[6].str.strip() == '+' ]
            df2 = df[ df[6].str.strip() == '-' ]

            gtfplus = (
                df1[[0, 3, 4, SPAN, 'gene_id']].reset_index(drop=True).
                rename(columns={0:'chrnam',3:LOWR,4:UPPR})
                )
            gtfminus = (
                df2[[0, 3, 4, SPAN, 'gene_id']].reset_index(drop=True).
                rename(columns={0:'chrnam', 3:LOWR, 4:UPPR})
                )

            if kind_ == SPECIFIC.lower():
                SPEC_PLUS = gtfplus
                SPEC_MINUS = gtfminus
                #logging.debug(f"{__name__}.{thisfunc()} SPEC; "
                #    f"SPEC_PLUS:\n{SPEC_PLUS}")
            elif kind_ == UNSPECIFIC.lower():
                UNSP_PLUS = gtfplus
                UNSP_MINUS = gtfminus
                #logging.debug(f"{__name__}.{thisfunc()} UNSP; "
                #    f"UNSP_PLUS:\n{UNSP_PLUS}\n"
                #    f"UNSP_MINUS:\n{UNSP_MINUS}")
            elif kind_ == REFERENCE.lower():
                REF_PLUS = gtfplus
                REF_MINUS = gtfminus
                #logging.debug(f"{__name__}.{thisfunc()} REF; "
                #    f"REF_PLUS:\n{REF_PLUS}")
            return _retrieve_gtf(kind_)

        except FileNotFoundError as e:
            msg = f"No gtf {gtf} or {GTFXTRA} found for kind {kind_}.\n{e}"
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            return
        except pd.errors.EmptyDataError:
            msg = f"No columns to parse from {gtf};  possibly no data in file."
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            return
        except IsADirectoryError as e:
            msg = ("Given path to gtf lacks file; check configuration; "
                f"see error:\n  {e}")
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            return
