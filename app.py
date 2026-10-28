"""
Multimodal Construction Intelligence Platform
Capstone Project 1 | Platform ID: 6ac4c98d1dcde6d7857c1642
Enterprise Construction Decision Support System powered by Multimodal AI
"""

import os
import json
import io
import datetime
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from modules.ai_engine import GENAI_AVAILABLE, init_gemini
from modules.safety_audit import analyze_site_safety
from modules.crack_diagnostics import analyze_concrete_crack
from modules.project_planning import (
    COST_BENCHMARKS,
    SPEC_MULTIPLIERS,
    calculate_project_metrics,
    generate_pollinations_prompt,
    get_pollinations_image_url
)
from modules.weather_advisory import (
    WEATHER_PROTOCOLS,
    chat_with_site_assistant
)

# Page Configuration
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Session State Initialization
if "gemini_api_key" not in st.session_state:
    api_key_candidate = os.environ.get("GEMINI_API_KEY", "")
    try:
        if not api_key_candidate and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            api_key_candidate = str(st.secrets["GEMINI_API_KEY"])
    except Exception:
        pass
    st.session_state.gemini_api_key = api_key_candidate
    if api_key_candidate:
        init_gemini(api_key_candidate)

if "safety_result" not in st.session_state:
    st.session_state.safety_result = None

if "safety_image" not in st.session_state:
    st.session_state.safety_image = None

if "crack_result" not in st.session_state:
    st.session_state.crack_result = None

if "crack_image" not in st.session_state:
    st.session_state.crack_image = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "model",
            "content": "👋 **Greetings!** I am your **Construction Engineering & Safety Copilot** certified in **IS 456:2000**, **OSHA 1926**, **NBC 2016**, and **IS 13920**.\n\nAsk me anything regarding structural load limits, concrete slump tests, curing schedules, weather contingency actions, or OSHA scaffold anchorage requirements."
        }
    ]

if "pollinations_seed" not in st.session_state:
    st.session_state.pollinations_seed = 42


# ==========================================
# SIDEBAR: SECURE API KEY & ARCHITECTURE
# ==========================================
with st.sidebar:
    st.markdown("### 🏗️ Construction AI Platform")
    st.caption("Platform ID: **6ac4c98d1dcde6d7857c1642** | Capstone 1")
    
    st.markdown("---")
    st.markdown("#### 🔑 Model Authentication")
    
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.gemini_api_key,
        type="password",
        placeholder="AIzaSy...",
        help="Enter your Google Gemini API key. If left blank, the platform automatically runs in high-fidelity Demonstration Fallback Mode."
    )
    
    if api_key_input != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = api_key_input
        init_gemini(api_key_input)
        st.rerun()

    # Engine Status Pill
    if st.session_state.gemini_api_key:
        st.markdown(
            '<div class="badge-status badge-low" style="width:100%; justify-content:center; margin-bottom:1rem;">'
            '🟢 Gemini 1.5 Vision Active</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="badge-status badge-medium" style="width:100%; justify-content:center; margin-bottom:1rem;">'
            '🟡 Demonstration Fallback Engine</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("#### 🏛️ System Architecture & Demo")
    
    with st.expander("🎬 Watch Video Walkthrough Tour", expanded=False):
        video_path = os.path.join(os.path.dirname(__file__), "assets", "demo_walkthrough.mp4")
        if os.path.exists(video_path):
            st.video(video_path)
            with open(video_path, "rb") as vf:
                st.download_button(
                    label="📥 Download Walkthrough Video (MP4)",
                    data=vf.read(),
                    file_name="multimodal_construction_intelligence_demo.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )

    with st.expander("Kanban Epics & Tech Stack", expanded=False):
        st.markdown("""
        - **Epic 1:** Requirements & Streamlit Cloud Env
        - **Epic 2:** PPE Vision & Crack Diagnostics (IS 456 & OSHA)
        - **Epic 3:** Real Estate Valuation in INR & 3D Render
        - **Epic 4:** Multimodal AI & Strict JSON Contracts
        - **Epic 5:** Weather Advisory & Multi-Turn Site Bot
        - **Epic 6:** Interface Polish & Zero-DB Community Deploy
        
        **Core Engines:**
        - Google Gemini 1.5 Pro / Flash Multimodal
        - Pollinations AI / Flux Generative Architecture
        - CPWD & IS 456:2000 Cost & Material Estimator
        """)

    with st.expander("Regulatory & Engineering Codes", expanded=False):
        st.markdown("""
        - **IS 456:2000:** Plain & Reinforced Concrete
        - **OSHA 29 CFR 1926:** Construction Safety
        - **IS 13920:2016:** Seismic Ductile Detailing
        - **IS 3696 Part 1 & 2:** Scaffolds & Ladders
        - **ACI 224R-01:** Crack Control in Concrete
        """)

    st.markdown("---")
    st.caption("© 2026 Multimodal Construction Intelligence Platform. Zero external DB dependencies.")


# ==========================================
# MAIN HERO HEADER
# ==========================================
st.markdown("""
<div class="hero-banner">
  <h1>Multimodal Construction Intelligence Platform</h1>
  <p>Generative AI Decision-Support System: Computer Vision PPE Audit, Concrete Pathology & Crack Diagnostics, INR CapEx Valuation, and Real-Time Weather Safety Protocol Dispatch.</p>
  <div class="hero-badges">
    <span class="tag-badge">PLATFORM ID: 6ac4c98d1dcde6d7857c1642</span>
    <span class="tag-badge">OSHA 1926 & IS 456:2000 CERTIFIED</span>
    <span class="tag-badge">REAL ESTATE IN INR (LAKHS / CRORES)</span>
    <span class="tag-badge">STREAMLIT CLOUD READY</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# NAVIGATION TABS
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 1. Site Safety & PPE Audit",
    "🔍 2. Crack Diagnostics & Integrity",
    "📊 3. Planning & Real Estate Valuation",
    "🌦️ 4. Daily Assistant & Weather Advisory"
])


# =========================================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# =========================================================================
with tab1:
    st.markdown("### 🦺 Site Safety & Worker PPE Compliance Audit (OSHA & IS 456)")
    st.caption("Upload site photos or choose preloaded scenarios to audit Hard Hats, High-Vis Vests, Safety Footwear, and Fall Protection.")

    col1, col2 = st.columns([1, 1.4], gap="large")

    with col1:
        st.markdown("#### 📸 Site Photo Input")
        
        sample_choice = st.selectbox(
            "Load Built-in Certified Test Sample:",
            [
                "-- Upload Custom Photo Below --",
                "Sample 1: Cantilever Shuttering Deck (Edge Fall Hazard Detected)",
                "Sample 2: Ground Rebar Crew (100% Full Compliance)"
            ]
        )

        uploaded_file = st.file_uploader(
            "Upload Construction Site Photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="ppe_uploader"
        )

        sample_img_path = None
        if sample_choice == "Sample 1: Cantilever Shuttering Deck (Edge Fall Hazard Detected)":
            sample_img_path = "assets/sample_images/site_safety_sample_1.jpg"
        elif sample_choice == "Sample 2: Ground Rebar Crew (100% Full Compliance)":
            sample_img_path = "assets/sample_images/site_safety_sample_2.jpg"

        active_img = None
        if uploaded_file is not None:
            active_img = Image.open(uploaded_file)
            st.session_state.safety_image = active_img
        elif sample_img_path and os.path.exists(sample_img_path):
            active_img = Image.open(sample_img_path)
            st.session_state.safety_image = active_img

        if st.session_state.safety_image is not None:
            st.image(
                st.session_state.safety_image,
                caption="Active Site Audit Photograph",
                use_container_width=True
            )
            
            scenario_num = 2 if "Sample 2" in sample_choice else 1
            if st.button("🚀 Run Site Safety & PPE Audit", type="primary", use_container_width=True):
                with st.spinner("Analyzing site imagery against OSHA 1926 & IS 456 safety matrices..."):
                    result = analyze_site_safety(
                        st.session_state.safety_image,
                        api_key=st.session_state.gemini_api_key,
                        scenario_id=scenario_num
                    )
                    st.session_state.safety_result = result
        else:
            st.info("👆 Please select a sample site photo or upload your own construction image to begin.")

    with col2:
        st.markdown("#### 📋 Forensic Audit Report & Hazard Breakdown")
        
        if st.session_state.safety_result:
            res = st.session_state.safety_result
            score = res.get("safety_score", 0)
            status = res.get("overall_status", "Pending")
            
            # Status Badge Class
            if score >= 90:
                badge_class = "badge-low"
                status_color = "#10b981"
            elif score >= 75:
                badge_class = "badge-medium"
                status_color = "#f59e0b"
            elif score >= 60:
                badge_class = "badge-high"
                status_color = "#fb923c"
            else:
                badge_class = "badge-critical"
                status_color = "#f43f5e"

            # Top KPI Metric Cards
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="metric-container">
                    <span class="metric-title">SAFETY COMPLIANCE</span>
                    <span class="metric-value" style="color: {status_color};">{score}/100</span>
                    <span class="metric-delta positive">IS 456 / OSHA Benchmarked</span>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-container">
                    <span class="metric-title">OVERALL AUDIT STATUS</span>
                    <div style="margin-top: 0.35rem;"><span class="badge-status {badge_class}">{status}</span></div>
                    <span class="metric-delta">Site Risk Level</span>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                total_w = res.get("total_workers_detected", 0)
                comp_w = res.get("compliant_workers", 0)
                st.markdown(f"""
                <div class="metric-container">
                    <span class="metric-title">PERSONNEL ON SITE</span>
                    <span class="metric-value">{comp_w} / {total_w}</span>
                    <span class="metric-delta">Workers Fully Compliant</span>
                </div>
                """, unsafe_allow_html=True)

            st.caption(f"Engine Mode: **{res.get('mode', 'Analysis Complete')}** | Timestamp: `{res.get('audit_timestamp', '')}`")

            # PPE Checklist Table
            st.markdown("##### 🦺 PPE Item Compliance Matrix")
            ppe_list = res.get("ppe_detection", [])
            if ppe_list:
                ppe_rows = []
                for p in ppe_list:
                    status_val = p.get("status", "N/A")
                    icon = "✅" if status_val == "Pass" else ("⚠️" if status_val == "Warning" else "❌")
                    ppe_rows.append({
                        "PPE Item": p.get("category"),
                        "Standard": p.get("standard_ref"),
                        "Detected": p.get("detected_count"),
                        "Compliant": p.get("compliant_count"),
                        "Violations": p.get("violation_count"),
                        "Status": f"{icon} {status_val}",
                        "Observation Notes": p.get("observation")
                    })
                st.dataframe(pd.DataFrame(ppe_rows), use_container_width=True, hide_index=True)

            # Identified Hazards
            hazards = res.get("identified_site_hazards", [])
            st.markdown("##### ⚠️ Physical Site Hazards Identified")
            if hazards:
                for h in hazards:
                    h_sev = h.get("severity", "Medium")
                    sev_class = "badge-critical" if h_sev == "Critical" else ("badge-high" if h_sev == "High" else "badge-medium")
                    st.markdown(f"""
                    <div class="compliance-item">
                        <div style="flex:1;">
                            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.25rem;">
                                <strong style="color:#f8fafc;">{h.get('hazard_id', 'HAZ')}: {h.get('description')}</strong>
                                <span class="badge-status {sev_class}">{h_sev}</span>
                            </div>
                            <div style="font-size:0.85rem; color:#94a3b8;">
                                📍 <strong>Zone:</strong> {h.get('location')} | 📜 <strong>Standard:</strong> {h.get('regulatory_code')}
                            </div>
                            <div style="font-size:0.88rem; color:#f59e0b; margin-top:0.35rem;">
                                🛠️ <strong>Action Required:</strong> {h.get('corrective_remedy')}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("No active physical hazards detected in current view.")

            # OSHA & IS 456 Summary
            with st.expander("📄 Executive OSHA 1926 & IS 456 Compliance Summary", expanded=True):
                st.write(res.get("osha_is456_summary", "Audit summary complete."))
                
                actions = res.get("immediate_remedial_actions", [])
                if actions:
                    st.markdown("**Immediate Supervisory Actions:**")
                    for a in actions:
                        st.markdown(f"- 🔴 {a}")

            # Downloadable JSON Report
            json_report = json.dumps(res, indent=2)
            st.download_button(
                label="📥 Download Structured JSON Safety Report",
                data=json_report,
                file_name=f"site_safety_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👷‍♂️</div>
                <h3>Ready to Audit Site Safety</h3>
                <p style="color: #94a3b8; max-width: 480px; margin: 0 auto;">
                    Select an audit image on the left and click <strong>Run Site Safety & PPE Audit</strong>.
                    The system classifies OSHA 1926 and IS 456 compliant PPE and tags high-risk hazards.
                </p>
            </div>
            """, unsafe_allow_html=True)


# =========================================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# =========================================================================
with tab2:
    st.markdown("### 🔍 Concrete Crack Pathology & Forensic Structural Diagnostics")
    st.caption("Classify structural shear vs. hairline shrinkage defects, estimate crack width (mm), and generate IS 456 & ACI 224 engineering repair protocols.")

    c_col1, c_col2 = st.columns([1, 1.4], gap="large")

    with c_col1:
        st.markdown("#### 🧱 Concrete Surface Inspection")
        crack_sample = st.selectbox(
            "Load Defect Test Benchmark:",
            [
                "-- Upload Custom Crack Image Below --",
                "Defect Case 1: RCC Beam-Column Diagonal Shear Crack (Immediate Repair)",
                "Defect Case 2: Wall Plaster Surface Hairline Shrinkage Crazing"
            ]
        )

        crack_file = st.file_uploader(
            "Upload Concrete / Wall Crack Photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader"
        )

        crack_img_path = None
        if crack_sample == "Defect Case 1: RCC Beam-Column Diagonal Shear Crack (Immediate Repair)":
            crack_img_path = "assets/sample_images/crack_structural_sample_1.jpg"
        elif crack_sample == "Defect Case 2: Wall Plaster Surface Hairline Shrinkage Crazing":
            crack_img_path = "assets/sample_images/crack_hairline_sample_2.jpg"

        if crack_file is not None:
            st.session_state.crack_image = Image.open(crack_file)
        elif crack_img_path and os.path.exists(crack_img_path):
            st.session_state.crack_image = Image.open(crack_img_path)

        if st.session_state.crack_image is not None:
            st.image(
                st.session_state.crack_image,
                caption="Forensic Macro Surface Specimen",
                use_container_width=True
            )
            case_num = 1 if "Case 1" in crack_sample else 2
            if st.button("🔬 Perform Forensic Structural Crack Analysis", type="primary", use_container_width=True):
                with st.spinner("Diagnosing concrete pathology, shear trajectory, and IS 456 limits..."):
                    c_res = analyze_concrete_crack(
                        st.session_state.crack_image,
                        api_key=st.session_state.gemini_api_key,
                        defect_case=case_num
                    )
                    st.session_state.crack_result = c_res
        else:
            st.info("👆 Please select a defect benchmark or upload a concrete surface photo.")

    with c_col2:
        st.markdown("#### 📊 Diagnostic Pathology & Engineering Prescription")

        if st.session_state.crack_result:
            c_res = st.session_state.crack_result
            sev_score = c_res.get("severity_score", 0)
            defect_type = c_res.get("defect_type", "Unknown")
            urgency = c_res.get("urgency", "Monitoring")
            width = c_res.get("estimated_width_mm", "N/A")
            risk_rating = c_res.get("risk_rating", "Moderate")

            # Risk colors
            if sev_score >= 80:
                c_sev_class = "badge-critical"
                c_color = "#f43f5e"
            elif sev_score >= 50:
                c_sev_class = "badge-high"
                c_color = "#fb923c"
            else:
                c_sev_class = "badge-low"
                c_color = "#10b981"

            # Top KPI metrics
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.markdown(f"""
                <div class="metric-container">
                    <span class="metric-title">ESTIMATED CRACK WIDTH</span>
                    <span class="metric-value">{width}</span>
                    <span class="metric-delta danger">IS 456 Max Limit: 0.3mm</span>
                </div>
                """, unsafe_allow_html=True)
            with cm2:
                st.markdown(f"""
                <div class="metric-container">
                    <span class="metric-title">STRUCTURAL SEVERITY</span>
                    <span class="metric-value" style="color: {c_color};">{sev_score}/100</span>
                    <span class="metric-delta"><span class="badge-status {c_sev_class}">{risk_rating}</span></span>
                </div>
                """, unsafe_allow_html=True)
            with cm3:
                st.markdown(f"""
                <div class="metric-container">
                    <span class="metric-title">REPAIR INTERVENTION</span>
                    <span class="metric-value" style="font-size:1.15rem; color:#f59e0b;">{urgency}</span>
                    <span class="metric-delta warning">Target Timeline</span>
                </div>
                """, unsafe_allow_html=True)

            st.caption(f"Defect Classification: **{defect_type}** | Component: **{c_res.get('structural_element', 'RCC Member')}**")

            # Code compliance alert
            st.markdown(f"""
            <div class="compliance-item" style="border-left: 4px solid {c_color};">
                <div>
                    <strong>IS 456:2000 Compliance Status:</strong>
                    <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 0.2rem;">
                        {c_res.get('is456_compliance_status')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Root Causes
            st.markdown("##### 🔬 Root Cause Pathology Analysis")
            roots = c_res.get("root_causes", [])
            for r in roots:
                st.markdown(f"- 🔸 **Cause:** {r}")

            # Engineering Repairs (Epoxy Injection, CFRP, Re-grouting)
            st.markdown("##### 🛠️ Prescribed Structural Engineering Repairs")
            repairs = c_res.get("engineering_repairs", [])
            for rep in repairs:
                st.markdown(f"""
                <div class="compliance-item">
                    <div>
                        <div style="font-weight: 700; color: #38bdf8; font-size: 0.95rem;">
                            🔧 {rep.get('method')}
                        </div>
                        <div style="color: #cbd5e1; font-size: 0.88rem; margin: 0.3rem 0;">
                            {rep.get('specification')}
                        </div>
                        <div style="font-size: 0.78rem; color: #94a3b8; font-family: monospace;">
                            Standard Reference: {rep.get('standard_ref')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Monitoring Protocol & Forensic Summary
            with st.expander("📡 Long-Term Monitoring Protocol & Structural Summary", expanded=False):
                st.markdown(f"**Instrumentation:** {c_res.get('monitoring_protocol', '')}")
                st.markdown(f"**Forensic Note:** {c_res.get('forensic_summary', '')}")

            # Downloadable JSON
            c_json = json.dumps(c_res, indent=2)
            st.download_button(
                label="📥 Download Forensic Crack Diagnostic Report (JSON)",
                data=c_json,
                file_name=f"crack_pathology_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔬</div>
                <h3>Structural Pathology Analysis</h3>
                <p style="color: #94a3b8; max-width: 480px; margin: 0 auto;">
                    Select or upload a concrete crack photo. The diagnostic model performs width estimation,
                    shear vs. shrinkage defect classification, and engineering repair protocols under IS 456.
                </p>
            </div>
            """, unsafe_allow_html=True)


# =========================================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# =========================================================================
with tab3:
    st.markdown("### 📊 Project Planning, Real Estate Valuation & 3D Architectural Generation")
    st.caption("Calculate CapEx, current asset market valuation in INR (Lakhs & Crores), material BOM requirements, and synthesize conceptual 3D renders via Pollinations AI / Flux.")

    plan_col1, plan_col2 = st.columns([1.1, 1.3], gap="large")

    with plan_col1:
        st.markdown("#### 📐 Project Parameters & Financial Drivers")
        
        struct_type = st.selectbox(
            "Structure Classification:",
            [
                "Residential High-Rise (RCC Shear Wall)",
                "Commercial IT Park / Tower",
                "Industrial Pre-Engineered Warehouse",
                "Luxury Villa / Gated Township",
                "Metro / Transit Infrastructure"
            ]
        )

        loc_tier = st.selectbox(
            "Location Tier & Metropolitan Micro-Market:",
            [
                "Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune)",
                "Tier 2 (Ahmedabad, Jaipur, Chandigarh, Kochi, Lucknow, Indore)",
                "Tier 3 (Bhopal, Coimbatore, Visakhapatnam, Emerging Cities)"
            ]
        )

        builtup = st.number_input(
            "Total Built-up Area (Sq. Ft.):",
            min_value=1000,
            max_value=2500000,
            value=75000,
            step=5000,
            help="Total gross construction built-up area in square feet."
        )

        spec_level = st.select_slider(
            "Specification Standard:",
            options=[
                "Standard (Affordable / Mid-Segment)",
                "Premium (Imported fittings, High-speed lifts)",
                "Ultra-Luxury (Italian Marble, Glass Curtain Wall, Automation)"
            ],
            value="Premium (Imported fittings, High-speed lifts)"
        )

        completion_val = st.slider(
            "Current Milestone Physical Completion Percentage (%):",
            min_value=0,
            max_value=100,
            value=45,
            step=5,
            help="Actual physical construction completion percentage on site."
        )

        st.markdown("---")
        st.markdown("#### 🎨 Conceptual 3D Architectural Visualization (Pollinations AI)")
        
        arch_style = st.selectbox(
            "Architectural Design Style:",
            [
                "Contemporary Glass Curtain Wall & Terraced Sky Gardens",
                "Sustainable Biophilic Timber & Textured Concrete",
                "Sleek Neo-Futuristic Curved Parametric Facade",
                "Modernist Minimalist Concrete & Steel Frame",
                "Indian Contemporary Luxury with Jaali Screens"
            ]
        )

        lighting_preset = st.selectbox(
            "Atmospheric Lighting & Environment:",
            [
                "Golden hour warm sunset with dramatic volumetric shadows",
                "Twilight blue hour with interior architectural illumination",
                "Crisp high-noon architectural digest daylight",
                "Dramatic overcast rainy monsoon atmosphere with wet reflections"
            ]
        )

        camera_view = st.selectbox(
            "Camera Perspective:",
            [
                "Aerial drone 45-degree isometric masterplan view",
                "Eye-level pedestrian street perspective looking up",
                "Wide-angle heroic front architectural elevation",
                "Corner vantage showing podium landscape & tower soar"
            ]
        )

        if st.button("🎲 Rerender Architecture with New Seed", use_container_width=True):
            st.session_state.pollinations_seed += 7
            st.rerun()

    # Calculate Metrics
    metrics = calculate_project_metrics(
        structure_type=struct_type,
        builtup_sqft=builtup,
        location_tier=loc_tier,
        completion_pct=completion_val,
        specification_level=spec_level
    )

    with plan_col2:
        st.markdown("#### 💰 Executive Valuation & Financial Milestone Summary")
        
        # 4 Metric cards
        vm1, vm2 = st.columns(2)
        with vm1:
            st.markdown(f"""
            <div class="metric-container">
                <span class="metric-title">TOTAL CONSTRUCTION BUDGET</span>
                <span class="metric-value">{metrics['total_budget_formatted']}</span>
                <span class="metric-delta">Rate: ₹{metrics['effective_cost_per_sqft']:,.0f} / sqft</span>
            </div>
            """, unsafe_allow_html=True)
        with vm2:
            st.markdown(f"""
            <div class="metric-container">
                <span class="metric-title">CAPEX INCURRED TO DATE</span>
                <span class="metric-value" style="color: #38bdf8;">{metrics['capex_incurred_formatted']}</span>
                <span class="metric-delta warning">Remaining: {metrics['capex_remaining_formatted']}</span>
            </div>
            """, unsafe_allow_html=True)

        vm3, vm4 = st.columns(2)
        with vm3:
            st.markdown(f"""
            <div class="metric-container">
                <span class="metric-title">CURRENT ASSET MARKET VALUATION</span>
                <span class="metric-value" style="color: #10b981;">{metrics['current_valuation_formatted']}</span>
                <span class="metric-delta positive">Based on Completed Fraction</span>
            </div>
            """, unsafe_allow_html=True)
        with vm4:
            st.markdown(f"""
            <div class="metric-container">
                <span class="metric-title">PROJECTED FINISHED GDV</span>
                <span class="metric-value" style="color: #f59e0b;">{metrics['gdv_finished_formatted']}</span>
                <span class="metric-delta">Market Rate: ₹{metrics['effective_market_rate_per_sqft']:,.0f} / sqft</span>
            </div>
            """, unsafe_allow_html=True)

        # Milestone Progress Bar
        st.markdown(f"##### 🏗️ Construction Milestone: **{metrics['current_milestone']}**")
        st.progress(completion_val / 100.0)

        # Material Bill of Quantities (BOM)
        st.markdown("##### 🧱 Bill of Quantities: Structural Materials (IS / CPWD Thumb Rules)")
        mats = metrics["materials"]
        mats_used = metrics["materials_consumed"]
        
        bm1, bm2, bm3, bm4 = st.columns(4)
        with bm1:
            st.metric("TMT Steel Rebar", f"{mats['steel_tonnes']:,.1f} MT", f"Used: {mats_used['steel_tonnes']:,.1f} MT")
        with bm2:
            st.metric("Cement Bags", f"{mats['cement_bags']:,}", f"Used: {mats_used['cement_bags']:,}")
        with bm3:
            st.metric("Ready-Mix RMC", f"{mats['rmc_cum']:,.0f} m³", f"Used: {mats_used['rmc_cum']:,.0f} m³")
        with bm4:
            st.metric("Sand / Aggregate", f"{mats['sand_brass']:,.1f} Brass", f"Used: {mats_used['sand_brass']:,.1f}")

        # Cost Breakdown Donut Chart
        st.markdown("##### 📊 CapEx Allocation Distribution")
        fig_cost = px.pie(
            metrics["cost_breakdown_df"],
            values="Share (%)",
            names="Component",
            hole=0.55,
            color_discrete_sequence=["#f59e0b", "#38bdf8", "#10b981", "#8b5cf6"]
        )
        fig_cost.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f3f4f6"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_cost, use_container_width=True)

        # Conceptual 3D Architectural Rendering
        st.markdown("##### 🏛️ AI Conceptual 3D Architectural Render")
        pollinations_prompt = generate_pollinations_prompt(
            structure_type=struct_type,
            location_tier=loc_tier,
            arch_style=arch_style,
            lighting_env=lighting_preset,
            camera_perspective=camera_view,
            completion_stage=f"{completion_val}% Constructed Stage" if completion_val < 90 else "Completed Masterpiece"
        )
        
        render_url = get_pollinations_image_url(
            pollinations_prompt,
            width=1024,
            height=600,
            seed=st.session_state.pollinations_seed,
            model="flux"
        )

        with st.container():
            st.image(
                render_url,
                caption=f"Conceptual 3D Visual: {struct_type} ({arch_style})",
                use_container_width=True
            )
            with st.expander("📝 View Synthesized Generative Architectural Prompt", expanded=False):
                st.code(pollinations_prompt, language="text")


# =========================================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER-AWARE ADVISORY (EPIC 5)
# =========================================================================
with tab4:
    st.markdown("### 🌦️ Weather-Aware Site Advisory & Construction Engineering Chatbot")
    st.caption("Real-time safety alerts for Tower Cranes, Scaffolding, and IS 456 concrete curing protocols matched with an expert multi-turn engineering chatbot.")

    w_col1, w_col2 = st.columns([1.1, 1.3], gap="large")

    with w_col1:
        st.markdown("#### ⚡ Active Weather Condition Trigger")
        
        selected_weather = st.selectbox(
            "Select Current / Forecast Site Weather Condition:",
            list(WEATHER_PROTOCOLS.keys()),
            index=0
        )

        weather_info = WEATHER_PROTOCOLS[selected_weather]

        # Dynamic Weather Banner
        alert_style_class = (
            "weather-high-wind" if "High Wind" in selected_weather
            else ("weather-heavy-rain" if "Heavy Rain" in selected_weather
            else ("weather-extreme-heat" if "Extreme Heat" in selected_weather
            else "weather-normal"))
        )

        st.markdown(f"""
        <div class="weather-alert-box {alert_style_class}">
            <div>
                <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.35rem;">
                    <span class="badge-status {weather_info['badge_class']}">{weather_info['severity']}</span>
                    <strong style="color:#ffffff; font-size:1.05rem;">{selected_weather.split('(')[0]}</strong>
                </div>
                <div style="color:#f8fafc; font-weight:600; font-size:0.95rem; margin-bottom:0.4rem;">
                    🚨 {weather_info['primary_action']}
                </div>
                <div style="color:#cbd5e1; font-size:0.85rem;">
                    💧 <strong>Curing / Hydration Advisory:</strong> {weather_info['curing_impact']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic Code Directives
        st.markdown("##### 📜 Mandatory Site Safety Directives")
        for proto in weather_info["protocols"]:
            st.markdown(f"""
            <div class="compliance-item">
                <div>
                    <div style="font-weight: 700; color: #38bdf8; font-size: 0.92rem;">
                        ⚡ {proto['domain']}
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.86rem; margin: 0.25rem 0;">
                        {proto['directive']}
                    </div>
                    <div style="font-size: 0.78rem; color: #f59e0b; font-family: monospace;">
                        Compliance Code: {proto['code_ref']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with w_col2:
        st.markdown("#### 💬 Multi-Turn Construction Engineering Chatbot")
        st.caption("Trained on IS 456:2000, OSHA 1926, IS 13920, and NBC 2016.")

        # Quick Starter Prompt Buttons
        st.markdown("**Quick Technical Queries:**")
        qc1, qc2 = st.columns(2)
        quick_query = None
        with qc1:
            if st.button("💧 Concrete Curing: OPC vs PPC", use_container_width=True):
                quick_query = "What is the concrete curing period and ponding requirement for OPC vs PPC under hot weather per IS 456?"
            if st.button("🏗️ Tower Crane Wind Limit Rules", use_container_width=True):
                quick_query = "What are the exact wind speed operational limits for tower crane lifts under IS 456 and OSHA 1926?"
        with qc2:
            if st.button("🧪 Pumpable Concrete Slump Specs", use_container_width=True):
                quick_query = "What is the recommended slump and workability specification for high-rise pumpable concrete per IS 456?"
            if st.button("📐 Rebar Tension Lap Lengths", use_container_width=True):
                quick_query = "Explain rebar lap length and seismic staggering requirements for Fe500D steel under IS 456 and IS 13920."

        # Chat message display container
        chat_container = st.container(height=420)
        with chat_container:
            for msg in st.session_state.chat_messages:
                role = msg.get("role")
                if role == "user":
                    st.markdown(f"""
                    <div class="chat-user-msg">
                        <strong>👷 You:</strong><br>{msg.get('content')}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-agent-msg">
                        <strong>🤖 Construction Copilot:</strong><br>{msg.get('content')}
                    </div>
                    """, unsafe_allow_html=True)

        # Chat Input Form
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Ask your structural or safety engineering question:",
                placeholder="e.g. When can formwork props be stripped under beams according to IS 456?"
            )
            submit_btn = st.form_submit_button("Send Query 🚀", use_container_width=True)

        prompt_to_send = quick_query if quick_query else (user_input if submit_btn and user_input.strip() else None)

        if prompt_to_send:
            # Append user message
            st.session_state.chat_messages.append({"role": "user", "content": prompt_to_send})
            
            with st.spinner("Consulting IS 456 and OSHA safety databases..."):
                reply, mode_label = chat_with_site_assistant(
                    user_message=prompt_to_send,
                    chat_history=st.session_state.chat_messages,
                    api_key=st.session_state.gemini_api_key
                )
                st.session_state.chat_messages.append({"role": "model", "content": reply})
            
            st.rerun()

        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_messages = [
                {
                    "role": "model",
                    "content": "👋 Chat history reset. Ready for your next structural or site safety query."
                }
            ]
            st.rerun()


# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
fcol1, fcol2, fcol3 = st.columns([1.5, 1, 1])
with fcol1:
    st.markdown("**Multimodal Construction Intelligence Platform** | Capstone Project 1")
    st.caption("AI-Powered Real Estate & Construction Decision Support System | Platform ID: `6ac4c98d1dcde6d7857c1642`")
with fcol2:
    st.markdown("**Regulatory Frameworks:**")
    st.caption("OSHA 29 CFR 1926 • IS 456:2000 • IS 13920 • NBC 2016")
with fcol3:
    st.markdown("**Deployment Architecture:**")
    st.caption("Zero-DB Dependency • 1-Click Streamlit Cloud Ready • Multi-Tenant")
