from flask import render_template, redirect, url_for
from app.interrogation.forms import AnswerForm
from random import choice
from app.models import Carnet, Answer, Question

from app.interrogation import bp


@bp.route('/interrogation/<id_carnet>')
def interrogation(id_carnet):
	carnet = Carnet.query.get(id_carnet)
	eligeable_questions = carnet.get_all_questions()
	question_to_ask = choice(eligeable_questions)
	
	return redirect(url_for('interrogation.question', id_carnet=id_carnet, id_question=question_to_ask.id))

@bp.route('/interrogation/question/<id_carnet>/<id_question>', methods=['GET', 'POST'])
def question(id_carnet, id_question):
	form = AnswerForm()

	if form.validate_on_submit():
		if form.not_known.data:
			print("not_known")
		elif form.not_enought.data:
			print("not_enought")
		elif form.known.data:
			print("known")
		elif form.mastered.data:
			print("mastered")

		return redirect(url_for('interrogation.interrogation', id_carnet=id_carnet))


	question = Question.query.get(id_question)
	answer = question.solution

	return render_template('interrogation/question.html', question=question, answer=answer, form=form)


