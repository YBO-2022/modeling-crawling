import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+"/csv-to-rdb")
from df_to_rdb_util import store_dataframe_to_db 


def game():

    response = requests.get("https://sports.news.naver.com/kbaseball/schedule/index.nhn")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    score_list = []
    for i in range(1, 6):
        if not soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_lft > p > strong'):
            continue
        left_team = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_lft > p > strong').get_text()
        right_team = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_rgt > p > strong').get_text()
        left_pitcher = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_lft > p > span > a').get_text()
        right_pitcher = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_rgt > p > span > a').get_text()
        state = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_cnt > em').get_text().strip()
        if state == "취소":
            game_state = "경기 취소"
            left_score = " "
            right_score = " "
        elif ":" in state:
            game_state = " 시작 전"
            left_score = " "
            right_score = " "
        elif state == "종료":
            game_state = "경기 종료"
            left_score = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_lft > strong').get_text()
            right_score = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_rgt > strong').get_text()
        else:
            game_state = " 경기 중"
            left_score = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_lft > strong').get_text()
            right_score = soup.select_one(f'#todaySchedule > li:nth-child({i}) > div.vs_rgt > strong').get_text()

        score = {
            "game_state": game_state,
            "left_team": left_team,
            "right_team": right_team,
            "left_score": left_score,
            "right_score": right_score,
            "state": state,
            "left_pitcher": left_pitcher,
            "right_pitcher": right_pitcher
        }
        
        score_list.append(score)
    df = pd.DataFrame(score_list)

    table_name = "realtime_game"
    df[f'{table_name}_id'] = df.index

    dtypesql = {f'{table_name}_id': sqlalchemy.types.Integer,
                'game_state': sqlalchemy.types.VARCHAR(255),
                'left_team': sqlalchemy.types.VARCHAR(255),
                'right_team': sqlalchemy.types.VARCHAR(255),
                'left_score': sqlalchemy.types.VARCHAR(255),
                'right_score': sqlalchemy.types.VARCHAR(255),
                'draw_number': sqlalchemy.types.VARCHAR(255),
                'state': sqlalchemy.types.VARCHAR(255),
                'left_pitcher': sqlalchemy.types.VARCHAR(255),
                'right_pitcher': sqlalchemy.types.VARCHAR(255)
                }

    # DB에 DataFrame 적재
    store_dataframe_to_db(df, table_name, dtypesql)

n = time.localtime().tm_wday
if n != 1:
    game()