#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  plot_utilities.py
#
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings

from matplotlib.offsetbox import AnchoredText

from coalispr.resources.constant import (
    ALPH, AXCOL, AXCOL2, AXLIMS,
    BACKEND,
    CONTEXT, CSFONTSZ,
    FIGCOL, FIGDIR, FIGFORMAT,
    GRID, GRIDALPHA, GRIDAXIS, GRIDCOLOR, GRIDSTYLE, GRIDWHICH,
    INTSTEP,
    MPLDEBUG,
    NONCAPT,
    PALETTE, PERC,
    SKIPINT, SNSFNTFAM, SNSFNTSZ,
    TXTALIAS,
    )

"""Functions used in plot modules."""
logger = logging.getLogger(__name__)

if not MPLDEBUG:
    logging.getLogger('matplotlib').setLevel(logging.WARNING),
    logging.getLogger('PIL').setLevel(logging.WARNING)


warnings.filterwarnings("ignore")
'''
# https://stackoverflow.com/questions/65597911/how-can-i-get-rid-of-these-seaborn-deprecation-warning-and-still-get-the-exact-s

# https://matplotlib.org/`matplotlib.__version__`/tutorials/introductory/customizing.html#customizing-with-matplotlibrc-files
# https://matplotlib.org/users/navigation_toolbar.html
# https://github.com/matplotlib/matplotlib/issues/15284
'''
with warnings.catch_warnings():
    #warnings.simplefilter("ignore")
    mpl.rcParams['toolbar'] = 'toolmanager'


def anchored_text(text):
    """Returns text annotation to plot."""
    at = AnchoredText(text, prop=dict(size=SNSFNTSZ), frameon=False,
        loc='upper right',)
    # when frameon is True:
    #at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    #at.patch.set_edgecolor(AXCOL2)
    return at


def break_xaxis(ax, ind, r=1):
    """Construct a 'broken' xaxis, i.e. with a gap to fit most of the data.

    Notes
    -----
    This is done by restricting the numebres and adding a text-annotation
    that mimicks the dividing lines of a 'broken-axis'.

    Parameters
    ----------
    ax : AxesSubplot
        Object to manipulate xaxis for
    ind : int
        Coordinate halfway omitted interval to place '/ /' text annotation.
    r : int
        Flag to indicate amount of margin the annotation needs to be offset by.

    """
    fsize = 'xx-small' if r > 1 else 'small'
    yoff = -3 if r > 1 else -5

    ax.annotate("/ /",  xy=(ind,0), xytext = (0,yoff),
        textcoords="offset points", fontsize=fsize,
        bbox = dict(fc='w', boxstyle='square,pad=-0.2'),
        antialiased=True,
        )


def capit_label(label):
    """Create label with first word capitalized."""
    def capt(labl):
        for abbr in NONCAPT:
            if labl.startswith(abbr):
                return labl
        return labl[0].capitalize() + labl[1:]

    if label.startswith(PERC):
        labl = label.split(PERC)[1].strip()
        return f"{PERC} {capt(labl)}"

    return capt(label)


def edit_toolbar(fig, onlySave=False):
    """Adapt toolbar to keep sensible controls.

    Notes
    -----
    https://docs.python.org/3/library/warnings.html#overriding-the-default-filter
    f"https://matplotlib.org/{matplotlib.__version__}/_modules/matplotlib/backend_managers.html"
    f"https://matplotlib.org/{matplotlib.__version__}/api/backend_tools_api.html"
    f"https://matplotlib.org/{matplotlib.__version__}/api/backend_bases_api.html?highlight=toolitems#matplotlib.backend_bases.NavigationToolbar2.toolitems"

    Adapt tool items shown in GUI menu bar; omit some disruptive options.

    The resulting tuple of 4-placed tuples will become:

    ::

        toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan',
             'Left button pans, Right button zooms x/y fixes axis, CTRL fixes aspect',
             'move', 'pan'),
            ('Zoom',
             'Zoom to rectangle x/y fixes axis, CTRL fixes aspect',
             'zoom_to_rect', 'zoom'),
            ('Subplots', 'Configure subplots', 'subplots','configure_subplots'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
        )

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure for which the GUI gets shown.

    onlySave : bool
        Keep only the 'save' button in the toolbar (the rest won't be useful).

    Returns
    -------
    tuple
        toolitems, a tuple of 4-placed tuples (see above)

    """
    allbutsave = ['home', 'back', 'forward', 'pan', 'zoom', 'subplots', 'help']
    # remove ways to upset figure as described in 'help': 'allnav', 'yscale',
    #'xscale', 'nav'
    unwanted = ['subplots', 'help',]
    try:
        dump = allbutsave if onlySave else unwanted
        for tool in dump:
            try:
                fig.canvas.manager.toolmanager.remove_tool(tool)
            except AttributeError:
                pass

    except KeyError:
        print("Not all tools covered as listed in 'Help' dialog ('F1' or '?')"
              "and at end of 'matplotlib/lib/matplotlib/backend_tools.py'")


def get_context(font_size = CSFONTSZ):
    """Returns common values for matplotlib rc parameters."""
    return {#'toolbar':'toolmanager',
            #'backend': "TkAgg",
            #'backend': "QtAgg",
            #'backend': "GTK3Agg",
            #'backend': "GTK4Agg",
            'backend': BACKEND,
            'font.size': font_size, #CSFONTSZ, # 12
            'grid.alpha': GRIDALPHA,
            'grid.color': GRIDCOLOR,
            'axes.grid.axis': GRIDAXIS,
            'axes.grid.which': GRIDWHICH,
            'axes.grid': GRID,
            'axes.formatter.limits': AXLIMS, #(default: [-5, 6])
            'font.family': SNSFNTFAM,
            'figure.facecolor' : FIGCOL,
            'savefig.format': FIGFORMAT,
            'savefig.directory': FIGDIR,
            'keymap.help': '', # remove unwanted toolbar functions
            'keymap.grid': '',
            'keymap.grid_minor': '',
            'keymap.yscale': '',
            'keymap.xscale': '',
            'text.antialiased': TXTALIAS,
            }


def less_xlabels(ax, axeslist, r=1):
    """Create broken x-axis with reduced number of tick-labels.

    Parameters
    ----------
    ax : AxesSubplot
        Object to draw labels for
    axeslist : list
        Objects to draw broken axis for
    ok: bool
        Create 'broken' sign?
    r : int
        Factor to reduce number of labels.
    """
    fac = r*int(INTSTEP)
    # only set less labels when really needed (when there are too many labels)
    if fac >= len(ax.get_xticklabels()):
        return

    for ind, label in enumerate(ax.get_xticklabels()):
            if ind % fac == 0:  # every INTSTEPth label is kept
                label.set_visible(True)
                label.set_rotation(45)
            else:
                label.set_visible(False)
            if SKIPINT and label.get_text() == str(int(SKIPINT[0]-fac/2)):
                #print(ind, label)
                for ax in axeslist:
                    break_xaxis(ax, ind, r)


def init_sns():
    """Set common sns settings"""
    pass
    sns.set_style(GRIDSTYLE)
    sns.plotting_context(CONTEXT) #"notebook", font_scale=1.5)
    sns.set_palette(PALETTE)


def no_titles(text, notitles):
    """Text used for including figure titles or not."""
    return '' if notitles == True else text


def save_output_as(fnam, savdir, savepath=FIGDIR):
    """Save a figure with name at given location.

    Parameters
    ----------
    fnam : str
        Name of figure to save.
    savdir : str
        Sub-folder for similar kinds of figures.
    savepath : Path
        Path to folder with figures, **FIGDIR**, in **PRGNAM** workfolder.
    """
    filepath = savepath.joinpath(savdir)
    print(f"Saving to file in {filepath}")
    plt.savefig(filepath.joinpath(fnam),
        bbox_inches='tight', pad_inches=0.4,)
        #transpararent=True)


def set_axes(ax, format_ax=None, log2_ax=None):
    """Returns common values for axes of a matplotlib figure.

    Parameters
    ----------
    ax : matplotlib.axes
        Axes to adapt.
    format_ax : str
        Name of axis to format, "x" or "y".
    log2_ax : str
        Name of axis to change to log2 scale, "x" (or "y").
    """
    ax.spines['left'  ].set_color(AXCOL)
    ax.spines['top'   ].set_color(AXCOL2)
    ax.spines['right' ].set_color(AXCOL2)
    ax.spines['bottom'].set_color(AXCOL)
    ax.tick_params(axis='both', grid_color=AXCOL2, grid_alpha=ALPH)
    #change (automatic) exponential format to integer ('d')
    if log2_ax =="x":
        ax.set_xscale('log', base=2)
    #elif log2_ax =="y":
    #    ax.set_yscale('log', base=2)

    if format_ax == "y":
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    elif format_ax == "x":
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    elif format_ax == True:
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    elif format_ax == "y1":
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.1f}'))
    elif format_ax == "y2":
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.2f}'))
