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
    return render_template('admin/client/gestion_client.html', user=user)

@admin_client.route('/admin/client/gestion/delete', methods=['GET'])
def delete_client():
    mycursor = get_db().cursor()
    id_client = request.args.get('id')
    tuple_insert = id_client
    sql = '''SELECT * FROM COMMANDE 
            INNER JOIN user u on commande.id_user = u.id_user
            INNER JOIN etat e on commande.id_etat = e.id_etat
            WHERE COMMANDE.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    commande = mycursor.fetchall()
    print(commande)
    if commande:
        return render_template('admin/client/delete_client.html', commande=commande)
    else:
        sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
    print("Je delete le client id : "+id_client)
    return redirect("/admin/client/gestion")

@admin_client.route('/admin/client/gestion/delete/all', methods=['GET'])
def delete_all():
    mycursor = get_db().cursor()
    id_client = request.args.get('id')
    tuple_insert = id_client
    sql = '''DELETE FROM COMMANDE WHERE COMMANDE.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/admin/client/gestion')

@admin_client.route('/admin/client/gestion/delete/commande', methods=['GET'])
def delete_client_user():
    mycursor = get_db().cursor()
    id_commande = request.args.get('id')[0]
    id_client = request.args.get('id')[1]
    tuple_insert = id_commande
    sql = '''DELETE FROM COMMANDE WHERE COMMANDE.id_commande = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    tuple_insert = id_client
    sql = '''SELECT * FROM COMMANDE 
            INNER JOIN user u on commande.id_user = u.id_user
            INNER JOIN etat e on commande.id_etat = e.id_etat
            WHERE COMMANDE.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    commande = mycursor.fetchall()
    if commande != ():
        return render_template('admin/client/delete_client.html', commande=commande)
    else:
        sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        return redirect('/admin/client/gestion')


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
    get_db().commit()
    print("J'ajoute un utilisateur")
    return redirect('/admin/client/gestion')

@admin_client.route('/admin/client/gestion/edit/<int:id>', methods=['GET'])
def edit_client(id):
    mycursor = get_db().cursor()
    tuple_insert = id
    query = '''SELECT * FROM USER WHERE USER.id_user = %s ;'''
    mycursor.execute(query, tuple_insert)
    user = mycursor.fetchone()
    return render_template('admin/client/edit_client.html', user=user)


@admin_client.route('/admin/client/gestion/edit', methods=['POST'])
def valid_edit_client():
    mycursor = get_db().cursor()
    id_user = request.form.get('id_user')
    print("Je modifie l'utilisateur : " + id_user)
    username_user = request.form.get('username_user')
    role_user = request.form.get('role_user')
    email_user = request.form.get('email_user')
    adresse_user = request.form.get('adresse_user')
    tuple_insert = (username_user, role_user, email_user, adresse_user, id_user)
    query = '''UPDATE USER SET username_user = %s, role_user = %s, email_user = %s, adresse_user = %s
                WHERE id_user = %s ;'''
    mycursor.execute(query, tuple_insert)
    get_db().commit()
    return redirect('/admin/client/gestion')