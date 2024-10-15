# url shortener

Aim of this project is to provide full stack platform for URL shortening. Project itself is realized using Django backend that stores all the data within SQLite database and Vue frontend client that allows you to both shorten the link and look for recent links that have been shortened.

## usage

In order to use the application, you need to run:

```sh
docker compose up --build
```

If you'd like to run database migrations feel free to type in:
```sh
docker compose exec backend python manage.py migrate
```

Also creating admin account can be used in the following way:
```sh
docker compose exec backend python manage.py createsuperuser
```

Note: to execute command above, your containers need to be running.

## other notes & further directions
Current configuration assumes that the project will be run in a development environment.

In order to make it production-ready you need to remember about couple things like:
- turning off the `DEBUG` mode in Django
- build the Vue application using `npm`
- have a stricter CORS policy, would be nice to use proxy
- provide some sort of throttling as the application itself doesn't contain any sort of authentication, it's easy to DDoS it
- and many more...
