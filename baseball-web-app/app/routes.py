import sys
import logging
import pymysql
from flask import render_template, request, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm, SearchForm
from app.orm import Analysis

@app.route('/')
def home():
  user = {'username': 'Miguel'}
  posts = [
      {
          'author': {'username': 'John'},
          'body': 'Beautiful day in Portland!'
      },
      {
          'author': {'username': 'Susan'},
          'body': 'The Avengers movie was so cool!'
      }
  ]
  results = []
  return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login')
def login():
  form = LoginForm()
  return render_template('login.html', title='Sign in', form=form)

@app.route('/search', methods=['GET','POST'])
def search():
  search_form = SearchForm()
  if search_form.validate_on_submit():
    results = Analysis.query.filter_by(playerid=search_form.first_name.data).all()
    for row in results:
      # print(row, file=sys.stderr)
      # app.logger.info(row)
      row.updateAge()
      if row.RC27 is None:
        row.setRC27()
    return render_template('search.html', title='Results', form=search_form, results=results)
  return render_template('search.html', title='Search', form=search_form)

@app.route('/signin', methods =['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        con = pymysql.connect(host='localhost', user='root', password='7998', db='baseball', cursorclass=pymysql.cursors.DictCursor)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        accounts = cursor.fetchall()
        account = cursor.fetchone()

        for row in accounts:
            print(row)

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('welcome.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg = msg)

@app.route('/register')
def register():
    return "You shall register...!"

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))