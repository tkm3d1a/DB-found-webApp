from flask import render_template, request
from app import app
from app.forms import LoginForm, SearchForm

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
  return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login')
def login():
  form = LoginForm()
  return render_template('login.html', title='Sign in', form=form)

@app.route('/search', methods=['GET','POST'])
def search():
  search_form = SearchForm()
  # No crashing, but screen does not refresh with this hardcode.  
  # Need to investigate more on why
  if search_form.validate_on_submit():
  # if request.method == "POST":
    # hard coding to test results display
    results = [
      {
        "firstName": search_form.first_name.data,
        "lastName": search_form.last_name.data
      }
    ]
    return render_template('search.html', title='Results', form=search_form, results=results)
  return render_template('search.html', title='Search', form=search_form)
