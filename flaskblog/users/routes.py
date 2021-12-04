from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # succesesfully login. store user in session, set the current user to that user in the database
            login_user(user, remember=form.remember.data)
            # if the user was sent here because wanted to access page that required login, that page will be in the params of the login route. we want to get that page and route there upon login.
            next_page = request.args.get('next')
            # pythons way of tenary assignment
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    else: 
        if form.validate_on_submit():
            # if picture was uploaded
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
                
                if current_user.image_file != 'default.jpg':
                    os.remove(os.path.join(users.root_path, 'static/profile_pics', current_user.image_file))


            current_user.username = form.username.data
            current_user.email = form.email.data

            # you can simply alter the model instance and commit after you're done to save changes
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


# route to get form and handle when user enters the email they want to reset for the account
# notice this is separate for the route when the user clicks the link in their email which is its own set of routes
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # this is more like "forgot password"
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    # if email is found, aka account is in the db, we will send a reset password email to the user then redirect back to user with the flash message that tells them check email.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# this is the link that gets sent to the email. 
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    # verify token.
    #if failed, flash message then redirect
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    # else token validate, create form and validate the password in the form
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # if success, rehash and update the user password then commit
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)