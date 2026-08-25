import re

BLOCKED_PATTERNS = [
    r"\breload\b",
    r"\berase\b",
    r"\bformat\b",
    r"\bdelete\b",
    r"\bno\s+ip\s+routing\b",
    r"\bshutdown\b\s+range",
    r"\bwrite\s+erase\b"
]

def audit_proposed_fix(fix_text: str) -> tuple[bool, str]:
    """
    Scans proposed fixes or Cisco commands for high-risk operations.
    Returns (is_safe, warning_message).
    """
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, fix_text, re.IGNORECASE):
            return False, f"GUARDRAIL BLOCKED: Dangerous command pattern detected ('{pattern}'). System execution halted."
            
    return True, "PASSED: Command set verified safe for production environments."