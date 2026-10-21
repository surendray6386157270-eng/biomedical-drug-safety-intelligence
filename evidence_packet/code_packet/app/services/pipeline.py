from __future__ import annotations

from typing import Any

from app.connectors.openfda import OpenFDAConnector
from app.db.database import get_connection, initialize_database
from app.db.repositories import save_evidence
from app.services.analysis import analyze_drug
from app.services.normalization import normalize_faers_records


def run_pipeline(
    drug_name: str,
    limit: int = 10,
) -> dict[str, Any]:
    """Run real source retrieval through storage and analysis."""

    if not drug_name or not drug_name.strip():
        raise ValueError("drug_name must not be empty")

    initialize_database()

    connector = OpenFDAConnector()

    source_response = connector.search_drug(
        drug_name=drug_name,
        limit=limit,
    )

    connection = get_connection()

    records_processed = 0
    records_inserted = 0

    try:
        for record in source_response["results"]:
            evidence_records = normalize_faers_records(
            record=record,
            retrieved_at=source_response["retrieved_at"],
            source_url=source_response["source_url"],
    )
            for evidence in evidence_records:
                records_processed += 1

                if save_evidence(connection, evidence):
                    records_inserted += 1
    finally:
        connection.close()

    analysis_result = analyze_drug(
        drug_name=drug_name,
        limit=limit,
    )

    return {
        "source": source_response["source"],
        "source_url": source_response["source_url"],
        "retrieved_at": source_response["retrieved_at"],
        "source_total": source_response["total"],
        "records_retrieved": len(source_response["results"]),
        "records_processed": records_processed,
        "records_inserted": records_inserted,
        "analysis": analysis_result,
    }