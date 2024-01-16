
# define an alias for the specific python version used in this file.
FROM python:3.11-bullseye as python

# Python build stage
FROM python:3.11-bullseye as python-build-stage

ARG BUILD_ENVIRONMENT=production

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev && pip install psycopg2

# Database dependencies
RUN apt-get update && apt-get install -y gcc \
  && apt-get install -y g++ \
  && apt-get install -y unixodbc unixodbc-dev \
  && apt-get install -y freetds-dev freetds-bin \
  && apt-get install -y --no-install-recommends apt-utils \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y unixodbc-dev \
  && apt-get -y install sudo \
  && apt-get install -y lsb-release \
  && apt-get install -y vim \
  && apt-get install -y wget \
  && apt-get install -y iputils-ping

# MSSQL ODBC
RUN apt-get update
RUN apt-get install -y bash-completion
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated msodbcsql18
ADD main.py .
# Copy openssl.cnf file to the image
COPY openssl.cnf /tmp/openssl.cnf
# Move the file to the original location
RUN mv /tmp/openssl.cnf /etc/ssl/openssl.cnf
# Modify the paremeter CipherString in openssl.cnf
RUN sed -i 's/CipherString = DEFAULT:@SECLEVEL=2/CipherString = DEFAULT:@SECLEVEL=0/' /tmp/openssl.cnf



RUN pip install --upgrade pip
RUN pip install pyodbc

# Instalación de dependencias y herramientas necesarias
RUN apt-get update && \
  apt-get install -y curl gnupg2 software-properties-common apt-transport-https && \
  apt-get install -y apt-utils lsb-release

# Verificar la versión de Ubuntu y ejecutar los comandos si es compatible
RUN if ! [[ "18.04 20.04 22.04 23.04" == *$(lsb_release -rs)* ]]; then \
  echo "Ubuntu $(lsb_release -rs) is not currently supported."; \
  exit; \
  fi


# Modificar el parámetro CipherString en openssl.cnf
RUN sed -i 's/CipherString = DEFAULT:@SECLEVEL=2/CipherString = DEFAULT:@SECLEVEL=0/' /tmp/openssl.cnf

# Mover el archivo modificado a la ubicación original
RUN mv /tmp/openssl.cnf /etc/ssl/openssl.cnf
# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN addgroup --system django \
  && adduser --system --ingroup django django


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  unixodbc-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/


COPY --chown=django:django ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=django:django ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
COPY --chown=django:django ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


COPY --chown=django:django ./compose/production/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat


COPY ./compose/production/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


# copy application code to WORKDIR
COPY --chown=django:django . ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown django:django ${APP_HOME}

USER django

RUN DATABASE_URL="" \
  CELERY_BROKER_URL="" \
  DJANGO_SETTINGS_MODULE="config.settings.test" \
  python manage.py compilemessages

ENTRYPOINT ["/entrypoint"]
