import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:fakepassword@localhost/fake_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    # REDIS_URL = 'redis://localhost:6379/0'

    UPLOAD_FOLDER = '/var/www/roommate/storage/'

    NUMBER_PER_PAGE = 9

    LOGGING = {
        'log_file_path': '/var/www/roommate/log/pyws.log',
        'level': logging.DEBUG,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
