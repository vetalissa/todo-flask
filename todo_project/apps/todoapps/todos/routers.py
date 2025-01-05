from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from apps.app import db
from .models import Todo

todos = Blueprint('todos', __name__, template_folder='templates')


@todos.route('/view-todo')
@login_required
def view_todo():
    user_id = current_user.id
    todo_list = Todo.query.filter(Todo.user_id == user_id, Todo.done == False).all()

    return render_template('todos/list_todo.html', todo_list=todo_list)


@todos.route('/completed')
@login_required
def completed():
    user_id = current_user.id
    todo_list = Todo.query.filter(Todo.user_id == user_id, Todo.done == True).all()

    return render_template('todos/completed.html', todo_list=todo_list)


@todos.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            user_id = current_user.id
            title = request.form.get('title')
            description = request.form.get('description')
            important = True if 'important' in request.form.keys() else False

            description = description if description else ''

            todo = Todo(title=title, description=description, important=important, done=False, user_id=user_id)

            db.session.add(todo)
            db.session.commit()
            flash('Задача добавлена!', category='success')
        except Exception:
            flash('Извините, произошла ошибка. Пробуйте снова.', category='error')

    return render_template('todos/create.html')


@todos.route('/update/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def update(todo_id):
    user_id = current_user.id
    todo = Todo.query.filter(Todo.id == todo_id, Todo.user_id == user_id).first()

    if request.method == 'GET':
        return render_template('todos/update.html', todo=todo)
    elif request.method == 'POST':
        try:
            title = request.form.get('title')
            description = request.form.get('description')
            important = True if 'important' in request.form.keys() else False

            todo.title = title
            todo.description = description
            todo.important = important

            db.session.commit()

            flash('Задача обновлена', category='success')
            return redirect(url_for('todos.view_todo'))
        except Exception:
            flash('Извините, произошла ошибка. Пробуйте снова.', category='error')


@todos.route('/done/<int:todo_id>/<string:redirect_to>')
@login_required
def done(todo_id, redirect_to):
    try:
        user_id = current_user.id
        todo = Todo.query.filter(Todo.id == todo_id and Todo.user_id == user_id).first()
        if todo.done is True:
            todo.done = False
        else:
            todo.done = True

        db.session.commit()
    except Exception:
        flash('Извините, произошла ошибка. Пробуйте снова.', category='error')

    if redirect_to == 'view_todo':
        return redirect(url_for('todos.view_todo'))
    elif redirect_to == 'completed':
        return redirect(url_for('todos.completed'))


@todos.route('/delete/<int:todo_id>/<string:redirect_to>')
@login_required
def delete(todo_id, redirect_to):
    try:
        user_id = current_user.id
        Todo.query.filter(Todo.id == todo_id and Todo.user_id == user_id).delete()

        db.session.commit()
        flash('Задача удалена!', category='success')
    except Exception:
        flash('Извините, произошла ошибка. Пробуйте снова.', category='error')

    if redirect_to == 'view_todo':
        return redirect(url_for('todos.view_todo'))
    elif redirect_to == 'completed':
        return redirect(url_for('todos.completed'))
