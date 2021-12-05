from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager
from flask import current_app
# we need to inherit this class inside our model which is required for the flask login extension.
from flask_login import UserMixin

# decorator so extension knows to get the user by id stored in session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create models
class User(db.Model, UserMixin):
    # because PK, id assigned automatically
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    password = db.Column(db.String(60), nullable=False)
    # set up bidirectional relationship with Post model. Access posts with User.posts but Post.author to get the user of post. 
    # like rails, this is not a field in table.
    posts = db.relationship('Post', backref='author', lazy=True)

    # create password reset token that expires in 1800.
    # 
    def get_reset_token(self, expires_sec=1800):
        # create serializer with app secret key
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # return json token using serializer by decoding the user id
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # because not using self
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        # try and catch block in case the token expired or there was an error.
        # We decode the serialized JSON object and access the user_id
        try:
            user_id = s.loads(token)['user_id']
        # if excpetion thrown, return none since no user can be found
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # set up the belongs to, or FK to the user table. Not like rails where model is User and table is users. 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

