FROM python:3.9.0

WORKDIR /usr/src/

RUN useradd -m -r user && chown user .

RUN export readonly TINI_VERSION="v0.19.0"
ARG TINI_VERSION="$(echo \$TINI_VERSION)"
COPY ./tini-amd64 .
RUN chmod +x ./tini-amd64

COPY requirements.txt .

RUN pip install -U \
    pip \
    setuptools \
    wheel

RUN pip install --disable-pip-version-check -r requirements.txt

COPY ./server/app.py .

# ARG GIT_HASH
# ENV GIT_HASH=${GIT_HASH:-dev}

USER user

ENTRYPOINT ["/usr/src/tini", "--"]
