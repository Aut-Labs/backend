from flask import Flask

from app.config import PgConfig

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
