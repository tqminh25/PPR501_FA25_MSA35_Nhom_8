#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

RAW_JSONL = os.path.join(DATA_DIR, "students_raw.jsonl")
RAW_TXT   = os.path.join(DATA_DIR, "students_raw.txt")

def fetch_all_students(limit=10000):
    params = {"limit": limit}
    r = requests.get(f"{API_BASE}/students", params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_student_by_id(id_):
    r = requests.get(f"{API_BASE}/students/{id_}", timeout=10)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def save_jsonl(records, path):
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def save_text(records, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            line = (
                f"{r.get('id')} | {r.get('student_code')} | "
                f"{(r.get('last_name') or '')} {(r.get('first_name') or '')} | "
                f"email={r.get('email')} | dob={r.get('dob')} | home_town={r.get('home_town')} | "
                f"math={r.get('math_score')} | lit={r.get('literature_score')} | eng={r.get('english_score')}"
            )
            f.write(line.strip() + "\n")

def main():
    all_students = fetch_all_students()

    enriched = []
    for s in all_students:
        s_detail = fetch_student_by_id(s["id"]) or s
        enriched.append(s_detail)

    save_jsonl(enriched, RAW_JSONL)
    save_text(enriched, RAW_TXT)

if __name__ == "__main__":
    main()