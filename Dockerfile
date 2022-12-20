# syntax=docker/dockerfile:1

FROM python:3.11-slim

# copy the source .py file and requirements file
COPY pipe.py /kpipe/
COPY requirements.txt /kpipe/

# Install requirements
RUN pip install -r /kpipe/requirements.txt

ENTRYPOINT ["python", "/kpipe/pipe.py"]
