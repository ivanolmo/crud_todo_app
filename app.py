from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' \
                                        'postgres:asdf@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<ToDo {self.id} - {self.item}>'


db.create_all()


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


@app.route('/todo/create', methods=['POST'])
def create_todo():
    new_item = request.get_json()['todo-item']
    todo = Todo(item=new_item)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'todo-item': todo.item
    })


if __name__ == '__main__':
    app.run()
