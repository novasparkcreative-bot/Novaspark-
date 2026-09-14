from database.db import connect, init_db

SERVICE_OWNERS = {
    "seo": "seo",
    "website": "web-cro",
    "web": "web-cro",
    "social": "social-media",
    "content": "content",
    "digital marketing": "marketing",
}


def create_project(client_id: int, services: list[str]):
    init_db()
    with connect() as con:
        client = con.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
        if client is None:
            raise ValueError(f"Client {client_id} not found")
        if client["payment_status"] != "paid" or client["onboarding_status"] != "completed":
            raise PermissionError("Project creation requires paid client and completed onboarding")
        created = []
        previous = None
        for service in services:
            key = service.strip().lower()
            owner = SERVICE_OWNERS.get(key, "delivery-manager")
            cur = con.execute(
                "INSERT INTO tasks(title, owner, status, priority, depends_on) VALUES (?, ?, 'pending', 'normal', ?)",
                (f"Deliver {service.strip()}", owner, previous),
            )
            previous = cur.lastrowid
            created.append(cur.lastrowid)
        cur = con.execute(
            "INSERT INTO tasks(title, owner, status, priority, depends_on) VALUES (?, 'qa', 'pending', 'high', ?)",
            ("Final quality assurance", previous),
        )
        created.append(cur.lastrowid)
    return {"client_id": client_id, "task_ids": created}


def project_tasks(client_id: int):
    init_db()
    with connect() as con:
        rows = con.execute(
            "SELECT t.* FROM tasks t JOIN clients c ON c.id=? WHERE t.title NOT LIKE 'Quality assurance' ORDER BY t.id",
            (client_id,),
        ).fetchall()
    return [dict(row) for row in rows]
