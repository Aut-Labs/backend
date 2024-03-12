import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    AUTH_TOKEN_DURATION = int(os.getenv("AUTH_TOKEN_DURATION"))
    AUTH_BEGIN_TIMESTAMP = int(os.getenv("AUTH_BEGIN_TIMESTAMP"))
