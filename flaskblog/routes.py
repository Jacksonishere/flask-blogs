# to save the uploaded pictures in local storage to the root path of project + static + profile_pics + hashedName.jpeg
import os
import secrets
from PIL import Image
from flaskblog import app, db, bcrypt, mail
# functionality
from flask import render_template, url_for, flash, redirect, request, abort
# forms
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
# models
from flaskblog.models import User, Post
# user session
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    # get the page param
    page = request.args.get('page', 1, type=int)
    # paginate the query for posts for the current page and the amount to show, 5 per page.
    # this returns an object with the items and other methods
    # passing page=page fills the items property of this paginate object
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

