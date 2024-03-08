def create_app():
    app = ...

    from . import auth3
    app.register_blueprint(auth3.bp)

    return app
