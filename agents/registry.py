AGENTS = {
    "lead-research": {"department": "sales", "risk": "low"},
    "outreach": {"department": "sales", "risk": "external"},
    "sales": {"department": "sales", "risk": "external"},
    "onboarding": {"department": "operations", "risk": "medium"},
    "seo": {"department": "marketing", "risk": "low"},
    "content": {"department": "marketing", "risk": "medium"},
    "social": {"department": "marketing", "risk": "external"},
    "qa": {"department": "quality", "risk": "low"},
}

def get_agent(name):
    if name not in AGENTS:
        raise KeyError(f"Unknown NovaSpark agent: {name}")
    return {"name": name, **AGENTS[name]}
