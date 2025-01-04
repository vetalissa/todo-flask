from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from apps.app import db
from .models import Todo

todos = Blueprint('todos', __name__, template_folder='templates')


@todos.route('/view-todo')
@login_required
def view_todo():
    user_id = current_user.id
    todo_list = Todo.query.filter(Todo.user_id == user_id and Todo.done == False).all()

    return render_template('todos/list_todo.html', todo_list=todo_list)


@todos.route('/completed')
@login_required
def completed():
    user_id = current_user.id
    todo_list = Todo.query.filter(Todo.user_id == user_id and Todo.done == True).all()

    return render_template('todos/completed.html', todo_list=todo_list)


@todos.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            print(request.form.keys())
            print(request.form)
            user_id = current_user.id
            title = request.form.get('title')
            description = request.form.get('description')
            important = True if 'important' in request.form.keys() else False

            description = description if description else ''

            todo = Todo(title=title, description=description, important=important, done=False, user_id=user_id)

            db.session.add(todo)
            db.session.commit()
            flash('Задача добавлена!', category='success')
        except Exception as e:
            flash(f'Извините, произошла ошибка. Пробуйте снова. {e}', category='error')

    return render_template('todos/create.html')
