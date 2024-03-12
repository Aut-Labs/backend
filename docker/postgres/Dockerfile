FROM postgres:14

# ====== pg_tsparser
RUN apt-get update && apt-get install -y \
      && git clone https://github.com/postgrespro/pg_tsparser \
      && cd pg_tsparser \
      && make USE_PGXS=1 install 
