from dataclasses import dataclass
from core.approvals.gates import request_approval


@dataclass
class SalesReply:
    stage: str
    message: str
    needs_human: bool = False
    approval_id: int | None = None


def handle_reply(business_name: str, incoming: str, services: str = "SEO, website and digital marketing", pricing: str = "") -> SalesReply:
    text = incoming.strip().lower()
    if not text:
        raise ValueError("incoming message cannot be empty")

    if any(x in text for x in ("unsubscribe", "stop", "remove me", "do not contact")):
        return SalesReply("opted_out", "Understood. We won't contact you again.")

    if any(x in text for x in ("price", "pricing", "cost", "how much")):
        price_text = pricing.strip() or "I can share the approved package options based on your requirements."
        return SalesReply("pricing", f"Thanks for asking. {price_text}")

    if any(x in text for x in ("interested", "yes", "tell me more", "sounds good", "book")):
        approval = request_approval("send_proposal", {"business_name": business_name, "services": services})
        return SalesReply(
            "qualified_interest",
            "Thanks — I'd be happy to put together a proposal based on your needs. I'll confirm the next step shortly.",
            needs_human=True,
            approval_id=approval["id"],
        )

    if any(x in text for x in ("no", "not interested", "not now")):
        return SalesReply("not_interested", "Thanks for letting us know. Wishing you all the best.")

    return SalesReply(
        "discovery",
        f"Thanks for getting back to us. To understand whether we can help {business_name}, what is the main marketing goal you'd like to improve right now?",
    )
