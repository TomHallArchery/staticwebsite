from flask import Flask
from flask_mongoengine import MongoEngine
import config

db = MongoEngine()


def create_app(config_class=None):
    ''' Default application initialisation '''
    app = Flask(__name__)
    app.config.from_object(config_class or config.Config)
    db.init_app(app)

    from .images import images_bp, responsive_images
    from .pages import pages_bp, prerender_jinja

    app.register_blueprint(images_bp)
    app.register_blueprint(pages_bp)

    app.add_template_filter(responsive_images)
    app.add_template_filter(prerender_jinja)

    with app.app_context():
        # required to bring app registered views in
        from website import (  # noqa
            routes,
            errors,
            models,
        )

    return app
