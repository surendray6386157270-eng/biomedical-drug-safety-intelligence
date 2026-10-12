from datetime import datetime, timezone

from app.db.database import get_connection, initialize_database
from app.db.repositories import save_evidence
from app.models.evidence import EvidenceRecord, Provenance
from app.services.analysis import analyze_drug


def test_analyze_drug_from_stored_evidence(
    tmp_path,
    monkeypatch,
):
    import app.db.database as database

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        tmp_path / "test.db",
    )

    initialize_database()

    retrieved_at = datetime.now(timezone.utc)

    records = [
        EvidenceRecord(
            evidence_id="analysis-001",
            drug_name="ASPIRIN",
            reaction="Headache",
            evidence_type="adverse_event_report",
            source="FDA FAERS / openFDA",
            source_record_id="REPORT001",
            retrieved_at=retrieved_at,
            source_reference="https://api.fda.gov/drug/event.json",
            schema_version="1.0",
            provenance=Provenance(
                source="FDA FAERS / openFDA",
                source_url="https://api.fda.gov/drug/event.json",
                source_record_id="REPORT001",
                retrieved_at=retrieved_at,
                transformation="FAERS normalization",
            ),
        ),
        EvidenceRecord(
            evidence_id="analysis-002",
            drug_name="ASPIRIN",
            reaction="Nausea",
            evidence_type="adverse_event_report",
            source="FDA FAERS / openFDA",
            source_record_id="REPORT002",
            retrieved_at=retrieved_at,
            source_reference="https://api.fda.gov/drug/event.json",
            schema_version="1.0",
            provenance=Provenance(
                source="FDA FAERS / openFDA",
                source_url="https://api.fda.gov/drug/event.json",
                source_record_id="REPORT002",
                retrieved_at=retrieved_at,
                transformation="FAERS normalization",
            ),
        ),
    ]

    connection = get_connection()

    for evidence in records:
        save_evidence(connection, evidence)

    connection.close()

    result = analyze_drug("ASPIRIN")

    assert result["drug_name"] == "ASPIRIN"
    assert result["input_evidence_count"] == 2
    assert result["analysis"]["total_records"] == 2
    assert result["analysis"]["unique_reactions"] == 2
    assert result["source"] == "FDA FAERS / openFDA"