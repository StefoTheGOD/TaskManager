
from services.ai_service import OllamaAIService


class MockAIService:
    """Тестов AI доставчик без връзка с Ollama."""

    def generate_response(self, user_message, tasks=None):
        return (
            "Тестов AI отговор.\n"
            f"Получен въпрос: {user_message}\n"
            f"Брой задачи: {len(tasks) if tasks else 0}"
        )


class AIFactory:
    """Factory Design Pattern - създава избрания AI доставчик."""

    @staticmethod
    def create_ai_service(provider="ollama"):
        if provider == "ollama":
            return OllamaAIService()

        if provider == "mock":
            return MockAIService()

        raise ValueError(
            f"Неподдържан AI доставчик: {provider}"
        )


