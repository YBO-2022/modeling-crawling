#!/bin/bash

set -e 

docker build -t wngusrud27/docker-cron ../

export $(cat $(dirname $(realpath $0))/../.env | xargs)

echo ${DOCKER_HUB_PASSWORD} | docker login -u ${DOCKER_HUB_ID} --password-stdin

docker push wngusrud27/docker-cron 
