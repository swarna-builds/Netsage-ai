# NetSage AI — Responsible AI & Human-in-the-Loop Log

Per project requirements, human reviewers must approve, edit, or reject all AI-generated diagnoses before applying fixes to production network devices. Below are 5 cases where human intervention corrected or rejected the AI's output:

| Case ID | Symptom / Input | AI Proposed Fix | Reviewer Action | Human Correction Reason |
|---------|-----------------|-----------------|-----------------|--------------------------|
| 1 | High latency occurs across BGP peering link | Reset BGP peer connection | EDITED | Preferred adjusting Local Preference over resetting active peer. |
| 2 | Internal clients failing to resolve local domain | Change primary DNS server | EDITED | Issue resolved by clearing stale client DNS cache instead of changing DNS. |
| 3 | SSH succeeds but Telnet fails | Enable Telnet on router | REJECTED | Rejected to maintain zero-trust security policy (Telnet is insecure). |
| 4 | High CPU utilization on core switch (98%) | Reboot core switch immediately | REJECTED | Reboot causes unacceptable downtime; resolved STP loop manually. |
| 5 | VPN tunnel Phase 2 negotiation failure | Rebuild VPN tunnel from scratch | EDITED | Resolved by updating crypto ACL matching rules without full rebuild. |