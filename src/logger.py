import csv
import os
from datetime import datetime

# Define log file paths
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_FILE = os.path.join(LOG_DIR, "cases.csv")
MD_FILE = os.path.join(LOG_DIR, "RESPONSIBLE_AI_LOG.md")

def log_case(
    problem,
    source="Gemini AI",
    root_cause="",
    next_command="",
    proposed_fix="",
    status="ACCEPTED",
    correction_reason="N/A",
    **kwargs
):
    """
    Logs diagnostic cases and human decisions to both CSV and Markdown audit logs.
    Captures additional fields (like osi_layer, confidence) via **kwargs safely.
    """
    # Ensure data directory exists
    os.makedirs(LOG_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Safely extract optional fields passed from app.py
    osi_layer = kwargs.get("osi_layer", "N/A")
    confidence = kwargs.get("confidence", "N/A")

    # 1. Append to CSV file
    file_exists = os.path.isfile(CSV_FILE)
    
    fieldnames = [
        "timestamp", "problem", "source", "root_cause", 
        "osi_layer", "confidence", "next_command", 
        "proposed_fix", "status", "correction_reason"
    ]

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "timestamp": timestamp,
            "problem": problem,
            "source": source,
            "root_cause": root_cause,
            "osi_layer": osi_layer,
            "confidence": confidence,
            "next_command": next_command,
            "proposed_fix": proposed_fix,
            "status": status,
            "correction_reason": correction_reason
        })

    # 2. Append to Markdown Governance Log
    with open(MD_FILE, mode="a", encoding="utf-8") as file:
        file.write(f"\n### Incident Log - {timestamp}\n")
        file.write(f"- **Problem:** {problem}\n")
        file.write(f"- **OSI Layer:** {osi_layer} | **Confidence:** {confidence}\n")
        file.write(f"- **Root Cause:** {root_cause}\n")
        file.write(f"- **Proposed Fix:**\n```cisco\n{proposed_fix}\n```\n")
        file.write(f"- **Human Action:** `{status}`\n")
        file.write(f"- **Auditor Notes:** {correction_reason}\n")
        file.write("---\n")

    return True