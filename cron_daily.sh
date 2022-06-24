#!/bin/sh
echo "Start Daily Crontab"

CODE_PATH=$(dirname $(realpath $0))
DATA_PATH=${CODE_PATH}/data

# 크롤링 
crawling_daily_path=${CODE_PATH}/crawling-daily
# python3 ${crawling_daily_path}/first_team.py
python3 ${crawling_daily_path}/pitcher.py
python3 ${crawling_daily_path}/hitter.py


# 데이터 전처리
preprocessing_path=${CODE_PATH}/preprocessing
python3 ${preprocessing_path}/era_preprocessing.py
python3 ${preprocessing_path}/ops_preprocessing.py


# 모델링 
modeling_path=${CODE_PATH}/modeling
python3 ${modeling_path}/era_modeling.py
python3 ${modeling_path}/ops_modeling.py







# sh ~/ybo_cron/cron_daily.sh > ~/ybo_cron/log/job_`date +\%Y-\%m-\%d_\%H:\%M:\%S`.log 2>&1 





# 크론 실행 중인지 확인 ps -ef | grep cron
## root 권한으로 돌고 있어야 함 
# 안 돌고 있으면 sudo service cron start

