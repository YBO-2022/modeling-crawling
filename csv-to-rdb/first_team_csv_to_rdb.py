import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import sqlalchemy
import configparser
from dotenv import load_dotenv
import os

table_name = "first_team"

current_dir = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(f"{current_dir}/../data/db/first_team.csv", thousands = ',', encoding='utf-8')
df[f'{table_name}_id'] = df.index

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
df.to_sql(index = False,
          name = table_name,
          con = engine,
          if_exists = 'replace',
          method = 'multi', 
          chunksize = 10000,
          dtype=dtypesql)

#with engine.connect() as con:
#    con.execute(f'ALTER TABLE `{table_name}` ADD PRIMARY KEY (`{table_name}_id`);')
