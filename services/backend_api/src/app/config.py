import os


class BackendApiConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    AUTH_TOKEN_DURATION = int(os.getenv("AUTH_TOKEN_DURATION"))
    AUTH_BEGIN_TIMESTAMP = int(os.getenv("AUTH_BEGIN_TIMESTAMP"))


# pylint: disable=duplicate-code
class PgConfig:
    # POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_HOST = "postgres"
