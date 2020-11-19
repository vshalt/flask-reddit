from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class NewReplyForm(FlaskForm):
    body = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Reply')

class EditReplyForm(FlaskForm):
    body = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Reply')
