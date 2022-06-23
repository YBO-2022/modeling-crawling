FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
MAINTAINER baeldung.com

WORKDIR /app
COPY . .
RUN export CODE_PATH=/app

# base tool
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils

# python
RUN apt-get install -y python3 python3-pip python3-dev build-essential
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN echo "y" | apt-get install python3-tk
RUN pip3 install requests
RUN pip3 install bs4
RUN pip3 install pandas
RUN pip3 install sqlalchemy
RUN pip3 install pymysql
RUN pip3 install python-dotenv

# cron
RUN apt-get install cron

RUN mkdir log
# Add the cron job
RUN crontab -l | { cat; echo "* * * * * sh /app/cron/cron_realtime.sh > /app/log/realtime_`date +\%Y-\%m-\%d_\%H:\%M:\%S`.log 2>&1"; } | crontab -

RUN service cron start
# Run the command on container startup
CMD ["cron", "-f"]

# docker-compose up -d 
# docker exec -it cron /bin/bash 