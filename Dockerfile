FROM python:3.8.5

WORKDIR /code

COPY foodpro .

RUN pip install -r /code/requirements.txt

CMD gunicorn foodpro.wsgi:application --bind 0.0.0.0:8000
