FROM python:3.9-slim-buster
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean


COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY . /app


EXPOSE 5000