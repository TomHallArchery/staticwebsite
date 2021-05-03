from website import app, flatpages
import flask
import os
from functools import partial

# Add highlighted primary component blocks for layout design
# flask.render_template = partial(flask.render_template, highlight_blocks=True)

# add filtering method to flatpages object
def filter_pages(dir):
    ''' return list of flask flatpage objects from subdirectory of "pages" '''
    return list(page for page in flatpages if os.path.dirname(page.path) == dir)
flatpages.filter = filter_pages

WP_POSTS_DIR = 'articles/archive'

@app.route('/')
def serve_home():
    return flask.render_template('generic/home.html.j2',
        title="Home",
        description = "The homepage of Tom Hall, Archer and Coach",
        keywords = "Archery, Athlete, Profile",
        )

@app.route('/results/')
def serve_results():
    results = flatpages.get_or_404('results')
    return flask.render_template('generic/page.html.j2',
        page=results,
        title='Results')

@app.route('/sponsors/')
def serve_sponsors():
    sponsors = flatpages.get_or_404('sponsors')
    return flask.render_template('generic/page.html.j2',
        page=sponsors,
        **sponsors.meta)

@app.route('/articles/')
def serve_articles():
    # Selects posts with a PATH starting with wpexport/_posts
    posts = filter_pages(WP_POSTS_DIR )

    return flask.render_template('articles/index.html.j2',
        title="Articles",
        pages=posts
        )

# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/<path:path_requested>/")
def serve_page(path_requested):

    path = os.path.split(path_requested)

    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template('generic/page.html.j2',
        page=flatpage,
        **flatpage.meta
        )
