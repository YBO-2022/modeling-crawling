import time
import pandas as pd
import sqlalchemy
import os
from csv_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))


df = pd.read_csv(f"{current_dir}/../data/output/predicted_goldenglove.csv", encoding='utf-8', usecols=["position", "name", "team"])
df.columns = ['position', 'name', 'team']
df['squad_predict_id'] = df.index


# DB 테이블 명
table_name = "squad_predict"

dtypesql = {'squad_predict_id': sqlalchemy.types.Integer,
            'position': sqlalchemy.types.VARCHAR(255),
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255)
}


# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)