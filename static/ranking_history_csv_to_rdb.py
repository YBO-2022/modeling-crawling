import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import sqlalchemy
import configparser
from dotenv import load_dotenv
import os


current_dir = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{current_dir}/../data/db/kbo-ranking-history.csv", thousands = ',', encoding='utf-8')
df['ranking_history_id'] = df.index

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
table_name = "ranking_history"

dtypesql = {'ranking_history_id': sqlalchemy.types.Integer, 
        'year':sqlalchemy.types.Integer, 
          'team':sqlalchemy.types.VARCHAR(255), 
          'ranking':sqlalchemy.types.Integer
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
    con.execute('ALTER TABLE `ranking_history` ADD PRIMARY KEY (`ranking_history_id`);')
