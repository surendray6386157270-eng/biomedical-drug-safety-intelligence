from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class Provenance(BaseModel):
    source: str
    source_url: str
    source_record_id: str
    retrieved_at: datetime
    schema_version: str = "1.0"
    transformation: str
    raw_record_reference: str | None = None


class EvidenceRecord(BaseModel):
    evidence_id: str
    drug_name: str
    drug_identifier: str | None = None

    reaction: str | None = None
    evidence_type: str = "adverse_event_report"

    event_date: date | None = None

    source: str
    source_record_id: str

    retrieved_at: datetime
    source_reference: str

    schema_version: str = "1.0"

    provenance: Provenance

    raw_record_reference: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
