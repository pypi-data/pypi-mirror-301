#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  panel_plotters.py
#
#
#  Copyright 2022-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module for organizing panes, based on samples and grouping, and plotting."""
import logging
import matplotlib.pyplot as plt
import seaborn as sns

from coalispr.resources.constant import (
    CONDITION, CONDITIONS, CPPHFAC,
    FRACTION, FRACTIONS,
    LIBCNTS, LENCNTS, LPPHFAC,
    MAXROW, METHOD, METHODS,
    REGCNTS, REST,
    THISALPH,
    )
from coalispr.resources.plot_utilities import (
    capit_label,
    edit_toolbar,
    less_xlabels,
    save_output_as,
    set_axes,
    )
from coalispr.resources.utilities import (
    get_string_info,
    remove_odds,
    thisfunc,
    )

logger = logging.getLogger(__name__)

class PanelPlotter():
    """Create paneled figure to display grouped graphs (described by ``fcie``).

    Attributes
    ----------
    group : str
        Name of group of categories; data for each category is shown in a
        separate panel.
    nams : list
        List of group names in each group.
    lens : dict
        Dict of group name vs number of samples in each group.
    sampls : dict
        Dict for group name vs members of group.
    df : Pandas.DataFrame
        Dataframe with data to display.
    numbers : list
        List of column headers to use.
    titels : dict
        Dictionary of figure titles: {'legtitl': '','suptitl':'', 'wintitl':''}.
    dolegend : bool
        Flag to show legend.
    hfac   : float
        Height factor, determining vertical space for individual sample-lanes
    gap : int
        Space in gridspec lines for legend
    xlabel : str
        Label on x-axis describing what the displayed bars refer to.
    ylabel : str
        Label on y-axis describing sample data is displayed for.
    savdir : str
        Name of sub-directory to store saved figure in.
    savedirect : bool
        Flag to save figure directly to file (to prevent distortion by
        resizing or scaling)
    figure : matplotlib.pyplot.figure

    Returns
    -------
    matplotlib.pyplot.figure
        Figure to be plotted or written to file.
    """

    def __init__(self, group, nams, lens, sampls, df, numbers, titles):
        self.group = group
        self.nams = nams
        self.lens = lens
        self.sampls = sampls
        self.df = df
        self.numbers = numbers
        self.titles = titles

        self.dolegend = True
        self.format_ax = None
        self.hfac = CPPHFAC
        self.gap = 2 # between panels in the same column
        self.xlabel = capit_label(titles['xlabel'])
        self.ylabel = capit_label(titles['ylabel'])
        (
        self.remain, # panel_other
        self.maxtuple,
            ) = self._get_griddicts()
        (
        self.hghtno,
        self.wdthno,
        self.idx,
        self.outofstack # omit
            ) = self._get_gridspec_parameters()
        self.savdir = None
        self.fig = plt.figure()

    def __repr__(self):
        return (f"{self.__class__.__name__}("
            f"df: {get_string_info(self.df)}"
            f"group: {self.group}, names: {self.nams}, lengths: {self.lens!r}, "
            f"numbers: {self.numbers}, titles: {self.titles!r}."
            )

    def __str__(self):
        return self.__repr__()

    def _vert_panels(self, fig, gs, omit=None):
        raise TypeError()

    def _build_panels(self, fig, gs):
        raise TypeError()

    def _get_griddicts(self, _3lens=None):
        lendict = self.lens if not _3lens else _3lens
        # gridspec parameters for vertical, horizontal bar display
        # get scaling with respect to maximum number of samples `maxnum`
        # get maximum number of samples out of the list of groups
        maxkey = max(lendict, key=lendict.get)
        maxnum = max(lendict.values())
        remain = lendict.copy() #need copy of dict, not reference
        del remain[maxkey]
        return remain, (maxkey, maxnum)

    def _get_gridspec_parameters(self):
        """Provide details that set up the gridspec to place panels; based
        around 2 to 4 conditions, methods, fractions or categories, 3 columns
        max.
        """

        def dolegh():
            if not self.dolegend:
                return 0
            else: #create space for legend
                lines = len(self.numbers)
                lh = gap+1 if self.titles['legtitl'] else gap
                lh += int(lines/2) + 1
                return lh

        gap = self.gap
        remain = self.remain
        maxtuple = self.maxtuple
        maxnum = maxtuple[1]
        legh = dolegh()
        toplace = len(remain)
        gaps =  legh + ((toplace - 1) * self.gap)
        allremain_in_1col = sum(remain.values(), gaps)
        wdthno = 3
        hghtno = maxnum
        outofstack = None



        def get_3colpatterns():
            # create a sorted list of tuples
            lefttwo, maxremain = self._get_griddicts(remain)
            gaps = legh + (2 * gap)
            wdthno = 3
            hghtno = maxnum
            outofstack = None
            allremain_in_1col = sum(remain.values(), gaps)
            tworemain_in_1col = sum(lefttwo.values(), (gap + legh))

            if allremain_in_1col < maxnum/2:
                idx = 200 #300
                hghtno = int(maxnum/2)
            elif allremain_in_1col < maxnum and maxnum < MAXROW:
                idx = 21 #31
                wdthno = 2
            elif allremain_in_1col < maxnum and maxnum >= MAXROW:
                idx = 200 #31
                hghtno = int(allremain_in_1col)
            elif allremain_in_1col >= maxnum:
                idx = 211
                outofstack = maxremain # always in between tworemain and maxnum
                if tworemain_in_1col >= maxnum:
                    hghtno = tworemain_in_1col
            return hghtno, wdthno, idx, outofstack


        # four groups (maxtuple and toplace == 3) of samples
        if toplace == 3:
            return get_3colpatterns()
        # three groups of samples
        elif toplace == 2:
            # groups cannot be rearranged and are placed alongside each other
            if allremain_in_1col > maxnum:
                idx = 111
            # one group is much larger (e.g. 'mutant') than other two combined
            # (e.g. the controls);
            # split the large group; place others in first column
            elif allremain_in_1col < maxnum/2:
                hghtno = int(maxnum/2)
                idx = 200
            # two groups fit one column and the other group the second column
            elif allremain_in_1col < maxnum:
                wdthno = 2
                idx = 21 #stack
        # two groups of samples, each in one column
        elif toplace == 1:
            idx = 21
            hghtno += gap
            wdthno = 2
        # one major group to split (say when one method used),
        # create gap for legend
        elif toplace == 0:
            # split over three columns
            if maxnum > 35:
                hghtno = int((maxnum+gap)/3) + 1
                idx = 3
            # split over two columns
            elif 15 < maxnum < 35:
            #elif maxnum < 35:
                hghtno = int((maxnum+gap)/2) + 1
                wdthno = 2
                idx = 2
            # keep group in one column
            else:
                hghtno += gap
                wdthno = 1
                idx = 1

        return hghtno, wdthno, idx, outofstack

    def _equalize_axes(self):
        """ Adjust subfigures to one with highest counts; from
            https://stackoverflow.com/questions/42973223/how-to-share-x-axes-of-two-subplots-after-they-have-been-created/66126384#66126384
            Intially used: ``ax_list[0].get_shared_x_axes().join(*ax_list)``,
            but 'join' is deprecated since 3.6; for 3.8 and up used:
            """
        ax_list = self.fig.get_axes()
        if len(ax_list) > 1:
            for ax in ax_list[1:]:
                ax.sharex(ax_list[0])
                ax_list[-1].autoscale(axis='x')


    def _no_xmarkings(self, ax):
        #ax.xaxis.set_visible(False) # removes vertical grid lines
        ax.set_xlabel('', labelpad=0, size='xx-small')
        ax.tick_params(axis='x', labelbottom=False, bottom=False)
        #ax.set_xticks([]) # affects grid appearance
        return ax

    def _titlelayout(self, gs):
        suptitle = self.titles['suptitl']
        top = 0.97
        if suptitle:
            print("Making title space")
            self.fig.suptitle(suptitle, y=0.99)
            #self.fig.subplots_adjust(top=0.93)
            top=0.90

        gs.update(top=top)

    def _do_legend(self, ax):
        legtitl = self.titles['legtitl']
        if self.dolegend:
            handles, labels = ax.get_legend_handles_labels()
            leg = self.fig.legend(
                handles, labels, loc='lower left' ,
                fontsize='small',
                ncol=2, title=legtitl,
                title_fontsize='small')
            leg.set_bbox_to_anchor((0.07, 0.04))
            leg.set_draggable(True)

    def _panetitle(self, key, number):
        if key == REST.upper():
            pantitl = key
        else:
            if self.group == METHOD:
                pantitl =  METHODS[key]
            elif self.group == FRACTION:
                pantitl =  FRACTIONS[key]
            elif self.group == CONDITION:
                pantitl =  CONDITIONS[key]
            else:
                pantitl = key
        return (f"{pantitl} (n = {number})")

    def _rotate_ylabel(self):
        if self.ylabel !='':
            self.fig.supylabel(self.ylabel, y=0.6, rotation='vertical',
                fontsize='medium')

    def plot_panels(self):
        logging.debug(f"{__name__}.{thisfunc()}\n: {self.__repr__()}")
        print("Building figure...")
        hghtno = self.hghtno
        wdthno = self.wdthno
        idx = self.idx
        hfac = self.hfac
        titles = self.titles
        fig = self.fig
        #print(idx, hghtno)
        figh = int(hghtno * hfac)
        figh += 6*hfac if figh < 5 else figh
        figw = wdthno * 4
        figw = wdthno * 6 if figw < 6 else figw
        fig = self.fig
        gs = self.fig.add_gridspec(hghtno, wdthno, wspace=0.4, hspace=0)
        msg = f"Column layout (``idx``) is {idx}"
        logging.debug(f"{__name__}.{thisfunc(1)}:\n{msg}")
        self._build_panels(gs)
        # Make all x/y-axes the same afterwards (i.e. as if sharex or sharey = True)
        self._equalize_axes()
        # keep only save button
        edit_toolbar(fig, True)
        self._rotate_ylabel()
        wtitl = remove_odds(titles['wintitl'])
        fig.canvas.manager.set_window_title(wtitl)
        hinch = figh if figh > 3 else 3
        fig.set_size_inches(figw, hinch)
        #print(figh, hinch)
        self._titlelayout(gs)
        try:
            save_output_as(wtitl, self.savdir)
        except FileNotFoundError:
            msg = f"Cannot save file; is {self.savdir} available?"
            print(msg)
        print("\nFigure finishing.")
        plt.show()
        plt.close()


class CountPanelPlotter(PanelPlotter):
    """Create paneled figure to display grouped library count graphs."""
    def __init__(self, group, nams, lens, sampls, df, numbers, titles): #, dolegend):
        super().__init__(group, nams, lens, sampls, df, numbers, titles)
        self.fcie = self._barh_plot
        self.log2_ax = None
        #self.dolegend = dolegend
        self.savdir = LIBCNTS

    def _barh_plot(self, samples, ax, titl):
        """Create barh-graph to fit paneled figure.

        Parameters
        ----------
        samples : list
            List of samples as members of chosen group.
        titls : str
            Graph title.
        ax : matplotlib.axes.Axes
            Axes object that needs the bardiagram drawn into.

        Returns
        -------
        matplotlib.axes.Axes
            Graphing instructions on ``ax``
        """
        xlabel = self.xlabel
        numbers = self.numbers
        df = self.df
        format_ax = self.format_ax
        log2_ax = self.log2_ax
        #sampleidxs = [ x for x in df.index if x in samples]
        df.loc[samples][numbers].plot(
            ax=ax,
            kind='barh',
            stacked=True,
            alpha=THISALPH,
            legend=None,
            )
        set_axes(ax, format_ax, log2_ax)
        # turn off 'Sample' label on y-axis
        ax.set_ylabel('')
        # reverse the display order to read from top to bottom
        ax.invert_yaxis()
        ax.tick_params(axis='y',labelsize='x-small')
        ax.set_xlabel(xlabel, fontsize='small')
        ax.set_title(titl, loc='left', fontsize='small')
        return ax

    def _vert_panels(self, gs, omit=None):
        gap = self.gap
        sampls = self.sampls
        lens = self.lens
        panel_other = self.remain
        fig = self.fig

        vpanels = list(panel_other.keys())
        if omit != None:
            vpanels.remove(omit[0])
        #print(vpanels, omit)
        j = 0 # follows grid-cells
        for key in vpanels:
            sm = sampls[key] # samples
            sl = lens[key]   # no of samples
            titl =  self._panetitle(key, sl)
            # section specific for class
            ax = fig.add_subplot(gs[j:j+sl, 0])
            ax = self.fcie(sm, ax, titl)

            if key != vpanels[-1]:
                self._no_xmarkings(ax)
            # prepare for next panel (no need for fake invisible panel)
            j += sl+gap

    def _build_panels(self, gs):
        """Divide gridspec ``gs`` given general layout (idx)"""
        idx = self.idx
        nams = self.nams
        sampls = self.sampls
        lens = self.lens
        maxtuple = self.maxtuple
        hghtno = self.hghtno
        outofstack = self.outofstack
        fig = self.fig

        def do111():
            # three columns with one panel
            i = 0
            for key in nams: #panel_other.keys():
                sm = sampls[key] # samples
                sl = lens[key] # no of samples
                titl =  self._panetitle(key, sl)
                ax = fig.add_subplot(gs[0:sl, i])        #
                # no need/error to create fake panel     #
                ax = self.fcie(sm, ax, titl)
                # prepare for next panel
                i += 1                                   #
            self._do_legend(ax)

        def doN00():
            # 1st column of 3 with multiple panels
            self._vert_panels(gs)
            # split max col
            key = maxtuple[0]
            sm1 = sampls[key][:hghtno] # samples
            sm2 = sampls[key][hghtno:]
            sl = lens[key] # orig no of samples
            titl =  self._panetitle(key, sl)
            ax1 = fig.add_subplot(gs[0:hghtno, 1])       #
            ax1 = self.fcie(sm1, ax1, titl)              #
            # next panel with second half of samples
            ax2 = fig.add_subplot(gs[0:sl-hghtno, 2])    #
            ax2 = self.fcie(sm2, ax2, "")                #
            self._do_legend(ax2)

        def doN1():
            # first column of 2 with multiple panels
            self._vert_panels(gs)
            # create max col
            key = maxtuple[0]
            sm = sampls[key]
            sl = lens[key] # no of samples
            titl =  self._panetitle(key, sl)
            ax = fig.add_subplot(gs[0:sl, 1])            #
            ax = self.fcie(sm, ax, titl)                 #
            self._do_legend(ax)

        def do2N1():
            # first column of 3 with multiple panels;
            # omit largest of panel_other
            self._vert_panels(gs, outofstack)
            # create next column with largest of panel_other
            i = 0
            for key in [outofstack[0], maxtuple[0]]:
                sm = sampls[key]
                sl = lens[key] # no of samples
                titl =  self._panetitle(key, sl)
                ax = fig.add_subplot(gs[0:sl, 1+i])      #
                ax = self.fcie(sm, ax, titl)             #
                i += 1
            self._do_legend(ax)

        def doN():
            # 1 group split over 3, 2, or 1 panel(s); make space for legend
            num = maxtuple[1]
            numsdict = {
                    3 : [num-2*hghtno, hghtno, hghtno],
                    2 : [num-hghtno, hghtno],
                    1 : [abs(hghtno-num)],
                    }
            nums = numsdict[idx]
            #print(nums)
            key = maxtuple[0]
            sl = lens[key]
            titl = self._panetitle(key, sl)
            if idx == 3:
                smdict = {
                        3 : [ sampls[key][:nums[0]] ,         # sm1
                              sampls[key][nums[0]: -nums[2]], # sm2
                              sampls[key][-nums[2]: ],        # sm3
                             ],
                             }
            else:
                smdict = {
                        2 : [ sampls[key][:nums[0]],          # sm1
                              sampls[key][nums[0]: ],         # sm2
                             ],
                        1 : [ sampls[key][:] ],               # sm1
                        }

            for i in range(idx):
                titl = titl if i ==0 else ""
                ax = fig.add_subplot(gs[0:nums[i], i])   #
                smi = smdict[idx][i]                     #
                ax = self.fcie(smi, ax, titl)            #
            self._do_legend(ax)

        # dictionary linking idx to a function
        doidxs = {
            111: do111,
            200: doN00, #300: doN00,
            21:   doN1, # 31:  doN1,
            211: do2N1, #201: do2N1,
            #11:   doN1,  12:   doN1,
            1:     doN,   2:   doN,  3: doN,
            }
        # call function linked to idx in dictonary
        #print("idx", idx)
        doidxs[idx]()
        return fig


class Log2CountPanelPlotter(CountPanelPlotter):
    """Create paneled figure to display grouped library log2(count) graphs."""
    def __init__(self, group, nams, lens, sampls, df, numbers, titles): #, dolegend):
        super().__init__(group, nams, lens, sampls, df, numbers, titles)
        self.fcie = self._barh_plot
        self.log2_ax = "x"
        #self.dolegend = dolegend
        self.savdir = LIBCNTS



class LengthPanelPlotter(PanelPlotter):
    """Create paneled figure to display grouped length distribution  graphs;
    each graph needs its own ax in a 'multipane' panel (therefore very similar
    idx-functions as in ``CountPanelPlotter()._build_panels``, but with
    different handling, marked by # in margin).
    """
    def __init__(self, group, nams, lens, sampls, df, numbers, titles):
        super().__init__(group, nams, lens, sampls, df, numbers, titles)
        self.hfac = LPPHFAC
        self.fcie = self._bar_lengths
        self.dolegend = True
        self.savdir = LENCNTS
        self.format_ax = 'y'
        self.rlessx = titles['rlessx']

    def _bar_lengths(self, sample, ax):
        """Create barv-graph of lengths to fit paneled figure.

        Parameters
        ----------
        sample : str
            Sample key to display.
        numbers : list
            List of column headers to use.
        ax : matplotlib.axes.Axes
            Axes object that needs the bardiagram drawn into.

        Returns
        -------
        matplotlib.axes.Axes
            Graphing instructions on ``ax``
        """
        numbers = self.numbers
        dfs = self.df[ [sample, *numbers ] ]
        format_ax = self.format_ax
        try:
            usehue = numbers[1]
        except IndexError:
            usehue = None
        try:
            ax=sns.barplot(
                data= dfs,
                ax=ax,
                x=numbers[0],
                y=dfs[sample],
                hue=usehue,
                alpha=THISALPH,
                edgecolor="w",
                linewidth=0.1,
                )
        except ValueError as e: # no data to display
            logging.debug(f"{__name__}.{thisfunc()}:\n{e}")
            raise SystemExit("No data to display")
        if ax.get_legend():
            ax.get_legend().remove()
        ax.set_ylabel(sample, rotation=0, ha='right', fontsize='x-small')
        ax.yaxis.set_label_coords(-0.033,0.1)
        set_axes(ax, format_ax)
        ax.set_yticks([])
        return ax

    def _equalize_axes(self):
        ax_list = self.fig.get_axes()
        if len(ax_list) > 1:
            #ax_list[0].get_shared_y_axes().join(*ax_list)
            for ax in ax_list[1:]:
                ax.sharey(ax_list[0])
            ax_list[-1].autoscale(axis='y')

    def _multipane(self, i, sm, ax, titl):
        xlabel = self.xlabel
        rlessx = self.rlessx

        ax = self.fcie(sm[i], ax)
        if sm[i] == sm[0]:
            ax.set_title(titl, loc='left', fontsize='small')
        if sm[i] != sm[-1]:
            self._no_xmarkings(ax)
        if sm[i] == sm[-1]:
            ax.set_xlabel(xlabel, fontsize='small')
            ax.tick_params(axis='x',labelsize='x-small')
            less_xlabels(ax, [ax], rlessx)
        return ax

    def _vert_panels(self, gs, omit=None):
        gap = self.gap
        sampls = self.sampls
        lens = self.lens
        panel_other = self.remain
        fig = self.fig

        vpanels = list(panel_other.keys())
        if omit != None:
            vpanels.remove(omit[0])
        #print(vpanels, omit)
        j = 0 # follows grid-cells
        for key in vpanels:
            sm = sampls[key] # samples
            sl = lens[key] # no of samples
            titl = self._panetitle(key, sl)
            # class-specific section
            for k in range(sl):
                ax = fig.add_subplot(gs[j+k:j+1+k, 0])
                self._multipane(k, sm, ax, titl)
                if sm[k] == sm[-1] and key != vpanels[-1]:
                    self._no_xmarkings(ax)
            # prepare for next panel (no need for fake invisible panel)
            j += sl+gap

    def _build_panels(self, gs):
        idx = self.idx
        nams = self.nams
        sampls = self.sampls
        lens = self.lens
        maxtuple = self.maxtuple
        hghtno = self.hghtno
        outofstack = self.outofstack
        fig = self.fig

        def do111():
            # three columns with one panel
            i = 0
            for key in nams:     # panel_other.keys():
                sm = sampls[key] # samples
                sl = lens[key]   # no of samples
                titl = self._panetitle(key, sl)
                for k in range(sl):                                   #
                    ax = fig.add_subplot(gs[k:1+k, i])                #
                    ax = self._multipane(k, sm, ax, titl)             #
                # prepare for next panel
                i += 1
            self._do_legend(ax)

        def doN00():
            # first column of 3 with multiple panels
            self._vert_panels(gs)
            # split max col
            key = maxtuple[0]
            sm1 = sampls[key][:hghtno] # samples
            sm2 = sampls[key][hghtno:]
            sl = lens[key] # orig no of samples
            titl = self._panetitle(key, sl)
            for k in range(hghtno):                                   #
                ax = fig.add_subplot(gs[k:1+k, 1])                    #
                self._multipane(k, sm1, ax, titl)                     #
            # next panel with second half of samples
            for k in range(sl-hghtno):                                #
                ax = fig.add_subplot(gs[k:1+k, 2])                    #
                ax = self._multipane(k, sm2, ax, "")                  #
            self._do_legend(ax)

        def doN1():
            # first column of 2 with multiple panels
            self._vert_panels(gs)
            # create max col
            key = maxtuple[0]
            sm = sampls[key]
            sl = lens[key] # no of samples
            titl = self._panetitle(key, sl)
            for k in range(sl):                                       #
                ax = fig.add_subplot(gs[k:1+k, 1])                    #
                ax = self._multipane(k, sm, ax, titl)                 #
            self._do_legend(ax)

        def do2N1():
            # 1st column of 3 with multiple panels;
            # omit largest of panel_other
            self._vert_panels(gs, outofstack)
            # create next column with largest of panel_other
            i = 0
            for key in [outofstack[0], maxtuple[0]]:
                sm = sampls[key]
                sl = lens[key] # no of samples
                titl = self._panetitle(key, sl)
                for k in range(sl):                                   #
                    ax = fig.add_subplot(gs[k:1+k, 1+i])              #
                    ax = self._multipane(k, sm, ax, titl)             #
                i += 1
            self._do_legend(ax)

        def doN():
            # 1 group split over 3, 2, or 1 panel(s); make space for legend
            num = maxtuple[1]
            numsdict = {
                    3 : [num-2*hghtno,hghtno,hghtno],
                    2 : [num-hghtno,hghtno],
                    1 : [abs(hghtno-num)],
                    }
            nums = numsdict[idx]
            key = maxtuple[0]
            sl = lens[key] # orig no of samples
            titl = self._panetitle(key, sl)
            if idx == 3:
                smdict = {
                        3 : [ sampls[key][:nums[0]] ,         # sm1
                              sampls[key][nums[0]: -nums[2]], # sm2
                              sampls[key][-nums[2]: ],        # sm3
                             ],
                             }
            else:
                smdict = {
                        2 : [ sampls[key][:nums[0]],          # sm1
                              sampls[key][nums[0]: ],         # sm2
                             ],
                        1 : [ sampls[key][:] ],               # sm1
                        }
            for i in range(idx):
                titl = titl if i ==0 else ""
                for k in range(nums[i]):                              #
                    ax = fig.add_subplot(gs[k:1+k, i])                #
                    smi = smdict[idx][i]                              #
                    ax = self._multipane(k, smi, ax, titl)            #
            self._do_legend(ax)
        # dictionary linking idx to a function
        doidxs = {
            111: do111,
            200: doN00, # 300: doN00,
            21:   doN1, #  31:  doN1,
            211: do2N1, # 201: do2N1,
            1:     doN,   2:   doN,  3: doN,
            }
        # call function linked to idx in dictonary
        doidxs[idx]()
        return fig


class BinPanelPlotter(LengthPanelPlotter):
    def __init__(self, group, nams, lens, sampls, df, numbers, titles):
        super().__init__(group, nams, lens, sampls, df, numbers, titles)
        self.dolegend = False
        self.df = df.reset_index()
        self.savdir = LIBCNTS


class BrokenLengthPanelPlotter(LengthPanelPlotter):
    """Create paneled figure to display grouped length graphs; each graph needs
    an ax.
    """
    def __init__(self, group, nams, lens, sampls, df, numbers, titles):
        super().__init__(group, nams, lens, sampls, df, numbers, titles)
        self.fcie = self._broken_lengths
        self.dolegend = False
        self.df = df.reset_index()
        self.format_ax = 'y'

    def _broken_lengths(self, sample, ax):
        """Create barv-graph of lengths with broken x-axis to fit paneled
        figure.

        Parameters
        ----------
        sample : str
            Key for sample to display.
        ax : matplotlib.axes.Axes
            Axes object that needs the bardiagram drawn into.

        Returns
        -------
        matplotlib.axes.Axes
            Graphing instructions on ``ax``
        """
        numbers = self.numbers[0]
        dfs = self.df[ [sample, numbers ] ]
        format_ax = self.format_ax

        ax=sns.barplot(
            ax=ax,
            data=dfs,
            x=numbers,
            y=dfs[sample],
            alpha=THISALPH,
            edgecolor="w",
            linewidth=0.2,
            )

        ax.set_ylabel(sample, rotation=0, ha='right', fontsize='x-small')
        ax.yaxis.set_label_coords(-0.033,0.1)
        set_axes(ax, format_ax)
        ax.set_yticks([])
        return ax


class RegionCountPanelPlotter(CountPanelPlotter):
    """Create paneled figure to display grouped region count graphs."""
    def __init__(self, group, nams, lens, sampls, df, numbers, titles): #, dolegend):
        super().__init__(group, nams, lens, sampls, df, numbers, titles)
        self.fcie = self._barh_region_plot
        self.log2_ax = None
        #self.dolegend = dolegend
        self.savdir = REGCNTS
        self.hfac = len(numbers) * CPPHFAC * 0.6

    def _barh_region_plot(self, samples, ax, titl):
        """Create barh-graph to fit paneled figure.

        Parameters
        ----------
        samples : list
            List of samples as members of chosen group.
        titls : str
            Graph title.
        ax : matplotlib.axes.Axes
            Axes object that needs the bardiagram drawn into.

        Returns
        -------
        matplotlib.axes.Axes
            Graphing instructions on ``ax``
        """
        xlabel = self.xlabel
        numbrs = self.numbers
        sampls = sorted(samples)
        df = self.df

        format_ax = self.format_ax
        log2_ax = self.log2_ax
        #sampleidxs = [ x for x in df.index if x in samples]

        df.loc[sampls,numbrs].plot(
            ax=ax,
            kind='barh',
            #stacked=True,
            alpha=THISALPH,
            legend=None,
            )
        set_axes(ax, format_ax, log2_ax)
        # turn off 'Sample' label on y-axis
        ax.set_ylabel('')
        # reverse the display order to read from top to bottom
        ax.invert_yaxis()
        ax.tick_params(axis='y',labelsize='x-small')
        ax.set_xlabel(xlabel, fontsize='small')
        ax.set_title(titl, loc='left', fontsize='small')
        return ax


class Log2RegionCountPanelPlotter(RegionCountPanelPlotter):
    """Create paneled figure to display grouped library log2(count) graphs."""
    def __init__(self, group, nams, lens, sampls, df, numbers, titles): #, dolegend):
        super().__init__(group, nams, lens, sampls, df, numbers, titles)
        self.fcie = self._barh_plot
        self.log2_ax = "x"
        #self.dolegend = dolegend
        self.savdir = LIBCNTS
