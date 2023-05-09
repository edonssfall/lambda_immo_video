FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y python3 python3-pip

WORKDIR /lambda
COPY . /lambda

RUN pip install --no-cache-dir -r requirements.txt
CMD python3 main.py