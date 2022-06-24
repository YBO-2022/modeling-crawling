import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings(action='ignore')

import os

current_dir = os.path.dirname(os.path.realpath(__file__))

gg_hit = pd.read_csv(f'{current_dir}/../data/input/preprocessed_ops.csv', index_col=0)
gg_pit = pd.read_csv(f'{current_dir}/../data/input/preprocessed_era.csv', index_col=0)

gg_hit = gg_hit[gg_hit.year==22]
gg_hit = gg_hit.drop(['year'], axis=1)
gg_hit = gg_hit[['position','name', 'team', 'WAR+']]
gg_hit.rename(columns = {'WAR+':'WAR'},inplace=True)

gg_pit = gg_pit[gg_pit.year==22]
gg_pit = gg_pit.drop(['year'], axis=1)
gg_pit = gg_pit[['name', 'team', 'WAR']]
gg_pit['position'] = 'P'

gg = pd.concat([gg_hit, gg_pit])

gg = gg.loc[gg.groupby(['position'])['WAR'].idxmax()]
gg = gg.set_index('position')
gg.to_csv(f'{current_dir}/../data/output/goldenglove.csv')

