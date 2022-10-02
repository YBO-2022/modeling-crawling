#!/bin/sh
echo "Start Static Job"

CODE_PATH=$(dirname $(realpath $0))
STATIC_PATH=${CODE_PATH}/static

## 역대 랭킹
python3 ${STATIC_PATH}/ranking_history_csv_to_rdb.py
## 역대 우승 수
python3 ${STATIC_PATH}/victory_num_csv_to_rdb.py

echo "Finish Static Job"
