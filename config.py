import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    ''' Standard configuration '''
    # MongoDB config
    MONGODB_SETTINGS = {
        'db': 'dev',
        'port': 5009,
        'username': 'app',
        'password': os.environ.get("DB_PWORD"),
        'authentication_source': 'admin'
    }

    # Flask flatpages configuration
    # 1. Pages are loaded on request.
    # 2. File name extension for pages is Markdown.
    CONTENT_ROOT = 'website/content'
    CONTENT_EXTENSION = ['.md', '.markdown']  # 2
    CONTENT_HTML_RENDERER = 'website.pages.services.prerender_jinja'
    CONTENT_MARKDOWN_EXTENSIONS = ['attr_list', 'md_in_html']

    # Images config
    IMG_ROOT = 'website/static/img/'
    IMG_SOURCE_DIR = 'src'
    IMG_OUTPUT_DIR = 'out'
    IMG_WIDTHS = [2000, 1600, 1200, 800, 400]
    IMG_DEFAULT_WIDTH = 1200
    IMG_DISPLAY_WIDTHS = {'min-width: 110ch': '60vw', None: '95vw'}
    IMG_FORMATS = ('.jpg', '.webp')
    REPROC_IMAGES = os.environ.get('REPROC_IMAGES', False)

    # Views config
    VIEW_POSTS_DIR_WP = 'archive'
    VIEW_TEST = os.environ.get('VIEW_TEST', False)

    # External Depedancies
    ALPINE_VERSION = '3.4.2'
    ALPINE_FILE_PATH = Path('website', 'static', 'js', 'alpine.js')

    # CSS config
    CSS_PREPROCESSOR = 'sass'
    CSS_SRC_DIR = Path('website', 'static', 'scss')
    CSS_OUT_DIR = Path('website', 'static', 'css')

    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevConfig(Config):
    ''' Development configuration: running local flask server '''

    # from run.py
    ENV = 'DEVELOPMENT'
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    IMG_URL = "/static/img/out/"
    VIEW_TEST = True


class BuildConfig(Config):
    ''' Build configuration: freezing to static files and serving locally '''

    ENV = 'PRODUCTION'
    IMG_URL = "http://localhost:5003/"

    # Manually add fonts to list to incorporate into freezer
    FONTS = {  # tuple: vf, latin, woff2
        'Roboto_Slab': 'RobotoSlab-VariableFont_wght-Latin.woff2',
        'Public_Sans': 'PublicSans-VariableFont_wght-Min.woff2',
    }

    # Frozen Flask config
    FREEZER_DESTINATION_IGNORE = ['404.html', 'netlify.toml']
    FREEZER_STATIC_IGNORE = [
        'fonts/',
        'scss/',
        'img/',
        'css/',
        'favicon/',
        'js/',
        '.DS_Store',
    ]
    FREEZER_IGNORE_404_NOT_FOUND = True

    CSS_OUT_DIR = Path('website', 'build', 'static', 'css')

    # Flask-HTMLmin
    MINIFY_HTML = True


class DeployConfig(BuildConfig):
    '''
    Deploy configuration: freezing to static files and deploying to netlify
    '''

    IMG_URL = "https://cdn.tomhallarchery.com/"
    MONGODB_DB = 'website'

    # Pynetlify config
    NETLIFY_AUTH_TOKEN = os.environ.get('NETLIFY_AUTH_TOKEN')
    NETLIFY_ROOT_ID = os.environ.get('NETLIFY_ROOT_ID')
    NETLIFY_CDN_ID = os.environ.get('NETLIFY_CDN_ID')


class TestConfig():
    pass
