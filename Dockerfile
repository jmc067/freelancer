FROM ubuntu:latest
MAINTAINER Julian Colina "jmc067@bucknell.edu"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
