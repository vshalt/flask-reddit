from app.main import main_blueprint
from flask import render_template
from flask_login import current_user, login_required

@main_blueprint.route('/')
def home():
    return render_template('main/home.html')

@main_blueprint.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', user=current_user)
