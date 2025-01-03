from flask import render_template, Blueprint

todos = Blueprint('todos', __name__, template_folder='templates')


@todos.route('/view-todo')
def view_todo():
    return render_template('todos/list_todo.html')

@todos.route('/completed')
def completed():
    return render_template('todos/completed.html')


@todos.route('/create')
def create():
    return render_template('todos/create.html')
