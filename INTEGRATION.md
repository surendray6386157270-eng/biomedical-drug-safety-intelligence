# Integration Guide — Biomedical Drug Safety Intelligence System

## 1. Purpose

This document explains how another developer or BHIV research application can integrate with the biomedical drug safety evidence prototype.

The system provides source ingestion, normalized evidence storage, drug-specific search, and descriptive adverse-reaction analysis.

It is a research-oriented prototype, not a clinical decision-making system.

## 2. Architecture

The implementation is organized into the following layers:

| Layer | Location | Responsibility |
|---|---|---|
| Source connector | `app/connectors/openfda.py` | Retrieve FDA FAERS/openFDA reports |
| Evidence schema | `app/models/evidence.py` | Define structured evidence and provenance |
| Normalization | `app/services/normalization.py` | Transform source reports into evidence records |
| Ingestion | `app/services/ingestion.py` | Process acquired evidence |
| Pipeline | `app/services/pipeline.py` | Coordinate ingestion and analysis |
| Storage | `app/db/` | SQLite persistence and retrieval |
| Search | `app/services/search.py` | Retrieve drug-specific evidence |
| Analytics | `app/analytics/drug_reaction.py` | Count and rank reported reactions |
| API | `app/api/` | Expose HTTP endpoints |
| Research interface | `app/ui/index.html` | Display evidence and analysis |

## 3. Installation

Create a Python virtual environment and install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python -m uvicorn app.main:app --reload
```

The default local API base URL is:

`http://127.0.0.1:8000`

## 4. API Integration

### Health Check

`GET /health`

Checks whether the application responds.

### Ingest Drug Evidence

`POST /api/drugs/{drug_name}/ingest?limit=10`

Retrieves and processes source records for a specified drug.

Example:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/drugs/aspirin/ingest?limit=10"
```

### Retrieve Evidence

`GET /api/drugs/{drug_name}/evidence?limit=10`

Returns normalized evidence for the requested drug.

### Retrieve Analysis

`GET /api/drugs/{drug_name}/analysis?limit=10`

Returns descriptive reaction counts, proportions, limitations, and supporting evidence.

The analysis endpoint reads previously stored evidence. It does not automatically retrieve new source data.

## 5. Example Consumer Workflow

A research application can:

1. Submit a drug name to the ingestion endpoint.
2. Retrieve normalized evidence through the evidence endpoint.
3. Request descriptive analysis through the analysis endpoint.
4. Display source evidence separately from derived analytical output.
5. Allow researchers to inspect provenance and source references.

The consumer must not interpret reported reaction frequencies as population incidence or causal risk.

## 6. Data Contract

Evidence records are defined in `app/models/evidence.py`.

The schema includes drug and reaction information, evidence identifiers, source metadata, schema version, and provenance.

Consumers should use the returned schema fields rather than assuming every optional biomedical field is populated.

Saved response examples are available in:

- `evidence_packet/api_samples/aspirin_evidence.json`
- `evidence_packet/api_samples/aspirin_analysis.json`

## 7. Adding Another Biomedical Source

To integrate an additional source:

1. Create a new connector in `app/connectors/`.
2. Implement source retrieval and error handling.
3. Define source-specific normalization rules.
4. Map available source fields into the evidence schema.
5. Preserve original source identifiers and retrieval metadata.
6. Extend the ingestion pipeline to select the connector.
7. Add tests for successful retrieval, malformed responses, empty results, and source failures.
8. Update the dataset registry, data dictionary, and architecture documentation.

These are extension steps; additional source integrations are not currently implemented.

## 8. Error Handling

Integration consumers should handle:

- Invalid drug or query input
- Empty evidence results
- External source errors
- Malformed upstream responses
- Missing analytical input
- Local application failures

Do not treat an empty result as proof that a drug has no adverse reactions.

## 9. Operational Limitations

- SQLite is used for local prototype storage.
- No production deployment is demonstrated.
- Authentication and authorization are not implemented.
- External source availability and response content can change.
- Large-scale ingestion and performance have not been validated.
- Analytical output is descriptive rather than predictive.

## 10. Handover References

For additional details, consult:

- `README.md`
- `ARCHITECTURE.md`
- `docs/data_dictionary.md`
- `docs/dataset_registry.md`
- `docs/experiment.md`
- `docs/runtime_proof.md`
- `HANDOVER.md`

## 11. Integration Summary

The system provides a modular research evidence capability that can be reused through HTTP endpoints or extended through its Python service layers.

Production adoption requires additional validation, security controls, operational monitoring, and domain review.