# Biomedical Drug Safety Intelligence System

## BHIV AI/ML Biotech — Project Submission



### 1. Project Overview



This project is a research-oriented biomedical drug safety evidence intelligence prototype.



It retrieves publicly available adverse-event reports from FDA FAERS through the openFDA API, normalizes and stores evidence, preserves source provenance, and provides descriptive analysis through a FastAPI backend and browser-based research interface.



\*\*Important:\*\* This system is intended for evidence exploration and research support. It is not a medical diagnosis, treatment recommendation, or clinical decision-making system.



### 2. GitHub Repository



Repository: https://github.com/surendray6386157270-eng/biomedical-drug-safety-intelligence



Branch: `main`



Initial implementation commit: `cb4597a`



Repository visibility: Private



Access must be granted to authorized BHIV reviewers.



### 3. Implemented Components



\- FDA FAERS/openFDA source connector

\- Drug-specific adverse-event ingestion pipeline

\- Evidence validation and normalization

\- Deterministic evidence identifiers

\- Source provenance and traceability

\- SQLite evidence storage

\- Drug-specific evidence search

\- Descriptive adverse-reaction analysis

\- FastAPI endpoints and interactive API documentation

\- Browser-based research interface

\- Automated unit and integration tests

\- Architecture and dataset documentation



### 4. Technology Stack



\- Python 3.12

\- FastAPI

\- Pydantic

\- HTTPX

\- SQLite

\- Pytest

\- HTML-based research interface



### 5. Running the Project



Clone the repository and navigate into the project directory.



Create a Python virtual environment and install dependencies:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

python -m pip install -r requirements.txt

```



Start the API server:



```powershell

python -m uvicorn app.main:app --reload

```



Open the following URLs:



\- Research interface: http://127.0.0.1:8000/

\- API documentation: http://127.0.0.1:8000/docs

\- Health endpoint: http://127.0.0.1:8000/health



Run the tests:



```powershell

python -m pytest -q

```



### 6. Validation and Test Results



The latest local automated test execution completed successfully.



\*\*Result: 18 tests passed.\*\*



Verified capabilities include evidence normalization, ingestion, pipeline behavior, search, and descriptive analysis.



Supporting evidence is stored in the `evidence\_packet/` directory.



### 7. Evidence Packet



The repository contains:



\- `evidence\_packet/screenshots/` — research interface, no-evidence handling, API documentation, ingestion, and test execution screenshots.

\- `evidence\_packet/api\_samples/` — sample evidence and analysis API responses.

\- `evidence\_packet/runtime\_logs/` — automated test results and health endpoint verification.

\- `evidence\_packet/deployment\_proof/` — local runtime environment details.



### 8. Scientific and Engineering Limitations



\- FDA FAERS contains spontaneous adverse-event reports.

\- Report frequencies must not be interpreted as population incidence rates.

\- Reported drug-event associations do not establish causation.

\- Data may include incomplete records, duplicates, reporting bias, and other limitations.

\- The current analytics implementation is descriptive; no trained predictive machine-learning model or model-performance evaluation is claimed.

\- Production deployment, authentication, access control, and operational monitoring have not been demonstrated.

\- The system must not be used to make patient-specific medical decisions.



### 9. Documentation



Additional technical information is available in:



\- `README.md`

\- `ARCHITECTURE.md`

\- `docs/dataset\_registry.md`

\- `docs/data\_dictionary.md`



### 10. Handover Status



The prototype implementation, local testing, documentation, evidence packet, and initial GitHub upload are complete.



The project is available in a private repository for authorized review.



Further work may include additional source integrations, analytical evaluation, security hardening, and production deployment, subject to BHIV requirements.

