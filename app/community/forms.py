from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp
from app.models import Community

class NewCommunityForm(FlaskForm):
    name        = StringField('Name', validators=[DataRequired(), Length(max=128), Regexp('^[a-zA-Z][a-zA-Z0-9_]*$', flags=0, message='Name can contain only alphanumeric characters')])
    description = StringField('Description', validators=[DataRequired(), Length(max=512)])
    submit      = SubmitField('Create community')

    def validate_name(self, field):
        if Community.query.filter_by(name=field.data).first():
            raise ValidationError('Community with that name already exists')

class UpdateCommunityForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(max=512)])
    submit      = SubmitField('Update community')
