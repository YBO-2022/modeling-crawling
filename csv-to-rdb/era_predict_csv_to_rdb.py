import time
import pandas as pd
import sqlalchemy
import os
from csv_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{current_dir}/../data/output/predicted_era.csv", encoding='utf-8', usecols=['name', 'team', 'ERA', 'prediction_ERA'])
df.columns = ['name', 'team' , 'era', 'predict_era']

# DB 테이블 명
table_name = "era_predict"
df[f'{table_name}_id'] = df.index

dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer, 
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255), 
            'era': sqlalchemy.types.Float,
            'predict_era': sqlalchemy.types.Float
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)