#!/usr/bin/env python3
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_JSONL = os.path.join(DATA_DIR, "students_raw.jsonl")

CLEAN_CSV = os.path.join(DATA_DIR, "students_clean.csv")
REPORT_TXT = os.path.join(DATA_DIR, "analysis_report.txt")

NUM_COLS = ["math_score", "literature_score", "english_score"]

def read_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return pd.DataFrame(rows)

def clean_scores(df: pd.DataFrame) -> pd.DataFrame:
    # Ép kiểu số
    for c in NUM_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # Ràng buộc 0..10 (điểm ngoài range xem như NaN, có thể clip nếu bạn muốn)
    for c in NUM_COLS:
        df.loc[(df[c] < 0) | (df[c] > 10), c] = np.nan

    # Xử lý thiếu: có nhiều cách, ở đây mình không fill để phân tích trung thực
    # Bạn có thể df[c].fillna(df[c].median()) nếu muốn điền
    return df

def english_vs_math_per_student(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[["student_code","last_name","first_name","home_town","math_score","english_score"]].copy()
    sub["eng_ge_math"] = np.where(sub["english_score"] >= sub["math_score"], True, False)
    sub["eng_minus_math"] = sub["english_score"] - sub["math_score"]
    return sub

def english_by_hometown(df: pd.DataFrame) -> pd.DataFrame:
    # Trung bình điểm English theo quê quán
    grp = (
        df.groupby("home_town", dropna=False)["english_score"]
        .agg(["count", "mean", "median"])
        .sort_values(by="mean", ascending=False)
    )
    return grp

def write_report(per_student: pd.DataFrame, by_hometown: pd.DataFrame, out_path: str):
    top_eng = by_hometown.head(10)
    bot_eng = by_hometown.tail(10)

    lines = []
    lines.append(f"# Report generated: {datetime.now().isoformat()}")
    lines.append("")

    # 1) So sánh từng sinh viên: Eng vs Math
    total = len(per_student)
    more_eng = int(per_student["eng_ge_math"].sum())
    less_eng = total - more_eng
    lines.append("## English vs Math (per student)")
    lines.append(f"Total students (with any score): {total}")
    lines.append(f"English >= Math: {more_eng} ({more_eng/total:.1%})")
    lines.append(f"English <  Math: {less_eng} ({less_eng/total:.1%})")
    lines.append("")

    # 2) Trung bình English theo quê quán
    lines.append("## Average English score by hometown (top 10)")
    lines.append(top_eng.to_string())
    lines.append("")
    lines.append("## Average English score by hometown (bottom 10)")
    lines.append(bot_eng.to_string())
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    if not os.path.exists(RAW_JSONL):
        raise SystemExit(f"❌ Missing raw file: {RAW_JSONL}. Hãy chạy scripts/crawl_students.py trước.")

    df = read_jsonl(RAW_JSONL)
    # Làm sạch
    df = clean_scores(df)

    # Lưu bản sạch (phục vụ các phân tích khác)
    df.to_csv(CLEAN_CSV, index=False, encoding="utf-8")
    print(f"✅ Saved clean data: {CLEAN_CSV}")

    # Phân tích:
    per_student = english_vs_math_per_student(df)
    by_hometown = english_by_hometown(df)

    write_report(per_student, by_hometown, REPORT_TXT)
    print(f"✅ Analysis report: {REPORT_TXT}")

if __name__ == "__main__":
    main()