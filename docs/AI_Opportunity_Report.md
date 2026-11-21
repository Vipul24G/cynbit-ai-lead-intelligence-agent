# AI Opportunity Report — Cynbit

**Candidate:** Vipul Gupta  
**Role:** AI/ML Engineer Intern  
**Selected opportunity:** AI Lead Intelligence and Qualification Assistant  
**Document status:** Assessment proposal; validate assumptions with Cynbit.

## 1.Summary

Cynbit operates across technology and digital service areas, including AI/automation and software-related services. A recurring operational challenge for a multi-service provider is converting varied inbound inquiries into consistent, actionable sales records. This report proposes an AI-assisted lead-intake workflow that extracts requirements, identifies likely service fit, asks for missing information and prioritizes records for human review.

The accompanying proof of concept demonstrates the workflow with a Streamlit interface, optional Groq-hosted Llama extraction, transparent rule-based scoring, SQLite persistence and CSV export.

## 2. Business context and assumptions

Public-facing company information and product/service pages should be reviewed and confirmed before production use. For this assessment, the proposed service taxonomy includes:
- AI automation and agent solutions
- Custom software development
- Digital marketing and SEO
- Cloud and infrastructure
- SaaS/product development

**Assumptions to validate:** 
enquiry volume, current lead handling process, CRM in use, sales response-time baseline, conversion rate, service taxonomy and data availability. No internal Cynbit CRM or customer data was available for this prototype.

## 3. High-value AI/ML opportunities

| Opportunity | Potential value | Complexity | Suggested first step |

| Lead intelligence and qualification | Faster triage, more consistent records, sales prioritization | Medium | Inquiry extraction and scoring POC |
| Review intelligence | Categorize feedback, detect recurring issues, draft response suggestions | Medium | Sentiment/topic analysis on approved review data |
| AI-assisted coding assessment | Faster feedback, rubric-based evaluation and learning support | High | Evaluation assistant with human moderation |
| Tenant/customer support assistant | Deflect repetitive questions and route complex cases | Medium–High | Retrieval-based FAQ assistant |
| SEO/content intelligence | Topic clustering, content briefs and performance summaries | Medium | Search-query and content analysis workflow |


## 4. Selected problem

Inbound inquiries can vary widely in detail and format. A sales representative may need to manually identify:
- What problem the customer wants solved
- Which service line is relevant
- Approximate budget
- Desired timeline and urgency
- Contact details
- Missing information needed for qualification

Inconsistent or incomplete intake can create avoidable follow-up work and make prioritization harder.

## 5. Proposed solution

An AI-assisted lead qualification workflow that:
1. Accepts a customer inquiry.
2. Extracts explicitly stated fields into a structured JSON record.
3. Maps the inquiry to a service category.
4. Calculates a transparent lead-priority score.
5. Labels the lead Hot, Warm or Cold.
6. Generates a concise handoff summary and next question.
7. Stores the record for review and CSV export.

The system supports human-in-the-loop review. It does not automatically reject leads, promise delivery, or contact customers.
## Another Idea which can be implement 
there is an another proposed solution that we can add an RAG chatbot with web page so that custumer can direct interct with our whole web page so that he can gain every info and services at a place.
1. Accepts customers query.
2. RAG system extrect all information reagrding query.
3. after info extraction it goes to an LLM .
4. LLM add some info 
5. finally LLM gave output according to user query
6. LLM output show on the screen 

## Another idea (Sentiment analysis)
1. we can use an Sentiment Analysis on customers feedback so that we can improve our service

## 6. Expected business value and KPIs

Potential benefits:
- Reduced manual data-entry and triage effort
- More consistent lead records
- Faster identification of high-priority inquiries
- Better visibility into missing information and service demand

Recommended KPIs for a controlled pilot:
- Field extraction precision/recall
- Service-category classification accuracy
- Median time to triage one inquiry
- Percentage of leads with complete contact/budget/timeline fields
- Sales-accepted lead rate by score band
- Conversion rate by score band
- Human correction rate
- Cost and latency per analyzed inquiry

No numerical ROI is claimed without baseline data.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Incorrect extraction or hallucination | JSON schema, null for unknown values, human verification |
| Biased or misleading lead scoring | Transparent rules, monitor outcomes, avoid protected/sensitive attributes |
| Exposure of personal data | Data minimization, access control, retention policy, approved providers |
| Prompt injection in customer text | Treat inquiry as untrusted data; strict system prompt and output validation |
| API outage or rate limit | Demo fallback, retries with limits, error logging |
| Over-reliance on score | Display reasons; label as priority heuristic, not conversion probability |

## 8. Recommendation

Run a small pilot after validating the service taxonomy and workflow with the sales team. Compare the assistant's extracted records and suggested priority against human-reviewed outcomes. Only calibrate or automate further after measuring quality and operational benefit.
