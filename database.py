import csv
import io
import json
import sqlite3
from datetime import datetime, timezone

DB_PATH = "leads.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            inquiry TEXT NOT NULL,
            name TEXT, company TEXT, email TEXT, phone TEXT,
            project_need TEXT, budget_inr REAL, timeline TEXT,
            recommended_service TEXT, score INTEGER,
            temperature TEXT, summary TEXT, details_json TEXT
        )
        """)

def save_lead(inquiry, result):
    lead = result["lead"]
    with _connect() as conn:
        cur = conn.execute("""
        INSERT INTO leads (
            created_at, inquiry, name, company, email, phone, project_need,
            budget_inr, timeline, recommended_service, score, temperature,
            summary, details_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(), inquiry,
            lead.get("name"), lead.get("company"), lead.get("email"), lead.get("phone"),
            lead.get("project_need"), lead.get("budget_inr"), lead.get("timeline"),
            result.get("recommended_service"), result.get("score"),
            result.get("temperature"), result.get("summary"), json.dumps(lead)
        ))
        return cur.lastrowid

def get_leads():
    with _connect() as conn:
        rows = conn.execute("""
        SELECT id, created_at, company, email, project_need, budget_inr,
               recommended_service, score, temperature
        FROM leads ORDER BY id DESC
        """).fetchall()
    return [dict(row) for row in rows]

def export_leads_csv():
    output = io.StringIO()
    rows = get_leads()
    if rows:
        writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return output.getvalue()
