#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from connexion_db import get_db

admin_client = Blueprint('admin_client', __name__,
                        template_folder='templates')

@admin_client.route('/admin/client/gestion')
def admin_gestion():
    print("Je vais afficher les clients")
    mycursor = get_db().cursor()
    insert = session['user_id']
    sql = ''' SELECT * FROM USER 
            WHERE USER.id_user != %s;'''
    mycursor.execute(sql, insert)
    user = mycursor.fetchall()
    print(user)
    return render_template('admin/client/gestion_client.html', user=user)

@admin_client.route('/admin/client/gestion/delete', methods=['GET'])
def delete_client():
    mycursor = get_db().cursor()
    id_client = request.args.get('id')
    print("Je delete le client id : "+id_client)
    tuple_insert = id_client
    sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect("/admin/client/gestion")

@admin_client.route('/admin/client/gestion/add', methods=['GET'])
def add_client():
    return render_template('admin/client/add_client.html')


@admin_client.route('/admin/client/gestion/add', methods=['POST'])
def valid_add_client():
    mycursor = get_db().cursor()
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    adresse = request.form.get('adresse')
    role = request.form.get('role_user', '')
    tuple_select = (username, email)
    sql = '''SELECT * FROM USER WHERE username_user = %s or email_user = %s'''
    retour = mycursor.execute(sql, tuple_select)
    user = mycursor.fetchone()
    if user:
        flash(u'votre adresse <strong>Email</strong> ou  votre <strong>Username</strong> (login) existe déjà')
        return redirect('/admin/client/gestion/add')

    # ajouter un nouveau user
    password = generate_password_hash(password, method='sha256')
    tuple_insert = (username, email, password, role, adresse)
    sql = '''INSERT INTO user(username_user,email_user,password_user,role_user, adresse_user) VALUES (%s,%s,%s,%s,%s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()  # position de cette ligne discutatble !
    sql = '''SELECT last_insert_id() AS last_insert_id;'''
    mycursor.execute(sql)
    info_last_id = mycursor.fetchone()
    user_id = info_last_id['last_insert_id']
    print('last_insert_id', user_id)
    get_db().commit()
    return redirect('/admin/client/gestion')