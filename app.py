from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.environ.get('DATABASE', 'todo.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        db.commit()

@app.route('/')
def index():
    db = get_db()
    tasks = db.execute('SELECT id, task, done FROM todos').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_content = request.form['task']
    if task_content.strip():
        db = get_db()
        db.execute('INSERT INTO todos (task, done) VALUES (?, ?)', 
                  [task_content, False])
        db.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:id>')
def done(id):
    db = get_db()
    task = db.execute('SELECT done FROM todos WHERE id = ?', [id]).fetchone()
    new_status = not task['done']
    db.execute('UPDATE todos SET done = ? WHERE id = ?', [new_status, id])
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ?', [id])
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db_dir = os.path.dirname(DATABASE)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
