from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SearchForm(FlaskForm):
    first_name = StringField('first_Name', validators=[InputRequired()])
    # last_name = StringField('lastName', validators=[InputRequired()])
    # save_search = BooleanField('Save Search')
    submit = SubmitField('Search')