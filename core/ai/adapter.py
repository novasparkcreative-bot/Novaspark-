from abc import ABC, abstractmethod


class AIAdapter(ABC):
    """Stable interface for optional local or hosted models."""

    @abstractmethod
    def generate(self, prompt: str, system: str = "") -> str:
        raise NotImplementedError


class TemplateAI(AIAdapter):
    """Zero-cost fallback. Keeps the application runnable without an API key."""

    def generate(self, prompt: str, system: str = "") -> str:
        return f"[LOCAL TEMPLATE MODE]\n{prompt.strip()}"


def get_ai_adapter():
    """Return the configured provider without making any network request."""
    # A future Ollama/local-model adapter can be plugged in here.
    return TemplateAI()
