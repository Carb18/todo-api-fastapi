import sqlite3

DB_NAME = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)",
            [("Buy groceries", "Eggs, bread, Milk", 0),
             ("Read a book", "Finish chapter 4", 0),
             ("Walk the dog", "Evening walk around the block", 0)]
        )

    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_task_by_id(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_task(title: str, description: str, done: bool = False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)",
        (title, description, done)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_task_by_id(new_id)

def update_task(task_id: int, title: str= None , description: str = None, done: bool = None):
    existing = get_task_by_id(task_id)
    if existing is None:
        return None

    new_title = title if title is not None else existing["title"]
    new_description = description if description is not None else existing["description"]
    new_done = done if done is not None else existing["done"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, done = ? WHERE id = ?",
        (new_title, new_description, new_done, task_id)
    )
    conn.commit()
    conn.close()
    return get_task_by_id(task_id)


def delete_task(task_id: int):
    existing = get_task_by_id(task_id)
    if existing is None:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return True

