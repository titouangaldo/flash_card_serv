from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import ValidationError, DataRequired, Length

class AddCarnetForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddAnswerForm(FlaskForm):
	text_content = StringField('Content', validators=[DataRequired()])
	submit = SubmitField('Add')

class EditAnswerForm(FlaskForm):
	text_content = StringField('Content', validators=[DataRequired()])
	submit = SubmitField('Edit')


class AddQuestionForm(FlaskForm):
	content = StringField('Content', validators=[DataRequired()])
	submit = SubmitField('Add')


