from database.db import connect, init_db


def confirm_payment_and_create_client(business_name: str, contact: str = ""):
    init_db()
    with connect() as con:
        cur = con.execute(
            "INSERT INTO clients(business_name, contact, payment_status, onboarding_status) VALUES (?, ?, 'paid', 'pending')",
            (business_name.strip(), contact.strip()),
        )
        client_id = cur.lastrowid
        return {"client_id": client_id, "business_name": business_name.strip(), "payment_status": "paid", "onboarding_status": "pending"}


def start_onboarding(client_id: int):
    init_db()
    with connect() as con:
        row = con.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
        if row is None:
            raise ValueError(f"Client {client_id} not found")
        if row["payment_status"] != "paid":
            raise PermissionError("Client onboarding cannot start until payment is confirmed")
        con.execute("UPDATE clients SET onboarding_status = 'in_progress' WHERE id = ?", (client_id,))
        return {"client_id": client_id, "onboarding_status": "in_progress"}


def complete_onboarding(client_id: int):
    init_db()
    with connect() as con:
        con.execute("UPDATE clients SET onboarding_status = 'completed' WHERE id = ?", (client_id,))
    return {"client_id": client_id, "onboarding_status": "completed"}
