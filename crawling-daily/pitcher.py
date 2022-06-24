import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

team_lst = ["KIA","kt","LG","NC","SSG","SK", "두산","롯데","삼성","키움","한화"]


def remove_tag(content, team):
    cleanr =re.compile('<.*?>')
    cleantext_1 = re.sub(cleanr, '', content)
    cleantext_2 = cleantext_1.replace("순\n이름\n팀\n정렬출장완투완봉선발승패세홀드이닝실점자책타자안타2타3타홈런볼넷고4사구삼진보크폭투비율WARWPA\n\nWARERAFIPWHIPERA+FIP+"," ")
    cleantext_3 = cleantext_2.replace(" -->\n -->", " ")
    cleantext_4 = cleantext_3.strip()
    if(team=="KIA") :
        cleantext_5 = cleantext_4.replace("K", "K")
        return cleantext_5
    elif (team == "kt") :
        cleantext_5 = cleantext_4.replace("K","k")
        return cleantext_5
    else :
        return cleantext_4
th = ["ranking","name","season_team", "war","choolzhang","wanto","sonbal","win","loose","save","hold","inning","silzeom","zachaeck","taza","anta","2hit","3hit","homerun","ballfour","gofour","sagu", "samzin","vok","poktu","era","fip","whip","whip","wra+","fip+","war","wpa"]
result = list()


for i in range(len(team_lst)):
    response = requests.get(f"http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=1&ys=2018&ye=2022&se=0&te={team_lst[i]}&tm=&ty=0&qu=75&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR&o2=OutCount&de=1&lr=0&tr=&cv=&ml=1&sn=100&si=&cn=")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    table= soup.find_all("table")[0]
    text = remove_tag(str(table), team_lst[i])
    ten_players = text.split('\n')

    for st in ten_players:
        lst = st.split()
        list_len = len(lst)
        col = 31

        for i in range(list_len//col):
            d = {}
            s = lst[i*col]
            tmp = ""
            while s[0].isdigit():
                tmp = tmp + s[0]
                s = s[1:]
            d[th[0]]=tmp
            tmp = ""
            while not s[0].isdigit():
                tmp = tmp + s[0]      
                s = s[1:]
            d[th[1]] =tmp
            d[th[2]]=s
            for k in range(3, len(th)):
                d[th[k]]=lst[i*col+k-2]
            result.append(d)



current_dir = os.getcwd()
df = pd.DataFrame.from_dict(result, orient='columns')
df.to_csv(f"{current_dir}/../data/input/pitcher.csv", encoding="utf-8")