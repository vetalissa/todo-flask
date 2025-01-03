from flask import Blueprint, render_template


def create_user_blueprint(bcrypt):
    users = Blueprint('users', __name__, template_folder='templates')

    @users.route('/login')
    def login():
        return render_template('users/login.html')

    @users.route('/register')
    def register():
        return render_template('users/registration.html')

    return users
