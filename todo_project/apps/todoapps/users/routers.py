from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from apps.app import bcrypt, db
from .models import User

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(User.username == username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('todos.view_todo'))
            else:
                flash('Неверные данные', category='error')
        else:
            flash('Пользователя не существует.', category='error')
        return render_template('users/login.html')


@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('users/registration.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        if User.query.filter(User.username == username).one_or_none() is None:
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            if password1 == password2:
                try:
                    hashed_password = bcrypt.generate_password_hash(password1)

                    user = User(username=username, password=hashed_password)

                    db.session.add(user)
                    db.session.commit()

                    flash('Вы успешно зарегистрированы!', category='success')
                    return redirect(url_for('users.login'))
                except:
                    flash('Извините, произошла ошибка. Пробуйте снова.', category='error')
            else:
                flash('Пароли не совпадают, попробуйте еще раз.', category='error')

        else:
            flash('Имя уже занято, попробуйте другое...', category='error')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))
