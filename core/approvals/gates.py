from database.db import connect, init_db
import json

HIGH_IMPACT_ACTIONS = {"send_outreach", "send_proposal", "pricing_exception", "confirm_payment", "contract_commitment"}


def request_approval(action, payload):
    init_db()
    status = "pending" if action in HIGH_IMPACT_ACTIONS else "auto"
    with connect() as con:
        cur = con.execute(
            "INSERT INTO approvals(action, payload, status) VALUES (?, ?, ?)",
            (action, json.dumps(payload, ensure_ascii=False), status),
        )
        return {"id": cur.lastrowid, "action": action, "status": status}


def set_approval(approval_id, status):
    if status not in {"approved", "rejected"}:
        raise ValueError("status must be approved or rejected")
    with connect() as con:
        con.execute("UPDATE approvals SET status = ? WHERE id = ?", (status, approval_id))
    return {"id": approval_id, "status": status}
