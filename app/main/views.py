from app.main import main_blueprint
from flask import render_template
from flask_login import current_user

@main_blueprint.route('/')
def home():
    return render_template('main/home.html')
