# Biomedical Drug Safety Intelligence — Evidence Review Packet

## 1. Purpose

This packet identifies the saved artifacts supporting the BHIV biomedical drug safety intelligence prototype.

The evidence demonstrates local execution of real biomedical data retrieval, normalization, storage, search, descriptive analysis, and automated testing.

The packet does not claim production deployment or clinical validation.

## 2. System Under Review

**Project:** Biomedical Drug Safety Intelligence & ML Evidence System

**Repository:** https://github.com/surendray6386157270-eng/biomedical-drug-safety-intelligence

**Source:** FDA FAERS / openFDA

**Backend:** Python, FastAPI

**Storage:** SQLite

**Analysis:** Descriptive drug–reaction frequency analysis

## 3. Evidence Artifact Index

| Artifact | Location | Purpose |
|---|---|---|
| Aspirin research screenshot | `screenshots/01_research_query_aspirin.png` | Demonstrates research interface |
| No-evidence screenshot | `screenshots/02_no_evidence_handling.png` | Demonstrates empty-result presentation |
| API documentation screenshot | `screenshots/03_api_documentation.png` | Shows available API endpoints |
| Ingestion screenshot | `screenshots/04_ingestion_proof.png` | Captures ingestion execution |
| Test screenshot | `screenshots/05_test_run.png` | Captures automated test execution |
| Aspirin evidence JSON | `api_samples/aspirin_evidence.json` | Saved normalized evidence |
| Aspirin analysis JSON | `api_samples/aspirin_analysis.json` | Saved analytical result |
| Test log | `runtime_logs/pytest_results.txt` | Automated test output |
| Health-check log | `runtime_logs/api_health_check.txt` | Local API health verification |
| Local runtime record | `deployment_proof/local_runtime.txt` | Local execution environment |

All paths in this table are relative to `evidence_packet/`.

## 4. Verified Analytical Output

The saved aspirin analysis response contains:

| Field | Observed value |
|---|---|
| Drug | aspirin |
| Analysis type | descriptive_drug_reaction_analysis |
| Input evidence count | 10 |
| Total analyzed records | 10 |
| Unique reactions | 10 |
| Source | FDA FAERS / openFDA |

The top five reaction entries are:

| Reaction | Count | Proportion |
|---|---:|---:|
| Drug hypersensitivity | 1 | 0.1 |
| Cerebrovascular accident | 1 | 0.1 |
| Blood pressure increased | 1 | 0.1 |
| Pain | 1 | 0.1 |
| Hypertension | 1 | 0.1 |

These proportions are calculated over the acquired evidence sample. They do not represent clinical incidence or establish causation.

## 5. Provenance and Traceability

The saved evidence JSON contains normalized records with source-related metadata.

The saved analysis JSON includes supporting evidence alongside derived analytical results.

Reviewers can inspect these files to distinguish source-derived information from system-generated summaries.

Relevant implementation:

- `../app/models/evidence.py`
- `../app/services/normalization.py`
- `../app/services/pipeline.py`
- `../app/analytics/drug_reaction.py`

## 6. Test Evidence

The previously recorded local test execution completed with:

**18 passed**

The captured output is stored in:

`runtime_logs/pytest_results.txt`

A screenshot of the test run is stored in:

`screenshots/05_test_run.png`

Tests should be rerun against the current checkout before making new validation claims.

## 7. Local Runtime Proof

The local application health endpoint returned HTTP 200.

Evidence:

`runtime_logs/api_health_check.txt`

The runtime environment is described in:

`deployment_proof/local_runtime.txt`

This is local execution evidence, not proof of a publicly deployed service.

## 8. Reproduction

From the repository root, install dependencies and start the application:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

In another PowerShell terminal, run:

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

Run automated tests:

```powershell
python -m pytest -q
```

The saved response files document an earlier execution. Live source responses may change.

## 9. Failure and Limitation Evidence

The no-evidence screenshot demonstrates the user interface's presentation of an empty result.

The test suite provides additional automated verification, with individual cases available in `tests/`.

This packet does not assert that every production failure mode has been tested.

## 10. Scientific Limitations

- FAERS reports are subject to reporting bias and incomplete information.
- Report frequency does not measure population incidence.
- A reported association does not establish causation.
- The captured analysis uses a small sample.
- No predictive risk model is implemented.
- No independent clinical validation has been performed.

## 11. Review Order

1. Inspect `api_samples/aspirin_analysis.json`.
2. Inspect the corresponding evidence records.
3. Review the screenshots and runtime logs.
4. Read `../docs/runtime_proof.md`.
5. Examine the implementation files listed in `code_packet/INDEX.md`.
6. Reproduce the API flow and automated tests.

## 12. Conclusion

The collected artifacts support review of a locally executed biomedical evidence intelligence prototype using real FDA FAERS/openFDA data.

The packet provides a traceable record of the captured outputs, while explicitly distinguishing prototype functionality from production or clinical readiness.