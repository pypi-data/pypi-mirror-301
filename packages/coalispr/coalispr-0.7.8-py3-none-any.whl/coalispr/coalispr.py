#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  coalispr.py
#
#  Copyright 2021-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
__author__      = "Rob van Nues"
__copyright__   = "Copyright 2020-2024"
__version__     = "0.5.5"  # sync with pyproject.toml
__credits__     = ["Rob van Nues"]
__maintainer__  = "Rob van Nues"
__email__       = "sborg63@disroot.org"
__status__      = "beta"


"""Coalispr aim, usage, commands and options

This program allows comparison of many bedgraphs at once; it enables removal
of background noise by means of a negative control; it enables fast counting
of thus specified reads. Bedgraphs and the outcome of operations are
visualized interactively for obtaining an overview. All processed data is saved
to text files as .tsv (tab-separated-value) for follow-up analyses.


Usage
-----
    ``coalispr init``
    ``coalispr setexp -e``
    ``coalispr storedata -d``
    ``coalispr showgraphs -c``
    ``coalispr countbams``
    ``coalispr showcounts``
    ``coalispr region -c -r``
    ``coalispr annotate``
    ``coalispr groupcompare -g``
    ``coalispr info``
    ``coalispr -h | --help``
    ``coalispr --version``
    ``coalispr test``

Commands
--------
    ``init``
        Set up Coalispr work folder and name session/experiment.
    ``setexp``
        Set experiment -e according to configuration files at path -p.
    ``storedata``
        Store bedgraphs files -d, or backup/edit as **TSV**.
    ``showgraphs``
        Show bedgraphs for chromosome -c.
    ``countbams``
        Count bam files for reads using **TAGSEG** segments found in **TAGBAM**
        bedgraphs; select for kind -k; write counted alignments to new bam files
        (-wb); find **UNSEL** reads in **TAGCOLL** data of kind **UNSPECIFIC**
        (-u). Tolerate point-deletions (-pd) or mismatches (-mm). Force
        counting (-f).
    ``showcounts``
        Show diagrams with count results: Get total raw counts (-rc) for
        mapped and unmapped reads. Display total library counts (-lc), as log2
        (-lg), length distribution (-ld, -lo), frequency of multimapper-hits
        (-md, -mo); chose kind of read (**SPECIFIC** or **UNSPECIFIC**) (-k) or
        mapper (**UNIQ** or **MULMAP**)(-ma), group (**CATEGORY**, **METHOD**,
        **FRACTION**)(-g), to display with/without titles (-nt), or excluded
        samples (-x).
    ``region`
        For a  region of chromosome -c, check distribution of read-lengths -dl
        for all (**LIBR** (1), **COLLR** (2) or **UNIQ** (-ma) reads in
        samples -s (controls (1), including mutants (2) or a selection (3)).
        Tolerate point-deletions (-pd) or mismatches (-mm)."
    ``annotate``
        Display read counts with annotations extracted from **GTF**.
    ``groupcompare``
        Compare lengths between reads for grouped library samples.
    ``info``
        Show paths to configuration files, or the experiment file (-p), display
        the effect of various parameter settings on the number of regions with
        specified reads (-r), show experiment name, or calculate memory use
        in Pandas of processed data (-i).
    ``test``
        Test or profile (-fu) commands of coalispr with -no lines of report
        output.


"""
import logging
import shutil
import sys

from io import StringIO
from logging.handlers import RotatingFileHandler
from pathlib import Path
from traceback import format_exc

from coalispr.bedgraph_analyze.process_bedgraphs import (
    merge_sets,
    process_graphs,
    process_reference,
    show_chr,
    show_unspecific_chr,
    show_specific_chr,
    )
from coalispr.bedgraph_analyze.compare import (
    gather_all_specific_regions,
    gather_all_unspecific_regions,
    test_intervals,
    )
from coalispr.bedgraph_analyze.experiment import (
    all_exps,
    controls,
    discarded,
    goption,
    has_discards,
    has_grouparg,
    has_redundant_muts,
    negative,
    mixed_groups,
    mutant, mutant_groups,
    positive,
    reference,
    )
from coalispr.bedgraph_analyze.genom import (
    chroms,
    )
from coalispr.bedgraph_analyze.info_plots import (
    show_regions_vs_settings,
    show_mapped_vs_unmapped,
    )
from coalispr.bedgraph_analyze.process_bamdata import (
    has_been_counted,
    num_counted_libs,
    process_bamfiles,
    process_reads_for_region,
    total_raw_counts,
    )
from coalispr.bedgraph_analyze.store import (
    backup_pickle_to_tsv,
    config_from_newdirs,
    pickle_from_backup_tsv,
    print_memory_usage_merged,
    rename_in_count_tsv,
    rename_in_data_tsv,
    rename_in_expfile,
    rename_unselected,
    )
from coalispr.bedgraph_analyze.unselected import (
    merge_unsel,
    process_unselected,
    )
from coalispr.count_analyze.annot import (
    annotate_libtotals,
    )
from coalispr.count_analyze.countfile_plots import (
    compare_exp_bins,
    compare_exp_lengths,
    compare_exp_mulmaps,
    compare_libtotals,
    compare_un_spec_lengths,
    compare_un_spec_mulmaps,
    )
from coalispr.count_analyze.groupcompare_plots import (
    compare_5nt_lengths,
    )
from coalispr.count_analyze.regioncount_plots import (
    plot_regioncounts,
    plot_regionlengths,
    )
from coalispr.resources.cmd_parser import (
    make_parser,
    )
from coalispr.resources.constant import (
    ALL,
    BAK, BAMPEAK, BAMSTART, BCO, BINS,
    CATEGORY, CHRXTRA,
    CIGFM, CIGPD, COLLR, COMBI,
    CONFBASE, CONFFILE,
    CONFFOLDER, CONFPATH, CORB,
    DISCARD,
    EXP, EXPFILE, EXPTXT,
    INTR,
    JPG,
    LIBR,
    LOGFIL, LOGMAX,
    MAXMM, MEAN, MEDIAN, MINUS, MULMAP, MUNR, MUTANT, MUTANTS,
    NEGCTL, NRMISM,
    PDF, PLUS, PNG, POSCTL,
    REST,
    SAVEBAM, SHARED, SKIP, SPECIFIC, SVG,
    TAG, TAGBAM, TAGCOLL, TAGSEG, TAGUNCOLL, TSV,
    UNIQ, UNSEL, UNSPECIFIC,
    XLIM0, XLIM00, XLIM1, XLIM11, XLIMR0, XLIMR1, XTRA,
    )
from coalispr.resources.constant_in.make_constant import (
    make_constant,
    )
from coalispr.resources.dialog import (
    assemble_groupsamples,
    collect_limits,
    get_experiment_name,
    get_old_new_samplenames,
    select_from,
    suggest_storepath,
    )
from coalispr.resources.utilities import (
    chrom_region,
    joinall,
    joiner,
    replacelist_list,
    thisfunc,
    )


def _start_logging():
    """Log events that could point to improvement"""
    if not Path(LOGFIL).parent.is_dir():
       Path(LOGFIL).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        datefmt='%Y-%m-%d %H:%M:%S',
        format='{asctime} {name} {levelname}: {message}',
        style='{',
        level=logging.DEBUG,
        handlers=[RotatingFileHandler(
            LOGFIL,
            maxBytes=LOGMAX,
            backupCount=4
            )],
        )
    return logging.getLogger(__name__)


def _mismatches(args_mism):
    choices_ = [x for x in range(NRMISM,MAXMM+1)]
    if not args_mism in choices_:
        msg = (f"Given choice ({args_mism}) not expected, "
            f"will be using default number ({NRMISM}).")
        logging.debug(f"{__name__}.{thisfunc()}: {msg}")
        print(msg)
        return NRMISM
    else:
        return args_mism


def _possible_samples(has_disc, has_redmuts):
    options = [{POSCTL: positive()},
               {NEGCTL: negative()},]

    if MUTANTS:
        options.append({MUTANT: mutant(allmut=has_redmuts)})
    if has_disc:
        options.append({DISCARD: discarded()})
    return options


def _get_samples(args_samplechoice, has_redmuts, has_disc):
    if args_samplechoice == 3:
        # start from controls() + mutant(True) + discarded()
        samples = select_from(_possible_samples(has_disc, has_redmuts))
    elif args_samplechoice in [1,2]:
        samples = {1: controls(),
                   2: controls() + mutant(has_redmuts),
                  }[args_samplechoice]
        if has_disc:
            samples += discarded()
    return samples


def init(args):
    """Execute command ``coalispr init``

    Name session/experiment and set up Coalispr work folder for storage of
    Coalispr-linked files. It is the place for keeping processed data (pickle,
    **TSV** or image files) and logs. Before continuation, the configuration
    files in ``config/constant_in`` (**CONFPATH**) have to be adapted.
    """
    p_ = Path(__file__).parent.joinpath('resources','constant_in')
    exp_ = get_experiment_name()
    if exp_:
        path_ = suggest_storepath()
    else:
        raise SystemExit(
            "\tSorry, need experiment name, setup aborted.\n")
    if not path_:
        raise SystemExit(
            "\t" + f"No storage path for '{exp_}', setup canceled.\n")

    newexptxt = f'3_{exp_}.txt'
    n=0

    def _isbackedup(pathtofile):
        nonlocal n
        if pathtofile.is_file():
            p = pathtofile.with_suffix(BAK)
            if p.is_file():
                print("An old backup was found.")
                n += 1
                pn = p.with_suffix(f"{BAK}{n}")
                shutil.copy2(p,pn)
                if not _isbackedup(pn):
                    return
            shutil.copy2(pathtofile, p)
            return True
        return False


    def _editconf():
        try:
            nonlocal exp_
            replaced = ''

            with open(p_.joinpath(EXPTXT), 'r') as f:
                file_source = f.read()
                #set path: replace ###SAVEIN_BY_INIT
                replaced = file_source.replace('###SAVEIN_BY_INIT', f'{path_}')
                #set experiment: replace ###EXP_BY_INIT
                replaced = replaced.replace('###EXP_BY_INIT', exp_)
                #set workfolder environment: replace ###SETBASE_BY_INIT
                replaced = replaced.replace('###SETBASE_BY_INIT', f'{path_.parent}')

            with open(newconf, 'w') as f:
                #save output
                f.write(replaced)
        except:
            print("\nSorry, something went wrong; please make this change "
                  "manually")
            pass

    confpath_ = config_from_newdirs(exp_, path_)
    #back_up previous config, if any.
    newconf = confpath_.joinpath(newexptxt)


    # copy over configuration templates
    fileparts = [ SHARED, EXPTXT ]
    if confpath_.is_dir():
        msg = f"A previous '{newexptxt}' was backed up. \n"
        msg = msg if _isbackedup(newconf) else ""
        for f in fileparts:
            try:
                shutil.copy(p_.joinpath(f), confpath_)
            except shutil.SameFileError:
                err=(f"File {f} already exists, pass.")
                logging.debug(f"{__name__}.{thisfunc()}: {err}")
                pass
        msg += (f"\nConfiguration files to edit are in: \n   {confpath_}"
              f"\n'SAVEIN' in '{newexptxt}' is set to:\n   {path_}")
        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}: {msg}")

    _editconf()


def setexp(args):
    """Execute command ``coalispr setexp``

    Set the name for experiment/session.

    This command sets and recalls the context of a coalispr session.
    It uses the session or experiment name, the value configured for **EXP** in
    an associated descriptor file (**CONSTANT**), and gathers all other
    information stored in that file. Such a file, with valid entries (i.e. files
    are where they are described to be), is required for coalispr to work.

    The result of the command is a configuration file, ``constant.py``, that is
    stored on disk and in memory. The ``constant.py`` guides analysis done in a
    session.

    Another session with another experiment can be started in another terminal,
    using this command. Note that this changes what configuration links to
    ``coalispr.resources.constant.py`` and determines the next 'default' context
    for ``coalispr``.

    Options
    -------
    -e  str

        Name of the experiment/session
    -p  {1,2}

        Path to ``3_EXP.txt``, which is now in **CONFPATH**; 1: Use this;
        2: Find it in another Coalispr work-folder. (default: 1)
    """
    otherpath = CONFPATH

    if EXP != args.experiment:
        print(f"\nCurrent session with experiment '{EXP}'; will be changed to "
        f"'{args.experiment}'.")

    if args.configpath == 2:
        print("\nCurrent path to configuration files will be changed:")
        path_ = suggest_storepath()
        if not path_:
            raise SystemExit("\n\tNo path configured, aborting..")
        else:
            otherpath = path_.joinpath(CONFBASE,CONFFOLDER)
    elif args.configpath == 1:
        otherpath = CONFPATH

    if not otherpath:
        msg = (f"\nPath given is '{otherpath}'; sorry, this is unusable.")
        logging.debug(f"{__name__}.{thisfunc()}: {msg}")
        raise SystemExit(msg)

    make_constant(exp=args.experiment, otherpath=otherpath)


def storedata(args):
    """Execute command ``coalispr storedata``

    Parse bedgraphs files -f for type alignments -t and store them into pandas
    dataframes using a quick assessible, binary format. Create **TSV** files
    with segment boundaries of specified aligned-reads, or as backups from
    pickled data.

    Options
    -------
    -d  {1, 2, 3, 4, 5}

        Inmport bedgraph files describing data (1), or RNA-seq references (2).
        Backup stored data as **TSV** (3), (re)pickle backed up
        **TSV** data (4). Rename sample(s) in data, count and experiment
        files (5).
    -t  {1, 2}

        Change the default collapsing type **TAG** of aligned-reads, between
        **TAGUNCOLL** (1) and **TAGCOLL** (2)
    -f  {0,1}

        Force processing; backup any previous data. 0: No, 1: Yes.
    """
    #uniq = 'unique ' if args.unique == 1  else ''
    uniq=''
    t_ = TAGUNCOLL if args.tag==1 else TAGCOLL
    f_ = args.force == 1

    msg = (f"Bedgraphs of '{t_}' aligned {uniq}reads "
        f"for experiment '{EXP}' are now collected and processed.")
    if f_:
        msg += "Previous processing will be ignored.\n"


    logging.debug(f"{__name__}.{thisfunc(1)}: {msg}")

    if t_ != TAG:
        print(f"Current experiment is changed from '{TAG}' - to '{t_}' "
        f"data with option -t = {args.tag}.")

    todolist = all_exps()

    def _merge_and_index(dolist, tag, force=f_):
        if tag in [TAGCOLL,TAGUNCOLL]:
            #need force=force
            merge_sets(dolist, tag, force=force)
            # needed for loading read info in tracks
            gather_all_specific_regions(tag)
            gather_all_unspecific_regions(tag)

    def _pickle_from_backup_tsv():
        if pickle_from_backup_tsv():
            msg =f"Pickle from backed-up'{TSV}' files completed."
            logging.debug(f"{__name__}.{thisfunc()}: {msg}")

    def _process_pickle_from_backup_tsv(dolist=todolist):
        for _t in [TAGCOLL,TAGUNCOLL]:
            _merge_and_index(dolist, tag=_t, force=1)
            process_reference(tag=_t, force=1)
        # when restoring backup this is needed
            merge_unsel(tag=_t, force=f_)
        #if process_unselected(force=f_):
        #    print("unselected reads have also been processed.")
        #sync backup
        backup_pickle_to_tsv(merged_only=True)

    def _rename_datasamples(names_old_new):
        print(f"Backup data to '{TSV}' format.")
        backup_pickle_to_tsv(data_only=True)
        print(f"Rename samples in backed-up '{TSV}' data.")
        if rename_in_data_tsv(names_old_new):
            print("Renaming samples in backed-up data complete.")
        if rename_unselected(names_old_new):
            print(f"Renaming filenames in '{SAVEBAM}' complete.")

    def _rename_othersamples(names_old_new, both):
        msg = ""
        if both:
            if rename_in_count_tsv(names_old_new):
                msg += "Updated count files by renaming samples."
                print(msg)
        if rename_in_expfile(names_old_new):
            msg += (f"\nRenamed samples '{names_old_new}'"
                   f"\n in experiment file: '{EXPFILE.name}'.")
            print(msg)
        logging.debug(f"{__name__}.{thisfunc()}: {msg}")

    if args.datafiles == 1:
        print(msg)
        print("\nProcessing bedgraphs for libraries:\n "
            f"{', '.join(todolist)}.\n")
        # storing files takes a while; do it piecemal
        for lib in todolist:
            process_graphs(select=lib, tag=t_, force=f_)
        _merge_and_index(todolist, tag=t_)

        msg = (f"For counting, process the '{TAGCOLL}' libraries with "
                "option ``-t 2`` (if you haven't done that already).")
        if t_==TAGUNCOLL:
            print(msg)
    if args.datafiles == 2:
        print("\nProcessing references ...\n")
        process_reference(tag=t_, force=f_)
    if args.datafiles in [3,4,5]:
        #log all feedback (writing output to terminal is slow)
        if args.datafiles == 3:
            msg2 = "\nCollect and back up pickled data .."
            print(msg2)
            logging.debug(f"{__name__}.{thisfunc(1)}: {msg2}")
            backup_pickle_to_tsv()
        elif args.datafiles == 4:
            msg3 = "\nRecreate pickled data from backup .."
            print(msg3)
            logging.debug(f"{__name__}.{thisfunc(1)}: {msg3}")
            _pickle_from_backup_tsv()
            _process_pickle_from_backup_tsv()
        elif args.datafiles == 5:
            msg4 = "\nRename samples in pickled and count data.."
            print(msg4)
            logging.debug(f"{__name__}.{thisfunc(1)}: {msg4}")
            names_old_new = get_old_new_samplenames(todolist)
            dolist = replacelist_list(todolist, names_old_new)
            both = True
            _rename_datasamples(names_old_new)
            _pickle_from_backup_tsv()
            _process_pickle_from_backup_tsv(dolist)
            _rename_othersamples(names_old_new, both)
            print("\nDone, but compare files `after` vs. "
                f"`before` ('{BAK}') to check all is well.")


def showgraphs(args):
    """Execute command ``coalispr showgraphs``

    Compare series of bedgraphs -w for chomosome -c  using type -t samples -s,
    by means of interactive bedgraph plots.

    Which samples, which section of the chromosome, which nearby genes,
    whether or not transcribed, can be displayed and all can be saved as
    **PNG**, **JPG**, **PDF** or **SVG** files.

    Options
    -------
    -c  ``chroms()``

        Name of chromosome; display associated bedgraphs for chromosome -c.
    -w  {1,2,3,4} (default: 1)

        Window sequence; in one go, various groups of reads can be displayed,
        each in a separate window that opens when the current window is closed.
        (1) a) with all mapped reads, b) with all unspecific reads, then c)
        with all specific reads, (2) only all mapped reads (1a), (3) only
        unspecific reads (1b), (4) only specific reads (1c).
    -s  {1,2,3} (default: 1)

        Show bedgraph traces for
        controls (1),
        configured non-redundant data (controls plus mutants) (2),
        configured data including redundant samples (3).
    -t  {1,2}

        Change type of aligned data (now: **TAG**) to 1: **TAGUNCOLL**, or
        2: **TAGCOLL**."
    -u  {0,1}

        Show **TAGCOLL** data (-t2) including unselected reads? 0: No, 1: Yes.
    -sp  {0,1}

        Include sidepane with sub-legends? 0: No, 1: Yes.
    -wg  {1,2,3,4,5}

        Show (1) or write graphs to **SVG** (2) **PNG** (3) **PDF** (4), or
        **JPG** (5).
    -r  (int,int) or 1

        Set region by providing start and end coordinates directly (tuple) or
        via dialog (1).

    -x  {0,1} (default: 0)

        Include unused, discarded samples: 0: No, 1: Yes.
    """
    chrnam_ = args.chrom

    sp_ = mutant_groups if args.sidepane else None
    dw_ = {1: "show", 2: SVG, 3: PNG, 4: PDF, 5: JPG}[args.dowhat]
    # force right conditions when unselected reads are loaded
    u_ = args.showunselected == 1              # only for tag_ == TAGCOLL
    tag_ = TAGCOLL if u_ or args.tag==2 else TAGUNCOLL
    if tag_ != TAG:
        print(f"Showing '{tag_}' data; this changed from configured default "
            f"'{TAG}'.")

    samples_ = {1: controls(),
                2: controls() + mutant(),      # configured data samples
                3: controls(False) + mutant(False),  # all data samples
                }[args.samplechoice]

    if has_discards() and args.discarded == 1: # 0, 'False' is default
        samples_.extend(discarded()),          # incl. discards


    if args.coord == (0,0):                    #default
        r_ = None
    else:
        r_ = collect_limits(chrnam_, args.coord)

    refs_ = False if len(reference()) == 0 else True
    wc_ = args.windowchoice
    if wc_ in [1, 2, ]:
        show_chr(chrnam_ , tag=tag_, refs=refs_, setlist=samples_, unsel=u_,
            dowhat=dw_, side=sp_, ridx=r_)
    if wc_ in [1, 3, ]:
        show_unspecific_chr(chrnam_ , tag=tag_, refs=refs_, unsel=u_,
            setlist=samples_, dowhat=dw_, side=sp_, ridx=r_)
    if wc_ in [1, 4, ]:
        show_specific_chr(chrnam_, tag=tag_, refs=refs_, unsel=0,
            setlist=samples_, dowhat=dw_, side=sp_, ridx=r_)


def countbams(args):
    """Execute command ``coalispr countbams``

    Count aligned reads in bam files; write these to **TSV** files.

    Options
    -------
    -h, --help
        Show this help message and exit
    -rc  {1,2}

        Obtain total mapped counts from length alignment file for:
        1: **TAGUNCOLL**, 2: **TAGCOLL** data, with strand information.
    -b  {1,3,5}

        Divide segments to be counted in: 1, 3 or 5 bins (default: **BINS** for
        **SPECIFIC** - and 1 for **UNSPECIFIC** read counting).
    -k  {1,2}

        Count Specific (1) or Unspecific reads (2). (default: 1)
    -u  {0,1}

        Include counting of unselected reads (within range **BAMPEAK**, with
        5\'-end **BAMSTART**),in **UNSPECIFIC** data? 0: No, 1: Yes. [This
        depends on a program extracting raw bedgraphs from bam data (like STAR)
        and needs raw input counts (-rc for **TAGBAM** reads).]
    -mm  {**NRMISM** to **MAXMM**}

        Number of tolerated substitutions
    -pd  {0,1}

        Accept point-deletions? 0: No, 1: Yes (default: 0)
    -f  {0,1}

        Force processing; backup any previous data. 0: No, 1: Yes.
    """
    kind_ = SPECIFIC if args.kind==1 else UNSPECIFIC
    bins_ = args.bins
    force_ = args.force
    unsel_ = args.unselected
    raw_ = args.rawcounts
    cigchk_ = CIGFM if args.pointdel == 0 else CIGPD
    nomis_ = _mismatches(args.mism)

    def check_files():
        numbam = num_counted_libs()
        if numbam > 0:
            msg = (f"Found {numbam} bamfiles to count, continuing...")
            print(msg)
            logging.debug(f"{__name__}.{thisfunc()}: {msg}")
        elif numbam == 0:
            msg = (f"No {TAGBAM} bamfiles found, ..stopping...")
            logging.debug(f"{__name__}.{thisfunc()}: {msg}")
            raise SystemExit(msg)

    def count_bamfiles():
        if kind_ == SPECIFIC:
            _bins = bins_
            unselected_ = False # exclude wtiting and counting absent files
        elif kind_ == UNSPECIFIC:
            # set bins to default 1 unless overwritten by setting parameter
            _bins = 1 if bins_ == BINS else bins_
            unselected_ = unsel_

        print(f"\nNow running: process_bamfiles(kind={kind_}, "
              f"bins={_bins}, writebam={unselected_}, force={force_}, "
              f"cigarchk={cigchk_}, mismatches={nomis_})")

        process_bamfiles(bins=_bins, kind=kind_, writebam=unsel_,
            force=force_, cigchk=cigchk_, nomis=nomis_)
        msg = (f"Done counting '{kind_}' reads from bam-alignments.\n ")

        print(msg)
        logging.debug(f"{__name__}.{thisfunc()}: {msg}")

    def processunselected():
        print("Unspecific reads in separate bam files will be processed.")
        process_unselected(force=force_)

    if raw_ in [1,2]:
        tagrc = TAGUNCOLL if raw_ == 1 else TAGCOLL
        total_raw_counts(tagBam=tagrc, stranded=True, force=force_)
    else:
        print(f"Bamfiles for experiment '{EXP}' are processed... "
              f"Counted are {TAGBAM} reads in bam alignments for regions "
              f"identified for {TAGSEG} reads.")
        if unsel_ and kind_ == UNSPECIFIC:
            print(f"Counted, {kind_} alignments within range {BAMPEAK}, with "
                  f" 5'-end {BAMSTART}, will be saved in separate bam files.")
        if force_:
            print("\nExisting folder `F` with count files will be backed up "
                  f"to `F{BAK}`.")

        check_files()
        count_bamfiles()
        if kind_ == UNSPECIFIC and unsel_:
            processunselected()


def showcounts(args):
    """Execute command ``coalispr showcounts``

    Display counts obtained with ``coalispr countbams`` and save figures.

    Options
    -------
    -h, --help
        Show this help message and exit
    -rc  {1,2}

        Display total mapped counts from length alignment file for
        1: **TAGUNCOLL**, or 2: **TAGCOLL** data, with strand information.
    -lc  {1,2,3,4,5,6,7}

        Display total library counts for **SPECIFIC** vs **UNSPECIFIC**, for 1:
        **ALL**, 2: **COLLR**, or 3: **CHRXTRA**, reads, or for 4: **INTR**
        gaps, or 5: those in **COLLR** reads; 6: **UNSEL** siRNA-like reads in
        **UNSPECIFIC** data. 7: **SKIP** due to irregular cigar-string.
    -bd  {1,2,3,4,5}

        Display average bin distribution for specific libraries of 1: **ALL**,
        2: **COLLR**, 3: **CHRXTRA** reads, 4: **INTR** gaps or 5: those in
        **COLLR** reads."
    -ld  {1,2,3,4,5,6}

        Display separate length distributions for 1: **ALL**, 2: **COLLR**, 3:
        **CHRXTRA** reads; or 4: **INTR** gaps, or 5: those in **COLLR** reads;
        6: **UNSEL** siRNA-like reads in **UNSPECIFIC** data.
    -md  int  {1,2}

        Display hit-number distribution for **MULMAP**s in separate
        libraries for **ALL** (1) or **INTR**-containing (2) reads.

    -lo  {1,2,3,4,5}

        Display overview, i.e. combined length distribution for **SPECIFIC** vs
        **UNSPECIFIC**, for  1:**ALL**, 2: **COLLR**, 3: **CHRXTRA**, reads; or
        4: **INTR** gaps, or 5: those in **COLLR** reads.
    -mo  {1,2}

        Display overview, i.e. combined hit-number distribution for **SPECIFIC**
        vs **UNSPECIFIC**, for 1: **ALL** **MULMAP** reads or those with an 2:
        **INTR** -like gap.
    -g  {1,2,3,4}

        Group libraries according to 1: **CATEGORY**, 2: **METHOD**, 3:
        **FRACTION**, 4: **CATEGORY** (if all have multiple subgroups).
        (useable for -lc, -rc, -ld, -md, -bd)
    -k  {1,2}

        Display separate libraries for **SPECIFIC** (1) or **UNSPECIFIC** (2)
        reads.
    -rl  {1,2,3,4}

        Read length is restricted to 1: (XLIMR0, XLIMR1); 2: {(XLIM00, XLIM11)};
        3: (XLIM0, XLIM1)}; or 4: Set lower and upper limits, separated by a
        comma (',') or hyphen ('-').
    -ma  {1,2}

        Kind of read to focus on, 1: **UNIQ**, 2: **MULMAP**.
    -st  {1,2,3}

        Show data for for **COMBI** (1), **MUNR** (2), or **CORB** (3) strands.
    -lg  {1,2,3}

        Display total counts on linear (1) or log2 (2) scale or show log2 values
        for **SPECIFIC** counts vs. the log2 difference between
        **SPECIFIC** and **UNSPECIFIC** mapped reads; (with -lc ).
    -x  {0,1}

        Include excluded (unused) samples; 0: No, 1: Yes.
    -nt  {0,1}

        No figure titles (1); keep those (0).
    """
    raw_  = args.rawcounts
    bd_   = args.binperc
    lc_   = args.libcounts
    lg_   = args.lgcounts
    ld_   = args.lengthdist
    lo_   = args.lenoverview
    mulms = {0: None, 1: LIBR, 2: INTR}
    md_   = mulms[args.mhitdist]
    mo_   = mulms[args.mhitoverview]
    mapr_ = {0: "", 1: UNIQ, 2: MULMAP}[args.mapper] # 0, "" is default
    unsel = (lc_==6 or ld_==6)
    k_    = UNSPECIFIC if args.kind == 2 or unsel else SPECIFIC
    g_    = CATEGORY if not has_grouparg() else goption()['usegroups'][args.grp]
    x_    = has_discards() and args.unused == 1
    nt_   = args.notitles                            # 1, 'off' is default
    strd_ = {1:COMBI, 2:MUNR, 3:CORB}[args.strands]  # COMBI is default

    kinds = {1:LIBR, 2:COLLR, 3:XTRA,  4:INTR, 5:INTR+COLLR,
             6:UNSEL, 7:SKIP}

    rl_ = {0: None, 1: (XLIM00,XLIM11), 2: (XLIM0,XLIM1),
           3: (0,0)}[args.readlengths]
    lim = collect_limits(chrnam_= None, rangex=(0,0)) if rl_ == (0,0) else rl_

    if raw_ in [1,2]:
        tagrc = TAGUNCOLL if raw_ == 1 else TAGCOLL
        if lg_ == 1:
            show_mapped_vs_unmapped(tagrc, g_, x_, nt_)
        if lg_ in [2,3]:
            show_mapped_vs_unmapped(tagrc, g_, x_, nt_, True)

    if not CHRXTRA and (lc_ == 3 or bd_ == 3 or ld_ == 3 or lo_ == 3):
        raise SystemExit("No data for extra sequences available,  "
            f"('CHRXTRA' defined as '{CHRXTRA}' or '{XTRA}'); stopping...")

    if lo_ != 0:
        #input: {kind}_{RLENCOUNTS | LENCOUNTS}_{ALL}_{strand}TSV.
        rdkind = mapr_+kinds[lo_] if lo_ in [1,2,4,5] else kinds[lo_]
        lim = (XLIM0, XLIM1) if not lim else lim
        compare_un_spec_lengths(rdkind, lim, strd_, nt_)
    if ld_ != 0:
        #input: {kind}_{RLENCOUNTS | LENCOUNTS}_{strand}TSV.
        rdkind = mapr_+kinds[ld_] if ld_ in [1,2,4,5] else kinds[ld_]
        lim = (XLIM00, XLIM11) if not lim else lim
        compare_exp_lengths(rdkind, lim, strd_, g_, nt_, k_, x_)
    if lc_ != 0:
        if lc_ == 7: # SKIP has only
            _st = COMBI
        else:
            _st = strd_
        #input: {kind}{BCO | COU}_{strand}{TSV}
        rdkind = mapr_+kinds[lc_] if lc_ in [1,2,4,5] else kinds[lc_]
        if lg_ == 1:
            compare_libtotals(rdkind, _st, g_, nt_, x_, False, False)
        elif lg_ == 2:
            compare_libtotals(rdkind, _st, g_, nt_, x_, False, True)
        elif lg_ == 3:
            compare_libtotals(rdkind, _st, g_, nt_, x_, True, False)
    if bd_ != 0:
        if not has_been_counted(typeofcount=BCO):
            raise SystemExit("Counted reads have not been split over bins")
        rdkind = mapr_+kinds[bd_] if bd_ in [1,2,4,5] else kinds[bd_]
        compare_exp_bins(rdkind, strd_, g_, nt_, x_)
    if md_ != None:
        compare_exp_mulmaps(md_, strd_, g_, nt_, k_, x_)
    if mo_ != None:
        compare_un_spec_mulmaps(mo_, strd_, nt_)


def region(args):
    """ Obtain overall counts and length-distributions of reads in a given
    chromosomal region; save figures.

    Options
    -------
    -c  ``chroms()``

        Name of chromosome for which a region is checked.
    -r  tuple

        Set region by providing start and end coordinates.
    -s  {1,2,3}

        Number to mark the samples to check: controls (1), controls and mutants
         (2), or make a selection (3).  (default: 1)
    -st  {1,2,3}

        Display counts for both strands (1), or only **PLUS** (2), or **MINUS**
        (3) strand. (default: 1)
    -cf  {1,2,3,4}

        Compare **LIBR** to **COLLR** (cDNA) (1); or **UNIQ** to **MULMAP** for
        **LIBR** (2) or for **COLLR** (3), all (4). (default: 1)
    -mm  {**NRMISM** to **MAXMM**}

        Number of tolerated substitutions.
    -pd  {0,1}

        Accept point-deletions? 0: No, 1: Yes. (default: 0).
    -g  {1,2,3}

        Group libraries according to 1: **CATEGORY**, 2: **METHOD**, or 3:
        **FRACTION**.
    -rl  {1,2,3,4}

        Read length is restricted to 1: {(XLIMR0, XLIMR1); 2:(XLIM00, XLIM11)};
        3: (XLIM0, XLIM1)}; or 4: Set lower and upper limits, separated by a
        comma (',') or hyphen ('-').
    -lg  {1,2}

        Display total counts on linear (1) or log2 (2) scale.
    -nt  {0,1}

        No figure titles (1); keep those (0).
    -rm  {0,1}

        Include redundant mutant samples; 0: No, 1: Yes.
    -x  {0,1}

        Include excluded (unused) samples; 0: No, 1: Yes.
    """
    chrnam_ = args.chrom
    st_ = {1: COMBI, 2: PLUS, 3: MINUS}[args.strands]
    cigchk_ = CIGFM if args.pointdel == 0 else CIGPD
    nomis_ = _mismatches(args.mism)
    g_ = CATEGORY if not has_grouparg() else goption()['usegroups'][args.grp]
    lg_ = args.lgcounts == 2
    r_ = args.coord
    nt_ = args.notitles # 1, 'off' is default
    x_  = has_discards() and args.unused == 1
    rm_ = has_redundant_muts() and args.redmuts == 1
    cf_ = {1:[LIBR, COLLR], 2:[LIBR, UNIQ, MULMAP+LIBR],
           3:[COLLR, UNIQ+COLLR, MULMAP+COLLR],
           4:[LIBR, UNIQ, COLLR, UNIQ+COLLR],
           }[args.comparechoice]
    rl_ = {1:(XLIMR0, XLIMR1), 2:(XLIM00,XLIM11), 3:(XLIM0,XLIM1), 4:(0,0),
           }[args.readlengths]
    lim = collect_limits(chrnam_= None, rangex=(0,0)) if rl_ == (0,0) else rl_

    samples_ = _get_samples(args.samplechoice, rm_, x_)
    #print(samples_)
    region_ = collect_limits(chrnam_, r_)
    chr_region = chrom_region(chrnam_, region_)
    #print(region_)
    lenframs, countfram = process_reads_for_region(samples_, chrnam_, region_,
        st_, cf_, cigchk_,  nomis_)
    #print(countfram)
    plot_regioncounts(chr_region, countfram, group=g_, strand=st_,
        notitles=nt_, log2=lg_,  showdiscards=x_)
    plot_regionlengths(chr_region, lenframs, group=g_, readlen=lim, strand=st_,
        notitles=nt_, showdiscards=x_
        )


def annotate(args):
    """Execute command ``coalispr annotate``

    Display read counts with annotations extracted from **GTF**.

    Options
    -------
    -h, --help
        Show this help message and exit
    -lc  {1,2,4,5}

        Annotate total library counts for 1: **ALL**; 2: **COLLR**; 3: None;
        4: **INTR**, 5: **INTR+COLLR**.
    -k  {1,2}

        Annotate Specific (1), or Unspecific (2) reads.
    -rf  {0,1}

        Include general **REFERENCE** GTF for annotations (slow). 0: No; 1: Yes.
    -st  {1,2,3}

        Show data for for **COMBI** (1), **MUNR** (2), or **CORB** (3) strands.
    -ma  {1,2}

        Kind of read to focus on, 1: **UNIQ**, 2: **MULMAP**.
    -lg  {1,2}

        Display total counts on linear (1) or log2 (2) scale.
    -sv  {0,1}

        Sort table with respect to values, descending from highest if 1.
    -x  {0,1}

        Include excluded (unused) samples; 0: No, 1: Yes.
    """
    if args.libcounts == 3:
        raise SystemExit("Nothing to annotate for this option.")
    k_ = SPECIFIC if args.kind == 1 else UNSPECIFIC
    lg_   = args.lgcounts
    st_ = {1: COMBI, 2: MUNR, 3: CORB}[args.strands]
    mapr_ = {0: "", 1: UNIQ, 2: MULMAP}[args.mapper] # 0, "" is default
    sv_ = args.sortvalues                            # 1, 'True' is default
    rf_ = args.plusref                               # 0, 'False' is default
    lg_ = args.lgcounts == 2
    x_  = has_discards() and args.unused == 1

    lc_ = {1:LIBR, 2:COLLR, 4:INTR, 5:INTR+COLLR,}[args.libcounts]
            #3:XTRA,  4:INTR, 5:INTR+COLLR, 6:UNSEL, 7:SKIP}
    #input: {kind}{BCO | COU}_{strand}{TSV}
    rdkind = mapr_+ lc_ if args.libcounts < 3 else lc_
    annotate_libtotals(rdkind, st_, k_, rf_, x_, lg_, sv_)



def groupcompare(args):
    """Make a length-distribution overview for grouped samples. Compare samples
    according to their type as defined by mutation (**GROUP**), **METHOD**,
    **FRACTION**, or **CONDITION**. Choose starting nt of reads.

    Options
    -------
    -g  {1,2,3,4}

        Compare 1: **METHOD**, 2: **FRACTION**, 3: **CONDITION** or 4:**GROUP**.
    -5e  (1,2,3,4,5}

         Choose 5' end of reads to compare length for 1: T, 2: A, 3: G, 4: C,
         or 5: N."
    -ld  {1,2,3}

        Display length distribution overview for 1: **ALL**, 2: **COLLR**, 3:
        **CHRXTRA** reads.
    -ts  {1,2,3}

        Trim samples. 1: No negative controls and specify; 2: No negative
        controls, only **REST** samples; 3: Specify all samples.
    -k  {1,2}

        Display **SPECIFIC** (1) or **UNSPECIFIC** (2) reads.
    -rl  {1,2,3,4}

        Show read lengths for 1: (XLIMR0, XLIMR1); 2:{(XLIM00, XLIM11)};
        3: (XLIM0, XLIM1)}; or 4: Set lower and upper limits, separated by a
        comma (',') or hyphen ('-').
    -me  {1,2}

        What kind of average to plot, 1: **MEAN**, 2: **MEDIAN**.
    -st  {1,2,3}

        Show data for for **COMBI** (1), **MUNR** (2), or **CORB** (3) strands.
    -ma  {1,2}

        Kind of read to focus on, 1: **UNIQ**, 2: **MULMAP**.
    -nt  {0,1}

        No figure titles (1); keep those (0).
    -rm  {0,1}

        Include redundant mutant samples; 0: No, 1: Yes.
    -x  {0,1}

        Include excluded (unused) samples; 0: No, 1: Yes.
    """
    x_  = has_discards() and args.unused == 1
    rm_ = has_redundant_muts() and args.redmuts == 1
    grps = mixed_groups(plusdiscards=x_, allmut=rm_)

    if not grps:
        raise SystemExit("No groups with items to compare.")
    # sync with cmd_parser options and get v for choice group
    g_ = {k:v for k,v in enumerate(grps.keys(),1)}[args.fromgroup]
    # chosen group with subgrouped samples
    grp = grps[g_]
    '''if g_== METHOD:
        assert(g_== METHOD and grp == {
    'total': ['a1', 'a1a2', 'a2_1', 'a2_2', 'a2_3od7', 'c4', 'd1_1', 'd1_1ms0',
        'd1_2', 'd1_3', 'd1d2', 'd2_1',  'd2_1ms0',  'd2_2',  'd5', 'd5c4',
        'dh_1', 'dh_2', 'dh_3', 'h1_1', 'h1_2', 'p5', 'r1_1', 'r1_2', 'wt_a',
        'wt_b',  'wt_c',  'wt_ms0'],
    'rip1': ['A1_1a',  'A1_1b',  'A1_1ms0', 'A1_2', 'A1a2_1', 'A1a2_2',
        'A1a2_3od7a', 'A1a2_3od7b', 'A1a2_3od7c', 'A1a2_3od7d', 'A1a2_3od7e',
        'A1a2_3od7f', 'A1be_a', 'A1be_b', 'A1c4', 'A1d1_1', 'A1d1_2', 'A1d1_3',
        'A1d1d2', 'A1d2_1a', 'A1d2_1b', 'A1d2_2', 'A1d5_1', 'A1d5_2', 'A1dh_1',
        'A1dh_2', 'A1h1_1a', 'A1h1_1b', 'A1h1_2', 'A1p5', 'A1rR_1', 'A1rR_2',
        'rA1_1', 'rA1_2', 'rA1_3', 'rA1a2_1', 'rA1a2_2', 'rA1agg_1', 'rA1agg_2',
        'rA1h99_1', 'rA1h99_2', 'rA1kgg_1', 'rA1kgg_2', 'rA1n2_1', 'rA1n2_2',
        'rA1n2rgg2_1', 'rA1n2rgg2_2', 'rA1nor_1', 'rA1nor_2', 'rA1rgg2_1',
        'rA1rgg2_2', 'rhA1', 'rhA1ye'],
    'rip2': ['A2R', 'A2_a', 'A2_b', 'A2_ms0', 'A2a1', 'A2be_a', 'A2be_b',
        'A2c4', 'A2d1_1', 'A2d1_2', 'A2d1_3', 'A2d2_1', 'A2d2_2', 'A2d5',
        'A2dh_1', 'A2dh_2', 'A2h1_1a', 'A2h1_1b', 'A2h1_2', 'A2rR_1', 'A2rR_2',
        'A2rR_3', 'rha1A2_1', 'rha1A2_2', 'rha1A2_3', 'rha1yeA2']
        }
    )'''
    # for trimming initial sample set
    ts_ = {1: NEGCTL, 2: f"{NEGCTL}{REST}", 3: ALL.upper()}[args.trimsampleset]
    grouptypes, subtypes, selectedsamples = assemble_groupsamples(grps, g_, ts_)
    msg = (f"\nSelected {len(selectedsamples)} samples to compare according to "
          f"'{g_}', types '{joinall(grouptypes, joiner())}', subtypes '"
          f"{joinall(subtypes, joiner())}': \n{selectedsamples}\n")
    print(msg)
    logging.debug(f"{__name__}.{thisfunc()}{msg}")
    lim = {1: (XLIMR0, XLIMR1), 2: (XLIM00,XLIM11), 3: (XLIM0,XLIM1),
           4: (0, 0),}[args.readlengths]
    if lim == (0, 0):
        lim = collect_limits(chrnam = None, rangex=(0, 0))

    _5nt = args.nt5end.upper()
    mapr_ = {0: "", 1: UNIQ, 2: MULMAP}[args.mapper]      # 0, "" is default
    ld_ = {1:LIBR, 2:COLLR, 3:XTRA,}[args.lengthsdistrib] # no introns
    rdkind = mapr_+ ld_ if args.lengthsdistrib < 4 else ld_
    var_ = MEAN if args.average == 1 else MEDIAN
    k_ = UNSPECIFIC if args.kind == 2 else SPECIFIC

    nt_   = args.notitles                                 # 1, 'off' is default
    strd_ = {1: COMBI, 2: MUNR, 3: CORB}[args.strands]    # COMBI is default

    compare_5nt_lengths(rdkind=rdkind,  nt5=_5nt, grp=g_, grpdict=grp,
    samples=selectedsamples, types=grouptypes, subtypes=subtypes, readlen=lim,
    var=var_, strand=strd_, mulmap=mapr_, use=k_, notitles=nt_)



def info(args):
    """Execute command ``coalispr info``

    Show experiment name, file paths, number of regions, or memory-usage. Plots,
    str, or **TSV** files with requested information are the output.

    Options
    -------
    -h, --help
        Show this help message and exit
    -i  {1,2}

        Show 1: current experiment, 2: memory-usage (default: 1).
    -p  {1,2}

        Show path to: 1: configuration file for **EXP** ``3_EXP.txt``; 2: file
        describing sequencing data **EXPFILE**.
    -r  {1,2,3}

        Regions found depending on settings for parameters **UNSPECLOG10**,
        from **UNSPECTST**, **USEGAPS**, from **UGAPSTST**, and **LOG2BG**,
        from **LOG2BGTST**, 1:**TSTREGIONS** data, 2: show **TAGUNCOLL** data;
        3: show **TAGCOLL** data. Note that 1 creates input for 2 or 3; run 1
        first.
    -nt  {0,1}

        No figure titles (1); keep those (0).
    """
    notitles = True if args.notitles == 1 else False
    if args.paths == 1:
        print(f"Configuration file is: \n{CONFFILE}")
    if args.paths == 2:
        print(f"Experiment file is: \n{EXPFILE}")
    if args.inform == 1:
        print(f"Current experiment is '{EXP}'")
    if args.inform == 2:
        print_memory_usage_merged()
    if args.regions == 1:
        test_intervals()
    if args.regions == 2:
        show_regions_vs_settings(TAGUNCOLL, notitles)
    if args.regions == 3:
        show_regions_vs_settings(TAGCOLL, notitles)


def test(args):
    """Execute command ``coalispr test``

    Test and profile main sections of the program.

    Options
    -------
    -h, --help
        Show this help message and exit
    -tp  {1,2,3,4}

        Test/profile 1: showgraphs, 2: countbams, 3: region, or 4: annotate.
    -no

        Show given number of lines topping the profiling report.
    -k  {1,2}

        Use **SPECIFIC** (1) or **UNSPECIFIC** (2) reads.
    """
    import pstats, cProfile
    from pstats import SortKey

    no_ = args.lineno
    if args.test == 1:
        samples_ = controls() + mutant()
        sp_ = mutant_groups
        chrnam_ = list(chroms())[0]
        refs_ = False if len(reference()) == 0 else True
        fcie = (
            "show_chr(chrnam_ , tag=TAG, refs=refs_, setlist=samples_, "
            "unsel=False, dowhat='show', side=sp_, ridx=None)"
            )
        proflog = (f"show_chr({chrnam_} , tag={TAG}, refs={refs_}, "
            f"setlist= [{len(samples_)} samples], "
            f"unsel=False, dowhat='show', side={sp_}, ridx=None)")
    elif args.test == 2:
        kind_= SPECIFIC if args.kind == 1 else UNSPECIFIC
        fcie = "process_bamfiles(force=True, kind=kind_, test=True)"
        proflog = (f"process_bamfiles(force=True, kind={kind_}, test=True)")
    elif args.test == 3:
        samples_ = controls()
        chrnam_ = list(chroms())[0]
        region_ = (45600, 78900)
        comp_ = [LIBR, COLLR]
        fcie = "process_reads_for_region(samples_,chrnam_,region_,COMBI,comp_)"
        proflog = (f"process_reads_for_region {chrnam_}:{region_[0]}-"
            f"{region_[1]} for {len(samples_)} samples.")
    elif args.test == 4:
        rdkind = LIBR                                     # library counts
        st_ = COMBI                                       # combined strands
        k_ = SPECIFIC if args.kind == 1 else UNSPECIFIC
        rf_ = 1                                           # with mRNA reference
        x_ = 0                                            # exclude unused
        lg_ = False                                       # linear scale
        sv_ = 1                                           # sort on value
        fcie = "annotate_libtotals(rdkind, st_, k_, rf_, x_, lg_, sv_)"
        proflog = (f"annotate(rdkind, kind={k_}).")
        #fcie = showcounts()
    cProfile.runctx(fcie, globals(), locals(), proflog)
    so = StringIO()
    s = pstats.Stats(proflog, stream=so)
    s.strip_dirs().sort_stats(SortKey.TIME, SortKey.CUMULATIVE).print_stats(no_)
    logging.debug(f"{__name__}.{thisfunc()} -fu {args.test}:\n"
        f"{so.getvalue()}")


def main():
    # Set up logging
    logger = _start_logging()

    comms ={'init':init, 'setexp':setexp, 'storedata':storedata,
        'showgraphs':showgraphs, 'countbams':countbams, 'showcounts':showcounts,
        'region':region, 'annotate':annotate, 'groupcompare': groupcompare,
        'info':info, 'test':test}

    def coalispr(args):
        f = comms[args.command]
        f(args)

    parser = make_parser(comms, __version__)
    args = parser.parse_args()

    if len(vars(args)) <= 1:
        parser.parse_args(['--help'])

    logger.debug(f"\n\nLogging {args}\n")
    try:
        coalispr(args)
    except SystemExit as e:
        logger.debug(f"SystemExit on: {e}\n")
        print(e)
        pass
    except:
        msg = format_exc()
        logger.debug(f"{msg}\n -- Sorry --\n")
        print(msg)
    finally:
        logger.debug("closing..\n\n")
    sys.exit(0)
