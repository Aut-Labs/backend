import os


class PostgresClient:
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_HOST: str = "postgres"
