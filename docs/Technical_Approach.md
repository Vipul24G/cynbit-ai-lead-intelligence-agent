# Technical Approach Report — Cynbit AI Lead Intelligence

**Candidate:** Vipul Gupta  
**Role:** AI/ML Engineer Intern

## 1. Objective

Build a small, demonstrable application that transforms inbound service inquiries into structured lead records and prioritizes them for human sales review.

## 2. System architecture

```text
Customer inquiry ->Streamlit interface ->LeadAgent ->GROQ_API_KEY present? ---- Yes ---> Groq Llama JSON extraction ->No ---> Demo extraction rules ->Output normalization/validation ->Service recommendation  / Lead scoring rules ->Handoff summary + next question ->SQLite storage ->Dashboard and CSV export
     
                              
   
## 3. Model choice

**LLM:** Groq-hosted  for extracting semi-structured details from natural-language inquiries.

Rationale:
- Supports instruction-following and structured JSON output.
- Suitable for a low-latency prototype.
- Keeps the model layer replaceable if the company prefers another provider.

The model is not used to determine the final lead score. A deterministic scoring function is used for transparency and reproducibility.

**Fallback:** If no API key is configured, a deterministic rule-based extractor allows the demo to run. This mode is not equivalent to LLM extraction and has lower language coverage.

## 4. Prompt engineering

The system prompt:
- Defines the assistant as an inquiry-intake extractor.
- Specifies a strict JSON schema.
- Requires `null` for unknown fields.
- Prohibits inventing contact details, budget, timeline or company names.
- Separates extraction from scoring.
- Prohibits promises about feasibility or delivery.

The customer inquiry is treated as untrusted input. In production, additional validation, prompt-injection testing, output constraints and provider data-handling review are required.

## 5. Data pipeline

1. **Input:** inquiry text entered in Streamlit.
2. **Pre-processing:** trim and limit text length.
3. **Extraction:** Groq JSON mode or demo rule extractor.
4. **Normalization:** enforce field types and allowed urgency values.
5. **Service mapping:** keyword-based mapping to a proposed service taxonomy.
6. **Scoring:** deterministic business rules.
7. **Persistence:** SQLite record with timestamp and structured details.
8. **Presentation:** lead summary, dashboard and CSV export.

No external customer dataset is included. The demo input is synthetic.

## 6. Lead scoring

| Signal | Points |
|---|---:|
| Project need present | 25 |
| Budget supplied | 25 |
| High urgency / near-term timeline | 25 |
| Email or phone supplied | 15 |
| Service category identified | 10 |

Bands:
- Hot: 70–100
- Warm: 40–69
- Cold: 0–39

This is an explainable heuristic, not a supervised ML model or a calibrated probability. The rules and thresholds must be agreed with the business and evaluated against historical outcomes before use.

## 7. Evaluation plan

Create an approved, anonymized evaluation set with representative inquiries and human-labeled fields. Measure:
- Exact-match and field-level precision/recall for budget, timeline and contact extraction
- Service classification macro-F1
- JSON validity rate
- Human correction rate
- Latency and cost per request
- Agreement between score band and sales-accepted/conversion outcomes

Use a held-out test set. Do not tune thresholds on the final test set.

## 8. Execution plan

**Phase 1 — Prototype**
- Build inquiry interface, extraction, scoring, SQLite and dashboard.
- Test with synthetic examples.
- Publish code and demo.

**Phase 2 — Validation**
- Confirm service taxonomy and workflow with sales stakeholders.
- Obtain approved anonymized historical inquiries and outcomes.
- Label data and establish baselines.

**Phase 3 — Pilot**
- Run in shadow mode beside the existing process.
- Compare AI suggestions with human decisions.
- Review false positives, false negatives and missing fields.

**Phase 4 — Production hardening**
- Integrate CRM through approved APIs.
- Add authentication, authorization, audit logs and retention controls.
- Add monitoring, rate limits, retries and human approval.
- Review privacy, security and vendor data-processing terms.

## 9. Deployment

The app is designed for Streamlit Community Cloud. Add the following secret in the app's deployment settings:

```toml
GROQ_API_KEY = "your-key"
GROQ_MODEL = "llama-3.3-70b-versatile"
```

Do not commit API keys. The SQLite database is suitable for a local demonstration; for multi-user production deployment, use a managed database with appropriate access controls and backups.

## 10. Limitations

- No live Cynbit CRM or customer data integration.
- No verified business baseline or measured ROI.
- Demo-mode extraction is rule-based and intentionally limited.
- Service mapping and scoring are proposed assumptions.
- SQLite is not intended for concurrent production workloads.
- Human review remains necessary.
