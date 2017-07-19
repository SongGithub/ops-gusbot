FROM python:2.7.13-alpine


COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


RUN apk add --update curl && \
    rm -rf /var/cache/apk/*

RUN curl -sL -o /usr/local/bin/shush \
    https://github.com/realestate-com-au/shush/releases/download/v1.3.1/shush_linux_amd64 \
 && chmod +x /usr/local/bin/shush
ENTRYPOINT ["/usr/local/bin/shush","--region","ap-southeast-2","exec", "--"]


ADD . /app
WORKDIR /app

CMD ["python", "run.py"]
