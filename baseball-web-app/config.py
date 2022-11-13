import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  # Change the database URL token here if needed for testing on your own machine
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_TK_LAPTOP') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False