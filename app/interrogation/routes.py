import logging
from flask import render_template, redirect, url_for
from app.interrogation.forms import AnswerForm
from random import choices
import datetime
from app.models import Carnet, Answer, Question, Evaluation

from app.interrogation import bp
from app import db

@bp.route('/interrogation/<id_carnet>')
def interrogation(id_carnet):
	carnet = Carnet.query.get(id_carnet)
	question_to_ask = question_choice(carnet)
	
	return redirect(url_for('interrogation.question', id_carnet=id_carnet, id_question=question_to_ask.id))

@bp.route('/interrogation/question/<id_carnet>/<id_question>', methods=['GET', 'POST'])
def question(id_carnet, id_question):
	question = Question.query.get(id_question)

	form = AnswerForm()
	if form.validate_on_submit():
		if form.not_known.data:
			db.session.add(Evaluation(question=question, result="not_known"))
		elif form.not_enought.data:
			db.session.add(Evaluation(question=question, result="not_enought"))
		elif form.known.data:
			db.session.add(Evaluation(question=question, result="known"))
		elif form.mastered.data:
			db.session.add(Evaluation(question=question, result="mastered"))

		db.session.commit()
		return redirect(url_for('interrogation.interrogation', id_carnet=id_carnet))

	answer = question.solution

	return render_template('interrogation/question.html', question=question, answer=answer, form=form)



def question_choice(carnet):
	eligeable_questions = carnet.get_all_questions()
	logging.getLogger(__name__).info(f"eligeable questions: {eligeable_questions}")   
	weights=[]
	for q in eligeable_questions:
		last_eval = q.evaluation.order_by(Evaluation.timestamp.desc()).first()

		

		if last_eval == None:
			weights.append(50)
		else:
			time_since_last_eval = datetime.datetime.utcnow() - last_eval.timestamp
			if time_since_last_eval < datetime.timedelta(hours=8):
				weights.append(1)

			elif last_eval.result=="mastered":
				if time_since_last_eval > datetime.timedelta(weeks=5):
					weights.append(5)
				else:
					weights.append(1)

			elif last_eval.result=="known":
				if time_since_last_eval > datetime.timedelta(weeks=3):
					weights.append(10)
				else:
					weights.append(5)

			elif last_eval.result=="not_enought":
				if time_since_last_eval > datetime.timedelta(weeks=1):
					weights.append(20)
				else:
					weights.append(10)

			elif last_eval.result=="not_known":
				if time_since_last_eval > datetime.timedelta(days=5):
					weights.append(100)
				elif time_since_last_eval > datetime.timedelta(days=3):
					weights.append(50)
				else:
					weights.append(30)

	return choices(eligeable_questions, weights=weights)[0]



