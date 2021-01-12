from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)
	bootstrap.init_app(app)

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	from app.interrogation import bp as interrogation_bp
	app.register_blueprint(interrogation_bp)

	from app.trash import bp as trash_bp
	app.register_blueprint(trash_bp)
	return app