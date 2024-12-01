#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, abort, flash

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

from flask import session, g
import pymysql.cursors


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",  # à modifier
            user="shamitou",  # à modifier
            password="Ceryne2006",  # à modifier
            database="but",  # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_layout():
    return render_template('layout.html', methods=['GET'])


### Inscription ###
@app.route('/inscription/show', methods=['GET'])
def show_inscription():
    mycursor = get_db().cursor()
    sql = '''SELECT id_inscription AS id, 
                    Seance.DateSeance, 
                    Participant.Nom_Participant, 
                    Inscription.date_Inscription, 
                    Inscription.prix_inscription
             FROM Inscription
             INNER JOIN Seance ON Inscription.idSeance = Seance.id_Seance
             INNER JOIN Participant ON Inscription.idParticipant = Participant.idParticipant
             ORDER BY id_inscription;'''
    mycursor.execute(sql)
    inscriptions = mycursor.fetchall()
    return render_template('Inscription/show_inscription.html', inscriptions=inscriptions)


@app.route('/inscription/delete', methods=['GET'])
def delete_inscription():
    print('''suppression d'une inscription''')
    id = request.args.get('id')
    print("une inscription supprimée, id :", id)
    message = u'une inscription supprimée, id : ' + id
    flash(message, 'alert-warning')

    mycursor = get_db().cursor()
    sql = "DELETE FROM Inscription WHERE id_inscription=%s;"
    tuple_sql = (id,)
    mycursor.execute(sql, tuple_sql)
    get_db().commit()
    return redirect('/inscription/show')


@app.route('/inscription/add', methods=['GET'])
def add_inscription():
    mycursor = get_db().cursor()

    sql = '''SELECT id_Seance, DateSeance 
           FROM Seance'''
    mycursor.execute(sql)
    seances = mycursor.fetchall()

    sql = '''SELECT idParticipant, Nom_Participant 
             FROM Participant'''
    mycursor.execute(sql)
    participants = mycursor.fetchall()

    return render_template('Inscription/add_inscription.html', seances=seances, participants=participants)


@app.route('/inscription/add', methods=['POST'])
def valid_add_inscription():
    idSeance = request.form.get('idSeance', '')
    idParticipant = request.form.get('idParticipant', '')
    date_Inscription = request.form.get('date_Inscription', '')
    prix_inscription = request.form.get('prix_inscription', '')
    mycursor = get_db().cursor()
    sql = ''' INSERT INTO Inscription(id_inscription, idSeance, idParticipant, date_Inscription, prix_inscription) 
              VALUES (NULL, %s, %s, %s, %s);'''
    tuple_sql = (idSeance, idParticipant, date_Inscription, prix_inscription)
    mycursor.execute(sql, tuple_sql)

    get_db().commit()
    message = f'Inscription ajoutée - Séance : {idSeance}, Participant : {idParticipant}, Date : {date_Inscription}, Prix : {prix_inscription}'
    flash(message, 'alert-success')
    return redirect('/inscription/show')


@app.route('/inscription/edit', methods=['GET'])
def edit_inscription():
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_inscription, idSeance, idParticipant, date_Inscription, prix_inscription 
             FROM Inscription 
             WHERE id_inscription = %s'''
    mycursor.execute(sql, (id,))
    inscription = mycursor.fetchone()

    sql = '''SELECT id_Seance, DateSeance 
             FROM Seance'''
    mycursor.execute(sql)
    seances = mycursor.fetchall()

    sql = '''SELECT idParticipant, Nom_Participant 
             FROM Participant'''
    mycursor.execute(sql)
    participants = mycursor.fetchall()

    return render_template('Inscription/edit_inscription.html', inscription=inscription, seances=seances,
                           participants=participants)


@app.route('/inscription/edit', methods=['POST'])
def valid_edit_inscription():
    idSeance = request.form.get('idSeance', '')
    idParticipant = request.form.get('idParticipant', '')
    date_Inscription = request.form.get('date_Inscription', '')
    prix_inscription = request.form.get('prix_inscription', '')
    id_inscription = request.form.get('id_inscription', '')

    mycursor = get_db().cursor()
    sql = '''UPDATE Inscription 
             SET idSeance = %s, idParticipant = %s, date_Inscription = %s, prix_inscription = %s 
             WHERE id_inscription = %s'''
    tuple_sql = (idSeance, idParticipant, date_Inscription, prix_inscription, id_inscription)
    mycursor.execute(sql, tuple_sql)
    get_db().commit()
    message = f'Inscription modifiée - Séance : {idSeance}, Participant : {idParticipant}, Date : {date_Inscription}, Prix : {prix_inscription}'
    flash(message, 'alert-success')
    return redirect('/inscription/show')
