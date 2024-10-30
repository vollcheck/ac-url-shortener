FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
