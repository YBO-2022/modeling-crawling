#!/bin/sh
echo "Start Daily Crontab"

CODE_PATH=$(dirname $(realpath $0))
DATA_PATH=${CODE_PATH}/data

# 크롤링 
CRAWLING_DAILY_PATH=${CODE_PATH}/crawling-daily
# python3 ${crawling_daily_path}/first_team.py
python3 ${CRAWLING_DAILY_PATH}/pitcher.py
python3 ${CRAWLING_DAILY_PATH}/hitter.py


# 데이터 전처리
PREPROCESSING_PATH=${CODE_PATH}/preprocessing
python3 ${PREPROCESSING_PATH}/era_preprocessing.py
python3 ${PREPROCESSING_PATH}/ops_preprocessing.py


# 이전 모델링 데이터 삭제
ERA_PREDICTION_FILE=${DATA_PATH}/output/predicted_era.csv
OPS_PREDICTION_FILE=${DATA_PATH}/output/predicted_ops.csv

rm ${ERA_PREDICTION_FILE}
rm ${OPS_PREDICTION_FILE}

# 모델링 
MODELING_PATH=${CODE_PATH}/modeling
python3 ${MODELING_PATH}/era_modeling.py
python3 ${MODELING_PATH}/ops_modeling.py


if [-f ${ERA_PREDICTION_FILE}] && [-f ${OPS_PREDICTION_FILE}]; then
    echo "없음!!"
fi





# sh ~/ybo_cron/cron_daily.sh > ~/ybo_cron/log/job_`date +\%Y-\%m-\%d_\%H:\%M:\%S`.log 2>&1 





# 크론 실행 중인지 확인 ps -ef | grep cron
## root 권한으로 돌고 있어야 함 
# 안 돌고 있으면 sudo service cron start

