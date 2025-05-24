from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    priority = db.Column(db.String(20), default='Medium')
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tasks_completed = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    high_priority_completed = db.Column(db.Integer, default=0)
    medium_priority_completed = db.Column(db.Integer, default=0)
    low_priority_completed = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()
    # Initialize performance record if it doesn't exist
    if not Performance.query.first():
        initial_performance = Performance()
        db.session.add(initial_performance)
        db.session.commit()

@app.route('/')
def index():
    tasks = Task.query.all()
    performance = Performance.query.first()
    return render_template('index.html', tasks=tasks, performance=performance)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    due_date_str = request.form.get('due_date')
    
    due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M') if due_date_str else None
    
    task = Task(title=title, description=description, priority=priority, due_date=due_date)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.priority = request.form.get('priority')
    due_date_str = request.form.get('due_date')
    task.due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M') if due_date_str else None
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete_task/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.completed:
        return redirect(url_for('index'))
        
    task.completed = True
    
    # Update performance metrics
    performance = Performance.query.first()
    performance.tasks_completed += 1
    
    # Update priority-specific counters
    if task.priority == 'High':
        performance.high_priority_completed += 1
    elif task.priority == 'Medium':
        performance.medium_priority_completed += 1
    else:
        performance.low_priority_completed += 1
    
    performance.score = calculate_performance_score(performance)
    
    db.session.commit()
    return redirect(url_for('index'))

def calculate_performance_score(performance):
    # Simple score based on priority weights
    score = (
        performance.high_priority_completed * 30 +
        performance.medium_priority_completed * 20 +
        performance.low_priority_completed * 10
    )
    
    return score

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
