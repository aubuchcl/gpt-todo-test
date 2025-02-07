from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(deleted=False).all()
    return jsonify([{"id": task.id, "title": task.title, "complete": task.complete} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400
    if len(title) > 200:
        return jsonify({"error": "Title is too long"}), 400
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title, "complete": new_task.complete}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.deleted:
        return jsonify({"error": "Task not found"}), 404
    task.complete = not task.complete
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "complete": task.complete})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.deleted:
        return jsonify({"error": "Task not found"}), 404
    task.deleted = True
    db.session.commit()
    return jsonify({"message": "Task marked as deleted"})

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Error occurred: {str(e)}")
    return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    if not os.path.exists('todo.db'):
        with app.app_context():
            db.create_all()

    # Force Flask to use the generated self-signed cert
    app.run(host='::', port=5000, ssl_context=('/app/cert.pem', '/app/key.pem'))

