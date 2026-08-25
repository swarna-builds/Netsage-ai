import csv
import os
from datetime import datetime

CSV_FILE = "data/cases.csv"

def log_case(
    problem: str, 
    source: str, 
    root_cause: str, 
    osi_layer: str, 
    confidence: str, 
    next_command: str, 
    proposed_fix: str, 
    status: str, 
    correction_reason: str = "N/A"
):
    """
    Appends incident details to the cases CSV file including OSI layer,
    confidence metrics, and human correction feedback.
    """
    file_exists = os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Write updated header if file is new or empty
        if not file_exists:
            writer.writerow([
                "Timestamp", 
                "Problem", 
                "Source", 
                "Root Cause", 
                "OSI Layer", 
                "Confidence", 
                "Next Command", 
                "Proposed Fix", 
                "Status", 
                "Correction Reason"
            ])
            
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            problem,
            source,
            root_cause,
            osi_layer,
            confidence,
            next_command,
            proposed_fix,
            status,
            correction_reason
        ])
    print("[LOGGING] Enhanced record saved to data/cases.csv")