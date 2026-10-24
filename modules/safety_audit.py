"""
Safety Audit Module - PPE Vision & Hazard Compliance (OSHA & IS 456 Standards)
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import datetime
from typing import Dict, Any, Optional
from PIL import Image
from modules.ai_engine import call_gemini_vision, clean_json_response

SAFETY_AUDIT_PROMPT = """
You are a senior construction safety auditor and structural safety inspector certified under OSHA 1926 (Safety and Health Regulations for Construction) and Indian Standard IS 456 / IS 3696 / IS 2925.

Analyze this construction site photograph thoroughly for worker PPE (Personal Protective Equipment) compliance and physical hazards.

Return ONLY a valid JSON object with the following schema:
{
  "safety_score": <integer from 0 to 100 based on overall compliance and hazard severity>,
  "overall_status": "<Compliant | Minor Deviations | Attention Required | Severe Non-Compliance | Critical Stop-Work>",
  "total_workers_detected": <integer>,
  "compliant_workers": <integer>,
  "ppe_detection": [
    {
      "category": "Hard Hats / Safety Helmets",
      "standard_ref": "OSHA 1926.100 / IS 2925",
      "detected_count": <integer>,
      "compliant_count": <integer>,
      "violation_count": <integer>,
      "status": "<Pass | Warning | Fail>",
      "observation": "<Specific visual observation on helmet usage and condition>"
    },
    {
      "category": "High-Visibility Safety Vests",
      "standard_ref": "OSHA 1926.201 / IS 15809",
      "detected_count": <integer>,
      "compliant_count": <integer>,
      "violation_count": <integer>,
      "status": "<Pass | Warning | Fail>",
      "observation": "<Specific visual observation on vest reflectivity and wear>"
    },
    {
      "category": "Steel-Toe Safety Boots",
      "standard_ref": "OSHA 1926.96 / IS 15298",
      "detected_count": <integer>,
      "compliant_count": <integer>,
      "violation_count": <integer>,
      "status": "<Pass | Warning | Fail>",
      "observation": "<Specific visual observation on footwear>"
    },
    {
      "category": "Safety Harnesses / Fall Protection",
      "standard_ref": "OSHA 1926.502 / IS 3521",
      "detected_count": <integer>,
      "compliant_count": <integer>,
      "violation_count": <integer>,
      "status": "<Pass | Warning | Fail | N/A - Ground Level>",
      "observation": "<Observation regarding anchorage, lanyards, or work at height>"
    },
    {
      "category": "Eye / Hand Protective Gear",
      "standard_ref": "OSHA 1926.102 / IS 2573",
      "detected_count": <integer>,
      "compliant_count": <integer>,
      "violation_count": <integer>,
      "status": "<Pass | Warning | Fail>",
      "observation": "<Observation on safety goggles and heavy-duty work gloves>"
    }
  ],
  "identified_site_hazards": [
    {
      "hazard_id": "HAZ-001",
      "description": "<Detailed description of hazard identified>",
      "severity": "<Low | Medium | High | Critical>",
      "location": "<Estimated location in image, e.g., Center scaffold tier, left foreground>",
      "regulatory_code": "<e.g., OSHA 1926.451(g) / IS 3696 Part 1>",
      "corrective_remedy": "<Immediate actionable engineering or procedural remedy>"
    }
  ],
  "osha_is456_summary": "<Professional executive paragraph summarizing safety compliance and regulatory risks>",
  "immediate_remedial_actions": [
    "<Action 1>",
    "<Action 2>"
  ]
}

DO NOT include markdown code blocks or additional text. Output pure JSON only.
"""


def get_demo_safety_data(scenario_id: int = 1) -> Dict[str, Any]:
    """
    Returns realistic fallback demonstration data for testing when API key is omitted.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    if scenario_id == 1:
        return {
            "safety_score": 78,
            "overall_status": "Attention Required",
            "total_workers_detected": 5,
            "compliant_workers": 3,
            "audit_timestamp": now,
            "mode": "Demonstration Fallback Mode",
            "ppe_detection": [
                {
                    "category": "Hard Hats / Safety Helmets",
                    "standard_ref": "OSHA 1926.100 / IS 2925",
                    "detected_count": 5,
                    "compliant_count": 4,
                    "violation_count": 1,
                    "status": "Warning",
                    "observation": "4 workers wearing Class E industrial hard hats; 1 operative near material hoist wearing cloth cap."
                },
                {
                    "category": "High-Visibility Safety Vests",
                    "standard_ref": "OSHA 1926.201 / IS 15809",
                    "detected_count": 5,
                    "compliant_count": 5,
                    "violation_count": 0,
                    "status": "Pass",
                    "observation": "All 5 workers equipped with Class 2 fluorescent yellow/orange reflective vests with retroreflective tape."
                },
                {
                    "category": "Steel-Toe Safety Boots",
                    "standard_ref": "OSHA 1926.96 / IS 15298",
                    "detected_count": 5,
                    "compliant_count": 4,
                    "violation_count": 1,
                    "status": "Warning",
                    "observation": "Worker in center rebar framing zone observed wearing non-reinforced canvas shoes on steel deck."
                },
                {
                    "category": "Safety Harnesses / Fall Protection",
                    "standard_ref": "OSHA 1926.502 / IS 3521",
                    "detected_count": 2,
                    "compliant_count": 1,
                    "violation_count": 1,
                    "status": "Fail",
                    "observation": "Operative on perimeter cantilever formwork has harness on but lanyard is not hooked to static lifeline."
                },
                {
                    "category": "Eye / Hand Protective Gear",
                    "standard_ref": "OSHA 1926.102 / IS 2573",
                    "detected_count": 5,
                    "compliant_count": 3,
                    "violation_count": 2,
                    "status": "Warning",
                    "observation": "Operative handling angle grinder lacks impact-resistant polycarbonate eye shields."
                }
            ],
            "identified_site_hazards": [
                {
                    "hazard_id": "HAZ-001",
                    "description": "Unanchored fall arrest lanyard during edge beam shuttering operations at 12m height.",
                    "severity": "Critical",
                    "location": "Upper cantilever deck edge, Grid Line C-4",
                    "regulatory_code": "OSHA 1926.501(b)(1) & IS 3696 Part 1",
                    "corrective_remedy": "Issue immediate Stop-Work on perimeter formwork; require 100% tie-off to certified 15kN anchorage line before re-entry."
                },
                {
                    "hazard_id": "HAZ-002",
                    "description": "Lack of perimeter toe-boards on working platform allowing dropped tool risk to ground crew.",
                    "severity": "High",
                    "location": "External tubular scaffold tier 3",
                    "regulatory_code": "OSHA 1926.451(h)(1) & IS 4014",
                    "corrective_remedy": "Install minimum 150mm timber/steel toe-boards and safety debris netting along outer scaffold bay."
                },
                {
                    "hazard_id": "HAZ-003",
                    "description": "Worker engaged in steel cutting without UV/impact eye protection.",
                    "severity": "Medium",
                    "location": "Ground staging yard (left foreground)",
                    "regulatory_code": "OSHA 1926.102(a)(1) & IS 5983",
                    "corrective_remedy": "Supply ANSI Z87.1 / IS 5983 approved wrap-around face shield and mandate hot-work eye protection."
                }
            ],
            "osha_is456_summary": "Site exhibits acceptable high-visibility vest compliance but critical fall protection lapses under OSHA 1926 Subpart M and IS 3696. Active work at height without secure tie-offs and inadequate toe-boards poses immediate life-safety liabilities requiring site supervisor intervention.",
            "immediate_remedial_actions": [
                "Execute instant 15-minute safety stand-down on fall protection anchorage.",
                "Enforce strict 100% mandatory tie-off on cantilever shuttering zones.",
                "Replace improper footwear for reinforcement tier crew before resuming steel placement.",
                "Inspect scaffolding per IS 4014 checklist and verify toe-board integrity."
            ]
        }
    else:
        return {
            "safety_score": 92,
            "overall_status": "Compliant",
            "total_workers_detected": 4,
            "compliant_workers": 4,
            "audit_timestamp": now,
            "mode": "Demonstration Fallback Mode",
            "ppe_detection": [
                {
                    "category": "Hard Hats / Safety Helmets",
                    "standard_ref": "OSHA 1926.100 / IS 2925",
                    "detected_count": 4,
                    "compliant_count": 4,
                    "violation_count": 0,
                    "status": "Pass",
                    "observation": "All personnel actively wearing EN 397 / IS 2925 certified hard hats with chin straps fastened."
                },
                {
                    "category": "High-Visibility Safety Vests",
                    "standard_ref": "OSHA 1926.201 / IS 15809",
                    "detected_count": 4,
                    "compliant_count": 4,
                    "violation_count": 0,
                    "status": "Pass",
                    "observation": "Reflective class 2 high-vis safety vests properly zipped on all detected staff."
                },
                {
                    "category": "Steel-Toe Safety Boots",
                    "standard_ref": "OSHA 1926.96 / IS 15298",
                    "detected_count": 4,
                    "compliant_count": 4,
                    "violation_count": 0,
                    "status": "Pass",
                    "observation": "Heavy-duty steel-toe boots with puncture-resistant midsoles verified."
                },
                {
                    "category": "Safety Harnesses / Fall Protection",
                    "standard_ref": "OSHA 1926.502 / IS 3521",
                    "detected_count": 1,
                    "compliant_count": 1,
                    "violation_count": 0,
                    "status": "Pass",
                    "observation": "Worker at elevated edge dual-hooked with energy-absorbing lanyard."
                },
                {
                    "category": "Eye / Hand Protective Gear",
                    "standard_ref": "OSHA 1926.102 / IS 2573",
                    "detected_count": 4,
                    "compliant_count": 3,
                    "violation_count": 1,
                    "status": "Warning",
                    "observation": "1 worker removed cut-resistant leather gloves during blueprint review."
                }
            ],
            "identified_site_hazards": [
                {
                    "hazard_id": "HAZ-001",
                    "description": "Minor electrical cable trailing across secondary transit pathway without cable ramp protection.",
                    "severity": "Low",
                    "location": "Passage between batching plant and crane staging",
                    "regulatory_code": "OSHA 1926.416(e)(1) & IS 732",
                    "corrective_remedy": "Route flexible extension cords overhead (min 2.4m clearance) or insert heavy-duty rubber cable crossover protectors."
                }
            ],
            "osha_is456_summary": "High-standard site housekeeping observed. PPE discipline aligns with OSHA 1926 standards and IS 456 safety clauses. Continuous monitoring recommended during heavy concreting shifts.",
            "immediate_remedial_actions": [
                "Install rubber cable protector ramp across transit pathway.",
                "Maintain daily pre-shift toolbox talk routine."
            ]
        }


def analyze_site_safety(
    image: Image.Image,
    api_key: Optional[str] = None,
    scenario_id: int = 1
) -> Dict[str, Any]:
    """
    Audits site photo using Gemini Multimodal vision or falls back to demonstration mode.
    """
    if not api_key or not api_key.strip():
        demo_data = get_demo_safety_data(scenario_id)
        return demo_data

    raw_response, error = call_gemini_vision(image, SAFETY_AUDIT_PROMPT, api_key=api_key)
    if error or not raw_response:
        demo_data = get_demo_safety_data(scenario_id)
        demo_data["mode"] = f"Demo Mode (API Notice: {error or 'Check Gemini Key'})"
        return demo_data

    try:
        parsed_data = clean_json_response(raw_response)
        parsed_data["audit_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
        parsed_data["mode"] = "Live Gemini 1.5 Multimodal Analysis"
        return parsed_data
    except Exception as e:
        fallback = get_demo_safety_data(scenario_id)
        fallback["mode"] = f"Demo Mode (JSON Parse Notice: {str(e)})"
        return fallback
