"""
Unit and Integration Tests for Multimodal Construction Intelligence Platform
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import os
import unittest
from PIL import Image

from modules.ai_engine import clean_json_response, init_gemini
from modules.safety_audit import get_demo_safety_data, analyze_site_safety
from modules.crack_diagnostics import get_demo_crack_data, analyze_concrete_crack
from modules.project_planning import (
    calculate_project_metrics,
    generate_pollinations_prompt,
    get_pollinations_image_url,
    format_inr
)
from modules.weather_advisory import (
    WEATHER_PROTOCOLS,
    get_intelligent_fallback_response,
    chat_with_site_assistant
)


class TestConstructionIntelligencePlatform(unittest.TestCase):

    def setUp(self):
        self.sample_img = Image.new("RGB", (100, 100), color=(128, 128, 128))

    def test_clean_json_response(self):
        sample_json_str = '```json\n{"status": "ok", "safety_score": 85}\n```'
        parsed = clean_json_response(sample_json_str)
        self.assertEqual(parsed["status"], "ok")
        self.assertEqual(parsed["safety_score"], 85)

    def test_format_inr(self):
        self.assertEqual(format_inr(15000000), "₹1.50 Cr")
        self.assertEqual(format_inr(450000), "₹4.50 L")
        self.assertEqual(format_inr(75000), "₹75,000")

    def test_safety_audit_fallback(self):
        data = analyze_site_safety(self.sample_img, api_key=None, scenario_id=1)
        self.assertIn("safety_score", data)
        self.assertIn("ppe_detection", data)
        self.assertIn("identified_site_hazards", data)
        self.assertGreaterEqual(data["safety_score"], 0)
        self.assertLessEqual(data["safety_score"], 100)
        self.assertGreater(len(data["ppe_detection"]), 0)

    def test_crack_diagnostics_fallback(self):
        data = analyze_concrete_crack(self.sample_img, api_key=None, defect_case=1)
        self.assertIn("defect_type", data)
        self.assertIn("severity_score", data)
        self.assertIn("engineering_repairs", data)
        self.assertIn("is456_compliance_status", data)
        self.assertGreaterEqual(data["severity_score"], 0)

    def test_project_planning_metrics(self):
        metrics = calculate_project_metrics(
            structure_type="Residential High-Rise (RCC Shear Wall)",
            builtup_sqft=50000,
            location_tier="Tier 1 (Mumbai, Bengaluru, Delhi NCR, Hyderabad, Pune)",
            completion_pct=50,
            specification_level="Premium (Imported fittings, High-speed lifts)"
        )
        self.assertGreater(metrics["total_construction_budget"], 0)
        self.assertEqual(metrics["capex_incurred"], metrics["total_construction_budget"] * 0.5)
        self.assertIn("materials", metrics)
        self.assertGreater(metrics["materials"]["steel_tonnes"], 0)
        self.assertGreater(metrics["materials"]["cement_bags"], 0)

    def test_pollinations_url_generation(self):
        prompt = generate_pollinations_prompt(
            structure_type="Commercial IT Park / Tower",
            location_tier="Tier 1",
            arch_style="Contemporary Glass Curtain Wall",
            lighting_env="Golden hour sunset",
            camera_perspective="Aerial drone 45-degree isometric"
        )
        self.assertIn("Commercial IT Park", prompt)
        url = get_pollinations_image_url(prompt, width=800, height=500, seed=123)
        self.assertTrue(url.startswith("https://image.pollinations.ai/prompt/"))
        self.assertIn("width=800", url)

    def test_weather_advisory(self):
        self.assertIn("High Wind (> 38 km/h / Beaufort Scale 6+)", WEATHER_PROTOCOLS)
        wind_proto = WEATHER_PROTOCOLS["High Wind (> 38 km/h / Beaufort Scale 6+)"]
        self.assertEqual(wind_proto["severity"], "CRITICAL HAZARD")

        curing_ans = get_intelligent_fallback_response("What is the curing duration for PPC under hot weather?")
        self.assertIn("IS 456", curing_ans)

        chat_resp, mode = chat_with_site_assistant("What is the wind limit for tower cranes?", [], api_key=None)
        self.assertIn("Demonstration", mode)
        self.assertIn("Tower Crane", chat_resp)


if __name__ == "__main__":
    unittest.main()
