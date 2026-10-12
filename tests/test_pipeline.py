from datetime import datetime, timezone

from app.services.pipeline import run_pipeline


def test_pipeline_rejects_empty_drug():
    try:
        run_pipeline("")
        assert False
    except ValueError as exc:
        assert "drug_name" in str(exc)


def test_pipeline_with_mocked_source(tmp_path, monkeypatch):
    import app.db.database as database
    import app.services.pipeline as pipeline

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        tmp_path / "pipeline.db",
    )

    class FakeConnector:
        def search_drug(self, drug_name, limit):
            return {
                "source": "FDA FAERS / openFDA",
                "source_url": "https://api.fda.gov/drug/event.json",
                "retrieved_at": datetime.now(timezone.utc),
                "total": 1,
                "results": [
                    {
                        "safetyreportid": "PIPELINE001",
                        "receivedate": "20260115",
                        "patient": {
                            "drug": [
                                {
                                    "medicinalproduct": "ASPIRIN"
                                }
                            ],
                            "reaction": [
                                {
                                    "reactionmeddrapt": "Headache"
                                }
                            ],
                        },
                    }
                ],
            }

    monkeypatch.setattr(
        pipeline,
        "OpenFDAConnector",
        FakeConnector,
    )

    result = run_pipeline("ASPIRIN", limit=1)

    assert result["records_retrieved"] == 1
    assert result["records_processed"] == 1
    assert result["records_inserted"] == 1
    assert result["source"] == "FDA FAERS / openFDA"
    assert result["analysis"]["analysis"]["total_records"] == 1