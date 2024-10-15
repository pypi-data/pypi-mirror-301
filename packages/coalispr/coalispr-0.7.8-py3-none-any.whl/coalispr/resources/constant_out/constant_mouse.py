#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  constant.py
#
#  Copyright 2020-2024 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
# DO NOT EDIT THE PYTHON SOURCE FILE 'constant.py'; 
# IT WILL BE REGENERATED AUTOMATICALLY FROM .TXT FILES.
# CHANGE '2_shared.txt' and '3_EXP.txt' INSTEAD.
# LOOK AND FEEL AND OTHER GENERAL OPTIONS ARE IN 
# '2_shared.txt'. ALL SETTINGS SPECIFIC FOR THE 
# EXPERIMENT/SESSION ARE IN '3_EXP.txt'
#
#

"""Module with constants.

Notes
-----
This file ``constant.py`` is actually a link/shortcut to 
``coalispr.resources.constant_out.constant_{EXP}.py``,
for EXP as defined in this file.

For notes on file naming and experiment descriptors in 
this file see ``howtoguides.html#Configuration`` in the documentation.
"""

from pathlib import Path

# File names of configuration-templates
SHARED = '2_shared.txt'
EXPTXT = '3_EXP.txt'
 

"""
Begin ``constant_in/2_shared.txt`` (**CONFFOLDER** / **SHARED**)
"""
# keep " " around text

p = Path(__file__).parent

# Program
# -------
# The name also features as name of the work folder where configuration and data
# is stored.
PRGNAM      = "Coalispr"
DESCRIPTION = "COunt ALIgned SPecified Reads"
#
# Commands
# ++++++++
DATASTOR  = "`coalispr storedata -d {1,2} -t {1,2}`"
INFOREGS  = "`coalispr info -r1`"
INPUTRCS  = "`coalispr countbams -rc {1,2}`"

# Logging
# -------
# Maximum log file size in bytes.
LOGMAX = 10000000
# FLAG to accept DEBUG logging level for matplotlib (floods the logs).
MPLDEBUG = False
# to set folder and file names: see below.


# PLOTTING
# ========
#
# Plot labels
# ---------------------
# Labels on interactive plot and saved figures.
# Samples/experiments related to controls:
NEGCTL      = "Negative" #"no RNAi" #"Uninduced" # "Mock"
POSCTL      = "Positive" #"wt RNAi" #"Induced"
# Reads (like) Negative control
UNSPECIFIC  = "Unspecific"
# Reads (like) Positive control
SPECIFIC    = "Specific"
# Typing samples
MUTANT      = "Mutant"
REFERENCE   = "Reference" # "RNAseq"
METHOD      = "Method"
CONDITION   = "Condition"
COLLAPSED   = "Collapsed"
UNCOLLAPSED = "Uncollapsed"
UNSEL       = "Unselected"
DISCARD     = "Not used"
FRACTION    = "Fraction"
# Gaps longer than MININTRON in alignments are called (assumed to be) introns
INTR        = "intron"
# Axis labels interactive plots; keep {} and spaces
# Note that FIGXLABEL is preceded by CHROMLBL set in "3_EXP.txt"
FIGXLABEL   = "{} position; scale 1:{} (bin size)"
FIGYLABEL   = "Bedgraph values; summed/bin"
TRACKLABEL  = "segm."
# Plot titles
PERC        = "%"
PLOTALL     = "All reads"
PLOTSPEC    = "Specific reads"
PLOTUNSP    = "Unspecific, discarded reads"
# Axis labels count figures
PLOTLEN     = "length (nt)"
PLOTINTRLEN = INTR + " " + PLOTLEN
PLOTLIB     = "Library counts"
PLOTPERC    = PERC + " reads"
MEAN        = "mean"
PLOTMEAN    = PERC + f" ({MEAN})" + " {}"
MEDIAN      = "median"
PLOTMEDIAN  = PERC + f" ({MEDIAN})" + " {}"
PLOTRAW     = "Raw counts"
#PLOTSTRT    = "start-nt"
PLOTSTRT    = "5' nt"
PLOTFREQ    = "number of hits"
PLOTMMAP    = PERC + " multimappers"
# Do not capitalize these words at beginning of a phrase:
NONCAPT     = [
              "cDNA", "gRNA", "lncRNA", "miRNA", "mRNA",
              "ncRNA", "piRNA", "rRNA", "sRNA", "siRNA",
              "snRNA", "snoRNA", "tRNA",
              ]
#
# Plot colors
# ------------
# Colors on interactive plot and saved figures
# xkcd: color-name from https://xkcd.com/color/rgb/
# REFERENCE trace
RCOL        = "xkcd:almost black"  # "xkcd:slate grey"
# UNSPECIFIC trace
UCOL        = "xkcd:dull red"
# SPECIFIC trace
SCOL        = "xkcd:cornflower blue" # "g"
# MUTANT trace
MCOL        = "tab:olive"
# NOTSELECTED trace
NCOL        = "xkcd:pale orange"
# DISCARD trace
DCOL        = "xkcd:pale magenta" #lavender"
# Annotation background
ACOL        = "#CAD9EF" # "xkcd:light grey blue"
# Annotation edge
AEC         = "xkcd:slate blue" #"#AFBDD7"
# Annotation arrow line-color
ALC         = "xkcd:slate" #"xkcd:cloudy blue" # "xkcd:slate blue"
# Method background
METHCOL     = "xkcd:cloudy blue"
# Colour of a prominent, major axis
AXCOL       = "xkcd:almost black" # "slate grey"
# Colour of subdued, minor axis
AXCOL2      = "xkcd:light grey"
# Background colour for diagram panels
BCKGRCOL    = "w"
# Background colour for main figure
FIGCOL      = "#f9f9f9" # 2.5% grey
# Colors dict
CKEY1       = "fAGO1"
CKEY2       = "no_sRNA"
CKEY3       = "fAGO2"
CKEY4       = "total_sRNA"
CVAL1       = "#c7b475" # tan
CVAL2       = "#8ec1d6" # light-blue
CVAL3       = "#597dbf" # mid-blue
CVAL4       = "#797979" # mid-gray
# Include vertical gridlines in plots of "coalispr showgraphs";
XGRID       = True
#
# Plot alpha settings
# -------------------
# Transparant traces to build up the plot so that intensity indicates overlap
ALPH        = 0.33
# On click increase trace density so that it lights up
HIGHALPH    = 0.7
# Background for annotation labels
ANNOTALPH   = 0.9
# Lighten up active legend items
HIGHLEG     = 0.8
# Reduced colour for inactive legend items
LOWLEG      = 0.3
# In count plots
THISALPH    = 0.8
#
# Plot line widths
# ----------------
# Normal line width
LINEW       = 1.5
# Fatten selected line
HIGHLINEW   = 2.2
#
# Plot legend layout
# ------------------
# Number of legend columns
LEGNCOL     = 1
#
# Plot font size
# --------------
# Font size used as default
CSFONTSZ    = 12
# For small labels in pile-up figures
SNSFNTSZ    = 8
#
# Font size for plotting bedgraph traces in "coalispr showgraphs";
# When groups in side panels overlap either reduce SGFONTSZ relative
# to SGHEIGHT or increase the showgraphs height).
SGFONTSZ    = 11 #10
# Showgrahs' figure dimensions. Change with SGFONTSZ to enhance readability.
SGHEIGHT    = 9 #8
SGWIDTH     = 12 #10
# anti-aliasing of fonts
TXTALIAS    = True #False



#
# Seaborn settings
# ----------------
GRIDSTYLE   = "whitegrid" #"darkgrid"
CONTEXT     = "paper"
# https://seaborn.pydata.org/tutorial/color_palettes.html
PALETTE     = "muted" #"colorblind
GRIDALPHA   = 0.5
GRIDCOLOR   = "xkcd:light grey"
GRIDAXIS    = "y"
GRIDWHICH   = "major"
GRID        = True
SNSFNTFAM   = "sans-serif"
#
#
# Axis scales
# --------------
# 2^LOGZERO is used as the lower boundary when displaying log2 graphs
#This can be set to chosen LOG2BG cutoff
#LOGZERO     = LOG2BG     #5           # 2^5 = 32
# 2^LOGLIM is used as the upper boundary when displaying log2 graphs
LOGLIM      = 20          # 2^20 = 1,048,576
# LINLIM is used as upper boundary when displaying linear graphs
LINLIM      = 20000       # 20,000
# Formatting numbers (standard)
AXLIMS      = [-3,4]
#
# Default figure format (choose from "png", "ps", "pdf", "svg")
FIGFORMAT   = "svg"
#


# DATAFILE TAGS/TYPES
# ===================
# For files containing data for collapsed reads
TAGCOLL     = "collapsed"
# For files with data for uncollapsed reads
TAGUNCOLL   = "uncollapsed"


# Extension output files/folders
# ==============================
# File extension for files with tab separated values; note the connecting dot.
TSV         = ".tsv"
#TSV         = ".tab"
# Suffix added to folders that are replaced during runs with -f option.
BAK         = ".bak"
TMP         = ".tmp"
# File extension for image files
PNG         = ".png"
SVG         = ".svg"
PDF         = ".pdf"
JPG         = ".jpg" # ".jpeg"
# Resolution for rasterized png files
DPI         = 400


# Unique backup connector
# =======================
# For tsv backups from pickles link sample, chromosome name, datakind and ,strand 
# so that chromosome name will not interfere (can have '_', '-') with restoring 
# to pickle (marked by "KeyError '<chromosome name>', stopping.. Have all files 
# to be merged already been binned?"
P2TDELIM    = "____"


# COUNT READS
# ===========
#
# Multimappers
# ------------
# Multimappers for collapsed and uncollapsed reads are counted differently.
# The MULMAPCOLL and MULMAPUNCOL parameters serve to point to alignment settings
# expected by the `countbams` scripts.
# When mapping your COLLAPSED reads, find an alignment parameter that does the
# following: each multimapping read will be mapped to each locus as 1 read
# (setting "--outSAMprimaryFlag AllBestScore" in STAR).
MULMAPCOLL  = 1
# During alignment of UNCOLLAPSED reads each multimapping read is counted once
# and randomly divided over loci (setting "--outSAMmultNmax 1" in STAR).
MULMAPUNCOLL= 1
# The following optional SAM-tags are used during counting of aligned reads and
# should be exported to the SAMBAM alignment file by the read mapper.
# The STAR aligner sets these as:
NH = "NH"  # > 1 for multimapping collapsed reads
HI = "HI"  # always 1 for uncollapsed reads
#
#
# Test regions
# ------------
# Evaluate number of regions with SPECIFIC reads by parameter settings for
# UNSPECLOG10, USEGAPS, LOG2BG.
# Label used in help dialog
TSTREGIONS  = "collect"
# Column or y-axis label used in output finding regions with various settings.
REGS        = "Regions"
TRSHLD      = "Threshold"

# Labels in TSV file or folder names to indicate particular counts.
# All filenames will end up in undercase and with dots replaced by underscores
# irrespective of settings here (if not, that would be a bug).
#
# Bam-counting
# ------------
#
# ALignment check
# +++++++++++++++
# For single-end fully matching small RNA-Seq reads, possibly with a gapped
# alignment due to the presence of an intron:
CIGFM       = "fullmatch"
# In case of UV-irradiated samples with point-deletions
CIGPD       = "pointdel"
# SAM-tag to check for number of tolerated mutations
NM          = "nM" # in standard output of STAR
# when alignment includes NM in output; can be configurted for STAR with option
# `--outSAMattributes A1 A2 A3 ...` during alignment.
#NM         = "NM" # total number of mutations: nM + (D + I)(D,I from cigar)
# maximum number of tolerated mismatches (integer)
MAXMM      = 10
#
# Raw counts
# ++++++++++
# Tsv files with counts for total mapped and unmapped reads based on alignment
# SAMBAM files and UNMAPPEDFIL (see 3_EXP.txt) are stored in folder:
TOTINPUT    = "input_totals"
# Index column label
SAMPLE      = "Sample"
# Column label for total mapped uncollapsed reads, retrieved from SAM-header.
INMAPUNCOLL = "Mapped"
# Column label for total unmapped reads (left over after alignment)
UNMAP       = "Unmapped"
# Column label marking total mapped collapsed reads, retrieved from SAM-header.
INMAPCOLL   = "Mapped cDNA"
# used in file name for total raw-counts of mapped input
TOTALS         = "totals"
#
# Common
# ++++++
# used in folder name for saving counts
READCOUNTS     = "readcounts"
# used in file name for graphs with CAT_D files shown
SHOWDISC       = "withdiscards"
# Labels for selections
# Reads from transcript-strand
CORB           = "corbett"
# Reads antisense to transcript
MUNR           = "munro"
# Reads for both strands (= CORB + MUNR)
COMBI          = "combined"
# Only data for uniq reads
UNIQ           = "uniq"  # also in "3_EXP.txt"
# Only data for extra reads
XTRA           = "extra" # depends on CHRXTRA in "3_EXP.txt"
# Only data for 'unselected' reads in reads specified as UNSPECIFIC
#NOTSELECTED
# Reads for all samples combined
ALL            = "all"
# Gaps longer than MININTRON in alignments are called (assumed to be) introns
#INTR           = "intron"
# in file name or label
COU            = "_counts"
LIBR           = "library"
# Read collapsed reads as cDNA from counting lines in TAGCOLL bamfiles
COLLR          = "cDNA"
# Skipped reads, not meeting only M or N in cigar (or main settings wrong)
SKIP           = "skipped"
#
# Read lengths
# ++++++++++++
# Lengths of gaps in reads, considered introns by alignment mapper (e.g. STAR)
LENCOUNTS      = "length" + COU
# Reads of a particular length with start nucleotide A, C, G or T.
RLENCOUNTS     = "read" + LENCOUNTS
#
# Multimappers
# ++++++++++++
MULMAP         = "multimapper"
#
# Bins
# ++++
# Labels for counts per bin of a segment with specified reads.
BCO            = "_bin" + COU
#
# Column labels
# +++++++++++++
# Headings for columns in tsv region files
LOWR           = "lower"
UPPR           = "upper"
SPAN           = "span"
SEGSUM         = "segmentsum"
# Headings for columns in tsv count files
# Index-column for intron/gap-length counts
LEN            = "length"
REPS           = "repeats"
# Multi-index-column for read-length counts (nt  RLENCOUNTS)
LENMER         = "start length"
# Multi-index-column for read-counts (segment  bin-no)
# Segment
REGI           = "region"
# Bin number (1 at 5" end and last at 3" end)
BINN           = "bin no"
# Region covered by given bin number
BREG           = "bin-region"
# Index header of dataframes with region counts.
#LABLREG        = "label_region"
#
# Labels for Y-axis
# +++++++++++++++++
# Short, printable titles for constant-constructs used in creating count graphs.
CNTLABELS      = {
    XTRA:             f"{XTRA.lower()} reads",
    COLLR:            f"{TAGCOLL.lower()} reads ({COLLR}s)",
    INTR:             f"reads + {INTR.lower()}",
    INTR+COLLR:       f"{COLLR}s + {INTR.lower()}",
    INTR+MULMAP:      f"{MULMAP.lower()}s + {INTR.lower()}",
    LIBR:             f"{LIBR} reads".lower(),
    LIBR+MULMAP:      f"{MULMAP.lower()}s",
    MULMAP+LIBR:      f"{MULMAP.lower()}s",
    MULMAP+COLLR:     f"{COLLR}s ({MULMAP.lower()})",
    MULMAP+INTR:      f"{MULMAP.lower()}s + {INTR.lower()}",
    MULMAP+INTR+COLLR:f"{COLLR}s ({MULMAP.lower()}) + {INTR.lower()}",
    SKIP:             f"{SKIP.lower()} reads",
    UNIQ+LIBR:        f"{UNIQ.lower()}ue reads",
    UNIQ+COLLR:       f"{COLLR}s ({UNIQ.lower()}ue)",
    UNIQ+INTR:        f"reads ({UNIQ.lower()}ue) + {INTR.lower()}",
    UNIQ+INTR+COLLR:  f"{COLLR}s ({UNIQ.lower()}ue) + {INTR.lower()}",
    UNSEL:            f"{UNSEL} {UNSPECIFIC} reads".lower(),
    }

# Counters
# --------
# Define here what to count. The lists mark items to create countfiles for;
# only (un)comment line to use that counter group or individual counter label
# from a list. Note that complexity/number/size of libraries are the major
# determinants of counting speed; therefore, counting is set (via TAGBAM) to go
# collapsed-read by collapsed-read for selected peak segments. Read-by-read
# counting with uncollapsed data files as input will take much longer.
#
# Counter for read numbers
# based around READCOUNTS, BCO, LIBBINCOUNTS, COU, LIBTOTCOUNTS
CNTREAD        = [LIBR, UNIQ, XTRA, UNSEL]  # MULMAP = LIBR-UNIQ
# Counter for cDNAs (i.e. number of collapsed reads used in the counting)
# based around READCOUNTS, COLLR, UNIQ+COLLR
# UNIQ+COLLR gives the number of unique cDNAs.
CNTCDNA        = [COLLR, UNIQ+COLLR]        # MULMAP+COLLR = COLLR-(UNIQ+COLLR)
# Counter for gaps/introns spanned by a read
# (the skipped "N" number in the cigar string of an aligned read)
# based around READCOUNTS, INTR, INTR+COLLR
CNTGAP         = [INTR, INTR+COLLR, UNIQ+INTR, UNIQ+INTR+COLLR]
# Counter for skipped reads
# based around READCOUNTS, SKIP
CNTSKIP        = [SKIP]
# List of counter lists; in "3_EXP.txt"
#CNTRS          = [CNTREAD, CNTCDNA, CNTGAP, CNTSKIP]
#

# Multimapper counter, i.e. counter for multimappers
# based around MULMAP, REPS
# count multimap occurrences for these counter lists; in "3_EXP.txt"
#MMAPCNTRS      = [ [LIBR, INTR] ]

# Length-counter, i.e. counter for read lengths incl. start nt
# based around RLENCOUNTS, LENMER
LENREAD        = [LIBR, UNIQ, XTRA, UNSEL]  # MULMAP = LIBR-UNIQ
# Length-counter for cDNA lengths incl. start nt
# based around  RLENCOUNTS, LENMER
LENCDNA        = [COLLR, UNIQ+COLLR]        # COLLR+MULMAP = COLLR-(UNIQ+COLLR)
# length-counter for gap-lengths, no starting nt (not in cigar string)
LENGAP         = [INTR, INTR+COLLR, UNIQ+INTR, UNIQ+INTR+COLLR]
# list of length-counters' lists; in "3_EXP.txt"
#LENCNTRS       = [LENREAD, LENCDNA, LENGAP]

# List of lists with total-plus-length counters for scanning a singular region
REGCNTRS       = [ [LIBR, UNIQ],  [COLLR, UNIQ+COLLR], CNTSKIP ]

# FOLDERS
# =======
#
# Output folders
# --------------
# Their paths are relative to the work folder set by `coalispr init` as shown
# at end of EXPTXT. Here are the names of the folders configured.
# Folder names for various output.
#STOREPATH   = defined in CONFNAM (from EXPTXT)
# Binary storage of bedgraph data and indexes (Major version changes in Python
# or Pandas affects readability of .pkl files)
STOREPICKLE = "pickled"
# Files with count data
SAVETSV     = "tsvfiles"
# Alignments extracted from negative data
SAVEBAM     = "bamfiles"
# Backup of binary bedgraph data as text (permanent storage)
PKL2TSV     = "backup_from_pickled"
# Recreated binary storage of bedgraph data (for after version changes)
TSV2PKL     = "pickled_from_backup"
#
##OUTPATH    = defined in CONFNAM (from EXPTXT)
CLUSTVIS    = "clustvis"
CLUSTGR     = "clustgr"
COSEQ       = "coseq"
STEM        = "stem"
PROPR       = "propr"




# Folder settings and names
# -------------------------
# 2 folders between SRCDIR (defined in CONFNAM) and bedgraph files
SRCNDIRLEVEL= 2
# 1 folder between REFDIR (defined in CONFNAM) and bedgraph files
#REFNDIRLEVEL= 1
# User directory
HOME        = "home"
# Current directory
CWD         = "current"
# PRGNAM installation directory with PRGNAM source directory
SRCPRGNAM   = "source"
# Different choice to be made
NOCHOICE    = "other; cancel"
# Base-folder with configuration files
CONFBASE    = "config"
# Folder with configuration templates "2_shared.txt" and "3_EXP_.txt"
# for generating "constant.py"
CONFFOLDER  = "constant_in"
# Folder with logging data
LOGS        = "logs"
#
# Logging file(s)
LOGFILNAM   = "run-log.txt"
# Folder with processed data files
DATA        = "data"
# Folder with downloaded data files
# Note: name is hard-coded in "share/bash_scripts/wget_resources.sh"
DWNLDS      = "downloads"
# Folder with produced figures
FIGS        = "figures"
# Figure folders per EXP
SAVEPNG     = "pngfigures"
SAVESVG     = "svgfigures"
SAVEPDF     = "pdfs"
SAVEJPG     = "jpgfigures"
# SubFolder for figures
CHROMFIG    = "chrom_graphs"
LENCNTS     = "lengthcounts"
LIBCNTS     = "libcounts"
REGCNTS     = "regions"
UNSELFIG    = "unselected_chrom_graphs"
GROUPAVG    = "groupaverages"
SUBFIGS     = [ CHROMFIG, LENCNTS, LIBCNTS, REGCNTS, UNSELFIG, GROUPAVG]

# Folder for processed data files usable by other programs as input
OUTPUTS     = "outputs"
# Folder with input files for generating others
SOURCE      = "source"
# Folder with used GTF files
GTFS        = "gtfs"
# Folder with used fasta files
FASTA       = "fasta"

"""
End ``constant_in/2_shared.txt`` (**CONFFOLDER** / **SHARED**)


Begin ``constant_in/3_EXP.txt`` (**CONFFOLDER** / **EXPTXT**)

"""
# begin "CONFFOLDER/3_EXP.txt"
#
# Notes
# -----
# All lines beginning with "#" are comments and ignored by the program.
# Removing or placing a "#" at the start will activate resp. silence that line.
#
# All strings (text in quotation marks) can be adapted but make sure to:
#     1. keep the quotation marks so that text stays of type string.
#     2. distinguish separate_WordsBy-otherMEANS than space, * | /\ $ : ; %
#     etc. (for file-handling).
# All numbers or True/False values can be changed (no surrounding quotes; these
#     are not strings).
#
# Save this file (EXPTXT) as unformatted text with "EXP" replaced by its value
# (ExpSessionName) set below, resulting in CONFNAM. This is done interactively
# when using the `coalispr init` command, including placing the file CONFNAM in
# the SAVEIN work folder.


# Name session/experiment "ExpSessionName"
# ----------------------------------------
# After editing is complete save this file as 3_ExpSessionName.txt in the same
# folder as the original. Replace "ExpSessionName" by one short word, no spaces
# or special characters (it is part of a file name), keep surrounding quotes.
# For "EXP" to be meaningful, strain names come to mind; e.g. JEC21, H99.
#EXP         = "ExpSessionName"
# Exp can be set by "coalispr init" with "mouse" as the given name.
EXP         = "mouse"
CONFNAM     = "3_mouse.txt"
# Display name for experiment is set to species name (not directly used),
#EXPNAM      = "SpeciesName"
EXPNAM      = "Mus musculus"
# Display experiment name in figure titles
# ----------------------------------------
EXPDISP     = r'$\mathit{'+EXPNAM+'}$'
#
# Parameter settings
# ------------------
# The kind of aligned reads, either collapsed or uncollapsed, in the dataset.
# Values are TAGCOLL (collapsed) or TAGUNCOLL (uncollapsed) set in 2_shared.txt
TAG         = TAGUNCOLL
# Choose which segments of reads are counted; as based on kind of aligned reads.
TAGSEG      = TAGUNCOLL
# Choose which kind of bam files with aligned reads are counted.
# Counting collapsed reads is very fast, no information will be lost.
TAGBAM      = TAGCOLL
#
# To facilitate bedgraph comparison the genome needs to be split into fragments;
# BINSTEP is the size of these fragments;
# Note that this approach reduces nucleotide resolution to a scale 1:BINSTEP
# Reducing BINSTEP, to say 20, increases resolution but slows down proceedings.
BINSTEP     = 50
#
# UNSPECLOG10 is the log10 fold difference between specific peaks and unspecific
# background noise. For example with UNSPECLOG10 set to 1.3 = 10^1.3 = 19.95, a
# ~20-fold difference is used. This means that, in order to be specified as
# "specific", 20-fold more signal needs to be present in a bin for reads of a
# specific/mutant sample than in that bin for reads from a negative sample. If
# less signal-difference is found, these reads are specified as "unspecific" and
# ignored. When no reads are specified (no bedgraphs are drawn) reduce this
# number; it indicates that the experiment has a lower signal-to-noise ratio.
# For example with UNSPECLOG10 = 0.61, the required difference is ~4-fold.
UNSPECLOG10 = 0.905
# Series of possibilities for UNSPECLOG10
# values corresponding to ~4, ~6, ~8, 10, ~20 #, ~50, 100 fold difference
UNSPECTST   = 0.61, 0.78, 0.905, 1.0, 1.3 #, 1.7, 2.0
#
# 2^LOG2B is used as background threshold for reads in that bin to be considered
LOG2BG      = 4           # 2^4 = 16
# Series of possibilities for LOG2BG
LOG2BGTST   = 4,5,6,7,8,9,10
#
# USEGAPS indicate the size of gaps tolerated between sections of a specified
# region/segment; 1*BINSTEP is the minimal gap that can be set. 
# For miRNAs BINSTEP seems a good choice; for large transcript regions targetted 
# by siRNAs a larger value is more fitting to reduce number of single hits.
USEGAPS     = BINSTEP #150         # 3*BINSTEP
# Keep unspecific signals as tight as possible, don"t fuse these.
UNSPCGAPS   = BINSTEP
# Series of possibilities for USEGAPS
UGAPSTST    = 50, 100, 150, 200, 300


# Bam-counting
# ------------
# For miRNAs single peaks can be expected. To score these for counting, expand
# hit coordinates by given, small fraction of BINSTEP (<1). 
MIRNAPKBUF  = 1/5  # 1/5 with BINSTEP 50; 1/4 for miRNA with BINSTEP 20.
# For siRNA analysis this buffer is less needed: siRNA peaks congregate and form 
# lengthy segments overlapping a target. Set to 0 to skip single peaks.
# The offsets define minimal length of region (2*BINSTEP*MIRNAPKBUF) to be 
# counted. BINSTEP is used when MIRNAPKBUF is set to 0.
#
# Alignment check
# +++++++++++++++
# Minimum length mapped read from (STAR) alignment or (Flexbar) trim parameters.
#XLIM0       = 12  # set in 'Settings for Figures'
#
#
# Setting to define sequencing type, single end (SE) vs paired-end  (PE)
#CNTTYP      = SE # if FLAG in [0,16], else
#CNTTYP      = PE
#
# Setting for expected alignment, that can be checked via the cigar string: 
# 'fully matched' (CIGFM) or 'with point deletions (CIGPD)' # see 2_shared.txt
# Cigar items as marked in 'cigartuples;cigarstring'
#   0;M, 1;I, 2;D, 3;N, 4;S, 5;H, 6;P, 7;=, 8;X, or 9;B
#   cigartuples = (operation, length)
#   # for short SE sequences only accept matches (0;M) and gaps (3;N)
#   # for UV-irradiated sequences with point deletions accept (0,2,3)
# For point-mutations (substitutions) (in UV-irradiated sequences) check, 
# separately, SAM-tag nM/NM via settings NM (in 2_shared.txt) and NRMISM.
#
# Set function to check cigar string with; for short RNAs:
CIGARCHK    = CIGFM # [0,3]
# Number of tolerated substitutions (mismatches) defined for NM:
NRMISM      = 0
# for UV-irradiated samples allow point-deletions (CRAC) or substitutions (CLIP)
# CIGARCHK    = CIGPD # [0,2,3] or [2,>1]
# NRMISM      = 1
#
# Minimum size for gap in alignment to count as "intron"
# During counting of bamfiles, gap sizes are read from the cigar string.
MININTRON   = 20
#
# BamCounters
# +++++++++++
# List of lists with counters for read numbers; (defined in "2_shared.txt")
#CNTRS          = [CNTREAD, CNTCDNA, CNTGAP, CNTSKIP]
# List of length-counters' lists; (subsets defined in "2_shared.txt")
#LENCNTRS       = [LENREAD, LENCDNA, LENGAP]
# For counting  multimap occurrences (defined in "2_shared.txt")
#MMAPCNTRS      = [ [LIBR, INTR] ]
# Omit counting introns/gaps: 
CNTRS          = [CNTREAD, CNTCDNA, CNTSKIP]
LENCNTRS       = [LENREAD, LENCDNA]
MMAPCNTRS      = [ [LIBR] ]
#
# Segments
# ++++++++
# BINS is the number of bins (1 or over) to split each specified segment for
# which reads are counted. This helps to map possible coverage differences
# dependent on conditions, say the effect of isolating RNA via RIP1 vs. RIP2).
BINS        = 1
#
# Reads in UNSPECIFIC segments that comply with SPECIFIC small RNA
# characteristics can be retrieved and copied to new bam files for further
# analysis/mapping. These reads are called "unselected" reads.
# Define here the length range and start nucleotide for such reads. The range
# is a tuple, that is: Shortest length (BAMLOW), Longest length (BAMHIGH).
BAMLOW      = 19
BAMHIGH     = 25
BAMPEAK     = BAMLOW, BAMHIGH
# List of start nucleotides; 5" end of siRNAs in fungi are U (T in the reads).
BAMSTART    = "T"
# Name of bash script to make bedgraphs from above new bam files using STAR.
BAM2BGNAM   = "bm2bg.sh"
# Path to script
BAM2BG = p / "share" / "bash_scripts" / BAM2BGNAM


# Settings for Figures
# --------------------
# Correct chromosome name when displaying bedgraph traces with `showgraphs` by
# adjusting x-axis label
#CHROMLBL    = "Chromosome"
CHROMLBL    = ""
#
# 'Backends' are the programs matplotlib uses to present a graphical users' 
# interface (GUI). You will see that this setting determines the look and 
# feel of the interface. A common backend is 'QtAgg', but when many samples 
# are analyzed some `showcount` options can cause python to exit with: 
#    `ICE default IO error handler doing an exit(), .. errno = 32`
# Errors or warnings with 'GTK4Agg' can also occur, like 
#    `Warning: Attempting to freeze the notification queue for object 
#    GtkImage[0x5e7f690]; 
#    Property  notification does not work during instance finalization.
#    lambda event: self.remove_toolitem(event.tool.name))'
# In those cases change 'Backend' to, say, 'TkAgg' or 'GTK3Agg'.
#BACKEND     = 'TkAgg'
#BACKEND     = 'GTK4Agg'
#BACKEND     = 'GTK3Agg'
BACKEND     = 'QtAgg'
# Length boundaries of introns (gaps in alignment) to be displayed in figures.
MINGAP      = 30 #MININTRON
MAXGAP      = 150 
# Interval for tick-labels on x-axis for intron-length distributions.
INTSTEP     = 10
# Set interval of lengths without data to skip
SKIPINT      = "" 
#SKIPINT    = 190, 350
# Length boundaries of reads to be displayed in count figures
XLIM0       = 12 # minimum mapping length
XLIM1       = 40
XLIM00      = 16
XLIM11      = 26
XLIMMIN     = 12 # minimal length of a mapped read
XLIMMAX     = 75 # maximum length of a read
# Allow separate constants for region length-distributions.
XLIMR0      = XLIM00
XLIMR1      = 36 #XLIM1
# Factor defining relative height of sample-panes in bardiagrams
# for many samples a low CPPHFAC keeps the figure managable
# Library counts (CountPanelPlotter)
CPPHFAC     = 1/8 #0.125
# Length distributions of reads or introns/gaps ((Broken)LengthPanelPlotter)
LPPHFAC     = 1/5 #0.2    #1/4 #0.25   #3/8  #0.375
# When assembling stacked panels for all samples, the total height of the 
# longest column defines the figure; with too many samples the figure runs off 
# the page. Setting MAXROW determines how many samples are tolerated before
# this column is split in two (non-equal) stacks. 
MAXROW      = 30

# Datafile folders and names
# --------------------------
# Default directory structure:
# full path to bedgraph and bam files:
# BASEDIR / SRCFLDR+TAG / FILEKEY* / FILEKEY*BEDGRAPH
# BASEDIR / SRCFLDR+TAG / FILEKEY* / SAMBAM
# SRCDIR = BASEDIR / SRCFLDR+TAG
# BASEDIR = Path(SETBASE)
#
# SETBASE is the string giving the absolute or full path to the base directory
# with input sequencing data. This directory contains SRCFLDR+TAG
# folders for either collapsed- or uncollapsed-read alignments, which -in turn-
# contain (links to) FILEKEY folders with bedgraph and bam files.
SETBASE     = "/home/working/DATA_ANALYSIS_2/zenodo/Sarshad-2018"
# SETBASE    = ""
#
# SRCFLDR is name of the folder containing folders with bedgraphs, which are
# based on alignments to a particular reference genome, which depends on EXP.
# When replacing the name, keep underscore at end (the "collapsed" or
# "uncollapsed" tag will get attached here)
# The string "0" reflects that zero mismatches were tolerated during mapping of
# the reads after adapter removal.
MUTNO       = "0"
SRCFLDR     = "STAR-analysis" + MUTNO + "-" + EXP + "_"
#
# Folder with downloaded reference RNA-seq bedgraph-files (separate from data)
# If in a sub-directory of the source folder: ( SRCFLDR / REFS )
# If in a top-level directory (BASEDIR / REFS ; or REFS )
#REFS        = "REFS"
REFS        = ""
# Self-processed reference RNA-seq bedgraph-files in folder alongside data.
# Rename Sra RUNs after downloading data to enable specific alignment parameters
# (settings for mapping reference mRNA will differ from those for small RNA).
#REFNAM      = "refSRR4024831_"
#REFS        = REFNAM + TAG + "_" + MUTNO + "mismatch-" + EXP
#
# File extension used for bedgraph or bam files; note the connecting dot
BEDGRAPH    = ".bedgraph"
#BEDGRAPH    = ".bg"
BAM         = ".bam"
#
# Label in bedgraph filename to indicate data for uniq reads only
# (An aligner as STAR can create such files). These files will be ignored
# unless they are the only ones available.
#UNIQ        # also used for count-file name; set in "2_shared.txt"
#
# Marker for upper, top, left-hand, 1, Watson, reference, (+) strand
# Cartwright and Graur 2011, http://www.biology-direct.com/content/6/1/7
# Used for file naming when writing/saving.
PLUS        = "plus"
# Marker for lower, bottom, right-hand, 2, Crick, (-) strand
MINUS       = "minus"
#
# Markers for PLUS, MINUS as available in names of input bedgraph files.
PLUSIN      = PLUS
MINUSIN     = MINUS
#
# Abbreviated strand-naming during storage via prefixes;
# for PLUS
PL          = "p"
# for MINUS
MI          = "m"
#
# Common/shared name for alignment files with .bam extension as generated by
# `samtools sort` and needed for indexing. Thus the same bam-file name covers
# the alignments for different experiments; therefore the name of the folder
# containing the generated bam-file (FILEKEY*) is used as the distinguishing
# factor.
SAMBAM      = "samtoolsAligned.sortedByCoord.out.bam"
#
# Filename of unmapped reads, filtered out of the sequencing data by alignment;
# an aligner as STAR saves this as a separate file, which can be compresssed.
UNMAPPEDFIL = "Unmapped.out.mate1.gz"
#
# Countable filetypes of unmapped output.
# After mapping by STAR, files with unmapped data (UNMAPPEDFIL) are saved in
# either the format of fastq (with uncollapsed data) or of fasta (with collapsed
# output from pyFastqDuplicateRemover.py from pyCRAC). Therefore:
# for uncollapsed reads unmapped output is of type:
UNMAPTYPE   = "fastq"
# for collapsed reads unmapped output is of type:
UNMAPCOLLTP = "fasta"
# With another aligner that would count unmapped reads, these might be
# retrievable from the SAM.header if these are saved therein. Otherwise
# unmapped read numbers have to be retrieved by other means if unmapped reads
# are not output in fastq or fasta format.


# Experiment file
# ---------------
# EXPFILNAM gives the path to the "experiment file" describing sequencing data.
#EXPFILNAM   = ""
EXPFILNAM   = "GSE108799_Exp.tsv"

# Column headers
# ++++++++++++++
# Headers of expected columns in an experiment file.
#
# FILEKEY is a column of identifiers that link to folders with BEDGRAPH and
# SAMBAM files. When downloading data from GEO with the sra-toolkit, a "Run" 
# column with SRA accession numbers is present in the 'SraRunTable.txt'.
# The expected folder hierarchy is then formed automatically, so that 
# the SRR names of folders can be directly used as links to the data.
FILEKEY     = "Run"
#
# SHORT is a column of memorable abbreviations as names for samples used in the
# display and for comparing bedgraphs.
SHORT       = "Short"
#
# CATEGORY divides samples according to their roles (see below)
CATEGORY    = "Category"
#
# EXPERIMENT gives a longer description than the SHORT name and possibly more
# informative than the FILEKEY. Basically for understanding the table in the
# file; not used in the program.
EXPERIMENT  = "Experiment"
#
# Use GROUP for keeping comparable mutations together. The various GROUPS (see
# below) can be redefined for displaying a longer name than the short version.
GROUP       = "Group"
#
# CONDITION defines environmental or genetic changes (see below)
# CONDITION is defined in "2_shared.txt" as plot label
#
# READDENS values are integers indicating relative density of Reference reads;
# these numbers are used to transform (or level up) overall peakheight of traces
# for reference RNA-seq libraries to allow for an easier visual comparison.
READDENS    = "Read-density"
#
# METHOD describes RNA preparation method (see below)
# METHOD    is defined in "2_shared.txt" as plot label
#
# FRACTION 
# FRACTION    is defined in "2_shared.txt" as plot label

# Column Values
# +++++++++++++
# The labels put in various columns to describe the sample
#
# FILEKEY column
# **************
# These values are as the beginning of bedgraph file-names and of the name of
# the sub-folder where the bedgraphs and alignment file are stored.
#
# SHORT column
# ************
# These values are the shortest possible abbreviation for a sample. Replicates
# of the same experiment should be divided from the short name by means of an
# underscore (_). This enables to display the technical (character) or
# biological (number) replicates of the same experiment as one group. Thus
# three wild-type replicates with SHORT names "wt_1a", "wt_2", "wt_1c" can be
# marked as "wt" in the GROUP column and then displayed as one group named "wt".
#
# CATEGORY column
# ***************
# These values specify the samples and direct how they get sorted/used.
# For Reference
CAT_R       = "R"
# For Unspecific i.e. negative control
# use lowercase for negative controls not used for defining 'UNSPECIFIC' reads
CAT_U       = "U"
# For Specific i.e. positive control
# use lowercase for positive controls not used for defining 'SPECIFIC' reads
CAT_S       = "S"
# For Mutant
# use lowercase for redundant samples not considered for bedgraph display
CAT_M       = "M"
# For Discard
CAT_D       = "D"
#
# METHOD column
# *************
# These values indicate the kind of experiment used for preparing the RNA
# input sample that has been sequenced. RIP, RNA extracted from
# immunoprecipitated proteins (IPs), give less/different background than
# sequences from total RNA preps, for which only a size-enrichment step can be
# applied.
# For reads from a total sRNA seq prep
TOTAL       = "total"
# For reads from a RNA IP sample
RIP1        = "rip1"
RIP2        = "rip2"
# For reads from a RNA IP beads/untagged control (found to be unusable as CAT_U;
# mostly CAT_D)
NOTAGIP     = "rip0"
#
# GROUP column
# ************
# These values will normally be the first part of the associated and
# comparable short names of a mutant, say a2 for a2_2, a2_1, a2_3ms0 samples.
# Other labels for a group of mutants could reflect a shared role.
# In this example for reads in mutants linked to DNA or histone methylation.
OTHR        = "meth"
#
# CONDITION column
# ****************
# Entries are optional; values will be extracted from the EXPFILE when needed.
#
# Values reflect different grow or genetic conditions that could affect
# phenotype, i.e. the kind of RNA produced that would be sequenced.
# For example a genetic modification with huge impact:
# Mutant made in RNAi-null parental strain. (REPAIR is not used in source code.)
REPAIR      = "rep"
# An example of an environmental change that can be expected to have an impact:
# Samples from Murashige and Skoog starvation medium (MS0) kept in the dark,
# described as stimulating mating, and spore formation, under which RNAi-
# proteins become more abundant in Cryptococcus (doi:10.1101/gad.1970910).
# (STARV as constant, is not used in source code.)
STARV       = "ms0"
# Samples that have been grown to a very high density possible leading to
# quorum or nutritional stress. (DENSE as constant, is not used in source code.)
DENSE       = "highOD"
# Samples not annotated are considered to represent the same standard condition
# and are referred to with constant REST (which is used in source code).
REST        = "standard"
#
# FRACTION column
# ***************
# These values reflect which fractions of a biological sample have been used for
# preparing the RNA
#Whole cell extract
WCE         = "WCE"
#Nucleolus
NUCLEO      = "Nucleo"
NUCL        = "Nuc"
# Cytosol, cytoplasmic
CYTO        = "Total"
MITOCH      = "Mit"
MEMBR       = "Mem"
VACUOL      = "Vac"
GRANUL      = "P-body"
#Endoplasmic reticulum
ENDRET      = "ER"
#Extracellular
EXCELL     = "Medium"

# Groups definitions
# ------------------
# A dictionary, key (= "SHORT label in EXPFILE") : value ("displayed");
#
# For a functional presentation order (not alphabetical) and to provide extra 
# description for short names (**SHORT**) when displaying values of a GROUP  
# column alongside bedgraph traces; these will form side-panel titles.
#
# Only replace key/value labels, keep { }, quotes " ", colon : and commas 
# between key:value entries.
# '\u0394' is unicode for the delta symbol; '\u03B2' for beta; '\u2192', arrow.
MUTGROUPS   = {
                "n" : "Nuclear no_dox",
                "t" : "Cytoplasmic no_dox",
                "A2n" : "AGO2 IP, nuclear",
                "A2t" : "AGO2 IP, cytoplasmic",
              }


# Other possible groups for the side panel legend, defines labels and order of
# presentation/appearance.
# Use (remove # sign) "" lines if only one condition or method has been tested
# and remove (comment out) lines with different conditions or different methods.

CONDITIONS  = ""
#METHODS     =  ""

METHODS     = {
                TOTAL:"Total", RIP1:"AGO1 IP", RIP2:"AGO2 IP",
                NOTAGIP:"No-tag IP",
              }
              
FRACTIONS   = {
                NUCL:"Nuclear", CYTO:"Cytoplasmic",
              }

# define (display order of) mutant-groups for CAT_M and CAT_U
UNSPECIFICS = [
               "n", "t",
              ]

MUTANTS     = ""


# Genome info
# -----------
# genome info; all files should be placed in the "config/source" folder;
# use "" if not applicable (remove # at beginning); remove or comment out
# example line (place # at beginning)
LENGTHSNAM = "GRCm_genome_fa-chrlengths.tsv"
#] When extra, mutational sequences are described in fasta and gtf
DNAXTRNAM  = ""
LENXTRFILNAM = ""
#LENGTHSFILE = ""
LENXTRA     = "" # 43824   # same value as in LENXTRAFILE;
# Name for extra "chromosome" with mutational DNA sequences;
CHRXTRA     = ""
#CHRXTRA     = XTRA # "extra", set in "2_shared.txt";
# Annotation files to be used for gtf-tracks in bedgraph display
# use "" if not applicable
GTFSPECNAM  = "miRNAs.gtf" # from "mmu.gff3" #Jec21sRNAsegmentsAll.gtf"
GTFUNSPNAM  = "common_ncRNAs.gtf" #Cryptococcus_neoformans.ASM9104v1.ncrna__db.gtf"
GTFREFNAM   = "miRNAtargets.gtf" #CrypJEC21-RNAi-spliced-genes_LTRs_pseudo.gtf"
# GTF file that annotates "chromosome" CHRXTRA;
# For extension of reference GTF
GTFXTRANAM  = "" #MitochCneoDTagsRecombinationalDNAs-genes_exons_cds.gtf"
# For extension of GTFUNSPNAM GTF with common non-coding RNAs
GTFUNXTNAM  = "" 

# In case other keywords are used to describe most relevant feature in GTF
GTFEXON     = "exon"        # kind of annotated feature to display
GTFFEAT     = "sirnasegment" # feature of choice to display


# Work-folder for storing configuration, logs, figures and data
# -------------------------------------------------------------
# Generated from above settings:
BASEDIR     = Path(SETBASE)
# Where to store outputs from ("data") and configuration files for the program
# (the EXPFILE, "2_shared.txt" and "3_EXP_.txt" files)
# Generated after init:
# User home directory, similar to choice "home folder" during "coalispr init".
#SAVEIN      = Path.home() / PRGNAM
# Near sequencing files, as choice "current directory" during "coalispr init".
#SAVEIN      = BASEDIR / PRGNAM
# Next to program folder, like "source folder" choice during "coalispr init".
#SAVEIN      = p.parent.parent
# Set by "coalispr init" to /home/working/DATA_ANALYSIS_2/dataOtherLabs/Sarshad-2018/Coalispr
SAVEIN      = Path("/home/working/DATA_ANALYSIS_2/zenodo/Sarshad-2018/Coalispr")

# Within program source folder "resources/" (remnant from development)
#CONFIG      = p
# In config subfolder (default)
CONFIG      = SAVEIN / CONFBASE

LENGTHSFILE = BASEDIR / LENGTHSNAM
#LENGTHSFILE = BASEDIR / SOURCE / LENGTHSNAM
DNAXTRA     = ""
#DNAXTRA     = BASEDIR / DNAXTRNAM
#DNAXTRA     = BASEDIR / SOURCE / DNAXTRNAM
LENXTRAFILE = ""
#LENXTRAFILE = BASEDIR / LENXTRFILNAM
#LENXTRAFILE = BASEDIR / SOURCE / LENXTRFILNAM

# Next to sequencing data
EXPFILE     =  BASEDIR / EXPFILNAM
# In/next to configuration folder
#EXPFILE     = CONFIG / EXPFILNAM
CONFPATH    = CONFIG / CONFFOLDER
CONFFILE    = CONFPATH / CONFNAM
OUTPATH     = SAVEIN / OUTPUTS / EXP
STOREPATH   = SAVEIN / DATA / EXP
# Parent-folder(BASEDIR)/TAG folder/exp-folder/exp-bedgraph-files
SRCDIR      = BASEDIR / (SRCFLDR + TAG)
# Parent-folder(BASEDIR/REFS)/reference-folder/reference-bedgraph-files
REFDIR      = BASEDIR / REFS
#REFDIR      = SRCDIR / REFS ## REFNDIRLEVEL= 2
# Number of folders between REFDIR and bedgraph files
REFNDIRLEVEL= 1

GTFSPEC     = BASEDIR / GTFSPECNAM
#GTFSPEC     = BASEDIR / SOURCE / GTFSPECNAM
GTFUNSP     = BASEDIR / GTFUNSPNAM
#GTFUNSP     = BASEDIR / SOURCE / GTFUNSPNAM
GTFREF      = BASEDIR / GTFREFNAM
#GTFREF      = BASEDIR / SOURCE / GTFREFNAM
# For extension of reference GTF
GTFXTRA     = ""
# For extension of GTFUNSPNAM GTF with common non-coding RNAs
#GTFUNXTR    = BASEDIR / SOURCE / GTFUNXTNAM
#GTFUNXTR    = BASEDIR / GTFUNXTNAM
GTFUNXTR    = ""


# Figure paths
FIGDIRSVG   = SAVEIN / FIGS / EXP / SAVESVG
FIGDIRPNG   = SAVEIN / FIGS / EXP / SAVEPNG
FIGDIRPDF   = SAVEIN / FIGS / EXP / SAVEPDF
FIGDIRJPG   = SAVEIN / FIGS / EXP / SAVEJPG
# Set here preferred default:
FIGDIR      = FIGDIRSVG

# Debug log
LOGFIL      = SAVEIN / LOGS / EXP / LOGFILNAM
