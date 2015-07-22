'''
representation of each web page
Q: can I put references in each of the method calls to access
	a unique file
'''
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
# these are set in the __init__.py file
from app import app, db, lm
# bring forms in from forms.py
from .forms import LoginForm, EditForm, AdminForm
from .models import User
#timestamp shit
from datetime import datetime

@lm.user_loader
def load_user(id):
	#loads user from db
	return User.query.get(int(id))

@app.before_request
def before_request():
	'''
	Check if user login in stored in flask session imported helper
	'''
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/home')
def home():
	if g.user is None or not g.user.is_authenticated():
		user = 'you sneaky anonymous user'
		return render_template('home.html',
								title="Welcome",
								user=user)
	else:
		return index()

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if user == None:
		flash('User %s was not found.' % username)
		return redirect(url_for('index'))
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html',
							user=user,
							posts=posts)


@app.route('/index')
@login_required
def index():
	'''
	main page for logged in users
	'''
	user = g.user
	posts = [ #fake array of posts
		{ #subbing in fake user username objects
			'author': {'username': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
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
	print 'enter login()'
	#if user login already stored in session data, skip everything
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	# get appropriate form
	form = LoginForm()
	if form.validate_on_submit():
		# if fields are filled and user clicks submit
		username = form.username.data
		password = form.password.data
		session['remember_me'] = form.remember_me.data
		print username, password
		return after_login(username, password)
	return render_template('login.html',
							title='Sign In',
							form=form)

def after_login(username, password):
	'''
	Verifies username and password against db.
	Flash error if user does not exist or incorrect password
	Create user if this is first user.
	'''
	print 'after login'
	if username is None or username == "" or not sanitize(username):
		# validate username for arbitrary conditions & sql injection
		flash('Invalid username.')
		# todo: fix pause_input
		flash('Invalid password.')
		return redirect(url_for('login'))
		# return pause_input('Invalid username. Please try again.', 'login')

	# get user info from db
		# could prolly change this call to check for matches on u/n and pass at once
		# but that wouldn't give useful info to user about what they did wrong
	user = User.query.filter_by(username=username).first()
	if user is not None:
		# if user exists in the system check for password
		if password != user.password:
			flash('Invalid password.')
			return redirect(url_for('login'))
		'''Covered
		else:
			# authenticated
			remember_me = False
			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None) # why pop here? removes
			# login_user is a flask ext that stores session info
			login_user(existing_user, remember=remember_me)
			return redirect(request.args.get('next') or url_for('index'))
		'''
	else:
		# username not found
		user_list = User.query.all()
		if len(user_list) > 1000:
			# username not in system
			flash('Uknown username. Please try again')
			return redirect(url_for('login'))
		else:
			# create 1st user
			user = User(username=username, password=password)
			db.session.add(user)
			db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None) # why pop here? multiuser?
	# login_user is a flask ext that stores session info
	login_user(user, remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))

def pause_input(warning_text, redirect):
	flash(warning_text)
	return redirect(url_for('index'))

@app.route('/logout')
def logout():
	#logout the user and take them back to the home page
	logout_user() # imported
	return redirect(url_for('home'))

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm()
	if form.validate_on_submit():
		# bugging out: no restrictions on same usernames--fixed
		g.user.username = form.username.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved')
		return redirect(url_for('edit'))
	else:
		form.username.data = g.user.username
		form.about_me.data = g.user.about_me
		return render_template('edit.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
	form = AdminForm() # for generating new logins
	if form.validate_on_submit():
		username = form.username.data
		password = form.password_creation.data
		user = User.query.filter_by(username=username).first()
		if user is not None:
			# username is taken
			flash('Username already taken. Please try again.')
			return redirect(url_for('admin'))
		else:
			# username is available
			new_user = User(username=username, password=password)
			db.session.add(new_user)
			db.session.commit()
			flash('New user created.')
			return redirect(url_for('admin'))
	user_list = User.query.all()
	admin = g.user
	return render_template('admin.html',
							title='Control Center',
							users=user_list,
							form=form,
							admin=admin)

@app.errorhandler(404)
def not_found_error(error):
	# todo: make 404 html page
	print 'In 404 method'
	return 'you just got 404\'d sucker'

@app.errorhandler(500)
def internal_error(error):
	# todo: make 500 html page
	db.session.rollback()
	return 'There was an error with your request. Please go back and try again.'

def sanitize(input):
	# sanitize strings of sql injection
	if type(input) == str:
		test_input = input.lower()
		fail_terms = ['; drop', '; update', '; insert', '; select']
		for term in fail_terms:
			if term in test_input:
				return False
	return True

@app.route('/sudo', methods=['GET', 'POST'])
def sudo():
	# superuser for debugging logins
	form = AdminForm() # for generating new logins
	if form.validate_on_submit():
		username = form.username.data
		user = User.query.filter_by(username=username).first()
		if user is not None:
			# username is taken
			flash('Username already taken. Please try again.')
			return redirect(url_for('sudo'))
		else:
			# username is available
			new_user = User(username=username, password=password)
			db.session.add(new_user)
			db.session.commit()
			flash('New user created.')
			return redirect(url_for('sudo'))
	user_list = User.query.all()
	admin = g.user
	return render_template('admin.html',
							title='Sudo',
							users=user_list,
							form=form,
							sudo=True,
							admin=admin)
