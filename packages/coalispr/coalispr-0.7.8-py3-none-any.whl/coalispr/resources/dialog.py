#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  dialog.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module for gathering user-input."""
import re
import logging
from pathlib import Path

from coalispr.bedgraph_analyze.genom import get_lengths
from coalispr.bedgraph_analyze.experiment import (
     negative,
     positive,
     )
from coalispr.resources.constant import (
    ALL,
    CONFFOLDER, CWD,
    DATA,
    FIGS,
    HOME,
    NEGCTL,
    PRGNAM,
    REST,
    SRCPRGNAM,
    TSV,
    XLIMMAX, XLIMMIN,
    )
from coalispr.resources.utilities import (
    clean_dict,
    joiner,
    thisfunc,
    )

logger = logging.getLogger(__name__)

class PresentDialog():
    """Present dialog based around given messages.

    Attributes
    ----------
    msg : str
        Welcome message
    item : str
        Requested item
    pattern : str
        Regular expression to validate user input
    per_confirm : bool
        Flag to use confirm-dialog to verify output
    fcie: function
        Function for extra test and that analyzes user input

    """
    SKIP = 'skip_this'

    def __init__(self, msg, item, pattern, per_confirm=True, fcie=None):
        self.msg1 = msg
        self.item = item
        self.pattern = pattern
        self.stop = 'stop'
        self.stopmsg = f"('{self.stop}' to cancel.)"
        self.msg2 = "{} will be set to:\n\t   {} \n\tIs that OK?"
        self.errortext = """
        Sorry, '{0}' cannot be used. {1}?"""
        self.fcie = fcie
        self.per_confirm = per_confirm

    def _test_input(self, userinput):
        test1 = bool(re.match(self.pattern, userinput))
        if test1 and self.fcie:
            return bool(self.fcie(userinput))
        return test1

    def try_input(self, commandinput):
        """Check (string) directly given input via the command line.

        Parameters
        ----------
        commandinput : str
            List of input argumnets converted to string that can be parsed by
            self.fcie and matches pattern.
        """
        if self._test_input(commandinput):
            output = self.fcie(commandinput) if self.fcie else commandinput
            return output
        else:
            return self.display_dialog()

    def _skip(self):
        print("\tSkipped.. ")
        return self.SKIP

    def _redo(self):
        print("\tAgain.. "+f"{self.msg1}")

    def display_dialog(self):
        """Show dialog with options."""
        print("\t"+f"{self.msg1}")
        while True:
            #print(f"\t{self.item}:\n\t{self.stopmsg}")
            print(f"\t{self.stopmsg}")
            userinput = input('\t')
            if userinput.upper() == self.stop.upper():
                raise SystemExit("\n\t"+"Canceled.")
            if self._test_input(userinput):
                output = self.fcie(userinput) if self.fcie else userinput
                msg = self.msg2.format(self.item, userinput)
                if self.per_confirm:
                    todo=self._confirm(msg)
                    if todo==1:
                        print(f"\n\t{self.item} has been set to '{output}'.\n")
                        return output
                    elif todo==2:
                        self._redo()
                        continue
                    elif todo==3:
                        return self._skip()
                elif output and not self.per_confirm:
                    print(f"\n\t{self.item}: {output}")
                    return output
                else:
                    msg = f"No valid choice ('{output}')"
                    logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
                    raise SystemExit(msg)
            else:
                print(self.errortext.format(userinput,self.item))

    def _set_options(self, choices, evalas):
        options = {}
        choice_names = list(choices)
        choice_values = list(choices.values())
        text2 = ""
        for choice in iter(choices):
            choiceno = choice_names.index(choice)
            chosen_value = choice_values[choiceno] if choice_values else choice
            option = str(choiceno + 1)
            options[ option ] = chosen_value
            if isinstance(evalas, str):
                evalas_ = eval('chosen_value'+evalas)
            else:
                evalas_ = f"{list(chosen_value)}"
            text2 += f"""
            {option}: {choice_names[choiceno]} ({evalas_})"""
        return options, text2

    def display_choices(self, choices, evalas=None):
        """Show choices for doing something.

        Parameters
        ----------
        choices : dir
            Choicename: choice
        evalas : str
            alternative string to display
        """
        inputtext = """
        Enter an option: """
        options, text2 = self._set_options(choices, evalas)
        print("\t"+f"{self.msg1}{self.stopmsg}")

        while True:
            print(f"{text2}")
            userinput = input(inputtext)
            if userinput.upper() == self.stop.upper():
                raise SystemExit("\n\t"+"Canceled.")
            if self._test_input(userinput):
                chosen = options.get(userinput)
                msg = self.msg2.format(self.item, chosen)
                todo = self._confirm(msg)
                if todo == 1:
                    return chosen
                elif todo == 2:
                    self._redo()
                    continue
                elif todo == 3:
                    return self._skip()
                else:
                    print(self.errortext.format(userinput))

    def _confirm(self, msg):
        """Obtain user feedback for given input."""
        yes = 'Yes'
        redo = 'Redo'
        skip = 'Skip'
        no = 'Cancel'
        conf = {'1': yes, '2': redo, '3': skip, '4': no}

        while True:
            print("\n\n\t"+f"{msg}\n")
            for option in conf:
                print(f"\t{option}: {conf[option]}")
            userinput = input("\n\t?: ")
            if bool(re.match('^[1,2,3,4]$', userinput)):
                answ = conf.get(userinput)
                if answ != no:
                    return int(userinput) # 1 = True
                else:
                    raise SystemExit("\n\t"+"Canceled.")
            else:
                print(self.errortext.format(userinput))


# Interactive choices
# -------------------
def assemble_groupsamples(groups, agroup, trimmings):
    """Assemble a list of samples to be used by groupcompare.

    Parameters
    ----------
    groups: dict of dicts
        Nested dictionaries of samples organized by grouping (from
        experiment.mixed_groups() )
    agroup: str
        Name of chosen group or type to compare samples for.
    trimmings: str
        Chosen setting for defining trimming sequence.

    Returns
    -------
        List of selected items.
    """
    def trim_list(items):
        """Return selection of a list of samples."""
        # list items can contain [ALL.upper()]
        print("Trim selection; which items to keep?")
             #f"'{', '.join([ i for i in items if i != ALL.upper() ])}'?")
        return select_from(items)

    def final_select():
        print("\nFinal set to select samples from; which items to keep?")
        return select_from( [ALL.upper()] + selitems )

    def keep_rest(subset):
        """Return samples in "REST.upper()" collection as list."""
        nonlocal selitems
        try:
            #print(f"\nGetting {REST} samples from '{subset}' ..")
            #print(subset[REST.upper()])
            return sorted( set(selitems).intersection(subset[REST.upper()]) )
        except KeyError: # no REST if all samples are in subgroups.
            print(f"\nNo {REST} samples in '{subset}'.")
            return sorted( set(selitems).intersection( positive() ))

    def unwanted(ingrp, startkeys, endkeys):
        """Return group_names that have not been selected"""
        dumped = sorted(set(startkeys).difference(endkeys))
        dumpitems = [ v for k in dumped for v in ingrp[k] ]
        logging.debug(f"{__name__}.{thisfunc(1)}:\nDumped from '{ingrp}':\n"
                      f"{dumpitems}")
        return dumpitems

    def clear_groups(clear):            # clear = [0,1,2,3,4]
        nonlocal groups
        groups2 = {}
        groups3 = {}
        for k,v in groups.items():      # 'Aa', {'Aa1':['a1','b1','c1',0]}
            for k2, v2 in v.items():    #        'Aa1',['a1','b1','c1',0]
                v[k2] = sorted( set(v2).difference( clear ))
                                        #       {'Aa1':['a1','b1','c1']}
            groups3[k] = v              # {'Aa':{'Aa1':['a1','b1','c1']} }
            groups2 = { k: clean_dict(v) for k,v in groups3.items() }
        return groups2 if groups2 else groups

    # remove negative controls
    if NEGCTL in trimmings:
        negs = negative()
        print(f"\nRemoving negative controls:\n{', '.join(negs)} ...")
        # clean negs from other groupings
        groups = clear_groups(negs)

    grp = groups.pop(agroup) # groups is now remainder
    grpkeys = list(grp.keys())
    print(f"\nFor '{agroup}' pick subgroup(s) to compare:")
    # select subgroups in grp to compare
    subgrps = select_from( [ALL.upper()] + grpkeys )
    subgrps = grpkeys if subgrps == [ALL.upper()] else subgrps
    # collect samples from chosen subgroups
    selitems = [ v for k in subgrps for v in grp[k] ]
    # clean up groups
    groups = clear_groups(unwanted(grp, grpkeys, subgrps))
    # make another selection when other groups than agroup are available
    if len(groups) > 0:
        print(f"\nSamples differ according to '{joiner('or').join(groups)}'.")
        # register subgrouping for diagram annotation
        subtyps = {}
        subtypkeys = list(groups.keys())
        keepgrps_ = trim_list([ALL.upper()] + subtypkeys)
        if ALL.upper() in keepgrps_:
            selitems = selitems
        # cycle through selected groups to collect relevant samples
        for grp_ in keepgrps_:
            if grp_ == ALL.upper() :
                continue
            subset_ = groups[grp_]
            subtyps[grp_] = []
            if REST in trimmings:
                print(f"\n'{REST.capitalize()}' per {grp_}:")
                subtyps[grp_] += [REST]
                selitems = keep_rest(subset_)
            else:
                keepitems = []
                print(f"\nFor '{grp_}':")
                if grp_ == ALL.upper():
                    subtyps[grp_] += [ALL]
                    continue
                elif grp_ == REST.upper():
                    selitems = keep_rest(subset_)
                    subtyps[grp_] += [REST]
                else:
                    subset_keys = list(subset_.keys())
                    for subgrp_ in trim_list( [ALL.upper()] + subset_keys):
                        if subgrp_ == ALL.upper():
                            subtyps[grp_] += [ALL]
                            continue
                        elif subgrp_ == REST.upper():
                            this_keep = keep_rest(subset_)
                            subtyps[grp_] += [REST]
                        else:
                            subtyps[grp_] += [subgrp_]
                            this_keep = [ v for v in subset_[subgrp_] ]
                        #print(this_keep)
                        keepitems += this_keep
                if keepitems:
                    selitems = sorted(set(selitems).intersection(keepitems))
        enditems = final_select()
    selitems = enditems if enditems != [ALL.upper()] else selitems
    # grouptypes, subtypes, selectedsamples
    return(sorted(subgrps), subtyps, selitems)


def collect_limits(chrnam, rangex):
    """Collect tuple with coordinates for region to display or, if no
    chromosome, a pair of limits setting a range.

    Parameters
    ----------
    chrnam : str
       Name of the chromosome for which the region is returned.
    rangex : tuple
       Start and end of region/range to be analyzed.

    Returns
    -------
       Dialog to gather and return chromosomal coordinates for the region or
       a pair of limits.
    """
    if chrnam:
        max_xlim = get_lengths()[chrnam]
        rangetxt = "chromosome length"
        min_xlim = 1
        msg = (
          f"Which region of chromosome {chrnam} ({max_xlim} bp) to focus on?")
        msg2 = "(e.g. 456000, 789000 or 632225-632375):"
        item = f"Region for chr. {chrnam}"
    else:
        max_xlim = int(XLIMMAX)
        rangetxt = "given read length"
        min_xlim = int(XLIMMIN)
        msg = (
          f"Which boundaries between {min_xlim} and {max_xlim} to select?")
        msg2 = "(e.g. 17, 36 or 17-36):"
        item = f"Reads with lengths between {min_xlim} to {max_xlim} nt."

    def prepstring(commandinput):
        """Make a string from with arguments.
        The parameter should be called with ``type=str, nargs="+",`` and
        based around ' ' or ',' or '-' as separators.

        commandinput : list
            Provided option values that need to be string(s) for pattern
            matching, as list.
        """
        # Turn input list into a string needed for re.match()
        cmdin = ','.join(str(x).strip(',') for x in commandinput
            ).replace(',-',',').replace('-,',',').replace(',,',',')
        return cmdin

    def possible(userinput):
        xlimlist = re.split(r'[,-]', userinput)
        x0 = int(xlimlist[0].strip('[( '))
        x1 = int(xlimlist[1].strip(' )]'))
        if len(xlimlist) > 2:
            print(f"Too many numbers: {len(xlimlist)}.")
            return False
        if x0 >= x1:
            print(f"The second number ({x1}) is expected to be bigger "
            f"than the first ({x0}).")
            return False
        if x1 > max_xlim :
            print(f"Second number ({x1}) cannot exceed {rangetxt} "
                f"{max_xlim}.")
            return False
        return (x0, x1)

    msg += f"""

        Provide 2 numbers separated by a comma or hyphen
        {msg2}"""
    pattern = '^[\s]?[(\[]?[0-9]+[\s]?[,-][\s]?[0-9]+[)\]]?[\s]?$'
    p = PresentDialog(msg, item, pattern, False, possible)

    if rangex == (0,0):
        return p.display_dialog()
    return p.try_input( prepstring(rangex) )


def get_experiment_name():
    """Obtain user feedback for name of experiment/session."""

    msg = """
        Please provide a name for this new session/experiment.

        This name will be used in commands and in file paths.
        (therefore best to keep it short and memorable, without
        spaces or special characters).
    """
    item = 'Experiment name'
    pattern = '^[a-zA-Z0-9_-]+$'
    p = PresentDialog(msg, item, pattern)
    name = p.display_dialog()
    return  name if name != PresentDialog.SKIP else None


def get_old_new_samplenames(todolist):
    """Collect tuple with old and new name for a sample in the experiment-file

    Returns
    -------
       Dialog to gather and return names for samples.
    """
    def test_new(inold):
        if not inold in todolist:
            return inold
        else:
            print(f"\tName '{inold}' is taken.")

    def get_sample_name(x):
        """Obtain user feedback for new sample name."""

        msg = f"""
        Provide a different name for sample '{x}':"""

        item = 'New sample name'
        pattern = '^[a-zA-Z0-9_@:#&%+*=|!?~{}()-]+$'
        p = PresentDialog(msg, item, pattern,fcie=test_new)
        return p.display_dialog()

    old = select_from(todolist)
    tuplelist = [ (x, get_sample_name(x)) for x in old]
    usetuples = [ (x,y) for (x,y) in tuplelist if y != PresentDialog.SKIP ]
    print(usetuples)
    return usetuples


def select_from(alist):
    """Obtain user choice for items from given list.

    Parameters
    ----------
    alist : list
        List of items, or of dicts with items, to choose from.

    Returns
    -------
        List of selected items.
    """
    listeddicts = True if isinstance(alist[0],dict) else False

    def printchoices():
        msg=""
        nr = 0
        for athing in alist:
            if listeddicts:
                for key,values in athing.items():
                    msg += f"\n {key}:\n"
                    for no, value in enumerate(values, start=1+nr):
                        msg += f"  {no}: {value}\t"
                nr = no
            else: # just items, no dicts with items in alist
                msg += f"  {nr+1}: {athing}\t"
                nr += 1
        return msg

    def getchoices(userinput):
        uinput = userinput.replace(' ','').strip()
        if ',' in uinput:
            uinputlist = uinput.split(',')
        #print(uinput)
            keylist = [ int(x) for x in uinputlist if x != '']
        elif not ',' in uinput: # one item
            keylist =[ int(uinput) ]

        choices = {}
        nr = 0
        for athing in alist:
            if listeddicts:
                for no, value in enumerate(*athing.values(), start=1+nr):
                    choices[no] = value
                nr = no
            else:
                choices[nr+1] = athing
                nr += 1

        samplechoices = []
        for x in keylist:
            if x in choices.keys():
                samplechoices.append(choices[x])
            else:
                print(f"\tNote, '{x}' is not a listed option.")
                return False
        return sorted(samplechoices)

    msg = f"""
      List item numbers, separated by a comma (','). Choose from:
    {printchoices()}
    """
    item = "Item(s)"
    pattern = '^[\s]*([\s]*[0-9]+[\s]*,)*[\s]*[0-9]+[\s]*,?[\s]*$'
    p = PresentDialog(msg, item, pattern, False, getchoices)
    return p.display_dialog()


def suggest_storepath(path=None):
    """Store Coalispr data and configuration files in suggested directory.

    Parameters
    ----------
    path : Path
        Location of configuration files (default: `None`); **CONFPATH**  might
        not be set properly yet, absent at beginning and needs to be chosen.

    Returns
    -------
    Local storage folder including sub-folders for data and configuration
    templates ('constant_in')
    """
    logging.debug(f"{__name__}.{thisfunc()}")

    path_choices = {
        HOME: Path.home() / PRGNAM,
        CWD: Path().resolve() / PRGNAM,
        SRCPRGNAM: Path(__file__).parent.parent.parent,
        }
    msg = f'''
        Set the work folder for this session/experiment.

        Files can be stored in folder '{PRGNAM}', either in the user's
        {HOME} directory, or in the {CWD} folder - change directory to
        this destination first; alternatively, keep files near the
        {SRCPRGNAM} code, in the '{PRGNAM.lower()}' installation folder.

        Configuration files, figures and data go into sub-folders:
        '{CONFFOLDER}' for configuration files, '{FIGS}' for images,
        and '{DATA}' for storage of .pkl and {TSV} files.

        Please choose a folder.
        '''
    item = (f"Path to {PRGNAM} folder")
    pattern = '[1-3]'

    if not path:
        p = PresentDialog(msg, item, pattern, None)
        pname = p.display_choices(path_choices, ".parent.stem")
        return  pname if pname != PresentDialog.SKIP else None
    else:
        return path
