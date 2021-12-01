import flask
import frontmatter as fmr

from website import utils
from .. import flatpages
from . import pages_bp
from .models import Page


@pages_bp.route('/results/')
def results_page():
    ''' render results page '''
    results = flatpages.get_or_404('results')
    sidebar = flatpages.get('sidebar')

    return flask.render_template(
        'generic/page.html.j2',
        page=results,
        side=sidebar,
        **results.meta)


@pages_bp.route('/sponsors/')
def sponsors_page():
    ''' render sponsors page '''
    sponsors = flatpages.get_or_404('sponsors')
    sidebar = flatpages.get('sidebar')
    return flask.render_template(
        'generic/page.html.j2',
        page=sponsors,
        side=sidebar,
        **sponsors.meta)


@pages_bp.route('/contact/')
def contact_page():
    ''' render contacts page '''
    contact = flatpages.get_or_404('contact')
    return flask.render_template(
        'contact.html.j2',
        page=contact,
        **contact.meta)


@pages_bp.route('/articles/')
def serve_articles_index():
    ''' render articles index page '''
    # Selects posts with a PATH starting with wpexport/_posts
    wp_dir = flask.current_app.config["VIEW_POSTS_DIR_WP"]
    wp_posts = utils.filter_pages(wp_dir)
    return flask.render_template(
        'articles/index.html.j2',
        title="Articles",
        pages=wp_posts
        )


@pages_bp.route("/articles/<path:path_requested>/")
def serve_article(path_requested):
    ''' render article page eg path_requested="archive/title" '''
    # reappend 'article/' to front of path
    # as has been stripped off by the route selector

    page = Page.objects.get_or_404(slug=path_requested)
    flatpage = fmr.load(page.filepath)
    flatpage.metadata.update(layout='default')
    return flask.render_template(
        'articles/article.html.j2',
        content=flatpage.content,
        **flatpage.metadata
        )


# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@pages_bp.route("/page/<path_requested>/")
def serve_page(path_requested):
    ''' render generic page '''
    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template(
        'generic/page.html.j2',
        page=flatpage,
        side=flatpages.get('sidebar'),
        **flatpage.meta
        )
