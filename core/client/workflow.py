from core.client.client_lifecycle import confirm_payment_and_create_client, start_onboarding, complete_onboarding
from core.client.project_manager import create_project


def activate_paid_client(business_name: str, contact: str, services: list[str]):
    """Move a confirmed payment through onboarding and create delivery tasks."""
    client = confirm_payment_and_create_client(business_name, contact)
    start_onboarding(client["client_id"])
    complete_onboarding(client["client_id"])
    project = create_project(client["client_id"], services)
    return {"client": client, "project": project}
