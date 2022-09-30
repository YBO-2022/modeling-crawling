#!/bin/sh
echo "Start Realtime Crawling"

CODE_PATH=$(dirname $(realpath $0))
crawling_realtime_path=${CODE_PATH}/crawling-realtime

python3 ${crawling_realtime_path}/game.py
python3 ${crawling_realtime_path}/ranking.py

echo "Finish Realtime Crawling"