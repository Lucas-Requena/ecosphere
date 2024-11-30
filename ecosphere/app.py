#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash, session, g
import pymysql.cursors

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="shamitou",
            password="Ceryne2006",
            database="but",
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

@app.route('/inscription/show', methods=['GET'])
def show_inscriptions():
    mycursor = get_db().cursor()
    sql = "SELECT id, nom, email, date_inscription FROM Inscription ORDER BY id;"
    mycursor.execute(sql)
    inscriptions = mycursor.fetchall()
    return render_template('Inscription/show_inscriptions.html', inscriptions=inscriptions)

@app.route('/inscription/add', methods=['GET'])
def add_inscription():
    return render_template('Inscription/add_inscription.html')

@app.route('/inscription/add', methods=['POST'])
def valid_add_inscription():
    nom = request.form.get('nom', '')
    email = request.form.get('email', '')
    date_inscription = request.form.get('date_inscription', '')

    mycursor = get_db().cursor()
    sql = "INSERT INTO Inscription (nom, email, date_inscription) VALUES (%s, %s, %s);"
    tuple_sql = (nom, email, date_inscription)
    mycursor.execute(sql, tuple_sql)
    get_db().commit()

    message = f"Inscription ajoutée: Nom = {nom}, Email = {email}, Date d'inscription = {date_inscription}"
    flash(message, 'alert-success')
    return redirect('/inscription/show')

@app.route('/inscription/delete', methods=['GET'])
def delete_inscription():
    id = request.args.get('id')

    mycursor = get_db().cursor()
    sql = "DELETE FROM Inscription WHERE id=%s;"
    tuple_sql = (id,)
    mycursor.execute(sql, tuple_sql)
    get_db().commit()

    message = f"Inscription supprimée, id: {id}"
    flash(message, 'alert-warning')
    return redirect('/inscription/show')

if __name__ == "__main__":
    app.run(debug=True)
