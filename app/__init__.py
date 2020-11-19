from flask import Flask
from config import config

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth import auth_blueprint
    from app.main import main_blueprint
    from app.community import community_blueprint
    from app.communities import communities_blueprint
    from app.post import post_blueprint
    from app.reply import reply_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(community_blueprint)
    app.register_blueprint(communities_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(reply_blueprint)
    return app
