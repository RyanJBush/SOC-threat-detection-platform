# Elasticsearch Setup

1. Start stack:
```bash
docker compose up --build
```
2. FastAPI writes logs to PostgreSQL and indexes each event to Elasticsearch (`soc-events`).
3. Open Kibana at `http://localhost:5601` and create a data view for `soc-events*`.
4. Validate ingestion:
```bash
curl http://localhost:9200/soc-events/_search?pretty
```
