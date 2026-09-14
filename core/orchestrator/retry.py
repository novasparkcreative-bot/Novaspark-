from database.db import connect, init_db


def retry_task(task_id: int, max_attempts: int = 3):
    init_db()
    with connect() as con:
        row = con.execute("SELECT output FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not row:
            raise ValueError(f"Task {task_id} not found")
        attempts = int((row["output"] or "").count("[attempt:")) + 1
        if attempts > max_attempts:
            return {"task_id": task_id, "status": "retry_limit_reached", "attempts": attempts - 1}
        con.execute(
            "UPDATE tasks SET status='pending', output=? WHERE id=?",
            (f"[attempt:{attempts}] retry scheduled", task_id),
        )
        return {"task_id": task_id, "status": "pending", "attempts": attempts}
