#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  groupcompare_plots.py
#
#  Copyright 2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module to plot count comparisons between typed samples for a given group.

   Relevant file names:

   ``tsvpath/<countfolder>/{kind}_{RLENCOUNTS}_{strand}TSV``

"""
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import pandas as pd

from coalispr.bedgraph_analyze.experiment import (
    get_grplabels,
    )
from coalispr.bedgraph_analyze.store import (
    save_average_table,
    )
from coalispr.count_analyze.load_countfile import (
    get_readlengths_frame,
    )
from coalispr.resources.constant import (
    CNTLABELS,
    EXP, EXPDISP,
    GROUPAVG,
    MEAN, MEDIAN,
    PLOTLEN, PLOTMEAN, PLOTMEDIAN, PLOTSTRT,
    RLENCOUNTS,
    SNSFNTSZ,
    THISALPH,
    )
from coalispr.resources.plot_utilities import (
    capit_label,
    edit_toolbar,
    get_context,
    init_sns,
    no_titles,
    save_output_as,
    set_axes,
    )

from coalispr.resources.utilities import (
    clean_dict,
    doneon,
    get_ylabel,
    joinall,
    joiner,
    remove_odds,
    thisfunc,
    )

logger = logging.getLogger(__name__)

init_sns()

# by ImportanceOfBeingErnest
# stackoverflow.com/questions/42017049/seaborn-how-to-add-error-bars-on-a-grouped-barplot#42033734
# adapted for nsamples
def _grouped_barplot(df, cat, subcat, val, err, nsamples):
    """ cat = "Candidate"
        subcat = "Sample_Set"
        val = "Values"
        err = "Error"
        nsamples = "n"
        df = pd.read_csv(datafile)
        """
    lfont = font_manager.FontProperties(family='monospace')
    u = df[cat].unique()
    x = np.arange(len(u))
    subx = df[subcat].unique()
    lsubx = len(subx)
    offsets = (np.arange(lsubx)-np.arange(lsubx).mean())/(lsubx+1.)
    width= np.diff(offsets).mean()
    for i,gr in enumerate(subx):
        dfg = df[df[subcat] == gr]
        plt.bar(x+offsets[i], dfg[val].values, width=width, alpha=THISALPH,
                label=f"{gr}   (n={dfg[nsamples].unique()[0]})",
                yerr=dfg[err].values, error_kw=dict(ecolor='gray', lw=1,
                capsize=3, capthick=1))
    plt.xlabel(cat)
    plt.ylabel(val)
    plt.xticks(x, u)
    plt.legend( prop=lfont)


@mpl.rc_context({"figure.autolayout":True, **get_context()})
def _plot_5NTlengths(dfall, types, var, titles):
    """Plot length distribution for given start nt."""
    figtitle = titles['suptitl']
    wintitle = titles['wintitl']
    cat = PLOTLEN #'length'
    subcat = 'type'
    err = 'std'
    nsamples = 'n'
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    _grouped_barplot(dfall, cat, subcat, var, err, nsamples )
    edit_toolbar(fig, True)
    leg = ax.legend(title=titles['legtitl'], loc='right',#)
        fontsize=SNSFNTSZ, #
        title_fontsize=SNSFNTSZ,#
        bbox_to_anchor=(1.03, 0.8))
    leg.set_draggable(True)
    yflt = 'y2' if dfall[var].max() < 1 else 'y'
    set_axes(ax, format_ax=yflt)
    ax.set_ylabel( titles['ylabel'] )
    fig.suptitle(figtitle, fontsize='large' ,x=0.5, y=0.95, ha='center',
        va='top')
    fig.canvas.manager.set_window_title(f"{wintitle}")
    save_output_as(wintitle, GROUPAVG)
    plt.show()
    plt.close()


@mpl.rc_context({"figure.autolayout":True, **get_context()}) #groupcompare -ld
def compare_5nt_lengths(rdkind, nt5, grp, grpdict, samples, types, subtypes,
    readlen, var, strand, mulmap, use, notitles):
    """Compare read-length distribution for a given group of types and library
    samples for reads with a given start nt.

    Relevant file-titles: ``{kind}_{RLENCOUNTS}_{strand}TSV``.

    Parameters
    ----------
    rdkind : str
        One of **LIBR**, cDNAs (**COLLR**), **CHRXTRA**, possibly preceded by
        **UNIQ** or **MULMAP** to get only uniquely-mapped reads (**UNIQ**),
        or the repetitive sequences (**MULMAP**) like tRNA, rRNA or some
        transposons).
    nt5 : str
        Start nucleotide; 'T', 'A', 'G', 'C' or 'N'.
    grp : str
        Original group (**METHOD**, **FRACTION**, **CONDITION** or **GROUP**),
        subgroups of which are in the comparison.
    grpdict : dict
        Dictionary of subgroups vs samples in chosen group to compare.
    samples : list
        List of short names for samples to use for plotting.
    types : list
        List with names for grouping of samples, to compare.
    subtypes : dict
        Collection of names for subgrouping of samples.
    readlen : tuple
        Limits (int,int) of read lengths to show.
    var : str
        Name for constant to select mean or median as standard for average;
        variance will be calculated.
    strand : str
        One of **COMBI**, **MUNR**, or **CORB**.
    mulmap : str
        Constant to refer to count files to be used, for **UNIQ**, **MULMAP** or
        none ('').
    use : str
        Tag to filter particular reads.
    notitles : bool
        Flag to set display of figure title on graph.
    """
    def typlabel(group,types):
        #logging.debug(f"{__name__}.{thisfunc()}{group,types}")
        typlabels = [ get_grplabels(group)[typ] for typ in types ]
        logging.debug(f"{group}: {typlabels}")
        return typlabels

    nam = f"{rdkind}_{RLENCOUNTS}_{strand}"
    # countdata
    df = get_readlengths_frame(nam, use, debug=0)
    numbers = [PLOTLEN, PLOTSTRT]
    df_in = df[ numbers + samples ].groupby(PLOTSTRT).get_group(nt5)
    df_in = df_in[ (df_in[PLOTLEN].astype(int) >= readlen[0])   #XLIM00)
                 & (df_in[PLOTLEN].astype(int) <= readlen[1]) ] #XLIM11) ]
    # experiment connections
    samtyps = clean_dict( {typ: [x for x in grpdict[typ] if x in samples]
                            for typ in types } )
    typelabels = typlabel(grp,types)
    labld_subtypes = ({ sgrp : [ styp for styp in typlabel(sgrp, styps) ] for
                            sgrp, styps in subtypes.items() })
    libno = len(samples)
    # build average table with categories
    dfNT5 = {}
    for ktyp, vsampls in samtyps.items():
        #print(ktyp, vsampls)
        dftyp = df_in[ numbers].copy()
        if var == MEDIAN:
            dftyp[var] = df_in[vsampls].copy().median(axis=1)
        elif var == MEAN:
            dftyp[var] = df_in[vsampls].copy().mean(axis=1)
        dftyp['std'] = df_in[vsampls].copy().std(axis=1)
        dftyp['n'] = df_in[vsampls].copy().count(axis =1)
        dftyp['type'] = get_grplabels(grp)[ktyp]
        dfNT5[ktyp] = dftyp.set_index(PLOTLEN)
    dfNT5all = pd.concat(objs=dfNT5.values()).reset_index()

    subs = ' '
    sgrps = ''
    if subtypes:
        subs = f", subtypes '{joinall(labld_subtypes,joiner())}' "
        newln = '\n'
        sgrps = f"\n{joinall(labld_subtypes, newln)}"
    msg = (f"\nGrouped length distributions according to '{grp}', types '"
           f"{joiner().join(typelabels)}'{subs}for {use.lower()} "
           f"{CNTLABELS[rdkind]} as bar graphs for {libno} libraries (for "
           f"{strand} strands).")
    print(msg)

    ylabA = (f"{PLOTMEAN if var==MEAN else PLOTMEDIAN} ")
    ylabB   = f"{use.lower()} {get_ylabel(rdkind, strand, 4)}"
    ylabel = ylabA.format(capit_label(ylabB))
    suptitl = (f"Average {rdkind} length distribution for {use.lower()} "
           f"{EXPDISP} reads:\n{strand} strands of {libno} libraries "
           f"for {grp.lower()} types '{joiner().join(typelabels)}'{subs}.")
    suptitl = no_titles(suptitl,notitles)

    wintitl = remove_odds(f"{grp} {sgrps} {rdkind} {nt5} length distributions "
           f"{EXP} {libno} {use} {strand}"
           f"{' ' if not notitles else ' notitles '}{doneon()}").lower()
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    ltitl = f"{grp}; {PLOTSTRT}: {nt5}{sgrps}"
    ftitles = {'legtitl':ltitl, 'suptitl':suptitl, 'wintitl':wintitl,
        'ylabel':ylabel,
        }
    _plot_5NTlengths(dfNT5all, types=types, var=var, titles=ftitles)
    save_average_table(df=dfNT5all, name=wintitl, use=use, samples=samples)
