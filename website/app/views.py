from app import app, flatpages
import flask
import os
from functools import partial

# Add highlighted primary component blocks for layout design
# flask.render_template = partial(flask.render_template, highlight_blocks=True)

# add filtering method to flatpages object
def filter_pages(dir):
    ''' return list of flask flatpage objects from subdirectory of "pages" '''
    return [page for page in flatpages if os.path.dirname(page.path) == dir]
flatpages.filter = filter_pages


@app.route('/')
def serve_home():
    return flask.render_template('generic/home.j2',
        title="Home",
        description = "The homepage of Tom Hall, Archer and Coach",
        keywords = "Archery, Athlete, Profile",
        )

@app.route('/results/')
def serve_results():
    results = flatpages.get_or_404('results')
    return flask.render_template('generic/page.j2',
        page=results,
        title='Results')

@app.route('/sponsors/')
def serve_sponsors():
    sponsors = flatpages.get_or_404('sponsors')
    return flask.render_template('generic/page.j2',
        page=sponsors,
        title='Results')

@app.route('/articles/')
def serve_articles():
    # Coded just to pick up wordpress markdown pages for now
    # will extend to my own identifier
    # posts = filter_pages('wpexport/_posts')
    return flask.render_template('articles/index.j2',
        title="Articles",
        links=flatpages.filter('wpexport/_posts'),
        )

# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/articles/<path:path_requested>/")
def serve_article(path_requested):
    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template(
        'generic/page.j2',
        page=flatpage,
        **flatpage.meta
        )
