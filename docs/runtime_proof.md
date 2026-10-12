# Runtime Proof — Biomedical Drug Safety Intelligence System

## 1. Purpose

This document records verified local execution evidence for the biomedical drug safety intelligence prototype.

The demonstrated flow is:

FDA FAERS/openFDA → Retrieval → Normalization → SQLite Evidence Store → Search → Descriptive Analysis → API Result → Evidence Trace.

The proof references actual saved API responses, runtime logs, and screenshots. It does not claim production deployment or clinical validation.

## 2. Execution Environment

- Operating system: Windows
- Python version: 3.12.7
- Backend: FastAPI
- Local application: http://127.0.0.1:8000
- Data source: FDA FAERS through openFDA
- Evidence storage: SQLite

Environment evidence: `evidence_packet/deployment_proof/local_runtime.txt`

## 3. Source Retrieval and Ingestion

The system uses the FDA FAERS/openFDA Drug Adverse Events API.

The project implements source retrieval in `app/connectors/openfda.py` and ingestion orchestration in `app/services/pipeline.py`.

Previously observed local ingestion retrieved 10 source records for the aspirin query. Normalization can produce multiple drug–reaction evidence records from the acquired source records.

The exact source response and ingestion details may vary between runs because the external dataset changes over time.

Supporting evidence:

- `evidence_packet/screenshots/04_ingestion_proof.png`
- `evidence_packet/api_samples/aspirin_evidence.json`

## 4. Validation and Normalization

The pipeline transforms acquired source information into structured evidence.

Relevant implementation files:

- `app/models/evidence.py`
- `app/services/normalization.py`
- `app/services/ingestion.py`

The normalized evidence model supports record identifiers, drug and reaction information, source metadata, schema version, and provenance.

Missing source values must not be fabricated.

## 5. Evidence Storage and Search

Normalized evidence is persisted locally using SQLite.

Evidence retrieval is implemented through:

`GET /api/drugs/{drug_name}/evidence?limit=10`

The saved aspirin evidence response is available at:

`evidence_packet/api_samples/aspirin_evidence.json`

This artifact allows reviewers to inspect stored evidence and source-derived metadata.

## 6. Actual Analytical Execution

**Drug query:** aspirin

**Endpoint:**

`GET /api/drugs/aspirin/analysis?limit=10`

**Analysis type:** `descriptive_drug_reaction_analysis`

**Source:** FDA FAERS / openFDA

### Verified Results

| Metric | Value |
|---|---:|
| Input evidence records | 10 |
| Total analyzed records | 10 |
| Unique reactions | 10 |

### Top Five Reactions

| Reaction | Count | Proportion |
|---|---:|---:|
| Drug hypersensitivity | 1 | 0.1 |
| Cerebrovascular accident | 1 | 0.1 |
| Blood pressure increased | 1 | 0.1 |
| Pain | 1 | 0.1 |
| Hypertension | 1 | 0.1 |

These values were read from the saved analysis response:

`evidence_packet/api_samples/aspirin_analysis.json`

The results represent reaction frequencies within the acquired evidence sample.

They are not population incidence estimates, causal findings, or patient-level risk predictions.

## 7. Evidence Trace and Provenance

The analysis endpoint returns the evidence used to generate the summary.

Relevant source fields and metadata can be inspected in the saved evidence and analysis JSON artifacts.

The evidence model and normalization implementation preserve source record identifiers and provenance information.

Reviewers can trace a displayed reaction back to its normalized evidence record and associated source metadata.

For detailed record-level provenance, inspect:

- `evidence_packet/api_samples/aspirin_evidence.json`
- `evidence_packet/api_samples/aspirin_analysis.json`
- `app/models/evidence.py`
- `app/services/normalization.py`

## 8. Automated Test Evidence

The previously verified automated test execution completed successfully.

**Result: 18 passed.**

Supporting log:

`evidence_packet/runtime_logs/pytest_results.txt`

Test execution screenshot:

`evidence_packet/screenshots/05_test_run.png`

## 9. API Health Check

The local health endpoint returned HTTP 200.

Endpoint:

`GET /health`

Observed response:

```json
{
  "status": "ok",
  "service": "Biomedical Drug Safety Evidence Intelligence System"
}
```

Supporting log:

`evidence_packet/runtime_logs/api_health_check.txt`

## 10. Research Interface Evidence

The browser-based interface is served from `app/ui/index.html`.

Supporting screenshots:

- `01_research_query_aspirin.png` — aspirin research query
- `02_no_evidence_handling.png` — no-evidence handling
- `03_api_documentation.png` — FastAPI API documentation
- `04_ingestion_proof.png` — ingestion execution
- `05_test_run.png` — automated test execution

All screenshots are stored in `evidence_packet/screenshots/`.

## 11. Reproducing the Execution

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python -m uvicorn app.main:app --reload
```

In a separate terminal, ingest aspirin evidence:

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/drugs/aspirin/ingest?limit=10"
```

Retrieve evidence:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/drugs/aspirin/evidence?limit=10"
```

Retrieve analysis:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/drugs/aspirin/analysis?limit=10" | ConvertTo-Json -Depth 12
```

Run tests:

```powershell
python -m pytest -q
```

Because openFDA data changes, a new ingestion may not reproduce the exact same reaction counts. The saved JSON files document the previously observed execution.

## 12. Limitations

- FAERS reports do not establish causality.
- The retrieved sample is small.
- Reaction frequencies are not incidence estimates.
- The analysis is descriptive, not predictive.
- Live source results may change.
- Production deployment has not been demonstrated.
- Clinical validation has not been performed.

## 13. Conclusion

The captured evidence demonstrates a functioning local biomedical data pipeline that retrieves real source data, creates structured evidence, supports search, and generates reproducible descriptive summaries over stored records.

The implementation is suitable for research-oriented prototype evaluation, not clinical decision-making.