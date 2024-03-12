from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.auth import bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.config import Config
    app.config.from_mapping({
        "SECRET_KEY": Config.SECRET_KEY,
        "AUTH_TOKEN_DURATION": Config.AUTH_TOKEN_DURATION,
        "AUTH_BEGIN_TIMESTAMP": Config.AUTH_BEGIN_TIMESTAMP
    })

    return app

app = create_app()
