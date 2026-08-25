# ⚡ NetSage AI — Intelligent Network Operations Center

An enterprise-grade, hybrid diagnostic engine and responsible AI system designed for Network Operations Centers (NOC). NetSage AI automatically analyzes network telemetry, maps issues to OSI layers, executes execution guardrails, generates Cisco IOS CLI fixes, and maintains a strict human-in-the-loop audit trail.

---

## 🌟 Key Features

* **Hybrid Diagnostic Engine:** Combines a deterministic local rule engine for sub-millisecond pattern matching with Google Gemini 2.5 Flash for complex, multi-variable root-cause analysis.
* **Safety Guardrail Audit:** Automatically screens generated remediation scripts for high-risk commands to prevent accidental outages.
* **Cisco IOS CLI Synthesizer:** Automatically compiles standard network operational fixes into precise, copy-pasteable Cisco configuration snippets.
* **Responsible AI and Human Oversight:** Requires human operator review (ACCEPTED, EDITED, REJECTED) for every AI suggestion before execution.
* **Interactive Analytics Dashboard:** Built with Streamlit and Plotly to visually present incident trends, OSI layer distribution, and governance metrics.

---

## 📁 Repository Structure

```text
NetSage-AI/
├── dashboard/
│   └── app.py                  # Main Streamlit Command-Center Dashboard
├── data/
│   └── cases.csv               # Audit dataset (30 pre-tested NOC scenarios)
├── prompts/
│   └── diagnose_prompt.md      # Structured prompt template for Gemini AI
├── src/
│   ├── ai_diagnosis.py         # Gemini AI API integration layer
│   ├── cli_generator.py        # Cisco IOS CLI script generator
│   ├── guardrails.py           # Safety checks and high-risk command blocker
│   ├── logger.py               # CSV and Markdown audit logger
│   ├── populate_dataset.py     # Script to populate test cases
│   └── rule_checker.py         # Local deterministic pattern-matching engine
├── .gitignore                  # Excluded sensitive environment files
├── README.md                   # Project documentation
└── RESPONSIBLE_AI_LOG.md       # Human oversight decision history