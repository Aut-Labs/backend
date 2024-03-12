FROM python:3.11.8

WORKDIR /usr/src/

RUN useradd -m -r user && chown user .

RUN export readonly TINI_VERSION="v0.19.0"
ARG TINI_VERSION="$(echo \$TINI_VERSION)"
COPY ./tini-amd64 ./tini
RUN chmod +x ./tini

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .

RUN pip install -U \
    pip \
    setuptools \
    wheel

RUN pip install --disable-pip-version-check -r requirements.txt

COPY source/app /usr/src/app

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app:/usr/src"

# ARG GIT_HASH
# ENV GIT_HASH=${GIT_HASH:-dev}

USER user

ENTRYPOINT ["/usr/src/tini", "--"]
