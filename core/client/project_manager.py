from database.db import connect, init_db

SERVICE_OWNERS = {
    "seo": "seo", "website": "web-cro", "web": "web-cro",
    "social": "social-media", "content": "content", "digital marketing": "marketing",
}


def create_project(client_id: int, services: list[str]):
    init_db()
    with connect() as con:
        client = con.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
        if client is None:
            raise ValueError(f"Client {client_id} not found")
        if client["payment_status"] != "paid" or client["onboarding_status"] != "completed":
            raise PermissionError("Project creation requires paid client and completed onboarding")
        created, previous = [], None
        for service in services:
            name = service.strip()
            if not name:
                continue
            owner = SERVICE_OWNERS.get(name.lower(), "delivery-manager")
            cur = con.execute(
                "INSERT INTO tasks(title, owner, status, priority, depends_on, client_id) VALUES (?, ?, 'pending', 'normal', ?, ?)",
                (f"Deliver {name}", owner, previous, client_id),
            )
            previous = cur.lastrowid
            created.append(cur.lastrowid)
        if not created:
            raise ValueError("At least one service is required")
        cur = con.execute(
            "INSERT INTO tasks(title, owner, status, priority, depends_on, client_id) VALUES (?, 'qa', 'pending', 'high', ?, ?)",
            ("Final quality assurance", previous, client_id),
        )
        created.append(cur.lastrowid)
    return {"client_id": client_id, "task_ids": created}


def project_tasks(client_id: int):
    init_db()
    with connect() as con:
        client = con.execute("SELECT id FROM clients WHERE id=?", (client_id,)).fetchone()
        if not client:
            raise ValueError(f"Client {client_id} not found")
        rows = con.execute("SELECT * FROM tasks WHERE client_id=? ORDER BY id", (client_id,)).fetchall()
    return [dict(row) for row in rows]
