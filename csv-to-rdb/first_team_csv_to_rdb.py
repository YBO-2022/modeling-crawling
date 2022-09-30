import time
import pandas as pd
import sqlalchemy
import os
from df_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{current_dir}/../data/db/first_team.csv", thousands = ',', encoding='utf-8')

table_name = "first_team"
df[f'{table_name}_id'] = df.index

dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer, 
          'team':sqlalchemy.types.VARCHAR(255), 
          'c':sqlalchemy.types.VARCHAR(255), 
          'cf':sqlalchemy.types.VARCHAR(255), 
          'dh':sqlalchemy.types.VARCHAR(255), 
          'fb':sqlalchemy.types.VARCHAR(255), 
          'lf':sqlalchemy.types.VARCHAR(255), 
          'p':sqlalchemy.types.VARCHAR(255), 
          'rf':sqlalchemy.types.VARCHAR(255), 
          'sb':sqlalchemy.types.VARCHAR(255), 
          'ss':sqlalchemy.types.VARCHAR(255), 
          'tb':sqlalchemy.types.VARCHAR(255), 
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)