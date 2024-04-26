import os


class PgTxFetcher:
    CHAINID_TRACK_LIST: list[int] = [1,]
    MORALIS_API_KEY: str = os.getenv("MORALIS_API_KEY")


__all__ = PgTxFetcher,
