import sqlite3

class TaskDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('tasks.db')
        self.cursor = self.connection.cursor()

        # Create the tasks table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                priority TEXT,
                due_date TEXT,
                status TEXT,
                done TEXT
            )
        ''')
        self.connection.commit()

    def add_task(self, task_name, priority, due_date, status, done):
        # Insert a new task into the tasks table
        self.cursor.execute('''
            INSERT INTO tasks (task_name, priority, due_date, status, done)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_name, priority, due_date, status, done))
        self.connection.commit()

    def get_all_tasks(self):
        # Retrieve all tasks from the tasks table
        self.cursor.execute('SELECT * FROM tasks')
        return self.cursor.fetchall()

    def delete_task(self, task_id):
        # Delete a task from the tasks table by ID
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.connection.commit()

    def clear_tasks(self):
        # Delete all tasks from the tasks table
        self.cursor.execute('DELETE FROM tasks')
        self.connection.commit()

    def search_tasks(self, search_term):
        # Search for tasks that match the given search term
        self.cursor.execute('''
            SELECT * FROM tasks
            WHERE task_name LIKE ? OR priority LIKE ? OR due_date LIKE ? OR status LIKE ? OR done LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        return self.cursor.fetchall()

    def __del__(self):
        # Close the database connection when the object is deleted
        self.connection.close()
