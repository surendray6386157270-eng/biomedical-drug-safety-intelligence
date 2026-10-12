# BHIV Biomedical Drug Safety Intelligence — Review Index

## 1. Project Entry Point

**Repository:** https://github.com/surendray6386157270-eng/biomedical-drug-safety-intelligence

**Branch:** `main`

**Visibility:** Private — reviewer access must be granted.

**Application entry point:** `app/main.py`

**Research interface:** `app/ui/index.html`

**Setup instructions:** `README.md` and `HANDOVER.md`

## 2. Core Implementation

| Component | File |
|---|---|
| FDA FAERS/openFDA connector | `app/connectors/openfda.py` |
| Versioned evidence schema | `app/models/evidence.py` |
| Evidence normalization | `app/services/normalization.py` |
| Ingestion pipeline | `app/services/pipeline.py` |
| SQLite persistence | `app/db/repositories.py` |
| Drug evidence search | `app/services/search.py` |
| Descriptive analytics | `app/analytics/drug_reaction.py` |
| Analysis service | `app/services/analysis.py` |
| FastAPI application | `app/main.py` |
| Research interface | `app/ui/index.html` |

## 3. Core Execution Flow

FDA FAERS/openFDA → Source Connector → Normalization → Evidence Storage → Drug Search → Descriptive Analysis → API/Research Interface → Provenance

The three recommended files for an initial code review are:

1. `app/services/pipeline.py` — pipeline orchestration.
2. `app/services/normalization.py` — source-to-evidence transformation.
3. `app/analytics/drug_reaction.py` — analytical implementation.

## 4. API Endpoints

- `GET /health` — application health.
- `POST /api/drugs/{drug_name}/ingest` — retrieve and ingest source evidence.
- `GET /api/drugs/{drug_name}/evidence` — search stored evidence.
- `GET /api/drugs/{drug_name}/analysis` — retrieve descriptive analysis and supporting evidence.

Interactive API documentation: `http://127.0.0.1:8000/docs`

## 5. Analytics Experiment

**Method:** Descriptive adverse-drug-reaction frequency analysis.

**Implementation:** `app/analytics/drug_reaction.py`

**Experiment documentation:** `docs/experiment.md`

**Captured result:** `evidence_packet/api_samples/aspirin_analysis.json`

The saved aspirin analysis contains 10 input evidence records and 10 unique reaction terms.

This analysis does not establish incidence, causation, or patient-specific risk.

## 6. Automated Tests

Test files are located in `tests/`.

Run:

`python -m pytest -q`

Previously verified result: **18 passed**.

Supporting evidence:

- `evidence_packet/runtime_logs/pytest_results.txt`
- `evidence_packet/screenshots/05_test_run.png`

## 7. Runtime and API Evidence

| Evidence | Location |
|---|---|
| Aspirin evidence response | `evidence_packet/api_samples/aspirin_evidence.json` |
| Aspirin analysis response | `evidence_packet/api_samples/aspirin_analysis.json` |
| API health check | `evidence_packet/runtime_logs/api_health_check.txt` |
| Local runtime details | `evidence_packet/deployment_proof/local_runtime.txt` |
| Complete runtime narrative | `docs/runtime_proof.md` |

## 8. Screenshots

All screenshots are stored in `evidence_packet/screenshots/`.

- `01_research_query_aspirin.png` — research query.
- `02_no_evidence_handling.png` — empty result handling.
- `03_api_documentation.png` — API documentation.
- `04_ingestion_proof.png` — ingestion execution.
- `05_test_run.png` — test execution.

## 9. Required Documentation

- `README.md` — overview and setup.
- `ARCHITECTURE.md` — system architecture.
- `INTEGRATION.md` — integration guidance.
- `HANDOVER.md` — developer handover.
- `CHANGELOG.md` — change history.
- `REVIEW_PACKET.md` — reviewer summary.
- `docs/learning_notes.md` — domain and engineering learning.
- `docs/experiment.md` — analytical experiment.
- `docs/data_dictionary.md` — evidence field definitions.
- `docs/dataset_registry.md` — dataset discovery.
- `docs/runtime_proof.md` — verified execution.
- `docs/ai_usage.md` — AI-assisted development disclosure.
- `docs/SUBMISSION.md` — submission overview.

## 10. Evidence Packet

The `evidence_packet/` directory contains screenshots, saved API samples, runtime logs, local deployment proof, and reviewer-facing code references.

See:

- `evidence_packet/review_packet.md`
- `evidence_packet/code_packet/INDEX.md`

## 11. Scientific Limitations

FAERS is a spontaneous adverse-event reporting system. Reports may contain incomplete data, duplicates, and reporting bias.

Observed frequencies are descriptive summaries of acquired evidence, not population incidence rates.

The system does not establish causation, diagnose patients, recommend treatment, or determine whether a drug is safe or unsafe.

## 12. Review Recommendation

Start with `README.md`, then inspect the three core implementation files, run the tests, reproduce an aspirin query, and compare the returned evidence with the captured API samples and runtime proof.

The implementation is a research prototype. Production deployment and independent clinical validation have not been demonstrated.
