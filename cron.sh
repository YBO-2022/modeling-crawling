#!/bin/sh
# ""으로 감싸면 안 됨! 
cron_path=~/ybo_cron
crawling_day_path=${cron_path}/crawling-day

echo "Hello, World!"

python3 ${crawling_day_path}/first_team.py

# 호출한 곳에서 상대 경로로 호출됨 


# sh ~/ybo_cron/cronjob.sh > ~/ybo_cron/log/job_`date +\%Y-\%m-\%d_\%H:\%M:\%S`.log 2>&1 

# ~/ybo_cron/log/ 폴더가 있어야함! 



# sudo apt install python3-pip
# pip install bs4
# pip install pandas


# mysql -u root -p -h ybo-phase1.cgkn3au7spxb.ap-northeast-2.rds.amazonaws.com
# pip install mysqlclient  
# pip3 install python-dotenv

# 실행: sh cron.sh



# 크론 실행 중인지 확인 ps -ef | grep cron
## root 권한으로 돌고 있어야 함 
# 안 돌고 있으면 service cron start

