import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY                      = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_TRACK_MODIFICATIONS  = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False

    MAIL_SERVER                     = os.environ.get('MAIL_SERVER')
    MAIL_PORT                       = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS                    = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL                    = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME                   = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD                   = os.environ.get('MAIL_PASSWORD')
    DEFAULT_MAIL_SENDER             = os.environ.get('DEFAULT_MAIL_SENDER')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'dev.db')
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
