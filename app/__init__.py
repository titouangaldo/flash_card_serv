from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from config import Config
import logging


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


console_log_handler = logging.StreamHandler()
console_log_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | [%(levelname)s] %(name)s: %(message)s')
console_log_handler.setFormatter(formatter)
logger.addHandler(console_log_handler)

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
	
	from app.latex import bp as latex_bp
	app.register_blueprint(latex_bp)

	return app