from flask_wtf import FlaskForm
from wtforms import SubmitField

class AnswerForm(FlaskForm):
	not_known = SubmitField('Not Known')
	not_enought = SubmitField('Not Known Enought')
	known = SubmitField('Known')
	mastered = SubmitField('Mastered')