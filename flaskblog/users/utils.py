import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    # generate random hashed name
    random_hex = secrets.token_hex(8)
    # get the extension of the picture file in the form submission
    _, f_ext = os.path.splitext(form_picture.filename)
    # append new hashed name with extension
    picture_fn = random_hex + f_ext
    # join the path with the file name
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resize and scales down the image using package callled pillow
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)