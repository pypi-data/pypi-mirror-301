#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  make_constant.py
#
#  Copyright 2021-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
import shutil
import sys
import logging
from traceback import format_exc
from pathlib import Path

logger = logging.getLogger(__name__)


def make_constant(exp="h99t", otherpath=None):
    """Create a configuration file ``constant.py`` from text files.

    Output is the configuration file ``constant.py`` after combining three text
    files with settings. Two of these files (**SHARED**, **EXPTXT**) a user can
    change (after which this command has to be run in order to activate the
    changes).

    The **EXPTXT** describes settings specific for a session or an experiment
    (like name **EXP**, file paths, sample names in particular groups..) and
    needs to be adapted to each new data set. The **SHARED** gives values for
    used terms, colours etc. that define the look and feel of the figures
    with bedgraph traces or count comparisons.

    Notes
    -----
    The newly made ``constant.py`` might be needed straight away: it is only
    working after restarting the program (call another command or the same
    command again), which also reset imported modules that rely on the
    ``constant.py`` module.

    This script is tied to setting the experiment/session **EXP**. The new
    settings direct any subsequent coalispr command. As Python load this info
    in memory, one could display bedgraphs for EXP1 by ``coalispr showgraphs``
    from one terminal. Then, for comparison, in another terminal a second
    session could be defined via ``coalispr setexp -e EXP2`` and associated
    bedgraphs checked via ``coalispr showgraphs``. In the first terminal any
    new coalispr command (which restarts the program) will follow the novel
    settings. So, to bypass settings for EXP2, in this terminal one need to
    run ``coalispr setexp -e EXP1`` again before displaying another set of
    bedgraphs with settings for the original **EXP** (EXP1).

    It is possible that after editing the **SHARED** or **EXPTXT** files,
    ``coalispr setexp -e EXPnew`` stalls. In that case, run this function
    directly: ``python3 -m coalispr.resources.constant_in.make_constant``. This
    will prepare a working configuration (``constant.py``) unlinked to EXPnew.
    Then, try ``coalispr setexp -e EXPnew`` again or check the newly edited
    configuration files **SHARED** or **EXPTXT** for typos or other problems
    highlighted by the errors described in the stack trace on the terminal
    (that also will have been written to the log files).

    Parameters
    ----------
    exp : str
        Short name to identify an initialized experiment or session with.
    otherpath : str
        Path to folders with prepared configuration input files.
    """
    shared = '2_shared.txt'
    exptxt = f'3_{exp}.txt'
    p = Path(__file__).parent
    defaultpaths = [Path(), p]
    o = p.parent.joinpath('constant_out')
    co = o.joinpath(f"constant_{exp}.py")
    resetpy = o.joinpath("constant_RESET.py")
    fileparts = [ '1_heading.txt', shared, exptxt ]
    USESAMEPATH = True


    if otherpath and not Path(otherpath) in defaultpaths:
        USESAMEPATH = False
        # remove edited files
        fileparts = fileparts[0:-2] #.pop()

    try:
        with open(co,'wb') as wco:
            for f in fileparts:
                with open(p.joinpath(f),'rb') as fin:
                    shutil.copyfileobj(fin, wco)
            if otherpath and not USESAMEPATH:
                op3 = Path(otherpath).joinpath(shared)
                op4 = Path(otherpath).joinpath(exptxt)
                logger.debug(f"Used files from \n{op3} and \n{op4}")
                for op in [op3,op4]:
                    with open(op, 'rb') as fin:
                        shutil.copyfileobj(fin, wco)
            const = p.parent.joinpath("constant.py")
            const.unlink(missing_ok=True)
            const.symlink_to(co)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        sys.exit(0)

    # test configuration
    try:
        import importlib
        import coalispr.resources.constant as cons
        importlib.reload(cons)
        msg = (f"Configuration ready for '{cons.EXP}'.") # - {const} -
        # no exception raised? Then backup this working constant.py
        conspath = const.readlink()
        if otherpath and not USESAMEPATH:
            bakpath = Path(
                otherpath.parent).joinpath(conspath.stem).with_suffix(".bak")
        else:
            bakpath = co.with_suffix(".bak")
        shutil.copy(conspath, bakpath)
        print(msg)
        logging.debug(msg)
    except:
        msg = format_exc()
        msg += ("\n\tSee last lines of above error trace and corresponding "
              "section in\n\t edited configuration files (and .bak) in:\n\t   "
              f"{otherpath.parent.name} \n\tRepair files before retrying to "
              f"configure {exp}; \n\t reset to shipped configuration.")
        logging.debug(msg)
        # remove bad constant.py
        const.readlink().unlink()
        const.unlink()
        # reset to shipped configuration
        const.symlink_to(resetpy)
        raise SystemExit(msg)

def main(args):
    if len(sys.argv) == 2:
        make_constant(exp=args[1])
    else:
        make_constant()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
