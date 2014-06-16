#coding:utf8

"""
One simple test for flask

2014/06/16 by varwey 
"""

from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash
from config import *

#DATABASE = '/tmp/flaskr.db'
#DEBUG = True
#SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASK_SETTINGS', silent=True)

def connect_db():
    #print app.config
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text, datetime from entries order by id desc')
    entries = [dict(title=row[0], text=row[1], datatime=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text, datetime) value (?, ?)',
                 [request.form['title'],
                  request.form['text'],
                   request.form['datetime']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME']:
            if request.form['password'] == app.config['PASSWORD']:
                session['logged_in'] = True
                flash('logged_in successfully !!!')
                return redirect(url_for('show_entries'))
            else:
                error = 'Invalid password'
        else:
            error = 'Invalid username'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You already logged out !!!')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
