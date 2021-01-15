from flask import Blueprint

bp = Blueprint('latex', __name__)

from app.latex import routes