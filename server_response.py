from flask import Flask, make_response, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['SECRET KEY'] = 'c11246086ce2f924c56bbddacf7de2fdb27789f0'

menu = [{"title": "Main page", "url": "/"},
        {"title": "Add post", "url": "/add_post"}]


@app.route('/')
def index():
    # (response, status)
    # server_response = make_response('<h1> Server error </h1>', 500)
    # return server_response
    return '<h1> Main Page </h1>', 200, {'Content-type': 'text/plain'}


@app.errorhandler(404)
def page_not_found(error):
    return ('Fuck you!!!', 404)


@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)


""" ---------------------------------- Cookies ---------------------------------- """


@app.route('/login')
def login():
    log = ""
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    response = make_response(f'<h1>Authorization form</h1><p>logged: {log}')
    response.set_cookie('logged', 'yes')
    return response


@app.route("/logout")
def logout():
    response = make_response("<p> Not authorizes </p>")
    response.set_cookie("logged", "", 0)

    return response


if __name__ == '__main__':
    app.run(debug=True)
