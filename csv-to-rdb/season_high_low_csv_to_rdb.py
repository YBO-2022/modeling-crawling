import time
import pandas as pd
import sqlalchemy
import os
from csv_to_rdb_util import store_dataframe_to_db


current_dir = os.path.dirname(os.path.realpath(__file__))


df = pd.read_csv(f"{current_dir}/../data/db/season_high_low.csv", encoding='utf-8', usecols=["팀명", "시즌 최고", "시즌 최저"])
df.columns = ['team', 'season_high', 'season_low']
df['season_high_low_id'] = df.index


# DB 테이블 명
table_name = "season_high_low"

dtypesql = {'season_high_low_id': sqlalchemy.types.Integer,
            'team': sqlalchemy.types.VARCHAR(255),
            'season_high': sqlalchemy.types.Integer, 
            'season_low': sqlalchemy.types.Integer
}


# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)