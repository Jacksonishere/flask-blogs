# create package with name of our app
# initialize the application and bring in diff components here. 

#this file or module houses the whole app?
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

# create database with our app and also allows interaction with it through its ORM framework?
# Create extensions for our app
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
# any routes that is wrapped in login_required decorator will reroute to the login route if not logged in.
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

# create instance of the app with default class of config
# this means the imports where we import the app from flaskblog, we need to replace with a flask import called current app. 
def create_app(config_class=Config):    
    #create flask app with this module
    app = Flask(__name__) #__name__ is a special var in python that just name of module. 
    #by default, __name__ is replaced with __main__ in ur local machine
    # config app with separate config object. we do this because possible we have different config settings.
    app.config.from_object(Config)

    # init app with the extensions we created using init_app function. 
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # import the blueprint objects
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    # register the blueprints with our app. 
    # it will basically just register all the functionality that was bound to the blueprint back to the app.
    # this also prefixes the endpoints defined in the routes with the name of the blueprint so we need to change it in URL_For
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)


    # return the instance of app
    return app
