# Engineering Handover — Biomedical Drug Safety Intelligence System

## 1. Project Overview

This repository contains a research-oriented biomedical drug safety evidence intelligence prototype developed for the BHIV AI/ML Biotech candidate assessment.

The system retrieves real FDA FAERS reports through openFDA, transforms them into structured evidence, preserves provenance, stores evidence in SQLite, and provides drug-specific search and descriptive adverse-reaction analysis.

It is not a diagnosis, treatment recommendation, or clinical decision-making system.

## 2. Repository

Repository: https://github.com/surendray6386157270-eng/biomedical-drug-safety-intelligence

Branch: `main`

Visibility: Private. Authorized reviewers require access.

## 3. Requirements

- Python 3.12
- Internet access for live openFDA ingestion
- Git
- Dependencies listed in `requirements.txt`

The project has been tested locally on Windows.

## 4. Installation

Clone the repository:

```powershell
git clone https://github.com/surendray6386157270-eng/biomedical-drug-safety-intelligence.git
cd biomedical-drug-safety-intelligence
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## 5. Start the Application

Run:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- Research interface: http://127.0.0.1:8000/
- Swagger documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## 6. Retrieve Real Biomedical Data

Open a second PowerShell terminal in the project directory.

Activate the environment if necessary.

Run:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/drugs/aspirin/ingest?limit=10"
```

This requests FDA FAERS/openFDA data and processes the retrieved records.

Live source results can change over time.

## 7. Search Evidence

Run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/drugs/aspirin/evidence?limit=10"
```

The endpoint returns normalized evidence already stored locally.

An empty response does not establish that a drug has no reported adverse events.

## 8. Execute Analysis

Run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/drugs/aspirin/analysis?limit=10" | ConvertTo-Json -Depth 12
```

The descriptive analysis provides:

- Total evidence record count
- Number of distinct reaction terms
- Top reported reactions
- Reaction counts
- Within-sample proportions
- Scientific limitations
- Supporting evidence

The analysis is not predictive ML and does not estimate population incidence or clinical risk.

## 9. Reproduce the Captured Experiment

The saved experiment is documented in `docs/experiment.md`.

Captured results are available in:

- `evidence_packet/api_samples/aspirin_evidence.json`
- `evidence_packet/api_samples/aspirin_analysis.json`

The saved aspirin analysis contains 10 evidence records and 10 distinct reaction terms.

Live retrieval may produce different results because openFDA data can change.

## 10. Run Automated Tests

Run:

```powershell
python -m pytest -q
```

The previously verified test suite completed with 18 passing tests.

Recorded output:

`evidence_packet/runtime_logs/pytest_results.txt`

The test suite should be rerun after any code modifications.

## 11. Important Source Files

| File | Responsibility |
|---|---|
| `app/connectors/openfda.py` | Source retrieval |
| `app/models/evidence.py` | Evidence schema |
| `app/services/normalization.py` | Evidence normalization |
| `app/services/pipeline.py` | Pipeline orchestration |
| `app/db/repositories.py` | Evidence persistence and retrieval |
| `app/services/search.py` | Drug-specific evidence search |
| `app/analytics/drug_reaction.py` | Descriptive analytics |
| `app/services/analysis.py` | Analytics service |
| `app/main.py` | Application entry point |
| `app/ui/index.html` | Research interface |

## 12. Configuration and Storage

The current implementation uses local SQLite storage.

The generated database is excluded from Git using `.gitignore`.

No production secrets or external API credentials are required for the documented public openFDA workflow.

Review the database configuration in `app/db/database.py` before deploying or changing storage behavior.

## 13. Evidence and Provenance

Evidence records include source-related metadata, record identifiers, retrieval information, and schema version information.

Review:

- `docs/data_dictionary.md`
- `docs/runtime_proof.md`
- `evidence_packet/api_samples/`

Derived analysis must remain distinguishable from source evidence.

## 14. Failure Handling

The system includes handling for empty results, invalid requests, source errors, and missing analytical input.

For troubleshooting:

1. Confirm the Python environment is active.
2. Check the health endpoint.
3. Check network access to openFDA.
4. Review the error returned by the API.
5. Run the automated tests.
6. Inspect stored evidence before interpreting an empty analysis.

## 15. Adding Another Source

The implementation currently integrates FDA FAERS/openFDA.

To add another source:

1. Create a connector in `app/connectors/`.
2. Implement retrieval and error handling.
3. Define source-specific validation and normalization.
4. Preserve source identifiers and provenance.
5. Integrate the connector into the pipeline.
6. Add automated tests.
7. Update the dataset registry, data dictionary, and documentation.

Additional source integrations require implementation and validation.

## 16. Known Limitations

- FAERS is a spontaneous reporting system with reporting bias.
- Reaction frequencies do not establish causation or incidence.
- Exact reaction-string counting does not harmonize synonymous terminology.
- SQLite is suitable for the prototype but has not been validated for large-scale deployment.
- Authentication and authorization are not implemented.
- Production deployment has not been demonstrated.
- Predictive ML and independent clinical validation are not implemented.

## 17. Pending Work

Before production adoption, the team should consider:

- Domain-expert review of the analysis
- Drug and reaction terminology harmonization
- Larger-scale ingestion and performance testing
- Authentication and access control
- Monitoring and deployment automation
- Expanded data-quality evaluation
- Additional biomedical source integrations

These are future engineering tasks, not capabilities claimed by the current prototype.

## 18. Handover References

- `README.md`
- `ARCHITECTURE.md`
- `INTEGRATION.md`
- `docs/experiment.md`
- `docs/learning_notes.md`
- `docs/ai_usage.md`
- `docs/runtime_proof.md`
- `evidence_packet/`

## 19. Handover Summary

The repository contains an implemented and locally tested biomedical evidence intelligence prototype.

A developer can install the dependencies, run the API and interface, ingest real FDA FAERS data, search stored evidence, execute descriptive analysis, and inspect the supporting evidence.

The system remains a research prototype and requires further scientific and operational validation before production use.