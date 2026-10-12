from datetime import datetime, timezone

import pytest

from app.db.database import get_connection, initialize_database
from app.db.repositories import save_evidence
from app.models.evidence import EvidenceRecord, Provenance
from app.services.search import search_drug_evidence


def test_search_rejects_empty_query():
    with pytest.raises(ValueError):
        search_drug_evidence("")


def test_search_rejects_invalid_limit():
    with pytest.raises(ValueError):
        search_drug_evidence("aspirin", limit=0)


def test_search_returns_saved_evidence(tmp_path, monkeypatch):
    import app.db.database as database

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        tmp_path / "test.db",
    )

    initialize_database()

    evidence = EvidenceRecord(
        evidence_id="test-evidence-001",
        drug_name="ASPIRIN",
        reaction="Headache",
        evidence_type="adverse_event_report",
        source="FDA FAERS / openFDA",
        source_record_id="TEST001",
        retrieved_at=datetime.now(timezone.utc),
        source_reference="https://api.fda.gov/drug/event.json",
        schema_version="1.0",
        provenance=Provenance(
            source="FDA FAERS / openFDA",
            source_url="https://api.fda.gov/drug/event.json",
            source_record_id="TEST001",
            retrieved_at=datetime.now(timezone.utc),
            transformation="test normalization",
        ),
    )

    connection = get_connection()
    save_evidence(connection, evidence)
    connection.close()

    results = search_drug_evidence("aspirin")

    assert len(results) == 1
    assert results[0]["drug_name"] == "ASPIRIN"
    assert results[0]["reaction"] == "Headache"