from core.ai.adapter import get_ai_adapter
from core.sales.outreach import create_draft


class AgentHandlers:
    """Safe default handlers. External side effects are intentionally not performed here."""

    def __init__(self):
        self.ai = get_ai_adapter()

    def research(self, task):
        return self.ai.generate(f"Prepare a research checklist for task: {task['title']}")

    def outreach(self, task):
        return self.ai.generate(f"Prepare an outreach draft for task: {task['title']}. Do not send it.")

    def sales(self, task):
        return self.ai.generate(f"Prepare a sales follow-up plan for task: {task['title']}.")

    def seo(self, task):
        return self.ai.generate(f"Create an SEO delivery checklist for task: {task['title']}.")

    def content(self, task):
        return self.ai.generate(f"Create a content production checklist for task: {task['title']}.")

    def social(self, task):
        return self.ai.generate(f"Create a social media delivery checklist for task: {task['title']}.")

    def qa(self, task):
        return self.ai.generate(f"Create a QA checklist for task: {task['title']}.")


def default_handlers():
    h = AgentHandlers()
    return {
        "lead-research": h.research,
        "outreach": h.outreach,
        "sales": h.sales,
        "seo": h.seo,
        "content": h.content,
        "social-media": h.social,
        "qa": h.qa,
    }
