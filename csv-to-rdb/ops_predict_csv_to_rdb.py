import time
import pandas as pd
import sqlalchemy
import os
from csv_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(f"{current_dir}/../data/output/predicted_ops.csv", encoding='utf-8', usecols=['name', 'team', 'OPS', 'prediction_OPS'])
df.columns = ['name', 'team' , 'ops', 'predict_ops']
df['ops_predict_id'] = df.index


# DB 테이블 명
table_name = "ops_predict"

dtypesql = {'ops_predict_id': sqlalchemy.types.Integer, 
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255), 
            'ops': sqlalchemy.types.Float,
            'predict_ops': sqlalchemy.types.Float
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)