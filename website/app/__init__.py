import flask
from flask import render_template_string, Markup
from flask_flatpages import FlatPages, pygmented_markdown

app = flask.Flask('__name__')

def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    return pygmented_markdown(prerendered_body)


# Some configuration, ensures
# 1. Pages are loaded on request.
# 2. File name extension for pages is Markdown.

FLATPAGES_EXTENSION = '.md'
FLATPAGES_HTML_RENDERER = prerender_jinja

app.config.from_object(__name__)
flatpages = FlatPages(app)

from app import views, errors
