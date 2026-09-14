from database.db import connect, init_db


def create_delivery_tasks(client_id: int, services: list[str]):
    init_db()
    tasks = []
    with connect() as con:
        client = con.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
        if client is None:
            raise ValueError(f"Client {client_id} not found")
        if client["payment_status"] != "paid" or client["onboarding_status"] != "completed":
            raise PermissionError("Delivery requires confirmed payment and completed onboarding")
        for service in services:
            cur = con.execute(
                "INSERT INTO tasks(title, owner, status, priority) VALUES (?, ?, 'pending', 'normal')",
                (f"Deliver {service.strip()}", service.strip().lower().replace(" ", "-")),
            )
            tasks.append(cur.lastrowid)
        cur = con.execute(
            "INSERT INTO tasks(title, owner, status, priority) VALUES ('Quality assurance', 'qa', 'pending', 'high')",
        )
        tasks.append(cur.lastrowid)
    return tasks
