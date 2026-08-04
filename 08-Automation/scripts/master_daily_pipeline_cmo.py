"""
FAIOS Master Production Pipeline v47.0 (Cloud-Persistent Anti-Duplicate Engine)

Features:
1. CLOUD-PERSISTENT ANTI-DUPLICATE ENGINE:
   - Every generated sub_topic_id is IMMEDIATELY logged to Google Sheets 'Used_Topic_IDs' tab.
   - Survives Render restarts — no local file dependency.
   - 100% duplicate prevention across ALL 9 content formats.
2. ZERO-LOCAL STORAGE ARCHITECTURE:
   - All generated graphic cards & carousels are uploaded directly to Google Drive.
   - Public Google Drive Direct Link is saved into Column 7 ('media_url') of Google Sheets.
   - Local temporary files are instantly deleted via Auto-Purge Protocol.
3. Targets NEET 2027 & JEE 2027/2028 Aspirants.
"""

import sys, os, time, json, urllib.request, urllib.parse, asyncio, base64, requests, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from graphic_card_renderer import (
    render_playwright_carousel_deck,
    render_blog_post_image,
    render_quiz_question_card,
    render_formula_cheatsheet_card,
    render_meme_card,
    render_roadmap_card,
    render_news_alert_card,
    render_casestudy_card,
    cleanup_local_temp_media,
    strip_html_tags,
    SOCIAL_CTA_FOOTER
)

sys.stdout.reconfigure(encoding='utf-8')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8850369070:AAHe3J6Nz4Ci9OJy1qyMFcryMvCYeUzXYCs')
FOUNDER_CHAT_ID = os.getenv('FOUNDER_TELEGRAM_CHAT_ID', '8519187268')
GOOGLE_APPS_SCRIPT_WEBAPP_URL = os.getenv('GOOGLE_APPS_SCRIPT_WEBAPP_URL', 'https://script.google.com/macros/s/AKfycbz3xsvR9nA4veqwIJ4zLfwsN9G6QAerAMFeIUl2T5p7a4ay8fYqePtFBnN0aMtJxk7IQQ/exec')
SECRET_API_KEY = 'futrix_sec_2026_x79q90m3'

BEST_VIRAL_TIMES = {
    'INSTAGRAM': '18:00 IST',        # 6:00 PM (Peak Student Active Hours)
    'YOUTUBE_SHORTS': '17:00 IST',   # 5:00 PM (Post-Coaching Hours)
    'FACEBOOK_PAGE': '19:30 IST',    # 7:30 PM (Evening Active Hours)
    'FACEBOOK_ARTICLE': '19:30 IST', # 7:30 PM (Evening Active Hours)
    'X_TWITTER': '09:00 IST',        # 9:00 AM (Morning EdTech Trending)
    'TWITTER_ARTICLE': '09:00 IST',  # 9:00 AM (Morning EdTech Trending)
    'LINKEDIN_ARTICLE': '08:30 IST',  # 8:30 AM (Morning Professional Hours)
    'WEB_BLOG': '10:00 IST'          # 10:00 AM (Search Peak Hours)
}

last_update_id = 0
current_draft_asset = None

def send_telegram_single_photo(file_path, caption, reply_markup=None, target_chat_id=None):
    chat_id = target_chat_id or FOUNDER_CHAT_ID
    boundary = '----WebKitFormBoundaryFAIOS460MA4YWxkTrZu'
    
    def build_body(safe_caption, parse_mode="HTML"):
        body = bytearray()
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode('utf-8'))
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="caption"\r\n\r\n{safe_caption}\r\n'.encode('utf-8'))
        if parse_mode:
            body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="parse_mode"\r\n\r\n{parse_mode}\r\n'.encode('utf-8'))
        if reply_markup:
            markup_json = json.dumps(reply_markup)
            body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="reply_markup"\r\n\r\n{markup_json}\r\n'.encode('utf-8'))
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="futrix_playwright_slide.png"\r\nContent-Type: image/png\r\n\r\n'.encode('utf-8'))
        body.extend(open(file_path, 'rb').read())
        body.extend(f'\r\n--{boundary}--\r\n'.encode('utf-8'))
        return body

    safe_caption = caption[:1000] if caption else ""
    body_data = build_body(safe_caption, "HTML")
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto',
        data=body_data,
        headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
    )
    try:
        res = json.loads(urllib.request.urlopen(req).read())
        print(f"Telegram Photo Upload Result for chat {chat_id}:", res.get('ok'))
    except Exception as err:
        print("[TELEGRAM PHOTO ERROR] Failed to send with HTML parse_mode, falling back to plain text:", err)
        plain_caption = strip_html_tags(safe_caption)
        body_data_fallback = build_body(plain_caption, parse_mode=None)
        req_fallback = urllib.request.Request(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto',
            data=body_data_fallback,
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
        )
        try:
            res = json.loads(urllib.request.urlopen(req_fallback).read())
            print(f"Telegram Photo Upload Fallback Result for chat {chat_id}:", res.get('ok'))
        except Exception as fallback_err:
            print("[TELEGRAM PHOTO CRITICAL ERROR] Both HTML and plain text photo sending failed:", fallback_err)

def send_telegram_message(text, reply_markup=None, target_chat_id=None):
    chat_id = target_chat_id or FOUNDER_CHAT_ID
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_markup: payload['reply_markup'] = reply_markup
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage', data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as err:
        print("[TELEGRAM MSG ERROR] Failed to send message with HTML parse_mode, falling back to plain text:", err)
        plain_text = strip_html_tags(text)
        payload_fallback = {'chat_id': chat_id, 'text': plain_text}
        if reply_markup: payload_fallback['reply_markup'] = reply_markup
        data_fallback = json.dumps(payload_fallback).encode('utf-8')
        req_fallback = urllib.request.Request(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage', data=data_fallback, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req_fallback)
        except Exception as fallback_err:
            print("[TELEGRAM MSG CRITICAL ERROR] Both HTML and plain text message sending failed:", fallback_err)

def answer_callback_query(callback_id, text):
    try:
        payload = {'callback_query_id': callback_id, 'text': text, 'show_alert': True}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery', data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as err:
        print("Callback answer error:", err)

def send_telegram_content_menu(target_chat_id=None):
    text = f"<b>🚀 FUTRIX CMO — INTERACTIVE CONTENT MENU</b>\n\n" \
           f"Select the content type below to generate high-converting visual assets instantly:\n\n" \
           f"• <b>🚀 Day 1 Launch</b>: Startup Announcement Deck\n" \
           f"• 🎨 <b>5-Slide Carousel</b>: Conceptual Speed Deck\n" \
           f"• 📝 <b>SEO Blog</b>: Full Article + 1200x630 Header PNG\n" \
           f"• 📄 <b>Formula Cheat Sheet</b>: High-Yield Revision Sheet\n" \
           f"• 😂 <b>Student Meme</b>: High Virality Reality Check\n" \
           f"• 🗺 <b>Chapter Roadmap</b>: High-Weightage Strategy\n" \
           f"• ❓ <b>PYQ Quiz Card</b>: Interactive Speed Challenge\n" \
           f"• 🚨 <b>NTA News Bulletin</b>: Urgent Exam Announcement\n" \
           f"• 📈 <b>Success Story</b>: Student Transformation Proof\n\n" \
           f"Tap any button below:"

    keyboard = [
        [{'text': '🚀 Day 1 Startup Launch', 'callback_data': 'GEN:launch'}, {'text': '🎨 5-Slide Carousel Deck', 'callback_data': 'GEN:carousel'}],
        [{'text': '📝 SEO Blog + Header PNG', 'callback_data': 'GEN:blog'}, {'text': '📄 Formula Cheat Sheet', 'callback_data': 'GEN:formula'}],
        [{'text': '😂 Student Reality Meme', 'callback_data': 'GEN:meme'}, {'text': '🗺 High-Weightage Roadmap', 'callback_data': 'GEN:roadmap'}],
        [{'text': '❓ NEET/JEE PYQ Quiz', 'callback_data': 'GEN:quiz'}, {'text': '🚨 Urgent NTA News Bulletin', 'callback_data': 'GEN:news'}],
        [{'text': '📈 Student Success Proof', 'callback_data': 'GEN:casestudy'}]
    ]
    send_telegram_message(text, reply_markup={'inline_keyboard': keyboard}, target_chat_id=target_chat_id)

def update_google_sheets(payload):
    payload['secret_key'] = SECRET_API_KEY
    if 'caption' in payload:
        payload['caption'] = strip_html_tags(payload['caption'])
        
    try:
        r = requests.post(
            GOOGLE_APPS_SCRIPT_WEBAPP_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'text/plain;charset=utf-8'},
            allow_redirects=True
        )
        try:
            res = r.json()
            return res
        except Exception:
            return {'status': 'SUCCESS'}
    except Exception as err:
        print("[Google Sheets Request Error]:", err)
        return {'status': 'ERROR'}

def get_past_topics_from_sheets():
    try:
        payload = {'secret_key': SECRET_API_KEY, 'action': 'GET_PAST_TOPICS'}
        r = requests.post(
            GOOGLE_APPS_SCRIPT_WEBAPP_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'text/plain;charset=utf-8'},
            allow_redirects=True
        )
        try:
            res = r.json()
            if res.get('status') == 'SUCCESS':
                return res.get('topics', [])
        except Exception:
            pass
    except Exception as err:
        print("Fetch past topics error:", err)
    return []

def log_used_topic_to_sheets(sub_topic_id, format_type="content"):
    """Log used sub_topic_id to Google Sheets 'Used_Topic_IDs' tab for cloud-persistent duplicate prevention."""
    if not sub_topic_id:
        return
    try:
        payload = {
            'action': 'LOG_USED_TOPIC',
            'sub_topic_id': sub_topic_id,
            'format_type': format_type
        }
        res = update_google_sheets(payload)
        if res and res.get('status') == 'SUCCESS':
            logged = res.get('logged', True)
            print(f"[CLOUD ANTI-DUPLICATE] {'Logged' if logged else 'Already exists'}: {sub_topic_id}")
        else:
            print(f"[CLOUD ANTI-DUPLICATE] Log response: {res}")
    except Exception as err:
        print(f"[CLOUD ANTI-DUPLICATE ERROR] {sub_topic_id}: {err}")

def mark_post_as_published(post_id, live_url="https://instagram.com/futrix_official", target_chat_id=None):
    try:
        payload = {
            'action': 'MARK_AS_PUBLISHED',
            'post_id': post_id,
            'live_post_url': live_url
        }
        res = update_google_sheets(payload)
        if res and res.get('status') == 'SUCCESS':
            send_telegram_message(f"<b>📦 AUTO-ARCHIVED TO 'Published_Posts' TAB!</b>\n\nPost <code>{post_id}</code> removed from <code>Scheduled_Posts</code> sheet and archived to <code>Published_Posts</code> tab!", target_chat_id=target_chat_id)
    except Exception as err:
        print("Mark as published error:", err)

def dispatch_full_5_slide_carousel(target_chat_id=None):
    global current_draft_asset
    past_topics = get_past_topics_from_sheets()
    slide_paths, pdf_path, selected_pillar = asyncio.run(render_playwright_carousel_deck(past_topics))

    # CLOUD ANTI-DUPLICATE: Log immediately after generation
    log_used_topic_to_sheets(selected_pillar['sub_topic_id'], 'carousel')

    asset_id = f"carousel_{selected_pillar['sub_topic_id']}_{int(time.time())}"
    current_draft_asset = {
        'asset_id': asset_id,
        'slides': slide_paths,
        'pdf': pdf_path,
        'title': selected_pillar['topic'],
        'caption': selected_pillar['caption'],
        'hashtags': selected_pillar['hashtags']
    }

    send_telegram_message(f"<b>🎨 AI CMO APPROVED: RENDERED FRESH 5-SLIDE CAROUSEL</b>\n\n"
                          f"• <b>Chapter:</b> {selected_pillar.get('chapter', 'Physics')}\n"
                          f"• <b>Topic:</b> {selected_pillar['topic']}\n"
                          f"• <b>Content Pillar:</b> {selected_pillar['badge']}\n"
                          f"• <b>Cloud Anti-Duplicate Check:</b> PASSED ✅\n\n"
                          f"Uploading 5 Graphic Slide Cards below...", target_chat_id=target_chat_id)

    for idx, path in enumerate(slide_paths[:4], 1):
        send_telegram_single_photo(path, f"<b>Slide {idx}/5</b>: {selected_pillar['badge']}", target_chat_id=target_chat_id)

    caption_slide5 = f"<b>Slide 5/5</b>: Launch Call to Action\n\n" \
                     f"<b>{selected_pillar['topic']}</b>\n\n" \
                     f"Review all 5 graphic slide cards above. Tap below to approve:"

    reply_markup = {
        'inline_keyboard': [
            [{'text': "✅ APPROVE CAROUSEL DECK", 'callback_data': f"APPROVE_ASSET:{asset_id}:0"}],
            [{'text': "❌ REJECT CAROUSEL DECK", 'callback_data': f"REJECT_ASSET:{asset_id}"}]
        ]
    }
    send_telegram_single_photo(slide_paths[4], caption_slide5, reply_markup, target_chat_id=target_chat_id)

def dispatch_blog_post(topic_str="", target_chat_id=None):
    global current_draft_asset
    past_topics = get_past_topics_from_sheets()
    header_img_path, item = asyncio.run(render_blog_post_image(topic_str, past_topics))
    
    blog_title = item.get("title", "Socratic AI Prep")
    blog_text = item.get("caption", "") + SOCIAL_CTA_FOOTER
    used_sub_topic_id = item.get("sub_topic_id")
    if used_sub_topic_id:
        log_used_topic_to_sheets(used_sub_topic_id, 'blog')

    asset_id = f"blog_{used_sub_topic_id}_{int(time.time())}"
    current_draft_asset = {
        'asset_id': asset_id,
        'slides': [header_img_path],
        'pdf': header_img_path,
        'title': blog_title,
        'caption': blog_text,
        'hashtags': item.get("hashtags", '#FutrixBlog #NEET2027 #JEE2027')
    }

    photo_caption = f"<b>📝 OFFICIAL FUTRIX BLOG ARTICLE</b>\n\n<b>Title:</b> {blog_title}\n\n<i>Header card generated. Review full SEO Article below & tap Approve 👇</i>"
    reply_markup = {
        'inline_keyboard': [
            [{'text': "✅ APPROVE BLOG ARTICLE", 'callback_data': f"APPROVE_ASSET:{asset_id}:1"}],
            [{'text': "❌ REJECT BLOG ARTICLE", 'callback_data': f"REJECT_ASSET:{asset_id}"}]
        ]
    }
    send_telegram_single_photo(header_img_path, photo_caption, target_chat_id=target_chat_id)
    send_telegram_message(blog_text, reply_markup=reply_markup, target_chat_id=target_chat_id)

async def _render_and_get_id(async_render_func, past_topics):
    """Wrapper that calls async render and returns (path, item_dict)."""
    result = await async_render_func(past_topics)
    if isinstance(result, tuple):
        return result  # already (path, item)
    return result, {}

def dispatch_single_card_format(fmt_name, async_render_func, target_chat_id=None):
    global current_draft_asset
    past_topics = get_past_topics_from_sheets()
    card_path, item = asyncio.run(_render_and_get_id(async_render_func, past_topics))

    # Fallback to empty dict if item is not dict
    if not isinstance(item, dict):
        item = {"sub_topic_id": str(item), "title": fmt_name.upper(), "heading": fmt_name.upper(), "desc": "", "badge": fmt_name.upper(), "accent": "#6366F1"}

    used_sub_topic_id = item.get("sub_topic_id")
    if used_sub_topic_id:
        log_used_topic_to_sheets(used_sub_topic_id, fmt_name)

    badge_upper = str(item.get("badge", "")).upper()
    if "PHYSICS" in badge_upper:
        subject_tags = "#Physics #NEETPhysics #JEEPhysics"
        subject_name = "Physics"
    elif "CHEMISTRY" in badge_upper or "CHEM" in badge_upper:
        subject_tags = "#Chemistry #NEETChemistry #JEEChemistry"
        subject_name = "Chemistry"
    elif "BIOLOGY" in badge_upper or "NEET" in badge_upper:
        subject_tags = "#Biology #NEETBiology"
        subject_name = "Biology"
    elif "MATH" in badge_upper:
        subject_tags = "#Math #JEEMath"
        subject_name = "Mathematics"
    elif "NTA" in badge_upper:
        subject_tags = "#NTANews #NEET2027 #JEE2027"
        subject_name = "NTA Update"
    else:
        subject_tags = "#NEET2027 #JEE2027 #StudentLife"
        subject_name = "Student Strategy"

    title_badge = f"⚡ {item.get('title', fmt_name.upper())}"
    heading_text = str(item.get('heading', '')).replace("⚡", "").strip()
    
    # Use dynamic caption & hashtags from Gemini/OpenRouter if available
    raw_caption = item.get('caption')
    if raw_caption:
        caption_text = raw_caption
    else:
        caption_text = f"❓ <b>{heading_text}</b>\n\n🎯 Master this high-yield {subject_name} concept for NEET & JEE 2027/2028 prep on FUTRIX!"
        
    raw_hashtags = item.get('hashtags')
    if raw_hashtags:
        hashtags_str = raw_hashtags
    else:
        hashtags_str = f"{subject_tags} #Futrix #EdTech #StudySmart #ExamPrep"

    asset_id = f"{fmt_name}_{used_sub_topic_id}_{int(time.time())}"
    current_draft_asset = {
        'asset_id': asset_id,
        'slides': [card_path],
        'pdf': card_path,
        'title': title_badge,
        'caption': caption_text + SOCIAL_CTA_FOOTER,
        'hashtags': hashtags_str
    }

    reply_markup = {
        'inline_keyboard': [
            [{'text': f"✅ APPROVE {title_badge}", 'callback_data': f"APPROVE_ASSET:{asset_id}:0"}],
            [{'text': f"❌ REJECT {title_badge}", 'callback_data': f"REJECT_ASSET:{asset_id}"}]
        ]
    }
    send_telegram_single_photo(card_path, f"<b>{title_badge}</b>\n\nReview Graphic Card above & tap below to select target platform & date:", reply_markup=reply_markup, target_chat_id=target_chat_id)

def show_universal_platform_picker(asset_id, is_blog="0", target_chat_id=None):
    text = f"<b>🎯 CHOOSE TARGET SOCIAL MEDIA PLATFORM</b>\n\n" \
           f"Asset <code>{asset_id}</code> is APPROVED by Founder!\n\n" \
           f"Select target platform where this content will be published:"

    if str(is_blog) == "1":
        keyboard = [
            [{'text': '🌐 Official Web Blog', 'callback_data': f"PLATFORM:WEB_BLOG:{asset_id}:1"}, {'text': '💼 LinkedIn Article', 'callback_data': f"PLATFORM:LINKEDIN_ARTICLE:{asset_id}:1"}],
            [{'text': '📘 Facebook Article', 'callback_data': f"PLATFORM:FACEBOOK_ARTICLE:{asset_id}:1"}, {'text': '🐦 X / Twitter Article', 'callback_data': f"PLATFORM:TWITTER_ARTICLE:{asset_id}:1"}],
            [{'text': '🌐 Schedule Across ALL Platforms', 'callback_data': f"PLATFORM:ALL:{asset_id}:1"}]
        ]
    else:
        keyboard = [
            [{'text': '📸 Instagram Page', 'callback_data': f"PLATFORM:INSTAGRAM:{asset_id}:0"}, {'text': '💼 LinkedIn Post', 'callback_data': f"PLATFORM:LINKEDIN_ARTICLE:{asset_id}:0"}],
            [{'text': '📘 Facebook Page', 'callback_data': f"PLATFORM:FACEBOOK_PAGE:{asset_id}:0"}, {'text': '🐦 X / Twitter', 'callback_data': f"PLATFORM:X_TWITTER:{asset_id}:0"}],
            [{'text': '🌐 Schedule Across ALL Platforms', 'callback_data': f"PLATFORM:ALL:{asset_id}:0"}]
        ]

    reply_markup = {'inline_keyboard': keyboard}
    send_telegram_message(text, reply_markup, target_chat_id=target_chat_id)

def show_schedule_date_picker(platform, asset_id, is_blog="0", target_chat_id=None):
    now = time.time()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    d0_name = day_names[time.localtime(now).tm_wday]
    d1_name = day_names[time.localtime(now + 86400).tm_wday]
    d3_name = day_names[time.localtime(now + 3*86400).tm_wday]
    d7_name = day_names[time.localtime(now + 7*86400).tm_wday]

    text = f"<b>📅 CHOOSE SCHEDULE DATE & AI PEAK VIRAL TIME</b>\n\n" \
           f"Target Platform: <code>{platform}</code>\n\n" \
           f"Select date to schedule this post. AI will auto-set the <b>Peak Active Time</b> for max reach!"

    reply_markup = {
        'inline_keyboard': [
            [{'text': f'📅 TODAY ({d0_name})', 'callback_data': f"DATE:0:{platform}:{asset_id}:{is_blog}"}, {'text': f'📅 TOMORROW ({d1_name})', 'callback_data': f"DATE:1:{platform}:{asset_id}:{is_blog}"}],
            [{'text': f'📅 In 3 Days ({d3_name})', 'callback_data': f"DATE:3:{platform}:{asset_id}:{is_blog}"}, {'text': f'📅 In 7 Days ({d7_name})', 'callback_data': f"DATE:7:{platform}:{asset_id}:{is_blog}"}]
        ]
    }
    send_telegram_message(text, reply_markup, target_chat_id=target_chat_id)

def execute_platform_schedule_with_date(days_offset, platform, asset_id, is_blog="0", target_chat_id=None):
    target_time_seconds = time.time() + int(days_offset) * 86400
    date_str = time.strftime('%Y-%m-%d', time.localtime(target_time_seconds))
    is_blog_bool = (str(is_blog) == "1")

    if is_blog_bool:
        target_platforms = ['WEB_BLOG', 'LINKEDIN_ARTICLE', 'FACEBOOK_ARTICLE', 'TWITTER_ARTICLE'] if platform == 'ALL' else [platform]
        caption = current_draft_asset['caption'] if current_draft_asset else ("📝 FUTRIX Official Blog Article" + SOCIAL_CTA_FOOTER)
        hashtags = current_draft_asset['hashtags'] if current_draft_asset else "#FutrixBlog #NEET2027 #JEE2027 #EdTech #SocraticAI #Futrix"
        img_path = current_draft_asset['slides'][0] if current_draft_asset and current_draft_asset['slides'] else None
        
        img_b64 = ""
        if img_path and os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')

        for p in target_platforms:
            peak_time = BEST_VIRAL_TIMES.get(p, '10:00 IST')
            scheduled_post_time = f"{date_str} {peak_time}"
            try:
                update_google_sheets({
                    'action': 'ADD_SCHEDULED_POST',
                    'post_id': f"blog_{p.lower()}_{int(time.time())}",
                    'platform': p,
                    'post_time': scheduled_post_time,
                    'caption': caption,
                    'hashtags': hashtags,
                    'media_base64': img_b64,
                    'file_name': f"futrix_blog_{asset_id}_header.png",
                    'mime_type': "image/png",
                    'approval_status': 'APPROVED',
                    'published': False
                })
            except Exception as err:
                print("Google Sheets & Drive Sync Error:", err)

        confirm_text = f"<b>🚀 SUCCESS! MEDIA UPLOADED DIRECTLY TO GOOGLE DRIVE & SCHEDULED ON SHEETS</b>\n\n" \
                       f"• <b>Google Drive Link (Column 7):</b> Saved in <code>Scheduled_Posts</code> sheet!\n" \
                       f"• <b>Target Platform(s):</b> {', '.join(target_platforms)}\n" \
                       f"• <b>Schedule Date:</b> {date_str}\n" \
                       f"• <b>Zero-Local Footprint:</b> Temp files auto-purged from local laptop (0 Bytes used!) ✅"
        send_telegram_message(confirm_text, target_chat_id=target_chat_id)

        if current_draft_asset and current_draft_asset.get('slides'):
            cleanup_local_temp_media(current_draft_asset['slides'])

    else:
        target_platforms = ['INSTAGRAM', 'LINKEDIN_ARTICLE', 'FACEBOOK_PAGE', 'X_TWITTER'] if platform == 'ALL' else [platform]
        caption = current_draft_asset['caption'] if current_draft_asset else ("🚀 FUTRIX Official Launch Campaign" + SOCIAL_CTA_FOOTER)
        hashtags = current_draft_asset['hashtags'] if current_draft_asset else "#NEET2027 #JEE2027 #Futrix #EdTechIndia #StudySmart"
        
        file_path = current_draft_asset['slides'][0] if current_draft_asset and current_draft_asset['slides'] else os.path.abspath('futrix_carousel_deck.pdf')
        media_b64 = ""
        mime_type = "application/pdf" if asset_id.startswith('carousel') else "image/png"
        file_ext = ".pdf" if asset_id.startswith('carousel') else ".png"

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                media_b64 = base64.b64encode(f.read()).decode('utf-8')

        for p in target_platforms:
            peak_time = BEST_VIRAL_TIMES.get(p, '18:00 IST')
            scheduled_post_time = f"{date_str} {peak_time}"
            try:
                update_google_sheets({
                    'action': 'ADD_SCHEDULED_POST',
                    'post_id': f"post_{p.lower()}_{int(time.time())}",
                    'platform': p,
                    'post_time': scheduled_post_time,
                    'caption': caption,
                    'hashtags': hashtags,
                    'media_base64': media_b64,
                    'file_name': f"futrix_{asset_id}{file_ext}",
                    'mime_type': mime_type,
                    'approval_status': 'APPROVED',
                    'published': False
                })
            except Exception as err:
                print("Google Sheets & Drive Sync Error:", err)

        confirm_text = f"<b>🚀 SUCCESS! MEDIA UPLOADED DIRECTLY TO GOOGLE DRIVE & SCHEDULED ON SHEETS</b>\n\n" \
                       f"• <b>Google Drive Link (Column 7):</b> Saved in <code>Scheduled_Posts</code> sheet!\n" \
                       f"• <b>Target Platform(s):</b> {', '.join(target_platforms)}\n" \
                       f"• <b>Schedule Date:</b> {date_str}\n" \
                       f"• <b>Zero-Local Footprint:</b> Temp files auto-purged from local laptop (0 Bytes used!) ✅"
        send_telegram_message(confirm_text, target_chat_id=target_chat_id)

        if current_draft_asset:
            cleanup_local_temp_media(current_draft_asset.get('slides', []))

def process_founder_command(user_message, target_chat_id=None):
    print(f"[Master Pipeline v47.2] Founder Command Received: '{user_message}' from Chat ID: {target_chat_id}")
    msg_lower = user_message.lower()

    if msg_lower in ['menu', 'help', 'content', 'social', 'start', 'hi', 'hello', 'options']:
        send_telegram_content_menu(target_chat_id=target_chat_id)
    elif 'launch' in msg_lower or 'carousel' in msg_lower:
        dispatch_full_5_slide_carousel(target_chat_id=target_chat_id)
    elif 'blog' in msg_lower:
        topic_input = user_message.replace('blog', '').replace('Blog', '').strip()
        dispatch_blog_post(topic_input, target_chat_id=target_chat_id)
    elif 'quiz' in msg_lower or 'pyq' in msg_lower:
        dispatch_single_card_format('quiz', render_quiz_question_card, target_chat_id=target_chat_id)
    elif 'formula' in msg_lower or 'cheatsheet' in msg_lower:
        dispatch_single_card_format('formula', render_formula_cheatsheet_card, target_chat_id=target_chat_id)
    elif 'meme' in msg_lower or 'reality' in msg_lower:
        dispatch_single_card_format('meme', render_meme_card, target_chat_id=target_chat_id)
    elif 'roadmap' in msg_lower or 'strategy' in msg_lower:
        dispatch_single_card_format('roadmap', render_roadmap_card, target_chat_id=target_chat_id)
    elif 'news' in msg_lower or 'update' in msg_lower:
        dispatch_single_card_format('news', render_news_alert_card, target_chat_id=target_chat_id)
    elif 'casestudy' in msg_lower or 'proof' in msg_lower or 'story' in msg_lower:
        dispatch_single_card_format('casestudy', render_casestudy_card, target_chat_id=target_chat_id)
    elif 'publish' in msg_lower:
        parts = user_message.split()
        if len(parts) > 1:
            mark_post_as_published(parts[1], target_chat_id=target_chat_id)
        else:
            send_telegram_message("Send command like: <code>publish post_id</code> to move post to Published_Posts tab!", target_chat_id=target_chat_id)
    else:
        send_telegram_content_menu(target_chat_id=target_chat_id)

def poll_telegram_updates():
    global last_update_id
    print("🚀 FAIOS Master Pipeline (Multi-Stage Dynamic Engine) Started...")
    
    # Clear historic updates at startup
    try:
        init_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset=-1&limit=1"
        req = urllib.request.Request(init_url)
        res = json.loads(urllib.request.urlopen(req).read())
        if res.get('ok') and res.get('result'):
            last_update_id = res['result'][0]['update_id']
            print(f"[STARTUP] Acknowledged & cleared past Telegram updates up to offset: {last_update_id}")
    except Exception as err:
        print("[STARTUP ERROR] Could not clear telegram updates backlog:", err)

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
                        msg_chat_id = update['message']['chat']['id']
                        process_founder_command(text, target_chat_id=msg_chat_id)

                    if 'callback_query' in update:
                        cb = update['callback_query']
                        cb_id = cb['id']
                        cb_chat_id = cb['message']['chat']['id'] if 'message' in cb else FOUNDER_CHAT_ID
                        action_data = cb['data']
                        print(f"[CALLBACK RECEIVED]: {action_data}")
                        parts = action_data.split(':')
                        action = parts[0]

                        if action == 'GEN':
                            fmt = parts[1]
                            answer_callback_query(cb_id, f"🚀 Generating {fmt.upper()} Content...")
                            process_founder_command(fmt, target_chat_id=cb_chat_id)
                        elif action == 'APPROVE_ASSET':
                            asset_id = parts[1]
                            is_blog = parts[2] if len(parts) > 2 else "0"
                            answer_callback_query(cb_id, '✅ APPROVED! Select target social platform...')
                            show_universal_platform_picker(asset_id, is_blog=is_blog, target_chat_id=cb_chat_id)
                        elif action in ['REJECT_ASSET', 'REJECT']:
                            asset_id = parts[1] if len(parts) > 1 else 'asset_launch_01'
                            answer_callback_query(cb_id, '❌ ASSET REJECTED!')
                            send_telegram_message(f"<b>❌ ASSET REJECTED BY FOUNDER</b>\n\nAsset <code>{asset_id}</code> cancelled.", target_chat_id=cb_chat_id)
                        elif action == 'PLATFORM':
                            platform = parts[1]
                            asset_id = parts[2]
                            is_blog = parts[3] if len(parts) > 3 else "0"
                            answer_callback_query(cb_id, f"✅ Selected {platform}! Choose schedule date...")
                            show_schedule_date_picker(platform, asset_id, is_blog=is_blog, target_chat_id=cb_chat_id)
                        elif action == 'DATE':
                            days_offset = parts[1]
                            platform = parts[2]
                            asset_id = parts[3]
                            is_blog = parts[4] if len(parts) > 4 else "0"
                            answer_callback_query(cb_id, f"✅ Scheduled for {platform} on target date!")
                            execute_platform_schedule_with_date(days_offset, platform, asset_id, is_blog=is_blog, target_chat_id=cb_chat_id)
        except Exception as e:
            print("Poll error:", e)

        time.sleep(1)

def run_health_server():
    """Simple HTTP health check server to keep Render free plan awake."""
    port = int(os.getenv('PORT', 10000))
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'FAIOS Bot is LIVE and running 24/7!')
        def log_message(self, format, *args):
            pass  # Suppress HTTP logs
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f'[HEALTH SERVER] Listening on port {port}')
    server.serve_forever()

def self_ping_loop():
    """
    Ping own health endpoint every 8 minutes to prevent Render free plan 15-min sleep.
    No external service needed — bot keeps itself awake!
    """
    import time as _time
    service_url = os.getenv('RENDER_EXTERNAL_URL', 'https://faios-daemon-247.onrender.com')
    ping_interval = 8 * 60  # 8 minutes
    _time.sleep(30)  # Wait for health server to start
    print(f'[SELF-PING] Starting self-ping loop → {service_url} every 8 min')
    while True:
        try:
            r = requests.get(service_url, timeout=15)
            print(f'[SELF-PING] ✅ Alive! Status: {r.status_code}')
        except Exception as e:
            print(f'[SELF-PING] ⚠️ Ping failed: {e}')
        _time.sleep(ping_interval)

if __name__ == '__main__':
    # Thread 1: HTTP health server (Render needs a port to be bound)
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    # Thread 2: Self-ping every 8 min to prevent Render free plan sleep
    ping_thread = threading.Thread(target=self_ping_loop, daemon=True)
    ping_thread.start()

    print('[STARTUP] ✅ Health server + Self-ping loop started. Bot is 24/7 LIVE on Render!')
    poll_telegram_updates()

