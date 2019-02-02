FROM python:3

RUN pip install redis  boto3

COPY ./duper_chains_object_scraping.py /usr/local/src/duper_chains_object_scraping.py
COPY ./tools.py /usr/local/src/tools.py
COPY ./constants.py /usr/local/src/constants.py

COPY ./queue_maker.py /usr/local/src/queue_maker.py
COPY ./rediswq.py /usr/local/src/rediswq.py

# CMD python print("dammit")
# CMD python /usr/local/src/queue_maker.py
# CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"


