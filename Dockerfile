# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add build-base jpeg-dev zlib-dev

#RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
#RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
#RUN apt-get update \
#    && apt-get install postgresql-client-12 gcc python3-dev -y

# install dependencies
RUN pip install --upgrade pip
RUN pip install 'setuptools==58.0.0'
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .