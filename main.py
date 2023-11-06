from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g
import sqlite3
import os

menu = [{'name': 'Home', 'url': '/'},
        {'name': 'About', 'url': 'about'},
        {'name': 'Post', 'url': 'post'},
        {'name': 'Contact', 'url': 'contact'}
        ]
# Data Base configuration
DATABASE = '/tmp/main_base.db'
DEBUG = True
# SECRET_KEY = 'qrf7wrwer8v22wer2v3ewrv3'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisis11asecretkey000'
app.config.from_object(__name__)

# root_path if there are several apps called
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main_base.db')))


# function making connection with DB
def connect_db():
    connection_db = sqlite3.connect(app.config['DATABASE'])
    connection_db.row_factory = sqlite3.Row
    return connection_db


# function that creates DB without webserver launching
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# This is a third step after creating DB and configuring basic connection
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    db = get_db()
    return render_template('index.html', menu=menu, title='Framework for web-development')


@app.route('/about')
def about():
    return render_template('about.html', menu=menu)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['name']) > 2:
            flash('Form submission successful! Yahooo', category='success')
        else:
            flash('Error sending message! Idiot!', category='error')

    return render_template('contact.html', menu=menu, title='Contact the internet')


# Profile set up
@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(404)

    return f'Profile of {username}'


# Route redirection
@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'shd' and request.form['password'] == '223':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Login', menu=menu)


# Error handling for wrong url address
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found', menu=menu), 404


# Closing connection with database
@app.teardown_appcontext
def close_bd(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)
