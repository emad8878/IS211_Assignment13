#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db(): 
    return sqlite3.connect(app.config['DATABASE'])

def init_db(): 
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

connect_db()
init_db()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'hw13.db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect(url_for('login'))  

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Username invalid'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('show_tests'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('show_quiz'))

@app.route('/dashboard') 
def show_quiz():
    curStudents = g.db.execute('select ID, firstName, lastName from Students')
    students = [
        dict(
            firstName=row[1],lastName=row[2]
            ) for row in curStudents.fetchall()
        ]
    curQuiz = g.db.execute('select ID, subject, question, quizDate from Quiz')
    quiz = [
        dict(
            subject=row[1],questions=row[2],quizDate=row[3]
            ) for row in cur2.fetchall()
        ]
    return render_template('show_quiz.html')

@app.route('/student/add', methods=['GET', 'POST']) 
def add_student(): 
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into Students(firstName, lastName,)\
                 ?, ?)', [request.form['title'], request.form['text']])
        g.db.commit()
        flash('A new student was added')
        return redirect(url_for('show_quiz'))
    return render_template('add_student.html')


@app.route('/student/<id>', methods = ['GET'])
def show_results(id): 
    msg = None
    cur = g.db.execute(
        'select quiz, score from Results where student=?', (id,))
    results = [dict(
        quiz = row[0], grade = row[1]) for row in cur.fetchall()]

    if not results:
        msg = 'There are no results.'
        return render_template(
            'student_results.html',results = results, msg = msg)

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz(): 
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into Quiz(subject, questions, quizDate)',
                     'values (?, ?, ?)', [request.form['subject'],
                                          request.form['questions'],
                                          request.form['quizDate']])
        g.db.commit()
        flash('A new quiz was added')
        return redirect(url_for('show_quiz'))
    return render_template('add_student.html')


if __name__ == '__main__':
    app.run()
