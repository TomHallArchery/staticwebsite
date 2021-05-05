from website import app, flatpages, clean_flatpage_metas
import flask
import os
from datetime import datetime
from functools import partial

# Add highlighted primary component blocks for layout design
# flask.render_template = partial(flask.render_template, highlight_blocks=True)

WP_POSTS_DIR = 'article/archive'

# add filtering method to flatpages object
def filter_pages(dir):
    ''' return list of flask flatpage objects from subdirectory of "pages" '''
    return list(page for page in flatpages if os.path.dirname(page.path) == dir)


@app.before_request
def reload_flatpages():
    clean_flatpage_metas()

@app.context_processor
def inject_year():
    this_year = datetime.now().year
    return dict(year=this_year)

@app.route('/')
def serve_home():
    return flask.render_template('generic/home.html.j2',
        title="Home",
        # move metadata into markdown? even if not calling from generic page tempalate
        # could still allow dict unpacking of metadata
        description = "The homepage of Tom Hall, Archer and Coach",
        keywords = "Archery, Athlete, Profile",
        )

@app.route('/results/')
def serve_results():
    results = flatpages.get_or_404('results')
    return flask.render_template('generic/page.html.j2',
        page=results,
        **results.meta)

@app.route('/sponsors/')
def serve_sponsors():
    sponsors = flatpages.get_or_404('sponsors')
    return flask.render_template('generic/page.html.j2',
        page=sponsors,
        **sponsors.meta)

@app.route('/contact/')
def contact_page():
    contact = flatpages.get_or_404('contact')
    return flask.render_template('generic/contact.html.j2',
        page=contact,
        **contact.meta)

@app.route('/articles/')
def serve_articles():
    # Selects posts with a PATH starting with wpexport/_posts
    posts = filter_pages(WP_POSTS_DIR)
    return flask.render_template('articles/index.html.j2',
        title="Articles",
        pages=posts
        )

@app.route("/article/<path:path_requested>/")
def serve_article(path_requested):

    # reappend 'article/' to front of path as has been stripped off by the route selector
    path = os.path.join('article', path_requested)
    flatpage = flatpages.get_or_404(path)

    return flask.render_template('articles/article.html.j2',
        page=flatpage,
        **flatpage.meta
        )

# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/<path_requested>/")
def serve_page(path_requested):

    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template('generic/page.html.j2',
        page=flatpage,
        **flatpage.meta
        )
