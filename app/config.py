import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'instance')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-peternakan-orange-123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(INSTANCE_DIR, 'peternakan.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False