from flask import Flask, request, render_template, session, redirect, url_for
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

app = Flask(__name__)
the_bcrypt = Bcrypt(app)
app.register_blueprint(user_blueprint)
app.register_blueprint(upload_blueprint)


# Secret key configuration
app.secret_key = "~\x7fS~\xa1\x08\xcd79Jgj"
app.config["SECRET_KEY"] = "~\x7fS~\xa1\x08\xcd79Jgj"

# Media configuration
cwd = Path.cwd()
UPLOAD_FOLDER = Path.joinpath(cwd, 'media/images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/home/", methods=["GET"])
def user_list():
    cnx = connection.connect()
    cursor = cnx.cursor()

    select_query = "SELECT user_id, first_name, last_name, username, email, phone, gender, birth_date FROM users;"
    cursor.execute(select_query)
    users = cursor.fetchall()
    
    # Retrieve files for each user
    user_files = {}
    
    for user in users:
        user_id = user[0]

        # Fetch user's filenames to show in home page
        select_file_query = "SELECT filename FROM files WHERE user_id=%s;"
        cursor.execute(select_file_query, (user_id,))
        files = cursor.fetchall()
        user_files[user_id] = [file[0] for file in files]

        file_names = []
        for files in user_files[user_id]:
            pattern1 = "b'"
            pattern2 = "\\..*"
            text = str(files)
            import re
            text = re.sub(pattern1, "", text)
            text = re.sub(pattern2, "", text)
            file_names.append(text)
        print(file_names)

        user_files[user_id] = [file for file in file_names]


        user_file_urls = {}
        # Generate URLs for the images
        # user_file_urls[user_id] = [url_for('static', os.path.join(UPLOAD_FOLDER, file)) for file in user_files[user_id]]
        # print(user_file_urls[user_id])

    cursor.close()
    cnx.close()
    
    return render_template('home.html', users=users, user_files=user_files,
                            )
""" user_file_urls=user_file_urls """



@app.route('/login/')
def login():
    return render_template('login.html')




@app.route('/login/errors/')
def login_errors():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)

    # Retrieve users, name, and email value from passed data
    username = session['username']
    password = session['password']
    phone = session['phone']
    first_name = session['first_name']
    last_name = session['last_name']
    gender = session['gender']
    birth_date = session['birth_date']
    email = session['email']
    errors = session['errors']

    return render_template('login.html', errors=errors, first_name=first_name, last_name=last_name, email=email,
                           username=username, password=password, gender=gender, birth_date=birth_date,                           
                           phone=phone)


if __name__ == "__main__":
    app.run(debug=True)
