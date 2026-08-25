def review_diagnosis(diagnosis_data: dict):
    """
    Presents the diagnosis to a human reviewer for approval.
    """
    print("\n--- HUMAN REVIEW REQUIRED ---")
    print(f"Source: {diagnosis_data.get('source', 'Unknown')}")
    print(f"Root Cause: {diagnosis_data.get('root_cause')}")
    print(f"Proposed Fix: {diagnosis_data.get('fix')}")
    print("-" * 30)

    decision = input("Approve fix? (y/n/edit): ").strip().lower()

    if decision == "y":
        print("[STATUS] Fix APPROVED. Proceeding to execution.")
        return True, diagnosis_data["fix"]
    elif decision == "edit":
        new_fix = input("Enter corrected fix: ").strip()
        print("[STATUS] Fix MODIFIED by reviewer.")
        return True, new_fix
    else:
        print("[STATUS] Fix REJECTED. Escalating to Level 2 Support.")
        return False, None

if __name__ == "__main__":
    sample_diag = {
        "source": "Rule Engine",
        "root_cause": "IP Configuration Error",
        "fix": "Reconfigure IP to 192.168.1.50/24"
    }
    review_diagnosis(sample_diag)