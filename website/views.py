from website import app, flatpages, utils
from website.images import SIZES
import flask
import os
from datetime import datetime
from functools import partial

# Add highlighted primary component blocks for layout design
# flask.render_template = partial(flask.render_template, highlight_blocks=True)

IMAGES_URL = "https://cdn.tomhallarchery.com/"
WP_POSTS_DIR = 'articles/archive'


@app.before_request
def reload_flatpages():
    utils.clean_flatpage_metas(flatpages)

@app.context_processor
def inject_data():
    this_year = datetime.now().year
    default_img_widths = {'60vw': 'min-width: 110ch', '95vw': None}
    return dict(
        year=this_year,
        img_url=IMAGES_URL,
        img_sizes=SIZES,
        img_layout=default_img_widths,
        srcset=utils.srcset,
        sizes=utils.sizes,

        )

@app.template_filter()
def responsive_images(html, conditions, img_url):
    parser = utils.parse_html(html)
    imgs = parser.getElementsByTagName('img')
    for img in imgs:
        print(repr(img))
        if img.src:
            if not img.width:
                img.width = '1600'
            widths = filter(lambda x: x<int(img.width), SIZES)
            print(widths)
            path, fname, ext = utils.split_filename(img.src)
            img.src = os.path.join(img_url, f'{fname}_{img.width}{ext}')
            img.srcset = utils.srcset(img_url, fname, widths, 'jpg')
            img.sizes = utils.sizes(conditions)

    return parser.toHTML()


@app.route('/')
def home_page():
    return flask.render_template('generic/home.html.j2',
        title="Home",
        # move metadata into markdown? even if not calling from generic page tempalate
        # could still allow dict unpacking of metadata
        description = "The homepage of Tom Hall, Archer and Coach",
        keywords = "Archery, Athlete, Profile",
        img_layout = {'80vw': 'min-width: 110ch', '95vw': None}
        )

@app.route('/results/')
def results_page():
    results = flatpages.get_or_404('results')
    sidebar = flatpages.get('sidebar')
    return flask.render_template('generic/page.html.j2',
        page=results,
        side=sidebar,
        **results.meta)

@app.route('/sponsors/')
def sponsors_page():
    sponsors = flatpages.get_or_404('sponsors')
    sidebar = flatpages.get('sidebar')
    return flask.render_template('generic/page.html.j2',
        page=sponsors,
        side=sidebar,
        **sponsors.meta)

@app.route('/contact/')
def contact_page():
    contact = flatpages.get_or_404('contact')
    return flask.render_template('contact.html.j2',
        page=contact,
        **contact.meta)

@app.route('/articles/')
def articles_page():
    # Selects posts with a PATH starting with wpexport/_posts
    posts = utils.filter_pages(WP_POSTS_DIR)
    return flask.render_template('articles/index.html.j2',
        title="Articles",
        pages=posts
        )

@app.route("/articles/<path:path_requested>/")
def serve_article(path_requested):
    ''' eg path_requested="archive/title" '''
    # # reappend 'article/' to front of path as has been stripped off by the route selector
    path = os.path.join('articles', path_requested)
    flatpage = flatpages.get_or_404(path)

    return flask.render_template('articles/article.html.j2',
        page=flatpage,
        **flatpage.meta
        )

# URL Routing - Flat Pages
# Retrieves the page specified by the url /path_requested
@app.route("/<path_requested>/")
def serve_page(path_requested):

    flatpage = flatpages.get_or_404(path_requested)
    return flask.render_template('generic/page.html.j2',
        page=flatpage,
        side=flatpages.get('sidebar'),
        **flatpage.meta
        )
