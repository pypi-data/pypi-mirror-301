#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  bam_counters.py
#
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#

"""Module with counters for extracting information from bamfiles."""
import logging
import pandas as pd

from coalispr.resources.constant import (
    ALL,
    BCO, BINN, BREG,
    CNTGAP, CNTRS, COLLR, COMBI, CORB, COU,
    LEN, LENCNTRS, LENCOUNTS, LENMER, LIBR,
    MMAPCNTRS, MULMAP, MUNR,
    REGCNTRS, REGI, REPS, RLENCOUNTS,
    SKIP,
    TSV,
    UNIQ,
    )
from coalispr.bedgraph_analyze.experiment import (
    get_discard,
    )
from coalispr.resources.utilities import (
    is_all_zero,
    merg,
    thisfunc,
    )


logger = logging.getLogger(__name__)

COLS = []

def set_cols(colslist):
    """Define the list of samples that are counted.

    Notes
    -----
    The ``colslist`` is defined by functions (``process_bamfiles`` or
    ``process_reads_for_region``) creating the count controllers (as
    *beancounter*), in  ``coalispr.bedgraph_analyze.process_bamdata``.

    Parameters
    ----------
    colslist : list
        List of samples that form column index of dataframes storing the counts.
    """
    global COLS
    COLS = colslist


def get_cols():
    """Return the list of samples for which counts are gathered."""
    return COLS


def count_frame(dtype=float):
    """Base dataframe with multi-index and column-keys to store counts.

    Parameters
    ----------
    dtype: pandas.dtype
        Datatype for dataframe

    Returns
    -------
        Empty dataframe to be filled when processing bam file.
    """
    global base_df
    IND = [f"{REGI}", f"{BINN}", f"{BREG}"]

    try:
        return base_df
    except NameError:
        # Stick with 'float', basis of NaN; use .astype() at end.
        # ("Int64" useless; type change when summing, merging etc.)
        base_df = pd.DataFrame(columns=IND+COLS, dtype=dtype)
        base_df = base_df.set_index(IND)
        return base_df



class BamCounterController():
    """Interface for counting; calls counter functions.

    Notes
    -----
    Counter groups defined in ``2_shared.txt`` (**SHARED**) and ``3_EXP.txt``
    (**EXPTXT**) are used here.

    ::

        CNTREAD        = [LIBR, UNIQ, XTRA, UNSEL]  # MULMAP = LIBR - UNIQ
        CNTCDNA        = [COLLR, UNIQ+COLLR]        # COLLR+MULMAP = COLLR - (UNIQ+COLLR)
        CNTGAP         = [INTR, INTR+COLLR, UNIQ+INTR, UNIQ+INTR+COLLR]
        #CNTSKIP        = [SKIP]

        CNTRS          = [CNTREAD, CNTCDNA, CNTGAP, [SKIP] ]

        LENREAD        = [LIBR, UNIQ, XTRA, UNSEL]
        LENCDNA        = [COLLR, UNIQ+COLLR]
        LENGAP         = [INTR, INTR+COLLR, UNIQ+INTR, UNIQ+INTR+COLLR]

        LENCNTRS       = [LENREAD, LENCDNA, LENGAP]

        MMAPCNTRS      = [ [LIBR, INTR] ]
    """
    def __init__(self):
        self.binners = self._generate_bincountersdict()
        self.sizers = self._generate_lencountersdict()
        self.mmappers = self._generate_mmapcountersdict()
        logging.debug(f"{__name__}.{self}") #print(self)

    def _generate_bincountersdict(self):
        binner_dict = {}
        for countgrps in CNTRS:
            for label in countgrps:
                if label == SKIP:
                    binner_dict[label] = SkipCounter(label)
                else:
                    binner_dict[label] = BinCounter(label)
        return binner_dict

    def _generate_lencountersdict(self):
        sizer_dict = { label : LengthCounter(label)
            for countgrps in LENCNTRS
            for label in countgrps }
        return sizer_dict

    def _generate_mmapcountersdict(self):
        mmapper_dict = { label: MultiMapCounter(label) for
            countgrps in MMAPCNTRS for
            label in countgrps if label
        }
        return mmapper_dict

    def __repr__(self):
        return( f"{self.__class__.__name__}("
                f"{self._get_allcounters()!r})")# at {hex(id(self))}")

    def __str__(self):
        return( f"{self.__class__.__name__}("
                f"'{self._get_allcounters()}')")

    def _get_allcounters(self):
        returnlst = []
        for dct in [self.binners, self.sizers, self.mmappers]:
            returnlst += dct.values()
        return returnlst

    def set_bincounts(self, cntidx, key):
        """Update bincounters with key-linked region counts.

        Parameters
        ----------
        cntidx : tuple
            (region, binno, binregion)
        key : str
            Name of the Series (sample that is counted)
        """
        if self.binners:
            for bincounter in self.binners.values():
                bincounter.set_bincounts(cntidx, key)

    def merge_lencounters(self, key):
        """Update length counter frames with key-linked info.

        Parameters
        ----------
        key : str
            Name of the Series (sample that is counted)
        """
        for dct in [self.sizers, self.mmappers]:
            for lencounter in dct.values():
                lencounter.merge_lencounters(key)

    def skip_count(self, val=1):
         """Add to SkipCounter only."""
         self.binners[SKIP].skip_count(val)

    def report_skipped(self, key):
        """Feedback on missed counts for each sample/key."""
        self.binners[SKIP].report_skipped(key)

    def update_strand_count(self, label, val, strand, lenreadidx):
        """Set in-read count for given counter

        Parameters
        ----------
        label : str
            Name for the counter to update.
        val : int or float
            Value to add to gathered counts.
        strand : str
            Name for strand where reads come from (**MUNR** or **CORB**).
        lenreadidx : index
            Index describing readlength to add counts to.
        """
        try:
            #if self.binners:
                #self.binners[label].update_strand_count(val, strand, None)
            if self.sizers:
                self.sizers[label].update_strand_count(val, strand, lenreadidx)
            if self.binners:
                self.binners[label].update_strand_count(val, strand, None)
        except KeyError: # counter not available
            pass

    def update_multimap_count(self, label, val, strand, nhreadidx):
        """Set count for multimapper hit-number (NH) for given counter.

        Parameters
        ----------
        label : str
            Name for the counter to update.
        val : int or float
            Value to add to gathered counts.
        strand : str
            Name for strand where reads come from (**MUNR** or **CORB**).
        nhreadidx : index
            Index describing hit/repeat-number to add counts to.
        """
        try:
            self.mmappers[label].update_strand_count(val, strand, nhreadidx)
        except KeyError: # counter not available
            pass

    def save_to_tsv(self, tsvpath, bins):
        """Save the counts to **TSV** files.

        Parameters
        ----------
        tsvpath : Path
            Path for folder to store files
        bins : int
            Number of sections a counted region is split into.
        """
        for counter in self._get_allcounters():
            counter.save_to_tsv(tsvpath, bins)



class BamRegionCountController(BamCounterController):
    """Interface for counting particular regions; calls counter functions.

    Notes
    -----
    Of the counter groups defined in '2_shared.txt` (**SHARED**) needed here
    are:

    ::

        REGCNTRS       = [ [LIBR, UNIQ],  [COLLR, UNIQ+COLLR] , CNTSKIP ]

    """
    def __init__(self,region, comparereads, strand):
        """Create just a few relevant counters that scan a given region."""
        self.region = region
        self.comparereads = comparereads
        self.strand = strand
        self.binners = self._generate_bincountersdict()
        self.sizers = self._generate_lencountersdict()
        self.mmappers = None
        logging.debug(f"{__name__}.{self}")

    def _generate_bincountersdict(self):
        binner_dict = { SKIP : SkipCounter(SKIP) for countgrps in REGCNTRS
            if SKIP in countgrps }
        return binner_dict

    def _generate_lencountersdict(self):
        sizer_dict = { label : RegionLengthCounter(label)
            for countgrps in REGCNTRS
            for label in countgrps
                if label != SKIP and label in self.comparereads }
        return sizer_dict

    def _get_allcounters(self):
        return  list(self.binners.values()) + list(self.sizers.values())

    def _isincomparereads(self, chklist):
        for x in chklist:
            if x not in self.comparereads:
                return False
        return True

    def merge_lencounters(self, key):
        if self.sizers:
            for lencounter in self.sizers.values():
                lencounter.merge_lencounters(key)

    def save_to_tsv(self, tsvpath, region, strand):
        """Save the counts to **TSV** files.

        Parameters
        ----------
        tsvpath : Path
            Path for folder to store files
        region : str
            Formatted descriptor for counted genome span;
            f"{chrnam}_{region[0]}-{region[1]}".
        strand : str
            One of **COMBI**, **PLUS** or **MINUS**;
        """
        for counter in self._get_allcounters():
            counter.save_to_tsv(tsvpath, region, strand)

    def get_lencount_frames(self):
        """Get dataframes with counts."""
        return( {label: counter.get_lencount_frame() for
           label,counter in self.sizers.items()})

    def get_count_frames(self):
        """Get dataframe with counts. Add multimappers."""
        try:
            fram = pd.concat([ counter.get_count_frame() for
                counter in self.sizers.values() ])
        except ValueError as e:# no data to display
            logging.debug(f"{__name__}.{thisfunc()}:\n{e}")
            raise SystemExit("No data to display")


        if self._isincomparereads( [LIBR, UNIQ, MULMAP+LIBR] ):
            fram.loc[f"{MULMAP+LIBR}"] = (
                fram.loc[f"{LIBR}"] - fram.loc[f"{UNIQ}"]
                )
        if self._isincomparereads( [COLLR, UNIQ+COLLR, MULMAP+COLLR] ):
            fram.loc[f"{MULMAP+COLLR}"] = (
                fram.loc[f"{COLLR}"] - fram.loc[f"{UNIQ+COLLR}"]
                )
        return fram



class Counter():
    """Interface class for making data-frame counters.

    Notes
    -----
    Dataframes used as counters in view of fractional counts for multimappers.
    Strand-specific counting can be facilitated.

    Attributes
    ----------
    label: str
        Name for BinCounter, from the **CNTRS** list
    dtype
        Can be ``int``, ``"Int64"`` (``pd.Int64Dtype()``) or ``float``.
        To let pandas choose appropriate Numpy format use ``int`` and ``float``;
        nullable integer ``"Int64"`` takes ``pd.NA`` for missing value instead
        of ``NaN`` (dtype ``float``) after merging frames without perfect index
        overlap (see https://pandas.pydata.org/docs/user_guide/integer_na.html).
        For rounding, with ``float`` and ``Int64``, calling ``astype(dtype)`` is
        not needed at end for bin-counters but needed for length-counters
        or in the case of ``int`` before saving to file. The ``float_format``
        function (commented out) could be used instead.
        Pre-indexed frames do not lead to a speed-up.

    Parameters
    ----------
    munrfram : pd.DataFrame
        Frame to hold counts for reads on munro-strand, divided over
        regions and bins (as index) with **SHORT** names as column keys.
    corbfram : pd.DataFrame
        As munrfram but holding counts for reads from opposite strand.
    munrcount : int or float
        Tracks munro-strand associated counts linked to region iterated;
        reset when a new region is iterated over.
    corbcount : int or float
        Tracks corbett-strand associated counts for region iterated
    """
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return( f"{self.__class__.__name__}("
                f"{self.label!r}, format as: {self.dtype!r})")# at {hex(id(self))}")

    def __str__(self):
        return( f"{self.__class__.__name__}("
                f"'{self.label}, format as: {self.dtype}')")

    def update_strand_count(self, val, strand, lenreadidx):
        """Set in-read count"""
        pass

    def set_bincounts(self, cntidx, key):
        """Set region-index for key to stranded counts; prepare
        for next round by resetting strand count.

        Parameters
        ----------
        cntidx : tuple
            Tuple to form index with: (region, binno, binregion).
        key : str
            Name of the Series (sample that is counted).
        """
        pass

    def merge_lencounters(self, key):
        """Merge counters; ``pass`` here, only valid for ``LengthCounter``."""
        pass

    '''
    def floatformat(self):
        """Set formatting for numbers in saved count files"""
        #return '%.2f' if self.dtype == float else None #'%.0f'
        return 2 if self.dtype == float else 0
    '''

    def save_to_tsv(self, tsvpath, bins):
        """Save stranded and combined counts to files; sum over bins and
        save summed counts to separate files; use lowercase filenames.

        Parameters
        ----------
        tsvpath : Path
            Path to folder to store **TSV** file with count information.
        bins : int (default: None)
            Number of bins to split segment with counts into to detect
            preferential accumulation of reads (near 5' or 3' for example).
        """
        pass



class BinCounter(Counter):
    """Class for making data-frame counters, with bin-regions in index."""
    def __init__(self, label):
        super().__init__(label)
        self.dtype = 'float'  if not UNIQ in label else 'Int64'
        self.rnd = 2 if not UNIQ in label else 0
        self._generate_frames()

    def _reset(self):
        self.munrcount = 0
        self.corbcount = 0

    def _generate_frames(self):
        self._reset()
        df = count_frame() #.astype(self.dtype)
        self.munrfram = df.copy()
        self.corbfram = df.copy()

    def update_strand_count(self, val, strand, lenreadidx):
        """Set in-read count, ignore lenreadidx)"""
        if strand == MUNR:
            self.munrcount += val
        else:
            self.corbcount += val

    def set_bincounts(self, cntidx, key):
        """Set region-index for key to stranded counts; prepare
        for next round by resetting strand count.

        Parameters
        ----------
        cntidx : tuple
            Tuple to form index with: (region, binno, binregion).
        key : str
            Name of the Series (sample that is counted).
        """
        self.munrfram.loc[cntidx, [key]] = self.munrcount
        self.corbfram.loc[cntidx, [key]] = self.corbcount
        self._reset()

    # process read-counts; these cover multimappers, leading to floats;
    # .round(2) does work with to_csv when using .astype();
    def save_to_tsv(self, tsvpath, bins):
        """Save stranded and combined counts to files; sum over bins and
        save summed counts to separate files; use lowercase filenames.

        Parameters
        ----------
        tsvpath : Path
            Path to folder to store **TSV** file with count information.
        bins : int (default: None)
            Number of bins to split segment with counts into to detect
            preferential accumulation of reads (near 5' or 3' for example).
        """
        nam = self.label
        typ = self.dtype
        rnd = self.rnd
        mdf = self.munrfram
        cdf = self.corbfram
        # for non-overlapping rows, fill NaN with 0 for sane summing
        # (otherwise float64-like NaN can be given as sum()-result)
        combdf = mdf.add(cdf, fill_value=0)
        for strd, frme in {COMBI:combdf, MUNR:mdf, CORB:cdf}.items():
            try:
                if not is_all_zero(frme):
                    frme = (frme
                            .dropna(how='all') # drop all-zero rows
                            #.dropna(axis=1, how='all') # drop all-zero columns
                            .fillna(0)
                            .round(rnd)
                            .astype(typ)
                            )
                    if bins > 1:
                        # write files with bins info
                        fnam = (f"{nam}{BCO}_{strd}{TSV}").lower()
                        frme.to_csv(
                            tsvpath.joinpath(fnam),
                            sep='\t')
                    # sum read-counts in bins for a region (drops bin column)
                    combbin = (frme
                        .groupby(level=REGI, sort=False)
                        .sum(numeric_only=True)
                        )
                    fnam = (f"{nam}{COU}_{strd}{TSV}").lower()
                    combbin.to_csv(
                        tsvpath.joinpath(fnam),
                        sep='\t',
                        )
                else:
                    raise ZerosFrameException()
            except ZerosFrameException:
                msg= f"ZerosFrameException for {strd}"
                logging.debug(f"{__name__}.{self}.{thisfunc()}: {msg}")



class SkipCounter(Counter):
    """Class to keep track of skipped reads with imperfect alignments
    or more than one hit-index for uncollapsed reads (should be none).

    Attributes
    ----------
    notfram : pd.DataFrame
        As munrfram or corbfram, but not stranded.
    not_keycntr : pd.Series
        As munr_keycntr or corb_keycntr, but not stranded.
    notcount : int
        Skipped count linked to key (**SHORT** name for sample).
    """
    def __init__(self, label):
        super().__init__(label)
        self.dtype = "Int64"
        self._generate_frames()
        #print(self.notfram.dtypes)

    def _generate_frames(self):
        self._reset()
        self.notfram = count_frame(self.dtype)#.astype(self.dtype)

    def _reset(self):
        self.notcount = 0

    def set_bincounts(self, cntidx, key):
        """Set region-index for key to stranded counts; prepare
        for next round by resetting strand count.

        Parameters
        ----------
        cntidx : tuple
            Tuple to form index with: (region, binno, binregion).
        key : str
            Name of the Series (sample that is counted).
        """
        self.notfram.loc[cntidx, [key]] = self.notcount
        # reset
        self._reset()

    def update_strand_count(self, val, strand, lenreadidx):
        pass

    def skip_count(self, val):
        """Use one counter, independent of strand.

        Parameters
        ----------
        val = int
            Value to add to gathered counts.
        """
        self.notcount += val

    def report_skipped(self, key):
        """Indicate how many reads have been skipped for sample ``key``."""
        print(f"\tSkipped: {self.notfram[key].sum():.0f}")

    def get_lencount_frame(self):
        pass

    def get_count_frame(self):
        """Organise basic counts into dataframe and return this."""
        nfram = (self.notfram
            .dropna(how='all')
            .fillna(0) # NaN are seen as floats
            #.round()
            .astype(self.dtype)
            )
        try:
            if not (nfram.empty or is_all_zero(nfram)):
                # skip bin info
                notframbin = (nfram
                    .groupby(level=REGI, sort=False)
                    .sum(numeric_only=True)
                    )
                return notframbin
            else:
                raise ZerosFrameException()
        except ZerosFrameException:
            msg= "ZerosFrameException"
            logging.debug(f"{__name__}.{self}.{thisfunc()}: {msg}")

    def save_to_tsv(self, tsvpath, arg, *args):
        """Save skipped read counts file; use lowercase filename.

        Parameters
        ----------
        tsvpath : Path
            Path to folder to store **TSV** file with count information.
        arg: int (when bins); or str (when region); default: None
        *args: could be strand for region counting
        """
        nam = self.label
        a = COMBI if type(arg)==int else arg
        b = '' if not args else f"_{'_'.join(str(i) for i in args)}"
        fnam = (f"{nam}{COU}_{a}{b}{TSV}").lower()
        try:
            self.get_count_frame().to_csv(
                tsvpath.joinpath(fnam),
                sep='\t',
                )
        except AttributeError:
            pass



class LengthCounter(Counter):
    """Class for making data-frame counters cataloging lengths.

    Notes
    -----
    ``pd.DataFrame`` is used instead of ``collections.Counter`` in order to
    keep float nature of counts for multimapped reads


    Attributes
    ----------
    munr_keycntr : pd.Series
        Series to hold munro-strand associated counts with region info
        as index; named to **SHORT** name for counted sample; reset when
        merged to munrfram and another sample is counted.
    corb_keycntr : pd.Series
        Series with all corbett-strand associated counts for each key.
    idxnam : str
        Name for index column when dataframes get saved to **TSV**.
    cntlabl : str
        Label to mark type of counts in saved file name.
    """
    def __init__(self, label):
        super().__init__(label)
        self.dtype = float if not UNIQ in label else "Int64"
        self.rnd = 2 if not UNIQ in label else 0
        self._generate_frames()

        if self.label in CNTGAP:
            self.cntlabl = LENCOUNTS
            self.idxnam = LEN
        else:
            self.cntlabl = RLENCOUNTS
            self.idxnam = LENMER

    def _generate_frames(self):
        self._reset()
        self.munrfram = pd.DataFrame(dtype=float) #self.dtype)
        self.corbfram = pd.DataFrame(dtype=float) #self.dtype)

    def _reset(self):
        self.munr_keycntr = pd.Series(dtype=float) #self.dtype)
        self.corb_keycntr = pd.Series(dtype=float) #self.dtype)

    def set_bincounts(self, cntidx, key):
        pass

    def merge_lencounters(self, key):
        """Merge key_length counters to count_frames then reset former.

        Notes
        -----
        Include ``.astype(self.dtype)`` at very end, not here, to have set type;
        otherwise a type change from merging series with non-overlapping indices
        causes a ``TypeError`` when summing row-values (cast to ``int64``
        (from count) and <NA> (``"Int64"``), or to ``NaN`` (``float``) and
        ``Float64`` (from ``"Int64"``)).

        Parameters
        ----------
        key : str
            **SHORT** name of sample as column index (key) to collect counts
            for.
        """
        # merge
        self.munrfram = merg(
            self.munrfram, self.munr_keycntr.to_frame(key) )#.astype(self.dtype)
        self.corbfram = merg(
            self.corbfram, self.corb_keycntr.to_frame(key) )#.astype(self.dtype)
        # reset
        self._reset()

    def update_strand_count(self, val, strand, lenreadidx):
        """Forward strand count to Series counter.

        Parameters
        ----------
        val : int or float
            Value to add to gathered counts.
        strand : str
            Name for strand where reads come from (**MUNR** or **CORB**).
        lenreadidx : index
            Index describing readlength to add counts to.
        """
        # pandas.Series used as counter
        s = self.munr_keycntr if strand == MUNR else self.corb_keycntr
        try:
            s.loc[lenreadidx] += val
        except KeyError:
            s.loc[lenreadidx] = val

    def update_multimap_count(self, val, strand, lenreadidx):
        pass

    def save_to_tsv(self, tsvpath, bins=None):
        """Save length frames for separate strands and samples, then for
        all samples combined. Use lowercase filenames.

        Parameters
        ----------
        tsvpath : Path
            Path to folder to store **TSV** file with count information.
        bins : int (default: None)
            Number of bins to split segment with counts into to detect
            preferential accumulation of reads (near 5' or 3' for example).
        """
        def save_allframe(frme, fnam2):
            """Create a combined (read)lengths frame; omit discards.

            Parameters
            ----------
            frme : pandas.DataFrame
                Dataframe to be saved to **TSV**.
            fnam2 : str
                Filename  for saved dataframe.
            """

            omits = get_discard(frme)
            fnam = (f"{fnam1}{ALL}_{fnam2}").lower()
            if omits:
                frme = (frme
                    .drop(omits, axis=1)
                    .dropna(how='all')
                    )

            frme = (frme
                .fillna(0)
                #.sum(axis=1) # gives floats from "Int64"
                .T.sum().T
                .round(rnd)
                .astype(typ)
                )
            frme.index.names = [f"{idx}"]
            frme.name = f'{ALL}_{labl}'
            frme.to_csv(
                    tsvpath.joinpath(fnam),
                    sep='\t',
                    na_rep='0',
                    )

        nam = self.label
        idx = self.idxnam
        labl = self.cntlabl
        typ = self.dtype
        rnd = self.rnd
        fnam1 = f"{nam}_{labl}_"
        mf = self.munrfram.sort_index()
        cf = self.corbfram.sort_index()
        combf = mf.add(cf, fill_value=0)
        for strd, frme in {COMBI:combf, MUNR:mf, CORB:cf}.items():
            try:
                if not (frme.empty or is_all_zero(frme)):
                    frme.index.names = [f"{idx}"]
                    fnam2 = f"{strd}{TSV}"
                    fnam = (f"{fnam1}{fnam2}").lower()
                    save_allframe(frme, fnam2)
                    frme = (frme
                        .dropna(how='all')
                        .fillna(0)
                        .round(rnd)
                        .astype(typ)
                        .to_csv(
                            tsvpath.joinpath(fnam),
                            sep='\t',
                            )
                        )
                else:
                    raise ZerosFrameException()
            except ZerosFrameException:
                msg= f"Empty or zeros' frame for {strd}"
                logging.debug(f"{__name__}.{self}.{thisfunc()}: {msg}")



class MultiMapCounter(LengthCounter):
    """Class for making data-frame counters cataloging multimappers."""
    def __init__(self, label):
        super().__init__(label)
        self.cntlabl = MULMAP
        self.idxnam = REPS



class RegionLengthCounter(Counter):
    """Class for making data-frame counters cataloging region counts
    without strand information.

    Attributes
    ----------
    keycntr : pd.Series
        Series to hold counts with region info as index; named to **SHORT**
        name for counted sample; reset when merged, for counting another sample.
    idxnam : str
        Name for index column when dataframes get saved to **TSV**.
    cntlabl : str
        Label to mark type of counts in saved file name.
    """
    def __init__(self, label):
        super().__init__(label)
        self.dtype = float if not UNIQ in label else "Int64"
        self.rnd = 2 if not UNIQ in label else 0
        self._generate_frames()
        self.cntlabl = RLENCOUNTS
        self.idxnam = LENMER

    def _generate_frames(self):
        self._reset()
        self.fram = pd.DataFrame(dtype=float) #self.dtype)

    def _reset(self):
        self.keycntr = pd.Series(dtype=float) #self.dtype)

    def set_bincounts(self, cntidx, key):
        pass

    def merge_lencounters(self, key):
        """Merge key_length counters to count_frames then reset former.

        Parameters
        ----------
        key : str
            **SHORT** name of sample as column index (key) to collect counts
            for.
        """
        # merge
        self.fram = merg(
            self.fram, self.keycntr.to_frame(key)
            )#.astype(self.dtype)
        # reset
        self._reset()

    def update_strand_count(self, val, strand, lenreadidx):
        """Forward strand count to Series counter; ignore strand.

        Parameters
        ----------
        val : int or float
            Value to add to gathered counts.
        strand : str
            Name for strand where reads come from; not used.
        lenreadidx : index
            Index describing readlength to add counts to.
        """
        # pandas.Series used as counter
        s = self.keycntr
        try:
            s.loc[lenreadidx] += val
        except KeyError:
            s.loc[lenreadidx] = val

    def update_multimap_count(self, val, strand, lenreadidx):
        pass

    def get_lencount_frame(self):
        idx = self.idxnam
        rnd = self.rnd
        typ = self.dtype
        frme = self.fram.sort_index()
        try:
            if not (frme.empty or is_all_zero(frme)):
                frme.index.names = [f"{idx}"]
                frme = (frme
                    .dropna(how='all')
                    .fillna(0)
                    .round(rnd)
                    .astype(typ)
                    )
                return frme
            else:
                raise ZerosFrameException()
        except ZerosFrameException:
            msg= f"Empty or zeros' frame for {self.label}"
            logging.debug(f"{__name__}.{self}.{thisfunc()}: {msg}")

    def get_count_frame(self):
        """Generate total counts for region by summing length counts."""
        rnd = self.rnd
        typ = self.dtype
        nidx = self.label
        try: # for ZerosFrameException()
            infram = self.get_lencount_frame()
            infram.loc[nidx] = infram.sum(axis=0)
            outfram = infram.loc[nidx:].round(rnd).astype(typ)
            return(outfram)
        except AttributeError:
            pass

    def save_to_tsv(self, tsvpath, region, strand):
        """Save length frames for separate samples. Use lowercase filenames.

        Parameters
        ----------
        tsvpath : Path
            Path to folder to store **TSV** file with count information.
        region : str
            Formatted descriptor of genome span counted.
        strand : str
            One of **COMBI**, **PLUS** or **MINUS**;
        """
        nam = self.label
        labl = self.cntlabl
        fnam = (f"{nam}_{labl}_{region}_{strand}{TSV}").lower()
        fnam2 = (f"{nam}{COU}_{region}_{strand}{TSV}").lower()
        try:
            self.get_lencount_frame().to_csv(
                tsvpath.joinpath(fnam),
                sep='\t',
                )
            self.get_count_frame().to_csv(
                tsvpath.joinpath(fnam2),
                sep='\t',
                )
        except AttributeError:
            pass



class ZerosFrameException(Exception):
    pass
