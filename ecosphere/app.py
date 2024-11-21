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
        g.db =  pymysql.connect(
            host="serveurmysql",                 # à modifier
            user="lrequena",                     # à modifier
            password="mdp",                # à modifier
            database="BDD_lrequena",        # à modifier
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
    return render_template('layout.html',methods=['GET'])

@app.route('/evaluation/show', methods=['GET'])
def show_evaluation():
    #print(types_articles)
    mycursor = get_db().cursor()
    sql = '''   SELECT id_evaluation AS id,Animateur.Nom_Animateur,Seance.DateSeance,Participant.Nom_Participant,Note_Seance,Note_Animation
    FROM Evaluation
    INNER JOIN Animateur ON Evaluation.N_Animateur = Animateur.N_Animateur
    INNER JOIN Seance ON Evaluation.idSeance = Seance.id_Seance
    INNER JOIN Participant ON Evaluation.idParticipant = Participant.idParticipant
    ORDER BY id_evaluation; '''
    mycursor.execute(sql)
    evaluations = mycursor.fetchall()
    return render_template('Evaluation/show_evaluation.html', evaluation=evaluations)