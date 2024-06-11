from flask import (Flask, request, render_template, Blueprint, redirect, flash
                    , url_for, session)
import connection

import os
from pathlib import Path

import re
from validatoins import *


user_blueprint = Blueprint('user_blueprint', __name__,
                            template_folder='templates')



@user_blueprint.route("/insert/", methods=["POST"])
def insert_user():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)
    
    # Retrieve name and email value from request
    username = request.form["username"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    password = request.form["password"]
    birth_date = request.form["birth_date"]
    phone = request.form["phone"]
    gender = request.form["gender"]
    email = request.form["email"]


    # Retrieve users to display in home page after rendring
    select_all = "SELECT user_id, first_name, last_name, email FROM users;"
    cursor.execute(select_all)
    users = cursor.fetchall()

    errors = (validate_username(username) + validate_first_name(first_name) 
              + validate_last_name(last_name)+ validate_email(email, users)
              + validate_gender(gender) + validate_birthdate(birth_date) 
              + validate_password(password)) + validate_phone(phone)

    if errors:
        session['username'] = username
        session['password'] = password
        session['gender'] = gender
        session['first_name'] = first_name
        session['last_name'] = last_name
        session['birth_date'] = birth_date
        session['phone'] = phone
        session['email'] = email
        session['errors'] = errors
        return redirect(url_for('login_errors', first_name=session['first_name'], 
                                last_name=session['last_name'], username=session['username'], 
                                password=session['password'], gender=session['gender'], 
                                email=session['email'], birth_date=session['birth_date'], 
                                phone=session['phone'], errors=session['errors']))
    
    if errors == []:
        # hash password 
        from main import the_bcrypt
        password = the_bcrypt.generate_password_hash('password').decode('utf-8')
        # insertion operation
        insertion = f"""INSERT INTO users (first_name, last_name, username, email, phone, gender,
                     birth_date, password) VALUES ('{first_name}', '{last_name}', '{username}', '{email}',
                     {phone}, '{gender}', STR_TO_DATE('{birth_date}','%m-%d-%Y'), '{password}')"""

        cursor.execute(insertion)
        cnx.commit()     
        flash(f'user {username} created successfuly')
        return redirect(url_for('user_list'))



@user_blueprint.route("/delete-user/<id>/")
def delete_view(id):
    # Conntect to database
    cnx = connection.connect()
    cursor = cnx.cursor()

    user_id = id

    # get user current informatino
    select_one = "SELECT username, email FROM users WHERE user_id={};".format(user_id)
    cursor.execute(select_one)
    user = cursor.fetchone()

    if cursor.rowcount > 0:
        return render_template('delete_user.html', id=user_id, user=user)
    else:
        return redirect('/home')




@user_blueprint.route("/delete/<id>/", methods=["POST"])
def delete_user(id):
    # Conntect to database
    cnx = connection.connect()
    cursor = cnx.cursor()

    user_id = id

    if not user_id:
        flash('error: Missing user_id in request')
        return redirect(url_for('home'))
    
    # get user's name
    select_one = "SELECT username FROM users WHERE user_id={};".format(user_id)
    cursor.execute(select_one)
    user = cursor.fetchone()

    name = user[0]

    # delete_files = 'DELETE FROM files WHERE user_id=%s;'
    # cursor.execute(delete_files, (user_id,))
    # cnx.commit()

    delete_query = "DELETE FROM users WHERE user_id=%s;"
    cursor.execute(delete_query, (user_id,))
    cnx.commit()
    
    cursor.close()
    cnx.close()

    if cursor.rowcount > 0:
        flash(f'user {name} deleted successfuly')
        return redirect('/home')
    else:
        flash(f'user {name} not found')
        return redirect('/home')





@user_blueprint.route("/update/", methods=["POST"])
def update_user():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor()

    # Get user information form request
    user_id = request.form.get('user_id')
    first_name =  request.form.get('name')
    email = request.form.get('email')

    # Update operation
    update_query = """UPDATE users
                    SET first_name=%s, email=%s
                    WHERE user_id=%s;"""
    user_data = (first_name, email, user_id)

    cursor.execute(update_query, user_data)
    cnx.commit()

    cursor.close()
    cnx.close()

    if cursor.rowcount > 0:
        return redirect('/home')
    else:
        return redirect('/home')





@user_blueprint.route("/fetch-update/<id>/", methods=["GET"])
def user_update(id):
    # connect to database
    cnx = connection.connect()
    cursor = cnx.cursor()
    
    user_id = id
    
    # get user current informatino
    select_one = "SELECT name, email FROM users WHERE user_id={};".format(user_id)
    cursor.execute(select_one)
    user = cursor.fetchone()

    cursor.close()
    cnx.close()
    
    return render_template('edit.html', user=user, id=user_id)


