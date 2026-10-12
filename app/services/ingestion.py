from app.connectors.openfda import OpenFDAConnector
from app.db.database import get_connection, initialize_database
from app.db.repositories import save_evidence
from app.services.normalization import normalize_faers_records


def ingest_drug(
    drug_name: str,
    limit: int = 10,
) -> dict:
    initialize_database()

    connector = OpenFDAConnector()

    response = connector.search_drug(
        drug_name=drug_name,
        limit=limit,
    )

    connection = get_connection()

    records_processed = 0
    records_inserted = 0

    for record in response["results"]:
        evidence_records = normalize_faers_records(
            record=record,
            retrieved_at=response["retrieved_at"],
            source_url=response["source_url"],
        )

        for evidence in evidence_records:
            records_processed += 1

            if save_evidence(connection, evidence):
                records_inserted += 1

    connection.close()

    return {
        "records_processed": records_processed,
        "records_inserted": records_inserted,
    }