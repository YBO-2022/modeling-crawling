import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import sqlalchemy
import configparser
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(f"{current_dir}/../data/output/predicted_ops.csv", encoding='utf-8', usecols=['name', 'team', 'OPS', 'prediction_OPS'])
df.columns = ['name', 'team' , 'ops', 'predict_ops']
df['ops_predict_id'] = df.index

# params
load_dotenv()
user = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = 3306
database = "ybo_db"


# DB 접속 엔진 객체 생성
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', encoding='utf-8')

# DB 테이블 명
table_name = "ops_predict"

dtypesql = {'ops_predict_id': sqlalchemy.types.Integer, 
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255), 
            'ops': sqlalchemy.types.Float,
            'predict_ops': sqlalchemy.types.Float
}

# DB에 DataFrame 적재
df.to_sql(index = False,
          name = table_name,
          con = engine,
          if_exists = 'replace',
          method = 'multi', 
          chunksize = 10000,
          dtype=dtypesql)

with engine.connect() as con:
    con.execute('ALTER TABLE `ops_predict` ADD PRIMARY KEY (`ops_predict_id`);')