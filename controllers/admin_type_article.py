#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = ''' SELECT COUNT(*) AS Nb_ski, TS.libelle_type_ski, TS.id_type_ski
                FROM SKI
                INNER JOIN TYPE_SKI TS on SKI.id_type_ski = TS.id_type_ski
                GROUP BY TS.libelle_type_ski
                ORDER BY TS.id_type_ski; '''
    mycursor.execute(sql)
    types_articles = mycursor.fetchall()
    print(types_articles)
    return render_template('admin/type_article/show_type_article.html', types_articles=types_articles)

@admin_type_article.route('/admin/type-article/etat')
def etat_type_article():
    return render_template('admin/type_article/etat_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle_type_ski', '')
    sql = ''' SELECT * FROM TYPE_SKI '''
    mycursor.execute(sql)
    types_articles = mycursor.fetchall()
    tuple_insert = (libelle)
    for elt in types_articles:
        if elt['libelle_type_ski'] == tuple_insert:
            message = u'type déjà ajouté veuillez réessayer'
            flash(message)
            return render_template('admin/type_article/add_type_article.html')
    sql = '''INSERT INTO TYPE_SKI(libelle_type_ski) VALUES (%s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message)
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    id_type_article = request.args.get('id', '')
    mycursor = get_db().cursor()
    tuple_insert = id_type_article
    sql = ''' SELECT * FROM SKI
    INNER JOIN TYPE_SKI AS ts on SKI.id_type_ski = ts.id_type_ski
                        WHERE ts.id_type_ski = %s; '''
    mycursor.execute(sql, tuple_insert)
    type_article = mycursor.fetchall()
    print(type_article)
    if type_article:
        flash(u'Il y a des articles qui sont associés aux type : '+type_article[0]['libelle_type_ski']+', veuillez '
              'd\'abord les supprimés')
        for elt in type_article:
            return redirect('/admin/article/delete?id='+str(elt['id_ski']))
    else:
        print('nlol')
    flash(u'suppression type article , id : ' + id_type_article)
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/edit/<int:id>', methods=['GET'])
def edit_type_article(id):
    mycursor = get_db().cursor()
    tuple_insert = id
    sql = ''' SELECT * FROM TYPE_SKI 
                    WHERE TYPE_SKI.id_type_ski = %s; '''
    mycursor.execute(sql, tuple_insert)
    type_article = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    mycursor = get_db().cursor()
    libelle = request.form['libelle_type_article']
    id_type_article = request.form.get('id', '')
    tuple_insert = (libelle, id_type_article)
    query = '''UPDATE TYPE_SKI SET libelle_type_ski = %s
                        WHERE id_type_ski = %s ;'''
    mycursor.execute(query, tuple_insert)
    get_db().commit()
    flash(u'type article modifié, id: ' + id_type_article + " libelle : " + libelle)
    return redirect('/admin/type-article/show') #url_for('show_type_article')







