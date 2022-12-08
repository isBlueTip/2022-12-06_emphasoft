FROM python:3.9-bullseye

RUN mkdir /app

RUN apt update
RUN apt upgrade -y

RUN pip install --upgrade pip

COPY /requirements_prod.txt /app

RUN pip install -r /app/requirements_prod.txt --no-cache-dir

COPY ./ /app

WORKDIR /app/backend

RUN python3 manage.py collectstatic --no-input

CMD ["gunicorn", "emphasoft.wsgi:application", "--bind", "0:8000"]
