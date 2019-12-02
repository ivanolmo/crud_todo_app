from flask import Flask, render_template, request, jsonify, redirect,\
    url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' \
                                        'postgres:asdf@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(128), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<ToDo {self.id} - {self.item}>'


# Migrate will now create tables
# db.create_all()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())


@app.route('/todo/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        new_item = request.get_json()['todo-item']
        todo = Todo(item=new_item, completed=False)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['item'] = todo.item
        body['completed'] = todo.completed
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


@app.route('/todo/<todo_id>/set-completed', methods=['POST'])
def check_completed(todo_id):
    try:
        new_completion = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = new_completion
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todo/<todo_id>/delete-todo', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run()
