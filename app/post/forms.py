from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from app.models import Post

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=256), Regexp('^[a-zA-Z][a-zA-Z0-9- ]*$', flags=0, message='Can only use aphanumeric characters and space')])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_title(self, field):
        if Post.query.filter_by(title=field.data).first():
            raise ValidationError('Post with that title already exists')

class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=256), Regexp('^[a-zA-Z][a-zA-Z0-9- ]*$', flags=0, message='Can only use aphanumeric characters and space')])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')

    def validate_title(self, field):
        if Post.query.filter_by(title=field.data).first():
            raise ValidationError('Post with that title already exists')
