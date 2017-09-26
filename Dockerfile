FROM python:2.7-alpine

WORKDIR /opt/ops-gus-bot

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD . /opt/ops-gus-bot/
CMD python run.py
