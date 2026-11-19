from qdrant_client import QdrantClient

from app.core.config import settings
from app.repositories.health_repository import HealthRepository


class HealthService:

    def __init__(self, repository: HealthRepository):

        self.repository = repository

        self.qdrant = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY or None,
            timeout=5
        )

    async def check_database(self):

        return await self.repository.check_database()

    def check_qdrant(self):

        self.qdrant.get_collections()

        return True

    def check_gemini_config(self):

        return bool(settings.GEMINI_API_KEY)
