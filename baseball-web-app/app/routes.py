from flask import render_template, request, flash, redirect, url_for
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
      if row.RC27 is None:
        row.setRC27()
    return render_template('search.html', title='Results', form=search_form, results=results)
  return render_template('search.html', title='Search', form=search_form)
