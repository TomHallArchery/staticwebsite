from flask import Flask
from flask_flatpages import FlatPages
from tinydb import TinyDB

import config

flatpages = FlatPages()
db = TinyDB('database.json', indent=4, separators=(',', ': '))


def create_app(config_class=None):
    ''' Default application initialisation '''
    app = Flask(__name__)
    app.config.from_object(config_class or config.Config)
    flatpages.init_app(app)

    with app.app_context():
        # required to bring app registered views in
        # pylint: disable=import-outside-toplevel, unused-import
        from website import views  # noqa
        from website import errors  # noqa
        from website import database

        database.connect_db()
    return app
