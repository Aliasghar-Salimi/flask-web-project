from flask import (Flask, request, render_template, Blueprint, redirect, flash
                    , url_for, session)
import connection

import os
from pathlib import Path

import re
from validatoins import validate_email, validate_name
user_blueprint = Blueprint('user_blueprint', __name__,
                            template_folder='templates')



@user_blueprint.route("/insert/", methods=["POST"])
def insert_user():
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)
    
    # Retrieve name and email value from request
    name = request.form["name"]
    email = request.form["email"]

    # Retrieve users to display in home page after rendring
    select_all = "SELECT user_id, name, email FROM user;"
    cursor.execute(select_all)
    users = cursor.fetchall()

    errors = validate_name(name) + validate_email(email, users)

    cursor.close()
    cnx.close()
    if errors:
        session['name'] = name
        session['email'] = email
        session['errors'] = errors
        return redirect(url_for('login_errors', name=session['name'], email=session['email']))
    if errors == []:
        # Connect again to database
        cnx = connection.connect()
        cursor = cnx.cursor(buffered=True)

        # Insertion operation
        insertion = "INSERT INTO user (name, email) VALUES (%s, %s)"
        data = (name, email)  
        cursor.execute(insertion, data)
        cnx.commit()     
        flash(f'user {name} created successfuly')
        return redirect(url_for('user_list'))


@user_blueprint.route("/delete-user/<id>/")
def delete_view(id):
    # Conntect to database
    cnx = connection.connect()
    cursor = cnx.cursor()

    user_id = id

    # get user current informatino
    select_one = "SELECT name, email FROM user WHERE user_id={};".format(user_id)
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
    select_one = "SELECT name FROM user WHERE user_id={};".format(user_id)
    cursor.execute(select_one)
    user = cursor.fetchone()

    name = user[0]

    delete_files = 'DELETE FROM file WHERE user_id=%s;'
    cursor.execute(delete_files, (user_id,))
    cnx.commit()

    delete_query = "DELETE FROM user WHERE user_id=%s;"
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
    name =  request.form.get('name')
    email = request.form.get('email')

    # Update operation
    update_query = """UPDATE user
                    SET name=%s, email=%s
                    WHERE user_id=%s;"""
    user_data = (name, email, user_id)

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
    select_one = "SELECT name, email FROM user WHERE user_id={};".format(user_id)
    cursor.execute(select_one)
    user = cursor.fetchone()

    cursor.close()
    cnx.close()
    
    return render_template('edit.html', user=user, id=user_id)


