FROM python:3.7
RUN pip install redis boto3
COPY ./worker.py /worker.py
COPY ./rediswq.py /rediswq.py

# CMD  python worker.py
