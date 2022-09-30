import time
import pandas as pd
import sqlalchemy
import os
from df_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))

df1 = pd.read_csv(f"{current_dir}/../data/input/preprocessed_era.csv", encoding='utf-8', usecols=["name", "WAR", "year", "team"])
df1.columns = ['name', 'war', 'year', 'team']
df1 = df1.loc[(df1['year'] == 22)]
df1 = df1.drop(['year'], axis=1).reset_index(drop=True)
df2 = pd.read_csv(f"{current_dir}/../data/input/preprocessed_ops.csv", encoding='utf-8', usecols=["name", "WAR+", "year", "team"])
df2.columns = ['name', 'war', 'year', 'team']
df2 = df2.loc[(df2['year'] == 22)]
df2 = df2.drop(['year'], axis=1).reset_index(drop=True)
df = pd.concat([df1,df2], ignore_index=True).reset_index(drop=True)

table_name = "war_list"
df[f'{table_name}_id'] = df.index

dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer, 
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255), 
            'war': sqlalchemy.types.Float
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)