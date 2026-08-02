"""
FAIOS Production Engine v13.0 (daily-linkedin-posts-pipeline Standard)
Renders Varun Mayya-style HTML Carousel Cards with Local Image Base64 Data URIs & Valid PDF / PNG Downloads.
"""

import os, sys, json, base64, asyncio, urllib.request, time
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8850369070:AAHe3J6Nz4Ci9OJy1qyMFcryMvCYeUzXYCs')
FOUNDER_CHAT_ID = os.getenv('FOUNDER_TELEGRAM_CHAT_ID', '8519187268')
GOOGLE_APPS_SCRIPT_WEBAPP_URL = os.getenv('GOOGLE_APPS_SCRIPT_WEBAPP_URL', 'https://script.google.com/macros/s/AKfycbxXOpIAijWjS-4a3Ft292jntUwTuKPkHgzzufBaC5AJGQO8xILS14mIONklMq54ox1a/exec')
SECRET_API_KEY = 'futrix_sec_2026_x79q90m3'

LOGO_PATH = "c:\\Users\\L470\\Desktop\\Futrix\\Logo\\Futrix Logo.png"
FAVICON_PATH = "c:\\Users\\L470\\Desktop\\Futrix\\Logo\\favicon.png"

def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

def build_varun_mayya_html(slide_num, total_slides, badge_text, title, subtitle, points):
    logo_base64 = get_base64_image(LOGO_PATH)
    favicon_base64 = get_base64_image(FAVICON_PATH)

    rows_html = ""
    for idx, p in enumerate(points[:4], 1):
        rows_html += f"""
        <div class="point-row">
            <div class="point-icon">{idx}</div>
            <div class="point-text">{p}</div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&display=swap');
  
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    background: #060A12;
    width: 1080px;
    height: 1080px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #F8FAFC;
  }}
  .card {{
    width: 1080px;
    height: 1080px;
    background: radial-gradient(circle at 10% 10%, #1E293B 0%, #060A12 85%);
    border: 6px solid #38BDF8;
    padding: 60px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    box-shadow: inset 0 0 140px rgba(56, 189, 248, 0.3);
  }}
  .top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .brand-logo-group {{
    display: flex;
    align-items: center;
    gap: 20px;
  }}
  .logo-img {{
    height: 70px;
    width: auto;
    filter: drop-shadow(0 0 16px rgba(56, 189, 248, 0.7));
  }}
  .badge {{
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
    border: 2px solid #818CF8;
    color: #A5B4FC;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 10px 24px;
    border-radius: 30px;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
  }}
  .slide-counter {{
    background: rgba(56, 189, 248, 0.15);
    border: 2px solid #38BDF8;
    color: #38BDF8;
    font-weight: 800;
    font-size: 20px;
    padding: 10px 22px;
    border-radius: 20px;
  }}
  .header-block {{
    margin-top: 15px;
  }}
  .title {{
    font-size: 46px;
    font-weight: 900;
    color: #38BDF8;
    line-height: 1.2;
    letter-spacing: -0.5px;
  }}
  .subtitle {{
    font-size: 28px;
    font-weight: 600;
    color: #94A3B8;
    margin-top: 10px;
  }}
  .content-container {{
    background: rgba(15, 23, 42, 0.88);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(56, 189, 248, 0.45);
    border-radius: 24px;
    padding: 36px;
    flex-grow: 1;
    margin: 25px 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.75);
  }}
  .point-row {{
    display: flex;
    align-items: center;
    gap: 20px;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 20px 24px;
    border-radius: 16px;
  }}
  .point-icon {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0284C7 0%, #6366F1 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 22px;
    color: #FFF;
    flex-shrink: 0;
  }}
  .point-text {{
    font-size: 24px;
    font-weight: 700;
    color: #F8FAFC;
    line-height: 1.4;
  }}
  .footer-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 2px solid rgba(255,255,255,0.15);
    padding-top: 20px;
  }}
  .tagline {{
    font-size: 22px;
    font-weight: 800;
    color: #38BDF8;
    letter-spacing: 2px;
  }}
  .swipe-btn {{
    background: #0284C7;
    color: #FFF;
    font-weight: 800;
    font-size: 18px;
    padding: 10px 24px;
    border-radius: 12px;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
  }}
</style>
</head>
<body>
<div class="card">
  <div class="top-bar">
    <div class="brand-logo-group">
      {'<img src="' + favicon_base64 + '" class="logo-img" />' if favicon_base64 else ''}
      <div class="badge">{badge_text}</div>
    </div>
    <div class="slide-counter">SLIDE {slide_num}/{total_slides}</div>
  </div>

  <div class="header-block">
    <div class="title">{title}</div>
    <div class="subtitle">{subtitle}</div>
  </div>

  <div class="content-container">
    {rows_html}
  </div>

  <div class="footer-bar">
    <div class="tagline">FUTRIX AI • LEARN • DECIDE • GROW</div>
    <div class="swipe-btn">SWIPE NEXT ➡️</div>
  </div>
</div>
</body>
</html>"""
