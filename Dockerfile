FROM python:3.12.8-alpine3.20

#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1  
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1


ENV APP_HOME=/app/src
RUN mkdir -p ${APP_HOME}

COPY  ./Pipfile /app
COPY  ./Pipfile.lock /app
COPY  ./entrypoint.sh /app

# give execute permission
RUN chmod +x /app/entrypoint.sh

WORKDIR /app/src


# to use pyscopg2 in the production environment
RUN apk add build-base libpq libpq-dev

RUN pip3 install pipenv 

# to install dependencies in the system Python environment (not a virtual environment)
RUN pipenv install --system --deploy 

COPY  ./src ${APP_HOME}

ENTRYPOINT ["/app/entrypoint.sh"]
