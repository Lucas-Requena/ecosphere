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