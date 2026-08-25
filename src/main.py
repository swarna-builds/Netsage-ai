import os
from google import genai
from rule_checker import check_known_rules
from human_review import review_diagnosis
from logger import log_case

def run_netsage_diagnosis(problem_text: str):
    print("\n" + "="*40)
    print("--- NetSage AI Diagnostic Pipeline ---")
    print("="*40)
    
    diagnosis_payload = {}

    # Step 1: Check Deterministic Rules
    rule_result = check_known_rules(problem_text)
    if rule_result["matched"]:
        diagnosis_payload = {
            "source": "Rule Engine (Fast Match)",
            "root_cause": rule_result["root_cause"],
            "fix": rule_result["fix"]
        }
    else:
        # Step 2: Fallback to Gemini AI
        print("\n[SOURCE: Gemini AI Fallback]")
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        
        with open("prompts/diagnose_prompt.md", "r") as f:
            prompt_template = f.read()
            
        full_prompt = prompt_template.replace("{{PROBLEM}}", problem_text)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        
        diagnosis_payload = {
            "source": "Gemini AI",
            "root_cause": "AI Analysis",
            "fix": response.text
        }

    # Step 3: Human-in-the-Loop Review
    approved, final_fix = review_diagnosis(diagnosis_payload)
    status = "APPROVED" if approved else "REJECTED"

    if approved:
        print(f"\n[EXECUTION] Executing Fix: {final_fix}")
    else:
        print("\n[EXECUTION] Action halted by administrator.")

    # Step 4: Save Case Log
    log_case(
        problem=problem_text,
        source=diagnosis_payload["source"],
        root_cause=diagnosis_payload["root_cause"],
        proposed_fix=final_fix if final_fix else diagnosis_payload["fix"],
        status=status
    )

if __name__ == "__main__":
    # Interactive CLI input
    user_problem = input("Enter network problem description: ").strip()
    if user_problem:
        run_netsage_diagnosis(user_problem)
    else:
        print("No input provided. Exiting.")