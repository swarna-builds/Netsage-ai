def check_known_rules(problem_description: str):
    text = problem_description.lower()

    if "incorrect ip" in text or "wrong ip" in text or "apipa" in text or "169.254" in text:
        return {
            "matched": True,
            "root_cause": "IP Configuration Error / DHCP Scope Mismatch",
            "osi_layer": "Layer 3",
            "confidence": "High",
            "evidence": "Assigned IP address does not match local subnet mask/VLAN schema",
            "next_command": "show ip interface brief",
            "fix": "Reconfigure static IP setting or issue release/renew on host."
        }

    if "duplex mismatch" in text or "speed mismatch" in text:
        return {
            "matched": True,
            "root_cause": "Physical / Data Link Layer Mismatch",
            "osi_layer": "Layer 2",
            "confidence": "High",
            "evidence": "Late collisions or interface errors reported on switch port",
            "next_command": "show interface status",
            "fix": "Configure speed and duplex settings manually or enable auto-negotiation on both sides."
        }

    return {"matched": False}