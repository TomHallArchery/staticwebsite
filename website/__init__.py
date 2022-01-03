from os import environ

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_htmlmin import HTMLMIN
from flask_frozen import Freezer

import config

db = MongoEngine()
htmlmin = HTMLMIN()
freezer = Freezer()


def configure_app(app, config_class=None):
    """Set the appropriate config based on the environment settings"""

    if config_class is None:
        settings_map = {
                'development': config.DevConfig,
                'build': config.BuildConfig,
                'deployment': config.DeployConfig,
                'testing': config.TestConfig,
                'base': config.Config
            }
        env = environ.get('FLASK_ENV', 'base').lower()
        config_class = settings_map[env]

    app.config.from_object(config_class)
    app.config["CONFIG_CLASS"] = config_class


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
    configure_app(app, config_class)

    # intialise extensions
    db.init_app(app)
    htmlmin.init_app(app)
    freezer.init_app(app)

    register_blueprints(app)

    with app.app_context():
        # required to bring app registered views in
        from website import (  # noqa
            errors,
            models,
        )

    return app
