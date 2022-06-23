
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os
import pymysql
from datetime import datetime

def ranking():
    # 환경 변수 설정
    load_dotenv()
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = 3306
    database = "ybo_db"

    now = datetime.now()
    table_name = f"realtime_ranking_{now.minute}"

    rank_list = []
    response = requests.get(f'https://sports.news.naver.com/kbaseball/record/index?category=kbo')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    for i in range(10):
        k = i + 1
        ranking = soup.select("#regularTeamRecordList_table > tr >th > strong")[i].get_text()
        team = soup.select("#regularTeamRecordList_table > tr > td > div > span.emblem")[
            i].next_sibling.next_sibling.get_text()
        game = soup.select_one(f'#regularTeamRecordList_table > tr:nth-child({k}) > td:nth-child(3) > span').get_text()
        win = soup.select_one(f'#regularTeamRecordList_table > tr:nth-child({k}) > td:nth-child(4) > span').get_text()
        lose = soup.select_one(f'#regularTeamRecordList_table > tr:nth-child({k}) > td:nth-child(5) > span').get_text()
        draw = soup.select_one(f'#regularTeamRecordList_table > tr:nth-child({k}) > td:nth-child(6) > span').get_text()
        winRate = soup.select_one(f'#regularTeamRecordList_table > tr:nth-child({k}) > td:nth-child(7) > strong').get_text()
        gameDiff = soup.select_one(f'#regularTeamRecordList_table > tr:nth-child({k}) > td:nth-child(8) > span').get_text()
        continuity = soup.select_one(f'#regularTeamRecordList_table > tr:nth-child({k}) > td:nth-child(9) > span').get_text()
        rank_dict = {"ranking": ranking,
                        "team": team,
                        "game_number": game,
                        "win_number": win,
                        "lose_number": lose,
                        "draw_number": draw,
                        "win_rate": winRate,
                        "game_diff": gameDiff,
                        "continuity": continuity
                        }
        rank_list.append(rank_dict)
    df = pd.DataFrame(rank_list)

    df[f'{table_name}_id'] = df.index

    # DB 접속 엔진 객체 생성
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}', encoding='utf-8')

    # DB 테이블 명


    dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer,
                'ranking': sqlalchemy.types.Integer,
                'team': sqlalchemy.types.VARCHAR(255),
                'game_number': sqlalchemy.types.Integer,
                'win_number': sqlalchemy.types.Integer,
                'lose_number': sqlalchemy.types.Integer,
                'draw_number': sqlalchemy.types.Integer,
                'win_rate': sqlalchemy.types.Float,
                'game_diff': sqlalchemy.types.Float,
                'continuity': sqlalchemy.types.VARCHAR(255),
                }

    # DB에 DataFrame 적재
    df.to_sql(index=False,
                name=table_name,
                con=engine,
                if_exists='replace',
                method='multi',
                chunksize=10000,
                dtype=dtypesql)

    with engine.connect() as con:
        con.execute(f'ALTER TABLE `{table_name}` ADD PRIMARY KEY (`{table_name}_id`);')

ranking()