"""
Config objects for flask
"""
import os


class BaseConfig(object):
    """
    Base configuration.
    """
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', None)


class DevelopmentConfig(BaseConfig):
    """
    Development configuration.
    """
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """
    Testing configuration.
    """
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(basedir, 'thundersnow-test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(path)
    SECRET_KEY = 'my precious'
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """
    Production configuration.
    """
    DEBUG = False
    DEBUG_TB_ENABLED = False
