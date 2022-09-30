import time
import pandas as pd
import sqlalchemy
import os
from csv_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{current_dir}/../data/input/preprocessed_ops.csv", encoding='utf-8', usecols=["name", "WAR+", "game수", "타석", "안타", "홈런", "타점", "도루", "삼진", "병살", "타율", "출루", "장타", "OPS", "year", "team", "position"])
df.columns = ['name', 'war', 'games', 'pa', 'hit', 'homerun', 'rbi', 'steal', 'strikeout', 'dp', 'ba', 'obp', 'slg', 'ops', 'year', 'team', 'position']
df = df.loc[(df['year'] == 22)]
df = df.drop(['year'], axis=1).reset_index(drop=True)

table_name = "hitter"
df[f'{table_name}_id'] = df.index

dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer, 
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255),
            'position': sqlalchemy.types.VARCHAR(20), 
            'war': sqlalchemy.types.Float,
            'games': sqlalchemy.types.Integer,
            'pa': sqlalchemy.types.Integer, #타석
            'hit': sqlalchemy.types.Integer,  #안타
            'homerun': sqlalchemy.types.Integer,
            'rbi': sqlalchemy.types.Integer,    #타점
            'steal': sqlalchemy.types.Integer,  #도루
            'strikeout': sqlalchemy.types.Integer,  #삼진
            'dp': sqlalchemy.types.Integer, #병살
            'ba': sqlalchemy.types.Float, #타율
            'obp': sqlalchemy.types.Float, #출루율
            'slg': sqlalchemy.types.Float, #장타율
            'ops': sqlalchemy.types.Float   #ops
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)