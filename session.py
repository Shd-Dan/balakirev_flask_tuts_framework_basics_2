from flask import session, Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "c11246086ce2f924c56bbddacf7de2fdb27789f0"


@app.route('/login')
def index():
    # Считает количество посещений
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1

    return f"<h1>Main page</h1><p>Number views: {session['visits']}"


data = [1, 2, 3, 4]


@app.route('/session')
# Acceptance of modification in session. Flask allows session object editing by .modified method.
def session_data():
    # Session save is on, even if client is closed
    session.permanent = True
    # Checking for data in session
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        #  Acceptance of modification
        session.modified = True

    return f'<p>Session data: {session["data"]}'


if __name__ == "__main__":
    app.run(debug=True)
