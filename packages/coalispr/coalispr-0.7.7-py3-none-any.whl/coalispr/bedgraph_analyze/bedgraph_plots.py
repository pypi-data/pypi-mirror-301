#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  bedgraph_plots.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
"""Matplotlib module to create a plot with bedgraph-traces for a chromosome."""
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.style as mplstyle
#import time


from matplotlib.axis import (
    XAxis,
    YAxis,
    )
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.text import Text
from matplotlib.collections import (
    #BrokenBarHCollection, # up to matplotlib 3.6.2
    PolyCollection,       # since matplotlib 3.7.0
    )
from matplotlib.legend_handler import HandlerPatch

from coalispr.bedgraph_analyze.genom import (
    get_genom_indexes,
    GTFtrack,
    SegmentTrack,
    )
from coalispr.resources.constant import (
    ACOL, AEC, ALC, ALL, ALPH, ANNOTALPH, AXCOL, AXCOL2,
    BCKGRCOL, BINSTEP,
    CONDITION, CONFPATH, CHROMFIG, CHROMLBL,
    DCOL, DISCARD, DPI,
    EXP, EXPFILE,
    FIGCOL, FIGDIRJPG, FIGDIRPDF, FIGDIRPNG, FIGDIRSVG, FIGXLABEL, FIGYLABEL,
    FRACTION,
    HIGHALPH, HIGHLEG, HIGHLINEW,
    JPG,
    LEGNCOL, LINEW, LINLIM, LOG2BG, LOGLIM, LOWLEG,
    MCOL, METHCOL, METHOD, MINUS, MUTANT,
    NCOL, NEGCTL,
    PDF, PLUS, PNG, POSCTL, PRGNAM,
    RCOL, REFERENCE,
    SCOL, SGFONTSZ, SGHEIGHT, SGWIDTH, SPECIFIC, SVG,
    TRACKLABEL,
    UCOL, UNSEL, UNSPECIFIC,
    XGRID,
    )
from coalispr.bedgraph_analyze.experiment import (
    get_discard,
    get_mutant,
    get_negative,
    get_positive,
    get_reference,
    )
from coalispr.resources.plot_utilities import (
    edit_toolbar,
    get_context,
    )
from coalispr.resources.utilities import (
    doneon,
    remove_odds,
    thisfunc,
    )

logger = logging.getLogger(__name__)

def _describe():
    """Notes plotted with figure."""
    print(f"""
    Colours, GTFs and labels are configured in files in
    '{CONFPATH}'.
    Fonts are relative to size {SGFONTSZ} (SGFONTSZ).

    {PRGNAM} display of bedgraph traces is interactive via the:
    a. menu bar options (see tooltips) with keybindings:
          Home/Reset         h, r, home
          Back               left, c, backspace
          Forward            right, v
          Pan/Zoom           p
          Zoom-to-rect       o
          Save               s, ctrl+s
          Toggle fullscreen  f, ctrl+f
          Close Figure       ctrl+w, cmd+w, q
       Hold x or y to constrain pan/zoom to that axis.
    b. y-axis: Toggle scale between log2 and linear
          (after a change reset y-scale before Home/Back/Forward).
    c. x-axis: Print chromosomal coordinates for region shown
          (usable input for `showgraphs -r` or `region -r`).
    d. bedgraph trace: Annotate and highlight.
    e. bars in gtf, segment tracks: Annotate.
    f. legend and side panel patches: Toggle traces as a group
          (legend overrules side panel).
    g. legend: Can be dragged around.
    h. title: Toggle legend.
    i. y-axis label: Toggle title.
    j. x-axis label: Reset toggled traces.
    k. tracks label: Reset track annotations.
    """)


@mpl.rc_context(get_context(SGFONTSZ))
def plot_chrset(chrnam, dflist, setname, refs, unsel, title, dowhat, scale, lim,
        ridx, sidepatcheslist):
    """Plot bedgraphs for both strands of a chromosome in one figure.

    Plot in the range ``ridx`` to peak size ``lim`` for a list of samples
    represented each by two dataframes (one for each strand); choose a log2 or
    linear scale; a side panel with secondary legends can be included. This is
    called by ``show_chr`` functions in ``bedgraph_analyze.process_bedgraphs``.

    Output is a GUI window, when ``dowhat`` is 'show', which displays an
    interactive figure from which **PNG**, **JPG**, **SVG** etc. image files
    can be saved.

    Alternatively the function writes directly such image files to disc as
    **PNG** ('save') or **SVG** ('savesvg').

    Parameters
    ----------
    chrnam : str
        Chromosome from list ``chroms()`` to display bedgraph traces for.
    dflist : [dfs, dfa]
        List of dataframes describing **PLUS** (df1) or **MINUS** (df2) strands.
    setname : str
        Description of data set, say no. of samples.
    refs : bool
        Flag to indicate whether reference traces should be used.
    unsel : str
        Flag indicating which unselected data to include (`None`, **UNSPECIFIC**).
    title : str
        Title to display above the figure.
    dowhat : str
        Give one of 'show', **SVG**, **PDF**, **JPG**, or 'return'. Choice
        gives instruction to 'show' the figure, save it as **PNG**, **JPG**,
        or **SVG** or return it. When 'show', the figure can manually be
        saved from the window-menu with the plotted traces, including
        annotations and highlights.
    scale : str
        Instruction how to scale the y-axis, linear or after log2 conversion.
    lim : int
        Number to set another upper limit than configured in ``constant.py``.
    ridx : list
        List with lower and upper boundary of a region, e.g. [785005,790850];
        when set to `None`, the whole chromosome will be shown. Zooming to such
        regions can be done manually from the window-menu.
    sidepatcheslist : list
        List describing groups of samples to be shown under separate headings
        in the side panel.

    Returns
    -------
    None or matplotlib.figure.Figure
        Only a figure is returned with ``dowhat``-option 'return'.
    """
    # check for any data (specific reads could be completely absent)
    if setname=='0': # No samples with data; possible for specific reads..
        msg = f"Sorry, nothing to display: 0 samples with {title.lower()}."
        raise SystemExit(msg)

    # choose display
    webplt = False
    guiplt = True if not webplt else False
    # figure size
    printwidth =  int(SGWIDTH)
    printheight = int(SGHEIGHT)
    # gridspec ratios
    figwidth = 8
    figheight = 41
    # print interactive usage information to the terminal
    logging.debug(f"{__name__}.{thisfunc()}:\nAfter plotting do: '{dowhat}'")
    if dowhat =='show':
        _describe()
    # digest instructions
    showside = False if dowhat != 'show' or not sidepatcheslist else True
    logzero = 2**LOG2BG
    loglim  = 2**LOGLIM  if not lim else 2**lim
    linlim  = LINLIM if not lim else lim
    refs_ = refs
    unsel_ = unsel # UNSPECIFIC or None
    scale_ = scale if scale !=None else 'log2'
    # adapt data for region and scale conversion
    d_  = [df if not ridx else df.loc[ridx[0]:ridx[1]] for df in dflist]
    # add 0.1 to zero's for log2 scaling
    dfs = [df.fillna(0.1) for df in d_]
    # required to get proper peaks instead of unwanted, interefering extensions:
    idx = get_genom_indexes()[chrnam]
    dfs = [df.drop_duplicates().reindex(idx).fillna(0.1) for df in d_]


    if scale_ == 'log2':
        zero = logzero
        lim  = loglim
    else:
        scale_ = 'linear'
        zero = 0
        lim = linlim

    # get all the labels to plot for various groups
    neglabs = get_negative(dfs[0])
    poslabs = get_positive(dfs[0])
    mutlabs = get_mutant(dfs[0])
    dislabs = get_discard(dfs[0])

    # Prepare for plotting
    # --------------------
    # relative legend position at opening
    legpos = (0.94, 0.82) if showside else (0.96, 0.82)
    # colors used:
    axcol    = AXCOL        # axis color
    axcol2   = AXCOL2       # subdued axis color
    backgr   = BCKGRCOL     # background color
    figcol   = FIGCOL       # main frame color
    methc    = METHCOL      # 'method' color, also for other categories
    annotcol = ACOL         # annotation-background color
    annotedg = AEC          # annotation-edge color
    annarrow = ALC          # line color annotation arrow
    uc = UCOL               # color for 'unspecific'
    sc = SCOL               # color for 'specific'
    mc = MCOL               # color for 'mutant'
    rc = RCOL               # color for 'reference'
    nc = NCOL               # color for 'notselected'
    dc = DCOL               # color for 'discarded'
    # texts
    def get_figxlabel():
        labl = FIGXLABEL.format(chrnam, BINSTEP)
        if CHROMLBL:
            return f"{CHROMLBL} {labl}"
        else:
            return f"{labl[0].upper()}{labl[1:]}"

    fregion     = f'{ridx[0]}-{ridx[1]}' if ridx else ''
    axtitle     = title
    figxlabel   = get_figxlabel()
    figylabel   = FIGYLABEL
    tracklabel  = TRACKLABEL
    windowadd   = ' region {}'.format(fregion) if ridx else ''
    if guiplt:
        windowtitle = remove_odds( f'{PRGNAM} {EXP} bedgraphs chr {chrnam}'
                      f'{windowadd} {title} {setname} libs')
    # alphas
    alph      = ALPH        # build up plot density; as a measure for overlap
    highalph  = HIGHALPH    # on click show whole plot with higher intensity
    annotalph = ANNOTALPH   # label background
    highleg   = HIGHLEG     # legend shown as active (high intensity)
    lowleg    = LOWLEG      # legend shown as inactive (low intensity)
    # line widths
    linew     = LINEW       # thin
    highlinew = HIGHLINEW   # fat
    # legend layout
    legncol   = LEGNCOL     # number of columns in legend
    # groupid's for interaction etc.
    ugid = NEGCTL #UNSPECIFIC
    sgid = POSCTL #SPECIFIC
    mgid = MUTANT
    rgid = REFERENCE
    ngid = UNSEL
    dgid = DISCARD
    maingids = [POSCTL, NEGCTL, REFERENCE, MUTANT]
    # sidepane-off-at-start groups (to begin simple)
    offpatches = [mgid, dgid, rgid]
    # multiple spaces used for separation gid and no clones
    sepr = '  ('
    # create a map between labels/gids and lists of experiments/lines
    plotmap   = [(poslabs, sc, sgid)]
    gid2lines = {  sgid:poslabs,}
    # create legend patches
    # matplotlib.org/`matplotlib.__version__`/tutorials/intermediate/legend_guide.html
    sc_patch = Patch(color= sc, label=f"{sgid}{sepr}{len(poslabs)})")
    # only add legend patches for plotted lines
    lpatches = [sc_patch,]

    def getlabels(category):
        labs = {
            SPECIFIC: poslabs + mutlabs + dislabs,
            UNSPECIFIC: neglabs,
            ALL: neglabs + poslabs + mutlabs + dislabs,
            }[category]
        return labs


    if neglabs:
        plotmap.append( (neglabs, uc, ugid) )
        gid2lines[ugid] = neglabs
        uc_patch = Patch(color= uc, label=f"{ugid}{sepr}{len(neglabs)})")
        lpatches.append(uc_patch)


    # associate alpha of positive and negative patches with visibility at start
    try:
        for patch in [sc_patch, uc_patch]: # lpatches:
            patch.set_alpha(highleg)
    except UnboundLocalError:
        # patch could be not associated with a value when no specific or
        # unspecific values are in datafrane after specification
        pass

    if mutlabs:
        plotmap.append( (mutlabs, mc, mgid))
        gid2lines[mgid] = mutlabs
        mc_patch = Patch(color= mc, label=f"{mgid}{sepr}{len(mutlabs)})")
        # set legend without mutant traces on
        mc_patch.set_alpha(lowleg)
        lpatches.append(mc_patch)

    # add discards if needed
    if dislabs:
        plotmap.append((dislabs, dc, dgid))
        gid2lines[dgid] = dislabs
        logging.debug(f"{__name__}.{thisfunc()}: Discards: {', '.join(dislabs)}")
        dc_patch = Patch(color= dc, label=f"{dgid}{sepr}{len(dislabs)})")
        lpatches.append(dc_patch)
        # set legend to begin without visible discards:
        dc_patch.set_alpha(lowleg)

    # add a reference legend if there is a reference
    if refs_:
        reflabs = get_reference(dfs[1])
        plotmap.append((reflabs, rc, rgid))
        gid2lines[rgid] = reflabs
        rc_patch = Patch(color= rc, label=f"{rgid}{sepr}{len(reflabs)})")
        lpatches.append(rc_patch)
        # set legend to begin without visible refs:
        rc_patch.set_alpha(lowleg)
    # add unselected reads from non-negative samples if available
    if unsel_:
        uselabs = getlabels(unsel_)
        unslabs = [f"u_{x}" for x in uselabs if f"u_{x}" in dfs[0].columns]
        plotmap.append((unslabs, nc, ngid))
        gid2lines[ngid] = unslabs
        nc_patch = Patch(color= nc, label=f"{ngid}{sepr}{len(unslabs)})")
        lpatches.append(nc_patch)
        # begin without visible refs:
        nc_patch.set_alpha(lowleg)

    # set up interactivity for the legend (part 2 is after creating plot/legend)
    handlermap = { patch: HandlerPatch() for patch in lpatches }

    # Side panel with number of legend panes derived from sidepatcheslist;
    class SidePane():
        def __init__(self):
            self.height              = figheight
            self.sidenos, self.slegs = self.create_legends()
            self.sides               = self.build_pane()
            self.allslegs            = self.add_legends()

        def create_legends(self):
            """Make separate legends from tuples in sidepatcheslist"""
            slegs = {}
            sidenos = []
            for label, groupdict in sidepatcheslist(dfs[0]):
                sidenos.append(len(groupdict))
                sidepatches = []
                cols = {NEGCTL: uc, MUTANT: mc, DISCARD: dc} #{UNSPECIFIC: uc, MUTANT: mc,}
                sidcol = cols[label] if label in cols.keys() else methc
                sidepatches.extend( [Patch(color=sidcol, label=sideitem)
                     for sideitem in groupdict.keys()]
                    )
                gid2lines.update( {sideitem: groupdict[sideitem]
                    for sideitem in groupdict}
                    )
                for patch in sidepatches:
                    #print(label)
                    if label in offpatches:
                        patch.set_alpha(lowleg)
                    else:
                        patch.set_alpha(highleg) # determines all 'on' at start
                sidehandlermap = {sidepatch: HandlerPatch()
                    for sidepatch in sidepatches}
                slegs[label] = (sidehandlermap, sidepatches)
            return sidenos, slegs

        def build_pane(self):
            height = self.height
            sidenos = self.sidenos # e.g [5, 3, 1, 3, 12]
            # space needed: number of groups plus a title and separation
            # plus the number of their items.
            total = 3*len(sidenos) + sum(sidenos)
            # check space for title
            titleroom = height - total
            if titleroom < 0:
                msg = ("Too many items to fit the sidepane. If possible change "
                    f" uniform value for a category to '' in '{EXPFILE}' "
                    "to gain space.")
                raise SystemExit(msg)
            sides = {}
            sidedis = []
            start = titleroom + 1
            # figure out distribution; fill from top
            for grpidx, grplen in enumerate(sidenos):
                # 0 5
                # 1 3
                # 2 1
                # 3 3
                # 4 12
                #print(grpidx, grplen)
                use = 1 + grplen
                sidedis.append( (grpidx, start, start + use) )
                start += (use + 2)
            #print(sidenos, sidedis)

            for side in sidedis: #reversed(sidedis):
                sideax = fig.add_subplot(gs[ side[1]:side[2], sidespace])
                sideax.axis('off')
                sideax.set_facecolor(figcol)
                sides[side[0]] = sideax

            return sides

        def add_legends(self):
            sides = self.sides
            sideno = 0
            allslegs = {}
            for label, patchgroup in self.slegs.items():
                sidehandlermap = patchgroup[0]
                sidepatches = patchgroup[1]
                sleg = sides[sideno].legend(
                    handler_map=sidehandlermap,
                    handles=sidepatches,
                    ncol=legncol, # alignment="left", #see below
                    title=label, title_fontsize='small',# 'small',
                    fontsize='small', # 'small' too big to fit grid cell,
                    # blend into the background
                    facecolor=figcol, frameon=False,
                    loc='upper left',
                    )
                # get title to the left-margin from default center
                # https://github.com/matplotlib/matplotlib/pull/23140
                # in matplotlib-3.6.0 can use sleg.set_alignment("left")
                ##sleg._legend_box.align = "left"
                sleg.set_alignment("left")
                # activate interactivity for the handles in the created legend:
                for slegpatch in sleg.legend_handles: #legendHandles:
                    slegpatch.set_picker(True)
                allslegs[label] = sleg
                sideno += 1
            return allslegs

        def get_legend(self):
            return self.allslegs



    # Build figure
    # ------------
    if guiplt:
        fig = plt.figure(figsize=(printwidth, printheight))
    else:
        fig = Figure(figsize=(printwidth, printheight)) # for web-display
    # remove unhelpful tools from toolbar
    edit_toolbar(fig)
    # set up a grid of panels to draw in with no space between axes
    # matplotlib manual gridspec
    # scipy-lectures.org/intro/matplotlib/auto_examples/plot_gridspec.html
    #figwidth  # defined at top
    #figheight # defined at top
    gs = fig.add_gridspec(figheight,figwidth, wspace=0.0, hspace=0.0)
    # Side panel for extra legends
    sidespace = -1 if showside else None

    # Main panel grid
    # +++++++++++++++
    # sharey gives problem on resizing with inverted y-axis of bottom panel
    top  = fig.add_subplot(gs[ 0:19, :sidespace])
    # add bot before track-panels, or set_zorder, to allow annotations for
    # track-axes to be placed above it and visible
    bot  = fig.add_subplot(gs[22:42, :sidespace], sharex = top) #, sharey = top)
    wat  = fig.add_subplot(gs[19:20, :sidespace], sharex = top) # Watson-strand
    cri  = fig.add_subplot(gs[21:22, :sidespace], sharex = top) # Crick-strand
    # add middle track last to get its annotations on top
    # fra for Franklin, Gosling, Wilkins
    fra  = fig.add_subplot(gs[20:21, :sidespace], sharex = top)
    # change 'Figure 1' to a proper title for the window frame
    if guiplt:
        fig.canvas.manager.set_window_title(windowtitle)

    # Axis-labels main panel
    # ++++++++++++++++++++++
    fig.supylabel(figylabel, rotation='vertical',
        fontsize='medium', picker=True, bbox=dict(ec=figcol, fc=figcol) )
    bot.set_xlabel(figxlabel, fontsize='medium', picker=True,
        bbox=dict(ec=figcol, fc=figcol))
    bot.xaxis.set_label_coords(0.45, -0.2)
    # give some info about graph
    axtop = top.set_title(axtitle, loc='left', fontsize='small', picker=True,
        bbox=dict(ec=figcol, fc=figcol), zorder=0)
    # make the legend later
    leg = None
    #
    # Settings frame edges, ticks and labels
    # ++++++++++++++++++++++++++++++++++++++
    for ax in [top, bot ]:
        ax.spines.left.set_color(axcol)
        ax.spines.top.set_color(axcol2)
        ax.spines.right.set_color(axcol2)
        ax.spines.bottom.set_color(axcol2)
        ax.tick_params(labelsize='small')
        ax.tick_params(axis='y', grid_color=axcol2, grid_alpha=alph)
        # right y-axis becomes sensitive as well, see:
        # https://github.com/matplotlib/matplotlib/issues/18879
        ax.yaxis.set_picker(True)
        if scale_ == 'log2':
            ax.set_yscale('log', base=2)
        else:
            ax.set_yscale('linear')
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    #bot.spines.bottom.set_color(axcol)
    # Allow turning off x-grid lines
    gc = backgr if not XGRID else axcol2
    top.tick_params(axis='x', grid_color=gc)
    bot.tick_params(axis='x', colors=axcol, grid_color=gc)
    bot.xaxis.set_picker(True)
    # Change exponential format to comma separated float (f) without digits.
    bot.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    # Reference tracks
    for ax in [wat, fra, cri]:
        ax.set_yticks([])   # no ticks, labels etc on this y axis
        ax.xaxis.set_visible(False)
        ax.spines.top.set_color(axcol2)
        ax.spines.left.set_color(figcol)
        ax.spines.right.set_color(figcol)
        ax.spines.bottom.set_color(axcol2)
        ax.set_facecolor(backgr)

    # Make figure
    # -----------
    def do_plot(zeroy,limy):
        nonlocal leg
        kwargsall = { 'legend':None, 'picker':True, 'alpha':alph, 'lw':linew,
            'xlim':ridx,}
        kwargstop = {'ax':top, 'ylim':[zeroy,limy], **kwargsall }
        # set minus axis to negative values for plotting
        # revert the y-axis for easier comparison # doesn't work with sharey
        kwargsbot = {'ax':bot, 'ylim':[limy,zeroy], **kwargsall }
        try:
            # plot subsections of each dataframe according to their grouping
            # (gid/label)
            for grp, col, grpnam in plotmap:
                dfs[0][grp].plot(color = col, gid=grpnam, **kwargstop)
                dfs[1][grp].plot(color = col, gid=grpnam, **kwargsbot)
        except TypeError:
            #"no numeric data to plot"
            raise SystemExit("Cannot create graph; no count data to plot.\n")

    # Make legend
    # +++++++++++
    # set legend to fig (not plt or ax) to keep it draggable throughout
    # and outwith plot def to keep 1 legend throughout ax-changes etc.
    leg = fig.legend(handler_map=handlermap, handles=lpatches,
        fontsize=('small'), ncol=legncol, #len(lpatches), shadow=False,
        loc='lower right', edgecolor=axcol2, facecolor=backgr,#figcol,
        bbox_to_anchor=legpos, borderpad=0.5)
    leg.set_draggable(True)
    # activate interactivity for the handles in the created legend:
    for legpatch in leg.legend_handles: # since 3.9 was legendHandles:
        legpatch.set_picker(True)
    # show side panel
    if showside:
        spane = SidePane()
        allslegs = spane.get_legend()

    # Make reference tracks (wat/fra/cri)
    # +++++++++++++++++++++++++++++++++++
    class Brbar():
        """Class to create broken-bar diagrams from figure parameters."""
        def __init__(self, ax, track, ymin, yheight, col, alph=highalph,
            bg=figcol):
            self.track = track
            self.ax = ax
            self.alph = alph
            #error when no GTFs available
            #ax.broken_barh # this function not deprecated in 3.7
            try:
                self.ax.set_ylim(0, 44)
                self.barh = ax.broken_barh(
                    self.track.get_segments(self.track.df),
                    yrange=(ymin, yheight),
                    picker=True,
                    facecolors=col,
                    alpha=self.alph)
            except TypeError:
                self.barh = None
            self.ax.set_facecolor(bg)

        def messages(self, clickpoint):
            return self.track.get_ctext(clickpoint)

    # y-start positions (relative to containing axis)
    ybot = 2
    ymid = 18
    # displayed bar-thickness
    barr = 24
    marg = 14
    # order of listing determines which track is 'on top' (the last one)
    segm = Brbar(fra, track=SegmentTrack(chrnam), col=methc, alph=annotalph,
        ymin=0, yheight=44)#, bg=backgr)
    swat = Brbar(wat, track=GTFtrack(chrnam, SPECIFIC, PLUS),
        ymin=ybot, yheight=barr+marg, col=mc)
    rwat = Brbar(wat, track=GTFtrack(chrnam, REFERENCE, PLUS),
        ymin=ymid, yheight=barr, col=rc)
    uwat = Brbar(wat, track=GTFtrack(chrnam, UNSPECIFIC, PLUS),
        ymin=ybot, yheight=barr, col=uc)
    scri = Brbar(cri, track=GTFtrack(chrnam, SPECIFIC, MINUS),
        ymin=ymid-marg, yheight=barr+marg, col=mc)
    rcri = Brbar(cri, track=GTFtrack(chrnam, REFERENCE, MINUS),
        ymin=ybot, yheight=barr, col=rc)
    ucri = Brbar(cri, track=GTFtrack(chrnam, UNSPECIFIC, MINUS),
        ymin=ymid, yheight=barr, col=uc)

    trackbarhs = {swat:swat.barh, scri:scri.barh, uwat:uwat.barh,
        ucri:ucri.barh, segm:segm.barh, rwat:rwat.barh, rcri:rcri.barh, }

    #Axis.set_label_coords(fra.yaxis, -0.04,-0.1)
    #fra.set_ylabel
    fig.text(0.075, 0.49, tracklabel, rotation=0, picker=True,
        bbox=dict(ec=figcol, fc=figcol))#, loc='bottom')

    # Interactivity
    # -------------
    #pick = True #on by default

    # Annotations
    # +++++++++++
    def annotaxis(ax, x, y):
        """Common annotate settings to be set per axis/panel."""
        annot = ax.annotate(
            "", xy = (0,0), xytext = (x,y),  # text above arrow if y up
            textcoords = "offset points",
            bbox = dict(boxstyle="round4",  ec=annotedg, fc=annotcol),
            arrowprops = dict(arrowstyle="->", color=annarrow),
            antialiased=True,
        )
        return annot

    def doannot(annotation, clickpoint, labels):
        """Common action for annotations."""
        if labels == '':
            return
        annotation.xy = clickpoint
        annotation.set_text(labels)
        annotation.get_bbox_patch().set_alpha(annotalph)
        annotation.set_visible(True)

    annottop = annotaxis(top, x=20, y=25)
    annottop.set_visible(False)

    annotbot = annotaxis(bot, x=-30, y=-25)
    annotbot.set_visible(False)
    #store annotations for when toggling axes or lines
    annotedexps = set()
    #label falls outside axes and remains hidden; up, no problem
    annotfra = annotaxis(fra, x=20, y=0)
    annotfra.set_visible(False)

    annotwat = annotaxis(wat, x=20, y=20)
    annotwat.set_visible(False)

    annotcri = annotaxis(cri, x=20, y=-30)
    annotcri.set_visible(False)
    # retrieve annotation setting with track/axis
    annottracks = {wat:annotwat, fra:annotfra, cri:annotcri}

    def linnam(line):
        """Return sample name associated with clicked trace/line"""
        #striplabel = str(line).strip('Line2D(').strip(')')
        return line._label #striplabel

    # to highlight the corresponding opposite strand for the same sample:
    def samelines(line):
        """Return lines in either panel associated with same sample."""
        picked = linnam(line)
        samelines = set()
        for ax in [top,bot]:
            for pick in ax.get_lines():
                if linnam(pick) == picked:
                    samelines.add(pick)
        return samelines

    class GTFAnnotator():
        """Control annotations for a pick event registered by multiple artists,
        each representing another GTF"""
        ctexts = []
        clickpoint = (0,0)
        annots = None

        def __init__(self):
            pass

        @classmethod
        def add_pevent(cls, pevent, barh):
            ctrack = pevent.artist.axes
            cx, cy = pevent.mouseevent.xdata, pevent.mouseevent.ydata
            if (cx, cy) != cls.clickpoint: # new point clicked, start over
                cls.clear()
                cls.clickpoint = (cx, cy)
            annots = annottracks[ctrack]
            if cls.annots != annots:
                cls.annots = annots
            ctext = barh.messages(cx)
            if ctext:
                cls.ctexts.append(ctext)
            #time.sleep(0.05)
            cls.doannots()

        @classmethod
        def doannots(cls):
            ctext = '\n'.join(list(set(cls.ctexts))) # no repeats
            doannot(cls.annots, cls.clickpoint, ctext)

        @classmethod
        def clear(cls):
            cls.ctexts = []
            cls.clickpoints = []
            cls.axes = []

    def update_annot_track(pevent):
        """Show gtf or sement info if available, otherwise click point."""
        if not pevent.mouseevent.inaxes:
            return
        if pevent.artist in trackbarhs.values():
            logging.debug("Picked PolyCollection (former BarHContainer)")
            barh = [trackbarh for trackbarh, barh in trackbarhs.items()
                if barh == pevent.artist][0]
            GTFAnnotator.add_pevent(pevent, barh)

    def reset_annot_track():
        """Remove visible annotations from gtf and segment tracks."""
        for visannot in annottracks.values():
            visannot.set_visible(False)

    def update_annot(expnams, linepoint,ax):
        """Trace annotations in upper and lower main panels."""
        logging.debug(f"\tannotation at {linepoint}")
        if len(sorted(expnams)) > 4:   # should no longer happen
            labels = ", ".join(sorted(expnams)[:4]) + ".."
        else:
            labels = ", ".join(sorted(expnams)) # should only be one
        if ax == top:
            annotbot.set_visible(False)
            doannot(annottop,linepoint,labels)
        elif ax == bot:
            annottop.set_visible(False)
            doannot(annotbot,linepoint,labels)

    # Toggle actions
    # ++++++++++++++
    def toggle_lineset(lineset, vison):
        """Make group of traces visible or turn them off."""
        # using gid would keep this only usable for the main groups of lines
        # vison to keep annotations and lines in sync
        '''if unsel_ and lineset != unslabs:
            seeklist = [f"u_{x}" for x in lineset]
            lineset += seeklist'''
        for ax in [bot,top]:
            for line in ax.get_lines():
                if linnam(line) in lineset:
                    line.set_visible(vison)

        for linename in lineset:
            if linename == annottop._text:
                annottop.set_visible(vison)
            if linename == annotbot._text:
                annotbot.set_visible(vison)

    def retrieve_active_sidepatches(group, vison=True):
        """Find patches that are 'on'."""
        alph = highleg if vison else lowleg
        toggled=[]
        if allslegs.get(group) is None: return toggled

        for spatch in allslegs.get(group).get_patches():
            if spatch.get_alpha() == alph:
                labl = spatch.get_label() #.split(" ")[0]
                toggled.extend(gid2lines[labl])
        return toggled

    def toggledoffcondition():
        """Find Condition patches that are 'off'."""
        return retrieve_active_sidepatches(group=CONDITION, vison=False)

    def toggledoffmutant():
        """Find Mutant patches that are 'off'."""
        return retrieve_active_sidepatches(group=MUTANT, vison=False)

    def toggledoffmethod():
        """Find Method patches that are 'off'."""
        return retrieve_active_sidepatches(group=METHOD, vison=False)

    def toggledofffraction():
        """Find Fraction patches that are 'off'."""
        return retrieve_active_sidepatches(group=FRACTION, vison=False)

    def toggledoffunspec():
        """Find Unspecific patches that are 'off'."""
        return retrieve_active_sidepatches(group=NEGCTL, vison=False)

    def toggle_patch(patch):
        """Use patch to control and reflect visibility of traces."""
        # get the gid part of the label (`sepr` defined above)
        pgid = patch.get_label().rsplit(sepr,1)[0].strip()
        # use current setting of patch button to determine wished, opposite
        # visibility of controlled traces and the button
        palph = patch.get_alpha()
        alphon = lowleg if palph == highleg else highleg
        vison = False if palph == highleg else True
        onoff=  'on' if vison else 'off'
        msg = f"Toggled Patch '{pgid}' {onoff}"
        logging.debug(msg)
        # get the traces controlled by the patch
        toggle = gid2lines[pgid]
        # provides patches (spatch) that can overlap in controlled traces
        if showside:
            # set patches alpha
            for spatch in [pgid]: #[*pgid_,*pgid_2]:
                if allslegs.get(spatch) is None: continue
                for spatch in allslegs.get(spatch).get_patches():
                    spatch.set_alpha(alphon)
            # bypass overlapping sidepatch effects
            if vison:
                # a (side) patch is clicked to show controlled traces;
                #   but get only those that fit other selections
                # a 'method' or 'fraction' patch defined by pgid contains
                #   SPECIFIC traces; a 'mutant' patch won't
                # a 'condition' patch can contain both muts or meth or fract;
                #   should act on existing open method/fraction/mutants not
                #   open other traces beyond those.
                offcond = set(toggledoffcondition())
                offmeth = set(toggledoffmethod())
                offfrac = set(toggledofffraction())
                offmut  = set(toggledoffmutant())
                offunsp = set(toggledoffunspec())
                pickedmethod = set(toggle).difference(
                    offcond.union(offmut, offunsp, offfrac) )
                pickedfraction = set(toggle).difference(
                    offcond.union(offmut, offunsp, offmeth) )
                pickedcondition = set(toggle).difference(
                    offmut.union(offmeth, offfrac, offunsp) )
                pickedmutant = set(toggle).difference(
                    offmeth.union(offcond, offfrac, offunsp) )
                pickedsomespec = set(toggle).difference(
                    offmeth.union(offmut, offcond, offfrac) )
                keeplist = sorted(list( pickedmutant.union(pickedmethod,
                    pickedfraction, pickedcondition, pickedsomespec) ))
                toggle_lineset(keeplist, vison)
            else:
                # turn all off is fine;
                toggle_lineset(toggle, vison)
        elif pgid in maingids:
            toggle_lineset(toggle, vison)
        #set patch alpha last as this is used to determine toggle state
        patch.set_alpha(alphon)

    def reset_toggled_ons():
        """Remove annotations and changes in line-thickness/alpha."""
        annotedexps.clear();
        for annot in [annottop,annotbot]:
            annot._text=''
            annot.set_visible(False)
        for ax in [top,bot]:
            for line in ax.get_lines():
                line.set_alpha(alph)
                line.set_lw(linew)

    # turn legend off via yaxis label
    # reset_toggled lines via xaxis label
    def toggle_from_text(textobject):
        """Reset changes via axis labels."""
        logging.debug(f"Picked {textobject}")
        text = textobject.get_text()
        if text == axtitle:
            vis = not leg.get_visible()
            leg.set_visible(vis)
        elif text == figylabel:
            axv = not axtop.get_visible()
            axtop.set_visible(axv)
        elif text == figxlabel:
            reset_toggled_ons()
        elif text == tracklabel:
            reset_annot_track()
        else:
            logging.debug(f"no show for {text}")

    def toggle_yaxis(axis):
        """Toggle scale of y-axis between log2 and linear."""
        if not isinstance(axis,YAxis):# and axis.spines.left:
            return
        logging.debug(f"Picked {axis}")
        curscale = axis.get_scale()
        unvisiblelist = set()
        # we need a list of all lines not the grouped set
        restorelist=set()
        # scan state of lines in each panel and remove them; change the yaxis
        for ax in [top, bot]:
            for line in ax.get_lines(): # works; do not use ax.lines
                # create a memory snapshot
                if line.get_alpha() == highalph:
                    #assert line.get_lw() == highlinew
                    restorelist.add(linnam(line)) # will also have thick line
                if not line.get_visible():
                    unvisiblelist.add(linnam(line))
                line.remove()
            # change the yaxis
            if curscale == 'linear':
                zero, limy = logzero, loglim
                ax.set_yscale('log', base=2)
            elif curscale == 'log':
                zero, limy = 0, linlim
                ax.set_yscale('linear')
                ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(
                    '{x:,.0f}'))
        # plot the data lines to the new scale
        do_plot(zero,limy)
        # restore previous state of each line
        for ax in [top, bot]:
            for line in ax.get_lines():
                if linnam(line) in unvisiblelist:
                    line.set_visible(False)
                if linnam(line) in restorelist:
                    line.set_alpha(highalph)
                    line.set_lw(highlinew)
        fig.canvas.draw_idle()

    def copy_xaxis_region(axis):
        if not isinstance(axis,XAxis):
            return
        lims = bot.get_xlim()
        x0 = int(lims[0] )#/ 1000) * 1000
        x1 = int(lims[1] )#/ 1000) * 1000
        msg = (f"{chrnam}:{x0 if x0 > 0 else 1}-{x1}")
        logging.debug(f"Selected region: {msg}")
        print(msg)

    # Event processing
    # ++++++++++++++++
    def onpick2D(pevent):
        """Process picking a trace."""
        thisline = pevent.artist
        if not thisline.get_visible():
            return
        logging.debug(f"Picked {thisline}")
        #expnam = mpl.artist.getp(thisline,"label")
        expnam = linnam(thisline)
        ind = pevent.ind
        xdata, ydata = thisline.get_xdata(), thisline.get_ydata()
        points = tuple(zip(xdata[ind], ydata[ind]))
        alphon = highalph if thisline.get_alpha() == alph else alph
        lineon = highlinew if thisline.get_lw() == linew else linew
        if thisline.get_alpha() == alph:
            # ensure that only one line will ever be picked
            reset_toggled_ons()
            annotedexps.add(expnam)
            update_annot(annotedexps,points[0],thisline.axes)
        else: #toggle off
            reset_toggled_ons()
        for line in samelines(thisline):
            line.set_alpha(alphon)
            line.set_lw(lineon)
        logging.debug(f'\talpha {thisline.get_alpha()}, '
                      f'linewith {thisline.get_lw()}')

    # matplotlib.org/`matplotlib.__version__`/users/event_handling.html
    def onpick(pevent): # PickEvent
        #print(pevent.artist) # for debugging interaction
        # for debugging right YAxis interaction
        #print(pevent.mouseevent)
        #print(pevent.artist.axes.get_tightbbox().bounds)
        """Process pick events."""
        if isinstance(pevent.artist, Patch):
            toggle_patch(pevent.artist)
        elif isinstance(pevent.artist, YAxis) and (pevent.mouseevent.x <
            pevent.artist.axes.get_tightbbox().bounds[2]):
            toggle_yaxis(pevent.artist)
        elif isinstance(pevent.artist, XAxis):
            copy_xaxis_region(pevent.artist)
        elif isinstance(pevent.artist, PolyCollection):
            # since matplotlib-3.7 no longer BrokenBarHCollection
            update_annot_track(pevent)
        #elif isinstance(pevent.artist, BrokenBarHCollection):
        #    # before matplotlib-3.7: BrokenBarHCollection:
        #    # https://matplotlib.org/examples/user_interfaces/wxcursor_demo.html
        #    update_annot_track(pevent)
        elif isinstance(pevent.artist, Text):
            toggle_from_text(pevent.artist)
        elif pevent.mouseevent.inaxes in [top, bot] and isinstance(
            pevent.artist, Line2D):
                onpick2D(pevent) # for coordinates not in pevent.artist
        fig.canvas.draw_idle()

    # Plotting
    # ---------
    do_plot(zero, lim)
    # begin simple, without Mutant and RNAseq peaks; and without marginal stuff
    if mutlabs:
        toggle_lineset(mutlabs, False)
    if dislabs:
        toggle_lineset(dislabs, False)
    if refs_:
        toggle_lineset(reflabs, False)
    if unsel_:
        toggle_lineset(unslabs, False)

    # Show or save
    # ------------
    region = '' if not fregion else f"_{fregion}"
    titlenam = remove_odds(f"{title}{setname}_chr{chrnam}{region}_{doneon()}")
    fdirs = {SVG: FIGDIRSVG, PNG: FIGDIRPNG, PDF: FIGDIRPDF, JPG: FIGDIRJPG,}
    if dowhat =='show':
        mplstyle.use('fast')
        fig.canvas.mpl_connect('pick_event', onpick)
        plt.show()
    elif dowhat == 'return':
        return fig
    else:
        titlefig = (f"{titlenam}{dowhat}")
        fpath = fdirs[dowhat].joinpath(CHROMFIG,titlefig)
        print(f"Saving {titlefig}")
        if dowhat in [SVG, PDF, JPG]:
            plt.savefig(fpath, transparent=False)
        else:
            plt.savefig(fpath, transparent=False, dpi=DPI)
    plt.close()
