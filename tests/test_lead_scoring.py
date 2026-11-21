from agent import LeadAgent

def test_hot_lead_with_budget_timeline_and_contact(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    agent = LeadAgent()
    result = agent.analyze(
        "I need an AI chatbot for my store. Budget ₹50,000, launch within 4 weeks. Email me at test@example.com"
    )
    assert result["score"] >= 70
    assert result["temperature"] == "Hot"
    assert result["recommended_service"] == "AI Automation"

def test_missing_budget_is_identified(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    agent = LeadAgent()
    result = agent.analyze("Need a website for my business. Contact me at hello@example.com")
    assert result["lead"]["budget_inr"] is None
    assert "Budget" in result["lead"]["missing_information"]
