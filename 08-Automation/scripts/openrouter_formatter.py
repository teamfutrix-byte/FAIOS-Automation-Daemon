"""
FAIOS OpenRouter Structural Polish & Sanitization Engine (Free Model Tier)
Formats and cleans captions, threads, and HTML tags for Telegram and Sheets delivery.
"""

import os
import json
import requests

def polish_and_structure_content(raw_data, format_type):
    """
    Uses OpenRouter free model (Gemma-2-9B-It-Free or Llama-3-8B-Instruct-Free)
    to clean up HTML tags, format caption lines, and structure data.
    If OpenRouter key is missing, falls back to Google Gemini API (which is already active).
    """
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    prompt = f"""
You are the FAIOS AI Chief Quality Inspector.
Format the following raw post data for the format '{format_type}'.
Ensure that:
1. No 'FUTRIX AI' or 'AI' suffix next to Futrix is present (change to 'FUTRIX' or 'FUTRIX App').
2. Captions have smooth spacing, emotional touchpoints, and clear footer CTAs.
3. Keep the exact 5 viral hashtags at the bottom.
4. Output strictly a clean JSON block (no markdown wrappers like ```json, just raw JSON) matching this structure:
{{
  "title": "Clean Title",
  "heading": "Clean Card Heading",
  "desc": "Clean Card Body Description (fit for drawing on image)",
  "badge": "Clean Badge Text",
  "caption": "Viral Caption with Footer CTA and 5 Hashtags"
}}

Raw Data:
{json.dumps(raw_data, indent=2)}
"""

    # 1. Try OpenRouter Free Tier
    if openrouter_key:
        try:
            print("[OPENROUTER] Formatting payload using free model tier...")
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openrouter/free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
            r = requests.post(url, json=payload, headers=headers, timeout=12)
            if r.status_code == 200:
                res_content = r.json()["choices"][0]["message"]["content"].strip()
                # Clean possible markdown wrap
                if res_content.startswith("```"):
                    res_content = res_content.split("```")[1]
                    if res_content.startswith("json"):
                        res_content = res_content[4:]
                cleaned_json = json.loads(res_content.strip())
                print("[OPENROUTER] Structural formatting successful!")
                return cleaned_json
            else:
                print(f"[OPENROUTER] Failed formatting with status {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"[OPENROUTER ERROR] Failed: {e}. Falling back to Gemini...")
 
    # 2. Fallback to Gemini API
    if gemini_key:
        try:
            print("[GEMINI FALLBACK] Formatting payload using Gemini API...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            r = requests.post(url, json=payload, headers=headers, timeout=12)
            if r.status_code == 200:
                res_text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                cleaned_json = json.loads(res_text)
                print("[GEMINI FALLBACK] Structural formatting successful!")
                return cleaned_json
            else:
                print(f"[GEMINI FALLBACK] Failed formatting with status {r.status_code}: {r.text[:200]}")
        except Exception as e:
            print(f"[GEMINI FALLBACK ERROR] Formatting failed: {e}")
            
    # Absolute default fallback: return raw data as is
    return {
        "title": raw_data.get("title", "NEET/JEE Prep"),
        "heading": raw_data.get("heading", "FUTRIX STUDY CARD"),
        "desc": raw_data.get("desc", ""),
        "badge": raw_data.get("badge", "FUTRIX"),
        "caption": raw_data.get("caption", "")
    }
