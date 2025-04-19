import unittest
import json
from app import app, init_db
import sqlite3

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the database before the tests run
        init_db()

    def setUp(self):
        # Set up a clean database for each test
        self.conn = sqlite3.connect('data.db')
        self.conn.execute('DELETE FROM tasks')  # Clear tasks table
        self.conn.commit()
        self.conn.close()

        # Create a test client
        self.client = app.test_client()

    def test_get_tasks_empty(self):
        # Test GET /tasks when there are no tasks
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_add_task(self):
        # Test POST /tasks to add a new task
        task_data = {'name': 'Test Task'}
        response = self.client.post('/tasks', json=task_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'message': 'Task added'})

    def test_get_tasks_after_post(self):
        # Test GET /tasks after adding a task
        task_data = {'name': 'Test Task'}
        self.client.post('/tasks', json=task_data)

        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        tasks = json.loads(response.data)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['name'], 'Test Task')

if __name__ == '__main__':
    unittest.main()
