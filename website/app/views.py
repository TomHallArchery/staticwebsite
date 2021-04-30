from app import app, flatpages
import flask
from functools import partial

# Add highlighted primary component blocks for layout design
# flask.render_template = partial(flask.render_template, highlight_blocks=True)

@app.route('/')
def serve_home():
    return flask.render_template('generic/home.j2',
        title="Home",
        description = "The homepage of Tom Hall, Archer and Coach",
        keywords = "Archery, Athlete, Profile",
        )

@app.route('/articles/')
def serve_articles():
    # Coded just to pick up wordpress markdown pages for now
    # will extend to my own identifier
    article_links = [link for link in flatpages if 'wordpress_id' in link.meta]
    return flask.render_template('articles/index.j2',
        title="Articles",
        links=article_links,
        )



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
