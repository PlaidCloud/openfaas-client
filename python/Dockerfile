FROM python:3.7-slim AS lint
RUN mkdir -p /client \
 && pip install pytest requests simplejson urllib3 kubernetes

COPY . /client/
WORKDIR /client
RUN python setup.py install
CMD ((git diff --name-only origin/master $GIT_COMMIT) | grep .py$) | xargs -r -n1 pylint faasclient --output-format=parseable --jobs=4 --reports=no>pylint.log

FROM python:3.7-slim

RUN mkdir -p /client \
 && pip install pytest requests simplejson urllib3 kubernetes

COPY . /client/
WORKDIR /client
RUN python setup.py install
CMD pytest -v
