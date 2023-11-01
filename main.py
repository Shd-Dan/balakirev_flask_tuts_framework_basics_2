from flask import Flask, render_template, request

menu = [{'name': 'Home', 'url': '/'},
        {'name': 'About', 'url': 'about'},
        {'name': 'Post', 'url': 'post'},
        {'name': 'Contact', 'url': 'contact'}
        ]

app = Flask(__name__)


# menu = ['Home', 'About', 'Sample Post', 'Contact']


@app.route('/')
def index():
    return render_template('index.html', menu=menu, title='Framework for web-development')


@app.route('/about')
def about():
    return render_template('about.html', menu=menu)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
    return render_template('contact.html', menu=menu, title='Contact the internet')


if __name__ == '__main__':
    app.run(debug=True)
