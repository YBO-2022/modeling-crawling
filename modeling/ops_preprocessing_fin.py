# -*- coding: utf-8 -*-

import pandas as pd

"""## KT 없는데이터 가지고 전처리"""

no_sk_kt = pd.read_csv('/content/drive/Shareddrives/[2022-1 Ybigta] 타율 어쩌구 구단이 울랄라/스탯티즈 크롤링/타자(kt,sk제외).csv', encoding='cp949')
yes_sk = pd.read_csv('/content/drive/Shareddrives/[2022-1 Ybigta] 타율 어쩌구 구단이 울랄라/스탯티즈 크롤링/타자sk.csv', encoding='cp949')

data = pd.concat([no_sk_kt, yes_sk])
data.rename(columns = {'순 이름 팀 정렬\nG\n타석\n타수\n득점\n안타\n2타\n3타\n홈런\n루타\n타점\n도루\n도실\n볼넷\n사구\n고4\n삼진\n병살\n희타\n희비\n비율\nWAR*\nWPA':'pre'},inplace=True)

def preprocessing(data):
    col = ['순서','name', 'year', 'team', 'position', 'WAR+', 'game수', '타석', '타수', '득점', '안타', '이루타', '삼루타', '홈런', '루타', '타점', '도루', '도실', '볼넷', '사구', '고의사구', '삼진', '병살', '희타','희비', '타율', '출루', '장타', 'OPS', 'wOBA', 'wRC+', 'WAR2','WPA']

    for i in range(0, len(col)):
        if(i==0) or (i==1):
            data[col[i]] = data.pre.str.split(' ').str[i]
        elif(i==2)or(i==3)or(i==4) :
            data[col[i]] = data.pre.str.split(' ').str[2]
        else :
            data[col[i]] = data.pre.str.split(' ').str[i-2]

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
        data.position[i] = str[3:] # position에 포지션 저장

    return data

data = preprocessing(data)
data = data.drop(['WAR2'], axis=1)

team_name = ['SSG', '삼성', 'NC', '한화', 'LG', '롯데', 'KIA', '두산', '키움']
team_short_name = ['S', '삼', 'N', '한', 'L', '롯', 'K', '두', '키']

for i in range(0,9):
    data = data.replace(team_short_name[i], team_name[i])

"""## KT 포함 전처리"""

yes_kt = pd.read_csv('/content/drive/Shareddrives/[2022-1 Ybigta] 타율 어쩌구 구단이 울랄라/스탯티즈 크롤링/타자kt.csv', encoding='cp949')

yes_kt.rename(columns = {'순 이름 팀 정렬\nG\n타석\n타수\n득점\n안타\n2타\n3타\n홈런\n루타\n타점\n도루\n도실\n볼넷\n사구\n고4\n삼진\n병살\n희타\n희비\n비율\nWAR*\nWPA':'pre'},inplace=True)
yes_kt = preprocessing(yes_kt)
yes_kt = yes_kt.drop(['WAR2'], axis=1)
yes_kt = yes_kt.replace('K','KT')


"""## KT 있는거 없는거 합치기"""

dataset = pd.concat([data, yes_kt])
dataset = dataset.reset_index()
dataset = dataset.drop(['index'], axis=1)
dataset.to_csv('preprocessed_ops.csv')

'''
#현재 OPS 페이지에 올릴 새로운 데이터프레임
data2022 = dataset[dataset.year=='22']
data2022.to_csv('ops2022.csv')
dataset = data2022[['name', 'year', 'team', 'OPS', 'game수', '타석', '타율', '안타', '홈런', '타점', '도루', '삼진', '병살', 'WAR+']]
dataset = dataset.sort_values('OPS')
dataset = dataset.drop(['year'], axis=1)
dataset.to_csv('ops.csv')
'''