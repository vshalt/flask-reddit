from app.auth import auth_blueprint
from app import db
from app.models import User
from flask import render_template, redirect, url_for, flash
from app.auth.forms import (
    RegisterForm,
    LoginForm,
    ChangePasswordForm,
    ChangeUsernameForm,
    RequestForgotPasswordForm,
    ConfirmForgotPasswordForm,
)
from flask_login import login_user, login_required, logout_user, current_user
from app.auth.emails import send_mail

# REGISTER USER
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower(), password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Test', 'auth/mail/confirm_email', token=token, user=current_user)
        flash('Account created login to continue')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

# LOGIN USER
@auth_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in')
            return redirect(url_for('main.home'))
        else:
            flash('Check credentials and try again')
    return render_template('auth/login.html', form=form)

# LOGOUT USER
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('main.home'))

# SEND ACCOUNT CONFIRMATION REQUEST
@auth_blueprint.route('/confirm')
@login_required
def get_confirmation_token():
    if current_user.is_confirmed:
        flash('Account already confirmed')
        return redirect(url_for('main.home'))
    else:
        token = current_user.generate_confirmation_token()
        send_mail(current_user.email, 'Confirm', 'auth/mail/confirm_email',user=current_user, token=token)
        return render_template('auth/confirm.html')

# CONFIRM TOKEN TO VERIFY ACCOUNT
@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm_token(token):
    if current_user.is_confirmed:
        flash('Account already confirmed')
        return redirect(url_for('main.home'))
    else:
        if current_user.confirm_token(token):
            db.session.commit()
            flash('Account confirmed successfully!')
        else:
            flash('Error validating the user. Try again later')
    return redirect(url_for('main.home'))

# CHANGE PASSWORD
@auth_blueprint.route('/change-password', methods=['POST', 'GET'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.change_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully')
            return redirect(url_for('main.home'))
        else:
            flash('Check your password and try again')
    return render_template('auth/change_password.html', user=current_user, form=form)

# CHANGE USERNAME
@auth_blueprint.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.change_username(form.new_username.data)
            db.session.commit()
            flash('Username changed successfully')
            return redirect(url_for('main.home'))
        else:
            flash('Check password and try again')
    return render_template('auth/change_username.html', user=current_user, form=form)

# TODO forgot password - generate_password_reset_token, confirm_password_reset_token
@auth_blueprint.route('/forgot-password', methods=['GET', 'POST'])
def request_forgot_password():
    form = RequestForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower())
        if user:
            token = user.generate_password_reset_token()
            send_mail(user.email, 'Reset password', 'auth/mail/reset_password_request', token=token, user=current_user)
            flash('Email sent')
        else:
            flash('Invalid email')

    return render_template('auth/reset_forgot_password.html')


# TODO change email    - generate_email_reset_token, confirm_email_reset_token
