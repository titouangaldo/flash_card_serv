from app.trash import bp
from app import db
from flask import redirect, url_for
from app.models import Carnet

@bp.route('/trash')
def trash():
	trash_carnet = Carnet.query.filter(Carnet.name == "_Trash_").first()
	return redirect(url_for('main.carnet', id_carnet=trash_carnet.id))