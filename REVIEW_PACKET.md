# BHIV Biomedical Drug Safety Intelligence — Review Packet

## 1. Project Summary

This repository contains a biomedical drug safety evidence intelligence prototype built for the BHIV AI/ML Biotech engineering candidate assessment.

The system retrieves real FDA FAERS adverse-event data through openFDA, normalizes the data into structured evidence records, stores the evidence in SQLite, and provides drug-specific search and descriptive adverse-reaction analysis.

The project is a research prototype, not a medical diagnosis or clinical decision-making system.

## 2. Repository and Starting Point

**Repository:** https://github.com/surendray6386157270-eng/biomedical-drug-safety-intelligence

**Branch:** `main`

**Visibility:** Private — reviewers require repository access.

**Start here:**

- `README.md` — overview and setup.
- `REVIEW_INDEX.md` — navigation guide.
- `ARCHITECTURE.md` — system architecture.
- `docs/runtime_proof.md` — captured execution evidence.

## 3. Three Critical Code Files

Review these files first:

1. `app/services/pipeline.py` — coordinates ingestion and analysis.
2. `app/services/normalization.py` — converts source reports into normalized evidence with provenance.
3. `app/analytics/drug_reaction.py` — performs descriptive reaction-frequency analysis.

Additional API, persistence, and schema files are listed in `REVIEW_INDEX.md`.

## 4. Run the System

Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Open the research interface:

`http://127.0.0.1:8000/`

Open the API documentation:

`http://127.0.0.1:8000/docs`

## 5. Demonstrate the Complete Flow

In a second PowerShell terminal, ingest real aspirin data:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/drugs/aspirin/ingest?limit=10"
```

Retrieve stored evidence:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/drugs/aspirin/evidence?limit=10"
```

Execute descriptive analysis:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/drugs/aspirin/analysis?limit=10" | ConvertTo-Json -Depth 12
```

The demonstrated flow is:

FDA FAERS/openFDA → Retrieval → Normalization → Provenance → SQLite Storage → Search → Descriptive Analysis → Result.

Live results may differ from saved samples because the external dataset changes.

## 6. Captured Analytical Result

The saved aspirin analysis returned:

| Metric | Verified result |
|---|---|
| Drug | aspirin |
| Analysis type | descriptive_drug_reaction_analysis |
| Evidence records analyzed | 10 |
| Unique reactions | 10 |
| Source | FDA FAERS / openFDA |

Five reported reactions in the captured sample were:

| Reaction | Count | Proportion |
|---|---:|---:|
| Drug hypersensitivity | 1 | 0.1 |
| Cerebrovascular accident | 1 | 0.1 |
| Blood pressure increased | 1 | 0.1 |
| Pain | 1 | 0.1 |
| Hypertension | 1 | 0.1 |

The source artifact is:

`evidence_packet/api_samples/aspirin_analysis.json`

These are within-sample frequencies, not population incidence estimates or causal conclusions.

## 7. Evidence and Provenance

The evidence schema and normalization service preserve source-related metadata, identifiers, and provenance.

The analysis response includes supporting evidence records.

Inspect:

- `app/models/evidence.py`
- `app/services/normalization.py`
- `evidence_packet/api_samples/aspirin_evidence.json`
- `evidence_packet/api_samples/aspirin_analysis.json`

This allows reviewers to distinguish source-derived records from computed summaries.

## 8. Automated Test Evidence

Run:

```powershell
python -m pytest -q
```

Previously captured result: **18 passed**.

Proof:

- `evidence_packet/runtime_logs/pytest_results.txt`
- `evidence_packet/screenshots/05_test_run.png`

## 9. Runtime Evidence

- `docs/runtime_proof.md` — full execution narrative.
- `evidence_packet/screenshots/01_research_query_aspirin.png` — research interface.
- `evidence_packet/screenshots/02_no_evidence_handling.png` — empty results.
- `evidence_packet/screenshots/03_api_documentation.png` — Swagger documentation.
- `evidence_packet/screenshots/04_ingestion_proof.png` — ingestion.
- `evidence_packet/runtime_logs/api_health_check.txt` — health check.
- `evidence_packet/deployment_proof/local_runtime.txt` — local runtime environment.

No production deployment is claimed.

## 10. Changes Delivered

The implementation includes:

- Real biomedical source integration.
- Structured evidence normalization and provenance.
- Local persistence and drug-specific search.
- Descriptive reaction-frequency analysis.
- FastAPI endpoints and research interface.
- Automated tests.
- Documentation, experiment records, and captured runtime evidence.

Change history: `CHANGELOG.md`

## 11. Failure Cases and Limitations

The system is designed to handle empty evidence and upstream source failures, although not every possible production failure mode has been validated.

Important limitations:

- FAERS is subject to reporting bias and incomplete data.
- Reaction frequency does not establish causation.
- The captured sample is small.
- The system does not estimate clinical risk or incidence.
- No predictive ML model is implemented.
- No production deployment or clinical validation is demonstrated.

## 12. Reproducibility

For the experiment design and reproduction steps, see:

- `docs/experiment.md`
- `docs/runtime_proof.md`
- `HANDOVER.md`

For the source schema and dataset information, see:

- `docs/data_dictionary.md`
- `docs/dataset_registry.md`

## 13. AI-Assisted Development

AI assistance was used during implementation and documentation.

The disclosure and verification approach are recorded in:

`docs/ai_usage.md`

## 14. Reviewer Conclusion

The project demonstrates a locally functioning, source-grounded biomedical evidence pipeline with structured provenance, searchable evidence, and descriptive analytical output.

Its intended use is research-oriented prototype evaluation. Production and clinical use would require additional scientific, security, and operational validation.
