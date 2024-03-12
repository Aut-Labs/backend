from flask import Flask, g
import psycopg2

from app.config import PgConfig

def get_db_connection():
    return psycopg2.connect(host=PgConfig.POSTGRES_HOST,
                            database=PgConfig.POSTGRES_DB,
                            user=PgConfig.POSTGRES_USER,
                            password=PgConfig.POSTGRES_PASSWORD)

def create_app():
    app = Flask(__name__)

    from app.routes import bp as blueprint
    app.register_blueprint(blueprint)

    from app.config import Config
    app.config.from_mapping({
        "SECRET_KEY": Config.SECRET_KEY,
        "AUTH_TOKEN_DURATION": Config.AUTH_TOKEN_DURATION,
        "AUTH_BEGIN_TIMESTAMP": Config.AUTH_BEGIN_TIMESTAMP
    })

    app.config.from_object(PgConfig())

    return app

app = create_app()
