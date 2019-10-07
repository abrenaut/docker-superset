FROM python:3.6-jessie

# Superset version
ARG SUPERSET_VERSION=0.34.0 

# Configure environment
ENV GUNICORN_BIND=0.0.0.0:8088 \
    GUNICORN_LIMIT_REQUEST_FIELD_SIZE=0 \
    GUNICORN_LIMIT_REQUEST_LINE=0 \
    GUNICORN_TIMEOUT=60 \
    GUNICORN_WORKERS=2 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    SUPERSET_HOME=/home/superset \
    PYTHONPATH=/home/superset:$PYTHONPATH \
    SUPERSET_VERSION=${SUPERSET_VERSION}
ENV GUNICORN_CMD_ARGS="--workers ${GUNICORN_WORKERS} --timeout ${GUNICORN_TIMEOUT} --bind ${GUNICORN_BIND} --limit-request-line ${GUNICORN_LIMIT_REQUEST_LINE} --limit-request-field_size ${GUNICORN_LIMIT_REQUEST_FIELD_SIZE}"

# Create superset user
RUN useradd -U -m superset

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        apt-transport-https \
        apt-utils \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        libsasl2-dev \
        libldap2-dev \
        libxi-dev && \
    apt-get clean && \
    rm -r /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --default-timeout=100 --no-cache-dir \
    gevent==1.2.2 \
    psycopg2==2.6.1 \
    redis==3.2.0 \
    apache-superset==${SUPERSET_VERSION}

# Configure Filesystem
WORKDIR /home/superset

USER superset

COPY config .

# Start application
CMD ["gunicorn", "superset:app"]
