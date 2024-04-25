import os


class PgTxFetcherConfig:
    CHAINID_TRACK_LIST = [1]
    MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")


# pylint: disable=duplicate-code
class PgConfig:
    # POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_HOST = "postgres"
