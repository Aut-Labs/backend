FROM python:3.11.8

WORKDIR /usr/src/

RUN useradd -m -r user && chown user .

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

USER user

ENTRYPOINT ["python3", "-m", "app"]
