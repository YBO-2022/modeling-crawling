cron_path=~/ybo_cron
crawling_realtime_path=${cron_path}/crawling-realtime

echo "Start Realtime Crawling"

python3 ${crawling_realtime_path}/game.py
python3 ${crawling_realtime_path}/ranking.py

echo "Finish Realtime Crawling"
