import flask
import markdown
from flask import render_template_string, Markup
from flask_flatpages import FlatPages

app = flask.Flask('website') #any name here works EXCEPT 'app'??
# static_folder='static'
# template_folder='templates'

# Setting flatpages extensions wasn't working for some reason, had to overwrite pygmented_markdown method
def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    pygmented_body = markdown.markdown(prerendered_body, extensions=FLATPAGES_MARKDOWN_EXTENSIONS)
    return pygmented_body

# dirty:
# strip '---' from ._meta attribute of page objects to allow flatpages to work with yaml delimiter
def clean_flatpage_metas():
    for page in flatpages:
        page._meta = page._meta.strip('---')

# Some configuration, ensures
# 1. Pages are loaded on request.
# 2. File name extension for pages is Markdown.

FLATPAGES_EXTENSION = ['.md', '.markdown']
FLATPAGES_HTML_RENDERER = prerender_jinja
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'attr_list']
FLATPAGES_AUTO_RELOAD = True

print(app.root_path)
print(app.static_folder)
print(app.template_folder)

app.config.from_object('app')
flatpages = FlatPages(app)
clean_flatpage_metas()

@app.before_request
def reload_flatpages():
    clean_flatpage_metas()

from app import views, errors
