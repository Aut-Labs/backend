FROM python:3.11.8

WORKDIR /usr/src/

RUN useradd -m -r user && chown user .

RUN apt-get update && \
    apt-get install -y cron && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .

RUN pip install -U \
    pip \
    setuptools \
    wheel

RUN pip install --disable-pip-version-check -r requirements.txt

COPY src/app /usr/src/app

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app:/usr/src"


# https://crontab.guru/
RUN cat > /etc/cron.d/job <<EOL
* * * * * python3 -m app
# 
EOL

# check syntax
RUN crontab -n /etc/cron.d/job

RUN crontab /etc/cron.d/job

RUN touch /var/log/cron.log

CMD ["cron", "-f"]
