from flask import Blueprint

images_bp = Blueprint('images', __name__)

# from . import routes
from .services import responsive_images
