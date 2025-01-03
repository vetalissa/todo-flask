from flask import render_template, Blueprint

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/login')
def login():
    return render_template('users/login.html')


@users.route('/register')
def register():
    return render_template('users/registration.html')
