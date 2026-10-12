# Code Review Packet — Biomedical Drug Safety Intelligence System

## 1. Purpose

This index identifies the key implementation files for reviewing the biomedical drug safety intelligence prototype.

The source files remain in their original repository locations. This index links to them rather than duplicating code.

## 2. Three Priority Files

Review these three files first.

### 1. Pipeline Orchestration

**File:** `../../app/services/pipeline.py`

**Purpose:** Coordinates retrieval, ingestion, evidence storage, and analysis.

**Review focus:**
- How a drug query enters the pipeline.
- How source retrieval and evidence processing are coordinated.
- How ingestion results are returned.
- How failures are handled.

### 2. Evidence Normalization

**File:** `../../app/services/normalization.py`

**Purpose:** Converts FDA FAERS source records into normalized evidence records.

**Review focus:**
- Source field extraction.
- Drug and reaction normalization.
- Deterministic evidence identifiers.
- Source provenance preservation.
- Handling of incomplete source records.

### 3. Descriptive Analytics

**File:** `../../app/analytics/drug_reaction.py`

**Purpose:** Computes drug–reaction frequency summaries from normalized evidence.

**Review focus:**
- Reaction counting.
- Unique reaction calculation.
- Within-sample proportions.
- Empty evidence handling.
- Scientific limitations.

## 3. Supporting Implementation

| Component | Source file |
|---|---|
| FDA FAERS connector | `../../app/connectors/openfda.py` |
| Evidence schema | `../../app/models/evidence.py` |
| Ingestion service | `../../app/services/ingestion.py` |
| SQLite repository | `../../app/db/repositories.py` |
| Evidence search | `../../app/services/search.py` |
| Analysis service | `../../app/services/analysis.py` |
| FastAPI entry point | `../../app/main.py` |
| Research interface | `../../app/ui/index.html` |

## 4. Source-to-Result Trace

The implementation follows this sequence:

1. Retrieve real adverse-event data through openFDA.
2. Normalize source records into structured evidence.
3. Preserve source identifiers and provenance.
4. Persist evidence in SQLite.
5. Retrieve drug-specific evidence.
6. Compute descriptive reaction-frequency summaries.
7. Return results and supporting evidence through the API.
8. Display source evidence separately from derived analysis.

## 5. Tests

Automated tests are located in:

`../../tests/`

Run from the repository root:

```powershell
python -m pytest -q
```

Previously captured result: **18 passed**.

Test evidence:

`../runtime_logs/pytest_results.txt`

## 6. Captured API Outputs

Saved evidence response:

`../api_samples/aspirin_evidence.json`

Saved analysis response:

`../api_samples/aspirin_analysis.json`

The captured aspirin analysis contains 10 evidence records and 10 distinct reaction terms.

## 7. Documentation References

- `../../README.md` — installation and project overview.
- `../../ARCHITECTURE.md` — architecture.
- `../../INTEGRATION.md` — integration instructions.
- `../../REVIEW_INDEX.md` — reviewer navigation.
- `../../REVIEW_PACKET.md` — main review packet.
- `../../docs/experiment.md` — analytical experiment.
- `../../docs/runtime_proof.md` — runtime evidence.
- `../../docs/data_dictionary.md` — evidence fields.
- `../review_packet.md` — evidence packet index.

## 8. Scientific and Engineering Boundaries

The implementation performs descriptive analysis over acquired FAERS evidence.

Reaction counts are not population incidence rates, and reported associations do not establish causation.

The project does not implement predictive clinical risk estimation, diagnosis, or treatment recommendations.

## 9. Suggested Review Sequence

1. Read the three priority files.
2. Inspect the evidence schema and source connector.
3. Trace the ingestion and storage flow.
4. Review the analysis service and API.
5. Run automated tests.
6. Inspect captured API outputs.
7. Reproduce a live aspirin ingestion and analysis.

## 10. Conclusion

The code packet provides a focused path through the implementation, connecting source ingestion, normalized evidence, provenance, persistence, descriptive analytics, and reviewer-verifiable outputs.
