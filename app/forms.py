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
from wtforms import StringField, BooleanField, SelectField, TextField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    '''
    Define two vars for use in : email & remember_me
    email: text that requires some imput
    remember_me: checkbox that defaults to True
    '''
    # requires data to be passed to @after_login
    email = StringField('email', validators=[DataRequired()])
    #used to house openid info but now depricating
    use_email = SelectField('use_email', default='email',
                            choices=[('email', 'email')])
    remember_me = BooleanField('remember_me', default=True)

class EditForm(Form):
    '''
    Provide fields for editing user login info.
    '''
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextField('about_me', validators=[Length(min=0, max=140)])
