from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class EditProfileForm(FlaskForm):
    name        = StringField('Name')
    location    = StringField('Location')
    about_me    = TextAreaField('About me')
    submit      = SubmitField('Update details')
