import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import sqlalchemy
import configparser
from dotenv import load_dotenv
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{current_dir}/../data/input/preprocessed_era.csv", usecols=["name", "WAR", "승", "패", "세이브", "홀드", "이닝", "실점", "자책", "피안타", "홈런", "볼넷", "삼진", "ERA", "year", "team"])
df.columns = ['name', 'war', 'win', 'lose', 'save', 'hold', 'inning', 'runs', 'earned_run', 'hit', 'homerun', 'bb', 'strikeout', 'era', 'year', 'team']
df = df.loc[(df['year'] == 22)]
df = df.drop(['year'], axis=1).reset_index(drop=True)
df['pitcher_id'] = df.index

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
table_name = "pitcher"

dtypesql = {'pitcher_id': sqlalchemy.types.Integer, 
            'name': sqlalchemy.types.VARCHAR(255), 
            'team': sqlalchemy.types.VARCHAR(255), 
            'war': sqlalchemy.types.Float,
            'win': sqlalchemy.types.Integer,
            'lose': sqlalchemy.types.Integer,
            'save': sqlalchemy.types.Integer,
            'hold': sqlalchemy.types.Integer,
            'inning': sqlalchemy.types.Float,
            'runs': sqlalchemy.types.Integer,
            'earned_run': sqlalchemy.types.Integer,
            'hit': sqlalchemy.types.Integer,
            'homerun': sqlalchemy.types.Integer,
            'bb': sqlalchemy.types.Integer,
            'strikeout': sqlalchemy.types.Integer,
            'era': sqlalchemy.types.Float,
            'wpa': sqlalchemy.types.Float
}

# DB에 DataFrame 적재
df.to_sql(index = False,
          name = table_name,
          con = engine,
          if_exists = 'replace',
          method = 'multi', 
          chunksize = 10000,
          dtype=dtypesql)

#with engine.connect() as con:
#    con.execute('ALTER TABLE `pitcher` ADD PRIMARY KEY (`pitcher_id`);')