import flask
from flask import render_template_string, Markup
from flask_flatpages import FlatPages, pygmented_markdown

app = flask.Flask('website') #any name here works EXCEPT 'app'
# static_folder='static'
# template_folder='templates'

def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    return pygmented_markdown(prerendered_body)


# Some configuration, ensures
# 1. Pages are loaded on request.
# 2. File name extension for pages is Markdown.

FLATPAGES_EXTENSION = ['.md', '.markdown']
FLATPAGES_HTML_RENDERER = prerender_jinja

app.config.from_object(__name__)
flatpages = FlatPages(app)
# dirty:
# strip '---' from ._meta attribute of page objects to allow flatpages to work with yaml delimiter
for page in flatpages:
    page._meta = page._meta.strip('---')

from app import views, errors
