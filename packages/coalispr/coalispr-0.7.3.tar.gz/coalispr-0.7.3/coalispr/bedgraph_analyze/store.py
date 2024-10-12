#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  store.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module for dealing with file storage and retrieval."""
import csv
import logging
import numpy as np
import pandas as pd
import shelve
import shutil

from itertools import zip_longest # to replace zip(), see:
# https://stackoverflow.com/questions/42297228/i-am-losing-values-when-i-use-the-zip-function-in-python-3
from pathlib import Path
from time import sleep

from coalispr.bedgraph_analyze.genom import (
    chroms,
    chr_test,
    )
from coalispr.bedgraph_analyze.process_bamdata import (
    count_folder,
    )
from coalispr.resources.constant import (
    BAK, BAM, BEDGRAPH,
    CONFBASE, CONFFOLDER,
    DATA, DATASTOR, DWNLDS,
    EXPFILE,
    FIGS,
    GROUPAVG,
    INPUTRCS,
    LOG2BG,
    MI, MINUS,
    OUTPUTS,
    P2TDELIM, PKL2TSV, PL, PLUS,
    READCOUNTS,
    SAMPLE, SAVEBAM, SAVEJPG, SAVEPNG, SAVESVG, SAVEPDF, SAVETSV,
    SHORT, STOREPATH, STOREPICKLE, SUBFIGS,
    TAG, TAGBAM, TAGCOLL, TAGUNCOLL, TMP, TOTALS, TOTINPUT, TSV, TSV2PKL,
    UNMAP, UNSPCGAPS, UNSPECLOG10, UNSPECIFIC, USEGAPS,
    )
from coalispr.resources.utilities import (
    get_tsvpath,
    replace_dot,
    replacelist,
    replacelist_list,
    thisfunc,
    timer,
    )

logger = logging.getLogger(__name__)


# Storage folders
# ---------------
def config_from_newdirs(exp, path):
    """Create storage folders during the initialization step ``coalispr init``.

    Returns
    -------
    Path
        Paths to storage folders linked to new experiment **EXP**.
    """
    datapath_ = path.joinpath(DATA, exp)
    picklpath_= datapath_.joinpath(STOREPICKLE)
    tsvpath_  = datapath_.joinpath(SAVETSV)
    bampath_  = datapath_.joinpath(SAVEBAM)
    downpath_ = path.joinpath(DWNLDS)
    figspath_ = path.joinpath(FIGS, exp)
    outpath_  = path.joinpath(OUTPUTS, exp)
    svgpath_  = figspath_.joinpath(SAVESVG)
    pngpath_  = figspath_.joinpath(SAVEPNG)
    pdfpath_  = figspath_.joinpath(SAVEPDF)
    jpgpath_  = figspath_.joinpath(SAVEJPG)
    confpath_ = path.joinpath(CONFBASE, CONFFOLDER)

    for npath in [confpath_, datapath_, picklpath_, tsvpath_, bampath_,
        figspath_, svgpath_, pngpath_, pdfpath_, jpgpath_, outpath_]:
        npath.mkdir(parents=True, exist_ok=True)

    for figmap in SUBFIGS:
        for path_ in [svgpath_, pngpath_, pdfpath_, jpgpath_]:
            pth = path_.joinpath(figmap)
            pth.mkdir(exist_ok=True)

    downpath_.mkdir(exist_ok=True)
    return confpath_


def get_unselected_folderpath(kind=UNSPECIFIC,tag=TAGCOLL):
    """Return path to folder with written bam files for unselected reads.

    Parameters
    ----------
    kind : str (default: **UNSPECIFIC**)
        Flag to indicate kind of specified reads to analyze, either specific or
        unspecific (default) for retrieving reads adhering to characteristics,
        when known, of specific RNAs.
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
        msg=(f"No bam-files found with:\n  '{pattern}'.")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return False
    # take first item as valid path
    folderpath = list(folderpath)[0]
    return  folderpath


# Store data
# ----------
# Access or set dict values via dict[key] rather than dict.get(key).
# Less buggy; the .get() only works for retrieval'''
def store_chromosome_data(name, plusdata, minusdata, tag, notag=False,
        otherpath=None):
    """Pickle binned bedgraph dataframes for easy access.

    Parameters
    ----------
    name : str
        Name for file to be stored.
    plusdata : object
        Data for plus strand.
    minusdata : object
        Data for minus strand.
    tag : str
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**.
    notag : bool
        Flag to indicate whether 'tag' needs an argument.
    otherpath : Path
        Path to storage location if different from default ``_get_storepath()``.

    Returns
    -------
    None
        Prints message upon completion of function
    """
    path_ = _get_storepath() if not otherpath else otherpath
    name_ = name  if notag else f'{name}_{tag}'
    name_ = replace_dot(name_)
    try:
        with shelve.open(str(path_.joinpath(f'{name_}.pkl'))) as db:
            db[f"{PL}{name_}"] = plusdata
            db[f"{MI}{name_}"] = minusdata
        msg = f"Pickle-file for '{name_}' saved"
    except FileNotFoundError:
        msg = f"Cannot store data as '{name_}'.pkl in '{path_}"
        raise SystemExit(msg)
    print(msg)
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")


def store_processed_chrindexes(name, chrnam, plusdata, minusdata, tag):
    """Pickle chromosomal indexfile tuples for easy access.

    Parameters
    ----------
    name : str
        Name for file to be stored.
    chrnam : str
        Name of chromosome for which data are stored.
    plusdata : object
        Data for plus strand of chromosome chrnam.
    minusdata : object
        Data for minus strand of chromosome chrnam.
    tag : str
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or **TAGCOLL**.

    Returns
    -------
    None
        Prints message upon completion of function.
    """
    path_ = _get_storepath()
    name_ = f'{name}_{tag}' if tag else name
    name_ = replace_dot(name_)
    try:
        with shelve.open(str(path_.joinpath(f"{name_}.pkl"))) as db:
            storedplusdata = db[f"{PL}{name_}"]
            storedminusdata = db[f"{MI}{name_}"]
    except KeyError:
        storedplusdata = {}
        storedminusdata = {}
        pass
    try:
        storedplusdata[chrnam] = plusdata
        storedminusdata[chrnam] = minusdata
        with shelve.open(str(path_.joinpath(f"{name_}.pkl"))) as db:
            db[f"{PL}{name_}"] = storedplusdata
            db[f"{MI}{name_}"] = storedminusdata
        msg = f"Saved index '{name_}.pkl' for chr. '{chrnam}'."
    except FileNotFoundError:
        msg = f"Cannot store data as {name_}.pkl in folder {path_}."
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)
    except KeyError:
        msg = "Key Error: No chromosome found, stopping..."
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)
    print(msg)



def store_chromosome_data_as_tsv(name, plusdata, minusdata, tag):
    """Store bedgraph or regions dataframes as tsv.

    Parameters
    ----------
    name : str
        Name for file to be stored.
    plusdata : object
        Data for plus strand.
    minusdata : object
        Data for minus strand.
    tag : str
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**.

    Returns
    -------
    None
        Prints message upon completion of function.
    """
    try:
        name_ = f'{name}_{tag}' if tag else name
        name_ = replace_dot(name_)
        path_ = _get_storepath(Path(STOREPATH).joinpath(SAVETSV,name_))

        for chrnam in chroms():
            plusdata[chrnam].to_csv(path_.joinpath(
            f"{chrnam}_{name_}_{PLUS}{TSV}"), sep="\t",
                quoting=csv.QUOTE_NONE, quotechar='"',escapechar='\\')
            minusdata[chrnam].to_csv(path_.joinpath(
            f"{chrnam}_{name_}_{MINUS}{TSV}"), sep="\t",
                quoting=csv.QUOTE_NONE, quotechar='"',escapechar='\\')
        msg = name,f"has been saved to {TSV} in {path_}"
    except Exception as e:
        msg = f"Sorry, nothing was saved because of:\n {e}"
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)


def _get_storepath(path_=None):
    """Return path to folder for storing pickled files."""
    if not path_:
        path_ = Path(STOREPATH) / STOREPICKLE
    else:
        path_ = Path(path_)
    if not path_.is_dir():
        path_.mkdir(parents=True, exist_ok=False)
        msg = f"Created '{path_}'."
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
    return path_


def save_average_table(df, name, use, samples, bam=TAGCOLL, segments=TAGUNCOLL,
    overmax=LOG2BG, maincut=UNSPECLOG10, usegaps=USEGAPS):
    """Save averaged count tables with given keywords in the folder/filename.

    Parameters
    ----------
    name : str
        Name of filename for output table to save; is equal to figure name.
    use : str (default: **SPECIFIC**)
        What type of counted reads to use, i.e. **SPECIFIC** or **UNSPECIFIC**.
    samples : list
        List of library samples used for averaging dataframe.
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
    """
    usegaps = UNSPCGAPS if use == UNSPECIFIC else USEGAPS
    use_folder = count_folder(use, bam, segments, overmax, maincut, usegaps)
    p_ = get_tsvpath().joinpath(use_folder, GROUPAVG)
    try:
        if not p_.is_dir():
            p_.mkdir(parents=True, exist_ok=False)
        df.round(2).to_csv(p_.joinpath(name+TSV), sep='\t', na_rep='0',)
        print(f"\nTable with averages saved in folder '{p_}'.")
        # save samples
        samplenam = name+"_samples"+TSV
        with open(p_.joinpath(samplenam), 'w', newline='') as csvfile:
            samplewriter = csv.writer(
                csvfile,
                delimiter='\t',
                quoting=csv.QUOTE_NONE)
            samplewriter.writerow(samples)
    except IndexError as e:
        msg = ("Sorry, no files saved at '{p_}'.")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}\n{e}")
        raise SystemExit(msg)
    except FileNotFoundError:
        msg = (f"Sorry, no such file '{name+TSV}' or storage folder "
            f"\n\t'{use_folder}/{GROUPAVG}'.")
        raise SystemExit(msg)




# Retrieve data
# -------------
def retrieve_merged(tag=TAG):
    """Retrieve the merged experimental data.

    Parameters
    ----------
    tag : str
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**.

    Returns
    -------
    dict of pandas.DataFrames, dict of pandas.DataFrames
        A tuple of dicts, one for each strand, with pandas dataframes, one for
        each chromosome, with columns of bedgraph values summed per **BINSET**
        for each sample.
    """
    global _plus_mergd
    global _minus_mergd
    try:
        if tag != TAG:
            return retrieve_processed_files('merged', tag=tag)
        else:
            return _plus_mergd, _minus_mergd
    except NameError:
        _plus_mergd, _minus_mergd = retrieve_processed_files('merged', tag=TAG)
    return _plus_mergd, _minus_mergd


def retrieve_processed_files(name, tag, notag=False):
    """Retrieve experimental data from pickle files.

    Defines internal class ``FileTooShortWarning(Exception)``


    Parameters
    ----------
    name : str
        Name for file
    tag : str
        Flag **TAG** to indicate kind of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**.
    notag : bool
        Flag to indicate whether 'tag' needs an argument.

    Raises
    ------
    FileTooShortWarning
        Raised when stored file has no significant size; previous file writing
        was inadequate.

    Returns
    -------
    dict, dict
        A tuple of dicts, one for each strand, with data structures, one for
        each chromosome.
    """

    class FileTooShortWarning(Exception):
       pass

    plusdata = {}
    minusdata = {}
    try:
        name_ = name  if notag else f'{name}_{tag}'
        name_ = replace_dot(name_)
        file_to_load = _get_storepath().joinpath(f"{name_}.pkl")
        if file_to_load.stat().st_size < 50:  #(50 bytes)
            raise FileTooShortWarning(file_to_load)
        with shelve.open(str(file_to_load)) as db:
            # https://github.com/pandas-dev/pandas/issues/53300
        #with pd.read_pickle(str(file_to_load)) as db:
        #with pd.compat.pickle_compat.load(str(file_to_load)) as db:
            plusdata =  db[f"{PL}{name_}"]
            #plusdata = db.get(f"{PL}{name}") #works as well here
            minusdata =  db[f"{MI}{name_}"]
    except FileNotFoundError:
        # possibly no files on first run
        if not file_to_load.exists():
            msg = (f"File {file_to_load} did not (yet) exist, "
                "returned {} {}")
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            return {}, {}
        msg = (f"Loading {file_to_load} gives {file_to_load.is_file()} in "
                "retrieve_processed_files")
        raise SystemExit(msg)
    except KeyError:
        msg = (f"(minus or) plusdata entry for {name_} not found in "
                "retrieve_processed_files")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)
    except FileTooShortWarning:
        msg = (f"{file_to_load}  is too small; check writer function")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)

    return plusdata, minusdata


def _stored_pickles(wholepath = False):
    """Return names of pickled files that have been stored."""
    path_ = _get_storepath()
    print(f"Pickles in: {path_}?")
    if not wholepath:
        return (path_.stem for path_ in path_.glob('**/*.pkl')) # generator
    else:
        return (path for path in path_.glob('**/*.pkl'))


def _check(listofkeys, testfil=None):
    """Assess whether keys are present in merged data."""
    testfil = retrieve_merged()[0] if not testfil else testfil
    result = []
    try:
        result = [ key for key in listofkeys
            if key in testfil[chr_test()].columns ]
            #if key in _plus_mergd.get(chr_test()).columns ] # works as well
        return result
    except KeyError:
        msg = 'Nothing to do'
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return result


def retrieve_merged_unselected():
    """Returns merged unselected data, organized per binned chromosome."""
    global _unsel1, _unsel2
    try:
        return _unsel1, _unsel2
    except NameError:
        _unsel1, _unsel2 = retrieve_processed_files('unselected_merged',
            tag=TAGBAM, notag=False)
    return _unsel1, _unsel2


def get_inputtotals(kind=TAGUNCOLL):
    """Returns total input counts from saved files.

    Parameters
    ----------
    kind : str
        Type of reads, **TAGUNCOLL** or **TAGCOLL**.
    """
    tsvpath = Path(STOREPATH).joinpath(SAVETSV, TOTINPUT)

    try:
        df = pd.read_csv(tsvpath.joinpath(f"{TOTALS}_{kind}{TSV}"),
            sep="\t", comment="#", header=[0], index_col=[0],
            skipinitialspace=False, dtype={SAMPLE: str,
            PLUS: np.int64, MINUS: np.int64, UNMAP: np.int64})
        return df
    except FileNotFoundError as e:
        msg = (f"No input found from {INPUTRCS}; did that step complete?")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}\n{e}")
        raise SystemExit(msg)


# Backup
# ------
def _backupdir(path_, moveit=False):
        return _backup(path_, moveit, dircpy=True)


def _backup(path_, moveit=False, dircpy=False):
    """Keep folder with original data when these will be changed"""
    backup = path_.with_suffix(BAK)
    if not backup.exists():
        print(f"  ..making a backup of '{path_.name}' ..")
        if moveit:
            print(f"  by renaming to '{backup.name}'.")
            shutil.move(path_, backup)
        elif dircpy:
            print("  which is a directory ..")
            shutil.copytree(path_, backup)
        else:
            shutil.copy(path_, backup)
    return True


def backup_pickle_to_tsv(data_only=False, merged_only=False):
    """Convert binary bedgraph-data to text; skip indexes-only files.

    Returns
    -------
    None
        Prints message upon completion of function
    """
    #msg = "   Files with only an index are skipped, can be regenerated."
    #print(msg)
    pickled = False
    pickles = list(_stored_pickles())
    if len(pickles) == 0:
        msg=(f"No pickled data found to convert to {TSV}; has data been stored?"
          f" (check {DATASTOR})\n")

    for pkl in pickles:
        _pickle_to_tsv(pkl, data_only, merged_only)
        pickled = True

    if pickled:
        msg=(f"Pickled data converted to '{TSV}' format.\n")
    print(msg)
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")


def _pickle_to_tsv(name, data_only, merged_only):
    """For more permanent/exchangeable storage of processed data."""

    if ("data" in name or "merged" in name):
        msg = f"Converting '{name}.pkl' to {TSV} .."
        print(f"{name} ..")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    # skip indexes; name.startswith('idx_'), or contains an UNSPECLOG10 value.
    else:
        msg = f"   Skipped index '{name}.pkl'."
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return

    plusdata = {}
    minusdata = {}

    try:
        name_ = replace_dot(name)
        file_to_load = _get_storepath().joinpath(f"{name_}.pkl")
        path_ = _get_storepath(Path(STOREPATH / PKL2TSV / name_))

    except FileNotFoundError:
        msg = f"Sorry, '{file_to_load}' not found."
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)

    try:
        with shelve.open(str(file_to_load)) as db:
            plusdata =  db[f"{PL}{name_}"]
            minusdata =  db[f"{MI}{name_}"]
            # merged data
            if 'merged' in name_ and not 'data' in name_ and not data_only:
                for chrnam in chroms():
                    plusdata[chrnam].to_csv(path_.joinpath(
                    f'{chrnam}{P2TDELIM}{name_}{P2TDELIM}{PLUS}{TSV}'),
                        sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                        escapechar='\\')
                    minusdata[chrnam].to_csv(path_.joinpath(
                    f'{chrnam}{P2TDELIM}{name_}{P2TDELIM}{MINUS}{TSV}'),
                        sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                        escapechar='\\')

                msg = f"   .. merged data of '{name_}.pkl' converted."
            # processed bedgraphs
            elif 'data' in name_ and not merged_only:
                for sample in plusdata.keys():
                    for chrnam in chroms():
                        # bits tsv.stem: sample   chrnam   name/datakind   strand
                        plusdata[sample][chrnam].to_csv(path_.joinpath(
                        f'{sample}{P2TDELIM}{chrnam}{P2TDELIM}{name_}{P2TDELIM}{PLUS}{TSV}'),
                            sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                            escapechar='\\')
                        minusdata[sample][chrnam].to_csv(path_.joinpath(
                        f'{sample}{P2TDELIM}{chrnam}{P2TDELIM}{name_}{P2TDELIM}{MINUS}{TSV}'),
                            sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                            escapechar='\\')
                msg = f"   .. bedgraph-data in '{name_}.pkl' converted."
            else:
                msg = f"   ..'{name_}.pkl' was skipped and not converted."
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    except KeyError as k:
        msg = (f"No (minus- or) plusdata entry for file '{name_}' found during "
               f"'{thisfunc()}'.\n(key error); {k}")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)


def _stored_folders_with_tsv_from_pickles():
    """Return names of folders with tsv files of backed-up data pickles"""
    try:
        path_ = Path(STOREPATH) / PKL2TSV
        return (path.stem for path in path_.glob('*data*')) # generator

    except FileNotFoundError:
        msg=(f"No backup folder ('{path_}') found.\nHave you created a text "
        f"copy of the stored binary data? (see {DATASTOR})\n")
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")


def _stored_tsv_from_pickles(fldrnam):
    """Return names of tsv files that represent backed-up data pickles"""
    try:
        path_ = Path(STOREPATH) / PKL2TSV / fldrnam
        pat = f'*{TSV}'
        return path_.glob(pat) # generator

    except FileNotFoundError:
        msg=f"Sorry, no {fldrnam} with {TSV} files found in ('{path_}')."
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")


@timer
def pickle_from_backup_tsv():
    """Restore binary bedgraph-data from text files. This will replace
    original **STOREPICKLE** contents.

    Returns
    -------
    None
        Prints message upon completion of function
    """
    pickled = False
    backedup = False
    oripath = Path(STOREPATH) / STOREPICKLE
    if oripath.exists() and not oripath.is_symlink():
        backedup = _backupdir(oripath, moveit=True)
    else:
        backedup = True

    repickl = Path(STOREPATH) / TSV2PKL

    def relink(t):
        sleep(t)
        oripath.symlink_to(repickl, target_is_directory=True)

    if backedup:
        print(f"\nConverting {TSV} files in '{PKL2TSV}' to .pkl ..")
        for tsvfldr in _stored_folders_with_tsv_from_pickles():
            tsvfldr_ = tsvfldr # string; remember passed-in generator item
            filnam = f"{tsvfldr_}.pkl"
            msg = f"Building '{filnam}' .."
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
            if "data" in tsvfldr_:
                _pickle_datatsv(filnam, tsvfldr_)
            else:
                continue
            pickled = True

    if pickled:
        if oripath.is_symlink():
            oripath.unlink(missing_ok=True)
        try:
            relink(0.1)
        except FileExistsError:
            relink(10)
        msg = f"Original '{STOREPICKLE}' replaced with a link to '{TSV2PKL}'\n"
        print(msg)
    elif not pickled:
        msg=(f"No {TSV} files found to convert to .pkl; is there a backup of "
          f"stored binary data? (check {DATASTOR})\n")
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    return pickled


'''
 def _pickle_mergedtsv(filnam, tsvfldr):
    """Create .pkl for merged data with column headers for each sample"""
    #for tsv in _stored_tsv_from_pickles(tsvfldr):
    #    print(tsv)
'''


def _pickle_datatsv(filnam, tsvfldr):
    """Create .pkl for data (dataframe for each sample)"""
    #print(tsvfldr)
    path = _get_storepath(Path(STOREPATH).joinpath(TSV2PKL)) / filnam
    filnamdir = {f"{PL}{tsvfldr}":{}, f"{MI}{tsvfldr}":{}}

    # build data structure
    for tsv in _stored_tsv_from_pickles(tsvfldr):
        tsv_= tsv
        df = pd.read_csv(tsv_, comment="#",sep="\t", index_col=0)
        # bits tsv.stem: sample   chrnam   datakind   strand
        # bits tsv.stem: "rha1A2_2- extra_ data_collapsed -plus"
        # bits tsv.stem: "j21-a1- 10_ reference_data -plus"
        # bits tsv.stem: "A2n_1- mmu-45S_ENA-X82564_ data_collapsed -minus"
        tsvbits = tsv_.stem.rsplit(P2TDELIM) #('-', maxsplit=2)
        sample = tsvbits[0]
        chrnam = tsvbits[1] #.split(f'_{tsvfldr}')[0]
        strd = tsvbits[-1][0]
        if not strd in [PL,MI]:
            raise SystemExit(f"Strand name '{strd}' does not fit current "
             f" storage configuration (**PL**: '{PL}' and **MI**: '{MI}'")
        try:
            sampledir = filnamdir[f"{strd}{tsvfldr}"][sample]
        except KeyError: # happens when sample folder is not yet initiated
            filnamdir[f"{strd}{tsvfldr}"][sample] = {}
            sampledir = filnamdir[f"{strd}{tsvfldr}"][sample]
            #msg = f"Initiated missing folder in 'filnamdir' for '{sample}'."
            #logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        sampledir[chrnam] = df

    with shelve.open(str(path)) as db:
        db[f"{PL}{tsvfldr}"] = filnamdir[f"{PL}{tsvfldr}"]
        db[f"{MI}{tsvfldr}"] = filnamdir[f"{MI}{tsvfldr}"]




'''
def _tsv_to_pickle(name):
    """For restoring binary data from more permanent/exchangeable storage."""
    # skip indexes
    if name.startswith('idx_'):
        msg = f"Skipped index '{name}.pkl' (can be regenerated)"
        #print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        return
    else:
        print(f"Name of file to store as {TSV}: {name}.")

    plusdata = {}
    minusdata = {}

    try:
        name_ = replace_dot(name)
        file_to_load = _get_storepath().joinpath(f"{name_}.pkl")
        path_ = _get_storepath(Path(STOREPATH / PKL2TSV / name_))

    except FileNotFoundError:
        msg = f"Sorry, '{file_to_load}' not found."
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)

    try:
        with shelve.open(str(file_to_load)) as db:
            plusdata =  db[f"{PL}{name_}"]
            minusdata =  db[f"{MI}{name_}"]
            # merged data
            if 'merged' in name_ and not 'data' in name_:
                for chrnam in chroms():
                    plusdata[chrnam].to_csv(path_.
                        joinpath(f'{chrnam}_{name_}-{PLUS}{TSV}'),
                        sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                        escapechar='\\')
                    minusdata[chrnam].to_csv(path_.
                        joinpath(f'{chrnam}_{name_}-{MINUS}{TSV}'),
                        sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                        escapechar='\\')
            # processed bedgraphs
            elif 'data' in name_:
                for sample in plusdata.keys():
                    for chrnam in chroms():
                        plusdata[sample][chrnam].to_csv(path_.
                            joinpath(f'{sample}-{chrnam}_{name_}-{PLUS}{TSV}'),
                            sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                            escapechar='\\')
                        minusdata[sample][chrnam].to_csv(path_.
                            joinpath(f'{sample}-{chrnam}_{name_}-{MINUS}{TSV}'),
                            sep="\t", quoting=csv.QUOTE_NONE, quotechar='"',
                            escapechar='\\')
    except KeyError as k:
        msg = (f"No (minus- or) plusdata entry for file '{name_}' found during "
               f"'{thisfunc()}'.\n(key error); {k}")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
        raise SystemExit(msg)
'''

# Change sample name
# ------------------
# only use text files, not binary, for editing
def rename_in_data_tsv(names_old_new):
    """Replace sample names in data files that were pickled.

    Parameters
    ----------
    names_old_new: list of tuples: [(old_name1, new_name1),
        (old_name2, new_name2),]

    Returns
    -------
    boolean expressing completion.

    """
    path_ = Path(STOREPATH) / PKL2TSV

    for tsvrootdir in path_.glob('*'): # generator
        tsvrootdir_ = tsvrootdir # remember and use up passed-in generator item
        if 'data' in tsvrootdir_.stem:
            _rename_in_datatsv(tsvrootdir, names_old_new)
        #else:
        #    _rename_in_othtsv(tsvrootdir, names_old_new)
    return True


def _rename_in_datatsv(rootdir, names_old_new):
    """Recursively replace names in data files
    https://stackoverflow.com/questions/4205854/recursively-find-and-replace-string-in-text-files
    by Kentgrav, Ufos
    """
    for filein in rootdir.rglob(f"*{TSV}"): #generator
        filein_ = filein
        for namtupl in names_old_new:
            if namtupl[0] in filein_.stem:
                filein__ = _rename_filename(filein_, namtupl)
                #filein__ = Path(f"{filein_.parent}").joinpath(
                #f"{filein_.stem.replace(namtupl[0],namtupl[1])}{TSV}")
                #filein_.replace(filein__)
                _rename_sample(filein__, names_old_new)
    return True


def _rename_filename(filein_, namtupl):
    filein__ = Path(f"{filein_.parent}").joinpath(
    f"{filein_.stem.replace(namtupl[0],namtupl[1])}{filein_.suffix}")
    filein_.replace(filein__)
    return filein__

'''
def _rename_in_othtsv(rootdir, names_old_new):
    """Recursively replace names in other files"""
    for filein in rootdir.rglob(f"*{TSV}"): #generator
        _rename_sample(filein, names_old_new)
    return True
'''

def rename_unselected(names_old_new, tag=None):
    """Replace sample in file names

    Parameters
    ----------
    names_old_new: list of tuples: [(old_name1, new_name1),
        (old_name2, new_name2),]
    tag : str
        Flag **TAG** to indicate ``kind`` of aligned-reads, **TAGUNCOLL** or
        **TAGCOLL**. Comes from counted bam files, which -for efficiency
        reasons- could be expected to be containing collapsed reads
        (**TAGCOLL**).

    Returns
    -------
    boolean expressing completion.

    """
    tag = TAGCOLL  if tag == None else tag
    kind = UNSPECIFIC
    path_ = get_unselected_folderpath(kind,tag)
    _backupdir(path_)

    bams = list(path_.glob(f"*{BAM}"))
    bais = list(path_.glob(f"*{BAM}.*"))
    babas = bais + bams
    print(len(babas))
    for filein in babas: #generator
        filein_ = filein
        for namtupl in names_old_new:
            if namtupl[0] in filein_.stem:
                filein__ = _rename_filename(filein_, namtupl)
                print(filein__)

    bgpaths = set(path_.glob(f"bedgraphs_{UNSPECIFIC.lower()}*/"))
    print(bgpaths)

    bgpath = list(bgpaths)[0]
    for bgfilein in bgpath.glob(f"u_*{BEDGRAPH}"): #generator
        bgfilein_ = bgfilein
        for namtupl in names_old_new:
            if namtupl[0] in bgfilein_.stem:
                bgfilein__ = _rename_filename(bgfilein_, namtupl)
                print(bgfilein__)
    return True


@timer
def rename_in_count_tsv(names_old_new):
    """Replace sample names in count files.

    Parameters
    ----------
    names_old_new: list of tuples: [(old_name1, new_name1),
        (old_name2, new_name2),]

    Returns
    -------
    boolean expressing completion.
    """
    path_ = Path(STOREPATH) / SAVETSV
    _backupdir(path_)
    for filein in path_.rglob(f'*{TSV}'):
        _rename_sample(filein, names_old_new)
    return True


def _rename_sample(filein, names_old_new):
    filein_ = filein
    temp = filein_.with_suffix(TMP)
    try:
        shutil.move(filein_, temp)
        with temp.open("r") as fin: # "rb" when stream opened as bytestream
            with filein_.open("w") as fileout: # "wb" for bytestream
                for line in fin:
                    fileout.write(replacelist(line,names_old_new))
        temp.unlink(missing_ok=True)
    except FileNotFoundError as e:
        logging.debug(f"{__name__}.{thisfunc()}:\n{e}")


def rename_in_expfile(names_old_new):
    """Replace sample names in experiment file **EXPFILE**.

    Parameters
    ----------
    names_old_new: list of tuples: [(old_name1, new_name1),
        (old_name2, new_name2),]

    Returns
    -------
    boolean expressing completion.
    """
    path_ = Path(EXPFILE)
    _backup(path_)
    temp = path_.with_suffix(TMP)

    try:
        shutil.move(path_, temp)
        with open(temp) as infil:
            reader = csv.reader(infil, delimiter="\t")
            as_columns = zip_longest(*reader)
            as_rows = []
            for row in as_columns:
                if SHORT in row:
                    # row is non-changeable tuple, use an intermediate list
                    row = tuple(replacelist_list(list(row), names_old_new))
                as_rows.append(row)
            # restore to list with each print line as tuple
            as_rows = list(zip_longest(*as_rows))
        temp.unlink(missing_ok=True)

        with open(path_, 'w', newline='') as outfil:
            writer = csv.writer(outfil, delimiter="\t",
                quoting=csv.QUOTE_NONE, quotechar='"',escapechar='\\')
            for line in as_rows:
                writer.writerow(line)
        temp.unlink(missing_ok=True)

    except FileNotFoundError as e:
        logging.debug(f"{__name__}.{thisfunc()}:\n{e}")

    return True


# Memory usage
# ------------
def print_memory_usage_merged():
    """Show pandas memory usage of merged data frames.

    Returns
    -------
    floats
        Floats describing (in MBs) memory usage of reference, **TAGCOLL** or
        **TAGUNCOLL** datasets in Pandas.
    """
    def _usage():
        nonlocal plus, minus
        strands = {strand: pd.concat(chrnam, axis=0) for strand, chrnam
                in {PLUS:plus, MINUS:minus}.items() }
        genomdf = pd.concat(strands, axis =0)
        usage_MB = genomdf.memory_usage().sum(axis =0) / 1000000
        return usage_MB


    plus, minus = retrieve_processed_files('reference_merged', tag=None,
        notag=True)
    if plus:
        print("Calculating memory-usage for reference")
        msg = f"\tUsage reference:\t{_usage():,.2f} MB"
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    for tag in [ TAGCOLL, TAGUNCOLL,]:
        print(f"Calculating memory-usage for {tag} aligned-reads")
        plus, minus = retrieve_merged(tag=tag)
        if plus:
            msg = f"\tUsage {tag} data:\t{_usage():,.2f} MB"
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
