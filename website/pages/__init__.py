from flask import Blueprint

pages_bp = Blueprint('pages_bp', __name__)

from . import routes
from .services import prerender_jinja
