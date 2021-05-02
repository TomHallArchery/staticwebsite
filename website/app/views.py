from app import app, flatpages
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

WP_POSTS_DIR = 'wpexport/_posts'

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
    # Selects posts with a PATH starting with wpexport/_posts and trim that directory from the link
    posts = filter_pages(WP_POSTS_DIR )
    cannonical_links = [os.path.join('WP', os.path.basename(post.path)) for post in posts]

    return flask.render_template('articles/index.j2',
        title="Articles",
        pages= zip(posts,cannonical_links)
        )

# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/articles/<path:path_requested>/")
def serve_article(path_requested):

    print("PATH:", path_requested)
    path = os.path.split(path_requested)
    # If requesting direct shorter link:
    if path[0] == 'WP':
        flatpage = flatpages.get_or_404(os.path.join(WP_POSTS_DIR , path[1]))
    # Else return full link
    else:
        flatpage = flatpages.get_or_404(os.path.join('articles', path_requested))

    return flask.render_template(
        'generic/page.j2',
        page=flatpage,
        **flatpage.meta
        )
