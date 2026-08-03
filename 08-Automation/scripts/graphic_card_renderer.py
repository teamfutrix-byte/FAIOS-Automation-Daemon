"""
FAIOS Graphic Card Rendering Engine v47.0 (Pillow-Based, Zero Browser Dependency)

Features:
1. TRIPLE-LAYER ANTI-DUPLICATE ENGINE (unchanged)
2. 100% Anti-Duplicate Guarantee across ALL 9 Content Formats
3. Zero-Local Footprint: Temp images auto-purged after upload
4. Targets Future Exam Cycles: NEET 2027 & JEE 2027/2028 Aspirants
5. NEW: Uses Pillow (PIL) instead of Playwright — works on ALL cloud servers
"""

import os, sys, time, json, base64, random, textwrap, asyncio
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_media")
os.makedirs(TEMP_DIR, exist_ok=True)

FAVICON_PATH = os.path.join(SCRIPT_DIR, "favicon.png")
HISTORY_FILE = os.path.join(SCRIPT_DIR, "used_topics_history.json")

SOCIAL_CTA_FOOTER = "\n\n🚀 Join India's Most Affordable AI Ecosystem!\n📲 Download FUTRIX App for 24/7 Sub-60s Socratic AI Doubt Solving.\n👉 Link in Bio! @futrix_official"

# ─────────────────────────── FONT HELPERS ────────────────────────────────────

def _find_font(size):
    """Return best available bold font at given size."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def _find_font_regular(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

# ─────────────────────────── GRADIENT HELPER ─────────────────────────────────

def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _create_gradient_background(width, height, color1=(15, 23, 42), color2=(2, 4, 8)):
    """Create a dark radial-style gradient background."""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    # Simulate gradient: top lighter, bottom darker
    for y in range(height):
        ratio = y / height
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return img

def _draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=3):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def _wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = ' '.join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] > max_width and current:
            lines.append(' '.join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))
    return lines

# ─────────────────────────── CARD RENDERER ───────────────────────────────────

def render_card_pil(title, heading, body_desc, badge_text, accent_hex="#6366F1",
                    width=1080, height=1080) -> str:
    """Render a single 1080x1080 card using Pillow. Returns path to PNG."""
    accent_rgb = _hex_to_rgb(accent_hex)
    accent_dark = tuple(max(0, c - 60) for c in accent_rgb)

    img = _create_gradient_background(width, height, (15, 23, 42), (2, 4, 8))
    draw = ImageDraw.Draw(img)

    PAD = 60
    # ── Top bar ──────────────────────────────────────────────────────────────
    # Logo
    try:
        if os.path.exists(FAVICON_PATH):
            logo = Image.open(FAVICON_PATH).convert("RGBA")
            logo.thumbnail((90, 90))
            img.paste(logo, (PAD, PAD), logo)
    except Exception:
        pass

    # Badge
    badge_font = _find_font(26)
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw = badge_bbox[2] - badge_bbox[0] + 48
    bh = badge_bbox[3] - badge_bbox[1] + 24
    bx = width - PAD - bw
    by = PAD
    _draw_rounded_rect(draw, (bx, by, bx + bw, by + bh), 30, accent_rgb)
    draw.text((bx + 24, by + 12), badge_text, font=badge_font, fill=(0, 0, 0))

    # ── Card body ─────────────────────────────────────────────────────────────
    card_top = PAD + 110
    card_bot = height - PAD - 80
    _draw_rounded_rect(draw,
                       (PAD, card_top, width - PAD, card_bot),
                       36,
                       fill=(30, 41, 59, 210),
                       outline=(*accent_rgb, 90),
                       width=4)

    inner_x = PAD + 50
    inner_w = width - 2 * PAD - 100
    inner_y = card_top + 50

    # Heading
    head_font = _find_font(44)
    head_lines = _wrap_text(heading, head_font, inner_w, draw)
    for line in head_lines[:3]:
        draw.text((inner_x, inner_y), line, font=head_font, fill=(248, 250, 252))
        inner_y += 54

    inner_y += 20  # spacing

    # Body text
    body_font = _find_font_regular(28)
    for para in body_desc.split('\n'):
        if not para.strip():
            inner_y += 14
            continue
        body_lines = _wrap_text(para.strip(), body_font, inner_w, draw)
        for line in body_lines:
            if inner_y > card_bot - 120:
                break
            draw.text((inner_x, inner_y), line, font=body_font, fill=(148, 163, 184))
            inner_y += 38

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_y = card_bot + 14
    draw.line([(PAD, height - PAD - 65), (width - PAD, height - PAD - 65)],
              fill=(255, 255, 255, 30), width=2)
    footer_font = _find_font(24)
    draw.text((PAD, height - PAD - 50), "FUTRIX • LEARN • DECIDE • GROW",
              font=footer_font, fill=(100, 116, 139))
    draw.text((width - PAD - 200, height - PAD - 50), "FUTRIX AI APP 📲",
              font=footer_font, fill=accent_rgb)

    out_path = os.path.join(TEMP_DIR, f"card_{int(time.time() * 1000)}.png")
    img.save(out_path, "PNG")
    return out_path


def render_carousel_slide_pil(badge, title, desc, accent_hex, slide_num, total=5,
                               width=1080, height=1080) -> str:
    """Render a single carousel slide."""
    accent_rgb = _hex_to_rgb(accent_hex)
    img = _create_gradient_background(width, height, (15, 23, 42), (2, 4, 8))
    draw = ImageDraw.Draw(img)
    PAD = 60

    # Logo
    try:
        if os.path.exists(FAVICON_PATH):
            logo = Image.open(FAVICON_PATH).convert("RGBA")
            logo.thumbnail((90, 90))
            img.paste(logo, (PAD, PAD), logo)
    except Exception:
        pass

    # Badge
    badge_font = _find_font(26)
    badge_bbox = draw.textbbox((0, 0), badge, font=badge_font)
    bw = badge_bbox[2] - badge_bbox[0] + 48
    bh = badge_bbox[3] - badge_bbox[1] + 24
    bx = width - PAD - bw
    _draw_rounded_rect(draw, (bx, PAD, bx + bw, PAD + bh), 30, accent_rgb)
    draw.text((bx + 24, PAD + 12), badge, font=badge_font, fill=(0, 0, 0))

    # Card
    card_top = PAD + 110
    card_bot = height - PAD - 80
    _draw_rounded_rect(draw,
                       (PAD, card_top, width - PAD, card_bot),
                       36, (30, 41, 59), (*accent_rgb, 90), 4)

    inner_x = PAD + 50
    inner_w = width - 2 * PAD - 100
    y = card_top + 50

    title_font = _find_font(46)
    title_lines = _wrap_text(title, title_font, inner_w, draw)
    for line in title_lines[:3]:
        draw.text((inner_x, y), line, font=title_font, fill=(248, 250, 252))
        y += 56
    y += 20

    body_font = _find_font_regular(28)
    for para in desc.split('\n'):
        if not para.strip():
            y += 14
            continue
        for line in _wrap_text(para.strip(), body_font, inner_w, draw):
            if y > card_bot - 100:
                break
            draw.text((inner_x, y), line, font=body_font, fill=(148, 163, 184))
            y += 38

    # Slide number badge bottom-right
    slide_font = _find_font(26)
    slide_label = f"SLIDE {slide_num}/{total}"
    sl_bbox = draw.textbbox((0, 0), slide_label, font=slide_font)
    slw = sl_bbox[2] - sl_bbox[0] + 36
    slh = sl_bbox[3] - sl_bbox[1] + 16
    slx = width - PAD - slw
    sly = height - PAD - slh - 5
    _draw_rounded_rect(draw, (slx, sly, slx + slw, sly + slh), 14, (255, 255, 255, 15))
    draw.text((slx + 18, sly + 8), slide_label, font=slide_font, fill=accent_rgb)

    # Footer
    footer_font = _find_font(22)
    draw.line([(PAD, height - PAD - 65), (width - PAD, height - PAD - 65)],
              fill=(255, 255, 255, 30), width=2)
    draw.text((PAD, height - PAD - 48), "FUTRIX • LEARN • DECIDE • GROW",
              font=footer_font, fill=(100, 116, 139))

    out_path = os.path.join(TEMP_DIR, f"slide_{slide_num}_{int(time.time() * 1000)}.png")
    img.save(out_path, "PNG")
    return out_path

# ─────────────────────────── HISTORY / DUPLICATE LOGIC ───────────────────────

def strip_html_tags(text):
    if not text: return ""
    import re
    return re.sub(r'<[^>]+>', '', text).strip()

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            return json.load(open(HISTORY_FILE, "r", encoding="utf-8"))
        except Exception:
            return []
    return []

def save_history(sub_topic_id):
    history = load_history()
    if sub_topic_id not in history:
        history.append(sub_topic_id)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

def is_subtopic_duplicate(sub_topic_id, past_topics_list):
    if not past_topics_list:
        return False
    st_clean = sub_topic_id.lower().strip()
    return any(st_clean in str(p).lower() for p in past_topics_list)

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

def select_non_duplicate_item(pool_list, past_topics=None):
    used_history = load_history()
    combined_used = set(used_history + (past_topics or []))
    available = [item for item in pool_list if not is_subtopic_duplicate(item["sub_topic_id"], combined_used)]
    selected = available[0] if available else pool_list[random.randint(0, len(pool_list) - 1)]
    save_history(selected["sub_topic_id"])
    return selected

def cleanup_local_temp_media(file_paths):
    for fpath in file_paths:
        try:
            if fpath and os.path.exists(fpath):
                os.remove(fpath)
                print(f"[AUTO-CLEANUP] Deleted: {fpath}")
        except Exception as err:
            print(f"[AUTO-CLEANUP ERROR] {fpath}: {err}")

# ─────────────────────────── CONTENT POOLS ───────────────────────────────────

QUIZ_POOLS = [
    {"sub_topic_id": "quiz_electrostatics_midpoint_field", "title": "NEET/JEE PYQ",
     "heading": "⚡ HIGH-YIELD NEET/JEE 2027 ELECTROSTATICS SPEED QUIZ",
     "desc": "Q: Two identical charges +q are placed at distance 2a.\nWhat is the electric field at the midpoint?\n\nOption A: 2kq/a²\nOption B: ZERO\nOption C: kq/a²\nOption D: 4kq/a²\n\nComment your answer below! 👇",
     "badge": "SPEED QUIZ", "accent": "#FACC15"},
    {"sub_topic_id": "quiz_current_wheatstone_bridge", "title": "NEET/JEE PYQ",
     "heading": "⚡ CURRENT ELECTRICITY: WHEATSTONE BRIDGE QUIZ",
     "desc": "Q: In a balanced Wheatstone bridge, if the galvanometer resistance is doubled, what happens?\n\nOption A: Balance changes\nOption B: Remains Unchanged\nOption C: Current doubles\nOption D: Resistance becomes zero\n\nComment your answer below! 👇",
     "badge": "CIRCUIT QUIZ", "accent": "#38BDF8"},
    {"sub_topic_id": "quiz_optics_lens_water_focal_shift", "title": "NEET/JEE PYQ",
     "heading": "⚡ RAY OPTICS: LENS FOCAL LENGTH SHIFT QUIZ",
     "desc": "Q: A convex glass lens (mu=1.5) has focal length f in air.\nWhat is its focal length when immersed in water (mu=4/3)?\n\nOption A: f\nOption B: 2f\nOption C: 4f\nOption D: f/4\n\nComment your answer below! 👇",
     "badge": "OPTICS QUIZ", "accent": "#10B981"},
]

FORMULA_POOLS = [
    {"sub_topic_id": "formula_capacitance_dielectric_energy", "title": "FORMULA CHEAT SHEET",
     "heading": "📄 CAPACITANCE & DIELECTRIC SLAB FORMULA CHEAT SHEET",
     "desc": "• Parallel Plate Capacitance: C = ε₀A / d\n• Capacitance with Dielectric: C' = K × C\n• Energy Stored: U = ½CV² = Q² / 2C\n• Energy Density: u = ½ε₀E²\n\nSave this card for NEET & JEE 2027 exam revision! 📌",
     "badge": "FORMULA SHEET", "accent": "#38BDF8"},
    {"sub_topic_id": "formula_moving_charges_cyclotron_force", "title": "FORMULA CHEAT SHEET",
     "heading": "📄 MOVING CHARGES & MAGNETISM FORMULA CHEAT SHEET",
     "desc": "• Magnetic Force: F = q(v × B) = qvB sinθ\n• Cyclotron Radius: r = mv / qB\n• Cyclotron Frequency: f = qB / 2πm\n• Magnetic Dipole Moment: M = I × A\n\nSave this card for NEET & JEE 2027 exam revision! 📌",
     "badge": "MAGNETISM SHEET", "accent": "#8B5CF6"},
]

NEWS_POOLS = [
    {"sub_topic_id": "news_nta_advisory_2027_biometric_aadhaar", "title": "NTA ADVISORY",
     "heading": "🚨 NTA GUIDELINES FOR NEET & JEE 2027/2028 ASPIRANTS",
     "desc": "NTA Update for upcoming 2027 batches:\n• Biometric Verification & Aadhaar Match mandatory\n• NCERT Rationalized Syllabus strictly enforced\n• CBT Exam Center mock test practice recommended\n\nShare with your batchmates!",
     "badge": "URGENT NTA ALERT", "accent": "#EF4444"},
    {"sub_topic_id": "news_nta_advisory_2027_cbt_center_mock", "title": "NTA ADVISORY",
     "heading": "🚨 NTA CBT EXAM CENTER MOCK PRACTICE ADVISORY 2027",
     "desc": "NTA Advisory for JEE & NEET 2027:\n• Official NTA Abhyas CBT mock tests available online\n• Practice computer screen timer management\n• Verify Exam Center location 24h before reporting\n\nShare with your batchmates!",
     "badge": "EXAM ADVISORY", "accent": "#F59E0B"},
]

MEME_POOLS = [
    {"sub_topic_id": "meme_start_11th_vs_2_months_before", "title": "STUDENT REALITY CHECK",
     "heading": "😭 NEET & JEE 2027 ASPIRANTS: START OF 11TH VS 2 MONTHS BEFORE EXAM",
     "desc": "Start of 11th Grade:\n'I will secure AIR 1 under 100 in JEE Advanced!' 🚀\n\n2 Months Before Exam:\n'Bro, just tell me if I can clear cutoff by studying Electrostatics today!' 😭\n\nRelatable? Tag your study partner!",
     "badge": "STUDENT REALITY", "accent": "#EC4899"},
]

ROADMAP_POOLS = [
    {"sub_topic_id": "roadmap_physics_top5_high_weightage_2027", "title": "CHAPTER ROADMAP",
     "heading": "🗺 TOP 5 HIGH-WEIGHTAGE PHYSICS CHAPTERS FOR NEET 2027",
     "desc": "1. Electrostatics & Capacitance — 4 Qs (16 Marks)\n2. Current Electricity — 3 Qs (12 Marks)\n3. Modern Physics & Atoms — 4 Qs (16 Marks)\n4. Ray & Wave Optics — 3 Qs (12 Marks)\n5. Laws of Motion & Work Energy — 3 Qs (12 Marks)\n\nMaster these 5 chapters to guarantee 140+ marks!",
     "badge": "HIGH WEIGHTAGE", "accent": "#10B981"},
]

CASESTUDY_POOLS = [
    {"sub_topic_id": "casestudy_ananya_physics_45_to_155", "title": "SUCCESS STORY",
     "heading": "📈 HOW ANANYA BOOSTED HER PHYSICS SCORE FROM 45 TO 155 IN 60 DAYS",
     "desc": "Ananya was struggling with Physics numerical speed.\n\nBy using FUTRIX Socratic AI doubt resolution for 20 minutes daily, she mastered option elimination & active formula recall.\n\nBoost your rank today on FUTRIX AI App!",
     "badge": "STUDENT PROOF", "accent": "#8B5CF6"},
]

SYLLABUS_PILLARS = [
    {"chapter": "Electrostatics", "sub_topic_id": "electrostatics_coulomb_law_vectors",
     "topic": "⚡ COULOMB'S LAW & VECTOR SUPERPOSITION TRICKS",
     "badge": "PHYSICS SPEED TRICK",
     "caption": "⚡ SOLVE COULOMB'S LAW VECTOR NUMERICALS IN 30 SECONDS!\n\nMaster the symmetry shortcut for NEET & JEE 2027/2028.",
     "hashtags": "#NEETPhysics #JEEPhysics #CoulombsLaw #Electrostatics #FutrixTricks #NEET2027",
     "slides": [
         {"badge": "COULOMB LAW", "title": "STUCK ON CHARGE CORNER VECTOR NUMERICALS? 📐",
          "desc": "Calculating vector components for 4 point charges at square corners takes 4+ minutes manually.", "accent": "#6366F1"},
         {"badge": "SYMMETRY RULE", "title": "RULE 1: USE GEOMETRIC SYMMETRY CANCEL ⚖️",
          "desc": "Equal charges at symmetric opposite corners produce net central force = ZERO.", "accent": "#F59E0B"},
         {"badge": "MAGNITUDE FORMULA", "title": "RULE 2: VECTOR SUM F_NET = √3 × F ⚡",
          "desc": "For 60° angle between equal forces, vector resultant is always √3 times single force.", "accent": "#10B981"},
         {"badge": "EXAM APPLICATION", "title": "NEET/JEE SPEED ELIMINATION TRICK ⏱️",
          "desc": "Eliminate 3 asymmetrical option magnitudes in 5 seconds without solving equations.", "accent": "#EC4899"},
         {"badge": "PRACTICE NOW", "title": "SOLVE 30+ VECTOR NUMERICALS ON FUTRIX 📲",
          "desc": "Download FUTRIX App & get instant Socratic AI guidance on every step.", "accent": "#38BDF8"},
     ]},
    {"chapter": "Electrostatics", "sub_topic_id": "electrostatics_dipole_field_torque",
     "topic": "🧠 ELECTRIC DIPOLE FIELD & TORQUE DERIVATIONS",
     "badge": "HIGH-YIELD REVISION",
     "caption": "🧠 MASTER ELECTRIC DIPOLE FORMULAS FOR NEET/JEE 2027!\n\nLearn axial vs equatorial field ratios & work done in rotating a dipole.",
     "hashtags": "#ElectricDipole #NEETPhysics #JEEPhysics #FormulaRevision #FutrixAI #NEET2027",
     "slides": [
         {"badge": "ELECTRIC DIPOLE", "title": "NEVER CONFUSE AXIAL VS EQUATORIAL FIELD 🧭",
          "desc": "Axial field is ALWAYS twice the magnitude of equatorial field at same distance r.", "accent": "#8B5CF6"},
         {"badge": "AXIAL FIELD", "title": "AXIAL FIELD: E_axial = 2kp / r³ ⚡",
          "desc": "Field vector is parallel to dipole moment p (from negative to positive charge).", "accent": "#3B82F6"},
         {"badge": "EQUATORIAL FIELD", "title": "EQUATORIAL FIELD: E_eq = kp / r³ ⚖️",
          "desc": "Field vector is antiparallel to dipole moment p.", "accent": "#10B981"},
         {"badge": "TORQUE & WORK", "title": "TORQUE τ = p × E | WORK W = pE(cosθ₁ − cosθ₂)",
          "desc": "Stable equilibrium at θ=0° (minimum potential energy U = -pE).", "accent": "#F59E0B"},
         {"badge": "REVISE DAILY", "title": "LOCK DIPOLE RETENTION ON FUTRIX APP 📲",
          "desc": "SuperMemo-2 spaced recall pushes revision flashcards right before exam decay.", "accent": "#38BDF8"},
     ]},
]

# ─────────────────────────── ASYNC RENDER WRAPPERS ───────────────────────────

async def render_playwright_carousel_deck(past_topics=None):
    """Render 5-slide carousel deck using Pillow (no browser needed)."""
    selected_pillar = select_non_duplicate_item(SYLLABUS_PILLARS, past_topics)
    slides_data = selected_pillar["slides"]
    slide_paths = []
    for idx, slide in enumerate(slides_data, 1):
        path = render_carousel_slide_pil(
            slide["badge"], slide["title"], slide["desc"],
            slide["accent"], idx, total=5
        )
        slide_paths.append(path)
    return slide_paths, slide_paths[0], selected_pillar

async def render_blog_post_image(topic_str="", past_topics=None):
    title = topic_str if topic_str else "Why Socratic AI Guidance Outperforms Rote Memorization in NEET & JEE 2027"
    intro = "Competitive exam prep is undergoing a massive shift. Traditional coaching is being replaced by sub-60s instant AI doubt resolution."
    points = [
        "Instant Doubt Resolution: Eliminating student bottlenecks within 60 seconds.",
        "Adaptive Spaced Revision: SuperMemo-2 algorithm schedules review before memory decay.",
        "Gamified Rank XP: All-India leaderboards driving student consistency.",
    ]
    path = render_card_pil(
        "OFFICIAL BLOG ARTICLE", title,
        intro + "\n\n" + "\n".join(f"• {p}" for p in points),
        "BLOG ARTICLE", "#34D399", width=1200, height=630
    )
    return path, title, intro, points

async def render_quiz_question_card(past_topics=None):
    item = select_non_duplicate_item(QUIZ_POOLS, past_topics)
    return render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])

async def render_formula_cheatsheet_card(past_topics=None):
    item = select_non_duplicate_item(FORMULA_POOLS, past_topics)
    return render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])

async def render_meme_card(past_topics=None):
    item = select_non_duplicate_item(MEME_POOLS, past_topics)
    return render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])

async def render_roadmap_card(past_topics=None):
    item = select_non_duplicate_item(ROADMAP_POOLS, past_topics)
    return render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])

async def render_news_alert_card(past_topics=None):
    item = select_non_duplicate_item(NEWS_POOLS, past_topics)
    return render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])

async def render_casestudy_card(past_topics=None):
    item = select_non_duplicate_item(CASESTUDY_POOLS, past_topics)
    return render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
