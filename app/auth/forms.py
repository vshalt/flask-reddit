from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    email               = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=64)])
    username            = StringField('Username', validators=[DataRequired(), Length(min=1, max=64), Regexp('^[a-zA-Z][a-zA-Z0-9_]*$',flags=0, message="Username can only contain alphanumerical characters")])
    password            = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('confirm_password', message="Passwords must match")])
    confirm_password    = PasswordField('Confirm Password', validators=[DataRequired()])
    submit              = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already exists')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

class LoginForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=64)])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit      = SubmitField('Login')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email does not exist')

class ChangePasswordForm(FlaskForm):
    password                = PasswordField('Old password', validators=[DataRequired()])
    new_password            = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('confirm_new_password', message='Passwords must match')])
    confirm_new_password    = PasswordField('Confirm new password', validators=[DataRequired()])
    submit                  = SubmitField('Change password')

class ChangeUsernameForm(FlaskForm):
    new_username    = StringField('Username', validators=[DataRequired(), Length(min=1, max=64), Regexp('^[a-zA-Z][a-zA-Z0-9_]*$', flags=0, message='Username can only contain alphanumerical characters')])
    password        = PasswordField('Password', validators=[DataRequired()])
    submit          = SubmitField('Change username')

    def validate_new_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

class RequestForgotPasswordForm(FlaskForm):
    email   = StringField('Email', validators=[DataRequired(), Length(min=1, max=64), Email()])
    submit  = SubmitField('Send link')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email does not exist')

class ConfirmForgotPasswordForm(FlaskForm):
    password            = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password    = PasswordField('Confirm password', validators=[DataRequired()])
    submit              = SubmitField('Change password')

class RequestChangeEmailForm(FlaskForm):
    new_email   = StringField('New email', validators=[DataRequired(), Email(), Length(min=1, max=64)])
    password    = PasswordField('Password', validators=[DataRequired()])
    submit     = SubmitField('Change email')

    def validate_new_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already exists')
