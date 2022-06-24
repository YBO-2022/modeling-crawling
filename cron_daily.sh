#!/bin/sh
echo "Start Daily Crontab"

CODE_PATH=$(dirname $(realpath $0))
DATA_PATH=${CODE_PATH}/data

# 크롤링 
CRAWLING_DAILY_PATH=${CODE_PATH}/crawling-daily
python3 ${CRAWLING_DAILY_PATH}/pitcher.py
python3 ${CRAWLING_DAILY_PATH}/hitter.py


# 데이터 전처리
PREPROCESSING_PATH=${CODE_PATH}/preprocessing
python3 ${PREPROCESSING_PATH}/era_preprocessing.py
python3 ${PREPROCESSING_PATH}/ops_preprocessing.py


# 이전 모델링 데이터 삭제
ERA_PREDICTION_FILE=${DATA_PATH}/output/predicted_era.csv
OPS_PREDICTION_FILE=${DATA_PATH}/output/predicted_ops.csv
GOLDENGLOVE_PREDICTION_FILE=${DATA_PATH}/output/predicted_goldenglove.csv
TEAMRANKING_PREDICTION_FILE=${DATA_PATH}/output/predicted_team_ranking.csv

rm ${ERA_PREDICTION_FILE}
rm ${OPS_PREDICTION_FILE}
rm ${GOLDENGLOVE_PREDICTION_FILE}
rm ${TEAMRANKING_PREDICTION_FILE}

# 모델링 
MODELING_PATH=${CODE_PATH}/modeling
python3 ${MODELING_PATH}/era_modeling.py
python3 ${MODELING_PATH}/ops_modeling.py
python3 ${MODELING_PATH}/gg_modeling.py
python3 ${MODELING_PATH}/team_modeling.py


if [ ! -f ${ERA_PREDICTION_FILE} ] && [ ! -f ${OPS_PREDICTION_FILE} ] && [ ! -f ${GOLDENGLOVE_PREDICTION_FILE} ] && [ ! -f ${TEAMRANKING_PREDICTION_FILE} ]; then
    echo "모든 모델링 결과가 존재하지 않습니다."
fi


# DB에 저장
CSV_TO_RDB_PATH=${CODE_PATH}/csv-to-rdb

## 주전
python3 ${CRAWLING_DAILY_PATH}/first_team.py
python3 ${CSV_TO_RDB_PATH}/first_team_csv_to_rdb.py

## 투수
python3 ${CSV_TO_RDB_PATH}/pitcher_csv_to_rdb.py

## 투수 ERA 예측
python3 ${CSV_TO_RDB_PATH}/era_predict_csv_to_rdb.py

## 타자
python3 ${CSV_TO_RDB_PATH}/hitter_csv_to_rdb.py

## 타자 OPS 예측
python3 ${CSV_TO_RDB_PATH}/ops_predict_csv_to_rdb.py

## 시즌 최고 최저
python3 ${CSV_TO_RDB_PATH}/season_high_low_csv_to_rdb.py

## 골글 예측
python3 ${CSV_TO_RDB_PATH}/gg_csv_to_rdb.py



## WAR 데이터 
python3 ${CSV_TO_RDB_PATH}/war_csv_to_rdb.py



STATIC_PATH=${CODE_PATH}/static

## 역대 랭킹
python3 ${STATIC_PATH}/ranking_history_csv_to_rdb.py

## 역대 우승 수
python3 ${STATIC_PATH}/victory_num_csv_to_rdb.py


# 크론 실행 중인지 확인 ps -ef | grep cron
## root 권한으로 돌고 있어야 함 
# 안 돌고 있으면 sudo service cron start

