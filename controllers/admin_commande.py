#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin/commande/index')
def admin_index():
    print("J'y vais")
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    commande = '''SELECT * FROM COMMANDE
                INNER JOIN etat e on commande.id_etat = e.id_etat
                INNER JOIN user u on commande.id_user = u.id_user'''
    mycursor.execute(commande)
    commande = mycursor.fetchall()
    return render_template('admin/commandes/show.html', commande=commande)

@admin_commande.route('/admin/commande/edit/<int:id>', methods=['GET'])
def edit_commande(id):
    mycursor = get_db().cursor()
    tuple_insert = id
    query = '''SELECT * FROM commande
            INNER JOIN etat e on commande.id_etat = e.id_etat
            INNER JOIN user u on commande.id_user = u.id_user
            WHERE id_commande = %s;'''
    mycursor.execute(query, tuple_insert)
    commande = mycursor.fetchone()
    query = '''SELECT * FROM etat;'''
    mycursor.execute(query)
    etat = mycursor.fetchall()
    print(commande)
    print(etat)
    return render_template('admin/commandes/edit_commande.html', commande=commande, etat=etat)


@admin_commande.route('/admin/commande/edit', methods=['POST'])
def valid_edit_commande():
    mycursor = get_db().cursor()
    id_commande = request.form.get('id_commande')
    print("Je modifie la commande : " + id_commande)
    id_etat = request.form.get('id_etat')
    tuple_insert = (id_etat, id_commande)
    query = '''UPDATE commande SET commande.id_etat =%s
                WHERE id_commande = %s ;'''
    mycursor.execute(query, tuple_insert)
    get_db().commit()
    return redirect('/admin/commande/show')


#@admin_commande.route('/admin/commande/valider', methods=['get','post'])
#def admin_commande_valider():
#    mycursor = get_db().cursor()
#
#    return redirect('/admin/commande/show')
