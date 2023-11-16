from flask import Flask, request, make_response

app = Flask(__name__)

menu = [
    {'title': 'Main Page', 'url': '/'},
    {'title': 'Add post', 'url': '/add_post'}
]


@app.route('/')
def index():
    return '<h1>Main page</h1>'


@app.route('/login')
def login():
    log = ''
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')

    response = make_response(f'<h2>Authorization</h2> <p> logged: {log}')
    response.set_cookie('logged', 'yes')
    return response


if __name__ == '__main__':
    app.run(debug=True)
