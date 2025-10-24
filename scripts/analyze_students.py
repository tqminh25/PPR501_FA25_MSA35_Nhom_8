
"""
analyze_students.py
-------------------
- Cleans data by dropping students with missing values in score columns (math, literature, english).
- Exports cleaned data to student-mgr/data as students_clean.txt and students_clean.json.
- Plots a Matplotlib line chart comparing average English and Math scores by home_town (province/city)
  on the same figure.
Usage:
    python analyze_students.py
Notes:
    - Input data sources searched in ./data:
        * students_raw.jsonl  (preferred if present)
        * students_random_100.csv (fallback if present)
        * students_raw.txt (fallback parser)
"""

import os
import json
import re
from typing import List, Dict, Any

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


HERE = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PROJ_ROOT, "data")

# ---------- Helpers ----------

def _load_from_jsonl(path: str) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    # Normalize expected columns
    rename_map = {
        "math_score": "math_score",
        "literature_score": "literature_score",
        "english_score": "english_score",
        "home_town": "home_town",
        "student_code": "student_code",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email",
        "dob": "dob",
    }
    # Some sources may have slightly different keys; enforce presence
    for col in ["math_score", "literature_score", "english_score"]:
        if col not in df.columns:
            # try short names
            short = {"math_score": "math", "literature_score": "lit", "english_score": "eng"}[col]
            if short in df.columns:
                df[col] = df[short]
    return df


def _load_from_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Standardize column names if needed
    cols = {c.lower().strip(): c for c in df.columns}
    # Map possible variants to target names
    variants = {
        "math_score": ["math_score", "math", "diem_toan", "toan"],
        "literature_score": ["literature_score", "lit", "diem_van", "van"],
        "english_score": ["english_score", "eng", "diem_ta", "ta", "diem_tieng_anh"],
    }
    for target, candidates in variants.items():
        if target not in df.columns:
            for cand in candidates:
                if cand in df.columns or cand in cols:
                    df[target] = df.get(cand, df.get(cols.get(cand, cand)))
                    break
    return df


def _load_from_txt(path: str) -> pd.DataFrame:
    """
    Parse lines like:
    94600 | Ha Tran | ha.tran13@gmail.com | 2005-03-20 | BacNinh | 7.5 | 6.2 | 6.2
    """
    rows: List[Dict[str, Any]] = []
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
                
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 8:
                continue
                
            # Tách tên
            name_parts = parts[1].split()
            if len(name_parts) < 2:
                continue
                
            rows.append({
                "student_code": parts[0],
                "first_name": name_parts[1],
                "last_name": name_parts[0],
                "email": parts[2],
                "dob": parts[3],
                "home_town": parts[4],
                "math_score": _to_float(parts[5]),
                "literature_score": _to_float(parts[6]),
                "english_score": _to_float(parts[7])
            })
    
    return pd.DataFrame(rows)


def _to_float(x: Any):
    try:
        return float(str(x).strip())
    except Exception:
        return np.nan


def load_students_df() -> pd.DataFrame:
    """
    Try multiple sources in priority order.
    """
    jsonl = os.path.join(DATA_DIR, "students_raw.jsonl")
    csv = os.path.join(DATA_DIR, "students_random_100.csv")
    txt = os.path.join(DATA_DIR, "students_raw.txt")

    if os.path.exists(jsonl):
        return _load_from_jsonl(jsonl)
    if os.path.exists(csv):
        return _load_from_csv(csv)
    if os.path.exists(txt):
        return _load_from_txt(txt)
    raise FileNotFoundError("No input data found in ./data")


def clean_students(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure numeric columns
    for col in ["math_score", "literature_score", "english_score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    before = len(df)
    df_clean = df.dropna(subset=["math_score", "literature_score", "english_score"]).copy()
    after = len(df_clean)
    print(f"Dropped {before - after} rows due to missing values in score columns.")
    return df_clean


def export_clean(df_clean: pd.DataFrame, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    # TXT: simple, one-line per record
    txt_path = os.path.join(out_dir, "students_clean.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        cols = ["student_code", "first_name", "last_name", "email", "dob", "home_town", "math_score", "literature_score", "english_score"]
        for _, row in df_clean[cols].iterrows():
            f.write(
                f"{row.student_code} | {row.last_name} {row.first_name} | {row.email} | {row.dob} | {row.home_town} | "
                f"math={row.math_score} | lit={row.literature_score} | eng={row.english_score}\n"
            )
    # JSON: list of dict
    json_path = os.path.join(out_dir, "students_clean.json")
    df_clean.to_json(json_path, orient="records", force_ascii=False, indent=2)
    print(f"Exported:\n- {txt_path}\n- {json_path}")
    return txt_path, json_path


def plot_avg_scores(df_clean: pd.DataFrame, out_dir: str):
    # Group by home_town and compute means
    group = df_clean.groupby("home_town", dropna=False).agg(
        avg_math=("math_score", "mean"),
        avg_eng=("english_score", "mean"),
        avg_lit=("literature_score", "mean"),
    ).reset_index()

    # Sort by home_town for consistent x-order
    group = group.sort_values("home_town").reset_index(drop=True)

    # Plot 3-line chart: Math, English, Literature
    plt.figure(figsize=(14, 6))
    x = range(len(group))
    plt.plot(x, group["avg_math"], marker="o", label="Điểm Toán trung bình", color="tab:blue")
    plt.plot(x, group["avg_eng"], marker="o", label="Điểm Tiếng Anh trung bình", color="tab:orange")
    plt.plot(x, group["avg_lit"], marker="o", label="Điểm Văn trung bình", color="tab:green")
    plt.xticks(ticks=x, labels=group["home_town"], rotation=45, ha="right")
    plt.xlabel("Tỉnh/Thành phố (home_town)")
    plt.ylabel("Điểm trung bình")
    plt.title("So sánh điểm trung bình: Toán • Tiếng Anh • Văn theo tỉnh/thành phố")
    plt.legend()
    plt.tight_layout()

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "avg_math_eng_lit_by_hometown.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved chart to {out_path}")

    return group, out_path


def plot_sorted_bars(group: pd.DataFrame, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    outputs = []
    
    # Lọc bỏ các giá trị null và đảm bảo home_town là string
    group = group.dropna(subset=['home_town'])
    group['home_town'] = group['home_town'].astype(str)

    # English
    g_eng = group.sort_values("avg_eng", ascending=True).reset_index(drop=True)
    plt.figure(figsize=(14, 6))
    plt.bar(g_eng["home_town"], g_eng["avg_eng"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Điểm Tiếng Anh trung bình")
    plt.title("Xếp hạng tỉnh/thành theo Điểm Tiếng Anh trung bình (thấp → cao)")
    plt.tight_layout()
    p1 = os.path.join(out_dir, "rank_home_town_by_english_avg.png")
    plt.savefig(p1, dpi=150); outputs.append(p1)

    # Math
    g_math = group.sort_values("avg_math", ascending=True).reset_index(drop=True)
    plt.figure(figsize=(14, 6))
    plt.bar(g_math["home_town"], g_math["avg_math"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Điểm Toán trung bình")
    plt.title("Xếp hạng tỉnh/thành theo Điểm Toán trung bình (thấp → cao)")
    plt.tight_layout()
    p2 = os.path.join(out_dir, "rank_home_town_by_math_avg.png")
    plt.savefig(p2, dpi=150); outputs.append(p2)

    # Literature
    g_lit = group.sort_values("avg_lit", ascending=True).reset_index(drop=True)
    plt.figure(figsize=(14, 6))
    plt.bar(g_lit["home_town"], g_lit["avg_lit"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Điểm Văn trung bình")
    plt.title("Xếp hạng tỉnh/thành theo Điểm Văn trung bình (thấp → cao)")
    plt.tight_layout()
    p3 = os.path.join(out_dir, "rank_home_town_by_literature_avg.png")
    plt.savefig(p3, dpi=150); outputs.append(p3)

    print("Saved bar charts:")
    for p in outputs:
        print(" -", p)
    return outputs


def main():
    df = load_students_df()
    df_clean = clean_students(df)
    # Export
    export_clean(df_clean, DATA_DIR)
    # Plot 3-line chart and ranked bars
    group, _ = plot_avg_scores(df_clean, DATA_DIR)
    plot_sorted_bars(group, DATA_DIR)
    
    # Thêm phân tích theo nhóm tuổi
    print("\n" + "="*50)
    print("BẮT ĐẦU PHÂN TÍCH THEO NHÓM TUỔI")
    print("="*50)
    
    # Import và chạy phân tích tuổi
    try:
        from analyze_by_age import main as analyze_age_main
        analyze_age_main()
    except ImportError:
        print("Không thể import analyze_by_age.py")
    except Exception as e:
        print(f"Lỗi khi chạy phân tích tuổi: {e}")


if __name__ == "__main__":
    main()
