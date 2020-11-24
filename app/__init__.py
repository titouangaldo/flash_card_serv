from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	from app.interrogation import bp as interrogation_bp
	app.register_blueprint(interrogation_bp)

	db.init_app(app)
	migrate.init_app(app, db)

	return app