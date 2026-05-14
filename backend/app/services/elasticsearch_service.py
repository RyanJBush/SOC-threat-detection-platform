from app.config import settings

try:
    from elasticsearch import Elasticsearch
except Exception:  # pragma: no cover
    Elasticsearch = None


class ElasticsearchService:
    def __init__(self) -> None:
        self.enabled = bool(getattr(settings, "elasticsearch_url", None)) and Elasticsearch is not None
        self.client = Elasticsearch(settings.elasticsearch_url) if self.enabled else None

    def index_event(self, event: object) -> None:
        if not self.client:
            return
        self.client.index(
            index="soc-events",
            document={
                "id": event.id,
                "organization_id": event.organization_id,
                "source": event.source,
                "source_ip": event.source_ip,
                "username": event.username,
                "event_type": event.event_type,
                "severity": event.severity,
                "status": event.status,
                "message": event.message,
                "metadata": event.event_metadata,
                "occurred_at": event.occurred_at.isoformat(),
            },
        )


elasticsearch_service = ElasticsearchService()
