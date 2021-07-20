FROM python:3.8.5-alpine

RUN apk add --no-cache postgresql-dev gcc g++ linux-headers mailcap musl-dev python3-dev libffi-dev openssl-dev cargo
RUN pip install --no-cache-dir -U pip uwsgi

WORKDIR /srv/api

COPY requirements.txt /srv/api/requirements.txt
RUN pip install --no-cache-dir -r /srv/api/requirements.txt

COPY . /srv/api
RUN DJANGO_DEBUG=True python manage.py collectstatic --noinput

CMD ["uwsgi","--http-socket", ":8080", "--wsgi-file", "config/wsgi.py", "--processes", "4", "--uid", "root", "--enable-threads", "--static-map=/static=/srv/api/static"]
