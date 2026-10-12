from __future__ import annotations

import hashlib
from datetime import date, datetime
from typing import Any

from app.models.evidence import EvidenceRecord, Provenance


def _first_value(value: Any) -> str | None:
    """Extract the first string value from a FAERS field."""
    if isinstance(value, list) and value:
        first = value[0]

        if isinstance(first, dict):
            value = first.get("medicinalproduct")

        if value is not None:
            return str(value).strip() or None

    if isinstance(value, str):
        return value.strip() or None

    return None


def _make_evidence_id(
    source_record_id: str,
    drug_name: str,
    reaction: str | None,
) -> str:
    raw = f"{source_record_id}|{drug_name}|{reaction or ''}"

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()[:24]


def normalize_faers_records(
    record: dict[str, Any],
    retrieved_at: datetime,
    source_url: str,
) -> list[EvidenceRecord]:
    """
    Normalize one FAERS report into one EvidenceRecord per drug/reaction pair.

    A FAERS report can contain multiple drugs. Keeping each drug explicitly
    prevents loss of the drug that matched the source query.
    """
    safety_report_id = str(
        record.get("safetyreportid")
        or record.get("safetyreportversion")
        or "UNKNOWN"
    )

    patient = record.get("patient") or {}
    drugs = patient.get("drug") or []
    reactions = patient.get("reaction") or []

    drug_names: list[str] = []

    for drug in drugs:
        if not isinstance(drug, dict):
            continue

        name = _first_value(drug.get("medicinalproduct"))

        if name and name not in drug_names:
            drug_names.append(name)

    reaction_names: list[str] = []

    for item in reactions:
        if not isinstance(item, dict):
            continue

        reaction = _first_value(item.get("reactionmeddrapt"))

        if reaction and reaction not in reaction_names:
            reaction_names.append(reaction)

    if not drug_names:
        drug_names = ["UNKNOWN"]

    if not reaction_names:
        reaction_names = [None]

    event_date = None
    receive_date = record.get("receivedate")

    if isinstance(receive_date, str) and len(receive_date) >= 8:
        try:
            event_date = date(
                int(receive_date[0:4]),
                int(receive_date[4:6]),
                int(receive_date[6:8]),
            )
        except ValueError:
            event_date = None

    provenance = Provenance(
        source="FDA FAERS / openFDA",
        source_url=source_url,
        source_record_id=safety_report_id,
        retrieved_at=retrieved_at,
        schema_version="1.0",
        transformation=(
            "FAERS JSON normalized into one EvidenceRecord "
            "per drug/reaction pair"
        ),
        raw_record_reference=safety_report_id,
    )

    evidence_records: list[EvidenceRecord] = []

    for drug_name in drug_names:
        for reaction in reaction_names:
            evidence_id = _make_evidence_id(
                safety_report_id,
                drug_name,
                reaction,
            )

            evidence_records.append(
                EvidenceRecord(
                    evidence_id=evidence_id,
                    drug_name=drug_name,
                    drug_identifier=None,
                    reaction=reaction,
                    evidence_type="adverse_event_report",
                    event_date=event_date,
                    source="FDA FAERS / openFDA",
                    source_record_id=safety_report_id,
                    retrieved_at=retrieved_at,
                    source_reference=source_url,
                    schema_version="1.0",
                    provenance=provenance,
                    raw_record_reference=safety_report_id,
                )
            )

    return evidence_records


def normalize_faers_record(
    record: dict[str, Any],
    retrieved_at: datetime,
    source_url: str,
) -> EvidenceRecord:
    """
    Backward-compatible single-record normalizer.

    Returns the first normalized evidence record from the
    multi-drug normalization function.
    """
    records = normalize_faers_records(
        record=record,
        retrieved_at=retrieved_at,
        source_url=source_url,
    )

    return records[0]