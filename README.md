# Cynbit AI Lead Intelligence

A practical proof of concept for converting inbound service inquiries into structured, prioritized sales leads.

## What it does

- Accepts an unstructured customer inquiry.
- Extracts project need, budget, timeline and contact details.
- Recommends a likely service category.
- Calculates a transparent heuristic lead-priority score.
- Labels leads Hot / Warm / Cold.
- Saves records in SQLite.
- Displays a dashboard and exports CSV.
- Uses Groq-hosted Llama for structured extraction when `GROQ_API_KEY` is configured; otherwise runs in deterministic demo mode.

## Run locally

```bash
git clone <your-repository-url>
cd cynbit-ai-lead-agent
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and configure:
```bash
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq key to `.env`:
```env
GROQ_API_KEY=your_real_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Run:
```bash
streamlit run app.py
```

Without a key, the app uses demo rules. Never commit `.env` or API keys.

## Scoring logic

| Signal | Points |
|---|---:|
| Project requirement present | 25 |
| Budget present | 25 |
| High urgency / near-term timeline | 25 |
| Email or phone present | 15 |
| Relevant service category identified | 10 |
| Maximum | 100 |

- Hot: 70–100
- Warm: 40–69
- Cold: 0–39

These are proposed heuristic thresholds for a demonstration. They are not trained probabilities and must be validated against consented historical CRM outcomes before operational use.

## Architecture

`Streamlit UI -> LeadAgent -> (Groq JSON extraction OR demo extraction) -> Service classification -> Rule-based scoring -> SQLite -> Dashboard/CSV`

## Project documents

- `docs/AI_Opportunity_Report.md`
- `docs/Technical_Approach.md`

## Tests

```bash
pytest -q
```

## Important limitations

This is an assessment prototype, not a production CRM integration. It does not send messages, contact leads, or create external CRM records. Company service descriptions and scoring assumptions should be validated with Cynbit. Avoid entering real personal or confidential customer information in a public demo.

## Future improvements

1. Validate taxonomy and service catalog with Cynbit stakeholders.
2. Evaluate extraction quality on an approved, anonymized dataset.
3. Calibrate lead scores against historical conversion outcomes.
4. Integrate an approved CRM using least-privilege credentials.
5. Add authentication, audit logs, retention controls and human approval.
6. Monitor latency, cost, extraction errors and lead conversion metrics.
