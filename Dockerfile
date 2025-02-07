FROM python:3.12.8-alpine3.20

ENV PYTHONUNBUFFERED 1

COPY  ./src /app
COPY  ./Pipfile /app
COPY  ./Pipfile.lock /app

WORKDIR /app

# to use pyscopg2 in the production environment
RUN apk add build-base libpq libpq-dev

RUN pip3 install pipenv 

# to install dependencies in the system Python environment (not a virtual environment)
RUN pipenv install --system --deploy 

EXPOSE 8000