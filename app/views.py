'''
representation of each web page
Q: can I put references in each of the method calls to access
	a unique file
'''
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
# these are set in the __init__.py file
from app import app, db, lm
from .forms import LoginForm
from .models import User

@app.before_request
def before_request():
	'''
	Check if user login in stored in flask session imported helper
	'''
	g.user = current_user

@app.route('/')
@app.route('/home')
def home():
	if g.user is None or not g.user.is_authenticated():
		user = 'you sneaky anonymous user'
	else:
		user = g.user.nickname
	return render_template('home.html',
							title="Welcome",
							user=user)

@app.route('/index')
@login_required
def index():
	'''
	main page for logged in users
	'''
	user = g.user
	posts = [ #fake array of posts
		{ #subbing in fake user nickname objects
			'author': {'nickname': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'nickname': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return render_template('index.html',
							title = 'Home',
							user = user,
							posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	'''
	Handles user login:
	GET: redirects user to index if stored in session/authenticated
	POST: validates user input & updates db if new user or retreives
		  old user data.
	NOTE: not supporting openid cause it suxdix
	'''
	#if user login already stored in session data, skip everything
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	# get appropriate form
	form = LoginForm()
	if form.validate_on_submit():
		# if fields are filled and user clicks submit
		session['remember_me'] = form.remember_me.data
		if form.use_email.data == 'email':
			email = form.email.data
			return after_login(email)
		#return resp
		# oid is a dum pos but this line handles a call to an external
		# source so that the user doesn't have to create a unique login
		# return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
	return render_template('login.html',
							title='Sign In',
							form=form)

def after_login(email):
	'''
	Verifies response from user input & sets user data to flask session
	'''
	if email is None or email == "":
		# validate email for arbitrary conditions
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	# get user info from db
	user = User.query.filter_by(email=email).first()
	if user is None:
		# create user if doesn't exist
		nickname = email.split('@')[0]
		user = User(email=email, nickname=nickname)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None) # why pop here?
	# login_user is a flask ext that stores session info
	login_user(user, remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@lm.user_loader
def load_user(id):
	#loads user from db
	return User.query.get(int(id))

@app.route('/logout')
def logout():
	#logout the user and take them back to the home page
	logout_user() # imported
	return redirect(url_for('home'))
