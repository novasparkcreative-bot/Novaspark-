from dataclasses import dataclass


@dataclass
class OutreachDraft:
    subject: str
    body: str


def create_draft(business_name: str, industry: str = "", website: str = "", opportunity: str = "") -> OutreachDraft:
    name = business_name.strip()
    context = industry.strip() or "your business"
    service = opportunity.strip() or "digital marketing"
    subject = f"A growth idea for {name}"
    body = (
        f"Hi {name} team,\n\n"
        f"I was researching {context} businesses and noticed there may be an opportunity "
        f"to improve your online growth through {service}.\n\n"
        "I can share a short, practical audit with a few opportunities and no obligation. "
        "If this is relevant, let me know and I’ll send it over.\n\n"
        "Best,\nNovaSpark Creative"
    )
    return OutreachDraft(subject, body)
