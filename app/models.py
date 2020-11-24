from app import db

class Question(db.Model):
	__tablename__ = 'question'
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(1024), index=True, unique=False)
	id_answer = db.Column(db.Integer, db.ForeignKey('answer.id'))
	need_paper= db.Column(db.Boolean)

	def __repr__(self):
		return f'<Question{self.id} {self.content} [solution={self.id_answer}] [need_paper={self.need_paper}]>'

	def edit_content(self, content):
		self.content=content
		db.session.commit()

	def eraze(self):
		db.session.delete(self)
		db.session.commit()

class Answer(db.Model):
	__tablename__ = 'answer'
	id = db.Column(db.Integer, primary_key=True)
	id_carnet = db.Column(db.Integer, db.ForeignKey('carnet.id'))
	text_content = db.Column(db.String(1024), index=True, unique=False)
	questions = db.relationship('Question', backref='solution', lazy='dynamic')

	def __repr__(self):
		return f'<Answer{self.id} {self.text_content} [carnet={self.id_carnet}]>'

	def eraze(self):
		for q in self.questions:
			q.eraze()

		db.session.delete(self)
		db.session.commit()

	def edit_content(self, text_content):
		self.text_content=text_content
		db.session.commit()

	def add_question(self, content, need_paper=False):
		db.session.add(Question(content=content, need_paper=need_paper, solution=self))
		db.session.commit()


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

	def add_answer(self, text_content):
		db.session.add(Answer(text_content=text_content, carnet=self))
		db.session.commit()

	def add_carnet(self, name):
		db.session.add(Carnet(name=name, parent=self))
		db.session.commit()

	def get_questions(self):
		questions = []
		for a in self.answers:
			for q in a.questions:
				questions.append(q)
		return questions

	def get_all_questions(self):
		questions = self.get_questions()
		print(questions)
		for c in self.children_carnets:
			questions += c.get_questions()
		print(questions)
		return questions



"""

Carnet2 = Carnet(2, "english")
Answer1 = Answer(1, id_carnet=2, text_content="abide abode abode")
Question1 = Question(1, id_answer=1, content="conjugaison de respecter, se conformer à")

Answer2 = Answer(2, id_carnet=2, text_content="arise arose arisen")
Question2 = Question(2, id_answer=2, content="conjugason de survenir")


Carnet1 = Carnet(1, "maths")
Answer3 = Answer(3, id_carnet=1, text_content="\\(a^2 + b^2 = c^2\\)")
Question3 = Question(3, id_answer=3, content="enoncer le théorème de pythagore")

Carnet3 = Carnet(3, "Analyse", id_parent_carnet=1)
Answer4 = Answer(4, id_carnet=3, text_content="Soient \\((X,d)\\) un espace compact et (E,|| \\(\\dot\\) ||) un espace de Banach.\n On considère une partie A de C(X,E) qui est A est uniformement équicontinue et ponctuellement d'adhérence compact. \n Alors A est dense dans C(X, E)")
Question4 = Question(4, id_answer=4, content="enoncer le theoreme d'Ascolie")
Question5 = Question(5, id_answer=4, content="donner une condition suffisante pour que A soit dense dans C(X, E).")

Carnet4 = Carnet(4, "Proba", id_parent_carnet=1)
Answer5 = Answer(5, id_carnet=4, text_content="Si T est un temps d'arrêt et (Xn) est une martingale alors (Xn) arretré au temps T est aussi une martingale")
Question6 = Question(6, id_answer=5, content="Donner une condition suffisante pour que (Xn) arreté au temps T soit une martingale")


carnets = [Carnet1, Carnet2, Carnet3, Carnet4]
answers = [Answer1, Answer2, Answer3, Answer4, Answer5]
questions = [Question1, Question2, Question3, Question4, Question5, Question6]
"""