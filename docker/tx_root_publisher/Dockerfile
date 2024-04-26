FROM python:3.11.8

WORKDIR /usr/src/

RUN useradd -m -r user && chown user .

RUN apt-get update && \
    apt-get install cron && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .

RUN pip install -U \
    pip \
    setuptools \
    wheel

RUN pip install --disable-pip-version-check -r requirements.txt

COPY src/app /usr/src/app

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app:/usr/src"

USER user

RUN cat > /etc/crond.d/job <<EOL
* * * * * python3 -m app
# 
EOL

RUN chomod 0644 /etc/cron.d/job

RUN crontab /etc/cron.d/job

RUN touch /var/log/cron.log

CMD ["cron", "-f"]
