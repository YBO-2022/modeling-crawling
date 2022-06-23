import requests
from bs4 import BeautifulSoup
import pandas as pd
import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()
conn = MySQLdb.connect(
    user=os.getenv('DB_USERNAME'),
    passwd=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    db="ybo_db"
    # charset="utf-8"
)
# type(conn): <class 'MySQLdb.connections.Connection'>

cursor = conn.cursor()
# type(cursor):  <class 'MySQLdb.cursors.Cursor'>

cursor.execute("DROP TABLE IF EXISTS first_team")
cursor.execute("""create table first_team (first_team_id bigint NOT NULL AUTO_INCREMENT, team varchar(255), C varchar(255), 1B varchar(255), 2B varchar(255), 3B varchar(255), SS varchar(255), 
                RF varchar(255), CF varchar(255), LF varchar(255), P varchar(255), DH varchar(255), PRIMARY KEY (first_team_id))""")


team_lst = ["KIA","KT","LG","NC","SSG","두산","롯데","삼성","키움","한화"]

position_dict = {
    "좌익수": "LF",
    "중견수": "CF",
    "우익수": "RF",
    "3루수": "3B",
    "2루수": "2B",
    "1루수": "1B",
    "유격수": "SS",
    "투수": "P",
    "포수": "C",
    "지명타자": "DH",    
}

position_lst = list(position_dict.keys())
l = position_lst
p = position_dict

for team in team_lst:
    response = requests.get(f"http://www.statiz.co.kr/team.php?cteam={team}&year=2022&opt=0&sopt=0")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    first_team_dict = {}

    for j, position in enumerate(position_lst):
        k = j+1
        if len(soup.select(f"body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(4) > div.box-body.no-padding > div > div:nth-child({k}) > a > span")) == 0:
            name = None
        else : 
            name = soup.select_one(f"body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(4) > div.box-body.no-padding > div > div:nth-child({k}) > a > span").find_all(text=True)[0]
        first_team_dict[position] = name
    f = first_team_dict

    if (team=="KT"):
        team = team.lower()

    cursor.execute(f"""INSERT INTO first_team (team, C, 1B, 2B, 3B, SS, RF, CF, LF, P, DH) VALUES ('{team}', '{f[l[0]]}', '{f[l[1]]}', '{f[l[2]]}', '{f[l[3]]}', '{f[l[4]]}', '{f[l[5]]}', '{f[l[6]]}', '{f[l[7]]}', '{f[l[8]]}',  '{f[l[9]]}')""")

conn.commit()
conn.close()
print("Finish First Team Crawling!")