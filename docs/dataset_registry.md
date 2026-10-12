# Dataset Discovery & Registry

## 1. Purpose

This document records the biomedical data sources evaluated for the Biomedical Drug Safety Evidence Intelligence System.

The purpose of the discovery stage is to identify a real, credible, reproducible biomedical source that can support:

* drug safety evidence retrieval
* adverse-event/reaction analysis
* provenance tracking
* reproducible ingestion
* researcher-facing search
* analytical/ML experimentation

The primary source selected for the prototype is **FDA Adverse Event Reporting System (FAERS) data through the openFDA API**.

---

## 2. Source Evaluation

| Source                                  | Owner                                                      | Primary Purpose                                           | Access                                            | Data Type                                        | Identifier                                      | Access Classification          | Integration Difficulty | Research Value |
| --------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------ | ----------------------------------------------- | ------------------------------ | ---------------------- | -------------- |
| FDA FAERS / openFDA Drug Adverse Events | U.S. FDA                                                   | Post-market adverse event and medication error reporting  | Public REST API                                   | Structured JSON adverse-event reports            | FDA/source record identifiers and report fields | AVAILABLE NOW                  | Medium                 | Very High      |
| DailyMed                                | U.S. National Library of Medicine / FDA labeling ecosystem | Current drug labeling information                         | Public REST services / downloads                  | Structured drug-label information                | SPL/set identifiers and drug names              | AVAILABLE NOW                  | Medium                 | High           |
| PubMed / NCBI                           | U.S. National Library of Medicine                          | Biomedical literature and citations                       | Public E-utilities API / FTP                      | Bibliographic records, abstracts and identifiers | PMID                                            | AVAILABLE NOW                  | Medium                 | High           |
| ClinicalTrials.gov                      | U.S. National Library of Medicine                          | Clinical study registration and results                   | Public API / downloads                            | Clinical study metadata and results              | NCT number                                      | AVAILABLE NOW                  | Medium                 | High           |
| WHO VigiBase / VigiAccess               | WHO / Uppsala Monitoring Centre                            | Global pharmacovigilance and adverse-reaction information | VigiAccess/API; full data has access restrictions | Aggregated/global pharmacovigilance data         | Drug/reaction/report dimensions                 | REQUIRES ACCESS / RESTRICTIONS | High                   | Very High      |

---

## 3. Candidate Source Details

### 3.1 FDA FAERS / openFDA

**Owner:** U.S. Food and Drug Administration (FDA)

**Purpose:**
FAERS contains adverse-event and medication-error reports submitted to the FDA. openFDA exposes FDA datasets through an API and provides a Drug Adverse Event endpoint for querying adverse-event records.

**Access method:**
Public HTTPS REST API.

**Data format:**
JSON.

**Potential identifiers:**
Source report identifiers and structured fields contained in the adverse-event record.

**Potential use in this project:**

* drug-level evidence retrieval
* adverse-event/reaction extraction
* reaction frequency analysis
* temporal analysis
* evidence provenance
* analytical/ML experimentation

**Strengths:**

* Directly relevant to drug safety.
* Publicly accessible.
* Machine-readable API.
* Structured adverse-event records.
* Suitable for building a real ingestion pipeline.
* Supports fielded queries.
* Strong fit with the assignment's drug-safety objective.

**Limitations:**

* Reports are spontaneous safety reports and should not be interpreted as proof of causation.
* Reporting frequency cannot by itself establish incidence or risk.
* Data quality and completeness can vary between reports.
* openFDA explicitly cautions that its data should not be used to make medical-care decisions.
* External source data can change over time.

**Integration difficulty:** Medium.

**Research value:** Very High.

**Classification:** `AVAILABLE NOW`

**Selection decision:** **PRIMARY SOURCE**

---

### 3.2 DailyMed

**Owner:** National Library of Medicine (NLM)

**Purpose:**
DailyMed provides the most recent labeling submitted to the FDA and currently in use for drugs and other regulated products.

**Access method:**
Public web services and downloadable data.

**Data format:**
JSON/XML and downloadable labeling resources.

**Potential identifiers:**

* drug names
* Structured Product Labeling (SPL) identifiers
* labeling-related identifiers

**Potential use in this project:**

* drug identity/context enrichment
* label-based evidence
* comparison between reported events and labeled information
* future evidence enrichment

**Strengths:**

* Official biomedical/regulatory source.
* Public access.
* Structured drug-label information.
* Useful for future contextual enrichment.

**Limitations:**

* It is primarily a labeling source rather than an adverse-event reporting database.
* More complex document/label structures would increase normalization work.
* It does not directly provide the same type of spontaneous adverse-event evidence as FAERS.

**Integration difficulty:** Medium.

**Research value:** High.

**Classification:** `AVAILABLE NOW`

**Selection decision:** Secondary/future enrichment source.

---

### 3.3 PubMed / NCBI

**Owner:** National Library of Medicine (NLM) / National Center for Biotechnology Information (NCBI)

**Purpose:**
PubMed provides access to biomedical literature citations and related bibliographic information.

**Access method:**
NCBI E-utilities API and FTP/download resources.

**Data format:**
XML/API responses and downloadable data.

**Primary identifier:** PMID.

**Potential use in this project:**

* literature evidence retrieval
* drug safety literature discovery
* evidence enrichment
* future literature-based similarity or retrieval analysis

**Strengths:**

* Large biomedical literature resource.
* Public programmatic access.
* Stable identifiers.
* Strong potential for evidence enrichment.

**Limitations:**

* Literature evidence is different from spontaneous safety-report evidence.
* Natural-language processing would introduce additional complexity.
* Full literature ingestion is substantially larger than the initial prototype scope.
* API usage has rate-control considerations.

**Integration difficulty:** Medium.

**Research value:** High.

**Classification:** `AVAILABLE NOW`

**Selection decision:** Secondary/future evidence source.

---

### 3.4 ClinicalTrials.gov

**Owner:** U.S. National Library of Medicine

**Purpose:**
ClinicalTrials.gov provides information about clinical studies, including study identifiers, status, conditions, interventions and available results.

**Access method:**
Public API and downloadable data.

**Data format:**
Structured API/download data.

**Primary identifier:** NCT number.

**Potential use in this project:**

* clinical-study evidence enrichment
* drug/intervention context
* study-status analysis
* future comparison with post-market safety evidence

**Strengths:**

* Public structured data.
* Stable NCT identifiers.
* Strong biomedical research value.
* Useful for understanding study-level evidence.

**Limitations:**

* Clinical trial records are not equivalent to spontaneous adverse-event reports.
* Different evidence model from FAERS.
* Combining it directly with FAERS would require careful evidence-type separation.

**Integration difficulty:** Medium.

**Research value:** High.

**Classification:** `AVAILABLE NOW`

**Selection decision:** Secondary/future source.

---

### 3.5 WHO VigiBase / VigiAccess

**Owner:** World Health Organization / Uppsala Monitoring Centre

**Purpose:**
VigiBase is a global database of reported adverse reactions to medicines and vaccines.

**Access method:**
VigiAccess provides public summarized information. More detailed VigiBase data has access and licensing restrictions.

**Data type:**
Global pharmacovigilance data and aggregated safety information.

**Potential use in this project:**

* global pharmacovigilance comparison
* future external validation/context
* international safety-signal research

**Strengths:**

* Very large global pharmacovigilance resource.
* International coverage.
* High scientific relevance to drug safety.

**Limitations:**

* Full VigiBase case-level access is restricted.
* Access may require organizational eligibility, approval or licensing.
* VigiAccess provides a summarized representation rather than unrestricted case-level data.
* Less suitable for a reproducible first prototype than an openly accessible API such as openFDA.

**Integration difficulty:** High.

**Research value:** Very High.

**Classification:** `REQUIRES ACCESS / RESTRICTIONS`

**Selection decision:** Not selected for the initial implementation.

---

## 4. Primary Source Selection

### Selected Source

**FDA FAERS through the openFDA Drug Adverse Event API**

### Selection Rationale

FAERS/openFDA is selected because it provides the closest match to the central objective of this prototype: building a traceable drug-safety evidence system from real biomedical adverse-event data.

The source provides:

1. Direct drug-safety relevance.
2. Public programmatic access.
3. Structured machine-readable records.
4. Searchable adverse-event fields.
5. Evidence that can be normalized into the project's internal schema.
6. Source records that can be retained for provenance.
7. Data suitable for descriptive analytical and ML experimentation.

The openFDA documentation confirms that the Drug Adverse Event endpoint returns adverse-event records containing information such as drugs and reactions, and supports field-based searching.

---

## 5. Planned Evidence Flow

```text
FDA FAERS / openFDA
        |
        v
Source Connector
        |
        v
Raw API Response
        |
        v
Validation
        |
        v
Normalization
        |
        v
Provenance Metadata
        |
        v
Evidence Store
        |
        +--------------------+
        |                    |
        v                    v
Research Search        Analytics / ML
        |                    |
        +---------+----------+
                  |
                  v
             API Result
                  |
                  v
        Evidence + Analysis
        + Provenance Trace
```

---

## 6. Source Limitations

The system must preserve the distinction between:

* a report existing in the source
* the frequency of reports
* an observed association in the acquired dataset
* a causal safety conclusion

The prototype will **not** interpret FAERS report counts as incidence, causation, clinical risk, or proof that a drug is safe or unsafe.

All analytical outputs will be presented as system-generated analysis over the acquired evidence.

---

## 7. Future Source Expansion

The architecture should allow additional evidence sources without coupling source-specific retrieval logic to the research interface.

Potential future integrations:

* DailyMed for labeling evidence
* PubMed for biomedical literature
* ClinicalTrials.gov for clinical-study evidence
* WHO VigiAccess/VigiBase where access permits

Each source should retain its own source identity and evidence type so that incompatible evidence is not silently merged.

---

## 8. Current Decision

**Primary implementation source:** FDA FAERS via openFDA

**Initial implementation status:** Selected

**Next engineering step:** Implement the source connector and deterministic fixture-based ingestion tests.

---

## References

* FDA openFDA datasets and FAERS information.
* FDA openFDA Drug Adverse Event API documentation.
* NLM DailyMed web services and data documentation.
* NCBI PubMed/E-utilities documentation.
* ClinicalTrials.gov data/API documentation.
* WHO/UMC VigiBase and VigiAccess documentation.
