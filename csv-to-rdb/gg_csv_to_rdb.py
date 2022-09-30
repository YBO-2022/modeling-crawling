import time
import pandas as pd
import sqlalchemy
import os
from df_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{current_dir}/../data/output/predicted_goldenglove.csv", encoding='utf-8', usecols=["position", "name", "team"])
df.columns = ['position', 'name', 'team']

table_name = "squad_predict"
df[f'{table_name}_id'] = df.index

dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer,
            'position': sqlalchemy.types.VARCHAR(255),
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255)
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)