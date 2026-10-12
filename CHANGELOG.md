# Changelog

All notable project changes are documented here.

## [0.1.0] — 2026-10-12

### Added

- Initial biomedical drug safety evidence intelligence prototype.
- FDA FAERS/openFDA connector for real adverse-event data retrieval.
- Evidence validation and normalization.
- Versioned evidence schema and provenance metadata.
- Deterministic evidence identifiers.
- SQLite evidence storage and duplicate handling.
- Drug-specific evidence search.
- Descriptive adverse-drug-reaction frequency analysis.
- Reaction counts, proportions, and scientific limitations.
- FastAPI ingestion, evidence, analysis, and health endpoints.
- Browser-based research interface.
- Automated tests for core system components.
- Dataset registry and data dictionary.
- Architecture and installation documentation.
- Screenshots, API response samples, and runtime logs.
- Experiment documentation and AI-assisted development disclosure.
- Integration guide and engineering handover.

### Validation

- 18 automated tests passed during local verification.
- Aspirin evidence and descriptive analysis responses captured.
- Local API health endpoint returned HTTP 200.
- Source code and initial submission documentation pushed to the private GitHub repository.

### Known Limitations

- Analysis is descriptive, not predictive machine learning.
- FAERS report frequencies do not establish causation or incidence.
- Production deployment and clinical validation have not been demonstrated.
- Authentication, authorization, and large-scale performance validation remain future work.

### Repository History

- `cb4597a` — Initial implementation of biomedical drug safety intelligence system.
- `d8ba0fb` — Add BHIV project submission and handover documentation.

Additional documentation prepared after these commits will be included in a subsequent commit.
