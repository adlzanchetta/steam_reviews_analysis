FROM python:3
FROM tensorflow/tensorflow:latest-gpu-py3

COPY utils/requirements.txt /requirements.txt

RUN python3 -m pip install -r /requirements.txt

CMD ["rm /requirements.txt"]

# I need to look up what the below command does... I know it sets up the environmental variable for PYTHONPATH but beyond that I need clarification
ENV PYTHONPATH /tmp/aaltd18

COPY script.sh /script.sh

CMD ["/scipt.sh"]
