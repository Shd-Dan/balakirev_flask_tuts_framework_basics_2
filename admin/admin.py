from flask import Blueprint, render_template, request, url_for, redirect, flash, session

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')


def login_admin():
    session['admin_logged'] = 1


def is_logged():
    return True if session.get("admin_logged") else False


def admin_logout():
    session.pop("admin_logged", None)


menu = [{'url': '.index', 'title': 'Panel'},
        {'url': '.logout', 'title': 'Sign-out'}]


@admin.route('/')
def index():
    if not is_logged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Admin panle')


@admin.route("/login", methods=['POST', 'GET'])
def login():
    if is_logged():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['user'] == 'admin' and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Wrong login or password", "error")

    return render_template("admin/login.html", title="Admin panel")


@admin.route("/logout", methods=['POST', 'GET'])
def logout():
    if not is_logged():
        return redirect(url_for('.login'))

    admin_logout()

    return redirect(url_for('.login'))
