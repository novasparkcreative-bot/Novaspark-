import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database.db import init_db, connect
from core.sales.lead_pipeline import add_lead, qualify_lead
from core.sales.outreach import create_draft
from core.approvals.gates import request_approval, set_approval
from core.client.workflow import activate_paid_client


def main():
    init_db()
    name = "NovaSpark Test Business"
    lead_id = add_lead(name, "https://example.com", "digital marketing", "Jaipur", "test@example.com", "smoke test")
    qualification = qualify_lead(lead_id)
    draft = create_draft(name, "digital marketing", "https://example.com", "needs more leads")
    approval = request_approval("send_outreach", {"business_name": name, "body": draft.body})
    decision = set_approval(approval["id"], "approved")
    client = activate_paid_client(name, "test@example.com", ["SEO", "Content"])

    with connect() as con:
        lead = con.execute("SELECT status FROM leads WHERE id=?", (lead_id,)).fetchone()
        assert lead is not None
        assert approval["id"] == decision["id"]
        assert decision["status"] == "approved"
        assert client["client"]["payment_status"] == "paid"
        assert client["project"]["task_ids"]

    print("E2E PASS")
    print({"lead_id": lead_id, "qualification": qualification, "approval_id": approval["id"], "client_id": client["client"]["client_id"], "task_ids": client["project"]["task_ids"]})


if __name__ == "__main__":
    main()
