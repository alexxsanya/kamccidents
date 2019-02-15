from os import environ

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret_key"
    UPLOAD_FOLDER = "./uploaded_files"
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 #max file size - 2MB

class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True