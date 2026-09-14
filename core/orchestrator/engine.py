from database.db import connect, init_db


class Orchestrator:
    """Small dependency-aware local task executor."""

    def add_task(self, title, owner, priority="normal", depends_on=None):
        init_db()
        with connect() as con:
            cur = con.execute(
                "INSERT INTO tasks(title, owner, status, priority, depends_on) VALUES (?, ?, 'pending', ?, ?)",
                (title, owner, priority, depends_on),
            )
            return cur.lastrowid

    def ready_tasks(self):
        init_db()
        with connect() as con:
            rows = con.execute(
                "SELECT * FROM tasks WHERE status='pending' ORDER BY CASE priority WHEN 'high' THEN 0 ELSE 1 END, id"
            ).fetchall()
            ready = []
            for row in rows:
                dep = row['depends_on']
                if dep is None:
                    ready.append(dict(row)); continue
                dep_row = con.execute("SELECT status FROM tasks WHERE id=?", (dep,)).fetchone()
                if dep_row and dep_row['status'] == 'completed':
                    ready.append(dict(row))
            return ready

    def start(self, task_id):
        init_db()
        with connect() as con:
            row = con.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
            if not row:
                raise ValueError(f"Task {task_id} not found")
            if row['depends_on'] is not None:
                dep = con.execute("SELECT status FROM tasks WHERE id=?", (row['depends_on'],)).fetchone()
                if not dep or dep['status'] != 'completed':
                    raise RuntimeError("Task dependency is not completed")
            con.execute("UPDATE tasks SET status='in_progress' WHERE id=?", (task_id,))

    def complete(self, task_id, output=""):
        init_db()
        with connect() as con:
            con.execute("UPDATE tasks SET status='completed', output=? WHERE id=?", (output, task_id))

    def fail(self, task_id, output=""):
        init_db()
        with connect() as con:
            con.execute("UPDATE tasks SET status='failed', output=? WHERE id=?", (output, task_id))
