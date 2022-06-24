# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings(action='ignore')

gg_hit = pd.read_csv('/Users/garam/Desktop/KBO_modeling/OPS_preprocessing_trade.csv', index_col=0)
gg_pit = pd.read_csv('/Users/garam/Desktop/KBO_modeling/preprocessed_era.csv', index_col=0)

gg_hit = gg_hit[gg_hit.year==22]
gg_hit = gg_hit.drop(['year'], axis=1)
gg_hit = gg_hit.iloc[:, :4]
gg_hit.rename(columns = {'WAR+':'WAR'},inplace=True)

gg_pit = gg_pit[gg_pit.year==22]
gg_pit = gg_pit.drop(['year'], axis=1)
gg_pit = gg_pit.iloc[:, :3]
gg_pit['position'] = 'P'

gg = pd.concat([gg_hit, gg_pit])

gg = gg.loc[gg.groupby(['position'])['WAR'].idxmax()]
gg = gg.set_index('position')
gg.to_csv('goldenGlove.csv')