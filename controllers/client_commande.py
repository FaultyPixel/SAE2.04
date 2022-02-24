#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db
import datetime

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    user_id = session["user_id"]
    sql = "SELECT * FROM PANIER WHERE id_user=%s"
    mycursor.execute(sql, user_id)
    panier = mycursor.fetchall()
    if panier is None or len(panier) < 1:
        flash(message="Pas d'article dans le panier")
        return  url_for("/client/article/show")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(type(date))
    print(date)

    tpl = (date, 1, user_id)
    sql = "INSERT INTO COMMANDE (date_achat_commande, id_etat, id_user) VALUES (%s,%s,%s)"
    mycursor.execute(sql, tpl)

    sql = """SELECT last_insert_id() as last_insert_id"""
    mycursor.execute(sql)
    id_commande = mycursor.fetchone()["last_insert_id"]
    for ski in panier:
        ski_id = ski["id_ski"]

        tpl = (user_id, ski_id)
        sql = """DELETE FROM PANIER WHERE id_user=%s AND id_ski=%s"""
        mycursor.execute(sql, tpl)

        sql = """SELECT prix_ski FROM SKI WHERE id_ski=%s"""
        mycursor.execute(sql, ski_id)
        prix_unitaire = mycursor.fetchone()["prix_ski"]
        qte = ski["quantite_panier"]
        sql = """INSERT INTO Ligne(id_ski, id_commande, prix_unit_ligne, quantite_ligne) VALUES(%s,%s,%s,%s)"""
        tpl = (ski_id, id_commande, prix_unitaire, qte)
        mycursor.execute(sql, tpl)
    get_db().commit()


    flash(u'Commande ajoutée')
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))



@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    commandes = None
    articles_commande = None
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

