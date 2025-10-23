#!/usr/bin/env python3

import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)

def run_script(script_name, description):
    print(f"\n{'='*60}")
    print(f"CHẠY: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], capture_output=True, text=True, cwd=HERE, check=False)
        
        if result.returncode == 0:
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("LỖI")
            if result.stderr:
                print("Error:")
                print(result.stderr)
                
    except (OSError, subprocess.SubprocessError) as e:
        print(f"LỖI KHI CHẠY SCRIPT: {e}")

def main():
    scripts = [
        ("analyze_students.py", "Phân tích cơ bản - Điểm theo quê quán"),
        ("analyze_by_age.py", "Phân tích theo nhóm tuổi"),
        ("analyze_top_bottom_students.py", "Phân tích học sinh xuất sắc/yếu kém")
    ]
    
    for script_name, description in scripts:
        run_script(script_name, description)

if __name__ == "__main__":
    main()
