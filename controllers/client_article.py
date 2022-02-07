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
               JOIN NIVEAU_SKIEUR ON NIVEAU_SKIEUR.id_niveau_skieur = ski.id_niveau_skieur
               JOIN NOYAU ON SKI.id_noyau = NOYAU.id_noyau
               JOIN PAYS_FABRICATION pf on SKI.id_pays_fabrication = pf.id_pays_fabrication
               JOIN POIDS_SKIEUR ps on SKI.id_poids_skieur = ps.id_poids_skieur
               JOIN SEXE s on SKI.id_sexe = s.id_sexe
               JOIN TYPE_SKI ts on SKI.id_type_ski = ts.id_type_ski
               """
    mycursor.execute(query);
    articles = mycursor.fetchall();
    print(articles)

    sql = """SELECT * FROM type_ski"""
    mycursor.execute(query)
    types_articles = mycursor.fetchall()
    user_id = session['user_id']
    query = f"""SELECT * FROM PANIER JOIN SKI ON PANIER.id_ski = SKI.id_ski WHERE id_user=%s"""
    tpl = (user_id)
    mycursor.execute(query, tpl)
    articles_panier = mycursor.fetchall()

    prix_total = None
    return render_template('client/boutique/panier_article.html', articles=articles, articlesPanier=articles_panier,
                           prix_total=prix_total, itemsFiltre=types_articles)


@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()
    article = None
    commentaires = None
    commandes_articles = None
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires,
                           commandes_articles=commandes_articles)
