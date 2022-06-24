# -*- coding: utf-8 -*-

import pandas as pd

"""## KT 없는데이터 가지고 전처리"""

temp = pd.read_csv('//content/drive/Shareddrives/[2022-1 Ybigta] 타율 어쩌구 구단이 울랄라/모델링팀/최종/pitcher.csv', encoding='UTF-8')

def eraPreprocessing(data):
    data = data.drop(['Unnamed: 0', 'ranking'], axis=1)

    data['year'] = 30
    data['team'] = 'a'

    for i in range(0, len(data)) :
        str = data.season_team[i]
        data.year[i] = str[0:2] # year에 연도 저장
        data.team[i] = str[2] # team에 한글자 팀 저장

    data = data.drop(['season_team'], axis=1)

    for i in data.columns[1:-3] :
        data[i] = pd.to_numeric(data[i])


    team_name = ['SSG', '삼성', 'NC', '한화', 'LG', '롯데', 'KIA', '두산', '키움', 'KT']
    team_short_name = ['S', '삼', 'N', '한', 'L', '롯', 'K', '두', '키', 'k']

    for i in range(0,10):
        data = data.replace(team_short_name[i], team_name[i])


    data.rename(columns = {'war':'WAR'},inplace=True)
    data.rename(columns = {'choolzhang':'출장'},inplace=True)
    data.rename(columns = {'wanto':'완투'},inplace=True)
    data.rename(columns = {'sonbal':'선발'},inplace=True)
    data.rename(columns = {'win':'승'},inplace=True)
    data.rename(columns = {'loose':'패'},inplace=True)
    data.rename(columns = {'wanbong':'완봉'},inplace=True)
    data.rename(columns = {'save':'세이브'},inplace=True)
    data.rename(columns = {'hold':'홀드'},inplace=True)
    data.rename(columns = {'inning':'이닝'},inplace=True)
    data.rename(columns = {'silzeom':'실점'},inplace=True)
    data.rename(columns = {'zachaeck':'자책'},inplace=True)
    data.rename(columns = {'taza':'타자'},inplace=True)
    data.rename(columns = {'anta':'피안타'},inplace=True)
    data.rename(columns = {'2hit':'이루타'},inplace=True)
    data.rename(columns = {'3hit':'삼루타'},inplace=True)
    data.rename(columns = {'homerun':'홈런'},inplace=True)
    data.rename(columns = {'ballfour':'볼넷'},inplace=True)
    data.rename(columns = {'gofour':'고의사구'},inplace=True)
    data.rename(columns = {'sagu':'사구'},inplace=True)
    data.rename(columns = {'samzin':'삼진'},inplace=True)
    data.rename(columns = {'vok':'보크'},inplace=True)
    data.rename(columns = {'poktu':'폭투'},inplace=True)
    data.rename(columns = {'era':'ERA'},inplace=True)
    data.rename(columns = {'fip':'FIP'},inplace=True)
    data.rename(columns = {'whip':'WHIP'},inplace=True)
    data.rename(columns = {'era+':'ERA+'},inplace=True)
    data.rename(columns = {'fip+':'FIP+'},inplace=True)
    data.rename(columns = {'WPA':'wpa'},inplace=True)

    return data

data = eraPreprocessing(temp)
data.to_csv('test_era.csv')


