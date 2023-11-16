# Welcome to StackEdit!

Hi! This project is a task for BitPin's interview flow. According to interview and it's limited time, this project is not completed.


## Setup Locally

Make a `.env` file like `.env.sample` and fill with your values. if you want to use postgres set `DATABASE` to `postgres`.
After setting env vars use `docker compose up -d` to deploy project locally on your system.
Now project is up on `localhost:8001` on your local machine. 

`localhost:8001/posts` --> to list and create posts.

`localhost:8001/posts/rate` --> to send rate on posts

> By rating on a previous post, your score will be updated




## Time Issues
Unfortunately because of time limitation there is no any flow to create user, It would better if there was an authentication system to create user, now to create user you should `exec` into the bitrate container and by using `python manage.py createsuperuser`  command , create a superuser to have access to django-admin panel. Each `User` should have a `UserProfile`. It would be better if there was a `signal` on these models to make this relation automated, but because of time issues, you should make a `UserProfile` manually for your users. 


## Cache 
There is a `redis` instance in docker compose which is for caching posts scores, because the number of rates on posts are too large we should prevent score calculation on each request. 
