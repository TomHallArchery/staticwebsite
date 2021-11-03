import os
import flask
import markdown
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Setting flatpages extensions wasn't working for some reason, had to overwrite pygmented_markdown method
def prerender_jinja(text):
    prerendered_body = flask.render_template_string(flask.Markup(text))
    pygmented_body = markdown.markdown(prerendered_body, extensions=Config.FLATPAGES_MARKDOWN_EXTENSIONS)
    return pygmented_body

class Config:
    # MongoDB config
    DB_PORT = 5009
    DB_PWD = os.environ.get("DB_PWORD")
    DB_CONFIG = 'database/db.conf'

    # Flask flatpages configuration
    # 1. Pages are loaded on request.
    # 2. File name extension for pages is Markdown.
    FLATPAGES_EXTENSION = ['.md', '.markdown'] #2
    FLATPAGES_HTML_RENDERER = prerender_jinja
    FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'attr_list', 'md_in_html']
    FLATPAGES_AUTO_RELOAD = True #1

    # Images config
    IMG_ROOT = 'website/static/img/'
    IMG_SOURCE_DIR = 'src'
    IMG_OUTPUT_DIR = 'out'
    IMG_WIDTHS = [2000, 1600, 1200, 800, 400]
    IMG_DEFAULT_WIDTH = '1200'
    IMG_DISPLAY_WIDTHS = {'min-width: 110ch': '60vw', None: '95vw'}
    IMG_FORMATS = ('.jpg', '.webp')

    # Views config
    VIEW_POSTS_DIR_WP = 'articles/archive'
    VIEW_TEST = os.environ.get('TEST')

    # External Depedancies
    ALPINE = {
        'url': "https://unpkg.com/alpinejs@3.4.2/dist/cdn.min.js",
        'fpath': Path('website', 'static', 'js', 'alpine.js')
    }

    # CSS config
    CSS_PREPROCESSOR = 'sass'
    CSS_SRC_DIR = Path('website', 'static', 'scss')
    CSS_OUT_DIR = Path('website', 'static', 'css')

class RunConfig(Config):
    # from run.py
    ENV = 'DEVELOPMENT'
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    IMG_URL = "/static/img/out/"
    REPROC_IMAGES = os.environ.get('REPROC_IMAGES', False)
    VIEW_TEST = True

class BuildConfig(Config):
    ENV = 'PRODUCTION'
    IMG_URL = "http://localhost:5003/"

    # Manually add fonts to list to incorporate into freezer
    FONTS = {
    'Roboto_Slab' : 'RobotoSlab-VariableFont_wght-Latin.woff2', #tuple: vf, latin, woff2
    'Public_Sans' : 'PublicSans-VariableFont_wght-Min.woff2'
    }

    # Frozen Flask config
    FREEZER_DESTINATION_IGNORE = ['404.html', 'netlify.toml']
    FREEZER_STATIC_IGNORE = [
    'fonts/', 'scss/', 'img/', 'css/', 'favicon/', 'js/', '.DS_Store'
    ]

    CSS_OUT_DIR = Path('website', 'build', 'static', 'css')

    # Flask-HTMLmin
    MINIFY_HTML = True

class DeployConfig(BuildConfig):

    IMG_URL = "https://cdn.tomhallarchery.com/"

    # Pynetlify config
    NETLIFY_AUTH_TOKEN = os.environ.get('NETLIFY_AUTH_TOKEN')
    NETLIFY_ROOT_ID = os.environ.get('NETLIFY_ROOT_ID')
    NETLIFY_CDN_ID = os.environ.get('NETLIFY_CDN_ID')
