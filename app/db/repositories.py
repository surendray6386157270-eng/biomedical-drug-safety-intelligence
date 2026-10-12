from __future__ import annotations

import sqlite3

from app.models.evidence import EvidenceRecord


def save_evidence(connection, evidence) -> bool:
    cursor = connection.execute(
        """
        INSERT OR IGNORE INTO evidence (
            evidence_id,
            drug_name,
            drug_identifier,
            reaction,
            evidence_type,
            event_date,
            source,
            source_record_id,
            retrieved_at,
            source_reference,
            schema_version,
            transformation,
            raw_record_reference
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            evidence.evidence_id,
            evidence.drug_name,
            evidence.drug_identifier,
            evidence.reaction,
            evidence.evidence_type,
            evidence.event_date.isoformat() if evidence.event_date else None,
            evidence.source,
            evidence.source_record_id,
            evidence.retrieved_at.isoformat(),
            evidence.source_reference,
            evidence.schema_version,
            evidence.provenance.transformation,
            evidence.raw_record_reference,
        ),
    )

    connection.commit()

    return cursor.rowcount == 1



def search_evidence(
    connection: sqlite3.Connection,
    drug_name: str,
    limit: int = 50,
) -> list[sqlite3.Row]:
    cursor = connection.execute(
        """
        SELECT *
        FROM evidence
        WHERE LOWER(drug_name) = LOWER(?)
        ORDER BY event_date DESC
        LIMIT ?
        """,
        (drug_name.strip(), limit),
    )

    return cursor.fetchall()