### Get Debian-based Python image
FROM python:3.8.14-slim-bullseye

### Get Java via the package manager
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main'
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-8-jre

### Setup and installation
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

### Run application
RUN python manage.py collectstatic --noinput
CMD gunicorn SemanticSearch.wsgi:application --bind 0.0.0.0:$PORT
