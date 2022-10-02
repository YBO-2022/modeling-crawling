FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src

# base tool
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils

# python
RUN apt-get install -y python3 python3-pip python3-dev build-essential
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# python libraries
RUN echo "y" | apt-get install python3-tk
RUN \ 
    pip3 install --upgrade pip &&\
    pip3 install requests --no-cache-dir &&\
    pip3 install bs4 --no-cache-dir &&\
    pip3 install pandas --no-cache-dir &&\
    pip3 install sqlalchemy --no-cache-dir &&\
    pip3 install pymysql --no-cache-dir &&\
    pip3 install python-dotenv --no-cache-dir &&\
    pip3 install sklearn --no-cache-dir &&\
    pip3 install xgboost --no-cache-dir 

# cron
RUN apt-get install cron

COPY . .

# Add the cron job
RUN crontab -l | { cat; echo "TZ=Asia/Seoul"; } | crontab -
RUN crontab -l | { cat; echo "* * * * * sh /usr/src/cron_realtime.sh > /usr/src/log-docker/realtime/\`date +\%Y-\%m-\%d_\%H:\%M:\%S\`.log 2>&1"; } | crontab -
RUN crontab -l | { cat; echo "0 3 * * * sh /usr/src/cron_daily.sh > /usr/src/log-docker/daily/\`date +\%Y-\%m-\%d_\%H:\%M:\%S\`.log 2>&1"; } | crontab -

RUN service cron start
CMD ["cron", "-f"]


# 빌드하고 실행
# docker-compose -f docker-compose-local.yml up -d --build 
# docker exec -it ybo_cron /bin/bash 

