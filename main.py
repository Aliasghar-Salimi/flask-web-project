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


app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(upload_blueprint)

# Secret key configuration
app.secret_key = "~\x7fS~\xa1\x08\xcd79Jgj"
app.config["SECRET_KEY"] = "~\x7fS~\xa1\x08\xcd79Jgj"

# Media configuration
cwd = Path.cwd()
UPLOAD_FOLDER = Path.joinpath(cwd, 'media/images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Database configiration
db_name = "employees"
db_user = "root"
db_password = "ali@1234"
db_host = "127.0.0.1"


@app.route("/home/", methods=["GET"])
def user_list():
    cnx = connection.connect()
    cursor = cnx.cursor()

    select_query = "SELECT user_id, name, email FROM user;"
    cursor.execute(select_query)
    users = cursor.fetchall()
    
    # Retrieve files for each user
    user_files = {}
    
    for user in users:
        user_id = user[0]

        # Fetch user's filenames to show in home page
        select_file_query = "SELECT filename FROM file WHERE user_id=%s;"
        cursor.execute(select_file_query, (user_id,))
        files = cursor.fetchall()
        user_files[user_id] = [file[0] for file in files]

        user_file_urls = {}
        # Generate URLs for the images
        user_file_urls[user_id] = [url_for('static', filename=os.path.join(UPLOAD_FOLDER, file)) for file in user_files[user_id]]
        print(user_file_urls[user_id])

    cursor.close()
    cnx.close()
    
    return render_template('home.html', users=users, user_files=user_files,
                            user_file_urls=user_file_urls)




@app.route('/login/')
def login():
    return render_template('login.html')




@app.route('/login/errors/')
def login_errors():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)

    # Retrieve users, name, and email value from passed data
    name = session['name']
    email = session['email']
    errors = session['errors']

    return render_template('login.html', errors=errors, name=name, email=email)




if __name__ == "__main__":
    app.run(debug=True)
