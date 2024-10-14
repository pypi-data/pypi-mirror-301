#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  filter_data.py
#
#  Copyright 2020 Rob van Nues <sborg63@disroot.org>
#
#  "Licensed under the EUPL-1.2 or later"
#
#
"""Module to filter data (#refactor by using pandas logic)"""
import pandas as pd
from pathlib import Path
#from glob import glob

from coalispr.resources.constant import (
    COSEQ,
    OUTPATH,
    )

def collect_coseqframes(folder,start,end,order,repeats,hit):
    print(OUTPATH)
    p = Path(OUTPATH / COSEQ / folder )

    datapaths = sorted(list(p.glob(f"{start}*{end}")))
    print(datapaths)
    alldfs = []
    for no in order:
         for rep in range(1,(repeats+1),1):
            alldfs.append( pd.read_csv(p.joinpath(f"{start}_{no}_{rep}_{end}"), sep='\t', index_col=0) )
    df=pd.concat(alldfs, ignore_index=False, axis=1)
    print(df)
    df.to_csv(p.joinpath(f"ALL_{start}_{no}_{rep}_{end}"), sep='\t')
    df.sort_values(by=hit).to_csv(p.joinpath(f"ALL_sorted_{start}_{no}_{rep}_{end}"), sep='\t')
