"""
AI Engine Module - Gemini Multimodal Interface & Intelligent Fallback System
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import json
import re
import os
import time
from typing import Optional, Dict, Any, Tuple
from PIL import Image

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Extracts and parses JSON from LLM output, handling markdown fences and extraneous text.
    """
    if not raw_text:
        raise ValueError("Empty response received from LLM.")
    
    # Strip markdown code blocks
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE)
    
    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    
    # Try finding the outermost JSON object
    match = re.search(r'(\{[\s\S]*\})', raw_text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try finding an outermost JSON array
    match_arr = re.search(r'(\[[\s\S]*\])', raw_text)
    if match_arr:
        try:
            return {"data": json.loads(match_arr.group(1))}
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Unable to parse structured JSON from response: {raw_text[:200]}...")


def init_gemini(api_key: Optional[str] = None) -> bool:
    """
    Configures the Gemini SDK if an API key is provided and library is available.
    """
    if not GENAI_AVAILABLE or not api_key:
        return False
    try:
        genai.configure(api_key=api_key.strip())
        return True
    except Exception:
        return False


def call_gemini_vision(
    image: Image.Image,
    prompt: str,
    api_key: Optional[str] = None,
    preferred_model: str = "gemini-1.5-flash"
) -> Tuple[Optional[str], Optional[str]]:
    """
    Executes a multimodal vision request via Gemini SDK.
    Returns (response_text, error_message).
    """
    if not GENAI_AVAILABLE:
        return None, "google-generativeai package not available. Running in demonstration mode."
    
    if not api_key or not api_key.strip():
        return None, "No API key provided. Using demonstration mode."

    models_to_try = [
        preferred_model,
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash"
    ]
    # Remove duplicates preserving order
    seen = set()
    ordered_models = []
    for m in models_to_try:
        if m not in seen:
            seen.add(m)
            ordered_models.append(m)

    last_error = None
    for model_name in ordered_models:
        try:
            genai.configure(api_key=api_key.strip())
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([prompt, image])
            if response and response.text:
                return response.text, None
        except Exception as e:
            last_error = str(e)
            continue

    return None, f"Gemini API request failed: {last_error}"


def call_gemini_chat(
    prompt: str,
    history: list,
    api_key: Optional[str] = None,
    system_instruction: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Executes a multi-turn chat request using Gemini.
    Returns (response_text, error_message).
    """
    if not GENAI_AVAILABLE:
        return None, "google-generativeai package not available. Using demonstration mode."
    
    if not api_key or not api_key.strip():
        return None, "No API key provided. Using demonstration mode."

    try:
        genai.configure(api_key=api_key.strip())
        
        # Prepare model
        kwargs = {}
        if system_instruction:
            kwargs["system_instruction"] = system_instruction
            
        model = genai.GenerativeModel("gemini-1.5-flash", **kwargs)
        
        # Format chat history for Gemini
        gemini_history = []
        for msg in history[:-1]:  # Exclude current prompt
            role = "user" if msg.get("role") == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg.get("content", "")]})
        
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(prompt)
        if response and response.text:
            return response.text, None
        return None, "Received empty response from Gemini model."
    except Exception as e:
        return None, str(e)
