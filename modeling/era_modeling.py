# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import RobustScaler
from xgboost import XGBRegressor
from sklearn.ensemble import VotingRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from math import sqrt
import os


import warnings
warnings.filterwarnings(action='ignore')

class EraPredict:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, index_col=0)

    def preprocessing(self) :
        
        pre_data = (self.data)

        pre_data = pre_data.set_index('name')

        preprocessed_data = pre_data.drop(['ERA+', 'FIP+', '완투', '완봉','보크','이닝','타자','고의사구','세이브','홀드'], axis=1)

        return preprocessed_data

    def modeling(self):
        
        preprocessed_data = self.preprocessing()

        test = preprocessed_data[preprocessed_data.year==22]
        preprocessed_data = preprocessed_data[preprocessed_data.year != 22]
        
        test_team = test['team']
        preprocessed_data_team = preprocessed_data['team']

        test = test.drop(['team'], axis=1)
        preprocessed_data = preprocessed_data.drop(['team'], axis=1)

        xgb = XGBRegressor()
        gbr = GradientBoostingRegressor()
        ridge = Ridge()

        model = VotingRegressor([('gbr', gbr), ('xgb', xgb), ('ridge', ridge)])
        
        X = preprocessed_data.drop('ERA', axis=1)
        y = preprocessed_data['ERA']
        X_test = test.drop('ERA', axis=1)
        y_test = test['ERA']
            
        scaler = RobustScaler()
        scaler.fit(X)
        X = scaler.transform(X)
        X_test = scaler.transform(X_test)

        model.fit(X,y)
        #y_pred_valid = model.predict(X_valid)

        y_pred = model.predict(X_test)

        result = pd.DataFrame(y_pred, index=y_test.index).rename(columns={0: 'prediction_ERA'})
        
        print('RMSE = ', sqrt(mean_squared_error(y_pred, y_test)))
        print('R2 = ', r2_score(y_pred, y_test))

        y_test = pd.concat([y_test, test_team], axis=1)
        result = pd.concat([y_test, result], axis=1)

        result = result.sort_values('prediction_ERA')
        result = result.reset_index()

        result = result[['name', 'team', 'ERA', 'prediction_ERA']]

        return result

current_dir = os.path.dirname(os.path.realpath(__file__))
ERA = EraPredict(f'{current_dir}/../data/input/preprocessed_era.csv')

data = ERA.modeling()
data

data.to_csv(f'{current_dir}/../data/output/predicted_era.csv')

