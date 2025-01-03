from flask import Blueprint, render_template
from flask_login import login_required

todos = Blueprint('todos', __name__, template_folder='templates')


@todos.route('/view-todo')
@login_required
def view_todo():
    return render_template('todos/list_todo.html')


@todos.route('/completed')
@login_required
def completed():
    return render_template('todos/completed.html')


@todos.route('/create')
@login_required
def create():
    return render_template('todos/create.html')
