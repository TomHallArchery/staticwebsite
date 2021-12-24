from flask import Blueprint

pages_bp = Blueprint('pages', __name__)

from . import routes, cli
from .services import prerender_jinja