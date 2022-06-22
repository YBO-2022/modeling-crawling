import requests
from bs4 import BeautifulSoup
import pandas as pd


team_lst = ["KIA","KT","LG","NC","SSG","두산","롯데","삼성","키움","한화"]
position_lst = ["좌익수","중견수","우익수","3루수","유격수","2루수","1루수","투수","포수","지명타자"]
df = pd.DataFrame(columns=["team","position","name"])

for team in team_lst:
    response = requests.get(f"http://www.statiz.co.kr/team.php?cteam={team}&year=2022&opt=0&sopt=0")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    for j, position in enumerate(position_lst):
        k = j+1
        if len(soup.select(f"body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(4) > div.box-body.no-padding > div > div:nth-child({k}) > a > span")) == 0:
            continue;
        else : 
            name = soup.select_one(f"body > div > div.content-wrapper > div > section.content > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(4) > div.box-body.no-padding > div > div:nth-child({k}) > a > span").find_all(text=True)[0]
            new_df = pd.DataFrame([[f"{team}",f"{position}",f"{name}"]], columns=["team","position","name"])
            df = pd.concat([df,new_df], ignore_index=True)


df.to_csv("./data/팀별주전.csv", header=True,index=False)


