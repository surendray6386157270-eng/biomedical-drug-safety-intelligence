# Evidence Data Dictionary

## Purpose

This document defines the normalized evidence representation used by the Biomedical Drug Safety Evidence Intelligence System.

The schema provides a stable internal representation independent of the external biomedical source format.

---

## EvidenceRecord

| Field                  | Type          | Required | Description                                                                   |
| ---------------------- | ------------- | -------: | ----------------------------------------------------------------------------- |
| `evidence_id`          | string        |      Yes | Deterministic identifier for the normalized evidence record                   |
| `drug_name`            | string        |      Yes | Normalized drug name associated with the evidence                             |
| `drug_identifier`      | string / NULL |       No | Source or normalized identifier for the drug when available                   |
| `reaction`             | string / NULL |       No | Reported adverse reaction/event                                               |
| `evidence_type`        | string        |      Yes | Type of evidence represented by the record                                    |
| `event_date`           | date / NULL   |       No | Event date when available from the source                                     |
| `source`               | string        |      Yes | Name of the originating data source                                           |
| `source_record_id`     | string        |      Yes | Identifier connecting the normalized record to the source                     |
| `retrieved_at`         | datetime      |      Yes | Timestamp at which the source record was retrieved                            |
| `source_reference`     | string        |      Yes | Reference to the source endpoint or source resource                           |
| `schema_version`       | string        |      Yes | Version of the internal evidence schema                                       |
| `provenance`           | object        |      Yes | Information describing source and transformation history                      |
| `raw_record_reference` | string / NULL |       No | Reference to retained raw source data when available                          |
| `metadata`             | object        |      Yes | Additional source-derived information that does not belong in the core schema |

---

## Provenance

| Field                  | Type          | Required | Description                                         |
| ---------------------- | ------------- | -------: | --------------------------------------------------- |
| `source`               | string        |      Yes | Original biomedical data source                     |
| `source_url`           | string        |      Yes | Source endpoint/resource used to retrieve evidence  |
| `source_record_id`     | string        |      Yes | Original source record identifier                   |
| `retrieved_at`         | datetime      |      Yes | Retrieval timestamp                                 |
| `schema_version`       | string        |      Yes | Internal evidence schema version                    |
| `transformation`       | string        |      Yes | Description of normalization/transformation applied |
| `raw_record_reference` | string / NULL |       No | Reference to raw source record                      |

---

## Missing Values

Missing source information must not be fabricated.

When a source does not provide a value:

* nullable fields use `NULL`
* optional identifiers remain `NULL`
* optional dates remain `NULL`
* unavailable source metadata remains `NULL`

The system must not invent values to complete a record.

---

## Evidence Identity

`evidence_id` identifies the normalized internal evidence record.

`source_record_id` identifies the corresponding record in the external source.

These identifiers serve different purposes:

```text
evidence_id
    ↓
Internal system identity

source_record_id
    ↓
External source identity
```

The relationship between them must remain traceable.

---

## Schema Versioning

Current version:

```text
1.0
```

Changes to required fields, field meaning, normalization behavior, or provenance semantics should result in an explicit schema-version change.

---

## Evidence vs Analysis

An `EvidenceRecord` represents information obtained from the external source after validation and normalization.

It does **not** represent:

* a causal conclusion
* a clinical recommendation
* a diagnosis
* a treatment recommendation
* a declaration that a drug is safe or unsafe

Analytical outputs will be represented separately from source evidence.

---

## Traceability Requirement

Every normalized evidence record must be traceable through:

```text
EvidenceRecord
      ↓
source
      ↓
source_record_id
      ↓
source_reference
      ↓
retrieved_at
      ↓
transformation
      ↓
schema_version
```

This allows a researcher or reviewer to understand where an analytical input originated and how it entered the system.
