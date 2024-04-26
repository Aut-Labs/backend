from flask import Flask

from app.config import PostgresClientConfig


def create_app():
    app = Flask(__name__)

    from app.routes import bp as blueprint
    app.register_blueprint(blueprint)

    from app.config import BackendApiConfig
    app.config.from_mapping({
        "SECRET_KEY": BackendApiConfig.SECRET_KEY,
        "AUTH_TOKEN_DURATION": BackendApiConfig.AUTH_TOKEN_DURATION,
        "AUTH_BEGIN_TIMESTAMP": BackendApiConfig.AUTH_BEGIN_TIMESTAMP
    })

    app.config.from_object(PostgresClientConfig())

    return app


app = create_app()


__all__ = app,
