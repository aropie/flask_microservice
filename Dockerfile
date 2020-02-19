FROM python:latest

WORKDIR /srv/user_service
COPY ./app/ .
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
