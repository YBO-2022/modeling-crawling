# -*- coding: utf-8 -*-


import pandas as pd
import os

"""## KT 없는데이터 가지고 전처리"""
current_dir = os.getcwd()
no_sk_kt = pd.read_csv(f'{current_dir}/../data-example/투수(kt,sk제외).csv', encoding='cp949')
yes_sk = pd.read_csv(f'{current_dir}/../data-example/투수sk.csv', encoding='cp949')
yes_kt = pd.read_csv(f'{current_dir}/../data-example/투수kt.csv', encoding='cp949')


# no_sk_kt = pd.read_csv(f'{current_dir}/../data/pitcher_except_sk_kt.csv', encoding='cp949')
# yes_sk = pd.read_csv(f'{current_dir}/../data/pitcher_sk.csv', encoding='cp949')
# yes_kt = pd.read_csv(f'{current_dir}/../data/pitcher_kt.csv', encoding='cp949')


data = pd.concat([no_sk_kt, yes_sk])
data.rename(columns = {'순 이름 팀 정렬\n출장\n완투\n완봉\n선발\n승\n패\n세\n홀드\n이닝\n실점\n자책\n타자\n안타\n2타\n3타\n홈런\n볼넷\n고4\n사구\n삼진\n보크\n폭투\n비율\nWAR\nWPA':'pre'},inplace=True)
print(data.info())

def preprocessing(data):
    col = ['순서','name', 'year', 'team', 'WAR', '출장', '완투', '완봉', '선발', '승', '패', '세이브', '홀드', '이닝', '실점', '자책', '타자', '피안타', '이루타', '삼루타', '홈런', '볼넷', '고의사구','사구', '삼진', '보크', '폭투', 'ERA', 'FIP', 'WHIP', 'ERA+', 'FIP+', 'WPA']

    for i in range(0, len(col)):
        if(i==0) or (i==1):
            data[col[i]] = data.pre.str.split(' ').str[i]
        elif(i==2)or(i==3) :
            data[col[i]] = data.pre.str.split(' ').str[2]
        else :
            data[col[i]] = data.pre.str.split(' ').str[i-1]

    data.isnull().sum()
    data = data.dropna()
    data = data.drop(['pre', '순서'], axis=1)
    data = data.reset_index()
    data = data.drop(['index'], axis=1)

    for i in data.columns[4:] :
        data[i] = pd.to_numeric(data[i])

    # ex) 18두LF -> 18, 두, LF 로 나누기
    for i in range(0, len(data)) :
        str = data.year[i]
        data.year[i] = str[0:2] # year에 연도 저장
        data.team[i] = str[2] # team에 한글자 팀 저장

    return data

data = preprocessing(data)

team_name = ['SSG', '삼성', 'NC', '한화', 'LG', '롯데', 'KIA', '두산', '키움']
team_short_name = ['S', '삼', 'N', '한', 'L', '롯', 'K', '두', '키']

for i in range(0,9):
    data = data.replace(team_short_name[i], team_name[i])

"""## KT 포함 전처리"""

yes_kt.rename(columns = {'순 이름 팀 정렬\n출장\n완투\n완봉\n선발\n승\n패\n세\n홀드\n이닝\n실점\n자책\n타자\n안타\n2타\n3타\n홈런\n볼넷\n고4\n사구\n삼진\n보크\n폭투\n비율\nWAR\nWPA':'pre'},inplace=True)
yes_kt = preprocessing(yes_kt)
yes_kt = yes_kt.replace('K','KT')
dataset = pd.concat([data, yes_kt])
dataset = dataset.reset_index()
dataset = dataset.drop(['index'], axis=1)

"""## KT 있는거 없는거 합치기"""

dataset = pd.concat([data, yes_kt])
dataset = dataset.reset_index()
dataset = dataset.drop(['index'], axis=1)
dataset.to_csv(f'{current_dir}/../data/preprocessed_ops.csv')

'''#현재 OPS 페이지에 올릴 새로운 데이터프레임
data2022 : 선수별 페이지 22년 OPS 랭킹
era : preprocessed_era

data2022 = dataset[dataset.year=='22']
data2022.to_csv('era2022.csv')
dataset = data2022[['name', 'year','team', 'ERA', 'WAR', '승', '패', '이닝', '실점', '자책','피안타','홈런', '볼넷', '삼진']]
dataset = dataset.sort_values('ERA')
dataset = dataset.drop(['year'], axis=1)
dataset.to_csv('era.csv')
'''

