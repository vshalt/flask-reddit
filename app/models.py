from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(db.Model, UserMixin):
    __tablename__   = 'users'
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(64), index=True, unique=True)
    email           = db.Column(db.String(64), index=True, unique=True)
    password_hash   = db.Column(db.String(128))
    is_confirmed    = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({"confirm": self.id}).decode('utf-8')

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        else:
            self.is_confirmed = True
            db.session.add(self)
            return True

    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def confirm_password_reset_token(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user:
            user.password = new_password
            db.session.add(user)
            return True

    def generate_email_reset_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset': self.id, 'email': new_email}).decode('utf-8')

    def confirm_email_reset_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('reset') != self.id:
            return False
        else:
            self.email = data.get('email')
            db.session.add(self)
            return False

    def change_password(self, new_password):
        self.password = new_password
        db.session.add(self)

    def change_username(self, new_username):
        self.username = new_username
        db.session.add(self)

    def __repr__(self):
        return f'<{self.username} - {self.email}>'

class AnonymousUser(AnonymousUserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser
