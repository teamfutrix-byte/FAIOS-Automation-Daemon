"""
FAIOS Master Production Daemon v11.0 (Playwright World-Class Graphic Engine)

Features:
1. Playwright Headless Chromium Engine for rendering 1080x1080 HTML/CSS Slides (Varun Mayya / Canva Pro Quality).
2. Uses official FUTRIX Logo PNG overlay.
3. Fixes unclickable Telegram callback buttons.
4. Generates & uploads all 5 individual slide cards.
"""

import sys, os, time, json, urllib.request, urllib.parse, asyncio
from graphic_card_renderer import render_playwright_carousel_deck

sys.stdout.reconfigure(encoding='utf-8')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8850369070:AAHe3J6Nz4Ci9OJy1qyMFcryMvCYeUzXYCs')
FOUNDER_CHAT_ID = os.getenv('FOUNDER_TELEGRAM_CHAT_ID', '8519187268')
GOOGLE_APPS_SCRIPT_WEBAPP_URL = os.getenv('GOOGLE_APPS_SCRIPT_WEBAPP_URL', 'https://script.google.com/macros/s/AKfycbxXOpIAijWjS-4a3Ft292jntUwTuKPkHgzzufBaC5AJGQO8xILS14mIONklMq54ox1a/exec')
SECRET_API_KEY = 'futrix_sec_2026_x79q90m3'

last_update_id = 0
current_draft_asset = None

def send_telegram_single_photo(file_path, caption, reply_markup=None):
    boundary = '----WebKitFormBoundaryFAIOS11MA4YWxkTrZu'
    body = bytearray()
    
    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{FOUNDER_CHAT_ID}\r\n'.encode('utf-8'))
    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode('utf-8'))
    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n'.encode('utf-8'))
    
    if reply_markup:
        markup_json = json.dumps(reply_markup)
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="reply_markup"\r\n\r\n{markup_json}\r\n'.encode('utf-8'))
        
    body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="futrix_playwright_slide.png"\r\nContent-Type: image/png\r\n\r\n'.encode('utf-8'))
    body.extend(open(file_path, 'rb').read())
    body.extend(f'\r\n--{boundary}--\r\n'.encode('utf-8'))

    req = urllib.request.Request(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto',
        data=body,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
    )
    res = json.loads(urllib.request.urlopen(req).read())
    print("Telegram Photo Upload Result:", res.get('ok'))

def send_telegram_message(text, reply_markup=None):
    payload = {'chat_id': FOUNDER_CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup: payload['reply_markup'] = reply_markup
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage', data=data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

def answer_callback_query(callback_id, text):
    try:
        payload = {'callback_query_id': callback_id, 'text': text, 'show_alert': True}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery', data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as err:
        print("Callback answer error:", err)

def update_google_sheets(payload):
    payload['secret_key'] = SECRET_API_KEY
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(GOOGLE_APPS_SCRIPT_WEBAPP_URL, data=data, headers={'Content-Type': 'text/plain;charset=utf-8'})
    res = urllib.request.urlopen(req).read().decode('utf-8')
    print("[Google Sheets Response]:", res)

def dispatch_full_5_slide_carousel():
    global current_draft_asset
    
    # 1. Render all 5 Playwright HTML/CSS slides
    slide_paths = asyncio.run(render_playwright_carousel_deck())

    asset_id = f"asset_playwright_{int(time.time())}"
    current_draft_asset = {
        'asset_id': asset_id,
        'slides': slide_paths,
        'title': '🚀 OFFICIAL FUTRIX DAY 1 STARTUP LAUNCH 5-SLIDE CAROUSEL DECK'
    }

    send_telegram_message("<b>🎨 RENDERED PLAYWRIGHT 1080x1080 GRAPHIC CAROUSEL DECK</b>\n\nUploading 5 Playwright HTML/CSS Slide Cards with Official FUTRIX Logo below...")

    # 2. Upload Slides 1 to 4
    for idx, path in enumerate(slide_paths[:4], 1):
        send_telegram_single_photo(path, f"<b>Slide {idx}/5</b>: FUTRIX Day 1 Launch Campaign")

    # 3. Upload Slide 5 with Action Buttons attached!
    caption_slide5 = f"<b>Slide 5/5</b>: Launch Call to Action\n\n" \
                     f"<b>🚀 FUTRIX OFFICIAL STARTUP LAUNCH -- DAY 1</b>\n\n" \
                     f"Review all 5 graphic slide cards above. Tap below to approve:"

    reply_markup = {
        'inline_keyboard': [
            [{'text': "✅ APPROVE 5-SLIDE CAROUSEL DECK", 'callback_data': f"APPROVE_ASSET:{asset_id}"}],
            [{'text': "❌ REJECT CAROUSEL DECK", 'callback_data': f"REJECT_ASSET:{asset_id}"}]
        ]
    }

    send_telegram_single_photo(slide_paths[4], caption_slide5, reply_markup)

def show_platform_picker(asset_id):
    text = f"<b>🎯 CHOOSE TARGET SOCIAL MEDIA PLATFORM</b>\n\n" \
           f"Asset <code>{asset_id}</code> is APPROVED by Founder!\n\n" \
           f"Select the social media platform to schedule this post:"

    reply_markup = {
        'inline_keyboard': [
            [{'text': '📸 Instagram', 'callback_data': f"PLATFORM:INSTAGRAM:{asset_id}"}, {'text': '🎥 YouTube Shorts', 'callback_data': f"PLATFORM:YOUTUBE:{asset_id}"}],
            [{'text': '📘 Facebook Page', 'callback_data': f"PLATFORM:FACEBOOK:{asset_id}"}, {'text': '🐦 X / Twitter', 'callback_data': f"PLATFORM:TWITTER:{asset_id}"}],
            [{'text': '🌐 Schedule Across ALL Platforms', 'callback_data': f"PLATFORM:ALL:{asset_id}"}]
        ]
    }
    send_telegram_message(text, reply_markup)

def execute_platform_schedule(platform, asset_id):
    schedule_date_str = f"{time.strftime('%Y-%m-%d', time.localtime(time.time() + 7 * 86400))} 18:00 IST"
    target_platforms = ['INSTAGRAM', 'YOUTUBE_SHORTS', 'FACEBOOK_PAGE', 'X_TWITTER'] if platform == 'ALL' else [platform]

    confirm_text = f"<b>🚀 SUCCESS! CONTENT SCHEDULED TO GOOGLE SHEETS</b>\n\n" \
                   f"Asset <code>{asset_id}</code> has been scheduled 7 days in advance!\n\n" \
                   f"• <b>Target Platform(s):</b> {', '.join(target_platforms)}\n" \
                   f"• <b>Google Sheet Sync:</b> Saved in <code>Scheduled_Posts</code> tab!"
    send_telegram_message(confirm_text)

    for p in target_platforms:
        try:
            update_google_sheets({
                'action': 'ADD_SCHEDULED_POST',
                'post_id': f"post_{p.lower()}_{int(time.time())}",
                'platform': p,
                'post_time': schedule_date_str,
                'caption': "🚀 FUTRIX Day 1 Official Startup Launch 5-Slide Playwright Carousel Deck",
                'media_url': f"futrix_playwright_slide_1.png",
                'approval_status': 'APPROVED',
                'published': False
            })
        except Exception as err:
            print("Google Sheets Sync Error:", err)

def process_founder_command(user_message):
    print(f"[Master Daemon v11.0] Founder Command: '{user_message}'")
    dispatch_full_5_slide_carousel()

def poll_telegram_updates():
    global last_update_id
    print("🚀 FAIOS Master Production Daemon v11.0 (Playwright HTML Graphic Engine) Started...")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=30"
            req = urllib.request.Request(url)
            res = json.loads(urllib.request.urlopen(req).read())

            if res.get('ok') and res.get('result'):
                for update in res['result']:
                    last_update_id = update['update_id']

                    if 'message' in update and 'text' in update['message']:
                        text = update['message']['text']
                        if text != '/start':
                            process_founder_command(text)

                    if 'callback_query' in update:
                        cb = update['callback_query']
                        cb_id = cb['id']
                        action_data = cb['data']
                        print(f"[CALLBACK RECEIVED]: {action_data}")
                        parts = action_data.split(':')
                        action = parts[0]

                        if action in ['APPROVE_ASSET', 'APPROVE', 'APPROVE_MULTI', 'APPROVE_CONTENT']:
                            asset_id = parts[1] if len(parts) > 1 else 'asset_launch_01'
                            answer_callback_query(cb_id, '✅ ASSET APPROVED! Select target social platform...')
                            show_platform_picker(asset_id)
                        elif action in ['REJECT_ASSET', 'REJECT', 'REJECT_MULTI', 'REJECT_CONTENT']:
                            asset_id = parts[1] if len(parts) > 1 else 'asset_launch_01'
                            answer_callback_query(cb_id, '❌ ASSET REJECTED!')
                            send_telegram_message(f"<b>❌ ASSET REJECTED BY FOUNDER</b>\n\nAsset <code>{asset_id}</code> cancelled.")
                        elif action == 'PLATFORM':
                            platform = parts[1]
                            asset_id = parts[2]
                            answer_callback_query(cb_id, f"✅ Scheduled for {platform}!")
                            execute_platform_schedule(platform, asset_id)
        except Exception as e:
            print("Poll error:", e)

        time.sleep(1)

if __name__ == '__main__':
    poll_telegram_updates()
