# Multimodal Construction Intelligence Platform 🏗️
> **Enterprise Generative AI Decision-Support System for Construction Safety, Structural Pathology, Real Estate Valuation, and Dynamic Site Protocols**  
> **Skill Wallet Capstone Project 1** | **Platform ID:** `6ac4c98d1dcde6d7857c1642`  
> **Category:** Generative AI | Real Estate Decision Support | Computer Vision

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---
 
## 🎬 Interactive Feature Video Walkthrough

A complete end-to-end video tour covering all 4 modules (PPE vision audit, crack pathology, INR valuation, and weather advisory):
- **Local MP4 Video File:** [`assets/demo_walkthrough.mp4`](assets/demo_walkthrough.mp4) (Full HD, 670 frames)
- **Local WebP Video File:** [`assets/demo_walkthrough.webp`](assets/demo_walkthrough.webp)
- **Live Streamlit App:** Embedded directly in the sidebar under **"🎬 Watch Video Walkthrough Tour"** with 1-click download.

---

## 📌 Executive Summary & Scope

The **Multimodal Construction Intelligence Platform** is an end-to-end, AI-powered decision-support system tailored for civil engineers, site safety auditors, real estate developers, and infrastructure asset managers. By fusing Multimodal Large Language Models (Gemini 1.5 Pro / Flash) with civil engineering codes (**IS 456:2000**, **OSHA 29 CFR 1926**, **IS 13920**, **NBC 2016**), the platform automates critical site inspections, quantifies structural risks, and models financial CapEx in Indian Rupees (INR Lakhs and Crores).

---

## 🧭 Kanban Epics Coverage

| Epic | Scope & Implementation | Modules |
| :--- | :--- | :--- |
| **Prerequisites & Epic 1** | Environment, Python 3.9+, modular package architecture, dark modern UI | `app.py`, `.streamlit/config.toml`, `assets/styles.css` |
| **Epic 2** | PPE Safety Vision Audit & Concrete Crack Pathology Diagnostics | `modules/safety_audit.py`, `modules/crack_diagnostics.py` |
| **Epic 3** | Project Planning, Real Estate Valuation in INR (Lakhs/Crores) & Pollinations AI 3D Renders | `modules/project_planning.py` |
| **Epic 4** | Multimodal Vision Prompts & Strict JSON Data Contracts | `modules/ai_engine.py` |
| **Epic 5** | Daily Weather-Aware Advisory & Multi-Turn Engineering Chatbot | `modules/weather_advisory.py` |
| **Epic 6** | Zero-DB Architecture, Interactive Testing, 1-Click Streamlit Cloud Deployment | `requirements.txt`, `README.md` |

---

## 🌟 Core Modules & Capabilities

### 🦺 1. Site Safety & PPE Audit (Epic 2 & 4)
- **Computer Vision Audits:** Analyzes construction site photos for worker PPE compliance:
  - ⛑️ **Hard Hats / Safety Helmets:** Certified under **OSHA 1926.100** and **IS 2925**
  - 🦺 **High-Visibility Reflective Vests:** Conforming to **OSHA 1926.201** and **IS 15809**
  - 🥾 **Steel-Toe Safety Footwear:** Conforming to **OSHA 1926.96** and **IS 15298**
  - 🪢 **Fall Arrest Harnesses & Static Lifelines:** Conforming to **OSHA 1926.502** and **IS 3521**
  - 🧤 **Eye & Hand Protection Gear:** Conforming to **OSHA 1926.102** and **IS 2573**
- **Structured JSON Contract:** Emits `safety_score` (0-100), `overall_status`, detailed item-by-item detection checklist, and identified physical hazards tagged with severity (`Low`, `Medium`, `High`, `Critical`) and actionable corrective remedies.
- **Export:** 1-click downloadable JSON audit report with timestamping.

### 🔍 2. Crack Diagnostics & Structural Integrity (Epic 2 & 4)
- **Defect Pathology:** Classifies concrete/masonry defects into:
  - Structural Shear (Diagonal 45° shear fissure)
  - Differential Settlement
  - Hairline Plastic & Thermal Shrinkage
  - Spalling & Rebar Corrosion Delamination
- **Quantitative Metrics:** Crack width estimation in millimeters (mm), severity score (0-100), and compliance verdict against **IS 456:2000 Clause 35.3.2** (0.3mm maximum permissible crack width).
- **Engineering Repair Specifications:** Prescribes concrete rehabilitation procedures such as low-viscosity epoxy resin pressure injection (ASTM C881 / IS 15809), Carbon Fiber Reinforced Polymer (CFRP) wrapping (ACI 440.2R), micro-concreting, and elastomeric joint sealing.

### 📊 3. Planning & Real Estate Valuation (Epic 3)
- **Interactive Multi-Tier Input:** Structure classification (High-Rise, Commercial IT Park, Industrial Warehouse, Luxury Villa, Metro Infrastructure), built-up area (sq. ft.), location tier (Tier 1, Tier 2, Tier 3 Indian cities), specification grade, and completion progress slider.
- **INR Valuation Engine:**
  - Total Estimated Construction Budget (INR Lakhs & Crores)
  - CapEx Incurred to Date & Remaining CapEx required
  - Current Market Asset Valuation (as-is completed value)
  - Gross Development Value (GDV finished value)
- **Bill of Quantities (BOM):** Structural steel/rebar requirement (Metric Tonnes), Cement bags, Ready-Mix Concrete (RMC m³), and Sand/Aggregate (Brass).
- **Milestone S-Curve & Cost Distribution:** Interactive financial allocation donut charts.
- **Conceptual 3D Architectural Generation:** Integrated with **Pollinations AI / Flux API** to synthesize photorealistic 3D architectural renders reflecting design styles, lighting presets, and construction stages.

### 🌦️ 4. Daily Site Assistant & Weather-Aware Advisory (Epic 5)
- **Weather Condition Triggers:** High Wind (>38 km/h), Heavy Rain & Monsoon (>45 mm/hr), Extreme Heat (>42°C), Normal/Favorable, Dense Fog, and Severe Thunderstorm.
- **Dynamic Site Protocols:**
  - 🏗️ Tower crane lift suspension and out-of-service weathervaning rules (ASME B30.3 & IS 456)
  - 🪜 Scaffolding and work-at-height shutdown procedures
  - ⚡ Electrical pump dewatering and ground fault isolation (OSHA 1926.404)
  - 💧 Hot-weather vs. rain concrete pouring, slump retention, and moist ponding curing protocols (IS 456 Cl. 13.5 & ACI 305R)
- **Multi-Turn Engineering Chatbot:** Technical conversational copilot fluent in civil codes, slump criteria, rebar lap lengths ($45\phi-50\phi$ for Fe500D per IS 13920), and formwork striking periods.

---

## 🏗️ Technical Architecture

```
g:/skillbridge project/
├── .streamlit/
│   └── config.toml           # Sleek dark theme configuration & server settings
├── assets/
│   ├── sample_images/        # High-res sample inspection benchmarks for 1-click audits
│   │   ├── site_safety_sample_1.jpg
│   │   ├── site_safety_sample_2.jpg
│   │   ├── crack_structural_sample_1.jpg
│   │   └── crack_hairline_sample_2.jpg
│   └── styles.css            # Glassmorphism, badges, and responsive UI styles
├── modules/
│   ├── __init__.py
│   ├── ai_engine.py          # Gemini 1.5 Multimodal SDK interface & JSON sanitizer
│   ├── safety_audit.py       # OSHA 1926 & IS 456 PPE audit engine & schema
│   ├── crack_diagnostics.py  # Concrete pathology, crack width, & repair specs
│   ├── project_planning.py   # CapEx in INR, valuation, BOM, & Pollinations 3D engine
│   └── weather_advisory.py   # Dynamic weather protocols & multi-turn site chatbot
├── scripts/
│   └── generate_sample_assets.py # Sample benchmark image generator
├── app.py                    # Main Streamlit application
├── requirements.txt          # Production dependencies
└── README.md                 # Complete system documentation
```

---

## ⚡ Quickstart Guide

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/nihar-rajput/multimodal-construction-intelligence.git
cd multimodal-construction-intelligence

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key (Optional)

The application features a **built-in demonstration fallback engine**. You can run the application immediately without an API key!

To enable live Google Gemini Multimodal analysis:
- Provide your key in the secure sidebar password input field within the app, OR
- Set it as an environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere"

# Linux / macOS
export GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere"
```

### 3. Launch the Application

```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ 1-Click Deployment on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app**, select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. (Optional) In **Advanced settings > Secrets**, add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
5. Click **Deploy!** The application will be live globally in under 2 minutes with zero database dependencies.

---

## 📜 Regulatory Standards Reference

- **IS 456:2000:** Code of practice for plain and reinforced concrete.
- **IS 13920:2016:** Ductile detailing of reinforced concrete structures subjected to seismic forces.
- **IS 3696 (Part 1 & 2):** Safety code for scaffolds and ladders.
- **OSHA 29 CFR 1926 Subpart C, E, M:** Safety and Health Regulations for Construction.
- **ACI 224R-01:** Control of Cracking in Concrete Structures.
- **National Building Code of India (NBC 2016):** Fire and life safety guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. Built for the Skill Wallet Capstone Program.
