from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from datetime import datetime
import hashlib

class User(db.Model, UserMixin):
    __tablename__           = 'users'
    id                      = db.Column(db.Integer, primary_key=True)
    username                = db.Column(db.String(64), index=True, unique=True)
    email                   = db.Column(db.String(64), index=True, unique=True)
    password_hash           = db.Column(db.String(128))
    is_confirmed            = db.Column(db.Boolean, default=False)
    name                    = db.Column(db.String(128))
    location                = db.Column(db.String(64))
    about_me                = db.Column(db.String(256))
    member_since            = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen               = db.Column(db.DateTime, default=datetime.utcnow)
    avatar_hash             = db.Column(db.String(32))

    communities             = db.relationship('Community', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    posts                   = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    replies                 = db.relationship('Reply', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    post_votes              = db.relationship('PostVote', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reply_votes             = db.relationship('ReplyVote', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    community_participants  = db.relationship('CommunityParticipant', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='robohash', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'https://www.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return f'{url}/{hash}?s={size}&d={default}&r={rating}'
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
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
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
            self.avatar_hash = self.gravatar_hash()
            db.session.add(self)
            return True

    def change_password(self, new_password):
        self.password = new_password
        db.session.add(self)

    def change_username(self, new_username):
        self.username = new_username
        db.session.add(self)

    def __repr__(self):
        return f'<User: {self.username} {self.email}>'


class AnonymousUser(AnonymousUserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser


class Community(db.Model):
    __tablename__   = 'communities'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(128))
    description     = db.Column(db.String(512))
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow)

    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    posts           = db.relationship('Post', backref='community', lazy='dynamic', cascade='all, delete-orphan')
    participants    = db.relationship('CommunityParticipant', backref='community', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Community: {self.name}>'


class Post(db.Model):
    __tablename__   = 'posts'
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(256))
    body            = db.Column(db.Text)
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow)

    community_id    = db.Column(db.Integer, db.ForeignKey('communities.id'))
    author_id       = db.Column(db.Integer, db.ForeignKey('users.id'))
    replies         = db.relationship('Reply', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    post_votes      = db.relationship('PostVote', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def remove_space_from_title(self):
        self.title = '-'.join(self.title.strip().split(' '))
        db.session.add(self)


    def __repr__(self):
        return f'<Post: {self.title}>'


class Reply(db.Model):
    __tablename__   = 'replies'
    id              = db.Column(db.Integer, primary_key=True)
    body            = db.Column(db.Text)
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow)

    author_id       = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id         = db.Column(db.Integer, db.ForeignKey('posts.id'))
    reply_votes     = db.relationship('ReplyVote', backref='reply', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Reply: {self.body}>'


class PostVote(db.Model):
    __tablename__   = 'post_votes'
    id              = db.Column(db.Integer, primary_key=True)
    count           = db.Column(db.Integer)

    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id         = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'<PostVotes {self.count}>'


class ReplyVote(db.Model):
    __tablename__   = 'reply_votes'
    id              = db.Column(db.Integer, primary_key=True)
    count           = db.Column(db.Integer)

    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    reply_id        = db.Column(db.Integer, db.ForeignKey('replies.id'))

    def __repr__(self):
        return f'<ReplyVotes {self.count}>'


class CommunityParticipant(db.Model):
    __tablename__   = 'community_participants'
    id              = db.Column(db.Integer, primary_key=True)

    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id    = db.Column(db.Integer, db.ForeignKey('communities.id'))

    def __repr__(self):
        return f'<CommunityParticipant: {self.id}>'
