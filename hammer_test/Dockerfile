FROM python:3.11


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN mkdir /usr/src/app/uploads && mkdir /usr/src/app/static

COPY . .

RUN pip install -r requirements.txt