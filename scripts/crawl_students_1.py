import os 
import json
import requests
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

RAW_TXT = os.path.join(DATA_DIR, "students_raw_2.txt")

def fetch_all_students(limit=10000):
    params = {"limit": limit}
    r = requests.get(f"{API_BASE}/students", params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def save_text(all_students, RAW_TXT):
    with open(RAW_TXT, "w", encoding="utf-8") as f:
        for student in all_students:
            f.write(f"{student['student_code']} | {student['first_name']} {student['last_name']} | {student['email']} | {student['dob']} | {student['home_town']} | {student['math_score']} | {student['literature_score']} | {student['english_score']}\n")


def main():
    all_students = fetch_all_students()
    save_text(all_students, RAW_TXT)
    print(len(all_students))

if __name__ == "__main__":
    main()
