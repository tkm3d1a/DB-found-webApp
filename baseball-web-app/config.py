import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

  db_user = os.environ.get('DB_USER')
  db_password = os.environ.get('DB_PW')
  db_host = os.environ.get('DB_HOST')
  
  # Change the database URL token here if needed for testing on your own machine
  db_port = os.environ.get('DB_PORT')
  db_name = os.environ.get('DB_NAME')
  
  db_uri = 'mysql+pymysql://'+db_user+':'+db_password+'@'+db_host+':'+db_port+'/'+db_name
  SQLALCHEMY_DATABASE_URI = db_uri or 'sqlite:///' + os.path.join(base_dir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False