#syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

# Install base libs
RUN apt update \
    && apt install -y python3-dev gcc g++ make \
    && pip install --no-cache-dir --upgrade pip

# Install poetry
ENV POETRY_HOME /usr/local
ADD https://install.python-poetry.org install_poetry.py
RUN python install_poetry.py --version 1.7.1 \
    && rm install_poetry.py

# Clean cache
RUN apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf $(pip cache dir)

ARG RELEASE
ENV RELEASE=${RELEASE}

WORKDIR /src/

COPY ["pyproject.toml", "poetry.lock", "Makefile", "/src/"]
RUN make install-deploy

COPY . /src/

RUN groupadd -r --gid 2000 app-user && \
    useradd -r --uid 2000 -s /bin/false -g app-user app-user && \
    chown -R app-user:app-user /src/ && \
    chmod -R 554 /src/

CMD [ "./bin/pre-start.sh", "./bin/gunicorn.sh" ]
