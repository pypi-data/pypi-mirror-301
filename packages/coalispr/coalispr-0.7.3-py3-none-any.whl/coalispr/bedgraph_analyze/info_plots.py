#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  info_plots.py
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module to plot info on program parameters or mapped data."""
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


from coalispr.bedgraph_analyze.experiment import for_group
from coalispr.bedgraph_analyze.store import get_inputtotals
from coalispr.resources.constant import (
    ALPH,
    DATASTOR,
    EXP,
    INFOREGS,
    INMAPCOLL, INMAPUNCOLL,
    LINEW, LOG2BG, LOG2BGTST,
    MINUS,
    PLOTRAW, PLUS,
    REGCNTS, REGS,
    SAVETSV, SCOL, STOREPATH,
    TAGUNCOLL, TSV, TRSHLD,
    UNMAP, UNSPECLOG10, UNSPECTST,
    )
from coalispr.count_analyze.panel_plotters import (
    CountPanelPlotter,
    Log2CountPanelPlotter,
    )
from coalispr.resources.plot_utilities import (
    edit_toolbar,
    get_context,
    init_sns,
    no_titles,
    save_output_as,
    set_axes,
    )
from coalispr.resources.utilities import (
    doneon,
    get_skip,
    get_string_info,
    remove_odds,
    thisfunc,
    )

logger = logging.getLogger(__name__)
init_sns()

@mpl.rc_context(get_context())
def show_regions_vs_settings(tag, notitles):
    """For picking some good value, keeping enough but no too many.

    Returns
    -------
    Two diagrams with seaborn plots
        Plots showing effects of changing parameters on number of regions
        identified for 1. **TAGUNCOLL** and 2. **TAGCOLL** reads; can be saved
        as png or svg.
    """

    def highlight_current_settings(g):
        """By picking the current UNSPECLOG10 pane and showing the current
        LOG2BG value with a dashed line"""
        lineidx = LOG2BGTST.index(LOG2BG)
        for (row_val, col_val), ax in g.axes_dict.items():
            if col_val == UNSPECLOG10:
                # get line coinciding with LOG2BG value from list
                l = ax.get_xgridlines()[lineidx]
                l.set_visible(True)
                l.set_linestyle('--')
                l.set_linewidth(LINEW)
                l.set_color(SCOL)
                l.set_alpha( ALPH)
                #ax.set_facecolor(".98")

    def show_data():
        title=("Settings vs. no. of regions with specified reads "
              f"(data: {tag})")
        title = no_titles(title, notitles)
        wtitl = remove_odds(f"{tag} regions vs settings for {EXP} "
          f"log2bg{LOG2BG} skip{get_skip()}"
          f"{' notitles' if notitles else ''} {doneon()}")
        # FacetGrid
        g = sns.catplot(
            data = dg,
            x = 'LOG2BG',
            y = REGS,
            hue = 'USEGAPS',
            col = 'UNSPECLOG10',
            row = 'KIND',
            height = 2,
            aspect = 1,
            margin_titles = True,
            sharex = True,
            #https://stackoverflow.com/questions/36016736/seaborn-facetgrid-axes-sharing-x-axis-across-rows-y-axis-across-columns
            sharey = "row",
            kind = 'point',
            legend = False,
            )
        axes=g.axes.flatten()
        for ax in axes:
            set_axes(ax, format_ax='y')
        g.add_legend(title='USEGAPS',loc='upper right',
            bbox_to_anchor=(0.98, 0.6))
        leg = g._legend
        leg.set_draggable(True)
        g.figure.subplots_adjust(top=0.9)
        if notitles == False:
            g.figure.suptitle(title)
        g.figure.set_size_inches(15,9)
        g.figure.canvas.manager.set_window_title(wtitl)
        highlight_current_settings(g)
        edit_toolbar(g.fig)
        save_output_as(wtitl, REGCNTS)
        plt.show()
        plt.close()

    testdata = STOREPATH.joinpath(SAVETSV,f"test_intervals{TSV}")
    try:
        df = pd.read_csv(testdata, sep="\t", comment="#", index_col=0,
            header=[0],
            dtype={'TAG': 'str','KIND': 'str', 'UNSPECLOG10': 'float',
                   'LOG2BG': 'int', 'USEGAPS': 'int',
                   REGS: 'int', TRSHLD: 'int'},
             skipinitialspace=True)
        logging.debug(f"{__name__}.{thisfunc()}:\n{get_string_info(df)}")
        logging.debug(f"{__name__}.{thisfunc()}:\n{df.head()}")
        _logs10 = list(UNSPECTST)
        data = df['UNSPECLOG10'].isin(_logs10)
        hastag = df['TAG'].str.startswith(tag.lower())

        dg = df[data & hastag].drop(TRSHLD, axis=1)
        show_data()

    except FileNotFoundError as e:
        msg = (f"No input files found. These are created by {INFOREGS}; "
                "did that step complete?")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}\n{e}")
        raise SystemExit(msg)
    except ValueError as e:
        msg = (f"No input data found. Did data get stored for type '{tag}' by "
               f"{DATASTOR}?")
        logging.debug(f"{__name__}.{thisfunc()}:\n{msg}\n{e}")
        raise SystemExit(msg)


@mpl.rc_context(get_context())
def show_mapped_vs_unmapped(tag, group, showdiscards, notitles, log2=False):
    """Provide a quick impression of sequencing data.

    Parameters
    ----------
    tag   : str
        Label marking type of reads analyzed: **TAGCOLL** or **TAGUNCOLL**.
    group : str
        Name determining grouping of samples, either **CATEGORY**, **METHOD** or
        **FRACTION**.
    log2 : bool
        Use log2 scale if True.

    Returns
    -------
    Diagrams with seaborn barh plots for collapsed or uncollapsed data;
        Plots showing total input numbers of mapped and unmapped (if available)
        reads; can be saved as png or svg.
    """
    msg = ("Showing available input counts "
           f"{'on a log2 scale' if log2 else ''} as bar graphs, split by "
           f"{group.lower()}{' (incl. unused)' if showdiscards else ''}\n")
    print(msg)
    df = get_inputtotals(kind=tag)
    col = INMAPUNCOLL if tag == TAGUNCOLL else INMAPCOLL
    # write df.info() to logger only
    #msg += f"\n{get_string_info(df)}"
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    #nams [] of group types/names
    #lens {] for group name vs length of group
    #sampls {} for group name vs members of group
    nams, lens, sampls = for_group(group, showdiscards)

    numbers = [PLUS, MINUS, UNMAP]
    #libno = sum(lens.values())
    ylabel = f"{tag.capitalize()} reads"
    xlabel = PLOTRAW
    suptitl = (f"Stranded {INMAPUNCOLL.lower()} vs. {UNMAP.lower()} "
               f"{tag.lower()} reads\n") #{libno} libraries grouped by {group.lower()}")
    suptitl = no_titles(suptitl, notitles)
    wintitl = (f"{'withdiscards ' if showdiscards else ''}"
               f"{tag} {'log2 ' if log2 else ''}input per {group} {EXP} "
               f"log2bg{LOG2BG} skip{get_skip()}"
               f"{' notitles' if notitles else ''} {doneon()}")
    ftitles = {'legtitl': col,'suptitl': suptitl, 'wintitl': wintitl,
        'xlabel': xlabel, 'ylabel': ylabel}
    fcie = Log2CountPanelPlotter if log2 else CountPanelPlotter
    fcie(group, nams, lens, sampls, df, numbers, ftitles,
        ).plot_panels()
