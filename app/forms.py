'''
Provides identifiers and default values for buttons and text boxes that
are filled out by the user.
This can and is used by both views and html file
By building these form submission tools in a separate file we separate the
issues of integrating html and python.
'''
# basic module import from flask
from flask.ext.wtf import Form
# you must pull in the types of fields and validators you need individually.
from wtforms import StringField, BooleanField, SelectField, TextField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput

class LoginForm(Form):
    '''
    Define two vars for use in : email & remember_me
    email: text that requires some imput
    remember_me: checkbox that defaults to True
    '''
    # requires data to be passed to @after_login
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()], widget=PasswordInput())
    # used to create passwords on admin table
    #password_creation = StringField('password_creation', validators=[DataRequired()])
    # used to house openid info but now depricating
    remember_me = BooleanField('remember_me', default=True)

class EditForm(Form):
    '''
    Provide fields for editing user login info.
    '''
    username = StringField('username', validators=[DataRequired()])
    about_me = TextField('about_me', validators=[Length(min=0, max=140)])

class AdminForm(Form):
    '''
    Provide fields for creating new user logins
    '''
    username = StringField('username', validators=[DataRequired()])
    password_creation = StringField('password_creation', validators=[DataRequired()])
