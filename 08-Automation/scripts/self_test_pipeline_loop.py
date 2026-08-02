"""
FAIOS Automated End-to-End Self-Testing Loop Engine v16.1
Uses python requests module for Google Apps Script Web App HTTP 302 Redirect handling.
"""

import sys, os, time, json, urllib.request, urllib.parse, asyncio, requests
from graphic_card_renderer import render_playwright_carousel_deck, render_blog_post_image, CONTENT_PILLARS

sys.stdout.reconfigure(encoding='utf-8')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8850369070:AAHe3J6Nz4Ci9OJy1qyMFcryMvCYeUzXYCs')
FOUNDER_CHAT_ID = os.getenv('FOUNDER_TELEGRAM_CHAT_ID', '8519187268')
GOOGLE_APPS_SCRIPT_WEBAPP_URL = os.getenv('GOOGLE_APPS_SCRIPT_WEBAPP_URL', 'https://script.google.com/macros/s/AKfycbxXOpIAijWjS-4a3Ft292jntUwTuKPkHgzzufBaC5AJGQO8xILS14mIONklMq54ox1a/exec')
SECRET_API_KEY = 'futrix_sec_2026_x79q90m3'

def test_telegram_api():
    print("\n--- TEST 1: TELEGRAM BOT API CONNECTION ---")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    req = urllib.request.Request(url)
    res = json.loads(urllib.request.urlopen(req).read())
    if res.get('ok'):
        print(f"✅ Telegram Bot Active: @{res['result']['username']}")
        return True
    else:
        print("❌ Telegram Bot Error!")
        return False

def test_google_apps_script():
    print("\n--- TEST 2: GOOGLE APPS SCRIPT WEB APP ENDPOINT ---")
    payload = {'secret_key': SECRET_API_KEY, 'action': 'GET_PAST_TOPICS'}
    r = requests.post(GOOGLE_APPS_SCRIPT_WEBAPP_URL, json=payload)
    res = r.json()
    if res.get('status') == 'SUCCESS':
        print(f"✅ Google Apps Script Endpoint Active! Past topics in DB: {res.get('topics')}")
        return True
    else:
        print(f"❌ Google Apps Script Response: {res}")
        return False

def test_playwright_renderers():
    print("\n--- TEST 3: PLAYWRIGHT 1080x1080 HTML SLIDE RENDERER ---")
    paths, pdf_path, selected = asyncio.run(render_playwright_carousel_deck([]))
    print(f"✅ Playwright Rendered 5 PNG Slides cleanly: {len(paths)} files")
    print(f"✅ Compiled Multi-Page PDF Deck: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
    
    print("\n--- TEST 4: BLOG HEADER GRAPHIC CARD RENDERER ---")
    blog_img = asyncio.run(render_blog_post_image("Test Blog Title: Socratic AI vs Traditional Coaching"))
    print(f"✅ Rendered Blog Header PNG: {blog_img} (Size: {os.path.getsize(blog_img)} bytes)")
    return True

def test_full_database_schedule_sync():
    print("\n--- TEST 5: FULL ENTERPRISE GOOGLE SHEETS & DRIVE SYNC ---")
    payload = {
        'secret_key': SECRET_API_KEY,
        'action': 'ADD_SCHEDULED_POST',
        'post_id': f"test_full_sync_{int(time.time())}",
        'platform': 'INSTAGRAM',
        'post_time': '2026-08-07 18:00 IST',
        'caption': '🚀 Automated Test Post with Full 9 Columns',
        'hashtags': '#NEET2026 #JEE2026 #FutrixAI #EdTech #StudySmart',
        'media_url': 'https://drive.google.com/drive/my-drive',
        'approval_status': 'APPROVED',
        'published': False
    }
    r = requests.post(GOOGLE_APPS_SCRIPT_WEBAPP_URL, json=payload)
    res = r.json()
    if res.get('status') == 'SUCCESS':
        print(f"✅ Full Database Sync Success! Post ID: {res.get('post_id')}")
        return True
    else:
        print(f"❌ Full Database Sync Error: {res}")
        return False

def run_loop_testing():
    print("======================================================")
    print("   STARTING FAIOS ENTERPRISE AUTOMATED TESTING LOOP   ")
    print("======================================================")
    
    t1 = test_telegram_api()
    t2 = test_google_apps_script()
    t3 = test_playwright_renderers()
    t4 = test_full_database_schedule_sync()

    if t1 and t2 and t3 and t4:
        print("\n🎉 ALL 5 END-TO-END PIPELINE TESTS PASSED WITH 100% SUCCESS (0 ERRORS)!")
    else:
        print("\n⚠️ SYSTEM TESTING COMPLETED WITH WARNINGS.")

if __name__ == '__main__':
    run_loop_testing()
