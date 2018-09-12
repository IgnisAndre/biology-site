from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired

class AddBlockForm(FlaskForm):
    blockname = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class AddQuestionForm(FlaskForm):
    block_id = DecimalField('Номер блока')
    question_text = StringField('Текст вопроса:', validators=[DataRequired()])
    correct_answer_text = StringField('Текст эталонного ответа', validators=[DataRequired()])
    submit = SubmitField('Добавить')
