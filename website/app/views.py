from app import app, flatpages
import flask


@app.route('/')
def serve_home():
    links = [link for link in flatpages]
    return flask.render_template('generic/home.j2', title="Home", links=links)

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
        page_content=flatpage
        )
