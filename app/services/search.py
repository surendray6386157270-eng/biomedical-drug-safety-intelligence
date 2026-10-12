from __future__ import annotations

from typing import Any

from app.db.database import get_connection, initialize_database
from app.db.repositories import search_evidence


def search_drug_evidence(
    drug_name: str,
    limit: int = 50,
) -> list[dict[str, Any]]:
    if not drug_name or not drug_name.strip():
        raise ValueError("drug_name must not be empty")

    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")

    initialize_database()

    connection = get_connection()

    try:
        rows = search_evidence(
            connection,
            drug_name.strip(),
            limit,
        )

        results = []

        for row in rows:
            item = dict(row)

            item["provenance"] = {
                "source": item["source"],
                "source_url": item["source_reference"],
                "source_record_id": item["source_record_id"],
                "retrieved_at": item["retrieved_at"],
                "schema_version": item["schema_version"],
                "transformation": item["transformation"],
                "raw_record_reference": item["raw_record_reference"],
            }

            results.append(item)

        return results

    finally:
        connection.close()