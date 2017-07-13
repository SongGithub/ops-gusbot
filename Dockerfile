FROM python:2.7.13-alpine

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD . /app
WORKDIR /app

CMD ["python", "run.py"]
