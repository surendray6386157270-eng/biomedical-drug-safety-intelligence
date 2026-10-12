# Analytics Experiment — Drug–Reaction Frequency Analysis



## 1. Dataset



**Source:** FDA Adverse Event Reporting System (FAERS), accessed through the openFDA Drug Adverse Events API.



The experiment uses normalized drug–reaction evidence records acquired through the project's ingestion pipeline and stored in SQLite.



The number and composition of records depend on the drug queried, the retrieval limit, and the source data available at execution time.



## 2. Problem Definition



Researchers need a reproducible way to summarize which adverse reactions appear most frequently within a retrieved set of drug safety reports.



Raw FAERS records are not sufficient on their own to provide a structured analytical summary.



The objective is to transform stored evidence into reaction-frequency summaries while preserving access to the underlying source records.



## 3. Research Question



For a selected drug, which reactions occur most frequently in the available normalized evidence, and what proportion of the analyzed records contains each reaction?



This is an exploratory research question, not a clinical risk-estimation question.



## 4. Input and Feature Selection



The analysis uses:



\- `drug\_name` to select the evidence dataset.

\- `reaction` to identify the reported adverse-event term.

\- The number of retrieved evidence records as the denominator for descriptive proportions.



Source identifiers and provenance are retained in the returned evidence but are not used as predictive features.



No patient-level features or clinical outcomes are used for prediction.



## 5. Preprocessing



The upstream pipeline retrieves, validates, and normalizes source records before storing them.



During analysis:



1\. Stored evidence is retrieved for the selected drug.

2\. Records with missing or empty reaction values are excluded from reaction counting.

3\. Reaction strings are stripped of surrounding whitespace.

4\. Exact reaction strings are counted.

5\. The 10 most frequent reaction strings are returned.



The implementation does not perform clinical terminology harmonization or semantic grouping of synonymous reaction terms.



## 6. Method



**Method:** Descriptive drug–reaction frequency analysis.



**Implementation:** `app/analytics/drug\_reaction.py`



The analysis uses Python's `collections.Counter`.



For each reaction:



`reaction\_count = number of analyzed records containing that reaction value`



`reaction\_proportion = reaction\_count / total\_analyzed\_evidence\_records`



The proportion is rounded to four decimal places.



The implementation returns:



\- Total evidence records

\- Number of unique non-empty reaction values

\- Top 10 reactions

\- Count for each reaction

\- Proportion for each reaction

\- Scientific limitations



## 7. Baseline



The baseline is an unaggregated listing of normalized evidence records returned by the evidence search service.



This provides individual reaction values but no ranked summary.



The analytical method adds deterministic frequency aggregation, ranking, and within-sample proportions.



This is a descriptive baseline comparison, not a predictive model benchmark.



## 8. Evaluation



Evaluation focuses on correctness and reproducibility rather than classification accuracy.



Relevant checks include:



\- Total record count matches the input dataset size.

\- Reaction frequencies match direct counts over the input.

\- Unique reaction count matches the number of distinct non-empty reaction strings.

\- Returned reactions are ranked by frequency.

\- Proportions use the total evidence record count as the denominator.

\- Empty input produces an explicit no-evidence result.

\- Repeated analysis over unchanged evidence produces the same output.



The project includes automated analytics and service tests.



## 9. Results



The implemented analysis returns structured descriptive summaries through:



`GET /api/drugs/{drug\_name}/analysis?limit=10`



A captured aspirin analysis response is stored at:



`evidence\_packet/api\_samples/aspirin\_analysis.json`



The saved response is the evidence artifact for the observed analysis results. Its exact numerical findings should be read from that file rather than assumed from a live source whose data can change.



The latest previously verified local test suite completed with **18 passing tests**.



Test evidence is stored at:



`evidence\_packet/runtime\_logs/pytest\_results.txt`



## 10. Why Predictive ML Was Not Used



The acquired FAERS reports do not provide a reliable population denominator, unbiased sampling, or independently validated clinical outcome labels suitable for estimating patient-specific adverse-reaction probabilities.



Training a predictive model without a defensible target and evaluation design could create misleading claims.



The chosen descriptive approach answers the research question directly without implying predictive clinical validity.



The BHIV assignment explicitly permits scientifically defensible descriptive analytics.



## 11. Assumptions and Limitations



\- FAERS is a spontaneous reporting system subject to reporting bias.

\- Report counts are not incidence rates.

\- Reported associations do not establish causation.

\- The acquired sample may not represent the broader reporting population.

\- Records may contain missing or inconsistent information.

\- Exact-string counting may treat equivalent reaction terms separately.

\- The denominator includes all input evidence records, including any without a usable reaction value.

\- The analysis counts normalized evidence records, not necessarily unique patients or unique FAERS cases.

\- No confidence intervals, causal estimates, predictive performance scores, or clinical risk estimates are produced.



## 12. Reproducibility



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



Start the application:



```powershell

python -m uvicorn app.main:app --reload

```



In a separate PowerShell terminal, ingest aspirin evidence:



```powershell

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/drugs/aspirin/ingest?limit=10"

```



Retrieve the analysis:



```powershell

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/drugs/aspirin/analysis?limit=10" | ConvertTo-Json -Depth 12

```



Run automated tests:



```powershell

python -m pytest -q

```



For deterministic review, use the captured API samples and automated test fixtures. Live source retrieval may produce different records over time.



## 13. Conclusion



The experiment implements a reproducible descriptive analytical capability over real biomedical evidence.



It adds reaction-frequency intelligence beyond raw API retrieval while retaining access to source evidence and avoiding unsupported clinical or predictive claims.
