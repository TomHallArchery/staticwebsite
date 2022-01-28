from os import environ

from flask import Flask
from flask_frozen import Freezer
from flask_htmlmin import HTMLMIN
from flask_mongoengine import MongoEngine

import config

db = MongoEngine()
htmlmin = HTMLMIN()
freezer = Freezer()


def configure_app(app, config_class=None):
    """Set the appropriate config based on the environment settings"""

    if config_class is None:
        cfg = environ.get('FLASK_CONFIG', 'base').lower()
        config_class = config.map[cfg]
    else:
        cfg = config_class.__name__

    app.config.from_object(config_class)
    app.cfg = cfg


def register_blueprints(app):
    from .cli import cli_bp
    from .errors import errors_bp
    from .images import images_bp
    from .pages import pages_bp

    app.register_blueprint(cli_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(pages_bp)

    # Conditionally registers testing endpoint based on config;
    # To avoid accidentally deploying test page
    if app.config["VIEW_TEST"]:
        app.add_url_rule(
            '/test/',
            endpoint='pages.serve_test',
            )


def create_app(config_class=None):
    ''' Default application initialisation '''

    app = Flask(__name__)
    configure_app(app, config_class)

    # intialise extensions
    db.init_app(app)
    htmlmin.init_app(app)
    freezer.init_app(app)

    register_blueprints(app)

    return app
