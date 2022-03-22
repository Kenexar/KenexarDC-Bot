# syntax=docker/dockerfile:1
FROM python:3.8-alpine3.14
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
RUN python3.8 -m venv venv/ && source venv/bin/activate

COPY req req
RUN pip3 install -r req --no-cache-dir
COPY discord/ .
CMD ['./start.sh']
