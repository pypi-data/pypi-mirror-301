#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  countfile_plots.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module to plot count comparisons."""
import logging
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


from coalispr.bedgraph_analyze.experiment import (
    for_group,
    )
from coalispr.bedgraph_analyze.process_bamdata import (
    num_counted_libs,
    )
from coalispr.count_analyze.load_countfile import (
    get_freq_frame,
    get_readlengths_frame,
    load_bin_table_perc,
    load_count_table,
    )
from coalispr.count_analyze.panel_plotters import (
    BinPanelPlotter,
    BrokenLengthPanelPlotter,
    CountPanelPlotter,
    LengthPanelPlotter,
    Log2CountPanelPlotter,
    )
from coalispr.resources.constant import (
    ALL,
    BCO, BINN,
    CHRXTRA,
    COU, CNTLABELS,
    EXP, EXPDISP,
    INTR,
    LENCNTS, LENCOUNTS, LIBR, LOG2BG,
    MAXGAP, MINGAP, MULMAP,
    PERC, PLOTFREQ, PLOTINTRLEN, PLOTLEN, PLOTLIB, PLOTMMAP, PLOTPERC, PLOTSTRT,
    REGI, RLENCOUNTS,
    SHOWDISC, SKIPINT, SNSFNTSZ, SPECIFIC,
    THISALPH,
    UNSEL, UNSPECIFIC, UNSPCGAPS,
    )
from coalispr.resources.plot_utilities import (
    anchored_text,
    capit_label,
    edit_toolbar,
    get_context,
    init_sns,
    less_xlabels,
    no_titles,
    save_output_as,
    set_axes,
    )
from coalispr.resources.utilities import (
    bins_sum,
    doneon,
    get_skip,
    get_ylabel,
    merg,
    remove_odds,
    thisfunc,
    )

logger = logging.getLogger(__name__)
init_sns()


def _mkplot_lengths(dflist, types, titles):
    """Plot read length distribution for two dataframes."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True, sharey=True)
    edit_toolbar(fig)
    colh = titles['coltitl']
    chue = titles['hue']
    xlab = titles['xlabel']
    ylab = titles['ylabel']
    info = "{:.1f}{} shown." #\n n = {}"
    #libn = titles['libno']
    for i in [0,1]:
        df = dflist[i]
        #df, ok = drop_skip(df)
        dfsum = df[colh].sum(axis=0)
        ax=sns.barplot(
            ax=axes[i],
            data=df,
            x=xlab,
            y=colh,
            hue=chue,
            alpha=THISALPH,
            edgecolor="w",
            linewidth=0.2,
            palette = [f"C{'0'if i ==1 else '1'}"] if not chue else None, #sns.color_palette(n_colors=1)
            )
        ax.set_title(f"{types[i]} reads", fontsize='medium', loc='left')
        ax.add_artist(anchored_text(info.format(dfsum,colh))) #,libn)))

        ax.set_ylabel(capit_label(ylab))
        set_axes(ax, format_ax='y')
    axes[0].set_xlabel('')
    axes[1].set_xlabel(capit_label(xlab))
    axes[1].legend().remove()
    if not chue: # only PLOTLEN
       less_xlabels(axes[1], [axes[0], axes[1]])
    if chue:
        leg = axes[0].legend(title=titles['legtitl'], loc='right',
            fontsize=SNSFNTSZ,)# bbox_to_anchor=(0.98, 0.1))
        leg.set_draggable(True)
    fig.suptitle(titles['suptitl'], fontsize='large', x=0.5, y=0.95,
        ha='center', va='top')
    fig.canvas.manager.set_window_title(titles['wintitl'])
    save_output_as(titles['wintitl'], LENCNTS)
    plt.show()
    plt.close()


def _get_chrom_data(df, chrom):
    """Return subsection of dataframe, based on index."""
    xtr = df.reset_index()[REGI].str.startswith(CHRXTRA)
    df = df.reset_index()[xtr].set_index(REGI)
    return df


def _get_sample_max(df, param):
    """Create dataframe with sample maxima for ``param``.

    ..   usable to show difference between libs??

    Parameters
    ----------
    df : Pandas.DataFrame
        Dataframe with data to display.
    param : str
    """
    #dh = df.idxmax().to_frame(name=param).merge(
     #   df.max().to_frame('value'), left_index=True, right_index=True)
    dh = merg(df.idxmax().to_frame(name=param),
              df.max().to_frame('value')).drop(param)
    return dh


def _gapped_frame(df):
    """Create dataframe for data display with broken x-axis.

    Parameters
    ----------
    df : Pandas.DataFrame
        Dataframe with data to display.
    """
    if PLOTINTRLEN in df.columns:
        usecol = PLOTINTRLEN
    elif PLOTLEN in df.columns:
        usecol = PLOTLEN
    logging.debug(f"{__name__}.{thisfunc()}:\n{_get_sample_max(df,usecol)}")
    # index will have gaps; fill those up
    df = df.set_index(usecol, drop=True).astype(int)
    # df = df.set_index(df[usecol].astype(int), drop=True)
    #df = df.drop(usecol, axis=1)
    dfmin = min(df.index)
    dfmax = max(df.index)
    dfmax = MAXGAP +2 if dfmax < MAXGAP else dfmax
    # make new dataframe with complete length column
    fullidx = list(range(dfmin,dfmax+1,1))
    df = df.reindex(fullidx, fill_value=0.0)
    # get subsection
    df = df.loc[int(MINGAP): int(MAXGAP)+1]
    # remove uninformative, internal region
    if SKIPINT:
        skip = range( int(SKIPINT[0]), int(SKIPINT[1]), 1) #iterator, only used once
        try:
            df = df.drop(skip)
        except KeyError as e:
            logging.debug(f"{__name__}.{thisfunc()}, KeyError:\n{e}")
            pass
        logging.debug(f"{__name__}.{thisfunc()}: "
            f"{df.loc[(int(SKIPINT[0])-3) : (3+int(SKIPINT[1]))]}")
    return df


#@mpl.rc_context(get_context())
@mpl.rc_context({"figure.autolayout":True, **get_context()}) #-lo
def compare_un_spec_lengths(rdkind, readlen, strand, notitles):
    """Compare distribution of lengths of all **SPECIFIC** and **UNSPECIFIC**
    reads.

    As set in the ``process_bamdata``; data from unused samples are not
    included.
    Relevant file-titles: ``{kind}_[RLENCOUNTS | LENCOUNTS]_ALL_{strand}TSV``.

    Output are diagrams with seaborn bar plots for read-length distribution
    of all or only **UNIQ** reads; can be saved as png or svg.

    Parameters
    ----------
    rdkind : str
        One of **LIBR**, **UNIQ**, **CHREXTRA**, **COLLR**, **INTR**,
        **INTR + COLLR**. Choose all (**LIBR**), only uniquely-mapped reads
        (**UNIQ**, leaving out repetitive sequences like tRNA, rRNA or common
        transposons), reads for extra sequences (**CHREXTRA**), or get
        intron-like gaps (**INTR**}.
    readlen : tuple
        Limits (int,int) of read lengths to show.
    strand : str
        One of **COMBI**, **MUNR**, or **CORB**.
    notitles : bool
        Flag to set display of figure title on graph.
    """
    def ungap_index():
        dfl = []
        for df in [dfu, dfs]:
            dfl.append( _gapped_frame(df).reset_index() )
        return dfl

    def select_range():
        dfl = []
        for df in [dfu, dfs]:
            df = df[ (df[PLOTLEN].astype(int) >= readlen[0]) &
                     (df[PLOTLEN].astype(int) <= readlen[1]) ]
            dfl.append(df)
        return dfl

    if INTR in rdkind:
        nam = f"{rdkind}_{LENCOUNTS}_{ALL}_{strand}"
        dfs = get_freq_frame(nam, use=SPECIFIC, debug=0)
        dfu = get_freq_frame(nam, use=UNSPECIFIC, debug=0)
        coltitl = PLOTPERC
        xlabel = PLOTINTRLEN
        hue = None
        dfl = ungap_index()
    else:
        nam = f"{rdkind}_{RLENCOUNTS}_{ALL}_{strand}"
        dfs = get_readlengths_frame(f"{nam}", use=SPECIFIC, debug=0)
        dfu = get_readlengths_frame(f"{nam}", use=UNSPECIFIC, debug=0)
        coltitl = PLOTPERC
        xlabel = PLOTLEN
        hue = PLOTSTRT
        dfl = select_range()

    libno = num_counted_libs(plusdiscards=False)
    msg = (f"\nShowing length distributions for {CNTLABELS[rdkind]} as bar "
          f"graphs for {libno} libraries for {strand} strands (without unused "
          " 'CAT_D' data).")
    print(msg)
    ylabel = f"{PERC} {CNTLABELS[rdkind]}"
    suptitl = (f"Summed {rdkind} length distribution for {EXPDISP}:"
          "\n"
          f"{strand} strands of {libno} libraries.")
    suptitl = no_titles(suptitl,notitles)
    wintitl = remove_odds(f"{rdkind} lengths {EXP} {libno} {strand} "
          f"log2bg{LOG2BG} skip{get_skip()}"
          f"{' ' if not notitles else ' notitles '}{doneon()}").lower()
    #msg += f"\n{get_string_info(dfs)}"
    #msg += f"\n{get_string_info(dfu)}"
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    ftitles = {'legtitl':hue, 'suptitl':suptitl, 'wintitl':wintitl,
        'coltitl':coltitl, 'hue':hue, 'xlabel':xlabel, 'ylabel':ylabel,
        #'libno'=libno,
        }
    _mkplot_lengths(dfl, types=[UNSPECIFIC,SPECIFIC], titles=ftitles)


@mpl.rc_context(get_context())  #-ld
def compare_exp_lengths(rdkind, readlen, strand, group, notitles, use,
    showdiscards):
    """Obtain read-length distribution for all separate library samples.

    Relevant file-titles: ``{kind}_[RLENCOUNTS | LENCOUNTS]_{strand}TSV``.

    Parameters
    ----------
    rdkind : str
        One of **LIBR**, cDNAs (**COLLR**), **CHRXTRA**, **COLLR**, **INTR**,
        **COLLR + INTR**, possibly preceded by **UNIQ** or **MULMAP** to get
        only uniquely-mapped reads (**UNIQ**), or the repetitive sequences
        (**MULMAP**) like tRNA, rRNA or some transposons).
    readlen : tuple
        Limits (int,int) of read lengths to show.
    strand: str
        One of **COMBI**, **MUNR**, or **CORB**.
    group : str
        Name determining grouping of samples, **CATEGORY**, **METHOD**, or
        **FRACTION**.
    notitles : bool
        Flag to set display of figure title on graph.
    use : str
        Tag to filter (**SPECIFIC** or **UNSPECIFIC**) particular reads.
    showdiscards : bool
        Show discarded samples.
    """
    #if rdkind :in [INTR, INTR+COLLR, UNIQ+INTR, UNIQ+INTR+COLLR, MULMAP+INTR,
    #            MULMAP+INTR+COLLR, MULMAP+UNIQ+INTR, MULMAP+UNIQ+INTR+COLLR]:
    if INTR in rdkind:
        nam = f"{rdkind}_{LENCOUNTS}_{strand}"
        df = get_freq_frame(nam, use, debug=0)
        df = _gapped_frame(df)
        numbers = [PLOTINTRLEN]
        ltitl = None
        fcie = BrokenLengthPanelPlotter
        #rlessx = 2
    else:
        nam = f"{rdkind}_{RLENCOUNTS}_{strand}"
        df = get_readlengths_frame(nam, use, debug=0)
        df = df[ (df[PLOTLEN].astype(int) >= readlen[0])   #XLIM00)
               & (df[PLOTLEN].astype(int) <= readlen[1]) ] #XLIM11) ]
        numbers = [PLOTLEN, PLOTSTRT]
        ltitl = PLOTSTRT
        fcie = LengthPanelPlotter
        #rlessx =2

    rlessx =2
    xtr = '' if not showdiscards else " plus unused samples"
    msg = (f"\nShowing length distributions for {use.lower()} "
        f"{CNTLABELS[rdkind]} as bar graphs for {strand} strands of separate "
        f"libraries, grouped by {group.lower()}{xtr}")
    print(msg)
    #msg += f"\n{get_string_info(df)}"
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    nams, lens, sampls = for_group(group, showdiscards)

    libno = sum(lens.values())
    ypart = "" if rdkind == UNSEL else f"{use.lower()}"
    ylabel = f"{PERC} {ypart} {get_ylabel(rdkind, strand, 4)}"
    suptitl = (f"Separate {use} {rdkind} length distributions for {EXPDISP}:"
        f"\n{strand} strands, grouped by {group.lower()}.")
    suptitl = no_titles(suptitl, notitles)
    wintitl = (f"{'' if not showdiscards else f'{SHOWDISC} '}"
        f"separate {use} {rdkind} lengths {EXP} {libno} "
        f"{strand} by {group} "
        f"log2bg{LOG2BG} skip{get_skip()}"
        f"{' notitles ' if notitles else ' '}{doneon()}")
    wintitl = remove_odds(wintitl).lower()

    ftitles = {'legtitl': ltitl, 'suptitl':suptitl, 'wintitl':wintitl,
               'xlabel':numbers[0],'ylabel':ylabel, 'rlessx':rlessx,
                }
    fcie(group, nams, lens, sampls, df, numbers, ftitles).plot_panels()


@mpl.rc_context(get_context()) #-lc
def compare_libtotals(rdkind, strand, group, notitles, showdiscards, diff, log2):
    """Obtain read total library count distribution for two dataframes

    Relevant file-titles: "{kind}{COU}_{strand}{TSV}".

    Parameters
    ----------
    rdkind : str
        One of **LIBR**, **UNIQ**, **CHRXTRA**, **COLLR**, **INTR**,
        **INTR+COLLR**, **INTR+MULMAP**, **SKIP**. Choose all (**LIBR**), only
        uniquely-mapped reads (**UNIQ**, leaving out repetitive sequences,
        **MULMAP**, like tRNA, rRNA or common transposons), reads for extra
        sequences (**CHREXTRA**), or get intron-like gaps (**INTR**}. Or reads
        skipped (**SKIP**) because of imperfect alignment according to cigar
        string.
    strand: str
        One of {**ALL_COMBI**, **COMBI**, **MUNR**, **CORB**}.
    group : str
        Name determining grouping of samples, either **CATEGORY**, **METHOD**,
        or **FRACTION**.
    notitles : bool
        Flag to set display of figure title on graph.
    showdiscards : bool
        Show discarded samples.
    diff : bool
        Show log2 difference or plain **UNSELECTED** values with log 2 scale.
    log2 : bool
        Use log2 scale if True.
    """
    nam = f"{rdkind}{COU}_{strand}"
    numb = f"{SPECIFIC}:{UNSPECIFIC}" if diff else UNSPECIFIC
    explan = (f"{'log2 difference ' if diff else ''}{SPECIFIC} vs. "
        f"{UNSPECIFIC.lower()}")
    if rdkind == UNSEL:
        explan = ''
    skipstrand = f"{strand} strands"
    xtr = '' if not showdiscards else " plus unused samples"
    numbers = [SPECIFIC, numb]
    msg = (f"\nShowing {'log2 ' if (diff or log2) else ''}total library "
        f"counts for {CNTLABELS[rdkind]}, {explan} for {skipstrand}, "
        f"grouped by {group.lower()}{xtr}.")

    if not rdkind == UNSEL:
        dfs = load_count_table(nam, debug=0)
    else:
        dfs = load_count_table(f"{LIBR}{COU}_{strand}", debug=0)

    dfu = load_count_table(nam, use=UNSPECIFIC, usegaps=UNSPCGAPS, debug=0)
    dfl = []
    for df in [dfs, dfu]:
        if rdkind == CHRXTRA:
            df = _get_chrom_data(df, CHRXTRA)
        df = df.sum(axis=0)
        # take log2 after adding 1 where sum is zero (log2 of 1 is 0)
        if diff:
            df = np.log2(df.where(df>0, 1))
        dfl.append(df)

    dfs = dfl[0]
    ddf = dfs-dfl[1] if diff else dfl[1]
    df = pd.concat(objs=[dfs,ddf], keys=numbers).unstack().T

    print(msg)
    #msg += f"\n{get_string_info(df)}"
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    nams, lens, sampls = for_group(group, showdiscards)

    libno = sum(lens.values())
    xlabel = f"{PLOTLIB}{' (log2)' if diff else ''}"
    ylabel = get_ylabel(rdkind, strand)

    if rdkind == UNSEL:
        ylabel = f"{SPECIFIC} vs {get_ylabel(rdkind, strand)}"
    suptitl = (f"Total {CNTLABELS[rdkind]} for {libno} libraries of {EXPDISP}\n"
        f"for {skipstrand}, grouped by {group.lower()}.")
    suptitl = no_titles(suptitl, notitles)
    wintitl = (f"{'' if not showdiscards else SHOWDISC+' '}counts "
        f"{CNTLABELS[rdkind]} {skipstrand} by {group} {EXP} "
        f"log2bg{LOG2BG} skip{get_skip()}"
        f"{' notitles ' if notitles else ' '}{doneon()}")
    wintitl = remove_odds(wintitl).lower()
    ftitles = {'legtitl':'','suptitl':suptitl, 'wintitl':wintitl,
        'xlabel':xlabel,'ylabel':ylabel}

    if log2:
        Log2CountPanelPlotter(group, nams, lens, sampls, df, numbers, ftitles,
            ).plot_panels()
    else:
        CountPanelPlotter(group, nams, lens, sampls, df, numbers, ftitles,
            ).plot_panels()


@mpl.rc_context(get_context())  #-bd
def compare_exp_bins(rdkind, strand, group, notitles, showdiscards):
    """Obtain bin distribution for all **SPECIFIC** samples.

    Relevant file-titles: ``{kind}_{BCO}_{strand}TSV``.

    Parameters
    ----------
    rdkind : str
        One of **LIBR**, **UNIQ**, **CHRXTRA**, **COLLR**, **INTR**, or
        **COLLR+INTR**.
        Choose all (**ALL**), only uniquely-mapped reads (**UNIQ**, leaving out
        repetitive sequences like tRNA, rRNA or common transposons), cDNAs
        (**COLLR**)}.
    strand: str
        One of **COMBI**, **MUNR**, or **CORB**.
    group : str
        Name determining grouping of samples, **CATEGORY**, **METHOD**, or
        **FRACTION**.
    notitles : bool
        Flag to set display of figure title on graph.
    showdiscards : bool
        Show discarded samples.
    """

    nam = f"{rdkind}{BCO}_{strand}"
    use = SPECIFIC
    perc_df = load_bin_table_perc(nam, use, debug=0
                ).dropna(how='all').fillna(0)
    perc_sum_df = bins_sum(perc_df, BINN)
    #perc_sum_df.to_csv(f"{nam}_percallsum{TSV}",float_format='%.4f', sep='\t')
    numbers = [BINN]
    rlessx =  1 # reduction factor for setting labels in less_xlabel; default
    fcie = BinPanelPlotter
    nams, lens, sampls = for_group(group, showdiscards)

    xtr = '' if not showdiscards else " plus unused samples"
    msg = (f"\nShowing bin distributions for {use.lower()} {CNTLABELS[rdkind]} "
        f"counts as bar graphs for {strand} strands of separate libraries, "
        f"grouped by {group.lower()}{xtr}")
    print(msg)
    #msg += f"\n{get_string_info(df)}"
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    libno = sum(lens.values())
    ylabel = f"{PERC} {get_ylabel(rdkind, strand)}"
    suptitl = (f"Bin distributions of library counts of separate {use} "
        f"{rdkind} for {EXPDISP}:\n"
        f"{strand} strands, grouped by {group.lower()}.")
    suptitl = no_titles(suptitl, notitles)
    wintitl = (f"{'' if not showdiscards else f'{SHOWDISC} '}"
        f"bin counts {use} {rdkind} reads {EXP} {libno} "
        f"{strand} by {group} "
        f"log2bg{LOG2BG} skip{get_skip()}"
        f"{' notitles ' if notitles else ' '}{doneon()}")
    wintitl = remove_odds(wintitl).lower()

    ftitles = {'legtitl': None, 'suptitl':suptitl, 'wintitl':wintitl,
               'xlabel':numbers[0],'ylabel':ylabel,'rlessx':rlessx,
                }
    fcie(group, nams, lens, sampls, perc_sum_df, numbers, ftitles).plot_panels()


@mpl.rc_context(get_context())  #-md
def compare_exp_mulmaps(rdkind, strand, group, notitles, use, showdiscards):
    """Obtain hit distribution for multimappers in each library.

    Relevant file-titles: ``{kind}_{MULMAP}_{strand}TSV``.

    Parameters
    ----------
    rdkind : str
        One of **LIBR** or **INTR**.
    strand: str
        One of **COMBI**, **MUNR**, or **CORB**.
    group : str
        Name determining grouping of samples, **CATEGORY**, **METHOD**,
        or **FRACTION**.
    notitles : bool
        Flag to set display of figure title on graph.
    use : str
        Tag to filter particular (**SPECIFIC** or **UNSPECIFIC**) reads.
    showdiscards : bool
        Show discarded samples.
    """
    nam = f"{rdkind}_{MULMAP}_{strand}"
    df = get_freq_frame(nam, use, idx=PLOTFREQ, allc=PLOTMMAP, debug=0)
    #df = _gapped_frame(df)
    numbers = [PLOTFREQ]
    fcie = BrokenLengthPanelPlotter
    nams, lens, sampls = for_group(group, showdiscards)
    libno = sum(lens.values())

    xtr = '' if not showdiscards else " plus unused samples"
    msg = (f"\nShowing distributions for {use.lower()} {MULMAP}s: "
        f"({CNTLABELS[rdkind]}) as bar graphs for {strand} strands of separate "
        f"libraries, grouped by {group.lower()}{xtr}")
    print(msg)
    #msg += f"\n{get_string_info(df)}"
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")
    ypart = f"{use}"
    ylabel = f"{PERC} {ypart} {get_ylabel(rdkind+MULMAP, strand, 4)}"
    suptitl = (f"Separate {use} {MULMAP} {rdkind} distributions for {EXPDISP}"
        f":\n{strand} strands, grouped by {group.lower()}.")
    suptitl = no_titles(suptitl, notitles)
    wintitl = (f"{'' if not showdiscards else f'{SHOWDISC} '}"
        f"separate {use} {rdkind} {MULMAP} {EXP} {libno} "
        f"{strand} by {group} "
        f"log2bg{LOG2BG} skip{get_skip()}"
        f"{' notitles ' if notitles else ' '}{doneon()}")
    wintitl = remove_odds(wintitl).lower()

    ftitles = {'legtitl': None, 'suptitl':suptitl, 'wintitl':wintitl,
               'xlabel':numbers[0],'ylabel':ylabel,'rlessx':0.5,
                }
    fcie(group, nams, lens, sampls, df, numbers, ftitles).plot_panels()


@mpl.rc_context({"figure.autolayout":True, **get_context()}) #-mo
def compare_un_spec_mulmaps(rdkind, strand, notitles):
    """Compare distribution of hit-numbers (repeats) for **SPECIFIC** and
    **UNSPECIFIC** multimappers.

    As set in the ``process_bamdata``; data from unused samples are not
    included to prevent affecting totals used for percentaging.
    Relevant file-titles: ``{kind}_[MULMAP]_ALL_{strand}TSV``.

    Output are diagrams with seaborn bar plots for hit-number distribution
    of **MULMAP**\ s; can be saved as png or svg.

    Parameters
    ----------
    rdkind : str
        One of **LIBR** or **INTR**.
    strand : str
        One of **COMBI**, **MUNR**, or **CORB**.
    notitles : bool
        Flag to set display of figure title on graph.
    """
    add = f" with {INTR.lower()}" if INTR in rdkind else ""
    coltitl = PLOTMMAP + add

    nam = f"{rdkind}_{MULMAP}_{ALL}_{strand}"
    dfs = get_freq_frame(f"{nam}", use=SPECIFIC, idx=PLOTFREQ, allc=coltitl,
            debug=0)
    dfu = get_freq_frame(f"{nam}", use=UNSPECIFIC, idx=PLOTFREQ, allc=coltitl,
            debug=0)
    dfl = [dfu,dfs] #select_range()

    libno = num_counted_libs(plusdiscards=False)
    msg = (f"\nShowing hit-number distributions for {CNTLABELS[MULMAP+rdkind]} "
        f"as bar graphs for {libno} libraries for {strand} strands (without "
        "unused **CAT_D** data).")
    print(msg)
    suptitl = (f"Combined {MULMAP}s{add} for {EXPDISP}:\n"
          f"{strand} strands of {libno} libraries.")
    suptitl = no_titles(suptitl,notitles)
    wintitl = remove_odds(f"{MULMAP} {rdkind} {EXP} {libno} {strand} "
          f"log2bg{LOG2BG} skip{get_skip()}"
          f"{' ' if not notitles else ' notitles '}{doneon()}").lower()
    #msg += f"\n{get_string_info(dfs)}"
    #msg += f"\n{get_string_info(dfu)}"
    logging.debug(f"{__name__}.{thisfunc()}:\n{msg}")

    ftitles = {'legtitl':None, 'suptitl':suptitl, 'wintitl':wintitl,
        'coltitl':coltitl, 'hue':None, 'xlabl':PLOTFREQ}
    _mkplot_lengths(dfl, types=[UNSPECIFIC,SPECIFIC], titles=ftitles)
