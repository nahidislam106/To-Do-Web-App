from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        if not task_content.strip():
            flash('Task cannot be empty!', 'error')
            return redirect(url_for('index'))
            
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect('/')
        except:
            flash('There was an issue adding your task', 'error')
            return redirect('/')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
        return redirect('/')
    except:
        flash('There was a problem deleting that task', 'error')
        return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect('/')
        except:
            flash('There was an issue updating your task', 'error')
            return redirect('/')
    else:
        return render_template('update.html', task=task)

@app.route('/toggle/<int:id>')
def toggle_complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        status = 'completed' if task.completed else 'marked incomplete'
        flash(f'Task {status}!', 'success')
        return redirect('/')
    except:
        flash('There was a problem updating the task status', 'error')
        return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)