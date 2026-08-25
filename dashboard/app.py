import streamlit as st
import pandas as pd
import plotly.express as px
import json
import sys
import os

# Add src directory to python path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from rule_checker import check_known_rules
from logger import log_case
from guardrails import audit_proposed_fix
from cli_generator import generate_cisco_cli
from google import genai

# Page Configuration
st.set_page_config(
    page_title="NetSage AI | NOC Operations",
    page_icon="⚡",
    layout="wide"
)

# Custom Command-Center Styling
st.markdown("""
<style>
    /* Dark Theme Accent Header */
    .noc-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border-left: 6px solid #38bdf8;
        padding: 20px 24px;
        border-radius: 8px;
        margin-bottom: 24px;
        color: #f8fafc;
    }
    .noc-title {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        color: #f8fafc;
    }
    .noc-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    
    /* Custom Status Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-rule { background-color: #dcfce7; color: #166534; }
    .badge-ai { background-color: #e0f2fe; color: #075985; }
    .badge-pass { background-color: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-warn { background-color: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }

    /* Button Customization */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        height: 2.8rem !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# NOC Top Banner Header
st.markdown("""
<div class="noc-header">
    <div class="noc-title">⚡ NetSage AI — Intelligent Network Operations Center</div>
    <div class="noc-subtitle">Hybrid Diagnostic Engine • Safety Guardrail Verification • Automated Cisco IOS CLI Synthesizer</div>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2 = st.tabs(["🔧 Incident Workbench", "📊 Responsible AI Audit & Analytics"])

# ==========================================
# TAB 1: INCIDENT WORKBENCH
# ==========================================
with tab1:
    col_input, col_output = st.columns([1, 1.1], gap="large")

    # LEFT COLUMN: INPUT SECTION
    with col_input:
        st.markdown("##### 1. Incident Input & Telemetry")
        problem_input = st.text_area(
            label="Enter network symptoms, topology notes, or paste Cisco show-command outputs:",
            placeholder="e.g., Host in VLAN 20 gets APIPA 169.254.x.x address.\ne.g., show interface status shows FastEthernet0/1 duplex mismatch.",
            height=210
        )
        
        run_btn = st.button("🔍 Execute Diagnostic Workflow", use_container_width=True)

        if run_btn:
            if problem_input.strip():
                # Step 1: Check Local Deterministic Rule Engine
                rule_result = check_known_rules(problem_input)
                
                if rule_result["matched"]:
                    st.session_state['diag'] = {
                        "source": "Rule Engine",
                        "root_cause": rule_result["root_cause"],
                        "osi_layer": rule_result["osi_layer"],
                        "confidence": rule_result["confidence"],
                        "evidence": rule_result["evidence"],
                        "next_command": rule_result["next_command"],
                        "fix": rule_result["fix"]
                    }
                else:
                    # Step 2: Query Gemini AI Engine
                    with st.spinner("🤖 Analyzing topology telemetry with Gemini AI..."):
                        try:
                            client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
                            with open("prompts/diagnose_prompt.md", "r") as f:
                                prompt_template = f.read()
                            
                            full_prompt = prompt_template.replace("{{PROBLEM}}", problem_input)
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=full_prompt
                            )
                            
                            raw_text = response.text.strip().replace("```json", "").replace("```", "")
                            ai_data = json.loads(raw_text)
                            
                            st.session_state['diag'] = {
                                "source": "Gemini AI",
                                "root_cause": ai_data.get("root_cause", "Analysis completed"),
                                "osi_layer": ai_data.get("osi_layer", "Layer 3"),
                                "confidence": ai_data.get("confidence", "Medium"),
                                "evidence": ai_data.get("evidence", "Command output matched pattern"),
                                "next_command": ai_data.get("next_command", "show ip route"),
                                "fix": ai_data.get("fix", "Check interface configuration")
                            }
                        except Exception as e:
                            st.error(f"Error parsing AI diagnosis: {e}")

                st.session_state['current_problem'] = problem_input
            else:
                st.warning("⚠️ Please provide symptom text or show-command output to initiate diagnosis.")

    # RIGHT COLUMN: OUTPUT & HUMAN OVERSIGHT
    with col_output:
        st.markdown("##### 2. Diagnostic Analysis & Automation")
        
        if 'diag' in st.session_state:
            diag = st.session_state['diag']
            
            # Source Badge Tag
            badge_class = "badge-rule" if "Rule" in diag["source"] else "badge-ai"
            st.markdown(f"**Diagnostic Source:** <span class='badge {badge_class}'>{diag['source']}</span>", unsafe_allow_html=True)
            st.write("")

            # Top Metrics Dashboard
            m1, m2, m3 = st.columns(3)
            m1.metric("OSI Layer", diag["osi_layer"])
            m2.metric("Confidence", diag["confidence"])
            m3.metric("Verification Tool", diag["next_command"])
            
            st.divider()

            # Structured Diagnosis Details
            st.markdown(f"**Root Cause Summary:**")
            st.info(f"**{diag['root_cause']}**\n\n*Evidence:* {diag['evidence']}")
            
            # Guardrails Audit Check
            is_safe, safety_msg = audit_proposed_fix(diag['fix'])
            
            if is_safe:
                st.markdown("<span class='badge badge-pass'>🛡️ Safety Check Passed</span>", unsafe_allow_html=True)
                st.caption(safety_msg)
                
                st.markdown("**Generated Cisco IOS Remediation Script:**")
                cli_code = generate_cisco_cli(diag['fix'], diag['osi_layer'])
                st.code(cli_code, language="text")
            else:
                st.markdown("<span class='badge badge-warn'>⚠️ Safety Block Triggered</span>", unsafe_allow_html=True)
                st.error(safety_msg)

            st.divider()

            # Human-In-The-Loop Approval Section
            st.markdown("##### 3. Responsible AI Human Oversight")
            with st.form("human_approval_form"):
                status_choice = st.radio(
                    "Human Review Action:", 
                    ["ACCEPTED", "EDITED", "REJECTED"], 
                    horizontal=True
                )
                
                reason = st.text_input(
                    "Correction / Approval Notes (Required for EDITED or REJECTED):", 
                    value="N/A"
                )
                
                submit_review = st.form_submit_button("💾 Commit Decision to Responsible AI Log")
                
                if submit_review:
                    log_case(
                        problem=st.session_state['current_problem'],
                        source=diag["source"],
                        root_cause=diag["root_cause"],
                        #osi_layer=diag["osi_layer"],
                        confidence=diag["confidence"],
                        next_command=diag["next_command"],
                        proposed_fix=diag["fix"],
                        status=status_choice,
                        correction_reason=reason
                    )
                    st.success(f"✅ Case logged successfully as **{status_choice}**!")
        else:
            st.info("👈 Enter incident telemetry on the left panel and click **Execute Diagnostic Workflow**.")

# ==========================================
# TAB 2: RESPONSIBLE AI LOGS & ANALYTICS
# ==========================================
with tab2:
    st.markdown("##### Audit Dashboard & Operational Governance")
    
    if os.path.exists("data/cases.csv"):
        df = pd.read_csv("data/cases.csv")
        
        # Performance Indicators
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Logged Cases", len(df))
        kpi2.metric("Rule Engine Matches", len(df[df["Source"].str.contains("Rule", na=False)]))
        kpi3.metric("AI Assisted Diagnoses", len(df[df["Source"].str.contains("Gemini", na=False)]))
        
        human_corrections = len(df[df['Status'].isin(['EDITED', 'REJECTED'])])
        kpi4.metric("Human Interventions", human_corrections)

        st.divider()

        # ==========================================
        # VISUAL ANALYTICS SECTION (CHARTS)
        # ==========================================
        st.markdown("##### 📈 Diagnostic & Governance Analytics")
        
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            # Chart 1: Human Reviewer Decisions (Donut Chart)
            status_counts = df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            fig_status = px.pie(
                status_counts, 
                values='Count', 
                names='Status', 
                title='Human Reviewer Action Breakdown',
                color='Status',
                color_discrete_map={
                    'ACCEPTED': '#22c55e', 
                    'EDITED': '#f59e0b', 
                    'REJECTED': '#ef4444'
                },
                hole=0.4
            )
            fig_status.update_layout(margin=dict(t=40, b=20, l=10, r=10), height=300)
            st.plotly_chart(fig_status, use_container_width=True)

        with chart_col2:
            # Chart 2: Incidents Distribution by OSI Layer (Bar Chart)
            osi_col = 'OSI_Layer' if 'OSI_Layer' in df.columns else 'OSI Layer'
            if osi_col in df.columns:
                osi_counts = df[osi_col].value_counts().reset_index()
                osi_counts.columns = ['OSI Layer', 'Count']

                fig_osi = px.bar(
                    osi_counts, 
                    x='OSI Layer', 
                    y='Count', 
                    title='Incidents Distribution by OSI Layer',
                    color='OSI Layer',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_osi.update_layout(margin=dict(t=40, b=20, l=10, r=10), height=300, showlegend=False)
                st.plotly_chart(fig_osi, use_container_width=True)

        st.divider()
        
        # Filterable Data Table
        st.markdown("##### Audit Trail Logs")
        selected_status = st.multiselect(
            "Filter Table by Status:", 
            options=["ACCEPTED", "EDITED", "REJECTED"], 
            default=["ACCEPTED", "EDITED", "REJECTED"]
        )
        
        filtered_df = df[df["Status"].isin(selected_status)]
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No audit dataset found (`data/cases.csv`). Run `python src/populate_dataset.py` to populate test scenarios.")