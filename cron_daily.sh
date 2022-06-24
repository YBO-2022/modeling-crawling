#!/bin/sh
# ""으로 감싸면 안 됨! 
CODE_PATH=$(dirname $(realpath $0))
crawling_daily_path=${CODE_PATH}/crawling-daily

echo "Hello, World!"

python3 ${crawling_daily_path}/first_team.py

# 호출한 곳에서 상대 경로로 호출됨 


# sh ~/ybo_cron/cron_daily.sh > ~/ybo_cron/log/job_`date +\%Y-\%m-\%d_\%H:\%M:\%S`.log 2>&1 

# sudo apt install python3-pip
# pip install bs4
# pip install pandas


# mysql -u root -p -h ybo-phase1.cgkn3au7spxb.ap-northeast-2.rds.amazonaws.com
# pip install mysqlclient  
# pip3 install python-dotenv

# 실행: sh cron.sh



# 크론 실행 중인지 확인 ps -ef | grep cron
## root 권한으로 돌고 있어야 함 
# 안 돌고 있으면 sudo service cron start

