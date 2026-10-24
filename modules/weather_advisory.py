"""
Weather Advisory & Daily Site Assistant Module
Dynamic Protocols (Wind, Rain, Heat) & Multi-turn Construction Engineering Chatbot
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

from typing import Dict, Any, List, Optional, Tuple
from modules.ai_engine import call_gemini_chat

WEATHER_PROTOCOLS = {
    "High Wind (> 38 km/h / Beaufort Scale 6+)": {
        "badge_class": "badge-critical",
        "severity": "CRITICAL HAZARD",
        "primary_action": "Halt all Tower Crane lifts, suspend boom placers, and clear elevated scaffolding decks immediately.",
        "protocols": [
            {
                "domain": "Tower Cranes & Hoists (OSHA 1926.1431 / IS 456)",
                "directive": "Cease all crane operations when sustained wind exceeds 38 km/h or gusts exceed 45 km/h. Park crane jib into the wind (weathervaning free-slew mode enabled) and disconnect hook blocks from loads.",
                "code_ref": "IS 456 & ASME B30.3"
            },
            {
                "domain": "Work at Height & Scaffolding (OSHA 1926.451)",
                "directive": "Prohibit worker access on external hanging scaffolding, swinging stages, and formwork decks > 6 meters. Secure or strike loose plywood sheets, unanchored safety netting, and corrugated metal roofing.",
                "code_ref": "OSHA 1926.451(f)(12)"
            },
            {
                "domain": "Facade & Glass Installation",
                "directive": "Suspend all curtain-wall glass panel hoisting with vacuum cups. Secure installed glass units with temporary timber wedges.",
                "code_ref": "IS 3548 / NBC 2016"
            }
        ],
        "curing_impact": "Accelerated surface wind desiccation. Wet burlap curing must be anchored with heavy timber sleepers to prevent displacement."
    },
    "Heavy Rain & Monsoon (> 45 mm/hr)": {
        "badge_class": "badge-high",
        "severity": "HIGH ENVIRONMENTAL RISK",
        "primary_action": "Halt open-deck concrete pours immediately; energize submersible dewatering sumps and isolate temporary power distribution boards.",
        "protocols": [
            {
                "domain": "Concrete Pouring & Hydration (IS 456:2000 Cl. 13)",
                "directive": "Do NOT pour fresh concrete in uncovered open formwork during continuous downpour. Rain increases the water-cement ratio, washing out cement paste and inducing severe cold joints. Cover recently placed slabs with 250-micron poly-sheeting.",
                "code_ref": "IS 456:2000 Cl. 13.3"
            },
            {
                "domain": "Electrical Safety & Dewatering (OSHA 1926.404)",
                "directive": "All portable electrical distribution boxes must be elevated > 300mm above ground with functioning 30mA Earth Leakage Circuit Breakers (ELCB/GFCI). Station submersible mud pumps in basement pits.",
                "code_ref": "IS 732 & OSHA 1926.404(b)"
            },
            {
                "domain": "Deep Excavation & Slope Stability (IS 3764)",
                "directive": "Inspect retaining sheet piles and soil nailing for hydrostatic piping or slope slumping. Keep heavy transit mixers at least 2.5 meters away from unsupported trench crests.",
                "code_ref": "IS 3764 Safety in Excavation"
            }
        ],
        "curing_impact": "Excessive rainwater dilution risks aggregate segregation. Shield fresh concrete until initial set (approx. 4 hours) is achieved."
    },
    "Extreme Heat & Heatwave (> 42°C / 108°F)": {
        "badge_class": "badge-medium",
        "severity": "MODERATE/HIGH PHYSIOLOGICAL RISK",
        "primary_action": "Reschedule structural concreting to nocturnal shifts (7 PM - 6 AM); enforce mandatory 15-minute hydration breaks every hour.",
        "protocols": [
            {
                "domain": "Hot Weather Concreting (IS 456 & ACI 305R)",
                "directive": "Maintain fresh concrete placement temperature below 32°C. Use chilled batching water or crushed flake ice substitution. Apply aliphatic alcohol surface evaporation retarders immediately after screeding to forestall plastic shrinkage cracks.",
                "code_ref": "IS 456 Cl. 14.2 & ACI 305R"
            },
            {
                "domain": "Curing Regimen (IS 456 Cl. 13.5)",
                "directive": "For Ordinary Portland Cement (OPC), continuous ponding or wet hessian curing must continue for a minimum of 10 days (extended from 7 days). For PPC with fly-ash/slag, extend curing to 14 days under extreme ambient heat.",
                "code_ref": "IS 456:2000 Cl. 13.5.1"
            },
            {
                "domain": "Worker Ergonomics & Heat Stress (OSHA Heat NEP)",
                "directive": "Establish shaded electrolyte hydration kiosks at 50-meter intervals across tower slabs. Shift heavy steel-tying work to morning shifts (6:00 AM - 11:30 AM).",
                "code_ref": "OSHA Directive CPL 03-00-024"
            }
        ],
        "curing_impact": "High rate of evaporation (> 1.0 kg/m²/hr) causes rapid micro-fissuring. Continuous saturated water misting is strictly enforced."
    },
    "Normal / Favorable Weather (22°C - 30°C, Clear Sky)": {
        "badge_class": "badge-low",
        "severity": "OPTIMAL OPERATING CONDITIONS",
        "primary_action": "Full-capacity operations authorized across all trades (Concreting, Tower Crane lifts, Scaffolding, Facade).",
        "protocols": [
            {
                "domain": "RCC Slab Casting & Structural Pours",
                "directive": "Ideal atmospheric conditions for monolithic slab casting, post-tensioned tendon stressing, and structural column shuttering. Verify slump (100–120mm for pumpable mixes) per IS 1199.",
                "code_ref": "IS 456 & IS 1199"
            },
            {
                "domain": "Lifting & Rigging Operations",
                "directive": "Standard rigging protocols apply. Maintain daily 10-point crane pre-lift checklist and ensure signalman has clear line of sight.",
                "code_ref": "OSHA 1926.1400"
            },
            {
                "domain": "Quality Audits & Rebar Inspection",
                "directive": "Perform pre-pour cover block verification (20mm for slabs, 40mm for columns, 50mm for foundations) and inspect lap lengths (typically 45d–50d for Fe500D rebar).",
                "code_ref": "IS 456 Cl. 26.5 & IS 13920"
            }
        ],
        "curing_impact": "Standard moist ponding curing: minimum 7 days for OPC, 10 days for mineral admixture mixes."
    },
    "Dense Fog & Low Visibility (< 100m)": {
        "badge_class": "badge-medium",
        "severity": "VISIBILITY HAZARD",
        "primary_action": "Prohibit blind crane slewing; activate high-intensity amber strobe beacons and enforce two-way radio verification.",
        "protocols": [
            {
                "domain": "Tower Crane & Heavy Plant Movement",
                "directive": "Restrict mobile crane movements in site yards without pedestrian spotters in high-vis vests. Dual-radio confirmation required for every hoist movement.",
                "code_ref": "OSHA 1926.1417 & IS 13367"
            },
            {
                "domain": "Site Lighting & Perimeter Illumination",
                "directive": "Energize minimum 50 lux floodlighting along material corridors, stair towers, and edge perimeters.",
                "code_ref": "IS 3646 Part 2"
            }
        ],
        "curing_impact": "High relative humidity slows curing evaporation favorably, but monitor condensation on smooth shuttering."
    },
    "Severe Thunderstorm & Lightning Warning": {
        "badge_class": "badge-critical",
        "severity": "ELECTROCUTION / LIFE HAZARD",
        "primary_action": "Evacuate all tower cranes, elevated steel decks, and open scaffolds immediately; shelter workers in grounded facilities.",
        "protocols": [
            {
                "domain": "Lightning Protection & Steel Decks",
                "directive": "Under the 30/30 Lightning Safety Rule, clear all metal roof frameworks, tower crane operator cabs, and rebar decks. Cranes must have certified lightning down-conductors (< 5 ohms earth resistance).",
                "code_ref": "IS/IEC 62305 & OSHA 1926"
            },
            {
                "domain": "Power Equipment Isolation",
                "directive": "Safely trip primary site switchgear and de-energize external mast climbing platforms.",
                "code_ref": "IS 732"
            }
        ],
        "curing_impact": "Shield fresh concrete with waterproof tarpaulins."
    }
}

SYSTEM_ENGINEERING_INSTRUCTION = """
You are Antigravity Construction Intelligence Copilot - an elite chief structural civil engineer, safety auditor, and project manager with 25+ years of experience across high-rise buildings, infrastructure, and heavy civil projects in India and internationally.
You are thoroughly certified and fluent in:
- Indian Standard IS 456:2000 (Plain and Reinforced Concrete Code of Practice)
- IS 13920:2016 (Ductile Design and Detailing of RCC Structures subject to Seismic Forces)
- IS 875 Parts 1 to 5 (Design Loads for Buildings: Dead, Imposed, Wind, Snow, Special)
- National Building Code of India (NBC 2016)
- OSHA 29 CFR 1926 (Safety and Health Regulations for Construction)
- ACI 318 & ACI 224 (American Concrete Institute structural codes)
- CPWD (Central Public Works Department) Specifications & DSR cost analysis

Your tone is authoritative, highly technical yet practical, crisp, and direct. When providing calculations or advice, always cite the relevant code clause (e.g. IS 456:2000 Cl. 26.2 for development length, Cl. 35.3.2 for crack limits, OSHA 1926.502 for fall protection). Use bullet points and clean structure.
"""

KNOWLEDGE_FALLBACK_ANSWERS = {
    "curing": """### Concrete Curing Protocol under IS 456:2000 (Clause 13.5)

**1. Curing Duration by Cement Type:**
* **Ordinary Portland Cement (OPC 43 / 53 Grade):** Minimum **7 days** under normal ambient conditions; extend to **10 days** if dry/hot weather prevails.
* **Pozzolana Portland Cement (PPC) / Slag Cement (PSC) / Mineral Admixtures (Fly-ash, GGBS, Silica Fume):** Minimum **10 days** under normal conditions; extend to **14 days** under hot/dry weather due to slower pozzolanic secondary hydration (calcium hydroxide conversion to C-S-H).

**2. Practical Site Methods:**
* **Horizontal Slabs:** Ponding with 50mm earthen/mortar bunds is mandatory. Alternatively, saturated hessian cloth continuously kept wet.
* **Vertical Columns / Shear Walls:** Membrane curing compound (ASTM C309) applied immediately upon formwork stripping, or columns tightly wrapped in damp hessian covered with plastic film.

**3. Critical Standard Reference:**
* Curing must commence as soon as concrete has attained sufficient hardness to resist surface damage (IS 456 Cl. 13.5.1). Compressive strength drops by 30–40% if early-age moist curing is neglected!""",

    "slump": """### Recommended Slump & Workability per IS 456:2000 (Clause 7.1, Table 2)

**1. Typical Slump Ranges for Construction Elements:**
* **Pavement & Mass Concreting (Gravity Dams, Raft cores):** 25 – 75 mm (Low to Medium workability)
* **Standard Reinforced Foundations, Footings, Retaining Walls:** 50 – 100 mm
* **Heavily Reinforced Beams, Slabs, and Columns (Manual Pour):** 75 – 100 mm
* **Pumpable Concrete (High-Rise Slabs, Chutes, Tremie Pours):** **100 – 150 mm** (Requires High-Range Water Reducers / Polycarboxylate Ether PCE superplasticizers)
* **Self-Compacting Concrete (SCC) for Dense Rebar / Shear Walls:** Slump flow diameter **600 – 750 mm** (measured by inverted slump cone flow test).

**2. Site Quality Check:**
* Slump test must follow **IS 1199 (Part 2): 2018**.
* Water-cement ratio must never be adjusted on site by adding untracked hose water. Only approved superplasticizers may be redosed if slump loss occurs during transit.""",

    "wind": """### Tower Crane Operation Limits under High Wind (IS 456 / OSHA 1926.1431)

**1. Operational Thresholds:**
* **Warning / Caution Threshold (30 – 38 km/h / ~20–24 knots):** Reduce slewing velocity; prohibited from lifting large flat sail-area loads (formwork gang panels, signboards, large prefabricated glass units).
* **Mandatory Lift Suspension (≥ 38 km/h / 24 knots / 10.5 m/s):** Immediately cease all crane hoisting operations. Ground all suspended loads.
* **Critical Out-of-Service / Weathervane Protocol (≥ 50 km/h):**
  1. Hoist hook block up to minimum 3m below trolley and park trolley near mast base.
  2. Release slewing brake to put jib in **100% free weathervaning mode**. (Locking the slewing brake during heavy wind creates lethal torsional overturning moments on the mast structure!).
  3. Disconnect power to hook travel and isolate cabin supply.

**2. Regulatory Codes:**
* OSHA 1926.1431, ASME B30.3 Tower Cranes, and IS 13367 (Safe use of cranes).""",

    "rebar": """### Rebar Lap Length & Detailing per IS 456:2000 & IS 13920:2016

**1. Tension Lap Length (IS 456 Cl. 26.2.5.1):**
* For deformed bars conforming to **IS 1786 (Fe 500 / Fe 500D)** in tension:
  * $L_d = \\frac{\\phi \\cdot \\sigma_s}{4 \\cdot \\tau_{bd}}$
  * In M25 concrete with Fe500D steel, standard development length is approximately **$41\\phi$**.
  * Where splices occur in tension flexural zones, lap length = $L_d$ or $30\\phi$ (whichever is greater), typically specified on structural drawings as **$45\\phi$ to $50\\phi$**.

**2. Critical Seismic Detailing Rules (IS 13920:2016):**
* **No lapping within plastic hinge zones:** Laps must NEVER be placed within a distance of $2d$ from the column face or beam-column junction.
* **Staggered Splices:** Not more than 50% of tensile reinforcement bars may be spliced at any single section.
* **Special Confining Hoops:** Lap zone must be enclosed with closed shear stirrups spaced at not greater than $100\\text{ mm}$ pitch or $d/4$ throughout lap length."""
}


def get_intelligent_fallback_response(user_query: str) -> str:
    """
    Supplies accurate structural engineering and construction safety answers when offline.
    """
    query_lower = user_query.lower()
    if any(k in query_lower for k in ["cure", "curing", "hydration", "ponding", "days"]):
        return KNOWLEDGE_FALLBACK_ANSWERS["curing"]
    elif any(k in query_lower for k in ["slump", "workability", "cone", "flow", "pour"]):
        return KNOWLEDGE_FALLBACK_ANSWERS["slump"]
    elif any(k in query_lower for k in ["wind", "crane", "gust", "storm", "hoist", "weathervan"]):
        return KNOWLEDGE_FALLBACK_ANSWERS["wind"]
    elif any(k in query_lower for k in ["rebar", "lap", "development", "splice", "reinforcement", "steel", "fe500"]):
        return KNOWLEDGE_FALLBACK_ANSWERS["rebar"]
    else:
        return (
            f"### Expert Structural Engineering Analysis\n\n"
            f"**Query Assessment:** *\"{user_query}\"*\n\n"
            f"Under Indian Standards (**IS 456:2000**, **IS 13920:2016**, **NBC 2016**) and **OSHA 1926** guidelines:\n\n"
            f"1. **Structural & Safety Mandate:** Any alterations to structural geometry, shuttering removal periods, or load-bearing shoring must be vetted against design load calculations (IS 875 Part 2). Formwork stripping under IS 456 Cl. 11.3 requires 16–24 hrs for beam sides/walls, 3 days for slab props left under, 7 days for beam soffits under 6m span, and 14 days for props under beams > 6m.\n"
            f"2. **Quality Verification Protocol:** Verify cube compressive strength testing at 7 and 28 days (IS 516). The 28-day characteristic target strength must satisfy $f_{ck} + 1.65 \\times \\sigma$.\n"
            f"3. **Site Execution Recommendation:** Maintain continuous supervision log, inspect clear covers with spacer blocks conforming to IS 2502, and document safety toolbox talks prior to high-risk activities.\n\n"
            f"*Tip: Connect your Google Gemini API key in the sidebar for live multimodal site vision synthesis and bespoke code solutions.*"
        )


def chat_with_site_assistant(
    user_message: str,
    chat_history: List[Dict[str, str]],
    api_key: Optional[str] = None
) -> Tuple[str, str]:
    """
    Dispatches chat queries to Gemini or intelligent engineering fallback.
    Returns (response_text, execution_mode).
    """
    if not api_key or not api_key.strip():
        response = get_intelligent_fallback_response(user_message)
        return response, "Demonstration Engineering Knowledge Base"

    response, error = call_gemini_chat(
        prompt=user_message,
        history=chat_history,
        api_key=api_key,
        system_instruction=SYSTEM_ENGINEERING_INSTRUCTION
    )

    if error or not response:
        fallback = get_intelligent_fallback_response(user_message)
        return fallback, f"Demo Mode (API Notice: {error or 'Check Gemini Key'})"

    return response, "Live Gemini 1.5 Engineering Assistant"
