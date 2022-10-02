import pandas as pd
import sqlalchemy
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+"/csv-to-rdb")
from df_to_rdb_util import store_dataframe_to_db 

current_dir = os.path.dirname(os.path.realpath(__file__))

table_name = "ranking_history"
df = pd.read_csv(f"{current_dir}/../data/db/kbo-ranking-history.csv", thousands = ',', encoding='utf-8')
df[f'{table_name}_id'] = df.index


dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer, 
        'year':sqlalchemy.types.Integer, 
          'team':sqlalchemy.types.VARCHAR(255), 
          'ranking':sqlalchemy.types.Integer
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)