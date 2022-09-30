from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pymysql


def get_engine():
    # get params by .env file
    load_dotenv()
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = 3306
    database = "ybo_db"

    # DB 접속 엔진 객체 생성
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', encoding='utf-8')
    return engine

# DB에 DataFrame 적재
def store_dataframe_to_db(df, table_name, dtypesql):
    engine = get_engine()
    df.to_sql(index = False,
          name = table_name,
          con = engine,
          if_exists = 'replace',
          method = 'multi', 
          chunksize = 10000,
          dtype=dtypesql)