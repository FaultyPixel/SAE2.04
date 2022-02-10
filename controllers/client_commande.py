#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    flash(u'Commande ajoutée')
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))



@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    id_commande = request.form.get('idCommande','')
    mycursor = get_db().cursor()

    sql = '''SELECT COMMANDE.id_commande, date_achat_commande, COMMANDE.id_etat, id_user, id_ski, SUM(prix_unit_ligne*quantite_ligne) AS prix_total,
                SUM(quantite_ligne) AS nbre_articles, libelle_etat AS libelle
                FROM COMMANDE
                JOIN Ligne ON COMMANDE.id_commande = Ligne.id_commande
                JOIN ETAT ON COMMANDE.id_etat = ETAT.id_etat
                WHERE id_user = %s;'''
    mycursor.execute(sql, session['user_id'])
    commandes = mycursor.fetchall()


    sql=''' SELECT Ligne.id_ski, Ligne.id_commande, prix_unit_ligne AS prix, quantite_ligne AS quantite, prix_unit_ligne*quantite_ligne AS prix_ligne, modele_ski AS nom
            FROM Ligne
            JOIN COMMANDE ON Ligne.id_commande = COMMANDE.id_commande
            JOIN SKI S on Ligne.id_ski = S.id_ski
            WHERE COMMANDE.id_commande = %s;'''

    mycursor.execute(sql, id_commande)
    articles_commande = mycursor.fetchall()
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

