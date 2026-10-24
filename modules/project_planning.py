"""
Project Planning & Real Estate Valuation Module
CapEx Forecasting, Valuation in INR (Lakhs/Crores), Material BOM & Pollinations AI 3D Rendering
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import urllib.parse
from typing import Dict, Any, Tuple
import pandas as pd


# Benchmarking constants based on Indian Construction Cost Indices (2025-2026 CPWD / RICS benchmarks)
COST_BENCHMARKS = {
    "Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune)": {
        "Residential High-Rise (RCC Shear Wall)": {"base_cost": 2950, "market_rate": 14500},
        "Commercial IT Park / Tower": {"base_cost": 3400, "market_rate": 16800},
        "Industrial Pre-Engineered Warehouse": {"base_cost": 1950, "market_rate": 7800},
        "Luxury Villa / Gated Township": {"base_cost": 3800, "market_rate": 22000},
        "Metro / Transit Infrastructure": {"base_cost": 4600, "market_rate": 19000}
    },
    "Tier 2 (Ahmedabad, Jaipur, Chandigarh, Kochi, Lucknow, Indore)": {
        "Residential High-Rise (RCC Shear Wall)": {"base_cost": 2250, "market_rate": 7800},
        "Commercial IT Park / Tower": {"base_cost": 2650, "market_rate": 9200},
        "Industrial Pre-Engineered Warehouse": {"base_cost": 1600, "market_rate": 4800},
        "Luxury Villa / Gated Township": {"base_cost": 2900, "market_rate": 12500},
        "Metro / Transit Infrastructure": {"base_cost": 3800, "market_rate": 11500}
    },
    "Tier 3 (Bhopal, Coimbatore, Visakhapatnam, Emerging Cities)": {
        "Residential High-Rise (RCC Shear Wall)": {"base_cost": 1850, "market_rate": 4800},
        "Commercial IT Park / Tower": {"base_cost": 2150, "market_rate": 5900},
        "Industrial Pre-Engineered Warehouse": {"base_cost": 1350, "market_rate": 3400},
        "Luxury Villa / Gated Township": {"base_cost": 2300, "market_rate": 7500},
        "Metro / Transit Infrastructure": {"base_cost": 3100, "market_rate": 7200}
    }
}

SPEC_MULTIPLIERS = {
    "Standard (Affordable / Mid-Segment)": 1.00,
    "Premium (Imported fittings, High-speed lifts)": 1.22,
    "Ultra-Luxury (Italian Marble, Glass Curtain Wall, Automation)": 1.55
}

# Material consumption factors per sqft of built-up area (Indian Standard CPWD thumb rules)
MATERIAL_FACTORS = {
    "Residential High-Rise (RCC Shear Wall)": {
        "steel_kg_per_sqft": 4.60,
        "cement_bags_per_sqft": 0.44,
        "rmc_cu_m_per_sqft": 0.052,
        "sand_cft_per_sqft": 1.80
    },
    "Commercial IT Park / Tower": {
        "steel_kg_per_sqft": 5.20,
        "cement_bags_per_sqft": 0.48,
        "rmc_cu_m_per_sqft": 0.058,
        "sand_cft_per_sqft": 1.95
    },
    "Industrial Pre-Engineered Warehouse": {
        "steel_kg_per_sqft": 3.80,
        "cement_bags_per_sqft": 0.28,
        "rmc_cu_m_per_sqft": 0.035,
        "sand_cft_per_sqft": 1.20
    },
    "Luxury Villa / Gated Township": {
        "steel_kg_per_sqft": 3.90,
        "cement_bags_per_sqft": 0.42,
        "rmc_cu_m_per_sqft": 0.048,
        "sand_cft_per_sqft": 1.70
    },
    "Metro / Transit Infrastructure": {
        "steel_kg_per_sqft": 6.80,
        "cement_bags_per_sqft": 0.62,
        "rmc_cu_m_per_sqft": 0.075,
        "sand_cft_per_sqft": 2.30
    }
}


def format_inr(amount: float) -> str:
    """
    Formats INR amounts into Lakhs and Crores for executive presentation.
    """
    if amount >= 10000000:  # >= 1 Crore (100 Lakhs)
        crores = amount / 10000000
        return f"₹{crores:,.2f} Cr"
    elif amount >= 100000:  # >= 1 Lakh
        lakhs = amount / 100000
        return f"₹{lakhs:,.2f} L"
    else:
        return f"₹{amount:,.0f}"


def calculate_project_metrics(
    structure_type: str,
    builtup_sqft: float,
    location_tier: str,
    completion_pct: float,
    specification_level: str
) -> Dict[str, Any]:
    """
    Calculates detailed CapEx, real estate valuation, and material bills of quantities.
    """
    tier_data = COST_BENCHMARKS.get(location_tier, COST_BENCHMARKS["Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune)"])
    struct_bench = tier_data.get(structure_type, tier_data["Residential High-Rise (RCC Shear Wall)"])
    spec_mult = SPEC_MULTIPLIERS.get(specification_level, 1.0)

    effective_cost_per_sqft = struct_bench["base_cost"] * spec_mult
    effective_market_rate_per_sqft = struct_bench["market_rate"] * (1.0 + (spec_mult - 1.0) * 0.75)

    total_construction_budget = effective_cost_per_sqft * builtup_sqft
    capex_incurred = total_construction_budget * (completion_pct / 100.0)
    capex_remaining = total_construction_budget - capex_incurred

    # Valuation logic:
    # Finished Asset Value (GDV - Gross Development Value)
    gdv_finished = effective_market_rate_per_sqft * builtup_sqft
    
    # As-Is Current Valuation:
    # Based on land residual base (approx 35% of finished rate) + work completed value + location premium
    land_and_permits_val = gdv_finished * 0.35
    structure_addition = (gdv_finished - land_and_permits_val) * (completion_pct / 100.0)
    current_asset_valuation = land_and_permits_val + structure_addition

    # Material estimations
    mat_factors = MATERIAL_FACTORS.get(structure_type, MATERIAL_FACTORS["Residential High-Rise (RCC Shear Wall)"])
    total_steel_tonnes = (mat_factors["steel_kg_per_sqft"] * builtup_sqft) / 1000.0
    total_cement_bags = mat_factors["cement_bags_per_sqft"] * builtup_sqft
    total_rmc_cum = mat_factors["rmc_cu_m_per_sqft"] * builtup_sqft
    total_sand_cft = mat_factors["sand_cft_per_sqft"] * builtup_sqft

    # Progress S-curve breakdown
    milestones = [
        {"Milestone": "Substructure & Piling", "Target %": 15, "Planned Cost": total_construction_budget * 0.15},
        {"Milestone": "Superstructure RCC Framing", "Target %": 45, "Planned Cost": total_construction_budget * 0.30},
        {"Milestone": "Blockwork & Plastering", "Target %": 65, "Planned Cost": total_construction_budget * 0.20},
        {"Milestone": "MEP (HVAC/Electrical/Plumbing)", "Target %": 85, "Planned Cost": total_construction_budget * 0.20},
        {"Milestone": "Finishes, Facade & Handover", "Target %": 100, "Planned Cost": total_construction_budget * 0.15}
    ]

    current_milestone = "Pre-Construction"
    for m in milestones:
        if completion_pct >= m["Target %"]:
            current_milestone = m["Milestone"] + " (Completed)"
        else:
            current_milestone = m["Milestone"] + " (In Progress)"
            break

    # Cost breakdown for charts
    cost_breakdown_df = pd.DataFrame({
        "Component": ["Civil & Substructure", "MEP & Vertical Transport", "Finishing & Facade", "Project Management & Contingency"],
        "Share (%)": [44, 22, 24, 10],
        "Amount (INR)": [
            total_construction_budget * 0.44,
            total_construction_budget * 0.22,
            total_construction_budget * 0.24,
            total_construction_budget * 0.10
        ]
    })

    return {
        "builtup_sqft": builtup_sqft,
        "effective_cost_per_sqft": effective_cost_per_sqft,
        "effective_market_rate_per_sqft": effective_market_rate_per_sqft,
        "total_construction_budget": total_construction_budget,
        "total_budget_formatted": format_inr(total_construction_budget),
        "capex_incurred": capex_incurred,
        "capex_incurred_formatted": format_inr(capex_incurred),
        "capex_remaining": capex_remaining,
        "capex_remaining_formatted": format_inr(capex_remaining),
        "current_asset_valuation": current_asset_valuation,
        "current_valuation_formatted": format_inr(current_asset_valuation),
        "gdv_finished": gdv_finished,
        "gdv_finished_formatted": format_inr(gdv_finished),
        "completion_pct": completion_pct,
        "current_milestone": current_milestone,
        "materials": {
            "steel_tonnes": round(total_steel_tonnes, 1),
            "cement_bags": int(total_cement_bags),
            "rmc_cum": round(total_rmc_cum, 1),
            "sand_brass": round(total_sand_cft / 100.0, 1)  # 1 Brass = 100 cu ft
        },
        "materials_consumed": {
            "steel_tonnes": round(total_steel_tonnes * (completion_pct / 100.0), 1),
            "cement_bags": int(total_cement_bags * (completion_pct / 100.0)),
            "rmc_cum": round(total_rmc_cum * (completion_pct / 100.0), 1),
            "sand_brass": round((total_sand_cft / 100.0) * (completion_pct / 100.0), 1)
        },
        "milestones": milestones,
        "cost_breakdown_df": cost_breakdown_df
    }


def generate_pollinations_prompt(
    structure_type: str,
    location_tier: str,
    arch_style: str,
    lighting_env: str,
    camera_perspective: str,
    completion_stage: str = "Completed Architectural Masterpiece"
) -> str:
    """
    Constructs an optimized visual prompt for Pollinations AI / Flux architectural generation.
    """
    clean_tier = location_tier.split("(")[0].strip()
    prompt = (
        f"Hyperrealistic 8k architectural photograph of a {structure_type} in {clean_tier}, India. "
        f"Design style: {arch_style}. "
        f"Construction stage: {completion_stage}. "
        f"Camera view: {camera_perspective}, wide-angle architectural lens, tilt-shift lens perspective. "
        f"Lighting: {lighting_env}, photorealistic reflections, natural atmospheric depth, lush landscaped podium, "
        f"modern glass curtain walls, textured fair-faced concrete, warm interior lighting visible, "
        f"award-winning architectural digest photography, raytraced shadows, unreal engine 5 render look."
    )
    return prompt


def get_pollinations_image_url(
    prompt: str,
    width: int = 1024,
    height: int = 640,
    seed: int = 42,
    model: str = "flux"
) -> str:
    """
    Constructs a direct HTTPS image URL from Pollinations AI endpoint.
    """
    encoded_prompt = urllib.parse.quote(prompt.strip())
    # Pollinations image endpoint format
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true&model={model}"
    return url
