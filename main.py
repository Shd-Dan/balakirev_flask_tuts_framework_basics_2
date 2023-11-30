import os
import sqlite3
from flask import Flask, render_template, request, flash, session, abort, g, url_for, redirect, make_response
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm

'''Dictionary below in beginning used as DB of urls and names for pages'''
# menu = [{'title': 'Home', 'url': '/'},
#         {'title': 'About', 'url': 'about'},
#         {'title': 'Post', 'url': 'post'},
#         {'title': 'Contact', 'url': 'contact'}
#         ]

'''Data-base configuration'''
DATABASE = '/tmp/main_base.db'
DEBUG = True
# SECRET_KEY = 'qrf7wrwer8v22wer2v3ewrv3'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisis11asecretkey000'
app.config.from_object(__name__)

# root_path if there are several apps called
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'main_base.db')))

login_manager = LoginManager(app)
# Redirection handler if user is not logged in but visits page where required to be logged in.
login_manager.login_view = 'login'


# Decorator creates user data fetch instance, arguments are integer as User_id and object of FDataBase class
@login_manager.user_loader
def load_user(user_id):
    print("Load_user")
    return UserLogin().from_data_base(user_id, data_base)


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


# Перехватчик запроса
data_base = None


@app.before_request
def before_request():
    global data_base
    db = get_db()
    data_base = FDataBase(db)


# Closing connection with database
@app.teardown_appcontext
def close_bd(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
@app.route('/index.html')
def index():
    # Below, previously we used a dict variable as DB for 'menu', now arguments are taken form data-base (FDataBase)
    return render_template('index.html', menu=data_base.getMenu(), posts=data_base.getPostsAnnounce(),
                           title='Framework for web-development')


@app.route('/about')
def about():
    return render_template('about.html', menu=data_base.getMenu())


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['name']) > 2:
            flash('Form submission successful! Yahooo', category='success')
        else:
            flash('Error sending message! Idiot!', category='error')

    return render_template('contact.html', menu=data_base.getMenu(), title='Contact the internet')


@app.route("/post", methods=['POST', 'GET'])
def addPost():
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            result = data_base.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not result:
                flash("Post adding error", category='error')
            else:
                flash("Post added successfully!", category='success')
        else:
            flash("Post adding error", category='error')

    return render_template('post.html', menu=data_base.getMenu(), title='Post')


# Get posts from DB by ID, # id was changed to url
@app.route("/post/<alias>")
# Limits access to posts
@login_required
def showPost(alias):
    # db = get_db()
    # data_base = FDataBase(db)
    title, post = data_base.getPost(alias)
    if not title:
        abort(404)

    return render_template('post_id.html', menu=data_base.getMenu(), title=title, post=post)


# Profile set up
# @app.route('/profile/<username>')
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(404)
#
#     return f'Profile of {username}'


# Route redirection
@app.route('/login', methods=['POST', 'GET'])
def login():
    # if 'userLogged' in session:
    #     return redirect(url_for('profile', username=session['userLogged']))
    # elif request.method == 'POST' and request.form['username'] == 'shd' and request.form['password'] == '223':
    #     session['userLogged'] = request.form['username']
    #     return redirect(url_for('profile', username=session['userLogged']))

    # If user is already logged in then in redirects to profile page
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    """WTForms are used for filling HTML attributes"""
    form = LoginForm()
    if form.validate_on_submit():
        user = data_base.get_user_by_email(form.email.data)
        if user and check_password_hash(user['psw'], form.password.data):
            user_login = UserLogin().create(user)
            remember_me = form.remember.data
            login_user(user_login, remember=remember_me)
            # Redirects to page where authorization where asked, after logging it user backs to this page
            # in html action must be empty
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Login or email are not correct", "error")

    return render_template('login.html', menu=data_base.getMenu(), title='Login', form=form)

    """Login request handling conditions: user data fetched from database"""
    # db = get_db()
    # data_bas = FDataBase(db)
    # if request.method == "POST":
    #     user = data_bas.get_user_by_email(request.form['email'])
    #     if user and check_password_hash(user['psw'], request.form['password']):
    #         user_login = UserLogin().create(user)
    #         remember_me = True if request.form.get('remember') else False
    #         login_user(user_login, remember=remember_me)
    #         # Redirects to page where authorization where asked, after logging it user backs to this page
    #         # in html action must be empty
    #         return redirect(request.args.get("next") or url_for("profile"))
    #
    #     flash("Login or email are not correct", "error")
    #
    # return render_template('login.html', menu=data_base.getMenu(), title='Login')


# Sign-up page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if (len(request.form['username']) > 4 and len(request.form['email']) > 4 and
                len(request.form['password']) > 4 and len(request.form['password'])
                == len(request.form['password-repeat'])):
            hashed = generate_password_hash(request.form['password'])
            res = data_base.add_user(request.form['username'], request.form['email'], hashed)
            if res:
                flash("Authorization successful", "success")
                return redirect(url_for('login'))
            else:
                flash("Such user is already registered", "error")
        else:
            flash("Please fill in correctly", "error")

    return render_template('signup.html', menu=data_base.getMenu(), title='Authorization')


# Error handling for wrong url address
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found'), 404


# logout_user() is used from flask_login
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You signed out', 'success')
    return redirect(url_for('login'))


# Profile handler, get_id() is used from flask_login
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", menu=data_base.getMenu(), title="Profile")
    # return 'this is a profile'


@app.route("/userava")
@login_required
def userava():
    img = current_user.get_avatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':  # check if data from DB is returned by POST
        file = request.files['file']  # corresponds to the name attribute of the file input field in the HTML form.
        if file and current_user.verify_ext(
                file.filename):  # function 'verify_extension' checks is file in PNG format. UserLogin
            try:
                img = file.read()  # image is read
                result = data_base.update_user_avatar(img, current_user.get_id())  # loads avatar image to database. FDataBase
                if not result:
                    flash('Avatar update error', 'error')
                flash('Avatar updated', 'success')
            except FileNotFoundError as e:
                flash("File reading error", 'error')
        else:
            flash('Avatar update error', 'error')

    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(debug=True)
