import sqlite3
from pydoc import render_doc
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    like = db.Column(db.Boolean, unique=False, default=False)

    def __rep__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'

    else:
        tasks = Todo.query.all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task)

@app.route('/like/<int:id>')
def like(id):
    task_to_like = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_like)
        task_to_like.like = True
        db.session.add(task_to_like)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while liking that task'

@app.route('/unlike/<int:id>')
def unlike(id):
    task_to_unlike = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_unlike)
        task_to_unlike.like = False
        db.session.add(task_to_unlike)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while unliking that task'