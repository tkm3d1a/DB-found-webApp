from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SearchForm(FlaskForm):
    # player_id = StringField('Player ID')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    # save_search = BooleanField('Save Search')
    submit = SubmitField('Search')

class SaveForm(FlaskForm):
    # player_id = StringField('Player ID')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    # save_search = BooleanField('Save Search')
    submit = SubmitField('Search')

class SelectForm(FlaskForm):
    # player_id = StringField('Player ID')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    # save_search = BooleanField('Save Search')
    submit = SubmitField('Search')