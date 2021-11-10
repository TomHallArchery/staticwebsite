import os
from datetime import datetime

import flask
from flask import current_app as app
from website import images, utils, flatpages


@app.before_request
def reload_flatpages():
    utils.clean_flatpage_metas(flatpages)


@app.before_first_request
def process_all_images():
    ''' process img/src into thumbnails in img/out '''
    print("Processing images")
    all_imgs = images.SourceImages()
    all_imgs.add_to_db()
    all_imgs.process(reprocess=app.config['REPROC_IMAGES'])


@app.context_processor
def inject_data():
    this_year = datetime.now().year
    return dict(
        year=this_year,
        img_sizes=app.config.get('IMG_WIDTHS'),
        img_layout=app.config.get('IMG_DISPLAY_WIDTHS'),
        src=utils.src,
        srcset=utils.srcset,
        sizes=utils.sizes,
        )


app.add_template_filter(images.responsive_images)

# ===============
# #ROUTES
# ===============


@app.route('/')
def home_page():
    return flask.render_template(
        'home.html.j2',
        title="Home",
        # move metadata into markdown?
        # even if not calling from generic page tempalate
        # could still allow dict unpacking of metadata
        description="The homepage of Tom Hall, Archer and Coach",
        keywords="Archery, Athlete, Profile",
        img_layout={'min-width: 110ch': '60vw', None: '95vw'},
        )


@app.route('/results/')
def results_page():
    results = flatpages.get_or_404('results')
    sidebar = flatpages.get('sidebar')
    return flask.render_template(
        'generic/page.html.j2',
        page=results,
        side=sidebar,
        **results.meta)


@app.route('/sponsors/')
def sponsors_page():
    sponsors = flatpages.get_or_404('sponsors')
    sidebar = flatpages.get('sidebar')
    return flask.render_template(
        'generic/page.html.j2',
        page=sponsors,
        side=sidebar,
        **sponsors.meta)


@app.route('/contact/')
def contact_page():
    contact = flatpages.get_or_404('contact')
    return flask.render_template(
        'contact.html.j2',
        page=contact,
        **contact.meta)


@app.route('/articles/')
def serve_articles_index():
    # Selects posts with a PATH starting with wpexport/_posts
    wp_posts = utils.filter_pages(app.config["VIEW_POSTS_DIR_WP"])
    return flask.render_template(
        'articles/index.html.j2',
        title="Articles",
        pages=wp_posts
        )


@app.route("/articles/<path:path_requested>/")
def serve_article(path_requested):
    ''' eg path_requested="archive/title" '''
    # reappend 'article/' to front of path
    # as has been stripped off by the route selector
    path = os.path.join('articles', path_requested)
    flatpage = flatpages.get_or_404(path)

    return flask.render_template(
        'articles/article.html.j2',
        page=flatpage,
        **flatpage.meta
        )


# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/page/<path_requested>/")
def serve_page(path_requested):

    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template(
        'generic/page.html.j2',
        page=flatpage,
        side=flatpages.get('sidebar'),
        **flatpage.meta
        )


@app.route("/test/")
def serve_test():
    ''' render test page '''
    print("TESTVAR: ", app.config["VIEW_TEST"])
    if not app.config["VIEW_TEST"]:
        flask.abort(404)
    return flask.render_template('generic/test.html.j2')
