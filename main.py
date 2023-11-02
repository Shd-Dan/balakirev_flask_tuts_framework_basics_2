from flask import Flask, render_template, request, flash

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


# Error handling for wrong url address
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found', menu=menu), 404


if __name__ == '__main__':
    app.run(debug=True)
