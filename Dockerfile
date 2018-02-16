# This image provides containers that can connect to a postGIS database instance.
FROM python:3.6-alpine
ADD requirements/requirements.txt /requirements.txt
ENV CFLAGS="$CFLAGS -L/lib"
ENV PYTHONUNBUFFERED 0
RUN apk update && \
    apk upgrade && \
    apk add --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
     bash \
     binutils \
     gcc \
     gdal \
     geos \
     git \
     jpeg-dev \
     libffi-dev \
     libpq \
     linux-headers \
     mailcap \
     musl-dev \
     proj4-dev \
     postgresql \
     postgresql-client \
     postgresql-dev \
     zlib-dev && \
    rm -rf /var/cache/apk/*
RUN ln -s /usr/lib/libgeos_c.so.1 /usr/local/lib/libgeos_c.so
RUN ln -s /usr/lib/libgdal.so.20.1.3 /usr/lib/libgdal.so
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# uWSGI will listen on this port
EXPOSE 8000

# Add any custom, static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=platyplus.settings.production
ENV DJANGO_ENV=production
ENV SECRET_KEY=TODO_REPLACE_BY_SECURE_ENV

# uWSGI configuration (customize as needed):
#ENV UWSGI_WSGI_FILE=platyplus/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
#RUN DATABASE_URL=none /venv/bin/python manage.py collectstatic --noinput

#ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
#CMD ["uwsgi", "--http-auto-chunked", "--http-keepalive"]
CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]