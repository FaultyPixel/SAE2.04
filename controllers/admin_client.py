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

@admin_client.route('/admin/client/delete', methods=['GET'])
def delete_client():
    mycursor = get_db().cursor()
    id_user = request.args.get('id')
    print(id_user)
    tuple_insert = id_user
    sqlL = '''SELECT * FROM COMMANDE AS c
                WHERE c.id_user = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                WHERE p.id_user = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                    WHERE c.id_user = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    commande = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    print(commande)
    print(panier)
    print(commentaire)
    if commande or panier or commentaire:
        sql = '''SELECT u.id_user, u.username_user FROM USER AS u
                            WHERE u.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        user = mycursor.fetchone()
        print(user)
        return render_template('admin/client/delete_client.html', commande=commande, panier=panier, commentaire=commentaire, user=user)
    else:
        sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un utilisateur supprimé, id :", id_user)
        flash(u'un utilisateur supprimé, id : ' + id_user)
        return redirect(url_for('admin_client.admin_gestion'))

@admin_client.route('/admin/client/delete/panier', methods=['GET'])
def delete_user_panier():
    mycursor = get_db().cursor()
    id_panier = request.args.get('id')[-2]
    id_user = request.args.get('id')[-1]
    tuple_insert = id_panier
    sql = '''DELETE FROM PANIER WHERE PANIER.id_panier = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    tuple_insert = id_user
    sqlL = '''SELECT * FROM COMMANDE AS c
                    WHERE c.id_user = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                    WHERE p.id_user = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                        WHERE c.id_user = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    commande = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    if commande or panier or commentaire:
        sql = '''SELECT u.id_user, u.username_user FROM USER AS u
                            WHERE u.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        user = mycursor.fetchone()
        print(user)
        return render_template('admin/client/delete_client.html', commande=commande, panier=panier,
                               commentaire=commentaire, user=user)
    else:
        sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un utilisateur supprimé, id :", id_user)
        flash(u'un utilisateur supprimé, id : ' + id_user)
        return redirect(url_for('admin_client.admin_gestion'))

@admin_client.route('/admin/client/delete/commande', methods=['GET'])
def delete_client_commande():
    mycursor = get_db().cursor()
    id_commande = request.args.get('id')[-2]
    id_user = request.args.get('id')[-1]
    tuple_insert = id_commande
    sql = '''DELETE FROM LIGNE WHERE LIGNE.id_commande = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM COMMANDE WHERE COMMANDE.id_commande = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    tuple_insert = id_user
    sqlL = '''SELECT * FROM COMMANDE AS c
                        WHERE c.id_user = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                        WHERE p.id_user = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                            WHERE c.id_user = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    commande = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    if commande or panier or commentaire:
        sql = '''SELECT u.id_user, u.username_user FROM USER AS u
                            WHERE u.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        user = mycursor.fetchone()
        print(user)
        return render_template('admin/client/delete_client.html', commande=commande, panier=panier,
                               commentaire=commentaire, user=user)
    else:
        sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un utilisateur supprimé, id :", id_user)
        flash(u'un utilisateur supprimé, id : ' + id_user)
        return redirect(url_for('admin_client.admin_gestion'))

@admin_client.route('/admin/client/delete/commentaire', methods=['GET'])
def delete_client_commentaire():
    mycursor = get_db().cursor()
    id_commentaire = request.args.get('id')[-2]
    id_user = request.args.get('id')[-1]
    tuple_insert = id_commentaire
    sql = '''DELETE FROM COMMENTAIRE WHERE COMMENTAIRE.id_commentaire = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    tuple_insert = id_user
    sqlL = '''SELECT * FROM COMMANDE AS c
                            WHERE c.id_user = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                            WHERE p.id_user = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                                WHERE c.id_user = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    commande = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    if commande or panier or commentaire:
        sql = '''SELECT u.id_user, u.username_user FROM USER AS u
                                WHERE u.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        user = mycursor.fetchone()
        print(user)
        return render_template('admin/client/delete_client.html', commande=commande, panier=panier,
                               commentaire=commentaire, user=user)
    else:
        sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un utilisateur supprimé, id :", id_user)
        flash(u'un utilisateur supprimé, id : ' + id_user)
        return redirect(url_for('admin_client.admin_gestion'))

@admin_client.route('/admin/client/delete/all', methods=['GET'])
def delete_all():
    mycursor = get_db().cursor()
    id_user = request.args.get('id')
    tuple_insert = id_user
    sql = '''SELECT COMMANDE.id_commande FROM COMMANDE WHERE COMMANDE.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    ligne = mycursor.fetchall()
    for elt in ligne:
        tuple_insert = elt['id_commande']
        sql = '''DELETE FROM LIGNE WHERE LIGNE.id_commande = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
    tuple_insert = id_user
    sql = '''DELETE FROM COMMENTAIRE WHERE COMMENTAIRE.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM COMMANDE WHERE COMMANDE.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM PANIER WHERE PANIER.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM USER WHERE USER.id_user = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print("un utilisateur supprimé, id :", id_user)
    flash(u'un utilisateur supprimé, id : ' + id_user)
    return redirect(url_for('admin_client.admin_gestion'))


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