# Support_Service
___
### Description
#### This project includes developed API for support service,where:
1) Client writes ticket
2) Support see ticket, can change ticket's status and give answers on them
3) After changing ticket's status email message announces client
___

### Requirements

This project requires Python, PostreSQL, Celery, Redis
___
### Deployment

1) You need to have installed Docker, Docker-compose and PostgreSQL with created DB.
2) Clone Git repo:
> $ git clone https://github.com/MikitaYeudakimau/celery_training_support.git .
3) Change email settings.
4) Update db settings in env.dev .
5) Build the images and run containers:
> $ docker-compose up -d --build
6) Load start data to db:
> $ python manage.py loaddata status users
7) Test it out at http://localhost:8000.

*P.S. Passwords for accounts are as usernames.*