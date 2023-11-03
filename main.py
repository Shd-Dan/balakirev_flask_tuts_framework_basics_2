from flask import Flask, render_template, request, flash, session, redirect, url_for, abort

menu = [{'name': 'Home', 'url': '/'},
        {'name': 'About', 'url': 'about'},
        {'name': 'Post', 'url': 'post'},
        {'name': 'Contact', 'url': 'contact'}
        ]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisis11asecretkey000'


@app.route('/')
def index():
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


if __name__ == '__main__':
    app.run(debug=True)
