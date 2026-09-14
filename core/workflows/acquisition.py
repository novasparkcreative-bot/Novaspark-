from database.db import connect, init_db
from core.ceo.alex import AlexCEO


def create_acquisition_workflow(lead_id: int) -> list[int]:
    """Create a dependency-ordered acquisition pipeline for one lead."""
    init_db()
    return AlexCEO().plan_acquisition(lead_id)


def ready_tasks() -> list[dict]:
    """Return pending tasks whose dependency is complete (or absent)."""
    init_db()
    with connect() as con:
        rows = con.execute(
            """
            SELECT t.* FROM tasks t
            WHERE t.status = 'pending'
              AND (t.depends_on IS NULL OR EXISTS (
                  SELECT 1 FROM tasks d WHERE d.id = t.depends_on AND d.status = 'completed'
              ))
            ORDER BY t.id
            """
        ).fetchall()
    return [dict(row) for row in rows]
