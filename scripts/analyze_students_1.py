import os
from typing import List, Dict, Any

import pandas as pd
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ_ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PROJ_ROOT, "data")

def _load_from_txt(path: str) -> pd.DataFrame:
    """
    Parse lines like:
    1 | 94600 | Tran Ha | email=ha.tran13@gmail.com | dob=2005-03-20 | home_town=BacNinh | math=7.5 | lit=6.2 | eng=6.2
    """
    rows: List[Dict[str, Any]] = []
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 8:
                continue
                
            # Tách tên
            name_parts = parts[2].split()
            if len(name_parts) < 2:
                continue
                
            rows.append({
                "student_code": parts[1],
                "first_name": name_parts[1],
                "last_name": name_parts[0],
                "email": parts[3].replace("email=", ""),
                "dob": parts[4].replace("dob=", ""),
                "home_town": parts[5].replace("home_town=", ""),
                "math_score": _to_float(parts[6].replace("math=", "")),
                "literature_score": _to_float(parts[7].replace("lit=", "")),
                "english_score": _to_float(parts[8].replace("eng=", ""))
            })
    
    return pd.DataFrame(rows)

def clean_students(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure numeric columns
    for col in ["math_score", "literature_score", "english_score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    before = len(df)
    df_clean = df.dropna(subset=["math_score", "literature_score", "english_score"]).copy()
    after = len(df_clean)
    print(f"Dropped {before - after} rows due to missing values in score columns.")
    return df_clean


def _to_float(x: Any):
    try:
        return float(str(x).strip())
    except Exception:
        return np.nan

def export_clean(df_clean: pd.DataFrame, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    txt_path = os.path.join(out_dir, "students_clean.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        

def main():
    txt = os.path.join(DATA_DIR, "students_raw.txt")
    df = _load_from_txt(txt)
    df_clean = clean_students(df)

    print(df)

if __name__ == "__main__":
    main()
