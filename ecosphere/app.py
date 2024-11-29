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
    sql = '''SELECT id_evaluation AS id,Animateur.Nom_Animateur,Seance.DateSeance,Participant.Nom_Participant,Note_Seance,Note_Animation
    FROM Evaluation
    INNER JOIN Animateur ON Evaluation.N_Animateur = Animateur.N_Animateur
    INNER JOIN Seance ON Evaluation.idSeance = Seance.id_Seance
    INNER JOIN Participant ON Evaluation.idParticipant = Participant.idParticipant
    ORDER BY id_evaluation;'''
    mycursor.execute(sql)
    evaluations = mycursor.fetchall()
    return render_template('Evaluation/show_evaluation.html', evaluation=evaluations)

@app.route('/animation/delete', methods=['GET'])
def delete_evaluation():
    print('''suppression d'une evaluation''')
    id = request.args.get('id')
    print("une evaluation supprimé, id :", id)
    message = u'un genre de film supprimé, id : ' + id
    flash(message, 'alert-warning')

    mycursor = get_db().cursor()
    sql = "DELETE FROM Evaluation WHERE id_evaluation=%s;"
    tuple_sql = (id)
    mycursor.execute(sql, tuple_sql)
    get_db().commit()
    return redirect('/evaluation/show')

@app.route('/animation/add', methods=['GET'])
def add_evaluation():
    mycursor = get_db().cursor()
    sql='''SELECT DISTINCT Animateur.N_Animateur, Animateur.Nom_Animateur
FROM Animateur
LEFT JOIN Evaluation ON Evaluation.N_Animateur = Animateur.N_Animateur;
'''
    mycursor.execute(sql)
    animateur = mycursor.fetchall()

    sql='''SELECT DISTINCT Seance.id_Seance, Seance.DateSeance
    FROM Seance
    LEFT JOIN Evaluation ON Seance.id_Seance = Seance.id_Seance'''
    mycursor.execute(sql)
    seance = mycursor.fetchall()

    sql = '''SELECT DISTINCT Participant.idParticipant, Participant.Nom_Participant
        FROM Participant
        LEFT JOIN Evaluation ON Participant.idParticipant = Evaluation.idParticipant'''
    mycursor.execute(sql)
    participant = mycursor.fetchall()

    return render_template('Evaluation/add_evaluation.html',animateurs=animateur,seances=seance,participants=participant)

@app.route('/animation/add', methods=['POST'])
def valid_add_evaluation():
    Nom_Animateur = request.form.get('Nom_Animateur', '')
    DateSeance = request.form.get('DateSeance', '')
    Nom_Participant = request.form.get('Nom_Participant', '')
    Note_Seance = request.form.get('Note_Seance', '')
    Note_Animation = request.form.get('Note_Animation', '')
    mycursor = get_db().cursor()
    sql = ''' INSERT INTO Evaluation(id_evaluation,N_Animateur,idSeance,idParticipant,Note_Seance,Note_Animation) VALUES (NULL, %s, %s, %s, %s, %s);'''
    tuple_sql = (Nom_Animateur,DateSeance,Nom_Participant,Note_Seance,Note_Animation)
    mycursor.execute(sql, tuple_sql)

    get_db().commit()
    message = u'evaluation ajouté , animateur :'+Nom_Animateur,"date :"+DateSeance,"participant :"+Nom_Participant,"note de seance :"+Note_Seance,"note d'animation"+Note_Animation
    flash(message, 'alert-success')
    return redirect('/evaluation/show')

@app.route('/seance/show', methods=['GET'])
def show_seance():
    mycursor = get_db().cursor()
    sql = '''SELECT id_Seance AS id,Seance.DateSeance,Seance.PlacesDisponibles,Seance.IDlieu,Seance.id_atelier
    FROM Seance'''
    mycursor.execute(sql)
    seances = mycursor.fetchall()
    return render_template('Seance/show_seance.html', seance=seances)

@app.route('/seance/add', methods=['GET'])
def add_seance():
    mycursor = get_db().cursor()
    sql='''SELECT * FROM Seance'''
    mycursor.execute(sql)
    seances = mycursor.fetchall()

    return render_template('Seance/add_seance.html',seance=seances)

@app.route('/seance/add', methods=['POST'])
def valid_add_seance():
    DateSeance = request.form.get('DateSeance', '')
    PlacesDisponibles = request.form.get('PlacesDisponibles', '')
    IDlieu = request.form.get('IDlieu', '')
    id_atelier = request.form.get('id_atelier', '')
    mycursor = get_db().cursor()
    sql = ''' INSERT INTO Seance(id_Seance,DateSeance,PlacesDisponibles,IDlieu,id_atelier) VALUES (NULL, %s, %s, %s, %s);'''
    tuple_sql = (DateSeance,PlacesDisponibles,IDlieu,id_atelier)
    mycursor.execute(sql, tuple_sql)

    get_db().commit()
    message = u'"Séance ajoutée ,'"date :"+DateSeance,"nombre de places disponibles :"+PlacesDisponibles,"ID du lieu :"+IDlieu,"ID de l'atelier"+id_atelier
    flash(message, 'alert-success')
    return redirect('/seance/show')

@app.route('/seance/delete', methods=['GET'])
def delete_seance():
    print('''suppression d'une seance''')
    id = request.args.get('id')
    print("une séance supprimée, id :", id)
    message = u'une séance supprimée, id : ' + id
    flash(message, 'alert-warning')

    mycursor = get_db().cursor()
    sql = "DELETE FROM Seance WHERE id_seance=%s;"
    tuple_sql = (id)
    mycursor.execute(sql, tuple_sql)
    get_db().commit()
    return redirect('/seance/show')
