from flask import Flask
from flask_flatpages import FlatPages
from flask_mongoengine import MongoEngine
import config

flatpages = FlatPages()
db = MongoEngine()


def create_app(config_class=None):
    ''' Default application initialisation '''
    app = Flask(__name__)
    app.config.from_object(config_class or config.Config)
    flatpages.init_app(app)
    db.init_app(app)

    from .images import images_bp, responsive_images
    app.register_blueprint(images_bp)
    app.add_template_filter(responsive_images)

    with app.app_context():
        # required to bring app registered views in
        from website import (  # noqa
            views,
            errors,
            models,
            pages,
        )

    return app
