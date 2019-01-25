FROM python:3.7-slim
# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apt-get update && apt-get install -y musl-dev gcc make curl \
    && curl -sSLf https://github.com/openfaas-incubator/of-watchdog/releases/download/0.4.2/of-watchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog \
    && apt-get remove -y curl

WORKDIR /root/

COPY requirements.txt   .
RUN pip install -r requirements.txt
COPY index.py           .

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /root/function/

WORKDIR /root/
COPY function           function

ENV fprocess="python index.py"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
