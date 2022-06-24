
import pandas as pd
import numpy as np

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from math import sqrt

from sklearn.ensemble import VotingRegressor
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold
import os
import warnings
warnings.filterwarnings(action='ignore')


current_dir = os.path.dirname(os.path.realpath(__file__))
kbo_data = pd.read_csv(f'{current_dir}/../data/input/team.csv',encoding='utf-8')
statiz_batter = pd.read_csv(f'{current_dir}/../data/input/team_hitter.csv',encoding='utf-8')
statiz_pitcher = pd.read_csv(f'{current_dir}/../data/input/team_pitcher.csv',encoding='utf-8')


statiz_pitcher.rename(columns = {'순 이름 팀 정렬\n출장\n완투\n완봉\n선발\n승\n패\n세\n홀드\n이닝\n실점\n자책\n타자\n안타\n2타\n3타\n홈런\n볼넷\n고4\n사구\n삼진\n보크\n폭투\n비율\nWAR\nWPA':'pre'},inplace=True)

def preprocessing(data):
    col = ['순서','team', 'year', 'WAR', '출장', '완투', '완봉', '선발', '승', '패', '세이브', '홀드', '이닝', '실점', '자책', '타자', '피안타', '이루타', '삼루타', '홈런', '볼넷', '고의사구','사구', '삼진', '보크', '폭투', 'ERA', 'FIP', 'WHIP', 'ERA+', 'FIP+', 'WAR2','WPA']

    for i in range(0, len(col)):
        data[col[i]] = data.pre.str.split(' ').str[i]


    data.isnull().sum()
    data = data.dropna()
    data = data.drop(['pre', '순서'], axis=1)
    data = data.reset_index()
    data = data.drop(['index'], axis=1)

    for i in data.columns[4:] :
        data[i] = pd.to_numeric(data[i])

    return data

statiz_pitcher = preprocessing(statiz_pitcher)
statiz_pitcher.drop(['WAR2'],axis=1,inplace=True)

statiz_batter.rename(columns = {'순 이름 팀 정렬\nG\n타석\n타수\n득점\n안타\n2타\n3타\n홈런\n루타\n타점\n도루\n도실\n볼넷\n사구\n고4\n삼진\n병살\n희타\n희비\n비율\nWAR*\nWPA':'pre'},inplace=True)

def preprocessing2(data):
    col = ['순서','team', 'year', 'WAR', '출장', '타석', '타수', '득점', '안타', '2루타', '3루타', '홈런', '루타', '타점', '도루', '도실', '볼넷', '사구', '고의사구', '삼진', '병살', '희타','희비', '타율', '출루율', '장타율', 'OPS', 'wOBA', 'wRC+', 'WAR2','WPA']

    for i in range(0, len(col)):
        data[col[i]] = data.pre.str.split(' ').str[i]


    data.isnull().sum()
    data = data.dropna()
    data = data.drop(['pre', '순서'], axis=1)
    data = data.reset_index()
    data = data.drop(['index'], axis=1)

    for i in data.columns[4:] :
        data[i] = pd.to_numeric(data[i])

    return data

statiz_batter = preprocessing2(statiz_batter)

statiz_batter.drop(['WAR2'],axis=1,inplace=True)

kbo_data.rename(columns = {'2020 경기 승 패 무 타율 평균자책점 승률' :'pre'},inplace=True)

col = ['team', 'name', '경기', '승', '패', '무', '타율', '평균자책점', '승률']

for i in range(0, len(col)):
    kbo_data[col[i]] = kbo_data.pre.str.split(' ').str[i]

kbo_data.drop(['pre'],axis=1,inplace=True)

kbo_data = kbo_data.drop([10, 21, 32, 43, 54, 65, 76], axis=0)
kbo_data.drop(['name'],axis=1,inplace=True)
kbo_data.head()

kbo = np.split(kbo_data, 8)

kbo[0]['year']=20
kbo[1]['year']=21
kbo[2]['year']=22
kbo[3]['year']=15
kbo[4]['year']=16
kbo[5]['year']=17
kbo[6]['year']=18
kbo[7]['year']=19

for i in range(0,8):
    kbo[i] = kbo[i].reset_index()
    kbo[i].index=kbo[i].index + 1
    kbo[i] = kbo[i].reset_index()
    kbo[i] = kbo[i].drop(['index'], axis=1)
    kbo[i].rename(columns = {'level_0' :'rank'},inplace=True)

result = kbo[0]
for i in range(1,8):
    result = pd.concat([result, kbo[i]], axis=0)
kbo = result

statiz_batter.rename(columns = {'WAR' :'타자WAR'},inplace=True)
statiz_batter.rename(columns = {'WPA' :'타자WPA'},inplace=True)
statiz_batter.rename(columns = {'삼진' :'피삼진'},inplace=True)

statiz_pitcher.rename(columns = {'WAR' :'투수WAR'},inplace=True)
statiz_pitcher.rename(columns = {'WPA' :'투수WPA'},inplace=True)
statiz_pitcher.rename(columns = {'승' :'선발승'},inplace=True)
statiz_pitcher.rename(columns = {'패' :'선발패'},inplace=True)
statiz_pitcher.rename(columns = {'안타' :'피안타'},inplace=True)
statiz_pitcher.rename(columns = {'홈런' :'피홈런'},inplace=True)
statiz_pitcher.rename(columns = {'볼넷' :'볼넷허용'},inplace=True)

statiz_batter = statiz_batter[['team', 'year','타자WAR', '안타', '2루타', '홈런', '타점', '볼넷', '피삼진', '병살', '타율', 'OPS', 'wOBA', 'wRC+', '타자WPA']]
statiz_pitcher = statiz_pitcher[['team', 'year','투수WAR', '선발승', '선발패', '세이브', '실점', '자책', '피안타', '피홈런', '볼넷허용', '삼진', 'ERA', 'FIP', 'WHIP', '투수WPA']]
kbo = kbo[['team', 'year', '승', '패', '승률', 'rank']]

statiz_batter = statiz_batter.replace('kt','KT')
statiz_pitcher = statiz_pitcher.replace('kt','KT')
kbo = kbo.replace('kt','KT')

statiz_batter = statiz_batter.replace('SK','SSG')
statiz_pitcher = statiz_pitcher.replace('SK','SSG')
kbo = kbo.replace('SK','SSG')

dataset= pd.merge(left=statiz_batter, right=statiz_pitcher, how='left', on=['team', 'year'], sort=False, suffixes=(" ", " "))
dataset.loc[:,'year'] = pd.to_numeric(dataset.loc[:,'year'])
dataset= pd.merge(left=dataset, right=kbo, how='left', on=['team', 'year'], sort=False, suffixes=(" ", " "))

dataset.dtypes
dataset.loc[:,'타자WAR'] = pd.to_numeric(dataset.loc[:,'타자WAR'])
dataset.loc[:,'투수WAR'] = pd.to_numeric(dataset.loc[:,'투수WAR'])
dataset.loc[:,'승'] = pd.to_numeric(dataset.loc[:,'승'])
dataset.loc[:,'패'] = pd.to_numeric(dataset.loc[:,'패'])
dataset.loc[:,'승률'] = pd.to_numeric(dataset.loc[:,'승률'])
dataset.loc[:,'rank'] = pd.to_numeric(dataset.loc[:,'rank'])

class RankPredict:
    def __init__(self, data):
        self.data = data

    def preprocessing(self) :
        
        pre_data = (self.data)

        preprocessed_data = pre_data.drop(['FIP', '선발승','선발패','자책','피안타','피홈런','삼진','병살','타자WPA','투수WPA','안타','2루타','wOBA','타율','승', '패','rank'], axis=1)

        return preprocessed_data

    def modeling(self):
        
        preprocessed_data = self.preprocessing()

        test = preprocessed_data[preprocessed_data.year==22]
        preprocessed_data = preprocessed_data[preprocessed_data.year != 22]
        
        test = test.drop(['year'], axis=1)
        preprocessed_data = preprocessed_data.drop(['year'], axis=1)
        
        test_team = test['team']
        preprocessed_data_team = preprocessed_data['team']

        test = test.drop(['team'], axis=1)
        preprocessed_data = preprocessed_data.drop(['team'], axis=1)
        
        X = preprocessed_data.drop('승률', axis=1)
        y = preprocessed_data['승률']
        X_test = test.drop('승률', axis=1)
        y_test = test['승률']
                    
        scaler = StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)
        X_test = scaler.transform(X_test)

        model = VotingRegressor([('knn', KNeighborsRegressor()),('xgb', XGBRegressor()),('ridge', Ridge())])
        #model = VotingRegressor([('ada', AdaBoostRegressor()),('bc', BaggingRegressor()),('gbc', GradientBoostingRegressor()),('rfc', RandomForestRegressor()),('knn', KNeighborsRegressor()),('svc', SVR()),('xgb', XGBRegressor()),('lgbm', LGBMRegressor()),('ridge', Ridge()),('dt', DecisionTreeRegressor())])
        
        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)
        soft_vote_cv = cross_validate(model, X, y, cv=k_fold)
        model.fit(X, y)

        y_pred = model.predict(X_test)

        result = pd.DataFrame(y_pred, index=y_test.index).rename(columns={0: 'prediction_Rank'})

        print('RMSE = ', sqrt(mean_squared_error(y_pred, y_test)))

        #컬럼 합치기
        y_test = pd.concat([y_test, test_team], axis=1)
        result = pd.concat([y_test, result], axis=1)

        result = result.sort_values('prediction_Rank', ascending=False)
        result = result.reset_index()

        result = result[['team', '승률', 'prediction_Rank']]
        result

        return result

Rank = RankPredict(dataset)

data = Rank.modeling()
data.to_csv(f'{current_dir}/../data/output/predicted_team_ranking.csv')

