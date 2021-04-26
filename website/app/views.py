from app import app, flatpages
import flask


@app.route('/')
def serve_home():
    return flask.render_template('pages/home.html', title="Home")

@app.route('/articles/')
def serve_articles():
    return flask.render_template('articles/index.html', title="Articles")

# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/<path:path_requested>/")
def serve_page(path_requested):
    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template(
        'pages/genericpage.html',
        page_content=flatpage)
