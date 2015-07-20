'''
Creates python classes out of sql db objects
Q: does order matter in the call user = User(email=x, nickname=y)
i'm thinking not
'''
from app import db

class User(db.Model):
    #maps users to db sql columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime)
    about_me = db.Column(db.String(140))

    def is_authenticated(self):
        #fill out if restricting unauthenticated users
        return True

    def is_active(self):
        #fill out if restricting a user by activation
        return True

    def is_anonymous(self):
        #fill out if restricting unknown users
        return False

    def get_id(self):
        #return primary_key for user in db
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        #how the user object is printed
        return '<userID=%r nickname=%r password=%r last_seen=%r>' % (self.id,
                self.username, self.password, self.last_seen)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
