# define an alias for the specific python version used in this file.
FROM ubuntu:22.04 as python

# Python build stage
FROM ubuntu:22.04 as python-build-stage

ARG BUILD_ENVIRONMENT=local

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev \
    unixodbc-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .


ARG BUILD_ENVIRONMENT=local

# install FreeTDS and dependencies
RUN apt-get update \
    && apt-get install curl -y \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install python3 -y \
    && apt-get install python3-dev -y \
    && apt-get install python3-pip -y\
    && apt-get -y install sudo \
    && apt-get install -y lsb-release \
    && apt-get install -y vim \
    && apt-get install -y wget \
    && apt-get clean all

RUN pip install --upgrade pip
RUN pip install pyodbc
RUN pip install "psycopg[binary]"

# Requirements are installed here to ensure they will be cached.
ADD main.py .
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
    -r ${BUILD_ENVIRONMENT}.txt


RUN apt-get update && \
    apt-get install -y curl gnupg2 software-properties-common apt-transport-https  && \
    apt-get install -y apt-utils lsb-release

# Verificar la versión de Ubuntu y ejecutar los comandos si es compatible
RUN if ! [[ "18.04 20.04 22.04 23.04" == *$(lsb_release -rs)* ]]; then \
    echo "Ubuntu $(lsb_release -rs) is not currently supported."; \
    exit; \
    fi

# Descargar claves de Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

# Agregar el repositorio de Microsoft
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Actualizar los paquetes
RUN apt-get update

# Instalar msodbcsql18
RUN export ACCEPT_EULA=Y && apt-get install -y msodbcsql18

# Opcional: Instalar mssql-tools18 para bcp y sqlcmd
RUN export ACCEPT_EULA=Y && apt-get install -y mssql-tools18

# Agregar mssql-tools18 al PATH
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

# Opcional: Instalar unixODBC development headers
RUN apt-get install -y unixodbc-dev

# Copiar el archivo openssl.cnf a la imagen
COPY openssl.cnf /tmp/openssl.cnf

# Modificar el parámetro CipherString en openssl.cnf
RUN sed -i 's/CipherString = DEFAULT:@SECLEVEL=2/CipherString = DEFAULT:@SECLEVEL=0/' /tmp/openssl.cnf

# Mover el archivo modificado a la ubicación original
RUN mv /tmp/openssl.cnf /etc/ssl/openssl.cnf

ENTRYPOINT ["/entrypoint"]
