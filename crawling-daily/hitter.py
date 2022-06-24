import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

team_lst = ["KIA","kt","LG","NC","SSG","SK", "두산","롯데","삼성","키움","한화"]


def remove_tag(content, team):
    cleanr =re.compile('<.*?>')
    cleantext_1 = re.sub(cleanr, '', content)
    cleantext_2 = cleantext_1.replace("순\n이름\n팀\n정렬G타석타수득점안타2타3타홈런루타타점도루도실볼넷사구고4삼진병살희타희비비율WAR*WPA\n\nWAR*타율출루장타OPSwOBAwRC+"," ")
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

th = ["ranking","name","season_team_position", "war","score","hit","2hit","3hit","homerun","ruta","tazeom","doru","dosil","ballfour","sagu","gofour","samzin","beongsal","heeta","teebi","tayul","choolru", "zhangta","ops","woba","wrc+","wpa"]
result = list()

for i in range(len(team_lst)):
    response = requests.get(f"http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2018&ye=2022&se=0&te={team_lst[i]}&tm=&ty=0&qu=50&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&pa=0&si=&cn=&sn=100")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    table= soup.find_all("table")[0]
    text = remove_tag(str(table), team_lst[i])
    ten_players = text.split('\n')
    for st in ten_players:

        lst = st.split()
        list_len = len(lst)
        col = 29

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
df.to_csv(f"{current_dir}/../data/input/hitter.csv", encoding="utf-8")
