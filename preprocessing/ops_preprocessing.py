# -*- coding: utf-8 -*-

import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
temp = pd.read_csv(f'{current_dir}/../data/input/hitter.csv', encoding="UTF-8")

def opsPreprocessing(data):
    data = data.drop(['Unnamed: 0', 'ranking'], axis=1)

    data['year'] = 30
    data['team'] = 'a'
    data['position'] = 'w'

    for i in range(0, len(data)) :
        str = data.season_team_position[i]
        data.year[i] = str[0:2] # year에 연도 저장
        data.team[i] = str[2] # team에 한글자 팀 저장
        data.position[i] = str[3:] # position에 포지션 저장

    data = data.drop(['season_team_position'], axis=1)

    for i in data.columns[1:-3] :
        data[i] = pd.to_numeric(data[i])


    team_name = ['SSG', '삼성', 'NC', '한화', 'LG', '롯데', 'KIA', '두산', '키움', 'KT']
    team_short_name = ['S', '삼', 'N', '한', 'L', '롯', 'K', '두', '키', 'k']

    for i in range(0,10):
        data = data.replace(team_short_name[i], team_name[i])


    data.rename(columns = {'war':'WAR+'},inplace=True)
    data.rename(columns = {'score':'득점'},inplace=True)
    data.rename(columns = {'tasuk':'타석'},inplace=True)
    data.rename(columns = {'tasu':'타수'},inplace=True)
    data.rename(columns = {'game':'game수'},inplace=True)
    data.rename(columns = {'hit':'안타'},inplace=True)
    data.rename(columns = {'2hit':'이루타'},inplace=True)
    data.rename(columns = {'3hit':'삼루타'},inplace=True)
    data.rename(columns = {'homerun':'홈런'},inplace=True)
    data.rename(columns = {'ruta':'루타'},inplace=True)
    data.rename(columns = {'tazeom':'타점'},inplace=True)
    data.rename(columns = {'doru':'도루'},inplace=True)
    data.rename(columns = {'dosil':'도실'},inplace=True)
    data.rename(columns = {'ballfour':'볼넷'},inplace=True)
    data.rename(columns = {'sagu':'사구'},inplace=True)
    data.rename(columns = {'gofour':'고의사구'},inplace=True)
    data.rename(columns = {'samzin':'삼진'},inplace=True)
    data.rename(columns = {'beongsal':'병살'},inplace=True)
    data.rename(columns = {'heeta':'희타'},inplace=True)
    data.rename(columns = {'teebi':'희비'},inplace=True)
    data.rename(columns = {'tayul':'타율'},inplace=True)
    data.rename(columns = {'choolru':'출루'},inplace=True)
    data.rename(columns = {'zhangta':'장타'},inplace=True)
    data.rename(columns = {'ops':'OPS'},inplace=True)
    data.rename(columns = {'woba':'wOBA'},inplace=True)
    data.rename(columns = {'wrc+':'wRC+'},inplace=True)
    data.rename(columns = {'wpa':'WPA'},inplace=True)

    return data

data = opsPreprocessing(temp)
data.to_csv(f'{current_dir}/../data/input/preprocessed_ops.csv', encoding="UTF-8")
