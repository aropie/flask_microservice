FROM debian:latest

# Set the locale
ENV LC_ALL C

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y python3-pip python3-dev git

WORKDIR /srv/user_service
COPY ./app/ .
RUN pip3 install -r requirements.txt
