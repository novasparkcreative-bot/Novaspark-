from database.db import connect, init_db

class AlexCEO:
    """NovaSpark CEO orchestration facade.

    Alex plans and coordinates work; high-impact external actions remain
    behind explicit approval gates.
    """
    name = "Alex"

    def __init__(self):
        init_db()

    def create_task(self, title, owner, priority="normal", depends_on=None):
        with connect() as con:
            cur = con.execute(
                "INSERT INTO tasks(title, owner, priority, depends_on) VALUES (?, ?, ?, ?)",
                (title, owner, priority, depends_on),
            )
            return cur.lastrowid

    def plan_acquisition(self, lead_id):
        steps = [
            ("Research lead", "lead-research"),
            ("Prepare personalized outreach", "outreach"),
            ("Qualify conversation", "sales"),
            ("Prepare proposal", "sales"),
            ("Onboard after payment confirmation", "onboarding"),
        ]
        ids = []
        previous = None
        for title, owner in steps:
            task_id = self.create_task(f"{title} #{lead_id}", owner, depends_on=previous)
            ids.append(task_id)
            previous = task_id
        return ids

    def status(self):
        with connect() as con:
            rows = con.execute(
                "SELECT status, COUNT(*) AS count FROM tasks GROUP BY status"
            ).fetchall()
        return {row["status"]: row["count"] for row in rows}
