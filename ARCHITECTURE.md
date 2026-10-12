# System Architecture

## 1. Purpose

This document describes the architecture of the Biomedical Drug Safety Intelligence System.

The system is designed to transform publicly accessible biomedical/drug-safety source data into structured, searchable, traceable evidence and descriptive analytical output.

## 2. Core Pipeline

```text
REAL SOURCE
    ↓
INGESTION
    ↓
VALIDATION
    ↓
NORMALISATION
    ↓
PROVENANCE
    ↓
EVIDENCE STORE
    ↓
ANALYSIS
    ↓
SEARCH / API
    ↓
RESEARCH INTERFACE
    ↓
EVIDENCE TRACE
```

## 3. Components

### Source Connector

Responsible for communicating with the selected external biomedical source.

Responsibilities:

* request data
* handle HTTP/API failures
* handle timeouts
* validate source responses
* record retrieval timestamp
* preserve source identifiers
* return structured source data

External-source logic must remain isolated from the user interface.

### Validation Layer

Responsible for checking:

* response structure
* required fields
* data types
* malformed records
* invalid values

Missing source information must not be invented.

### Normalization Layer

Transforms source-specific records into the internal evidence schema.

The normalized representation should be independent of the external API format where practical.

### Provenance Layer

Maintains traceability between normalized evidence and the original source record.

Important provenance fields include:

* source
* source record identifier
* retrieval timestamp
* source reference
* schema version
* raw record reference
* transformation metadata

### Evidence Store


The system uses SQLite to persist normalized biomedical drug-safety evidence.

The repository layer separates database operations from ingestion, search, and analytical services.

Evidence records preserve drug names, reported reactions, source record identifiers, schema versions, and provenance information.

Deterministic evidence identifiers support duplicate prevention during repeated ingestion.

The database stores source-derived evidence. Descriptive analysis is performed separately over retrieved evidence records.

SQLite is suitable for the current research prototype. A future production deployment may require additional database scalability, access control, and operational monitoring.

### Analytics Layer

The system implements descriptive drug–reaction analysis using normalized evidence records retrieved from SQLite.

The analysis summarizes:

- Number of evidence records analyzed
- Number of unique reported reactions
- Reaction frequencies
- Proportions of reactions within the analyzed evidence subset

The analytical output is identified as `descriptive_drug_reaction_analysis`.

The analysis operates on stored evidence records rather than directly on raw openFDA responses.

Scientific limitations:

- Reporting frequency is not adverse-event incidence.
- FAERS reporting data cannot establish causation.
- Results do not determine whether a drug is safe or unsafe.
- Analysis is limited to the evidence records included in the query.
- Descriptive patterns must not be interpreted as clinical recommendations.

The system separates SOURCE EVIDENCE from SYSTEM ANALYSIS.

Temporal analysis and predictive machine-learning models are not part of the currently verified implementation.

### API Layer

The system uses FastAPI to expose ingestion, evidence retrieval, descriptive analysis, and service-health operations.

Implemented endpoints:

| Method | Endpoint | Responsibility |
|---|---|---|
| GET | `/health` | Report service health |
| GET | `/api/drugs/{drug_name}/evidence` | Retrieve stored evidence for a drug |
| GET | `/api/drugs/{drug_name}/analysis` | Return descriptive analysis of stored evidence |
| POST | `/api/drugs/{drug_name}/ingest` | Run source ingestion, normalization, storage, and analysis |

The ingestion endpoint accepts a drug name and a `limit` query parameter (default 10, minimum 1, maximum 100).

FastAPI automatically provides interactive API documentation at `/docs` and an OpenAPI specification at `/openapi.json`.

The research interface is served from `/` using `FileResponse` and the HTML file at `app/ui/index.html`.

The API separates source ingestion, stored evidence retrieval, and system-generated descriptive analysis. Analytical results are not represented as original source evidence.

The ingestion route returns HTTP 400 for `ValueError` exceptions and HTTP 502 for other pipeline exceptions. Error behavior for other routes is defined by their respective implementations.

### Research Interface

The system provides a browser-based research interface implemented using HTML, CSS, and JavaScript.

The interface is available at `http://127.0.0.1:8000/` and is served by FastAPI from `app/ui/index.html`.

Implemented capabilities include:

- Searching stored evidence by drug name
- Displaying normalized drug–reaction evidence records
- Showing descriptive reaction analysis
- Displaying source identifiers and provenance information
- Showing evidence schema versions and transformation metadata
- Separating SOURCE EVIDENCE from SYSTEM ANALYSIS
- Displaying scientific limitations
- Handling queries that return no evidence
- Displaying request errors

The interface consumes the FastAPI evidence and analysis endpoints.

It is a research prototype and does not provide medical diagnosis, treatment recommendations, or clinical decision-making.

## 4. Evidence vs Analysis


The implemented research interface explicitly separates two categories of information:

**SOURCE EVIDENCE**

Normalized records derived from FDA FAERS/openFDA, including reported drug names, reactions, source record identifiers, retrieval timestamps, schema versions, and provenance metadata.

**SYSTEM ANALYSIS**

Descriptive summaries computed from stored evidence records, including reaction frequencies, unique reaction counts, and proportions within the analyzed evidence subset.

System-generated analysis is not presented as original clinical or regulatory evidence.

FAERS reporting patterns do not establish causation, adverse-event incidence, or whether a drug is safe or unsafe.

This separation supports transparent interpretation and traceability of research results.

## 5. Failure Handling
## 5. Failure Handling

The system implements error handling across the ingestion, API, and research interface layers.

The ingestion endpoint handles:

- Invalid pipeline inputs resulting in `ValueError`, returned as HTTP 400.
- Other ingestion pipeline exceptions, returned as HTTP 502 with an error description.

The research interface supports:

- Queries that return no evidence records.
- Displaying request errors.
- Avoiding fabricated evidence when no matching records are available.
- Displaying scientific limitations alongside analysis results.

The evidence storage layer uses deterministic evidence identifiers to support duplicate prevention during repeated ingestion.

External dependencies, including openFDA, may experience network failures, timeouts, rate limits, or service interruptions.

The current implementation is a research prototype. Production-grade retry policies, monitoring, and comprehensive operational recovery remain future improvements.

## 6. Reproducibility


The system supports local reproducibility through documented dependencies, source ingestion, versioned evidence records, and automated tests.

### Environment Setup

The verified development environment uses Python 3.12 on Windows.

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Application Execution

Start the FastAPI application:

```powershell
python -m uvicorn app.main:app --reload
```

The research interface is available at:

`http://127.0.0.1:8000/`

API documentation is available at:

`http://127.0.0.1:8000/docs`

### Evidence Ingestion

Retrieve real FDA FAERS/openFDA evidence for aspirin:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/drugs/aspirin/ingest?limit=10"
```

The ingestion pipeline retrieves source records, normalizes drug–reaction evidence, preserves provenance, and stores evidence in SQLite.

Repeated ingestion may produce zero newly inserted records when matching deterministic evidence identifiers already exist.

### Automated Testing

Run:

```powershell
python -m pytest -q
```

Latest locally verified result on October 12, 2026:

`18 passed in 0.38s`

### Evidence and Runtime Proof

The `evidence_packet/screenshots/` directory contains five captured proof files covering:

- Successful aspirin evidence search
- Empty-result handling
- API documentation
- Ingestion execution
- Automated test execution

### Reproducibility Limitations

FAERS/openFDA is an external, continuously updated source. Repeated live queries may return different data or source totals.

Automated tests provide repeatable checks, while live ingestion requires network connectivity and external service availability.

The system does not guarantee identical live-source results across different execution dates.

## 7. Scientific Limitations

The system provides descriptive evidence intelligence.

It does not establish:

* patient diagnosis
* treatment recommendations
* clinical efficacy
* causality
* that a drug is safe
* that a drug is unsafe
* regulatory approval

Analytical conclusions must remain proportional to the underlying data.
