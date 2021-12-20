"""
View functions for pages with content stored in markdown files

Access to data via models and services layers.
Page: ODM, mongoengine
Pages: Utility class shortcut for collection queries
Content: utility function, returns formatted body html
from Page objects referenced file.
Meta: Utility function, returns metadata dictionary
from Page objects referenced file.

Templates used:
- generic/page.html.j2
- contact.html.j2
- articles/index.html.j2
- articles/article.html.j2



"""
import flask

from . import pages_bp
from .models import Pages
from .services import content, meta


def _render_page_args(**query):
    """ Shortcut function to help render standard page """
    page = Pages.get_or_404(**query)
    sidebar = Pages.get(name='sidebar')

    return dict(
        content=content(page),
        side=content(sidebar),
        title=page.metadata.title,
        description=page.metadata.description,
        keywords=page.metadata.keywords,
    )


@pages_bp.route('/results/')
def results_page():
    ''' render results page '''

    return flask.render_template(
        'generic/page.html.j2',
        **_render_page_args(name='results')
        )


@pages_bp.route('/sponsors/')
def sponsors_page():
    ''' render sponsors page '''

    return flask.render_template(
        'generic/page.html.j2',
        **_render_page_args(name='sponsors')
        )


@pages_bp.route('/contact/')
def contact_page():
    ''' render contacts page '''
    return flask.render_template(
        'contact.html.j2',
        **_render_page_args(name='contact')
        )


@pages_bp.route('/articles/')
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
@pages_bp.route("/articles/<path:path_requested>/")
def serve_article(path_requested):
    ''' render article page eg path_requested="archive/title" '''

    return flask.render_template(
        'articles/article.html.j2',
        **_render_page_args(slug=path_requested)
        )


# TODO fix slugs in model
# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@pages_bp.route("/page/<path_requested>/")
def serve_page(path_requested):
    ''' render generic page '''

    return flask.render_template(
        'generic/page.html.j2',
        **_render_page_args(slug=path_requested)
        )
