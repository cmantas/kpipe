# syntax=docker/dockerfile:1

FROM python:3.11-slim

COPY . /kpipe

RUN pip install -r /kpipe/requirements.txt

ENTRYPOINT ["python", "/kpipe/pipe.py"]
