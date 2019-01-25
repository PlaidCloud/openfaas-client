FROM python:3.7-slim

RUN mkdir -p /client \
 && pip install pytest requests simplejson urllib3 kubernetes

COPY . /client/
WORKDIR /client
RUN python setup.py install
CMD pytest -v