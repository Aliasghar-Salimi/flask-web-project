from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from flask_session import Session

import mysql.connector
from mysql.connector import errorcode


from blueprints.user.user import user_blueprint
from blueprints.file.upload import upload_blueprint

from flask_wtf import FlaskForm
from wtforms import FileField

import connection
from blueprints.file.upload import allowed_file, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename

import os
from pathlib import Path

from flask_bcrypt import Bcrypt

from datetime import timedelta


app = Flask(__name__)
the_bcrypt = Bcrypt(app)
app.register_blueprint(user_blueprint)
app.register_blueprint(upload_blueprint)

from flask_mail import Mail, Message

# send email configuration
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '9805cba5014dbf'
app.config['MAIL_PASSWORD'] = 'e5ba71e838d88b'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Session setings
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Secret key configuration
app.secret_key = "~\x7fS~\xa1\x08\xcd79Jgj"
app.config["SECRET_KEY"] = "~\x7fS~\xa1\x08\xcd79Jgj"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

# Media configuration
UPLOAD_FOLDER = ('media/images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def name_creater(user_files, user_id):
    file_names = []
    for files in user_files[user_id]:
        pattern1 = "b'"
        pattern2 = "\\..*"
        text = str(files)
        import re
        text = re.sub(pattern1, "", text)
        text = re.sub(pattern2, "", text)
        file_names.append(text)
    return file_names

def binary_remove(user_files, user_id):
    file_names = []
    for files in user_files[user_id]:
        pattern1 = "b'"
        text = str(files)
        import re
        text = re.sub(pattern1, "", text)
        text = text.replace("'", "")
        file_names.append(text)
    return file_names

# send email section
import json
thesender= "ali.kurd13830000@gmail.com" 
@app.route('/send-email/', methods=['POST'])
def send_email():
    therecipients = ["aliasghar.salimi.05@gmail.com"]
    msg = Message("Hi there",
                  sender=thesender,
                  recipients=therecipients)
    msg.body = "this is a test email"

    mail.send(msg)

    return json.dumps({'email': 'sent'})


@app.route("/", methods=["GET"])
def home():
    cnx = connection.connect()
    cursor = cnx.cursor()

    select_query = "SELECT id, first_name, last_name, username, email, phone, gender, birth_date FROM users WHERE delete_date is NULL;"
    cursor.execute(select_query)
    users = cursor.fetchall()

    if cursor.rowcount == 0:
        return redirect('/register/')

    # Retrieve files for each user
    user_files = {}
    user_file_types_urls = {}
    for user in users:
        user_id = user[0]
        if session.get('username'):
            # Fetch user's filenames to show in home page
            select_file_query = f"SELECT filename FROM files WHERE user_id={user_id};"
            cursor.execute(select_file_query)
            files = cursor.fetchall()

            user_files[user_id] = [file[0] for file in files]

            name_but_binary = binary_remove(user_files, user_id)
            file_names = name_creater(user_files, user_id)

            user_files[user_id] = [file for file in file_names]
            user_file_types_urls[user_id] = [file for file in name_but_binary]

            # Generate URLs for the images
            user_file_urls = {}
            user_file_urls[user_id] = [os.path.join(UPLOAD_FOLDER, file) for file in user_file_types_urls[user_id]]

            cursor.close()
            cnx.close()
            return render_template('home.html', users=users, user_files=user_files, user_file_urls=user_file_urls, session=session)
        else:
            return redirect('/login/')


if __name__ == "__main__":
    app.run(debug=True)
