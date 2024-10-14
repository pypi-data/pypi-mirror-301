#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  experiment.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#

"""Module to manage experiments and samples."""
from coalispr.bedgraph_analyze.collect_bedgraphs import (
    label_frame,
    get_experiments,
    )
from coalispr.resources.constant import (
    ALL,
    CAT_D, CATEGORY, CAT_M, CAT_R, CAT_S, CAT_U, CONDITION, CONDITIONS,
    DISCARD,
    EXPFILE,
    FRACTION, FRACTIONS,
    GROUP,
    METHOD, METHODS, MUTANT, MUTANTS, MUTGROUPS,
    NEGCTL,
    OTHR,
    POSCTL,
    REST,
    UNSPECIFICS,
    )


def all_exps(plusdiscards=True, allpos=True, allneg=True, allmut=True):
    """Return **SHORT** names for all (non-redundant) experimental/data samples.

    Parameters
    ----------
    plusdiscards : bool
        If 'True', any **CAT_D** samples will be included.
    minimal : bool (default: `False`)
        Flag to include redundant samples, i.e. to return all mutant samples.
    """
    global _AllExps

    try:
        if allpos and allneg and allmut:
            return _AllExps
        else:
            exps = sorted( set( controls(allpos, allneg) ).union(
                                    mutant(allmut) ) )
            if plusdiscards:
                exps += discarded()
            return exps
    except NameError:
        _AllExps = get_experiments(plusdiscards = plusdiscards) # category= not CAT_R)
        return _AllExps


def controls(allpos=True, allneg=True):
    """Return **SHORT** names for positive and negative control samples."""
    return  sorted( set(positive(allpos)).union(negative(allneg)) )


def discarded():
    """Return **SHORT** names for discarded samples (**CAT_D**)."""
    global _Discards
    try:
        return _Discards
    except NameError:
        _Discards = get_experiments(category=CAT_D)
        return _Discards


def for_group(group, plusdiscards=False, samples=None): #, onlydiscards=False):
    """Return dicts of group member names vs. lenghts and samples.

    Parameters
    ----------
    group: str
        Name of group to use.
    plusdiscards : bool
        If 'True', any **CAT_D** samples will be included.
    samples: list
        Samples to group
    """
    if group in [METHOD, FRACTION, CONDITION]:
        return _for_methfractcond(group, plusdiscards, samples)
    else:
        return _for_category(plusdiscards, samples) #, onlydiscards)


def get_grplabels(keygrp):
    """Return labels to denote various samples in a group. This could be for
    **REST** or **ALL**.

    Parameters
    ----------
    keygrp : str
        Key for selecting proper dictionary with group labels.
    """
    rests = { REST: REST.capitalize(), REST.upper(): REST.capitalize(),
              ALL: ALL.capitalize(), ALL.upper(): ALL.capitalize()
              }

    grpdicts = {
        METHOD: {**METHODS, **rests},
        FRACTION: {**FRACTIONS, **rests},
        CONDITION: {**CONDITIONS, **rests},
        GROUP: {**MUTGROUPS, **rests},
        }

    return grpdicts[keygrp]


def goption():
    """Assemble values for -g command-line options according to availability.

    Returns
    -------
    dict
        Dictionary to assemble command parser item '-g' and options vs. choices.
        {'usegroups':{1:CATEGORY, 2:grouping2,},
        '-g':' -g{1,2,}',
        'glist':[1, 2,],
        '-h':'Group libraries according to 1: CATEGORY; 2: grouping2;.'
        }
    """
    usegrps = {1: f"{CATEGORY}"}
    goptions = {'usegroups':usegrps, '-g':'', 'glist':[], '-h':''}
    grps = mixed_groups()
    if not grps:
        return goptions

    for k,v in enumerate(grps.keys(),2):
        # no CONDITION for -g to organize all samples according to group
        if v in [METHOD, FRACTION, CONDITION]:
            usegrps[k] = v

    goptions['usegroups'] = usegrps
    grplist = list(usegrps.keys())
    if len(grplist) > 1:
        goptions['-h'] = ("Group libraries according to "
           f"{'; '.join(f'{k}: {v.upper()}' for k,v in usegrps.items())}.")
        # convert list of int to list of str first before join
        goptions['-g'] = ' -g{' + f'{",".join(str(v) for v in grplist)}' + '}'
        goptions['glist'] = grplist
    return goptions


def has_discards():
    """Return True if samples have been declared as unused (**CAT_D**)"""
    global _hasDiscards
    try:
        return _hasDiscards
    except NameError:
        _hasDiscards = len(discarded()) > 0
        return _hasDiscards


def has_redundant_muts():
    """Return True if samples have been declared as **CAT_M**.lower()"""
    global _hasRedMuts
    try:
        return _hasRedMuts
    except NameError:
        _hasRedMuts = len(_redundantmutants()) > 0
        return _hasRedMuts


def has_grouparg():
    """Boolean to indicate if -g command-line option is feasible"""
    global hasGrouping

    try:
        return hasGrouping
    except NameError:
        hasGrouping = True if goption()['-h'] else False
        return hasGrouping


def mixed_groups(plusdiscards=False, allmut=False, samples=None):
    """Return nested dict with sample names for groups with multiple subgroups
    (for group-comparison).

    Parameters
    ----------
    plusdiscards : bool
        If 'True', any **CAT_D** samples will be included.
    allmut : bool (default: `False`)
        Flag to include redundant samples, i.e. to return all mutant samples.
    samples: list
        List of samples.
    """
    global _MixGrpsI, _MixGrpsII
    try:
        return _MixGrpsI if not allmut else _MixGrpsII
    except NameError:
        grps = [METHOD, FRACTION, CONDITION, GROUP]
        _mixgrps = {}
        samples = samples if samples else all_exps(plusdiscards, allmut=allmut)
        for colnam in grps:
            _rest = set(samples)
            subgrpnams = _gettypes(colnam, plusdiscards, samples)
            grptypes = {}
            if len(subgrpnams) >1:
                for subgrp in subgrpnams:
                    sm = _grplist(colnam, subgrp, plusdiscards, samples)
                    if len(sm) >0: # exclude categories without samples
                        grptypes[subgrp] = sm
                        _rest -= set(sm)
                if _rest:
                    grptypes[REST.upper()] = sorted(_rest)
                _mixgrps[colnam] = grptypes
        if not allmut:
            _MixGrpsI = _mixgrps
        else:
            _MixGrpsII = _mixgrps
        return _MixGrpsI if not allmut else _MixGrpsII


def mutant(allmut=False):
    """Return **SHORT** names for mutant samples (**CAT_M**).

    Get mutants to be analyzed. Set 'allmut' to `True` to include redundant
    samples. This could change/induce bias when deviance (from positive
    controls) of mapped reads gets more weight due to a larger number of
    similar (technical) repeats.

    Parameters
    ----------
    allmut : bool (default: `False`)
        Flag to include redundant samples, i.e. to return all mutant samples.

    Returns
    -------
    list
        A list of **SHORT** names for non-redundant or (all) mutant samples.
    """
    global _muts
    try:
        if not allmut:
            return _muts
        else:
            return [*get_experiments(category=CAT_M),
                *get_experiments(category=CAT_M.lower())]
    except NameError:
        _muts = get_experiments(category=CAT_M)
        return _muts


def negative(allneg=True):
    """Return list of **SHORT** names for negative control samples (**CAT_U**).

    Parameters
    ----------
    minimal : bool (default: `False`)
        Flag to include all negative control samples where process is found to
        be turned off (`False`) or when proteins expected to bind sequenced RNA
        or are known to be essential to sustain the biological process under
        study have been inactivated/deleted; this is the minimal set of negative
        controls (`True`)`), marked by **CAT_U** in uppercase in **EXPFILE**.
    """
    global _Negative
    try:
        if allneg:
            return _Negative
        else:
            return get_experiments(category=CAT_U)
    except NameError:
        _Negative = [*get_experiments(category=CAT_U),
            *get_experiments(category=CAT_U.lower())]
        return _Negative


def othr(plusdiscards=False):
    """Return **SHORT** names for samples defined as **OTHR**.

    Parameters
    ----------
    plusdiscards : bool
        If 'True', any **CAT_D** samples will be included.
    """
    global _othr
    try:
        return _othr
    except NameError:
        _othr = _grplist(GROUP, OTHR, plusdiscards)
        return _othr


def positive(allpos=True):
    """Return **SHORT** names for positive control samples (**CAT_S**). Samples
       marked by **CAT_S** in uppercase in **EXPFILE** are collected only. """
    global _Positive
    try:
        if allpos:
            return _Positive
        else:
            return get_experiments(category=CAT_S)
    except NameError:
        _Positive = [*get_experiments(category=CAT_S),
            *get_experiments(category=CAT_S.lower())]
        return _Positive


def reference():
    """Return **SHORT** names for reference samples (**CAT_R**)."""
    global _Reference
    try:
        return _Reference
    except NameError:
        _Reference = get_experiments(category=CAT_R)
        return _Reference


def _for_category(plusdiscards, samples): #, onlydiscards=False):
    """Return dicts of **CATEGORY** names vs lenghts and samples.

    Parameters
    ----------
    plusdiscards : bool
        Flag to indicate whether **CAT_D** samples need to be included.
    samples: list
        Samples to group
    plusdiscards : bool
        If 'True', any **CAT_D** samples will be included.
    """
    neg_ = get_negative()
    pos_ = get_positive()
    mut_ = mutant(True)
    dis_ = discarded()
    if samples != None:
        neg_ = sorted(list(set(samples).intersection(neg_)))
        pos_ = sorted(list(set(samples).intersection(pos_)))
        mut_ = sorted(list(set(samples).intersection(mut_)))
        #print("using samples")
        dis_ = sorted(list(set(samples).intersection(dis_)))

    lens = {} # dict for group name vs length of group
    nams = [NEGCTL, POSCTL, MUTANT]
    sampls = { # dict for group name vs members of group
        NEGCTL:neg_,
        POSCTL:pos_,
        MUTANT:mut_,
        }
    if len(dis_) > 0 and plusdiscards:
        sampls[DISCARD] = dis_
        nams.append(DISCARD)
    '''
    elif len(dis_) > 0 and onlydiscards:
        nams = [DISCARD]
        sampls = {DISCARD:dis_,}
    '''
    for cat in nams.copy(): # .copy() to continue loop when deleting from nams
        sm = sampls[cat]
        lsm = len(sm)
        if lsm == 0:
            nams.remove(cat)
            del sampls[cat]
            continue
        lens[cat] = lsm

    return nams, lens, sampls


def _for_methfractcond(colnam, plusdiscards, samples):
    """Return dicts of names of subgroups for colnam (**METHOD**, or
    **FRACTION** or **CONDITION**) vs. numbers and samples."""
    subgrps = mixed_groups()[colnam]
    lens = {} # dict for group name vs length of group
    sampls = {} # dict for group name vs members of group
    nams = list(subgrps.keys()) #_gettypes(colnam, plusdiscards, samples)

    for subgrp, subsamples in subgrps.items():
        sm = subsamples #_grplist(colnam, subgrp, plusdiscards, samples)
        lsm = len(sm)
        if lsm:
            sampls[subgrp] = sm
            lens[subgrp] = lsm
    return nams, lens, sampls


def _getshortsdict(colnam, listofgroupkeys, plusdiscards, df=None):
    """Return labels for groups in defined order with associated lists of
    **SHORT** names if present in data frame.

    Parameters
    ----------
    colnam : str
        Constant referring to column header in **EXPFILE** to be searched for
        groups.
    listofgroupkeys : str
        Constant referring to ordered list of groups (keys for groupdict defined
        in **EXPFILE**  as dict of groupconstants vs. labels, that is:
        **MUTGROUPS**, **CONDITIONS**, **METHODS**, or **FRACTIONS**).
    plusdiscards : bool
        Flag to indicate whether **CAT_D** samples need to be included.
    df : Pandas.DataFrame
        Data that covers libraries in list

    Returns
    -------
    dict
        A dictionary of group names as keys with lists of **SHORT** sample
        names as values.
    """
    columns = {GROUP : MUTGROUPS, CONDITION: CONDITIONS, METHOD: METHODS,
        FRACTION: FRACTIONS }

    if len(columns[colnam]) > 0:
        if not isinstance(columns[colnam], dict):
            msg = (f"Constant ('{colnam}') is linked to some item, but not to "
                "a collection/dictionary of groups with display labels. Check "
                f"the **EXPFILE** ('{EXPFILE}').")
            raise SystemExit(msg)

    groupdict = columns[colnam]
    shortsdict = {}

    for group in listofgroupkeys:
        grpname = groupdict[group]
        grplist = _grplist(colnam, group, plusdiscards, df)
        if grplist:
            shortsdict[grpname] = grplist
    return shortsdict

def _gettypes(sampletype, plusdiscards, samples):
    """Return non-redundant types in a group of samples of given category.

    Parameters
    ----------
    sampletype : str
        Group name (**METHOD**, **CONDITION**, **GROUP**) for which types to
        return.
    plusdiscards : bool
        If 'True', any **CAT_D** samples will be included.
    samples: list
        Samples to group

    Returns
    -------
    numpy.ndarray
        Array of typenames present in given group.
    """
    types = []
    if isinstance(samples, list) and len(samples) > 0:
        types =  list(label_frame().loc[samples,sampletype].unique())
    elif samples == None:
        data = _getwanted(plusdiscards)
        # When '' (no value), get rid of nan output; only return unique values.
        types = list(label_frame()[data][sampletype].dropna().unique())
    return types


def _getwanted(plusdiscards):
    """Return boolean column for wanted (= experiment) rows.

    Parameters
    ----------
    plusdiscards : bool
        If 'True', any **CAT_D** samples will be included.
    """
    global _Wanted
    try:
        return _Wanted
    except NameError:
        # unwanted = [CAT_R, CAT_D]
        wanted = [CAT_U, CAT_S, CAT_M]
        if plusdiscards:
            wanted.append(CAT_D)  #else [CAT_D]
        # Some types could be associated with lower case category labels.
        wanted += [x.lower() for x in wanted]
        _Wanted = label_frame()[CATEGORY].isin(wanted)
        return _Wanted


def _grplist(group, subgroup, plusdiscards, samples):
    """Return list of samples for a group in [**METHOD**, **FRACTION**,
    **CONDITION**, **GROUP**] that are in a given subgroup.

    Parameters
    ----------
    group : str
        Name of group column **GROUP** of **EXPFILE** to be found.
    subgroup : str
        Name of characteristic in group to select (eg. **RIP1** in **METHOD**)
    plusdiscards : bool
        Flag to indicate whether **CAT_D** samples need to be included.
    samples : list
         List of **SHORT** names to select those of a particular group from.

    Returns
    -------
    list
        A list of samples being part of given group.
    """
    fram = label_frame()[_getwanted(plusdiscards)]
    ingroup = fram[group] == subgroup
    grplist = sorted(list(fram[ingroup].index))
    if isinstance(samples, list):
        return [x for x in grplist if x in samples]
    return grplist


def _redundantmutants():
    """Return **SHORT** names for redundant mutant samples **CAT_M**.lower()."""
    global _redmuts
    try:
        return _redmuts
    except NameError:
        _redmuts = get_experiments(category=CAT_M.lower())
        return _redmuts


# Method to build side panel with groups in bedgraph plots.
# ---------------------------------------------------------

def mutant_groups(df):
    """Build and return a list of tuples for generating sidepanels with
    labels described in group dicts like **MUTGROUPS** in **EXPFILE**;
    Samples are selected from dataframe incl. discards if needed; being
    marked irrelevant, discards do not get a legend in the side panel.

    ::

        Determines order of appearance: [
            (NEGCTL, _getshortsdict(GROUP, UNSPECIFICS)),
            (METHOD, _getshortsdict(METHOD, METHODS)),
            (FRACTION, _getshortsdict(FRACTION, FRACTIONS)),
            (CONDITION, _getshortsdict(CONDITION, CONDITIONS)),
            (MUTANT, _getshortsdict(GROUP, MUTANTS)),
            ]


    Parameters
    ----------
    df : Pandas.DataFrame
        Dataframe like that for merged bedgraphs: sample names to be retrieved
        - to define groupings via the **EXPFILE** - are in the columns.
    """
    groupings = [
        (NEGCTL, GROUP, UNSPECIFICS),
        (METHOD, METHOD, METHODS),
        (FRACTION, FRACTION, FRACTIONS),
        (CONDITION, CONDITION, CONDITIONS),
        (MUTANT, GROUP, MUTANTS),
        ]
    plusdiscards=False # not included
    tupleslist =  []
    samples = list(df.columns)

    for grpnam, colnam, collection in groupings:
        dict_ = _getshortsdict(colnam, collection, plusdiscards, samples)
        if dict_:
            tupleslist.append( (grpnam, dict_) )
    return tupleslist


# Methods to select from data dataframes using experiment file definitions.
# -------------------------------------------------------------------------

def drop_discarded(df):
    """Return dataframe without discarded samples.

    Calling function should check for empty discarded() (and then skip this)
    """
    df=df.drop([x for x in discarded() if x in df.columns], axis=1)
    return df


def get_discard(df=None):
    """Provide discard selection present in dataframe df."""
    if df is not None:
        return [x for x in discarded() if x in df.columns]
    return discarded()


def get_mutant(df=None, allmut=False):
    """Provide mutant selection present in dataframe df."""
    muts = mutant(allmut)
    if df is not None:
        return [x for x in muts if x in df.columns]
    return muts


def get_negative(df=None, allneg=True):
    """Provide negative control selection present in dataframe df."""
    negs = negative(allneg)
    if df is not None:
        return [x for x in negs if x in df.columns]
    return negs

def get_positive(df=None, allpos=True):
    """Provide positive control selection present in dataframe df."""
    posi = positive(allpos)
    if df is not None:
        return [x for x in posi if x in df.columns]
    return posi


def get_reference(df=None):
    """Provide reference selection present in dataframe df."""
    if df is not None:
        return [x for x in reference() if x in df.columns]
    return reference()
