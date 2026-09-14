from core.ceo.alex import AlexCEO
from core.orchestrator.engine import Orchestrator
from core.sales.lead_pipeline import qualify_lead
from core.sales.outreach import create_draft
from core.approvals.gates import request_approval


class NovaSparkPipeline:
    """Connects the local acquisition components into one controlled workflow."""

    def __init__(self):
        self.ceo = AlexCEO()
        self.orchestrator = Orchestrator()

    def prepare_lead(self, lead_id: int):
        result = qualify_lead(lead_id)
        return {"lead_id": lead_id, "qualification": result}

    def prepare_outreach(self, business_name, industry="", website="", opportunity=""):
        draft = create_draft(business_name, industry, website, opportunity)
        approval = request_approval(
            "send_outreach",
            {"business_name": business_name, "subject": draft.subject, "body": draft.body},
        )
        return {"draft": {"subject": draft.subject, "body": draft.body}, "approval": approval}

    def plan_goal(self, goal: str):
        return self.ceo.plan(goal)
