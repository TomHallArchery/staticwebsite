from app import app, flatpages
import flask
from functools import partial

# Add highlighted primary component blocks for layout design
# flask.render_template = partial(flask.render_template, highlight_blocks=True)

@app.route('/')
def serve_home():
    links = [link for link in flatpages]
    return flask.render_template('generic/home.j2',
        title="Home",
        description = "The homepage of Tom Hall, Archer and Coach",
        keywords = "Archery, Athlete, Profile",
        links=links,
        )

@app.route('/articles/')
def serve_articles():
    return flask.render_template('articles/index.j2', title="Articles")



# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/<path:path_requested>/")
def serve_page(path_requested):
    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template(
        'generic/page.j2',
        page=flatpage,
        **flatpage.meta
        )
