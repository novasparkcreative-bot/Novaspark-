import unittest

from database.db import connect, init_db
from core.ai.adapter import get_ai_adapter
from core.sales.lead_pipeline import add_lead, qualify_lead, get_leads
from core.sales.outreach import create_draft
from core.orchestrator.engine import Orchestrator


class NovaSparkSmokeTests(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_database_and_lead_flow(self):
        lead_id = add_lead(
            "Smoke Test Business",
            "https://example.com",
            "marketing",
            "Jaipur",
            "test@example.com",
        )
        result = qualify_lead(lead_id)
        self.assertEqual(result["status"], "qualified")
        self.assertTrue(any(x["id"] == lead_id for x in get_leads()))

    def test_outreach_is_draft_only(self):
        draft = create_draft("Smoke Test Business", "marketing")
        self.assertTrue(draft.subject)
        self.assertIn("Smoke Test Business", draft.body)

    def test_ai_fallback_requires_no_api_key(self):
        output = get_ai_adapter().generate("hello")
        self.assertIn("LOCAL TEMPLATE MODE", output)

    def test_orchestrator_dependency(self):
        runner = Orchestrator()
        first = runner.add_task("first", "qa")
        second = runner.add_task("second", "qa", depends_on=first)
        ready = {task["id"] for task in runner.ready_tasks()}
        self.assertIn(first, ready)
        self.assertNotIn(second, ready)
        runner.start(first)
        runner.complete(first, "ok")
        ready = {task["id"] for task in runner.ready_tasks()}
        self.assertIn(second, ready)


if __name__ == "__main__":
    unittest.main()
