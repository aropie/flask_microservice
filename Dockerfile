FROM python:latest

WORKDIR /srv/user_service
COPY ./app/ ./app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN cd .. && mkdir app
CMD gunicorn --bind="0.0.0.0:$PORT" --reload "app:create_app()"
