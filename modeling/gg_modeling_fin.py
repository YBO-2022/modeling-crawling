import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings(action='ignore')

gg_hit = pd.read_csv('//content/drive/Shareddrives/[2022-1 Ybigta] 타율 어쩌구 구단이 울랄라/모델링팀/최종/test_ops.csv', index_col=0)
gg_pit = pd.read_csv('/content/drive/Shareddrives/[2022-1 Ybigta] 타율 어쩌구 구단이 울랄라/모델링팀/최종/test_era.csv', index_col=0)

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
gg.to_csv('goldenglove.csv')

