# url shortener

Aim of this project is to provide full stack platform for URL shortening. Project itself is realized using Django backend that stores all the data within SQLite database and Vue frontend client that allows you to both shorten the link and look for recent links that have been shortened.

## usage

In order to use the application, you need to run:

```sh
docker-compose up --build
```

or use prepared script for that:
```sh
./script/run-app
```

Just make sure that script is executable by saying:
```sh
chmod +x script/run-app
```

If you'd like to run database migrations feel free to type in:
```sh
docker-compose exec backend python manage.py migrate
```

Also creating admin account can be used in the following way:
```sh
docker-compose exec backend python manage.py createsuperuser
```

Note: to execute these two commands above, your containers need to be running.

## running tests

In order to run tests for both backend and frontend, please do:
```sh
docker-compose --profile tests up --abort-on-container-exit
```

or use prepared script for that:
```sh
./script/run-tests
```

Just make sure that script is executable by saying:
```sh
chmod +x script/run-tests
```

## other notes & further directions
Current configuration assumes that the project will be run in a development environment.

In order to make it production-ready you need to remember about couple things like:
- turning off the `DEBUG` mode in Django
- build the Vue application using `npm`
- have a stricter CORS policy, would be nice to use proxy
- provide some sort of throttling as the application itself doesn't contain any sort of authentication, it's easy to DDoS it
- and many more...
