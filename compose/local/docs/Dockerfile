# define an alias for the specific python version used in this file.
FROM python:3.11-bullseye as python

# Python build stage
FROM python:3.11-bullseye as python-build-stage

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  && apt-get install unixodbc -y \
  && apt-get install unixodbc-dev -y \
  && apt-get install freetds-dev -y \
  && apt-get install freetds-bin -y \
  && apt-get install tdsodbc -y \
  && pip install psycopg2 \
  && apt-get install python3-pyodbc \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

# create python dependency wheels
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels  \
  -r /requirements/local.txt -r /requirements/production.txt \
  && rm -rf /requirements


# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y \
  # To run the Makefile
  make \
  # psycopg2 dependencies
  libpq-dev \
  unixodbc-dev \
  # Translations dependencies
  gettext \
  # Uncomment below lines to enable Sphinx output to latex and pdf
  # texlive-latex-recommended \
  # texlive-fonts-recommended \
  # texlive-latex-extra \
  # latexmk \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# install FreeTDS and dependencies
RUN apt-get update \
  && apt-get install unixodbc -y \
  && apt-get install unixodbc-dev -y \
  && apt-get install freetds-dev -y \
  && apt-get install freetds-bin -y \
  && apt-get install tdsodbc -y \
  && apt-get install --reinstall build-essential -y

# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels

# use wheels to install python dependencies
RUN pip install --no-cache /wheels/* \
  && rm -rf /wheels

COPY ./compose/local/docs/start /start-docs
RUN sed -i 's/\r$//g' /start-docs
RUN chmod +x /start-docs

WORKDIR /docs
