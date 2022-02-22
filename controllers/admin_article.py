#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                        template_folder='templates')

@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    articles = ''' SELECT * 
                FROM SKI AS s 
                LEFT JOIN note n on s.id_ski = n.id_ski'''
    mycursor.execute(articles)
    articles = mycursor.fetchall()
    print(articles)
    return render_template('admin/article/show_article.html', articles=articles)

@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    mycursor = get_db().cursor()
    id_article = request.args.get('id')
    print(id_article)
    tuple_insert = id_article
    sqlL = '''SELECT * FROM LIGNE AS l
                WHERE l.id_ski = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                INNER JOIN USER u on p.id_user = u.id_user
                WHERE p.id_ski = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                    INNER JOIN USER u on c.id_user = u.id_user
                    WHERE c.id_ski = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    ligne = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    print(ligne)
    print(panier)
    print(commentaire)
    if ligne or panier or commentaire:
        sql = '''SELECT s.id_ski, s.modele_ski FROM SKI AS s
                            WHERE s.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        ski = mycursor.fetchone()
        print(ski)
        return render_template('admin/article/delete_article.html', ligne=ligne, panier=panier, commentaire=commentaire, ski=ski)
    else:
        sql = '''DELETE FROM FOURNI WHERE FOURNI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        sql = '''DELETE FROM SKI WHERE SKI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un article supprimé, id :", id_article)
        flash(u'un article supprimé, id : ' + id_article)
        return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete/panier', methods=['GET'])
def delete_article_panier():
    mycursor = get_db().cursor()
    id_panier = request.args.get('id')[-2]
    id_article = request.args.get('id')[-1]
    tuple_insert = id_panier
    sql = '''DELETE FROM PANIER WHERE PANIER.id_panier = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    tuple_insert = id_article
    sqlL = '''SELECT * FROM LIGNE AS l
                    WHERE l.id_ski = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                    INNER JOIN USER u on p.id_user = u.id_user
                    WHERE p.id_ski = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                        INNER JOIN USER u on c.id_user = u.id_user
                        WHERE c.id_ski = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    ligne = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    if ligne or panier or commentaire:
        sql = '''SELECT s.id_ski, s.modele_ski FROM SKI AS s
                                WHERE s.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        ski = mycursor.fetchone()
        return render_template('admin/article/delete_article.html', ligne=ligne, panier=panier, commentaire=commentaire,
                               ski=ski)
    else:
        sql = '''DELETE FROM FOURNI WHERE FOURNI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        sql = '''DELETE FROM SKI WHERE SKI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un article supprimé, id :", id_article)
        flash(u'un article supprimé, id : ' + id_article)
        return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete/ligne', methods=['GET'])
def delete_article_ligne():
    mycursor = get_db().cursor()
    id_commande = request.args.get('id')[-2]
    id_article = request.args.get('id')[-1]
    tuple_insert = id_commande
    sql = '''DELETE FROM LIGNE WHERE LIGNE.id_commande = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    tuple_insert = id_article
    sqlL = '''SELECT * FROM LIGNE AS l
                    WHERE l.id_ski = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                    INNER JOIN USER u on p.id_user = u.id_user
                    WHERE p.id_ski = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                        INNER JOIN USER u on c.id_user = u.id_user
                        WHERE c.id_ski = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    ligne = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    if ligne or panier or commentaire:
        sql = '''SELECT s.id_ski, s.modele_ski FROM SKI AS s
                                WHERE s.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        ski = mycursor.fetchone()
        return render_template('admin/article/delete_article.html', ligne=ligne, panier=panier, commentaire=commentaire,
                               ski=ski)
    else:
        sql = '''DELETE FROM FOURNI WHERE FOURNI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        sql = '''DELETE FROM SKI WHERE SKI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un article supprimé, id :", id_article)
        flash(u'un article supprimé, id : ' + id_article)
        return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete/commentaire', methods=['GET'])
def delete_article_commentaire():
    mycursor = get_db().cursor()
    id_commentaire = request.args.get('id')[-2]
    id_article = request.args.get('id')[-1]
    tuple_insert = id_commentaire
    sql = '''DELETE FROM COMMENTAIRE WHERE COMMENTAIRE.id_commentaire = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    tuple_insert = id_article
    sqlL = '''SELECT * FROM LIGNE AS l
                    WHERE l.id_ski = %s;'''
    sqlP = '''SELECT * FROM PANIER AS p
                    INNER JOIN USER u on p.id_user = u.id_user
                    WHERE p.id_ski = %s;'''
    sqlC = '''SELECT * FROM COMMENTAIRE AS c 
                        INNER JOIN USER u on c.id_user = u.id_user
                        WHERE c.id_ski = %s;'''
    mycursor.execute(sqlL, tuple_insert)
    ligne = mycursor.fetchall()
    mycursor.execute(sqlP, tuple_insert)
    panier = mycursor.fetchall()
    mycursor.execute(sqlC, tuple_insert)
    commentaire = mycursor.fetchall()
    if ligne or panier or commentaire:
        sql = '''SELECT s.id_ski, s.modele_ski FROM SKI AS s
                                WHERE s.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        ski = mycursor.fetchone()
        return render_template('admin/article/delete_article.html', ligne=ligne, panier=panier, commentaire=commentaire,
                               ski=ski)
    else:
        sql = '''DELETE FROM FOURNI WHERE FOURNI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        sql = '''DELETE FROM SKI WHERE SKI.id_ski = %s;'''
        mycursor.execute(sql, tuple_insert)
        get_db().commit()
        print("un article supprimé, id :", id_article)
        flash(u'un article supprimé, id : ' + id_article)
        return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete/all', methods=['GET'])
def delete_all():
    mycursor = get_db().cursor()
    id_article = request.args.get('id')
    tuple_insert = id_article
    sql = '''DELETE FROM COMMENTAIRE WHERE COMMENTAIRE.id_ski = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM LIGNE WHERE LIGNE.id_ski = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM PANIER WHERE PANIER.id_ski = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM FOURNI WHERE FOURNI.id_ski = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    sql = '''DELETE FROM SKI WHERE SKI.id_ski = %s;'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print("un article supprimé, id :", id_article)
    flash(u'un article supprimé, id : ' + id_article)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/edit/<int:id>', methods=['GET'])
def edit_article(id):
    mycursor = get_db().cursor()
    tuple_insert = id
    sql = '''SELECT * FROM SKI 
                INNER JOIN PAYS_FABRICATION AS p ON SKI.id_pays_fabrication = p.id_pays_fabrication
                INNER JOIN NIVEAU_SKIEUR AS n ON SKI.id_niveau_skieur = n.id_niveau_skieur
                INNER JOIN POIDS_SKIEUR AS p2 ON SKI.id_poids_skieur = p2.id_poids_skieur
                INNER JOIN NOYAU AS n2 ON SKI.id_noyau = n2.id_noyau
                INNER JOIN FIXATION AS f ON SKI.id_fixation = f.id_fixation
                INNER JOIN SEXE AS s ON SKI.id_sexe = s.id_sexe
                INNER JOIN FABRICANT AS f2 ON SKI.id_fabricant = f2.id_fabricant
                INNER JOIN TYPE_SKI AS t ON SKI.id_type_ski = t.id_type_ski
                WHERE id_ski = %s;'''
    mycursor.execute(sql, tuple_insert)
    article = mycursor.fetchone()
    print(article)
    sql = '''SELECT * FROM PAYS_FABRICATION AS p WHERE p.id_pays_fabrication NOT IN(SELECT p.id_pays_fabrication FROM SKI 
                    INNER JOIN PAYS_FABRICATION AS p ON SKI.id_pays_fabrication = p.id_pays_fabrication
                    WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    pays_fabrication = mycursor.fetchall()
    sql = '''SELECT * FROM NIVEAU_SKIEUR AS n WHERE n.id_niveau_skieur NOT IN(SELECT n.id_niveau_skieur FROM SKI 
                        INNER JOIN NIVEAU_SKIEUR AS n ON SKI.id_niveau_skieur = n.id_niveau_skieur
                        WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    niveau_skieur = mycursor.fetchall()
    sql = '''SELECT * FROM POIDS_SKIEUR AS p WHERE p.id_poids_skieur NOT IN(SELECT p.id_poids_skieur FROM SKI 
                            INNER JOIN POIDS_SKIEUR AS p ON SKI.id_poids_skieur = p.id_poids_skieur
                            WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    poids_skieur = mycursor.fetchall()
    sql = '''SELECT * FROM NOYAU AS n WHERE n.id_noyau NOT IN(SELECT n.id_noyau FROM SKI 
                        INNER JOIN NOYAU AS n ON SKI.id_noyau = n.id_noyau
                            WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    noyau = mycursor.fetchall()
    sql = '''SELECT * FROM FIXATION AS f WHERE f.id_fixation NOT IN(SELECT f.id_fixation FROM SKI 
                            INNER JOIN FIXATION AS f ON SKI.id_noyau = f.id_fixation
                                WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    fixation = mycursor.fetchall()
    sql = '''SELECT * FROM SEXE AS s WHERE s.id_sexe NOT IN(SELECT s.id_sexe FROM SKI 
                                INNER JOIN SEXE AS s ON SKI.id_sexe = s.id_sexe
                                    WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    sexe = mycursor.fetchall()
    sql = '''SELECT * FROM FABRICANT AS f WHERE f.id_fabricant NOT IN(SELECT f.id_fabricant FROM SKI 
                                    INNER JOIN FABRICANT AS f ON SKI.id_fabricant = f.id_fabricant
                                        WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    fabricant = mycursor.fetchall()
    sql = '''SELECT * FROM TYPE_SKI AS t WHERE t.id_type_ski NOT IN(SELECT t.id_type_ski FROM SKI 
                                        INNER JOIN TYPE_SKI AS t ON SKI.id_type_ski = t.id_type_ski
                                            WHERE id_ski = %s);'''
    mycursor.execute(sql, tuple_insert)
    type_ski = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', article=article, pays_fabrication=pays_fabrication,
                           niveau_skieur=niveau_skieur, poids_skieur=poids_skieur, noyau=noyau, fixation=fixation,
                           sexe=sexe, fabricant=fabricant, type_ski=type_ski)

@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    id_ski = request.form.get('id_ski')
    modele_ski = request.form.get('modele_ski')
    image_ski = request.form.get('image_ski')
    prix_ski = request.form.get('prix_ski')
    poids_ski = request.form.get('poids_ski')
    longueur_ski = request.form.get('longueur_ski')
    stock_ski = request.form.get('stock_ski')
    annee = request.form.get('AAAA')
    id_pays_fabrication = request.form.get('id_pays_fabrication')
    id_niveau_skieur = request.form.get('id_niveau_skieur')
    id_poids_skieur = request.form.get('id_poids_skieur')
    id_noyau = request.form.get('id_noyau')
    id_fixation = request.form.get('id_fixation')
    id_sexe = request.form.get('id_sexe')
    id_fabricant = request.form.get('id_fabricant')
    id_type_ski = request.form.get('id_type_ski')
    tuple_insert = (modele_ski,image_ski,prix_ski,poids_ski,longueur_ski, stock_ski, annee, id_pays_fabrication, id_niveau_skieur, id_poids_skieur, id_noyau, id_fixation, id_sexe, id_fabricant, id_type_ski, id_ski)
    query = '''UPDATE SKI SET modele_ski = %s, image_ski = %s, prix_ski = %s, poids_ski = %s, longueur_ski = %s, 
                    stock_ski = %s, AAAA = %s, id_pays_fabrication = %s, id_niveau_skieur = %s, id_poids_skieur = %s,
                    id_noyau = %s, id_fixation = %s, id_sexe = %s, id_fabricant = %s, id_type_ski = %s
                    WHERE id_ski = %s ;'''
    mycursor.execute(query, tuple_insert)
    get_db().commit()
    #print(u'article modifié , nom : ', nom, ' - type_article:', type_article_id, ' - prix:', prix, ' - stock:', stock, ' - description:', description, ' - image:', image)
    #message = u'article modifié , nom:'+nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - stock:'+  stock + ' - description:' + description + ' - image:' + image
    #flash(message)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM PAYS_FABRICATION ;'''
    mycursor.execute(sql)
    pays_fabrication = mycursor.fetchall()
    sql = '''SELECT * FROM NIVEAU_SKIEUR ;'''
    mycursor.execute(sql)
    niveau_skieur = mycursor.fetchall()
    sql = '''SELECT * FROM POIDS_SKIEUR ;'''
    mycursor.execute(sql)
    poids_skieur = mycursor.fetchall()
    sql = '''SELECT * FROM NOYAU ;'''
    mycursor.execute(sql)
    noyau = mycursor.fetchall()
    sql = '''SELECT * FROM FIXATION ;'''
    mycursor.execute(sql)
    fixation = mycursor.fetchall()
    sql = '''SELECT * FROM SEXE ;'''
    mycursor.execute(sql)
    sexe = mycursor.fetchall()
    sql = '''SELECT * FROM FABRICANT ;'''
    mycursor.execute(sql)
    fabricant = mycursor.fetchall()
    sql = '''SELECT * FROM TYPE_SKI ;'''
    mycursor.execute(sql)
    type_ski = mycursor.fetchall()
    print(pays_fabrication)
    print(niveau_skieur)
    print(poids_skieur)
    print(noyau)
    print(fixation)
    print(sexe)
    print(fabricant)
    print(type_ski)
    return render_template('admin/article/add_article.html', pays_fabrication=pays_fabrication, niveau_skieur=niveau_skieur,
                           poids_skieur=poids_skieur, noyau=noyau, fixation=fixation, sexe=sexe, fabricant=fabricant,
                           type_ski=type_ski)

@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()
    modele_ski = request.form.get('modele_ski')
    image_ski = request.form.get('image_ski')
    prix_ski = request.form.get('prix_ski')
    poids_ski = request.form.get('poids_ski')
    longueur_ski = request.form.get('longueur_ski')
    stock_ski = request.form.get('stock_ski')
    annee = request.form.get('AAAA')
    id_pays_fabrication = request.form.get('id_pays_fabrication')
    id_niveau_skieur = request.form.get('id_niveau_skieur')
    id_poids_skieur = request.form.get('id_poids_skieur')
    id_noyau = request.form.get('id_noyau')
    id_fixation = request.form.get('id_fixation')
    id_sexe = request.form.get('id_sexe')
    id_fabricant = request.form.get('id_fabricant')
    id_type_ski = request.form.get('id_type_ski')
    sql = '''SELECT * FROM SKI WHERE modele_ski = %s ;'''
    mycursor.execute(sql, modele_ski)
    retour = mycursor.fetchone()
    if retour:
        flash(u'votre article existe déjà')
        return redirect('/admin/article/add')
    tuple_insert = (modele_ski,image_ski,prix_ski,poids_ski,longueur_ski, stock_ski, annee, id_pays_fabrication,
                    id_niveau_skieur, id_poids_skieur, id_noyau, id_fixation, id_sexe, id_fabricant, id_type_ski)
    sql = '''INSERT INTO SKI(modele_ski,image_ski,prix_ski,poids_ski,longueur_ski, stock_ski, AAAA, id_pays_fabrication,
     id_niveau_skieur, id_poids_skieur, id_noyau, id_fixation, id_sexe, id_fabricant, id_type_ski) VALUES (%s,%s,%s,%s
     ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'article ajouté , nom: ', modele_ski, ' - prix:', prix_ski, ' - stock:', stock_ski,
          ' - image:', image_ski)
    message = u'article ajouté , nom: '+ modele_ski+ ' - prix:'+ prix_ski+ ' - stock:'+ stock_ski+' - image:'+ image_ski
    flash(message)
    return redirect(url_for('admin_article.show_article'))