from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hakunamatata'


# db=SQLAlchemy(app)
# login_manager=LoginManager()
# login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/skills')
def skills():
    return render_template('skills.html')


if __name__ == '__main__':
    app.run(debug=True)
