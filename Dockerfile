FROM python:3.9.4

WORKDIR /

ADD . .

ENV FLASK_APP=app.initialize:web_app

RUN pip install -r requirements.txt

ENTRYPOINT []
