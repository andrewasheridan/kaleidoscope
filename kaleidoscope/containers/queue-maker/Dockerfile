FROM python:3

RUN pip install redis  boto3

COPY ./constants.py /usr/local/src/constants.py
COPY ./key_scraper.py /usr/local/src/key_scraper.py
COPY ./queue_maker.py /usr/local/src/queue_maker.py
COPY ./rediswq.py /usr/local/src/rediswq.py
