from database.db import connect, init_db


def score_lead(website="", industry="", location="", contact=""):
    score = 0
    if website.strip(): score += 25
    if industry.strip(): score += 25
    if location.strip(): score += 20
    if contact.strip(): score += 30
    return min(score, 100)


def add_lead(business_name, website="", industry="", location="", contact="", notes=""):
    init_db()
    score = score_lead(website, industry, location, contact)
    with connect() as con:
        cur = con.execute(
            "INSERT INTO leads(business_name, website, industry, location, contact, score, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (business_name.strip(), website.strip(), industry.strip(), location.strip(), contact.strip(), score, notes.strip()),
        )
        return cur.lastrowid


def get_leads(status=None):
    init_db()
    with connect() as con:
        if status:
            rows = con.execute("SELECT * FROM leads WHERE status = ? ORDER BY score DESC, id DESC", (status,)).fetchall()
        else:
            rows = con.execute("SELECT * FROM leads ORDER BY score DESC, id DESC").fetchall()
    return [dict(row) for row in rows]


def qualify_lead(lead_id, minimum_score=60):
    init_db()
    with connect() as con:
        row = con.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
        if row is None:
            raise ValueError(f"Lead {lead_id} not found")
        status = "qualified" if row["score"] >= minimum_score else "unqualified"
        con.execute("UPDATE leads SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (status, lead_id))
        return {"lead_id": lead_id, "status": status, "score": row["score"]}
