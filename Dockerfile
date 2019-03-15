FROM python:3
FROM tensorflow/tensorflow:latest-gpu-py3
FROM alpine

COPY utils/requirements.txt /requirements.txt

RUN python3 -m pip install -r /requirements.txt

CMD ["rm /requirements.txt"]

RUN python3 -m pip install -r requirements.txt

COPY script.sh /script.sh

CMD ["./script.sh"]