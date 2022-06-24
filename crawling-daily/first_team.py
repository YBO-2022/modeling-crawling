import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import warnings
warnings.filterwarnings(action='ignore')
team_lst = ["KIA","KT","LG","NC","SSG","두산","롯데","삼성","키움","한화"]
position_lst = ["좌익수","중견수","우익수","3루수","유격수","2루수","1루수","투수","포수","지명타자"]
df = pd.DataFrame(columns=["team","c","cf", "dh", "fb", "lf", "p", "rf", "sb", "ss", "tb"])

position_dict = {
    "좌익수": "lf",
    "중견수": "cf",
    "우익수": "rf",
    "3루수": "tb",
    "2루수": "sb",
    "1루수": "fb",
    "유격수": "ss",
    "투수": "p",
    "포수": "c",
    "지명타자": "dh",    
}


result = list()
for i in range(len(team_lst)):
    team = team_lst[i]
    response = requests.get(f"http://www.statiz.co.kr/team.php?cteam={team}&year=2022&opt=0&sopt=0")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    team_dict={}
    for j in range(len(position_lst)):
        position=position_lst[j]
        k = j+1
        if len(soup.select(f"body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(4) > div.box-body.no-padding > div > div:nth-child({k}) > a > span")) == 0:
            name = "None"
        else : 
            name = soup.select_one(f"body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(4) > div.box-body.no-padding > div > div:nth-child({k}) > a > span").find_all(text=True)[0]
        team_dict[position_dict[position]]=name
    team_dict['team']=team
    df=df.append(team_dict, ignore_index=True)


current_dir = os.path.dirname(os.path.realpath(__file__))
df.to_csv(f"{current_dir}/../data/db/first_team.csv", header=True,index=False)