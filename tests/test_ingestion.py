
from app.db.database import get_connection, initialize_database
from app.db.repositories import search_evidence
from app.services.ingestion import ingest_drug


def test_database_initializes(tmp_path, monkeypatch):
    database_path = tmp_path / "test.db"

    import app.db.database as database

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        database_path,
    )

    initialize_database()

    connection = get_connection()

    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    ).fetchall()

    connection.close()

    assert any(row["name"] == "evidence" for row in tables)


def test_repeat_ingestion_does_not_create_duplicate_evidence(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "test.db"

    import app.db.database as database
    import app.services.ingestion as ingestion

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        database_path,
    )

    class FakeConnector:
        def search_drug(self, drug_name, limit=10):
            return {
                "source": "FDA FAERS / openFDA",
                "source_url": "https://api.fda.gov/drug/event.json",
                "retrieved_at": "2026-01-20T00:00:00+00:00",
                "total": 1,
                "results": [
                    {
                        "safetyreportid": "DUPLICATE_TEST_001",
                        "receivedate": "20260120",
                        "patient": {
                            "drug": [
                                {
                                    "medicinalproduct": "ASPIRIN",
                                },
                                {
                                    "medicinalproduct": "IBUPROFEN",
                                },
                            ],
                            "reaction": [
                                {
                                    "reactionmeddrapt": "Headache",
                                },
                            ],
                        },
                    }
                ],
            }

    monkeypatch.setattr(
        ingestion,
        "OpenFDAConnector",
        FakeConnector,
    )

    first_result = ingest_drug("aspirin", limit=1)
    second_result = ingest_drug("aspirin", limit=1)

    connection = get_connection()

    total = connection.execute(
        "SELECT COUNT(*) FROM evidence"
    ).fetchone()[0]

    duplicate_ids = connection.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT evidence_id
            FROM evidence
            GROUP BY evidence_id
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]

    connection.close()

    assert first_result["records_processed"] == 2
    assert first_result["records_inserted"] == 2

    assert second_result["records_processed"] == 2
    assert second_result["records_inserted"] == 0
    assert total == 2
    assert duplicate_ids == 0
