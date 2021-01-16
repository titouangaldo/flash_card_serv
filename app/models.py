from app import db
from datetime import datetime
import enum
import logging

logger = logging.getLogger(__name__)

class Question(db.Model):
	__tablename__ = 'question'
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(1024), index=True, unique=False)
	id_answer = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
	need_paper= db.Column(db.Boolean)

	evaluation = db.relationship('Evaluation', backref='question', lazy='dynamic')


	def __repr__(self):
		return f'<Question{self.id} {self.content} [solution={self.id_answer}] [need_paper={self.need_paper}]>'

	def edit_content(self, content):
		self.content=content
		db.session.commit()
		logger.info(f"Question edited: {self}")

	def eraze(self):
		db.session.delete(self)
		db.session.commit()
		logger.info(f"Question deleted: {self}")

class Answer(db.Model):
	__tablename__ = 'answer'
	id = db.Column(db.Integer, primary_key=True)
	id_carnet = db.Column(db.Integer, db.ForeignKey('carnet.id'), nullable=False)
	text_content = db.Column(db.String(1024), index=True, unique=False)
	questions = db.relationship('Question', backref='solution', lazy='dynamic')


	def __repr__(self):
		return f'<Answer{self.id} {self.text_content} [carnet={self.id_carnet}]>'

	def eraze(self):
		for q in self.questions:
			q.eraze()

		db.session.delete(self)
		db.session.commit()
		logger.info(f"Answer erased: {self}")

	def move(self, id_carnet):
		self.id_carnet = id_carnet
		db.session.commit()
		logger.info(f"Question moved: {self}")

	def edit_content(self, text_content):
		self.text_content=text_content
		db.session.commit()
		logger.info(f"Question edited: {self}")

	def add_question(self, content, need_paper=False):
		question = Question(content=content, need_paper=need_paper, solution=self)
		db.session.add(question)
		db.session.commit()

		logger.info(f"Question add")


class Carnet(db.Model):
	__tablename__ = 'carnet'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=False)

	id_parent_carnet = db.Column(db.Integer, db.ForeignKey('carnet.id'), nullable=True)
	children_carnets = db.relationship('Carnet', backref=db.backref('parent', remote_side=[id]))
	
	answers = db.relationship('Answer', backref='carnet', lazy='dynamic')


	def __repr__(self):
		return f'<Carnet{self.id} {self.name} [parent={Carnet.query.get(self.id_parent_carnet).name if self.id_parent_carnet else ""}]>'

	def eraze(self):
		for a in self.answers:
			a.eraze()

		for child in self.children_carnets:
			child.eraze()

		db.session.delete(self)
		db.session.commit()
		logger.info(f"Carnet erazed: {self}")

	def move(self, id_carnet):
		self.id_parent_carnet = id_carnet
		print(self.id_parent_carnet)
		db.session.commit()

		logger.info(f"Carnet moved: {self}")

	def add_answer(self, text_content):
		db.session.add(Answer(text_content=text_content, carnet=self))
		db.session.commit()
		logger.info(f"Answer added to carnet {self}")

	def add_carnet(self, name):
		db.session.add(Carnet(name=name, parent=self))
		db.session.commit()
		logger.info(f"carnet added to carnet {self}")		

	def get_questions(self):
		questions = []
		for a in self.answers:
			questions += a.questions
		return questions

	def get_all_questions(self):
		questions = self.get_questions()
		for c in self.children_carnets:
			questions += c.get_all_questions()
		return questions

class autoeval(enum.Enum):
	not_known = 1
	not_enought = 2
	known = 3
	mastered = 4

class Evaluation(db.Model):
	__tablename__ = 'evaluation'
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	id_question = db.Column(db.Integer, db.ForeignKey('question.id'))
	result = db.Column(db.Enum(autoeval))

	def __repr__(self):
		return f"Eval [id_question: {self.id_question}] {self.result} -- {self.timestamp}"






