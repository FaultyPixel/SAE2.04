#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    idSki = request.form.get("idArticle")
    userID = session["user_id"]
    qte = int(request.form.get("quantite", 1))
    print(userID)
    print(idSki)
    print(qte)
    sql = """SELECT quantite_panier FROM PANIER WHERE id_user=%s AND id_ski=%s"""
    tpl = (userID, idSki)
    mycursor.execute(sql, tpl)
    qte_panier = mycursor.fetchone()
    print(qte_panier)

    sql = """SELECT stock_ski FROM SKI WHERE id_ski=%s"""
    mycursor.execute(sql, idSki)
    stock = mycursor.fetchone()["stock_ski"]
    if qte_panier:
        qte += qte_panier["quantite_panier"]
        if qte > stock:
            qte = stock
            flash(f"Il n'y a que {stock} skis disponibles pour cet article")
        sql = """UPDATE PANIER SET quantite_panier=%s WHERE id_user=%s AND id_ski=%s"""
    else:
        sql = """INSERT INTO PANIER(quantite_panier, id_user, id_ski) VALUES (%s,%s,%s)"""
    tpl = (qte, userID, idSki)
    mycursor.execute(sql, tpl)
    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_ski = request.form.get("idArticle")
    user_id = session["user_id"]
    tpl = (user_id, id_ski)
    print(tpl)
    sql = """SELECT quantite_panier FROM PANIER WHERE id_user=%s AND id_ski=%s"""
    mycursor.execute(sql, tpl)
    qte = mycursor.fetchone()["quantite_panier"]
    if qte > 1:
        tpl = (qte-1,id_ski, user_id )
        sql = """UPDATE PANIER SET quantite_panier=%s WHERE id_ski=%s AND id_user=%s"""
    else:
        tpl = (id_ski, user_id)
        sql = """DELETE FROM PANIER WHERE id_ski=%s and id_user=%s"""
    mycursor.execute(sql, tpl)

    get_db().commit()

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    sql = """DELETE FROM PANIER WHERE id_user=%s"""
    tpl = session["user_id"]
    mycursor.execute(sql, tpl)
    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_ski = request.form.get("idArticle")
    sql = """DELETE FROM PANIER WHERE id_ski=%s AND id_user=%s"""
    tpl = (id_ski, session["user_id"])
    mycursor.execute(sql, tpl)
    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    # SQL
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))
