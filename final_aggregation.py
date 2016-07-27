# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 00:09:23 2016

@author: tim

Description:
Simple script to aggregate data to the required weekly ratios
"""

# === load data === #
import pandas as pd

dat = pd.read_csv('completeData.csv')

# fix the index
dat.index = pd.to_datetime(dat.hour)


# === aggregation === #
# aggregate within languages and across types
## non-mobile data
dat_nm = dat.query('type!="mw"').groupby(['language', 'hour'])
dat_nm = dat_nm.agg('sum')
## mobile data
dat_m = dat.query('type=="mw"')


# subset english
dat_nm_en = dat_nm.query('language=="en"')
dat_m_en = dat_m.query('language=="en"')

# fix indexfrom multiindex to just hourly index
dat_nm_en.index = pd.to_datetime(dat_nm_en.index.get_level_values(1))

# calculate the ratio
dat_ratio_en = dat_m_en.visits / (dat_m_en.visits + dat_nm_en.visits)

# aggregate to weekly data
# dat_nm_w = dat_nm.groupby(['language', lambda x: x.week]).mean()
# dat_m_w = dat_m.groupby(['language', lambda x: x.week]).mean()
dat_ratio_en_w = dat_ratio_en.groupby([lambda x: x.year, lambda x: x.week])\
                .mean()