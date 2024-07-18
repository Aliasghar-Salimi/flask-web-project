from flask import (Flask, request, render_template, Blueprint, redirect, flash
                    , url_for, session, jsonify)
import connection

import hashlib

from validatoins import *

import json

from werkzeug.security import generate_password_hash, check_password_hash # http://flask.pocoo.org/snippets/54/
from datetime import datetime

user_blueprint = Blueprint('user_blueprint', __name__,
                            template_folder='templates')



@user_blueprint.route("/register/", methods=["GET","POST"])
def register():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)
    
    if request.method == "POST":
        # Retrieve name and email value from request
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        birth_date = request.form.get("birth_date")
        phone = request.form.get("phone")
        gender = request.form.get("gender")
        email = request.form.get("email")
        password = request.form.get("password")
        print(gender)
        # Retrieve users to display in home page after rendring
        select_all = "SELECT id, first_name, last_name, email FROM users;"
        cursor.execute(select_all)
        users = cursor.fetchall()

        # Validating files
        errors = (validate_username(username) + validate_first_name(first_name) 
                  + validate_last_name(last_name)+ validate_email(email, users)
                  + validate_gender(gender)+ validate_phone(phone))
    
        if errors:
            return render_template('register.html', errors=errors, first_name=first_name, last_name=last_name, email=email,
                           username=username, password=password, gender=gender, birth_date=birth_date,                           
                           phone=phone)
        if errors == []:
            # hash password 
            password = generate_password_hash(str(password))

            # insertion operation
            insertion = f"""INSERT INTO users (first_name, last_name, username, email, phone, gender,
                         birth_date, password) VALUES ('{first_name}', '{last_name}', '{username}', '{email}',
                         {phone}, '{gender}', '{birth_date}', '{password}')"""

            cursor.execute(insertion)
            cnx.commit()     
            session.permanent = True
            session['username'] = request.form.get('username')
            flash(f'user {username} created successfuly')
            return redirect(url_for('home'))
        
    elif request.method == "GET":
        return render_template('register.html')




@user_blueprint.route('/login/', methods=["POST", "GET"])
def user_login():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)

    errors = []
    if request.method == "POST":
        password = request.form.get('password')
        username = request.form.get('username')
        errors = (validate_username(username) + validate_password(password))

        select_one = "SELECT password FROM users WHERE username='{}';".format(username)
        cursor.execute(select_one)
        current_password = cursor.fetchone()

        cursor.close()
        cnx.close()
        
        if errors:
            return render_template("login.html", errors=errors)
        else:
            if cursor.rowcount > 0:
                if check_password_hash(current_password[0], password):
                    session.permanent = True
                    session['username'] = request.form.get('username')
                    return redirect('/')
                else:
                    flash('wrong username or password')
                    return redirect('/login/')
            else:
                flash('the user does not exist')
                return redirect('/login/')
    else:
        return render_template('login.html')
     
    

@user_blueprint.route("/logout/")
def logout():
	session["username"] = None
	return redirect("/")



@user_blueprint.route("/delete/<id>/", methods=["POST", "GET"])
def delete_user(id):
    # Conntect to database
    cnx = connection.connect()
    cursor = cnx.cursor()

    user_id = id

    if not user_id:
        flash('error: Missing user_id in request')
        return redirect(url_for('home'))
    
    # get user's name
    select_one = "SELECT username FROM users WHERE id={};".format(user_id)
    cursor.execute(select_one)
    user = cursor.fetchone()

    name = user[0]

    now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    delete_query = "UPDATE users SET delete_date=%s WHERE id=%s;"
    cursor.execute(delete_query, (now, user_id,))
    cnx.commit()
    
    cursor.close()
    cnx.close()

    if cursor.rowcount > 0:
        flash(f'user {name} deleted successfuly')
        return redirect('/')
    else:
        flash(f'user {name} not found')
        return redirect('/')





@user_blueprint.route("/update/", methods=["POST"])
def update_user():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor()

    # Get user information form request
    user_id = request.form.get('user_id')
    first_name =  request.form.get('first_name')
    last_name =  request.form.get('last_name')
    username = request.form.get("username")
    email = request.form.get('email')

    # Update operation
    update_query = """UPDATE users
                    SET first_name=%s, last_name=%s, username=%s, email=%s
                    WHERE id=%s;"""
    user_data = (first_name, last_name, username, email, user_id)

    cursor.execute(update_query, user_data)
    cnx.commit()

    cursor.close()
    cnx.close()

    if cursor.rowcount > 0:
        return redirect('/')
    else:
        return redirect('/')





@user_blueprint.route("/fetch-update/<id>/", methods=["GET"])
def user_update(id):
    # connect to database
    cnx = connection.connect()
    cursor = cnx.cursor()
    
    user_id = id
    
    # get user current informatino
    select_one = "SELECT first_name, last_name, username, email FROM users WHERE id={};".format(user_id)
    cursor.execute(select_one)
    user = cursor.fetchone()
    
    cursor.close()
    cnx.close()
    
    return render_template('edit.html', user=user, id=user_id)


@user_blueprint.route("/update_password/<id>/", methods=["POST"])
def update_password(id):
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor()

    # opdate operation
    current_pass = request.form["current_password"]
    c_pass = hashlib.md5(current_pass.encode('utf-8'))
    print(c_pass)

    new_pass = request.form["new_password"]
    n_pass = hashlib.md5(new_pass.encode('utf-8'))

    select_pass_query = f"SELECT password FROM users WHERE id={id}"
    cursor.execute(select_pass_query)
    old_user_pass = cursor.fetchone()
    print(old_user_pass[0])

    if old_user_pass[0] == c_pass:
        update_pass_query = f"INSERT INTO users (password) VALUES ({n_pass})"
        cursor.execute(update_pass_query)
        cnx.commit()
        
        cursor.close()
        cnx.close()
        return json.dumps({'status': 'ok'})
    else:
        return json.dumps({'status': 'failed'})
        

@user_blueprint.route("/check-password/", methods=["POST", "GET"])
def check_password():
    cnx = connection.connect()
    cursor = cnx.cursor()
    if request.method == 'POST':
        email = request.form.get("email")
        old_password = request.form.get("old-password")
        new_password = request.form.get("new-password")
        confirm_password = request.form.get("confirm_password")

        errors = []
        errors = (validate_password(new_password))

        check_users_query = f"SELECT password, email, id FROM users WHERE email='{email}'"
        cursor.execute(check_users_query)
        user = cursor.fetchone()
        
        id = user[2]
        session['id'] = id

        current_password = user[0]
        if errors:
            return render_template("check_password.html", errors=errors)
        else:
            if check_password_hash(current_password, old_password):
                # return json.dumps({'password': f"{new_password}"f"{confirm_password}"})
                if new_password == confirm_password:
                    hashed_pass = generate_password_hash(str(new_password))

                    session['hashed_pass'] = hashed_pass
                    return redirect("/send-email/")
                else:
                    flash("Password does not match")
                    return redirect("/check_password/")
            else:
                flash("enter the right password")
                return redirect("/check_password/")
    else:
        return render_template("reset_password.html")

@user_blueprint.route('/reset-password/', methods = ['POST', 'GET'])
def reset_password():
    # connect to the databes
    cnx = connection.connect()
    cursor = cnx.cursor()

    user_id = session.get('id')
    temp_code_query = f"SELECT code FROM temp_codes WHERE user_id='{user_id}'"
    cursor.execute(temp_code_query)
    temp_codes = cursor.fetchall()
    print(temp_codes)
    if cursor.rowcount != 0:
        temp_code = temp_codes[len(temp_codes)-1:]
        temp_code = temp_code[0][0]
    else:
        return json.dumps({'code': 'doesn\'t exist'})

    print(temp_code)
    
    code = request.form.get("code")
    print(code)
    if request.method == 'POST':
        if str(temp_code) == str(code):
            hashed_pass = session.get('hashed_pass')
            update_pass_query = f"update users set password='{hashed_pass}' where id='{user_id}';"
            cursor.execute(update_pass_query)
            cnx.commit()  

            delete_code_query = f"DELETE FROM temp_codes WHERE user_id={user_id}"
            cursor.execute(delete_code_query)
            cnx.commit()

            cursor.close()
            cnx.close()

            flash("password chaged")
            return redirect('/login/')
        else:
            flash("the code is incorrect")
            return render_template("email_verification.html")
    else:
        return render_template('email_verification.html')
