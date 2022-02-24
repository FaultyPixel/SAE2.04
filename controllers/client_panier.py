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
    mycursor = get_db().cursor()
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    print((filter_word, filter_prix_min, filter_prix_max, filter_types))

    sql = """SELECT * FROM SKI
                JOIN FIXATION ON SKI.id_fixation = FIXATION.id_fixation
                JOIN NIVEAU_SKIEUR ON NIVEAU_SKIEUR.id_niveau_skieur = ski.id_niveau_skieur
                JOIN NOYAU ON SKI.id_noyau = NOYAU.id_noyau
                JOIN PAYS_FABRICATION pf on SKI.id_pays_fabrication = pf.id_pays_fabrication
                JOIN POIDS_SKIEUR ps on SKI.id_poids_skieur = ps.id_poids_skieur
                JOIN SEXE s on SKI.id_sexe = s.id_sexe
                JOIN TYPE_SKI ts on SKI.id_type_ski = ts.id_type_ski
               """
    values = []

    if (filter_word, filter_prix_min, filter_prix_max, filter_types) == ('', '', '', []):
        mycursor.execute(sql)
        articles = mycursor.fetchall()
    else:
        c = 0
        sql += "WHERE "
        session['filter_word'] = filter_word
        session['filter_prix_max'] = filter_prix_max
        session['filter_prix_min'] = filter_prix_min
        session['filter_types'] = filter_types

        if filter_word:
            # sql += 'modele_ski LIKE "%%s%' # Si j'utilise ça il y a une erreur de symbol non supporté
            # sql += 'modele_ski RLIKE ".*%s.*"\n' # Si j'utilise cette ligne sans ajouter "*" devant le mot, aucun resultat car ce foutu pymysql ajoute des caractères dans ma string. si je veux chercher .*2022.*, avec %s le 2022 devient '2022' et la regex ne donnera plus aucun resultat
            sql += 'modele_ski RLIKE ".*%s*.*"\n'  # c'est immonde mais ça marche
            values.append("*"+filter_word)
            c += 1

        if filter_prix_min:
            if c > 0:
                sql += "AND "
            sql += "prix_ski > %s\n"
            values.append(filter_prix_min)
            c += 1

        if filter_prix_max:
            if c > 0:
                sql += "AND "
            sql += "prix_ski < %s\n"
            values.append(filter_prix_max)
            c += 1

        if len(filter_types) != 0:
            if c > 0:
                sql += "AND "
            sql += "id_type_ski in %s"
            values.append(filter_types)

        # print(sql)
        print(values)
        mycursor.execute(sql, values)
        print(mycursor._last_executed)
        articles = mycursor.fetchall()

    print(articles)



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


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))
