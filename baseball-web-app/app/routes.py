import os
import hashlib
from flask import render_template, request, flash, redirect, url_for, session
from app import app, db
from app.forms import LoginForm, SearchForm, SaveForm, SelectForm
from app.orm import Analysis, People, Web_Users, Saved_Searches

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
    return render_template('welcome.html', title='Home', session=session)
  else:
    return render_template('index.html', title='Home - Logged in', session=session)

@app.route('/search', methods=['GET','POST'])
def search():
  search_form = SearchForm()
  nameResults = []
  msg=''
  
  if request.method == 'POST':
    # Only populate nameResults if data is in the fields
    # This can likely be moved to the WTForms with validations
    if (len(search_form.first_name.data) > 1 and len(search_form.last_name.data) >= 1):
      nameFirstData = search_form.first_name.data + '%%' #this needs better input validation
      nameLastData = search_form.last_name.data + '%%' #this needs better input validation
      nameResults = People.query.filter(People.nameFirst.like(nameFirstData),People.nameLast.like(nameLastData)).all()
    
    # If no results are found aka nameResults is not populated at all
    # Creates new page, leaves search form up and displays a message to the user
    if len(nameResults) < 1:
      msg = 'No results found'
      noResults = True
      return render_template('resultsNone.html', 
                             title='Search Again', 
                             form=search_form, 
                             nameResults=nameResults, 
                             msg=msg, 
                             noResults=noResults)
    
    # If there is only one result, it goes straight to batting results page
    if(len(nameResults) == 1):
      return redirect(url_for('batting_analysis', playerid=nameResults[0].playerID))
    
    # If more than 1 result in list, goes to display the list
    # has a pick list for the user to select from
    if(len(nameResults) > 1):
      session['nameRes'] = nameResults
      return redirect(url_for('multi_results'))
    
  return render_template('search.html', 
                         title='Search', 
                         form=search_form)

@app.route('/favplayers', methods=['GET','POST'])
def favPlayers():
  msg=''
  select_form = SelectForm()
  favouritePlayers = Saved_Searches.query.filter_by(webuserID=session.get('username')).all()

  if (len(favouritePlayers) == 0):
    msg="You donot have any favourite players!"

  if request.method == 'POST':
      return redirect(url_for('batting_analysis', playerid=select_form.player_id.data))

  select_form.player_id.choices = [(g.playerID, " ".join([g.playerName])) for g in favouritePlayers]

  return render_template('resultsFavPlayers.html',
                         title='Favourite Players',
                         msg=msg,
                         selectPlayer=select_form,
                         favouritePlayers=favouritePlayers)

@app.route('/search/multi_res', methods=['GET','POST'])
def multi_results():
  nameResults = session.get('nameRes')
  session.pop('nameRes', None)
  
  select_form = SelectForm()
  playerIDS = []
  
  if request.method == 'POST':
    return redirect(url_for('batting_analysis', playerid=select_form.player_id.data))
  
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
      
      accountORM = Web_Users.query.filter_by(username=username).first()
      # print(accountORM.pw_hash)
      # print(accountORM.salt)
      if accountORM is None:
          msg = 'Incorrect username / password !'
          return render_template('signin.html', title="Sign In", msg = msg)

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

@app.route('/ba-analysis/<playerid>', methods=['GET','POST'])
def batting_analysis(playerid):
  msg=''
  search_form = SearchForm()
  results = Analysis.query.filter_by(playerid=playerid).all()
  for row in results:
        row.updateAge()
        if row.RC27 is None:
          row.setRC27()
        # print(row)
  if request.method == 'POST':
    player_ID = results[0].playerid
    player_Name = results[0].playerName
    userID = session.get('username')

    favoritePlayer = Saved_Searches.query.filter_by(playerID=player_ID, webuserID=userID).first()

    if favoritePlayer is None:
      newFavouritePlayer = Saved_Searches(
      webuserID=userID,
      playerName=player_Name,
      playerID=player_ID)
      db.session.add(newFavouritePlayer)
      db.session.commit()
      msg = 'Player marked as favourite'
    else:
      msg = "Already a favourite player"

  return render_template('resultsPlayerID.html', 
                         title='Results', 
                         form=search_form, 
                         results=results,
                         msg=msg)