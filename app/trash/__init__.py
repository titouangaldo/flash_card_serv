from flask import Blueprint

bp = Blueprint('trash', __name__)

from app.trash import routes