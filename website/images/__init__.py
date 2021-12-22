from flask import Blueprint

images_bp = Blueprint('images', __name__)

from . import cli
from .services import responsive_images
