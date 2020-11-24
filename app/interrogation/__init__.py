from flask import Blueprint

bp = Blueprint('interrogation', __name__)

from app.interrogation import routes