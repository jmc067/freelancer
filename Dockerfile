FROM ubuntu:latest
MAINTAINER Julian Colina "jmc067@bucknell.edu"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install pymongo==2.6.3
RUN pip install bcrypt
ENTRYPOINT ["python"]
CMD ["app.py"]