FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

RUN mkdir /var/log/uwsgi

RUN /usr/bin/apt-get update
RUN /usr/bin/apt-get install -y --allow-unauthenticated \
libjpeg-turbo-progs \
librsvg2-bin \
optipng \
ca-certificates

RUN pip install boto3

COPY src/owl /app/owl
COPY .docker/settings.py /app/owl/settings.py
COPY .docker/uwsgi.ini /app/uwsgi.ini
COPY src/runserver.py /app/runserver.py
COPY .docker/nginx.conf /app/nginx.conf

RUN mkdir /var/data

#COPY .docker/entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh
