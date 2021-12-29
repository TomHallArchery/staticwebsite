from flask import Flask
from flask_mongoengine import MongoEngine
import config

db = MongoEngine()


def register_blueprints(app):
    from .images import images_bp
    from .pages import pages_bp
    from .cli import cli_bp

    app.register_blueprint(images_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(cli_bp)


def create_app(config_class=None):
    ''' Default application initialisation '''
    app = Flask(__name__)
    app.config.from_object(config_class or config.Config)
    db.init_app(app)

    register_blueprints(app)

    with app.app_context():
        # required to bring app registered views in
        from website import (  # noqa
            routes,
            errors,
            models,
        )

    return app
