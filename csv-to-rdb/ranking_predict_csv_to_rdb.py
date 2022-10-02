import time
import pandas as pd
import sqlalchemy
import os
from df_to_rdb_util import store_dataframe_to_db

current_dir = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{current_dir}/../data/output/predicted_team_ranking.csv", encoding='utf-8', usecols=["team", "승률", "prediction_Rank"])
df.columns = ['team', 'win_rate', 'predict_win_rate']

table_name = "ranking_predict"
df[f'{table_name}_id'] = df.index

dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer,
            'team': sqlalchemy.types.VARCHAR(255),
            'win_rate': sqlalchemy.types.Float,
            'predict_win_rate': sqlalchemy.types.Float
}

# DB에 DataFrame 적재
store_dataframe_to_db(df, table_name, dtypesql)