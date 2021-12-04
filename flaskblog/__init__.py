# create package with name of our app
# initialize the application and bring in diff components here. 

import os
#this file or module houses the whole app?
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


#create flask app with this module
app = Flask(__name__) #__name__ is a special var in python that just name of module. 
#by default, __name__ is replaced with __main__ in ur local machine

# our csrf token
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# relative path from current file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
# create database with our app and also allows interaction with it through its ORM framework?
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# any routes that is wrapped in login_required decorator will reroute to the login route if not logged in.
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# mailer config
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

# print(os.environ.get('EMAIL_PASS'), "this is how we access env variables")

# import the blueprint objects
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

# register the blueprints with our app. 
# it will basically just register all the functionality that was bound to the blueprint back to the app.
# this also prefixes the endpoints defined in the routes with the name of the blueprint so we need to change it in URL_For
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
