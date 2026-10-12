
from datetime import datetime, timezone

from app.services.normalization import (
    normalize_faers_record,
    normalize_faers_records,
)


def test_normalizes_faers_record():
    record = {
        "safetyreportid": "TEST123",
        "receivedate": "20260115",
        "patient": {
            "drug": [
                {
                    "medicinalproduct": "ASPIRIN",
                }
            ],
            "reaction": [
                {
                    "reactionmeddrapt": "Headache",
                }
            ],
        },
    }

    retrieved_at = datetime.now(timezone.utc)

    evidence = normalize_faers_record(
        record,
        retrieved_at,
        "https://api.fda.gov/drug/event.json",
    )

    assert evidence.source_record_id == "TEST123"
    assert evidence.drug_name == "ASPIRIN"
    assert evidence.reaction == "Headache"
    assert evidence.event_date is not None
    assert evidence.source == "FDA FAERS / openFDA"
    assert evidence.schema_version == "1.0"
    assert evidence.provenance.source_record_id == "TEST123"


def test_missing_reaction_is_explicit_null():
    record = {
        "safetyreportid": "TEST456",
        "patient": {
            "drug": [
                {
                    "medicinalproduct": "ASPIRIN",
                }
            ]
        },
    }

    retrieved_at = datetime.now(timezone.utc)

    evidence = normalize_faers_record(
        record,
        retrieved_at,
        "https://api.fda.gov/drug/event.json",
    )

    assert evidence.reaction is None


def test_multi_drug_report_preserves_all_drugs():
    record = {
        "safetyreportid": "TEST789",
        "receivedate": "20260120",
        "patient": {
            "drug": [
                {
                    "medicinalproduct": "DOXYCYCLINE",
                },
                {
                    "medicinalproduct": "ASPIRIN",
                },
            ],
            "reaction": [
                {
                    "reactionmeddrapt": "Headache",
                },
            ],
        },
    }

    retrieved_at = datetime.now(timezone.utc)

    evidence_records = normalize_faers_records(
        record,
        retrieved_at,
        "https://api.fda.gov/drug/event.json",
    )

    drug_names = {evidence.drug_name for evidence in evidence_records}

    assert "DOXYCYCLINE" in drug_names
    assert "ASPIRIN" in drug_names
    assert len(evidence_records) == 2

    for evidence in evidence_records:
        assert evidence.source_record_id == "TEST789"
        assert evidence.reaction == "Headache"
        assert evidence.provenance.source_record_id == "TEST789"