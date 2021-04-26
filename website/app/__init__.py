import flask
from flask_flatpages import FlatPages

app = flask.Flask('__name__')


# Some configuration, ensures
# 1. Pages are loaded on request.
# 2. File name extension for pages is Markdown.
# DEBUG = True
# FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app.config.from_object(__name__)
flatpages = FlatPages(app)

from app import views, errors
