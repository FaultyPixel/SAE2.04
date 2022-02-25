#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')  # remplace /client
def client_article_show():  # remplace client_index
    mycursor = get_db().cursor()
    query = """SELECT * 
               FROM SKI
               JOIN FIXATION ON SKI.id_fixation = FIXATION.id_fixation
               JOIN NIVEAU_SKIEUR ON NIVEAU_SKIEUR.id_niveau_skieur = SKI.id_niveau_skieur
               JOIN NOYAU ON SKI.id_noyau = NOYAU.id_noyau
               JOIN PAYS_FABRICATION pf on SKI.id_pays_fabrication = pf.id_pays_fabrication
               JOIN POIDS_SKIEUR ps on SKI.id_poids_skieur = ps.id_poids_skieur
               JOIN SEXE s on SKI.id_sexe = s.id_sexe
               JOIN TYPE_SKI ts on SKI.id_type_ski = ts.id_type_ski
               """
    mycursor.execute(query);
    articles = mycursor.fetchall();

    user_id = session['user_id']
    query = f"""SELECT * FROM PANIER JOIN SKI ON PANIER.id_ski = SKI.id_ski WHERE id_user=%s"""
    tpl = (user_id)
    mycursor.execute(query, tpl)
    articles_panier = mycursor.fetchall()

    sql = """SELECT prix_ski, quantite_panier FROM SKI JOIN PANIER ON SKI.id_ski = PANIER.id_ski WHERE id_user=%s"""
    mycursor.execute(sql, tpl)
    res = mycursor.fetchall()
    prix_total = 0
    for row in res:
        prix_total += row["prix_ski"] * row["quantite_panier"]

    query = """SELECT * FROM TYPE_SKI"""
    mycursor.execute(query)
    types_articles = mycursor.fetchall()
    return render_template('client/boutique/panier_article.html', articles=articles, articlesPanier=articles_panier,
                           prix_total=prix_total, itemsFiltre=types_articles)


@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()
    sql = """SELECT * 
               FROM SKI
               JOIN FIXATION ON SKI.id_fixation = FIXATION.id_fixation
               JOIN NIVEAU_SKIEUR ON NIVEAU_SKIEUR.id_niveau_skieur = SKI.id_niveau_skieur
               JOIN NOYAU ON SKI.id_noyau = NOYAU.id_noyau
               JOIN PAYS_FABRICATION pf on SKI.id_pays_fabrication = pf.id_pays_fabrication
               JOIN POIDS_SKIEUR ps on SKI.id_poids_skieur = ps.id_poids_skieur
               JOIN SEXE s on SKI.id_sexe = s.id_sexe
               JOIN TYPE_SKI ts on SKI.id_type_ski = ts.id_type_ski
               JOIN FABRICANT f2 on SKI.id_fabricant = f2.id_fabricant
               WHERE SKI.id_ski = %s;
               """
    mycursor.execute(sql, id)
    article = mycursor.fetchone()
    print(article)


    commentaires = None

    sql = """
    SELECT *
    FROM COMMANDE
    JOIN Ligne l ON COMMANDE.id_commande = l.id_commande
    WHERE id_user=%s
    GROUP BY COMMANDE.id_commande"""
    mycursor.execute(sql, session["user_id"])
    commandes_articles = mycursor.fetchall()


    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires,
                           commandes_articles=commandes_articles)
