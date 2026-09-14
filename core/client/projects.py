from database.db import connect, init_db


def list_client_tasks(client_id: int):
    init_db()
    with connect() as con:
        client = con.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
        if not client:
            raise ValueError(f"Client {client_id} not found")
        # Tasks are currently linked through the client's workflow execution context.
        rows = con.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


def update_task_status(task_id: int, status: str):
    allowed = {"pending", "in_progress", "completed", "failed", "cancelled"}
    if status not in allowed:
        raise ValueError(f"Invalid status: {status}")
    init_db()
    with connect() as con:
        cur = con.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        if cur.rowcount == 0:
            raise ValueError(f"Task {task_id} not found")
    return {"task_id": task_id, "status": status}
