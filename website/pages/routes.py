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
from .models import Pages
from .services import render_page_args


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


@bp.route('/results/')
def results_page():
    ''' render results page '''

    return flask.render_template(
        'generic/page.html.j2',
        **render_page_args(name='results')
        )


@bp.route('/sponsors/')
def sponsors_page():
    ''' render sponsors page '''

    return flask.render_template(
        'generic/page.html.j2',
        **render_page_args(name='sponsors')
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
    wp_posts = Pages.query(filepath__contains=wp_dir)

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
        **render_page_args(metadata__slug=path_requested)
        )


# TODO fix slugs in model
# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@bp.route("/page/<path_requested>/")
def serve_page(path_requested):
    ''' render generic page '''

    return flask.render_template(
        'generic/page.html.j2',
        **render_page_args(slug=path_requested)
        )


@bp.endpoint("pages.serve_test")
def serve_test():
    ''' render test page '''
    return flask.render_template('generic/test.html.j2')
