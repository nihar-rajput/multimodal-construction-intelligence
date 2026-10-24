"""
Crack Diagnostics & Structural Integrity Module
Defect Classification, Width Estimation, Root Causes & IS 456 / ACI 224 Engineering Repairs
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import datetime
from typing import Dict, Any, Optional
from PIL import Image
from modules.ai_engine import call_gemini_vision, clean_json_response

CRACK_DIAGNOSTICS_PROMPT = """
You are a senior structural forensic engineer and concrete pathology specialist adhering to Indian Standard IS 456:2000 (Section 35.3.2 crack control criteria) and ACI 224R-01 (Control of Cracking in Concrete Structures).

Perform a detailed forensic structural inspection of the provided concrete, beam, column, or masonry wall photograph.

Identify crack characteristics, severity, propagation risk, and repair specifications.

Return ONLY a valid JSON object matching this schema:
{
  "defect_type": "<Hairline (< 1mm) | Differential Settlement | Structural Shear (Diagonal 45°) | Thermal Expansion / Shrinkage | Spalling & Rebar Corrosion | Flexural Tension>",
  "estimated_width_mm": <float or string, e.g., 2.8>,
  "severity_score": <integer from 0 to 100>,
  "risk_rating": "<Low Risk | Moderate Hazard | Severe Structural Risk | Critical - Immediate Evacuation>",
  "urgency": "<Immediate (0-24 hrs) | High Priority (24-48 hrs) | Medium (Within 2 Weeks) | Routine Monitoring>",
  "structural_element": "<e.g., RCC Transfer Girder / Column Junction / Masonry Infill / Slab Soffit>",
  "root_causes": [
    "<Primary root cause, e.g. Differential subgrade settlement exceeding allowable limits>",
    "<Secondary contributing factor, e.g. Inadequate shear stirrup spacing under increased dead loads>"
  ],
  "is456_compliance_status": "<Compliant with 0.3mm exposure limit | Exceeds IS 456 0.3mm limit | Severe structural integrity compromise>",
  "engineering_repairs": [
    {
      "method": "<e.g., Low-viscosity epoxy resin pressure injection / Polymer modified micro-concrete / CFRP carbon wrap>",
      "specification": "<Engineering details, material grade, pressure bar requirements, surface prep>",
      "standard_ref": "<e.g., IS 15809 / ACI 546R>"
    }
  ],
  "monitoring_protocol": "<Recommendations for tell-tale crack gauges, optical displacement sensors, or ultrasonic pulse velocity (UPV) testing>",
  "forensic_summary": "<Professional technical summary of the structural diagnosis>"
}

DO NOT include markdown code blocks or text outside JSON. Pure JSON output only.
"""


def get_demo_crack_data(defect_case: int = 1) -> Dict[str, Any]:
    """
    Returns realistic structural defect forensic evaluations for demonstration/offline mode.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    if defect_case == 1:
        return {
            "defect_type": "Structural Shear (Diagonal 45°)",
            "estimated_width_mm": "3.8 mm",
            "severity_score": 88,
            "risk_rating": "Severe Structural Risk",
            "urgency": "Immediate (0-24 hrs)",
            "structural_element": "Reinforced Concrete Beam-Column Joint (Zone 1)",
            "analysis_timestamp": now,
            "mode": "Demonstration Fallback Mode",
            "is456_compliance_status": "Severe Failure - Exceeds IS 456:2000 Clause 35.3.2 limit (0.3mm) by >12x",
            "root_causes": [
                "Principal tensile stress exceeding concrete tensile strength near maximum shear zone",
                "Inadequate transverse shear reinforcement (stirrup spacing > 0.75d) under modified live load",
                "Micro-vibrations from nearby heavy excavation causing stress concentration"
            ],
            "engineering_repairs": [
                {
                    "method": "Ultra-Low Viscosity Epoxy Resin Pressure Injection",
                    "specification": "Inject solvent-free, low-viscosity thermosetting epoxy resin (viscosity < 200 cps) at 0.2–0.4 MPa via staggered injection nipples spaced at crack depth intervals.",
                    "standard_ref": "ASTM C881 Type I / IS 15809"
                },
                {
                    "method": "Carbon Fiber Reinforced Polymer (CFRP) Composite Wrapping",
                    "specification": "Apply 2-ply bidirectional CFRP composite laminate (modulus > 230 GPa) around shear span with minimum 150mm anchor development length to restore shear capacity.",
                    "standard_ref": "ACI 440.2R-17 & IS 13920:2016"
                },
                {
                    "method": "Temporary Acrow Prop Shoring",
                    "specification": "Install heavy-duty adjustable steel shores directly beneath beam midpoint prior to injection to relieve dead weight flexural strain.",
                    "standard_ref": "IS 4014 Part 2"
                }
            ],
            "monitoring_protocol": "Install calibrated mechanical Avongard tell-tale crack width monitors across top and bottom ends. Conduct Ultrasonic Pulse Velocity (UPV) per IS 516 Part 4 to map internal crack depth.",
            "forensic_summary": "Active diagonal shear fissure originating at support face and inclined at approximately 42 degrees. Indicates dangerous diagonal tension distress. Immediate structural shoring and epoxy/CFRP rehabilitation is mandatory to prevent progressive shear shear failure."
        }
    else:
        return {
            "defect_type": "Hairline Thermal & Plastic Shrinkage",
            "estimated_width_mm": "0.45 mm",
            "severity_score": 32,
            "risk_rating": "Low Risk",
            "urgency": "Routine Monitoring",
            "structural_element": "RCC Slab Soffit & Screed Surface",
            "analysis_timestamp": now,
            "mode": "Demonstration Fallback Mode",
            "is456_compliance_status": "Marginal - Near IS 456:2000 0.30mm threshold for mild exposure",
            "root_causes": [
                "Rapid surface moisture evaporation during initial concrete setting under ambient heat",
                "Inadequate early-age moist ponding curing within first 48 hours of casting",
                "Differential thermal movement between screed and structural slab core"
            ],
            "engineering_repairs": [
                {
                    "method": "Elastomeric Polyurethane (PU) Crack Sealer",
                    "specification": "V-groove chase crack to 6mm x 6mm, brush apply silane-siloxane penetrating primer, and seal with high-movement elastomeric polyurethane joint compound.",
                    "standard_ref": "ASTM C920 Class 25 / IS 1838"
                },
                {
                    "method": "Crystalline Waterproofing Slurry Barrier",
                    "specification": "Apply two coats of osmotic crystalline waterproofing slurry (1.2 kg/m²) to activate secondary calcium silicate hydrate (C-S-H) autogenous healing.",
                    "standard_ref": "ACI 212.3R Chapter 15"
                }
            ],
            "monitoring_protocol": "Record width measurements monthly using an optical crack magnifier (40x). Re-inspect after heavy monsoon rainfall for efflorescence or dampness.",
            "forensic_summary": "Non-structural superficial surface crazing/shrinkage fissure. No shear or load-bearing displacement detected. Sealing is advised to inhibit carbonation ingress and safeguard reinforcement durability."
        }


def analyze_concrete_crack(
    image: Image.Image,
    api_key: Optional[str] = None,
    defect_case: int = 1
) -> Dict[str, Any]:
    """
    Classifies crack defects and prescribes structural repairs via Gemini Vision or demo engine.
    """
    if not api_key or not api_key.strip():
        return get_demo_crack_data(defect_case)

    raw_response, error = call_gemini_vision(image, CRACK_DIAGNOSTICS_PROMPT, api_key=api_key)
    if error or not raw_response:
        demo = get_demo_crack_data(defect_case)
        demo["mode"] = f"Demo Mode (API Notice: {error or 'Check Gemini Key'})"
        return demo

    try:
        data = clean_json_response(raw_response)
        data["analysis_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        data["mode"] = "Live Gemini 1.5 Multimodal Analysis"
        return data
    except Exception as e:
        fallback = get_demo_crack_data(defect_case)
        fallback["mode"] = f"Demo Mode (JSON Parse Notice: {str(e)})"
        return fallback
