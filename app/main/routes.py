from app.main import bp
from app.main.forms import AddCarnetForm, AddAnswerForm, EditAnswerForm, AddQuestionForm
from flask import render_template, redirect, url_for, request
from app.models import Carnet, Answer, Question
from app import db
import logging

def get_trash_carnet():
	return Carnet.query.filter(Carnet.name == "_Trash_").first()

def get_base_carnet():
	return Carnet.query.filter(Carnet.name=="_Base_").first()

@bp.before_app_first_request
def before_app_first_request():
	if not get_base_carnet():
		db.session.add(Carnet(name="_Base_"))
		db.session.commit()
		logging.getLogger(__name__).warn("Base Carnet was added because there were not any")

	if not get_trash_carnet():
		db.session.add(Carnet(name="_Trash_"))
		db.session.commit()
		logging.getLogger(__name__).warn("Trash Carnet was added because there were not any")


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
	
	addCarnetForm = AddCarnetForm()
	if addCarnetForm.validate_on_submit():
		get_base_carnet().add_carnet(name=addCarnetForm.name.data)
		return redirect(url_for('main.index'))

	
	main_carnets = get_base_carnet().children_carnets

	# delete carnet
	carnet_to_delete_id=request.args.get('delete-carnet', None, type=int)
	if carnet_to_delete_id:
		print("Carnet to delete:", carnet_to_delete_id)
		Carnet.query.get(carnet_to_delete_id).move(get_trash_carnet().id)
		return redirect(url_for('main.index'))

	# move carnet
	carnet_to_move_id=request.args.get('move-carnet', None, type=int)
	if carnet_to_move_id:
		print("Carnet to move:", carnet_to_move_id)
		return redirect(url_for('main.move_carnet', id_carnet=carnet_to_move_id))


	class CarnetxKnowledges:
		def __init__(self, carnet, knowledge):
			self.carnet = carnet
			self.knowledge = knowledge

	carnetsXknowledges = []
	for c in main_carnets:
		carnetsXknowledges.append(CarnetxKnowledges(c, c.get_knowledge_composition()))
		
	return render_template('index.html', title='Home', inner_carnets=carnetsXknowledges, addCarnetForm=addCarnetForm)



@bp.route('/carnet/<id_carnet>', methods=['GET', 'POST'])
def carnet(id_carnet):

	# if carnet is _Base_ we go to index
	if int(id_carnet) == Carnet.query.filter(Carnet.name=="_Base_").first().id:
		return redirect(url_for('main.index'))

	carnet = Carnet.query.get(int(id_carnet))
	inner_carnets = carnet.children_carnets
	inner_answers = list(carnet.answers)
	addCarnetForm = AddCarnetForm()
	if addCarnetForm.validate_on_submit():
		carnet.add_carnet(addCarnetForm.name.data)
		return redirect(url_for('main.carnet', id_carnet=id_carnet))

	addAnswerForm = AddAnswerForm()
	if addAnswerForm.validate_on_submit():
		carnet.add_answer(addAnswerForm.text_content.data)
		return redirect(url_for('main.carnet', id_carnet=id_carnet))

	# move carnet
	carnet_to_move_id=request.args.get('move-carnet', None, type=int)
	if carnet_to_move_id:
		print("Carnet to move:", carnet_to_move_id)
		return redirect(url_for('main.move_carnet', id_carnet=carnet_to_move_id))

	# move answer
	answer_to_move_id=request.args.get('move-answer', None, type=int)
	if answer_to_move_id:
		print("Answer to move:", answer_to_move_id)
		return redirect(url_for('main.move_answer', id_answer=answer_to_move_id))

	# delete carnet
	carnet_to_delete_id=request.args.get('delete-carnet', None, type=int)
	if carnet_to_delete_id:
		print("Carnet to delete:", carnet_to_delete_id)
		Carnet.query.get(carnet_to_delete_id).move(get_trash_carnet().id)
		return redirect(url_for('main.carnet', id_carnet=id_carnet))

	# delete answer
	answer_to_delete_id=request.args.get('delete-answer', None, type=int)
	if answer_to_delete_id:
		Answer.query.get(answer_to_delete_id).move(get_trash_carnet().id)
		return redirect(url_for('main.carnet', id_carnet=id_carnet))

	# edit answer
	answer_to_edit_id=request.args.get('edit-answer', None, type=int)
	if answer_to_edit_id:
		return redirect(url_for('main.edit_answer', id_answer=answer_to_edit_id))

	class CarnetxKnowledges:
		def __init__(self, carnet, knowledge):
			self.carnet = carnet
			self.knowledge = knowledge

	carnetsXknowledges = []
	for c in inner_carnets:
		carnetsXknowledges.append(CarnetxKnowledges(c, c.get_knowledge_composition()))

	return render_template('carnet.html', carnet=carnet,\
	 	inner_carnets=carnetsXknowledges, inner_answers=inner_answers,\
		addCarnetForm=addCarnetForm, addAnswerForm=addAnswerForm)


@bp.route('/edit_answer/<id_answer>', methods=['GET', 'POST'])
def edit_answer(id_answer):
	answer = Answer.query.get(int(id_answer))

	editAnswerForm = EditAnswerForm()

	if editAnswerForm.validate_on_submit():
		answer.edit_content(editAnswerForm.text_content.data)
		return redirect(url_for('main.edit_answer', id_answer=id_answer))
	else:
		editAnswerForm.text_content.data = answer.text_content

	# add a question
	addQuestionForm = AddQuestionForm()
	if addQuestionForm.validate_on_submit():
		answer.add_question(addQuestionForm.content.data)
		return redirect(url_for('main.edit_answer', id_answer=id_answer))

	#edit question
	request_dict = dict(request.args)
	for k,v in request_dict.items():
		if k.startswith('edit-question'):
			question_to_edit_id = int(k.replace('edit-question', ''))
			Question.query.get(question_to_edit_id).edit_content(v)
			return redirect(url_for('main.edit_answer', id_answer=id_answer))

	# delete question
	question_to_delete_id=request.args.get('delete-question', None, type=int)
	if question_to_delete_id:
		Question.query.get(question_to_delete_id).eraze()
		return redirect(url_for('main.edit_answer', id_answer=id_answer))



	return render_template('edit_answer.html', answer=answer,\
		editAnswerForm=editAnswerForm, addQuestionForm=addQuestionForm)


@bp.route('/move_carnet/<id_carnet>', methods=['GET', 'POST'])
def move_carnet(id_carnet):
	carnet_to_move = Carnet.query.get(id_carnet)

	id_carnet_to_move_to=request.args.get('move-carnet', None, type=int)
	if id_carnet_to_move_to:
		carnet_to_move_to = Carnet.query.get(id_carnet_to_move_to)
		print("move carnet ", carnet_to_move, " to carnet ", carnet_to_move_to)
		carnet_to_move.move(id_carnet_to_move_to)
		return redirect(url_for('main.carnet', id_carnet=id_carnet_to_move_to))

	carnets = Carnet.query.filter(Carnet.name != "_Trash_" and Carnet.id_parent_carnet != get_trash_carnet().id)

	return render_template('move.html', carnet_to_move=carnet_to_move, base_carnet=get_base_carnet(),\
		carnets=carnets)

@bp.route('/move_answer/<id_answer>', methods=['GET', 'POST'])
def move_answer(id_answer):
	answer_to_move = Answer.query.get(id_answer)
	
	id_carnet_to_move_to=request.args.get('move-carnet', None, type=int)
	if id_carnet_to_move_to:
		carnet_to_move_to = Carnet.query.get(id_carnet_to_move_to)
		print("move answer ", answer_to_move, " to carnet ", carnet_to_move_to)
		answer_to_move.move(id_carnet_to_move_to)
		return redirect(url_for('main.carnet', id_carnet=id_carnet_to_move_to))

	carnets = Carnet.query.filter(Carnet.name != "_Trash_" and Carnet.id_parent_carnet != get_trash_carnet().id)

	return render_template('move.html', answer_to_move=answer_to_move, carnets=carnets)













