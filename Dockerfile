FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
MAINTAINER baeldung.com

WORKDIR /app

RUN export ACTIVE=Docker

# base tool
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils

# python
RUN apt-get install -y python3 python3-pip python3-dev build-essential
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN echo "y" | apt-get install python3-tk
RUN \ 
    pip3 install requests &&\
    pip3 install bs4 &&\
    pip3 install pandas &&\
    pip3 install sqlalchemy &&\
    pip3 install pymysql &&\
    pip3 install python-dotenv

# cron
RUN apt-get install cron

COPY . .

# Add the cron job
RUN crontab -l | { cat; echo "ACTIVE=Docker"; } | crontab -
RUN crontab -l | { cat; echo "TZ=Asia/Seoul"; } | crontab -
RUN crontab -l | { cat; echo "* * * * * sh /app/cron_realtime.sh > /app/log-docker/realtime_\`date +\%Y-\%m-\%d_\%H:\%M:\%S\`.log 2>&1"; } | crontab -

RUN service cron start
# Run the command on container startup
CMD ["cron", "-f"]

# docker-compose up -d 
# docker exec -it cron /bin/bash 

# 추가
# pip install selenium
# pip install webdriver_manager

# 크롬 드라이버 설치 코드 추가 
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt install ./google-chrome-stable_current_amd64.deb
# sudo wget https://chromedriver.storage.googleapis.com/93.0.4577.63/chromedriver_linux64.zip
# unzip chromedriver_linux64.zip



