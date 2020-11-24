from app import create_app, db
from app.models import Carnet, Answer, Question, Evaluation

app = create_app()

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'Carnet': Carnet, 'Answer': Answer, 'Question': Question,\
		'Evaluation': Evaluation}