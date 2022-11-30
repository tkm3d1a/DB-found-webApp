import os
import hashlib
from flask import render_template, request, flash, redirect, url_for, session
from app import app, db
from app.forms import LoginForm, SearchForm, SaveForm, SelectForm
from app.orm import Analysis, People, Web_Users

# Root user information from os environment
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PW')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

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
  save_form = SaveForm()
  select_form = SelectForm()
  results = []
  nameResults = []
  playerIDS = []
  msg=''
  
  if request.method == 'POST':

    if (len(search_form.first_name.data) > 1 and len(search_form.last_name.data) >= 1):
      nameFirstData = search_form.first_name.data + '%%'
      nameLastData = search_form.last_name.data + '%%'
      nameResults = People.query.filter(People.nameFirst.like(nameFirstData),People.nameLast.like(nameLastData)).all()
    
    if len(nameResults) < 1:
      msg = 'No results found'
      noResults = True
      return render_template('resultsNone.html', 
                             title='Search Again', 
                             form=search_form, 
                             nameResults=nameResults, 
                             msg=msg, 
                             noResults=noResults)
    
    if(len(nameResults) == 1):
      # return redirect(url_for('battingAnalysis',res=results))
      results = Analysis.query.filter_by(playerid=nameResults[0].playerID).all()
      for row in results:
        row.updateAge()
        if row.RC27 is None:
          row.setRC27()
        print(row)
        
      return render_template('resultsPlayerID.html',
                             title='Results', 
                             form=search_form,
                             savePlayer=save_form,
                             results=results)
    
    if(len(nameResults) > 1):
      session['nameRes'] = nameResults
      return redirect(url_for('multi_results'))
    
  return render_template('search.html', 
                         title='Search', 
                         form=search_form)

@app.route('/search/multi_res', methods=['GET','POST'])
def multi_results():
  nameResults = session.get('nameRes')
  session.pop('nameRes', None)
  
  select_form = SelectForm()
  playerIDS = []
  
  if request.method == 'POST':
    print("Im in post for multi_res")
    # FIXME:Placeholder
    # Currently just loops back to search page
    # use session to pass whatever the selection is?
    # How do I get that value?
    # need another route to handle display of final results page
    session['nameRes'] = nameResults
    return redirect(url_for('search'))
  
  for row in nameResults:
        print(row)
        playerIDS.append(row.playerID)
  
  select_form.player_id.choices = [(g.playerID, " ".join([g.nameFirst, g.nameLast])) for g in nameResults]
  
  return render_template('resultsPlayerName.html', 
                             title='Player List', 
                             selectPlayer=select_form, 
                             nameResults=nameResults)

@app.route('/sign_in', methods =['GET', 'POST'])
def sign_in():
  msg = ''
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      username = request.form['username']
      password = request.form['password']
      
      accountORM = Web_Users.query.filter_by(username=username).first_or_404()
      # print(accountORM.pw_hash)
      # print(accountORM.salt)
      testPassword = password + accountORM.salt
      testPassword = str.encode(testPassword)
      testhash = hashlib.new('sha256')
      testhash.update(testPassword)
      testPassword = testhash.hexdigest()
      # print(testPassword)
      # print(session)
      # print(username)
      # print(password)
      if accountORM.pw_hash == testPassword:
        session['loggedin'] = True
        session['id'] = accountORM.webuser_ID
        session['username'] = accountORM.username
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
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
    userExists = userNameExists = userEmailExists = False
    usernameEnt = request.form['username']
    password = request.form['password']
    emailEnt = request.form['email']
    userSalt = os.urandom(4).hex()
    toHash = password + userSalt
    toHash = str.encode(toHash)
    
    users = Web_Users.query.all()
    for row in users:
      print(row)
      if row.email == emailEnt:
        userEmailExists = True
        break
      if row.username == usernameEnt:
        userNameExists = True
        break
    
    if userEmailExists:
      userExists = True
      msg = 'Sorry, that email is already registered'
    
    if userNameExists:
      userExists = True
      msg = 'Sorry, that username already exists'

    h = hashlib.new('sha256')
    h.update(toHash)
    hashedPassword = h.hexdigest()

    if not userExists:
      newUser = Web_Users(
        username=usernameEnt, 
        email=emailEnt, 
        salt=userSalt, 
        pw_hash=hashedPassword)
      db.session.add(newUser)
      db.session.commit()
      msg = 'User Successfully registered!'
    
    testRes = Web_Users.query.all()
    for row in testRes:
      print(row)
    
    

  return render_template('register.html', title="Register", msg = msg)

@app.route('/logout')
def logout():
  print(session)
  session.pop('id', None)
  session.pop('username', None)
  session['loggedin'] = False
  return redirect(url_for('sign_in'))

# @app.route('/ba-analysis/<playerid>', methods=['GET','POST'])
# def battingAnalysis():
#   search_form = SearchForm()
#   results = request.args['res']
#   return render_template('resultsPlayerID.html', title='Results', form=search_form, results=results)