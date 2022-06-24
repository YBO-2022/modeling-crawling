# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.ensemble import VotingRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error
from math import sqrt

import warnings
warnings.filterwarnings(action='ignore')

class OpsPredict:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, index_col=0)

    def preprocessing(self) :
        
        pre_data = (self.data)

        preprocessed_data = pre_data.set_index('name')
        '''
        encoder = LabelEncoder()
        
        col = ['team', 'position']

        for i in col:
            encoder.fit(preprocessed_data[i])
            preprocessed_data[i] = encoder.transform(preprocessed_data[i])
        
        #nan값 처리
        #preprocessed_data.loc[['전민수', '서상우'],['position']] = 5
        
        #preprocessed_data = pre_data.drop(['team', 'ERA+', 'FIP+', '완투', '완봉'], axis=1)
        '''
        return preprocessed_data

    def modeling(self):
        
        preprocessed_data = self.preprocessing()
        
        test_data = preprocessed_data[preprocessed_data.year==22]
        train_data = preprocessed_data[preprocessed_data.year != 22]

        test_team = test_data['team']
        train_team = train_data['team']

        X_train = train_data.drop(['OPS','year','team','position','도루','도실','희타','타석','wOBA','루타','삼루타','고의사구'], axis=1)
        y_train = train_data['OPS']
        X_test = test_data.drop(['OPS','year','team','position','도루','도실','희타','타석','wOBA','루타','삼루타','고의사구'], axis=1)
        y_test = test_data['OPS']
            
        scaler=RobustScaler()
        scaler.fit(X_train)
        X_scaled = scaler.transform(X_train)
        X_scaled = pd.DataFrame(data=X_scaled)
        X_scaled.columns=['WAR+', 'game수', '타수', '득점', '안타', '이루타', '홈런', '타점', '볼넷', '사구','삼진', '병살', '희비', '타율', '출루', '장타', 'wRC+', 'WPA']
        
        X_test_scaled = scaler.transform(X_test)
        X_test = pd.DataFrame(data=X_test_scaled)
        X_test.columns=['WAR+', 'game수', '타수', '득점', '안타', '이루타', '홈런', '타점', '볼넷', '사구','삼진', '병살', '희비', '타율', '출루', '장타', 'wRC+', 'WPA']
        
        xgb = XGBRegressor()
        gbr = GradientBoostingRegressor()
        ridge = Ridge()

        model = VotingRegressor([('gbr', gbr), ('xgb', xgb), ('ridge', ridge)])
        
        model.fit(X_scaled,y_train)
        y_pred =model.predict(X_test)

        print('RMSE = ', sqrt(mean_squared_error(y_pred, y_test)))
        print('R2 = ', r2_score(y_pred, y_test))

        result = pd.DataFrame(y_pred, index=y_test.index).rename(columns={0: 'prediction_OPS'})

        y_test = pd.concat([y_test, test_team], axis=1)
        result = pd.concat([y_test, result], axis=1)

        result = result.sort_values(['prediction_OPS'], ascending=False)
        result = result.reset_index()

        result = result[['name', 'team', 'OPS', 'prediction_OPS']]

        return result

Ops = OpsPredict('/Users/garam/Downloads/OPS_preprocessing_trade.csv')

data = Ops.modeling()
data.to_csv('predict_ops.csv')

