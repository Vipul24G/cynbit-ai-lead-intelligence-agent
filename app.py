import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from agent import LeadAgent
from database import init_db, save_lead, get_leads, export_leads_csv

load_dotenv()
st.set_page_config(page_title="Cynbit AI Lead Intelligence", page_icon="Cynbit", layout="wide")
init_db()

st.title("Cynbit AI Lead Intelligence")
st.caption("AI-assisted inquiry qualification | Assessment proof of concept")

with st.sidebar:
    st.header("Configuration")
    api_ready = bool(os.getenv("GROQ_API_KEY"))
    st.write("Groq API")
    st.divider()
    page = st.radio("Navigate", ["Lead Assistant", "Lead Dashboard", "About & Limitations"])

agent = LeadAgent()

if page == "Lead Assistant":
    st.subheader("Qualify a prospective customer")
    st.write("Enter an enquiry as if it came from a website contact form or chat.")
    default = "Hi, I run an online clothing store. I need an AI chatbot that can answer product questions and help customers track orders. My budget is around ₹50,000 and I want to launch within 4 weeks. You can contact me at demo@example.com."
    inquiry = st.text_area("Customer inquiry", value=default, height=160)
    if st.button("Analyze lead", type="primary", use_container_width=True):
        if not inquiry.strip():
            st.warning("Please enter a customer inquiry.")
        else:
            with st.spinner("Analyzing inquiry..."):
                result = agent.analyze(inquiry)
                lead_id = save_lead(inquiry, result)
            st.success(f"Analysis complete. Lead #{lead_id} saved.")
            st.session_state["latest_result"] = result
            st.session_state["latest_id"] = lead_id

    result = st.session_state.get("latest_result")
    if result:
        st.divider()
        st.subheader("Analysis result")
        c1, c2, c3 = st.columns(3)
        c1.metric("Lead score", f'{result["score"]}/100')
        c2.metric("Task temperature ", result["temperature"])
        c3.metric("Recommended service", result["recommended_service"])
        left, right = st.columns(2)
        with left:
            st.markdown("**Extracted details**")
            details = result["lead"]
            st.json(details)
        with right:
            st.markdown("**Sales handoff summary**")
            st.write(result["summary"])
            st.markdown("**Suggested next question**")
            st.info(result["next_question"])
            st.caption("This is a prioritization suggestion, not a prediction of conversion probability.")

elif page == "Lead Dashboard":
    st.subheader("Lead pipeline")
    rows = get_leads()
    if not rows:
        st.info("No leads saved yet. Analyze an inquiry in Lead Assistant.")
    else:
        df = pd.DataFrame(rows)
        a, b, c = st.columns(3)
        a.metric("Total leads", len(df))
        b.metric("Hot leads", int((df["temperature"] == "Hot").sum()))
        c.metric("Average score", round(float(df["score"].mean()), 1))
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download leads as CSV",
            data=export_leads_csv(),
            file_name="cynbit_leads.csv",
            mime="text/csv",
            use_container_width=True,
        )

else:
    st.subheader("What this proof of concept demonstrates")
    st.markdown("""
- Converts unstructured customer inquiries into structured lead records.
- Recommends a relevant service category.
- Applies transparent, rule-based lead prioritization.
- Stores analyzed leads in a local SQLite database.
- Provides a sales handoff summary and CSV export.

**Important limitations**
- The sample company/service knowledge in this prototype is an assessment assumption and should be validated with Cynbit.
- Scores are heuristic rules, not a trained machine-learning model and not calibrated conversion probabilities.
- The demo does not send emails, create CRM records, or contact customers.
- Do not enter real personal or confidential customer data in a public demo.
- In demo mode, extraction uses deterministic keyword/rule logic. With a valid Groq API key, the LLM extracts structured fields; scoring remains deterministic.
""")
    st.markdown("**Suggested next phase:** connect an approved CRM, evaluate on consented historical leads, calibrate thresholds, add access controls, monitoring and human approval.")
