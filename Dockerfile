#syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

# Install base libs
RUN apt update \
    && apt install -y python3-dev curl gcc g++ make

# Install python libs and poetry
ENV POETRY_HOME /usr/local
RUN pip install --no-cache-dir --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.3.2

# Clean cache
RUN apt-get clean autoclean \
    && apt-get autoremove --yes curl \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf $(pip cache dir)

ARG REVISION
ENV REVISION=${REVISION}

WORKDIR /src/

COPY pyproject.toml poetry.lock Makefile /src/
RUN make install-deploy

COPY . /src/

RUN groupadd -r --gid 2000 app-user && \
    useradd -r --uid 2000 -s /bin/false -g app-user app-user && \
    chown -R app-user:app-user /src/ && \
    chmod -R 554 /src/

CMD [ "./bin/pre-start.sh", "./bin/gunicorn.sh" ]
