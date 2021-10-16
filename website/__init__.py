import flask
import markdown
from flask import render_template_string, Markup
from flask_flatpages import FlatPages

app = flask.Flask(__name__)

# Setting flatpages extensions wasn't working for some reason, had to overwrite pygmented_markdown method
def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    pygmented_body = markdown.markdown(prerendered_body, extensions=FLATPAGES_MARKDOWN_EXTENSIONS)
    return pygmented_body

# Some configuration, ensures
# 1. Pages are loaded on request.
# 2. File name extension for pages is Markdown.

FLATPAGES_EXTENSION = ['.md', '.markdown']
FLATPAGES_HTML_RENDERER = prerender_jinja
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'attr_list', 'md_in_html']
FLATPAGES_AUTO_RELOAD = True


app.config.from_object(__name__)
flatpages = FlatPages(app)

from website import utils, database, images, errors, views
