# Welcome to INVTASK

----
## Overview

Your task is to build a backend for a web scraper.
It will be used by client applications to retrieve the following structured content:

* Twitter profiles

Decorated with a popularity index calculated as:

* Twitter (followers)

----
## Solution

I solved it in two different ways:

1. I decorated the REST API with a popularity property, and too I decorated the model with other popularity property.
1. I added a method in model manager that annotate a rank field.

----
## App Features

* REST API created with Django and Tastypie.
* Minimal Consumer frontend created with VueJS.
* Script to setup local environment.
* Script to setup docker.

----
## Requeriments

* Python 3+
* PostgreSQL
* Redis


----
## Development

To get started with development, clone this repository and set up the dependencies:

    > ./scripts/devsetup.sh

And start the development server:

    > ./scripts/dev.sh

### Services
Now you are able to access:

* **WEB Consumer:** http://localhost:8000
* **REST Api:** http://localhost:8000/api/v1/
* **Flower Monitoring:** http://localhost:5555


----
## Development with Docker

Check .env file, database configuration. 
Install [Doker](http://www.doker.com)
and execute:

    > docker-compose build
    > docker-compose up

Then you can check your containers with this :    

    > docker-compose ps

To access container:
    > docker exec -i -t invtask_web_1 /bin/bash

----
## Monitoring

You can monitor all task with Flower accessing:

    http://localhost:5555

Or from terminal with commands

    > celery --app=invtask.app.celery:app control enable_events
    > celery --app=invtask.app.celery:app events

----
## Deploy

You can quickly deploy invtask to Heroku:

    heroku login
    heroku create invtask
    heroku addons:create heroku-redis:hobby-dev # for Celery
    git push heroku master
    heroku run python manage.py migrate

----
## Whats Next?

* Create documentation with Sphinx and ReadTheDocs theme
* Integrate with travis-ci
* Integrate with sentry.io
* Configure AWS S3, to store static media
* Configure AWS EC2 to run django and celery with supervisord
* Configure ansible or fabric to deploy to AWS server
