# app.py
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT)')
    conn.close()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('data.db')
    cursor = conn.execute('SELECT * FROM tasks')
    tasks = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    conn = sqlite3.connect('data.db')
    conn.execute('INSERT INTO tasks (name) VALUES (?)', (data['name'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added'}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
