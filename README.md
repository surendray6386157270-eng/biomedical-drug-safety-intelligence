# Biomedical Drug Safety Intelligence System

## Overview

The Biomedical Drug Safety Intelligence System is a research-oriented prototype for processing publicly accessible biomedical drug-safety evidence.

The system is designed to support a traceable workflow:

**Real Biomedical Source → Ingestion → Validation → Normalisation → Provenance → Analysis → Search → Result → Evidence Trace**

The system is intended for research and descriptive evidence intelligence. It is not a medical diagnosis system, treatment recommendation system, or clinical decision-support authority.

## Objectives

The prototype aims to:

* retrieve real publicly accessible biomedical/drug-safety data
* validate and normalize source records
* preserve source identifiers and provenance
* store structured evidence
* support drug/evidence search
* perform scientifically defensible descriptive analysis
* expose results through an API and research interface
* handle source and processing failures
* provide reproducible execution and testing

## Implemented Data Source

The system uses publicly accessible FDA Adverse Event Reporting System (FAERS) data through the openFDA Drug Event API.

The ingestion pipeline retrieves source reports, validates and normalizes records, preserves provenance, and stores structured drug–reaction evidence in SQLite.

FAERS reports are spontaneous safety reports. Reporting frequencies must not be interpreted as incidence rates, evidence of causation, or proof that a drug is safe or unsafe.

## Technology Stack

- Python 3.12
- FastAPI and Uvicorn
- Pydantic
- HTTPX
- SQLite
- pytest
- HTML, CSS, and JavaScript research interface

Additional project dependencies are listed in `requirements.txt`.

## Installation and Execution

From the project root, create and activate a Python virtual environment on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python -m uvicorn app.main:app --reload
```

Open the research interface at:

`http://127.0.0.1:8000/`

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check service health |
| GET | `/api/drugs/{drug_name}/evidence` | Retrieve stored evidence |
| GET | `/api/drugs/{drug_name}/analysis` | Retrieve descriptive analysis |
| POST | `/api/drugs/{drug_name}/ingest` | Retrieve, normalize, and store source evidence |

The ingestion endpoint accepts a `limit` query parameter between 1 and 100, with a default of 10.

Example:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/drugs/aspirin/ingest?limit=10"
```

Source access requires network connectivity and depends on openFDA service availability.

## Automated Tests

Run the test suite from the project root:

```powershell
python -m pytest -q
```

Latest verified result, October 12, 2026:

`18 passed in 0.38s`

## Evidence Traceability

Evidence records retain source identification, source record references, retrieval timestamps, schema version, and transformation metadata.

The research interface separates source evidence from system-generated descriptive analysis.

## Current Project Status

Implemented and locally tested:

- openFDA/FAERS connector
- Ingestion and normalization pipeline
- Structured evidence schema and provenance
- SQLite evidence storage
- Drug evidence search API
- Descriptive reaction analysis
- FastAPI research interface
- Automated test suite
- Empty-result handling
- Initial runtime evidence screenshots

Remaining submission work includes final documentation review, reproducibility verification, evidence packet assembly, and handover materials.