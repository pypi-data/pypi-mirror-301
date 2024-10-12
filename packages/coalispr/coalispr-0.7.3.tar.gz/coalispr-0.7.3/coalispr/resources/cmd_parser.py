#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  cmd_parser.py
#
#  Copyright 2023-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
from argparse import (
    ArgumentParser,
    ArgumentDefaultsHelpFormatter,
    )
from coalispr.bedgraph_analyze.experiment import (
    goption,
    has_grouparg,
    has_discards,
    has_redundant_muts,
    mixed_groups,
    )
from coalispr.bedgraph_analyze.genom import (
    chroms
    )
from coalispr.resources.constant import (
    ALL,
    BAMPEAK, BAMSTART, BINS,
    CATEGORY,
    COLLR, COMBI, CONDITION, #CONDITIONS,
    CONFPATH, CORB,
    DESCRIPTION,
    FRACTION, #FRACTIONS,
    GROUP,
    INTR,
    JPG,
    LIBR, LOG2BGTST,
    MAXMM, MEAN, MEDIAN, METHOD, #METHODS,
    MINUS, MULMAP, MUNR, #MUTANT, MUTGROUPS,
    NRMISM,
    PDF, PLUS, PNG, PRGNAM,
    REST,
    SKIP, SPECIFIC, SVG,
    TAG, TAGBAM, TAGCOLL, TAGSEG, TAGUNCOLL, TSTREGIONS,
    UGAPSTST, UNIQ, UNSEL, UNSPECIFIC, UNSPECTST,
    XLIM0, XLIM00, XLIM1, XLIM11, XLIMR0, XLIMR1,
    )
from coalispr.resources.utilities import (
    chrxtra,
    )



def make_parser(comms, version):
    """Assemble the parser for coalispr command line.

    Parameters
    ----------
    comms : dict
       Dictionary of commands.
    version : str
       The ``__version__`` string from calling module.

    """

    tag_now = 1 if TAG == TAGUNCOLL else 2
    ifdisc = ['-x{0,1}' if has_discards() else '',
              '-x' if has_discards() else '',
              ]

    grps = mixed_groups()
    gopt = goption()

    mutexcl = ("init | setexp | storedata | showgraphs | countbams | "
               "showcounts | region | annotate |"
              f"{' groupcompare |' if grps else ''} info | test")

    parser = ArgumentParser(
        prog=f'{PRGNAM.lower()}',
        add_help=False,
        description=(f"{PRGNAM}:\n  '{DESCRIPTION}'"),
        usage = (f"{PRGNAM.lower()} {mutexcl}"
            "\n\t[-v,--version  -h,--help]\n\n")
        )
    subparsers = parser.add_subparsers(title="commands", metavar="", #metavar - string presenting available sub-commands in help
        dest="command")


    init_parser = subparsers.add_parser('init',
        description=f"Name experiment and set up {PRGNAM} work folder",
        usage=f"{PRGNAM.lower()} init [-h] ",
        help=("Provide a name for session/experiment; set path to folder "
            f"for {PRGNAM} output and configuration files. Before continuation"
            ", adapt the configuration files."),
        )
    init_parser.set_defaults(func=comms['init'])


    setexp_parser = subparsers.add_parser('setexp',
        description="Set the name for experiment/session",
        usage=f"{PRGNAM.lower()} setexp -e " + "[-p {1,2} -h] ",
        help=("Set experiment/session to -e with path -p to its configuration "
            "file."),
        formatter_class=ArgumentDefaultsHelpFormatter,
        )
    setexp_parser.set_defaults(func=comms['setexp'])
    # https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments
    setexp_optional = setexp_parser._action_groups.pop()
    setexp_required = setexp_parser.add_argument_group('required arguments')
    setexp_parser._action_groups.append(setexp_optional)
    setexp_required.add_argument('-e', type=str, required=True,
        dest='experiment', metavar='EXP',
        help=("The current experiment/session EXP, for example 'h99' or "
            "'mouse'."),
        )
    setexp_parser.add_argument('-p', type=int, choices=[1, 2],
        dest='configpath', default=2,
        help=(f"Path to '3_EXP.txt', which is now in '{CONFPATH}'; "
            f"1: Use this; 2: Find it in another {PRGNAM} work-folder."),
        )


    storedata_parser = subparsers.add_parser('storedata',
        description="Process bedgraphs, back up",
        usage=(f"{PRGNAM.lower()} storedata "
            "-d{1..5} [-t{1,2} -f{0,1} -h] "),
        help=("Process bedgraph files for aligned-reads, make or "
            "restore backups, and rename samples."),
        #formatter_class=ArgumentDefaultsHelpFormatter,
        )
    storedata_parser.set_defaults(func=comms['storedata'])
    storedata_optional = storedata_parser._action_groups.pop()
    storedata_required = storedata_parser.add_argument_group('required '
          'arguments')
    storedata_parser._action_groups.append(storedata_optional)
    storedata_required.add_argument('-d', type=int, choices=[1,2,3,4,5],
        required=True,  dest='datafiles',
        help=("Process bedgraph files: 1: store data (in binary format); "
            "2: store reference(s); "
            "3: backup binary data to text files; "
            "4: restore binary data from text backup; "
            "5: rename sample(s) in data, count and experiment files."
            )
        )
    storedata_parser.add_argument('-t', type=int, choices=[1, 2], dest='tag',
        default=tag_now,
        help=(f"Set file-name tag (now: {TAG}) to type of aligned data: "
            f"1: {TAGUNCOLL}; 2: {TAGCOLL}.")
        )
    storedata_parser.add_argument('-f', type=int, choices=[0, 1],
        dest='force', default=0,
        help=("Force processing; backup any previous data. 0: No; 1: Yes.")
        )


    showgraphs_parser = subparsers.add_parser('showgraphs',
        description="Compare bedgraphs for a chomosome",
        usage=(f"{PRGNAM.lower()} showgraphs -c "
            "[-w{1..4} -s{1,2,3} -t{1,2} -r{0,1} "
            f"{ifdisc[0]} "
            "-u{0,1} -sp {0,1} -wg {1,2,3}]"),
        help=("Compare series of bedgraphs -w for chromosome -c  using samples "
            "-s for aligned reads of type -t "
            f"{'(include discarded samples -x)' if has_discards() else ''}. "
            "Show side panel with sub-legends (-sp). "
            "Start with region (-r), show or write to file (-wg)"),
        formatter_class=ArgumentDefaultsHelpFormatter,
        )
    showgraphs_parser.set_defaults(func=comms['showgraphs'])
    showgraphs_optional = showgraphs_parser._action_groups.pop()
    showgraphs_required = showgraphs_parser.add_argument_group('required '
        'arguments')
    showgraphs_parser._action_groups.append(showgraphs_optional)
    showgraphs_required.add_argument('-c', type=str, choices=chroms(),
        required=True, dest='chrom',
        help="Chromosome for which bedgraphs to show.")
    showgraphs_parser.add_argument('-w', type=int, choices=[1,2,3,4],
        default=1, dest='windowchoice',
        help=("Sequence of windows to show: 1: a) with all mapped reads, b) "
            "with all unspecific reads, then c) with all specific reads; 2: "
            "only all mapped reads (1a); 3: only unspecific reads (1b); or 4: "
            "only specific reads (1c)."),
        )
    showgraphs_parser.add_argument('-s', type=int, choices=[1,2,3],
        default=2, dest='samplechoice',
        help=("Choose libraries to show:  1: controls; 2: configured non-"
            "redundant data (controls plus mutants); 3: data incl. redundant "
            "samples."),
        )
    showgraphs_parser.add_argument('-t', type=int, choices=[1,2],
        default=tag_now, dest='tag',
        help=(f"Change type of aligned data (now: '{TAG}') to 1:'{TAGUNCOLL}'; "
            f"or 2:'{TAGCOLL}'.")
        )
    showgraphs_parser.add_argument('-r', type=str, nargs="+",
        default=(0, 0), dest='coord',
        help=("Set the region by directly providing start and end coordinates, "
            "separated by a comma (',') or hyphen ('-'). With incorrect input "
            "or with '-r 1' a dialog helps to enter coordinates."),
        )
    if has_discards():
        showgraphs_parser.add_argument('-x', type=int, choices=[0,1],
            default=0, dest='discarded',
            help="Include discarded samples? 0: No, 1: Yes."
            )
    showgraphs_parser.add_argument('-u', type=int, choices=[0,1],
        default=0, dest='showunselected',
        help=(f"Show {TAGCOLL} data (-t2) including unselected reads? 0: No, "
            f"1: Yes. [Only useful if '{PRGNAM.lower()} countbams -k2 -u1' has "
            f"been run. That is, when unspecific reads have been counted using"
            f" {TAGCOLL} bam files and processed with raw input counts (-rc)]"),
        )
    showgraphs_parser.add_argument('-sp', type=int, choices=[0,1],
        default=1, dest='sidepane',
        help="Include sidepane with sub-legends? 0: No, 1: Yes.",
        )
    showgraphs_parser.add_argument('-wg', type=int, choices=[1,2,3,4,5],
        default=1, dest='dowhat',
        help=(f"Show (1) or write graphs to {SVG} (2), {PNG} (3), {PDF} (4) or "
            f"{JPG} (5)."),
        )


    countbams_parser = subparsers.add_parser('countbams',
        description="Count aligned reads in bam files",
        usage=(f"{PRGNAM.lower()} countbams [-rc "
            "{1,2} -b{1,3,5} -k{1,2} -u{0,1} -pd{0,1} -mm -f{0,1}]"),
        help=(f"Count bam alignment files with '{TAGBAM}' reads using segments "
            f"found in '{TAGSEG}' bedgraphs; divide segments in -b bins; "
            "select for kind -k; and include unselected alignments -u for "
            f"{UNSPECIFIC} reads (with -k2). Tolerate point-deletions (-pd) or "
            "mismatches (-mm). Force counting (-f). "),
        formatter_class=ArgumentDefaultsHelpFormatter,
        )
    countbams_parser.set_defaults(func=comms['countbams'])
    countbams_parser.add_argument('-rc', type=int, choices=[1,2],
        dest='rawcounts',
        help=("Obtain total mapped counts from length alignment files for: "
            f"1: '{TAGUNCOLL}'; 2: '{TAGCOLL}' data with strand information."),
        )
    countbams_parser.add_argument('-b', type=int, choices=[1, 3, 5],
        default=BINS, dest='bins',
        help=("Divide segments to be counted in: 1, 3 or 5 bins; by default "
            f"bins = {BINS}, used for '{SPECIFIC}'-read counting, but is set "
            f"to bins = 1 when counting '{UNSPECIFIC}' reads."),
        )
    countbams_parser.add_argument('-k', type=int, choices=[1, 2], default=1,
        dest='kind',
        help=f"Count '{SPECIFIC}' (1), or '{UNSPECIFIC}' (2) reads.",
        )
    countbams_parser.add_argument('-u', type=int, choices=[0, 1], default=0,
        dest='unselected',
        help=(f"Include counting of unselected reads (within range {BAMPEAK}, "
            f"with 5'-end {BAMSTART}),in {UNSPECIFIC} data? 0: No, 1: Yes."
            "This depends on a program extracting raw bedgraphs from bam data "
            f"(like STAR) and needs raw input counts (-rc for {TAGBAM} reads) "
            "for normalizing created bedgraphs."),
        )
    countbams_parser.add_argument('-pd', type=int, choices=[0, 1], default=0,
        dest='pointdel',
        help="Accept point-deletions? 0: No; 1: Yes."
        )
    countbams_parser.add_argument('-mm', type=int,
        default=NRMISM, dest='mism',
        help=(f"Set tolerated number of mismatches (maximum: {MAXMM})."),
        )
    countbams_parser.add_argument('-f', type=int, choices=[0, 1], default=0,
        dest='force',
        help="Force processing; backup any previous data. 0: No; 1: Yes."
        )


    showcounts_parser = subparsers.add_parser('showcounts',
        description="Display count files",
        usage=(f"{PRGNAM.lower()} showcounts "
            "[-rc {1,2} -lc {1..7} -ld {1..6} -lo {1..5} -bd {1..5} "
            f"-md {1,2} -mo {1,2}{gopt['-g']}{1,2} -k {1,2} -ma {1,2} -st "
            f"{1,2,3} -lg {1,2,3} {ifdisc[0]} -nt {0,1} -h]"),
        help=("Display total raw counts (-rc) for mapped and unmapped reads, "
            "or total library counts (-lc), on log2 (-lg) scale and bin (-bd) "
            f"or length (-ld) distributions for separate '{SPECIFIC}' or "
            f"'{UNSPECIFIC}' libraries (-k) or an overview (-lo); select only "
            f"reads mapping to strand -st; group libraries (-g) by '{CATEGORY}', "
            f"'{METHOD}' or '{FRACTION}'; select mapper type (-ma) to '{UNIQ}' "
            f"or '{MULMAP}' or check hit-number distributions for '{MULMAP}s' "
            "or those with introns (-md, -mo)"
            f"{'; show unused, excluded samples (x)' if has_discards() else ''}"
            "."),
        formatter_class=ArgumentDefaultsHelpFormatter,
        )
    showcounts_parser.set_defaults(func=comms['showcounts'])
    showcounts_parser.add_argument('-rc', type=int, choices=[1,2],
        dest='rawcounts',
        help=("Display total mapped counts from length alignment files for: "
            f"'{TAGUNCOLL}' (1), or '{TAGCOLL}' (2) data with strand "
            "information. Use option -g to change grouping, -lg to use log2 "
            "scale"),
        )
    showcounts_parser.add_argument('-lc', type=int, choices=[1,2,3,4,5,6,7],
        default=0, dest='libcounts',
        help=("Display total library counts for all samples, comparing "
            f"'{SPECIFIC}' and '{UNSPECIFIC}' reads, for {ALL} (1), {COLLR} "
            f"(2), {chrxtra()} (3) reads, or with {INTR}-like gaps (4) or "
            f"those in {COLLR}s (5); or for '{UNSEL}' siRNA-like reads in "
            f"'{UNSPECIFIC}' data (6); or that were {SKIP} (7). Use option "
            "-g to change grouping; -ma for mapper-type; -lg for log2 scale."),
        )
    showcounts_parser.add_argument('-ld', type=int, choices=[1,2,3,4,5,6],
        default=0, dest='lengthdist',
        help=(f"Display separate library distributions for lengths of"
            f"{ALL} (1), {COLLR} (2), {chrxtra()} (3) reads, or for sizes of "
            f"{INTR}-like gaps (4), or those in {COLLR}s (5); or for lengths "
            f"of {UNSEL} siRNA-like reads in {UNSPECIFIC} data (6). Use option "
            f"-g to change grouping; -k2 to change kind to '{UNSPECIFIC}'; "
            "-ma to focus on mapping type."),
        )
    showcounts_parser.add_argument('-lo', type=int, choices=[1,2,3,4,5],
        default=0, dest='lenoverview',
        help=(f"Overview of distributions for {SPECIFIC} vs. {UNSPECIFIC} for "
            f"lengths of {ALL} (1), {COLLR} (2), or {chrxtra()} (3) reads; or "
            f"for sizes of {INTR}-like gaps (4), or those in {COLLR}s (5). "
            "Use -ma to choose mapper-type"),
        )
    showcounts_parser.add_argument('-bd', type=int, choices=[1,2,3,4,5],
        default=0, dest='binperc',
        help=("Display average bin distribution for separate libraries, of "
            f"{ALL} (1), {COLLR} (2), {chrxtra()} (3) reads, or sizes of "
            f"{INTR}-like gaps (4), or those in {COLLR}s (5). Use option -g "
            f"to change grouping; -k2 to change kind to '{UNSPECIFIC}'; "
            "-ma for mapper-type."),
        )
    showcounts_parser.add_argument('-md', type=int, choices=[1,2],
        default=0, dest='mhitdist',
        help=(f"For separatae libraries display distribution of hit numbers "
            f"for {MULMAP}s in 1: {ALL} reads; or in 2: those that contain an "
            f"{INTR}-like gap. Use option -g to change grouping; -k2 to change "
            f"kind to '{UNSPECIFIC}'."),
        )
    showcounts_parser.add_argument('-mo', type=int, choices=[1,2],
        default=0, dest='mhitoverview',
        help=(f"Display an overview of hitnumbers for {SPECIFIC} vs. "
            f"{UNSPECIFIC} for 1: {ALL} {MULMAP}s; or 2: those with an {INTR}."
            ),
        )
    showcounts_parser.add_argument('-rl', type=int, choices=[1,2,3,4],
        default=0,  dest='readlengths',
        help=("Read length (shortest, longest) is restricted to "
             f"1: {(XLIMR0, XLIMR1)}; 2: {(XLIM00, XLIM11)}; "
             f"3: {(XLIM0, XLIM1)}; or 4: Set lower and upper limits, "
             "separated by a comma (',') or hyphen ('-')."),
        )
    if has_grouparg():
        showcounts_parser.add_argument('-g', type=int, choices=gopt['glist'],
            default=1,  dest='grp',
            help=gopt['-h'],
            #help=(f"Display data grouped per {CATEGORY} (1), {METHOD} (2), or "
            #    f"{FRACTION} (3)."),
            )
    showcounts_parser.add_argument('-lg', type=int, choices=[1,2,3],
        default=1, dest='lgcounts',
        help=("Display total counts on linear (1), or log2 (2) scale, or show "
            f"{SPECIFIC} and difference with {UNSPECIFIC} as log2 values (3) "
            "(with -lc or -rc)."),
        )
    showcounts_parser.add_argument('-k', type=int, choices=[1,2], default=1,
        dest='kind',
        help=(f"Display characteristic for {SPECIFIC} (1), or {UNSPECIFIC} (2) "
            "reads of separate libraries.")
        )
    showcounts_parser.add_argument('-ma', type=int, choices=[1,2], default=0,
        dest='mapper',
        help=f"Display characteristics for {UNIQ} (1) reads, or {MULMAP}s (2).",
        )
    showcounts_parser.add_argument('-st', type=int, choices=[1,2,3],
        default=1, dest='strands',
        help=f"Show data for {COMBI} (1), {MUNR} (2), or {CORB} (3) reads.",
        )
    if has_discards():
        showcounts_parser.add_argument('-x', type=int, choices=[0,1], default=0,
            dest='unused',
            help="Include unused samples? 0: No, 1: Yes.",
            )
    showcounts_parser.add_argument('-nt', type=int, choices=[0,1], default=1,
        dest='notitles',
        help=("No titles? Omit figure titles above displayed graphs? 0: Keep; "
            "1: Omit."),
        )


    region_parser = subparsers.add_parser('region',
        description="Get detailed read information for a chromosomal region",
        usage=(f"{PRGNAM.lower()} region -c -r "+" [-s -mm -lg -g -nt "
            f"{ifdisc[1]} -h]"),
        help=("For region -r on chromosome -c, check counts and distribution "
            "of read-lengths for controls (-s1), including mutants (-s2) "
            "or a sample selection (-s3). Compare different counts (-cf), "
            "tolerate point-deletions (-pd) or "
            "mismatches (-mm). Plot on normal or log2 scale (-lg)"
            f"{', organized by group (-g)' if has_grouparg() else ''}."),
        formatter_class=ArgumentDefaultsHelpFormatter,
        )
    region_parser.set_defaults(func=comms['region'])
    region_optional = region_parser._action_groups.pop()
    region_required = region_parser.add_argument_group('required arguments')
    region_parser._action_groups.append(region_optional)
    region_required.add_argument('-c', type=str, choices=chroms(),
        required=True, dest='chrom',
        help="Chromosome for which bedgraphs to show.")
    region_required.add_argument('-r', type=str, nargs="+", dest='coord',
        help=("Set region to analyze by providing start and end coordinates, "
            "separated by a comma (',') or hyphen ('-')."),
        )
    region_parser.add_argument('-s', type=int, choices=[1,2,3],
        dest='samplechoice', default=1,
        help=("Show readlengths for a chromosome region for 1: controls; 2: "
            "controls plus mutants; or 3: a selection of samples."),
        )
    region_parser.add_argument('-cf', type=int, choices=[1,2,3,4],
        dest='comparechoice', default=1,
        help=(f"Compare read-counts for '{LIBR}' to '{COLLR}' (1); or "
            f"'{UNIQ}' to '{MULMAP}' for '{LIBR}' (2), or for '{COLLR}' (3), "
            f"'or all (4)."),
        )
    region_parser.add_argument('-rl', type=int, choices=[1,2,3,4],
        default=1,  dest='readlengths',
        help=("Read length (shortest, longest) is restricted to "
             f"1: {(XLIMR0, XLIMR1)}; 2: {(XLIM00, XLIM11)}; "
             f"3: {(XLIM0, XLIM1)}; or 4: Set lower and upper limits, "
             "separated by a comma (',') or hyphen ('-')."),
             )
    region_parser.add_argument('-st', type=int, choices=[1,2,3],
        default=1, dest='strands',
        help=f"Show data for {COMBI} (1), {PLUS} (2), or {MINUS} (3) strands.",
        )
    region_parser.add_argument('-pd', type=int, choices=[0, 1], default=0,
        dest='pointdel',
        help="Accept point-deletions? 0: No; 1: Yes."
        )
    region_parser.add_argument('-mm', type=int,
        default=NRMISM, dest='mism',
        help=(f"Set tolerated number of mismatches (maximum: {MAXMM})."),
        )
    if has_grouparg():
        region_parser.add_argument('-g', type=int, choices=gopt['glist'],
            default=1, dest='grp',
            help=gopt['-h'],
            #help=(f"Display data grouped per {CATEGORY} (1), {METHOD} (2), or "
            #    f"{FRACTION} (3)."),
            )
    region_parser.add_argument('-lg', type=int, choices=[1,2],
        default=1, dest='lgcounts',
        help=("Display total counts on linear (1), or log2 (2) scale."),
        )
    region_parser.add_argument('-nt', type=int, choices=[0,1], default=1,
        dest='notitles',
        help=("No titles? Omit figure titles above displayed graphs? 0: Keep; "
            "1: Omit."),
        )
    if has_redundant_muts():
        region_parser.add_argument('-rm', type=int, choices=[0,1], default=0,
            dest='redmuts',
            help="Include redundant mutant samples? 0: No; 1: Yes.",
            )
    if has_discards():
        region_parser.add_argument('-x', type=int, choices=[0,1], default=0,
            dest='unused',
            help="Include unused samples? 0: No; 1: Yes.",
            )


    annotate_parser = subparsers.add_parser('annotate',
        description="Annotate regions with counted reads",
        usage=f"{PRGNAM.lower()} annotate [-lc -k -rf -sv -st -ma -lg -x -h]",
        help=("For reads -lc annotate counts for kind -k, mapper -ma and "
           "strand -st; include ref -rf, order libraries by values (-sv) and "
           "use log2 scale for counts (-lg)"
           f"{'; include unused samples (-x).' if has_discards() else '.'}"),
        formatter_class=ArgumentDefaultsHelpFormatter,
        )
    annotate_optional = annotate_parser._action_groups.pop()
    #annotate_required = annotate_parser.add_argument_group('required arguments')
    annotate_parser._action_groups.append(annotate_optional)
    annotate_parser.set_defaults(func=comms['annotate'])
    annotate_parser.add_argument('-lc', type=int, choices=[1,2,4,5],
        default=1, dest='libcounts',
        help=(f"Annotate total library counts for {ALL} reads (1), {COLLR}s "
           f" (2), or reads with {INTR}-like gaps (4) or {COLLR}s with "
           f"{INTR}s (5)."),
        )
    annotate_parser.add_argument('-k', type=int, choices={1,2},
        default=1, dest='kind',
        help=("Annotate Specific (1) or Unspecific reads (2)"),
        )
    annotate_parser.add_argument('-rf', type=int, choices={0,1},
        default=0, dest='plusref',
        help=("Include general **REFERENCE** GTF for annotations (slow). "
           "0: No; 1: Yes."),
        )
    annotate_parser.add_argument('-sv', type=int, choices=[0,1], default=1,
        dest='sortvalues',
        help=("Sort table with respect to values, descending from highest: "
           "0: False; 1: True."),
        )
    annotate_parser.add_argument('-st', type=int, choices=[1,2,3],
        default=1, dest='strands',
        help=(f"Annotate data for {COMBI} (1), {MUNR} (2), or {CORB} (3) "
           "strands."),
        )
    annotate_parser.add_argument('-ma', type=int, choices=[1,2], default=0,
        dest='mapper',
        help=f"Restrict annotations to {UNIQ} (1) reads, or {MULMAP}s (2).",
        )
    annotate_parser.add_argument('-lg', type=int, choices=[1,2],
        default=1, dest='lgcounts',
        help=("Display total counts on linear (1), or log2 (2) scale."),
        )
    if has_discards():
        annotate_parser.add_argument('-x', type=int, choices=[0,1], default=0,
            dest='unused',
            help="Include unused samples? 0: No; 1: Yes.",
            )

    if grps:
        picks = {k:v for k,v in enumerate(grps.keys(),1)}
        picklist = list(picks.keys())
        pickitems = picks.items()

        groupcompare_parser = subparsers.add_parser('groupcompare',
            description=("Compare length-distributions of samples according "
            f" to their type as defined by mutation ('{GROUP}'), '{METHOD}', "
            f"'{FRACTION}', or '{CONDITION}'."),
            usage=(f"{PRGNAM.lower()} groupcompare -g [ -5e ld -ts -st -av -rl "
            f"-ma -nt {ifdisc[1]} ]"),
            help=("Groupwise (-g) comparison of length distributions (-ld) for "
               "reads with 5' end -5e and readlengths -rl, showing "
               "standard deviations with respect to average -av for selected "
               "samples (-ts) with mapping frequency -ma and of kind -k "
               "for strand -st"
               f"{'; include unused samples (-x).' if has_discards() else '.'}"
               ),
            formatter_class=ArgumentDefaultsHelpFormatter,
            )
        groupcompare_parser.set_defaults(func=comms['groupcompare'])
        groupcompare_optional = groupcompare_parser._action_groups.pop()
        groupcompare_required = groupcompare_parser.add_argument_group(
            'required arguments')
        groupcompare_parser._action_groups.append(groupcompare_optional)
        groupcompare_required.add_argument('-g', type=int, choices=picklist,
            required=True, dest='fromgroup',
            help=("Restrict comparison to "
                f"{', '.join(f'{k}: {v}' for k,v in pickitems)}."),
            )
        groupcompare_parser.add_argument("-5e", type=str,
            choices=["T","t", "A","a", "G","g", "C","c", "N","n"], default='T',
            dest='nt5end',
            help=("Choose the start nucleotide of reads to compare. One of "
                "T; A; G; C; or N."),
            )
        groupcompare_parser.add_argument('-ts', type=int, choices=[1,2,3],
            dest='trimsampleset', default=1,
            help=("Trim samples. 1: No negative controls and specify; "
                f"2: No negative controls, only {REST} samples; 3: Specify all "
                "samples."),
            )
        groupcompare_parser.add_argument('-ld', type=int, choices=[1,2,3],
            default=1, dest='lengthsdistrib',
            help=(f"Compare length distributions for 1: {ALL}; 2: {COLLR}; "
                f"3: {chrxtra()} reads."),
            )
        groupcompare_parser.add_argument('-av', type=int, choices=[1,2],
            default=1, dest='average',
            help=f"Kind of average to plot. 1: '{MEAN}'; or 2: '{MEDIAN}'.",
            )
        groupcompare_parser.add_argument('-rl', type=int, choices=[1,2,3,4],
        default=1,  dest='readlengths',
            help=("Show read lengths (shortest, longest) for "
             f"1: {(XLIMR0, XLIMR1)}; 2: {(XLIM00, XLIM11)}; "
             f"3: {(XLIM0, XLIM1)}; or 4: Set lower and upper limits, "
             "separated by a comma (',') or hyphen ('-')."),
             )
        groupcompare_parser.add_argument('-st', type=int, choices=[1,2,3],
            default=1, dest='strands',
            help=(f"Show data for {COMBI} (1), '{MUNR}' (2), or '{CORB}' "
                "(3) reads."),
            )
        groupcompare_parser.add_argument('-ma', type=int, choices=[1,2],
            default=0,  dest='mapper',
            help=f"Restrict annotations to {UNIQ} (1) reads, or {MULMAP}s (2).",
            )
        groupcompare_parser.add_argument('-k', type=int, choices=[1,2],
            default=1, dest='kind',
            help=(f"Display characteristic for {SPECIFIC} (1) or {UNSPECIFIC} "
                "(2) reads.")
            )
        groupcompare_parser.add_argument('-nt', type=int, choices=[0,1],
            default=1, dest='notitles',
            help=("No titles? Omit figure titles above displayed graphs? "
                "0: Keep; 1: Omit."),
            )
        if has_redundant_muts():
            groupcompare_parser.add_argument('-rm', type=int, choices=[0,1],
                default=0, dest='redmuts',
                help="Include redundant mutant samples? 0: No; 1: Yes.",
                )
        if has_discards():
            groupcompare_parser.add_argument('-x', type=int, choices=[0,1],
                default=0, dest='unused',
                help="Show unused samples? 0: No; 1: Yes.",
                )


    info_parser = subparsers.add_parser('info',
        description=("Show experiment name, file paths, number of regions, "
            "or memory-usage"),
        usage=f"{PRGNAM.lower()} info "+"[-i{1,2} -p{1,2} -r{1,2,3} -h]",
        help=("Describe file paths (-p); show detected number of regions with "
            f"'{SPECIFIC.lower()}' reads as a result of parameter settings "
            f"(-r); give experiment name or calculate memory-usage of {PRGNAM} "
            "data in Pandas (-i)."),
        #formatter_class=ArgumentDefaultsHelpFormatter,
        )
    info_parser.set_defaults(func=comms['info'])
    info_parser.add_argument('-i', type=int, choices=[1,2], dest='inform',
        default=1,
        help="Show current experiment (1), or memory-usage (2).",
        )
    info_parser.add_argument('-p', type=int, choices=[1,2], dest='paths',
        help=("Show path to configuration file '3_EXP.txt' (1), or to file "
            "describing sequencing data 'EXPFILE' (2)."),
        )
    info_parser.add_argument('-r', type=int, choices=[1,2,3], dest='regions',
        help=("Obtain regions depending on settings for parameters "
            f"'UNSPECLOG10', from {UNSPECTST}, 'USEGAPS', from {UGAPSTST}, "
            f"and 'LOG2BG', from {LOG2BGTST}. 1: {TSTREGIONS} data; then "
            f"2: show '{TAGUNCOLL}' data; or 3: show '{TAGCOLL}' data. "
             "Note that 1 creates input for 2 or 3.")
        )
    info_parser.add_argument('-nt', type=int, choices=[0,1], default=1,
        dest='notitles',
        help="Omit figure title from graph. 0: Keep; 1: Omit.",
        )


    test_parser = subparsers.add_parser('test',
        description=(f"Test and profile {PRGNAM}"),
        usage=f"{PRGNAM.lower()} test "+"-tp {1,2,3,4} -no -k {1,2} -h",
        help=(f"Test or profile (-tp) commands of {PRGNAM} with -no lines of "
            "report output."),
        formatter_class=ArgumentDefaultsHelpFormatter,
        )
    test_parser.set_defaults(func=comms['test'])
    test_parser.add_argument('-tp', type=int, choices=[1,2,3,4], dest='test',
        default=1,
        help=("Test/profile 1: showgraphs; 2: countbams; 3: count region; or "
            "4: annotate."),
        )
    test_parser.add_argument('-no', type=int, dest='lineno',
        default=25,
        help="Show given number of lines topping the profiling report.",
        )
    test_parser.add_argument('-k', type=int, dest='kind', choices=[1,2],
        default=1,
        help=(f"Test 'countbams' or 'annotate' with {SPECIFIC} (1), or "
            f"{UNSPECIFIC} (2) reads."),
        )

    parser.add_argument('-v','--version', action='version',
        version=f'%(prog)s {version}')
    parser.add_argument('-h','--help', action='help',
        help='Show this help message and exit.')

    return parser
