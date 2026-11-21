import json
import os
import re
from groq import Groq

SERVICES = {
    "AI Automation": ["ai chatbot", "chatbot", "automation", "ai assistant", "agent", "workflow"],
    "Custom Software Development": ["website", "web app", "application", "software", "platform", "mobile app"],
    "Digital Marketing & SEO": ["seo", "marketing", "social media", "content", "advertising"],
    "Cloud & Infrastructure": ["cloud", "hosting", "server", "deployment", "infrastructure"],
    "SaaS / Product Development": ["saas", "subscription product", "multi-tenant", "product development"],
}

SYSTEM_PROMPT = """You are a lead-intake assistant for a software and AI services company.
Extract only information explicitly stated or strongly implied by the inquiry.
Never invent a name, company, email, phone, budget, or deadline. Use NA when unknown.
Return valid JSON only, matching this schema:
{
 "name": string|NA,
 "company": string|NA,
 "email": string|NA,
 "phone": string|NA,
 "project_need": string,
 "budget_inr": number|NA,
 "timeline": string|NA,
 "urgency": "high"|"medium"|"low"|"unknown",
 "service_interest": string,
 "missing_information": [string]
}
Do not decide the lead score. Do not claim that a project is feasible or promise delivery."""

class LeadAgent:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    def analyze(self, inquiry: str) -> dict:
        lead = self._extract_with_groq(inquiry) if self.api_key else self._extract_demo(inquiry)
        service = self._recommend_service(inquiry, lead.get("service_interest"))
        score, temperature, reasons = self._score(lead, service)
        summary = self._summary(lead, service, score, temperature, reasons)
        return {
            "lead": lead,
            "recommended_service": service,
            "score": score,
            "temperature": temperature,
            "score_reasons": reasons,
            "summary": summary,
            "next_question": self._next_question(lead),
            "mode": "Groq LLM" ,
        }

    def _extract_with_groq(self, inquiry: str) -> dict:
        client = Groq(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": inquiry[:6000]},
            ],
        )
        data = json.loads(response.choices[0].message.content)
        return self._normalize(data)

    def _normalize(self, data: dict) -> dict:
        fields = ["name", "company", "email", "phone", "project_need", "budget_inr",
                  "timeline", "urgency", "service_interest", "missing_information"]
        clean = {k: data.get(k) for k in fields}
        for k in ["name", "company", "email", "phone", "timeline"]:
            if clean[k] is not None:
                clean[k] = str(clean[k])[:200]
        clean["project_need"] = str(clean.get("project_need") or "Not specified")[:1000]
        clean["service_interest"] = str(clean.get("service_interest") or "Not specified")[:100]
        clean["urgency"] = str(clean.get("urgency") or "unknown").lower()
        if clean["urgency"] not in {"high", "medium", "low", "unknown"}:
            clean["urgency"] = "unknown"
        try:
            clean["budget_inr"] = float(clean["budget_inr"]) if clean["budget_inr"] is not None else None
        except (ValueError, TypeError):
            clean["budget_inr"] = None
        if not isinstance(clean["missing_information"], list):
            clean["missing_information"] = []
        return clean

    def _extract_demo(self, inquiry: str) -> dict:
        text = inquiry.strip()
        email_match = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", text, re.I)
        phone_match = re.search(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", text)
        budget_match = re.search(r"(?:₹|rs\.?\s*|inr\s*)([\d,]+)", text, re.I)
        budget = float(budget_match.group(1).replace(",", "")) if budget_match else None
        lower = text.lower()
        if any(x in lower for x in ["within", "week", "month", "urgent", "asap", "days"]):
            urgency = "high" if any(x in lower for x in ["urgent", "asap", "within 2 weeks", "within one month", "within 4 weeks"]) else "medium"
        else:
            urgency = "unknown"
        company = None
        company_match = re.search(r"(?:at|for|company is)\s+([A-Z][A-Za-z0-9& ]{2,40})", text)
        if company_match:
            company = company_match.group(1).strip()
        service = self._recommend_service(text, None)
        missing = []
        if not budget: missing.append("Budget")
        if not re.search(r"\b(week|month|day|date|quarter)\b", lower): missing.append("Time not Mentioned")
        if not email_match and not phone_match: missing.append("Contact Not Found")
        return {
            "name": None, "company": company,
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0) if phone_match else None,
            "project_need": text[:1000],
            "budget_inr": budget,
            "timeline": self._find_timeline(text),
            "urgency": urgency,
            "service_interest": service,
            "missing_information": missing,
        }

    def _find_timeline(self, text):
        m = re.search(r"\b(?:within\s+)?\d+\s*(?:days?|weeks?|months?)\b|\b(?:one|two|three|four)\s+(?:weeks?|months?)\b", text, re.I)
        return m.group(0) if m else None

    def _recommend_service(self, inquiry, extracted):
        text = (inquiry + " " + str(extracted or "")).lower()
        scores = {service: sum(1 for word in words if word in text) for service, words in SERVICES.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "Needs human review"

    def _score(self, lead, service):
        score, reasons = 0, []
        if lead.get("project_need") and lead["project_need"] != "Not specified":
            score += 25; reasons.append("Clear project requirement (+25)")
        if lead.get("budget_inr") is not None:
            score += 25; reasons.append("Budget provided (+25)")
        if lead.get("urgency") == "high":
            score += 25; reasons.append("Urgent timeline (+25)")
        elif lead.get("urgency") == "medium":
            score += 15; reasons.append("Timeline indicated (+15)")
        if lead.get("email") or lead.get("phone"):
            score += 15; reasons.append("Contact information provided (+15)")
        if service != "Needs human review":
            score += 10; reasons.append("Relevant service identified (+10)")
        temperature = "Hot" if score >= 70 else "Warm" if score >= 40 else "Cold"
        return min(score, 100), temperature, reasons

    def _summary(self, lead, service, score, temperature, reasons):
        budget = f"₹{lead['budget_inr']:,.0f}" if lead.get("budget_inr") is not None else "Not provided"
        contact = lead.get("email") or lead.get("phone") or "Not provided"
        return (
            f"{temperature} lead (score {score}/100). Interest: {service}. "
            f"Need: {lead.get('project_need', 'Not specified')}. "
            f"Budget: {budget}. Timeline: {lead.get('timeline') or 'Not provided'}. "
            f"Contact: {contact}. Verify details with the customer before making commitments."
        )

    def _next_question(self, lead):
        if not lead.get("project_need") or lead["project_need"] == "Not specified":
            return "Could you briefly describe the problem you want to solve?"
        if lead.get("budget_inr") is None:
            return "Do you have an approximate project budget range?"
        if not lead.get("timeline"):
            return "When would you ideally like to start and launch this project?"
        if not (lead.get("email") or lead.get("phone")):
            return "What is the best business email address or phone number for follow-up?"
        return "Could you share any must-have integrations or success criteria for this project?"
