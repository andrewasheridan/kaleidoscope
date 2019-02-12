FROM python:3.7
RUN pip install redis boto3
RUN pip install awscli --upgrade
RUN pip install numpy opencv-python
COPY ./worker.py /worker.py
COPY ./rediswq.py /rediswq.py
COPY ./image_augmenter.py /image_augmenter.py
COPY ./transformations.py /transformations.py
COPY ./constants.py /constants.py


# CMD  python worker.py
