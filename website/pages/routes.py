"""
View functions for pages with content stored in markdown files

Access to data via models and services layers.
Page: ODM, mongoengine
Pages: Utility class shortcut for collection queries

Templates used:
- generic/page.html.j2
- contact.html.j2
- articles/index.html.j2
- articles/article.html.j2

"""
from datetime import datetime

import flask

from . import pages_bp as bp
from .models import Page


def render_page_args(page=None, **query):
    """ Shortcut function to help render standard page """

    if not page:
        page = Page.objects.get_or_404(**query)
    sidebar = Page.objects.get(name='sidebar')

    return dict(
        content=page.render_content(),
        side=sidebar.render_content(),
        title=page.title,
        description=page.description,
        keywords=page.keywords,
    )


@bp.app_context_processor
def inject_data():
    ''' global context for all templates '''
    this_year = datetime.now().year
    return dict(
        year=this_year,
        )


@bp.route('/')
def home_page():
    ''' render homepage '''
    return flask.render_template(
        'home.html.j2',
        title="Home",
        description="The homepage of Tom Hall, Archer and Coach",
        keywords="Archery, Athlete, Profile",
        img_layout={'min-width: 110ch': '60vw', None: '95vw'},
        )


@bp.route('/contact/')
def contact_page():
    ''' render contacts page '''
    return flask.render_template(
        'contact.html.j2',
        **render_page_args(name='contact')
        )


@bp.route('/articles/')
def serve_articles_index():
    ''' render articles index page '''
    # Selects posts with a PATH starting with wpexport/_posts
    wp_dir = flask.current_app.config["VIEW_POSTS_DIR_WP"]
    wp_posts = Page.objects(filepath__contains=wp_dir)

    return flask.render_template(
        'articles/index.html.j2',
        title="Articles",
        pages=wp_posts
        )


# TODO fix slugs in model
@bp.route("/articles/<path:path_requested>/")
def serve_article(path_requested):
    ''' render article page eg path_requested="archive/title" '''

    return flask.render_template(
        'articles/article.html.j2',
        # query embedded metadata object
        **render_page_args(slug=path_requested)
        )


@bp.route("/page/<slug>/")
def serve_page(slug):
    ''' render generic page by name '''
    print(slug)
    page = Page.objects.get_or_404(slug=slug)

    if not page.visible():
        flask.abort(403)

    return flask.render_template(
        'generic/page.html.j2',
        **render_page_args(page=page)
        )


@bp.endpoint("pages.serve_test")
def serve_test():
    ''' render test page '''
    return flask.render_template('generic/test.html.j2')
