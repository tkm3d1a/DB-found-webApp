import os
import logging
import pymysql
from flask import render_template, request, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm, SearchForm
from app.orm import Analysis, People

# Root user information from os environment
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PW')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

# Base Session details?
# sessionCurrent = session
# session['loggedin'] = False

@app.route('/')
def home():
  
  print(session)
  
  if (session.get('loggedin', False)):
    return render_template('index.html', title='Home', session=session)
  else:
    return render_template('index.html', title='Home - Logged in', session=session)

@app.route('/search', methods=['GET','POST'])
def search():
  search_form = SearchForm()
  results = []
  nameResults = []
  playerIDS = []
  
  if search_form.validate_on_submit():

    if (len(search_form.first_name.data) > 1 and len(search_form.last_name.data) >= 1):
      nameFirstData = search_form.first_name.data + '%%'
      nameLastData = search_form.last_name.data + '%%'
      nameResults = People.query.filter(People.nameFirst.like(nameFirstData),People.nameLast.like(nameLastData)).all()
        
    for row in nameResults:
      print(row)
      playerIDS.append(row.playerID)
      
    selectedID = playerIDS[0]
    print(selectedID)
    
    results = Analysis.query.filter_by(playerid=selectedID).all()
    for row in results:
      row.updateAge()
      if row.RC27 is None:
        row.setRC27()
      print(row)
    
    if(len(nameResults) == 1):
      return render_template('resultsPlayerID.html', title='Results', form=search_form, results=results)
    
    if(len(nameResults) > 1):
      return render_template('resultsPlayerName.html', title='Player List', form=search_form, nameResults=nameResults)
    
  return render_template('search.html', title='Search', form=search_form)


@app.route('/signin', methods =['GET', 'POST'])
def sign_in():
  msg = ''
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      username = request.form['username']
      password = request.form['password']
      con = pymysql.connect(
        host=db_host, 
        user=db_user, 
        password=db_password, 
        db=db_name, 
        cursorclass=pymysql.cursors.DictCursor)
      cursor = con.cursor()
      
      cursor.execute(
        'SELECT * FROM webusers WHERE username = %s AND password_pt = %s', 
        (username, 
         password))
      account = cursor.fetchone()
      print(session)
      print(username)
      print(password)
      if account:
        session['loggedin'] = True
        session['id'] = account['webuser_ID']
        session['username'] = account['username']
        msg = 'Logged in successfully !'
        print(session)
        return render_template('welcome.html', msg=msg, session=session)
      else:
        session['loggedin'] = False
        msg = 'Incorrect username / password !'
          
  print(session)
  
  return render_template('signin.html', title="Sign In", msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
  msg = ''
  # needs if post method for signing up user
  # should have logic on checking email and password
  # need hashing at minimum to store password
  return render_template('register.html', title="Register", msg = msg)

@app.route('/logout')
def logout():
  print(session)
  session.pop('id', None)
  session.pop('username', None)
  session['loggedin'] = False
  return redirect(url_for('sign_in'))