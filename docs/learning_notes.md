# Learning Notes — Biomedical Drug Safety Intelligence System



## 1. Project Learning Objective



Understand how to build a reproducible biomedical evidence intelligence pipeline using publicly available drug safety data.



The focus is on source integration, data validation, normalization, provenance, descriptive analytics, testing, and scientific limitations.



## 2. Biomedical Data Source



**Selected source:** FDA Adverse Event Reporting System (FAERS), accessed through the openFDA API.



FAERS contains adverse-event reports involving drugs. It supports exploratory pharmacovigilance research but does not independently establish drug-related causation.



The project uses the openFDA Drug Adverse Events API to retrieve source records.



## 3. Important Domain Concepts



\- **Pharmacovigilance:** Detection, assessment, understanding, and prevention of adverse effects or other medicine-related problems.

\- **Adverse event:** An undesirable medical occurrence reported in association with drug use, without necessarily establishing causation.

\- **Drug–reaction relationship:** A reported association between a medicinal product and a reaction.

\- **Provenance:** Information identifying the source record, retrieval time, and transformations associated with evidence.

\- **Reporting bias:** Differences in which adverse events are reported and captured.

\- **Missing data:** Fields that may be absent or incomplete in source reports.



## 4. Engineering Concepts Learned



The implementation demonstrates:



1\. Retrieving real biomedical data through an external API.

2\. Handling network and source-response failures.

3\. Validating and normalizing incoming records.

4\. Creating deterministic evidence identifiers.

5\. Preserving source metadata and evidence provenance.

6\. Storing structured evidence in SQLite.

7\. Retrieving drug-specific evidence.

8\. Performing descriptive reaction-frequency analysis.

9\. Exposing evidence and analysis through FastAPI.

10\. Testing individual components and the pipeline.



## 5. AI-Assisted Learning and Development



GPT-based assistance was used to help plan the implementation, explain biomedical data limitations, develop and debug Python code, prepare documentation, and organize testing and evidence collection.



AI-generated explanations and code suggestions were treated as development assistance rather than independent scientific verification.



The candidate remains responsible for validating the implementation and understanding its limitations.



Further details are recorded in `docs/ai\_usage.md`.



## 6. Verification Evidence



The following activities were demonstrated during development:



\- Successful retrieval of FDA FAERS data through openFDA.

\- Local execution of the ingestion and evidence-storage pipeline.

\- Retrieval of aspirin evidence through the API.

\- Execution of descriptive drug–reaction analysis.

\- Browser access to the research interface and API documentation.

\- Automated test execution with 18 passing tests.

\- Capture of API responses, screenshots, and runtime logs.



Supporting artifacts are stored in `evidence\_packet/`.



These checks verify local software behavior; they do not constitute independent clinical validation of FAERS reports.



## 7. Technical Decisions



**Source selection:** FDA FAERS/openFDA was chosen because it provides publicly accessible adverse-event data through an API.



**Storage:** SQLite was selected for a lightweight, reproducible prototype.



**Backend:** FastAPI was selected for modular API endpoints and automatically generated API documentation.



**Analysis:** Descriptive reaction-frequency analysis was selected instead of predictive ML because the available data does not support defensible patient-level risk prediction without additional assumptions and validation.



**Provenance:** Source identifiers, retrieval metadata, and schema information are retained to support evidence traceability.



## 8. Assumptions



\- The external source may change between retrievals.

\- Drug-name searches depend on the source's representation of medicinal products.

\- Normalized evidence records may represent drug–reaction combinations rather than independent clinical cases.

\- Reaction counts represent the acquired dataset, not the population incidence of adverse reactions.

\- Source reports may contain incomplete or inconsistent information.



## 9. Limitations and Unresolved Questions



\- How should synonymous drug names and reaction terms be harmonized?

\- How should repeated FAERS reports and follow-up versions be identified?

\- What additional evidence is required before performing statistical safety-signal detection?

\- How should larger datasets be processed and stored efficiently?

\- What authentication, monitoring, and deployment controls would be required for production use?

\- How should domain experts validate the analytical interpretation?



## 10. Further Learning



Future work may include:



\- Official FAERS documentation and reporting conventions.

\- Standardized drug and reaction terminologies.

\- Statistical pharmacovigilance signal-detection methods.

\- Data quality assessment and missingness analysis.

\- Reproducible analytical experiments.

\- Scientific validation of derived results.



## 11. Conclusion



This project provided practical experience in transforming publicly accessible biomedical reports into structured, traceable evidence and descriptive research intelligence.



The implementation is a research prototype, not a clinical decision-making system.
