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


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    commande = '''SELECT * FROM COMMANDE
                INNER JOIN ETAT e on COMMANDE.id_etat = e.id_etat
                INNER JOIN USER u on COMMANDE.id_user = u.id_user
                INNER JOIN Ligne l on COMMANDE.id_commande = l.id_commande
                INNER JOIN SKI s on l.id_ski = s.id_ski'''
    mycursor.execute(commande)
    commande = mycursor.fetchall()
    id = []
    commande_classe = {}
    totaux = {}
    for elt in commande:
        if elt['id_commande'] not in id:
            id.append(elt['id_commande'])
            commande_classe[elt['id_commande']] = []
            totaux[elt['id_commande']] = []
    for id_elt in totaux.keys():
        r = 0
        c = 0
        for elt in commande:
            if id_elt == elt['id_commande']:
                c += 1
                r += elt['prix_unit_ligne'] * elt['quantite_ligne']
                if c == 1:
                    totaux[id_elt].append(elt['libelle_etat'])
                    totaux[id_elt].append(elt['username_user'])
                    totaux[id_elt].append(elt['id_user'])
                    totaux[id_elt].append(elt['email_user'])
                    totaux[id_elt].append(elt['adresse_user'])
                    totaux[id_elt].append(elt['date_achat_commande'])
        totaux[id_elt].append(r)
    for elt in commande:
        for id_elt in commande_classe.keys():
            if elt['id_commande'] == id_elt:
                commande_classe[id_elt].append(elt)
    return render_template('admin/commandes/show.html', commande=commande, commande_classe=commande_classe,
                           totaux=totaux)


@admin_commande.route('/admin/commande/edit/<int:id>', methods=['GET'])
def edit_commande(id):
    mycursor = get_db().cursor()
    tuple_insert = id
    query = '''SELECT * FROM COMMANDE
            INNER JOIN ETAT e on COMMANDE.id_etat = e.id_etat
            INNER JOIN USER u on COMMANDE.id_user = u.id_user
            WHERE id_commande = %s;'''
    mycursor.execute(query, tuple_insert)
    commande = mycursor.fetchone()
    query = '''SELECT * FROM ETAT;'''
    mycursor.execute(query)
    etat = mycursor.fetchall()
    return render_template('admin/commandes/edit_commande.html', commande=commande, etat=etat)


@admin_commande.route('/admin/commande/edit', methods=['POST'])
def valid_edit_commande():
    mycursor = get_db().cursor()
    id_commande = request.form.get('id_commande')
    print("Je modifie la commande : " + id_commande)
    id_etat = request.form.get('id_etat')
    tuple_insert = (id_etat, id_commande)
    query = '''UPDATE COMMANDE SET COMMANDE.id_etat =%s
                WHERE COMMANDE.id_commande = %s ;'''
    mycursor.execute(query, tuple_insert)
    get_db().commit()
    return redirect('/admin/commande/show')
