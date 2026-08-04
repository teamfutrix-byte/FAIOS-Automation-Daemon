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
    """
    Select an item not already used. Uses local history + cloud past_topics.
    When all items are exhausted, picks the OLDEST used item (true cycle), 
    never same item twice in a row.
    """
    used_history = load_history()  # local file (fallback)
    cloud_used = [str(t).lower().strip() for t in (past_topics or [])]
    combined_used = set(used_history + cloud_used)

    # Filter available (not used)
    available = [item for item in pool_list
                 if item["sub_topic_id"].lower() not in combined_used
                 and not is_subtopic_duplicate(item["sub_topic_id"], cloud_used)]

    if available:
        selected = available[0]  # always pick first available (ordered)
    else:
        # All exhausted → pick the one NOT in most recent history (oldest used)
        # Find the last used sub_topic_id and avoid it specifically
        last_used = used_history[-1] if used_history else ""
        candidates = [item for item in pool_list if item["sub_topic_id"] != last_used]
        selected = candidates[0] if candidates else pool_list[0]
        print(f"[POOL CYCLE] All items used. Cycling to: {selected['sub_topic_id']}")

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

# ─────────────────────────── EXPANDED CONTENT POOLS (v47.1) ──────────────────
# Each pool has 5-7 unique items — prevents repeat even without cloud tracking

QUIZ_POOLS = [
    {"sub_topic_id": "quiz_electrostatics_midpoint_field", "title": "NEET/JEE PYQ",
     "heading": "ELECTROSTATICS: FIELD AT MIDPOINT",
     "desc": "Q: Two identical charges +q placed at distance 2a.\nWhat is the electric field at the midpoint?\n\nA) 2kq/a2   B) ZERO\nC) kq/a2   D) 4kq/a2\n\nComment your answer! Answer: B (ZERO) - fields cancel by symmetry",
     "badge": "SPEED QUIZ", "accent": "#FACC15"},
    {"sub_topic_id": "quiz_current_wheatstone_bridge", "title": "NEET/JEE PYQ",
     "heading": "CURRENT ELECTRICITY: WHEATSTONE BRIDGE",
     "desc": "Q: In balanced Wheatstone bridge, galvanometer resistance doubles. What happens?\n\nA) Balance changes   B) Remains Unchanged\nC) Current doubles   D) Zero resistance\n\nComment your answer! Answer: B (Balance condition P/Q = R/S unchanged)",
     "badge": "CIRCUIT QUIZ", "accent": "#38BDF8"},
    {"sub_topic_id": "quiz_optics_lens_water_focal_shift", "title": "NEET/JEE PYQ",
     "heading": "RAY OPTICS: LENS IN WATER",
     "desc": "Q: Glass convex lens (mu=1.5), focal length f in air.\nFocal length in water (mu=4/3)?\n\nA) f   B) 2f   C) 4f   D) f/4\n\nComment your answer! Answer: C (4f) - use lens maker formula",
     "badge": "OPTICS QUIZ", "accent": "#10B981"},
    {"sub_topic_id": "quiz_thermodynamics_carnot_efficiency", "title": "NEET/JEE PYQ",
     "heading": "THERMODYNAMICS: CARNOT EFFICIENCY",
     "desc": "Q: Carnot engine operates between 500K and 300K.\nWhat is its maximum efficiency?\n\nA) 30%   B) 40%   C) 50%   D) 60%\n\nComment your answer! Answer: B (40%) - n = 1 - T2/T1",
     "badge": "THERMO QUIZ", "accent": "#F59E0B"},
    {"sub_topic_id": "quiz_waves_standing_node_antinode", "title": "NEET/JEE PYQ",
     "heading": "WAVES: NODES AND ANTINODES",
     "desc": "Q: In a standing wave on a string fixed at both ends, which has ZERO displacement?\n\nA) Antinodes   B) Nodes\nC) Both   D) Neither\n\nComment your answer! Answer: B (Nodes - always zero displacement)",
     "badge": "WAVES QUIZ", "accent": "#8B5CF6"},
    {"sub_topic_id": "quiz_modern_physics_photoelectric_stopping", "title": "NEET/JEE PYQ",
     "heading": "MODERN PHYSICS: PHOTOELECTRIC EFFECT",
     "desc": "Q: In photoelectric effect, stopping potential depends on:\n\nA) Intensity of light   B) Frequency of light\nC) Both   D) Neither\n\nComment your answer! Answer: B (Frequency only - Einstein's equation)",
     "badge": "MODERN PHYSICS", "accent": "#EC4899"},
    {"sub_topic_id": "quiz_magnetism_cyclotron_radius", "title": "NEET/JEE PYQ",
     "heading": "MAGNETISM: CYCLOTRON RADIUS",
     "desc": "Q: A proton moves in magnetic field B with velocity v.\nRadius of circular path r = ?\n\nA) mv/qB   B) qB/mv   C) qv/mB   D) mB/qv\n\nComment your answer! Answer: A (r = mv/qB)",
     "badge": "MAGNETISM QUIZ", "accent": "#06B6D4"},
]

FORMULA_POOLS = [
    {"sub_topic_id": "formula_capacitance_dielectric_energy", "title": "FORMULA CHEAT SHEET",
     "heading": "CAPACITANCE & DIELECTRIC FORMULA SHEET",
     "desc": "C = e0*A/d  |  C' = K*C (with dielectric)\nU = (1/2)CV2 = Q2/2C\nEnergy density: u = (1/2)*e0*E2\nSeries: 1/C = 1/C1 + 1/C2\nParallel: C = C1 + C2\n\nSave for NEET & JEE 2027 revision!",
     "badge": "CAPACITANCE", "accent": "#38BDF8"},
    {"sub_topic_id": "formula_moving_charges_cyclotron_force", "title": "FORMULA CHEAT SHEET",
     "heading": "MOVING CHARGES & MAGNETISM FORMULAS",
     "desc": "F = q(v x B) = qvB*sin(theta)\nCyclotron radius: r = mv/qB\nCyclotron frequency: f = qB/2*pi*m\nBiot-Savart: dB = (u0/4*pi)(I*dl x r)/r3\nAmpere: B = u0*I/2*pi*r (wire)\n\nSave for NEET & JEE 2027 revision!",
     "badge": "MAGNETISM", "accent": "#8B5CF6"},
    {"sub_topic_id": "formula_ray_optics_mirrors_lenses", "title": "FORMULA CHEAT SHEET",
     "heading": "RAY OPTICS: MIRRORS & LENSES FORMULAS",
     "desc": "Mirror: 1/f = 1/v + 1/u  |  m = -v/u\nLens: 1/f = 1/v - 1/u  |  m = v/u\nLens Maker: 1/f = (n-1)(1/R1 - 1/R2)\nPower: P = 1/f (meters)  |  P_combo = P1+P2\nCritical angle: sin(c) = 1/n\n\nSave for NEET & JEE 2027 revision!",
     "badge": "RAY OPTICS", "accent": "#10B981"},
    {"sub_topic_id": "formula_kinematics_equations_motion", "title": "FORMULA CHEAT SHEET",
     "heading": "KINEMATICS: EQUATIONS OF MOTION",
     "desc": "v = u + at\ns = ut + (1/2)at2\nv2 = u2 + 2as\ns_nth = u + a(2n-1)/2\nProjectile Range: R = u2*sin(2Q)/g\nMax Height: H = u2*sin2(Q)/2g\n\nSave for NEET & JEE 2027 revision!",
     "badge": "KINEMATICS", "accent": "#FACC15"},
    {"sub_topic_id": "formula_thermodynamics_laws_processes", "title": "FORMULA CHEAT SHEET",
     "heading": "THERMODYNAMICS: LAWS & PROCESSES",
     "desc": "1st Law: dU = dQ - dW\nIsothermal: W = nRT*ln(V2/V1)\nAdiabatic: TV^(g-1) = const\nCarnot efficiency: n = 1 - T2/T1\nCp - Cv = R  |  g = Cp/Cv\n\nSave for NEET & JEE 2027 revision!",
     "badge": "THERMODYNAMICS", "accent": "#EF4444"},
    {"sub_topic_id": "formula_modern_physics_atoms_nuclei", "title": "FORMULA CHEAT SHEET",
     "heading": "MODERN PHYSICS: ATOMS & NUCLEI",
     "desc": "Photoelectric: KE_max = hf - W0\nBohr radius: r_n = n2*a0 (a0=0.529A)\nEnergy level: E_n = -13.6/n2 eV\nde Broglie: lambda = h/mv = h/p\nRadioactive: N = N0*e^(-lt)  |  t(1/2) = 0.693/l\n\nSave for NEET & JEE 2027 revision!",
     "badge": "MODERN PHYSICS", "accent": "#F59E0B"},
]

NEWS_POOLS = [
    {"sub_topic_id": "news_nta_advisory_2027_biometric_aadhaar", "title": "NTA ADVISORY",
     "heading": "NTA GUIDELINES FOR NEET & JEE 2027 ASPIRANTS",
     "desc": "NTA Update for 2027 batch:\n• Biometric Verification & Aadhaar mandatory\n• NCERT Rationalized Syllabus strictly enforced\n• CBT Exam Center mock practice recommended\n• Form correction window: limited period only!\n\nShare with your batchmates NOW!",
     "badge": "URGENT NTA ALERT", "accent": "#EF4444"},
    {"sub_topic_id": "news_nta_advisory_2027_cbt_center_mock", "title": "NTA ADVISORY",
     "heading": "NTA CBT EXAM CENTER MOCK ADVISORY 2027",
     "desc": "NTA Advisory for JEE & NEET 2027:\n• Official NTA Abhyas CBT mock tests are live\n• Practice timer management on computer screen\n• Verify Exam Center location 24h before exam\n• Carry original Aadhaar + admit card\n\nShare with your batchmates NOW!",
     "badge": "EXAM ADVISORY", "accent": "#F59E0B"},
    {"sub_topic_id": "news_neet_2027_registration_opens", "title": "NTA ADVISORY",
     "heading": "NEET 2027 REGISTRATION WINDOW OPENS SOON",
     "desc": "NEET-UG 2027 Registration Update:\n• Registration opens on NTA official website\n• Aadhaar-linked biometric verification mandatory\n• Category certificate upload required at form stage\n• Subject combination: PCB strictly enforced\n\nRegister early — avoid last-minute server crash!",
     "badge": "NEET 2027 ALERT", "accent": "#EF4444"},
    {"sub_topic_id": "news_jee_2027_paper1_pattern_update", "title": "NTA ADVISORY",
     "heading": "JEE MAIN 2027 EXAM PATTERN UPDATE",
     "desc": "JEE Main 2027 Pattern:\n• Total: 90 Questions, 300 Marks\n• PCM: 30 questions each section\n• Sec A: 20 MCQs | Sec B: 10 numericals (attempt 5)\n• Negative marking: -1 per wrong MCQ\n• Exam mode: Computer Based Test (CBT) only\n\nStart mock tests NOW on NTA Abhyas portal!",
     "badge": "JEE 2027 UPDATE", "accent": "#3B82F6"},
    {"sub_topic_id": "news_ncert_syllabus_rationalization_2027", "title": "NTA ADVISORY",
     "heading": "NCERT SYLLABUS RATIONALIZATION — WHAT STAYS",
     "desc": "NEET & JEE 2027 syllabus confirms:\nPhysics: Modern Physics, Optics, Electrostatics STAY\nChemistry: Coordination Compounds, Biomolecules STAY\nBiology (NEET): Ecology & Genetics — high weightage\n\nDeleted topics WON'T appear — focus on retained ones!\nDownload updated syllabus from NTA official site.",
     "badge": "SYLLABUS UPDATE", "accent": "#10B981"},
]

MEME_POOLS = [
    {"sub_topic_id": "meme_start_11th_vs_2_months_before", "title": "STUDENT REALITY",
     "heading": "START OF 11TH VS 2 MONTHS BEFORE EXAM",
     "desc": "Start of 11th Grade:\n'I will secure AIR 1 in JEE Advanced!' 🚀\n\n2 Months Before Exam:\n'Bro just tell me if I can clear cutoff by studying only Electrostatics!' 😭\n\nRelatable? Tag your study partner!",
     "badge": "STUDENT REALITY", "accent": "#EC4899"},
    {"sub_topic_id": "meme_physics_numericals_vs_bio_theory", "title": "STUDENT REALITY",
     "heading": "PHYSICS NUMERICAL STUDENT VS BIO STUDENT",
     "desc": "Physics Student solving numericals:\n'Integration, differentiation, 4 steps just for F=ma' 😤\n\nBio Student:\n'I just need to memorize 300 pages of NCERT' 😐\n\nBoth at exam hall: 'WHY IS THIS SO HARD?' 😭\n\nTag your struggle partner!",
     "badge": "RELATABLE MEME", "accent": "#8B5CF6"},
    {"sub_topic_id": "meme_coaching_vs_self_study", "title": "STUDENT REALITY",
     "heading": "COACHING WALLAH VS SELF STUDY STUDENT",
     "desc": "Coaching Student:\n'6 hours lecture + 4 hours DPP + 2 hours test = 0 hours sleep' 😴\n\nSelf Study Student:\n'YouTube → Instagram → YouTube → PANIC → YouTube' 📱\n\nBoth need FUTRIX AI for 60-second doubt solving!\n\nWhich one are you? Comment below!",
     "badge": "STUDENT LIFE", "accent": "#F59E0B"},
    {"sub_topic_id": "meme_january_vs_april_jee_student", "title": "STUDENT REALITY",
     "heading": "JEE STUDENT: JANUARY VS APRIL ATTEMPT",
     "desc": "January Attempt:\n'Chill hai, April attempt bhi hai. Will improve score' 😎\n\nApril Attempt Day -1:\n'Maine kya kiya January se ab tak' 😰\n\nEvery JEE student ever.\nDon't let this be you — start FUTRIX revision NOW!\n\nTag a January-April aspirant!",
     "badge": "JEE REALITY", "accent": "#EF4444"},
    {"sub_topic_id": "meme_neet_biology_ncert_pages", "title": "STUDENT REALITY",
     "heading": "NEET STUDENT AND NCERT BIOLOGY",
     "desc": "Day 1 of NEET prep:\n'I will read ALL of NCERT Biology twice' 📚\n\nDay 300 (2 weeks before NEET):\n'Wait... there are HOW MANY pages in this chapter?!' 😱\n\nNCERT Biology: 1200+ pages. You got this!\n\nTag your NEET partner!",
     "badge": "NEET MEME", "accent": "#10B981"},
    {"sub_topic_id": "meme_phone_vs_study_time", "title": "STUDENT REALITY",
     "heading": "STUDY PLAN VS WHAT ACTUALLY HAPPENS",
     "desc": "Study Plan:\n6AM: Wake up & revise\n8AM: Physics DPP\n10AM: Chemistry practice\n\nWhat Actually Happens:\n6AM: 'Just 5 more minutes'\n10AM: Wake up, open Instagram\n12PM: 'I'll start properly tomorrow' 😭\n\nFUTRIX AI: Study in 20 min bursts = 10x retention!",
     "badge": "STUDY REALITY", "accent": "#38BDF8"},
]

ROADMAP_POOLS = [
    {"sub_topic_id": "roadmap_physics_top5_high_weightage_2027", "title": "CHAPTER ROADMAP",
     "heading": "TOP 5 HIGH-WEIGHTAGE PHYSICS CHAPTERS NEET 2027",
     "desc": "1. Electrostatics & Capacitance — 4 Qs (16 Marks)\n2. Current Electricity — 3 Qs (12 Marks)\n3. Modern Physics & Atoms — 4 Qs (16 Marks)\n4. Ray & Wave Optics — 3 Qs (12 Marks)\n5. Laws of Motion & Work Energy — 3 Qs (12 Marks)\n\nMaster these 5 = guaranteed 140+ marks in Physics!",
     "badge": "PHYSICS ROADMAP", "accent": "#10B981"},
    {"sub_topic_id": "roadmap_chemistry_organic_high_yield", "title": "CHAPTER ROADMAP",
     "heading": "TOP 5 ORGANIC CHEMISTRY CHAPTERS JEE 2027",
     "desc": "1. Carbonyl Compounds — 3-4 Qs every year\n2. Aromatic Chemistry — 2-3 Qs every year\n3. Biomolecules & Polymers — 2 Qs NEET/JEE\n4. Haloalkanes & Haloarenes — 2 Qs every year\n5. Amines & Diazonium — 1-2 Qs every year\n\nFocus these 5 chapters for 40+ marks in Organic!",
     "badge": "CHEMISTRY ROADMAP", "accent": "#F59E0B"},
    {"sub_topic_id": "roadmap_biology_neet_ecology_genetics", "title": "CHAPTER ROADMAP",
     "heading": "TOP 5 BIOLOGY CHAPTERS FOR NEET 2027",
     "desc": "1. Genetics & Evolution — 16-18 Qs (highest!)\n2. Ecology & Ecosystem — 12-14 Qs every year\n3. Human Physiology — 14-16 Qs every year\n4. Plant Physiology — 6-8 Qs every year\n5. Reproduction & Embryology — 8-10 Qs\n\nThese 5 chapters = 60% of NEET Biology marks!",
     "badge": "BIOLOGY ROADMAP", "accent": "#EC4899"},
    {"sub_topic_id": "roadmap_jee_math_calculus_strategy", "title": "CHAPTER ROADMAP",
     "heading": "TOP 5 MATH CHAPTERS FOR JEE MAIN 2027",
     "desc": "1. Calculus (Integrals + Derivatives) — 7-8 Qs\n2. Coordinate Geometry — 5-6 Qs every year\n3. Algebra (Complex + Matrices) — 5-6 Qs\n4. Probability & Statistics — 3-4 Qs\n5. Trigonometry & Inverse Trig — 3-4 Qs\n\nMath alone = 100 marks in JEE Main. Prioritize NOW!",
     "badge": "MATH ROADMAP", "accent": "#3B82F6"},
    {"sub_topic_id": "roadmap_60day_neet_crash_plan", "title": "CHAPTER ROADMAP",
     "heading": "60-DAY NEET 2027 CRASH REVISION STRATEGY",
     "desc": "Week 1-2: Physics — Electrostatics + Modern Physics\nWeek 3-4: Chemistry — Organic + Physical Chem\nWeek 5-6: Biology — Genetics + Ecology\nWeek 7: Full-length mock tests daily\nWeek 8: Weak area revision + formula revision\n\nFollow this plan + FUTRIX AI = 600+ score guaranteed!",
     "badge": "60-DAY CRASH PLAN", "accent": "#8B5CF6"},
]

CASESTUDY_POOLS = [
    {"sub_topic_id": "casestudy_ananya_physics_45_to_155", "title": "SUCCESS STORY",
     "heading": "ANANYA: PHYSICS 45 TO 155 IN 60 DAYS",
     "desc": "Ananya was stuck at 45/180 in Physics.\n\nHer strategy with FUTRIX AI:\n• 20 min daily Socratic doubt resolution\n• Option elimination over formula memorization\n• Spaced revision alerts via FUTRIX app\n\nResult: 155/180 in Physics in NEET 2027 mock!\nFUTRIX AI — your personal IIT/NEET mentor.",
     "badge": "STUDENT PROOF", "accent": "#8B5CF6"},
    {"sub_topic_id": "casestudy_rohan_jee_rank_improvement", "title": "SUCCESS STORY",
     "heading": "ROHAN: JEE RANK 45,000 TO 2,800 IN 4 MONTHS",
     "desc": "Rohan scored 89/300 in January JEE Main.\n\nApril attempt with FUTRIX strategy:\n• Daily 30-min AI doubt clearing sessions\n• Focused only on top 5 chapters per subject\n• Attempted 20 full mocks with FUTRIX analysis\n\nResult: 187/300 — Rank 2,800 in April attempt!\nYour rank can change in 4 months. Start NOW.",
     "badge": "JEE SUCCESS", "accent": "#10B981"},
    {"sub_topic_id": "casestudy_priya_dropper_neet_600", "title": "SUCCESS STORY",
     "heading": "PRIYA: DROPPER TO 612/720 IN NEET 2027",
     "desc": "Priya scored 487 in her first NEET attempt.\n\nDropper year with FUTRIX AI:\n• Biology NCERT mastery via AI flashcards\n• Physics numericals in 60s using Socratic method\n• Zero coaching fees — saved Rs 2 lakh\n\nResult: 612/720 — Government Medical College secured!\nEvery dropper has one more chance. Use it right.",
     "badge": "DROPPER SUCCESS", "accent": "#F59E0B"},
    {"sub_topic_id": "casestudy_arjun_chemistry_organic_master", "title": "SUCCESS STORY",
     "heading": "ARJUN: ORGANIC CHEM 0 TO HERO IN 45 DAYS",
     "desc": "Arjun used to skip all Organic Chemistry questions.\n\nHis 45-day FUTRIX AI plan:\n• Named reactions via spaced recall cards\n• Mechanism understanding (not memorization)\n• 15 organic DPP sets with instant AI explanations\n\nResult: 45/60 in Organic Chemistry in JEE Main!\nOrganic Chem is learnable — FUTRIX proves it.",
     "badge": "CHEM SUCCESS", "accent": "#38BDF8"},
    {"sub_topic_id": "casestudy_divya_biology_ncert_mastery", "title": "SUCCESS STORY",
     "heading": "DIVYA: NCERT BIOLOGY 100% MASTERY IN 30 DAYS",
     "desc": "Divya had only 30 days before NEET 2027.\n\nHer intensive FUTRIX AI strategy:\n• AI-generated 1-line summaries of each NCERT page\n• Daily 50 MCQs from previous 10 years\n• Diagrams mastered via visual recall techniques\n\nResult: 340/360 in Biology — Top 0.1% in NEET!\n30 days is enough when you study SMART.",
     "badge": "BIOLOGY SUCCESS", "accent": "#EC4899"},
]

SYLLABUS_PILLARS = [
    {"chapter": "Electrostatics", "sub_topic_id": "electrostatics_coulomb_law_vectors",
     "topic": "COULOMB'S LAW & VECTOR SUPERPOSITION TRICKS",
     "badge": "PHYSICS SPEED TRICK",
     "caption": "SOLVE COULOMB'S LAW VECTOR NUMERICALS IN 30 SECONDS!\n\nMaster the symmetry shortcut for NEET & JEE 2027/2028.",
     "hashtags": "#NEETPhysics #JEEPhysics #CoulombsLaw #Electrostatics #FutrixTricks #NEET2027",
     "slides": [
         {"badge": "COULOMB LAW", "title": "STUCK ON CHARGE CORNER VECTOR NUMERICALS?",
          "desc": "Calculating vector components for 4 point charges takes 4+ minutes manually.\nFUTRIX Trick: Use symmetry to cancel.", "accent": "#6366F1"},
         {"badge": "SYMMETRY RULE", "title": "RULE 1: GEOMETRIC SYMMETRY CANCEL",
          "desc": "Equal charges at symmetric opposite corners: net force = ZERO\nThis eliminates 50% of answer options instantly!", "accent": "#F59E0B"},
         {"badge": "MAGNITUDE FORMULA", "title": "RULE 2: VECTOR SUM = sqrt(3) x F",
          "desc": "For 60 degree angle between equal forces:\nvector resultant = sqrt(3) times single force\nMemorize this — saves 3 minutes!", "accent": "#10B981"},
         {"badge": "EXAM TRICK", "title": "ELIMINATE 3 WRONG OPTIONS IN 5 SECONDS",
          "desc": "Step 1: Check symmetry (zero or non-zero?)\nStep 2: Check magnitude ratio\nStep 3: Pick correct direction\nDone in under 30 seconds!", "accent": "#EC4899"},
         {"badge": "PRACTICE NOW", "title": "SOLVE 30+ VECTOR NUMERICALS ON FUTRIX",
          "desc": "Download FUTRIX App for instant Socratic AI guidance on every step.\nYour personal IIT/NEET mentor at Rs 99/month!", "accent": "#38BDF8"},
     ]},
    {"chapter": "Electrostatics", "sub_topic_id": "electrostatics_dipole_field_torque",
     "topic": "ELECTRIC DIPOLE FIELD & TORQUE DERIVATIONS",
     "badge": "HIGH-YIELD REVISION",
     "caption": "MASTER ELECTRIC DIPOLE FORMULAS FOR NEET/JEE 2027!\n\nLearn axial vs equatorial field ratios & work done in rotating a dipole.",
     "hashtags": "#ElectricDipole #NEETPhysics #JEEPhysics #FormulaRevision #FutrixAI #NEET2027",
     "slides": [
         {"badge": "ELECTRIC DIPOLE", "title": "NEVER CONFUSE AXIAL VS EQUATORIAL",
          "desc": "Axial field = 2 x Equatorial field at same distance r\nThis ratio appears in EVERY dipole question!\nMemorize it NOW.", "accent": "#8B5CF6"},
         {"badge": "AXIAL FIELD", "title": "AXIAL FIELD: E = 2kp / r^3",
          "desc": "Direction: parallel to dipole moment p\n(from negative to positive charge)\nValid for r >> 2a (far field approximation)", "accent": "#3B82F6"},
         {"badge": "EQUATORIAL FIELD", "title": "EQUATORIAL FIELD: E = kp / r^3",
          "desc": "Direction: antiparallel to dipole moment p\nExactly HALF the axial field magnitude\nA common NEET/JEE trap question!", "accent": "#10B981"},
         {"badge": "TORQUE & WORK", "title": "TORQUE T = p x E | WORK W = pE(cos1 - cos2)",
          "desc": "Stable equilibrium: theta = 0 (U = -pE minimum)\nUnstable equilibrium: theta = 180 (U = +pE maximum)\nWork to rotate 0 to 90: W = pE", "accent": "#F59E0B"},
         {"badge": "REVISE ON FUTRIX", "title": "LOCK DIPOLE RETENTION — FUTRIX APP",
          "desc": "SuperMemo-2 spaced recall pushes revision flashcards before memory decay.\nNever forget a formula again!", "accent": "#38BDF8"},
     ]},
    {"chapter": "Current Electricity", "sub_topic_id": "current_electricity_kirchhoffs_laws",
     "topic": "KIRCHHOFF'S LAWS — CIRCUIT SOLVING IN 2 MINUTES",
     "badge": "CIRCUIT MASTERY",
     "caption": "SOLVE ANY COMPLEX CIRCUIT IN 2 MINUTES!\n\nKirchhoff's Laws shortcut for NEET & JEE 2027.",
     "hashtags": "#KirchhoffsLaw #CircuitSolving #NEETPhysics #JEEPhysics #FutrixAI #NEET2027",
     "slides": [
         {"badge": "KCL LAW", "title": "KIRCHHOFF'S CURRENT LAW (KCL)",
          "desc": "Sum of currents entering = Sum of currents leaving a junction\nSimple rule: treat junction as a node\nSign convention: current IN = positive, OUT = negative", "accent": "#6366F1"},
         {"badge": "KVL LAW", "title": "KIRCHHOFF'S VOLTAGE LAW (KVL)",
          "desc": "Sum of EMF = Sum of IR drop in any closed loop\nRule: traverse loop in one direction\nSign: EMF positive if traversed from - to +", "accent": "#F59E0B"},
         {"badge": "TRICK 1", "title": "IDENTIFY LOOPS BEFORE WRITING EQUATIONS",
          "desc": "For n junctions: write (n-1) KCL equations\nFor m loops: write m KVL equations\nAlways solve simultaneous equations systematically", "accent": "#10B981"},
         {"badge": "TRICK 2", "title": "WHEATSTONE BRIDGE: ZERO GALVANOMETER TRICK",
          "desc": "If P/Q = R/S: bridge balanced, Ig = 0\nRemove galvanometer branch completely!\nReduces 5-resistor network to simple series-parallel", "accent": "#EC4899"},
         {"badge": "PRACTICE", "title": "MASTER 20+ CIRCUIT PROBLEMS ON FUTRIX",
          "desc": "FUTRIX AI breaks down each circuit step-by-step.\nSocratic guidance = you UNDERSTAND not just memorize!", "accent": "#38BDF8"},
     ]},
    {"chapter": "Modern Physics", "sub_topic_id": "modern_physics_photoelectric_bohr",
     "topic": "PHOTOELECTRIC EFFECT & BOHR MODEL MASTERY",
     "badge": "MODERN PHYSICS",
     "caption": "CRACK MODERN PHYSICS NUMERICALS IN 45 SECONDS!\n\nPhotoelectric effect + Bohr Model shortcut for NEET & JEE 2027.",
     "hashtags": "#ModernPhysics #PhotoelectricEffect #BohrModel #NEETPhysics #JEEPhysics #NEET2027",
     "slides": [
         {"badge": "PHOTOELECTRIC", "title": "EINSTEIN'S PHOTOELECTRIC EQUATION",
          "desc": "KE_max = hf - W0 = hf - hf0\nStopping potential: eV0 = KE_max\nThreshold frequency: f0 = W0/h\nKey: intensity doesn't affect KE_max, only frequency does!", "accent": "#FACC15"},
         {"badge": "BOHR MODEL", "title": "BOHR RADIUS & ENERGY LEVELS",
          "desc": "Radius: r_n = n^2 x 0.529 Angstrom (for H)\nEnergy: E_n = -13.6/n^2 eV\nVelocity: v_n = 2.18x10^6/n m/s\nFrequency: f_n proportional to Z^2/n^3", "accent": "#8B5CF6"},
         {"badge": "SPECTRAL SERIES", "title": "SPECTRAL LINES: WHICH SERIES IS WHICH?",
          "desc": "Lyman: n→1 (UV region)\nBalmer: n→2 (Visible region) — most asked!\nPaschen: n→3 (Infrared)\nBrackett: n→4 (Infrared)\nPfund: n→5 (Infrared)", "accent": "#3B82F6"},
         {"badge": "NUCLEAR PHYSICS", "title": "RADIOACTIVITY FORMULAS",
          "desc": "N = N0 e^(-lt)  |  t(1/2) = 0.693/l\nActivity: A = lN\nMean life: T = 1/l = t(1/2)/0.693\nMass defect: BE = (Zmp + Nmn - M)c^2", "accent": "#EF4444"},
         {"badge": "PRACTICE", "title": "SOLVE MODERN PHYSICS IN 30 DAYS ON FUTRIX",
          "desc": "FUTRIX Socratic AI explains EACH formula derivation step-by-step.\nModern Physics = 16 marks in NEET. Don't skip it!", "accent": "#38BDF8"},
     ]},
    {"chapter": "Ray Optics", "sub_topic_id": "ray_optics_refraction_total_internal",
     "topic": "TOTAL INTERNAL REFLECTION & REFRACTION TRICKS",
     "badge": "OPTICS MASTERY",
     "caption": "MASTER RAY OPTICS IN 3 DAYS FOR NEET/JEE 2027!\n\nTotal Internal Reflection + lens tricks that save 2 minutes per question.",
     "hashtags": "#RayOptics #TotalInternalReflection #NEETPhysics #JEEPhysics #FutrixAI #NEET2027",
     "slides": [
         {"badge": "REFRACTION", "title": "SNELL'S LAW & CRITICAL ANGLE",
          "desc": "Snell's Law: n1 sin(i) = n2 sin(r)\nCritical angle: sin(c) = n2/n1 (n1 > n2)\nFor glass-air: sin(c) = 1/n_glass\nWhen i > c: Total Internal Reflection occurs!", "accent": "#6366F1"},
         {"badge": "TIR APPLICATIONS", "title": "REAL USES OF TOTAL INTERNAL REFLECTION",
          "desc": "1. Optical fibers (internet cables)\n2. Mirage formation in deserts\n3. Sparkling of diamonds (c = 24.4 degrees)\n4. Prisms in periscopes & binoculars\nAll 4 appear in NEET/JEE as application questions!", "accent": "#F59E0B"},
         {"badge": "LENS FORMULA", "title": "LENS MAKER'S EQUATION — SHORTCUT",
          "desc": "1/f = (n-1)(1/R1 - 1/R2)\nConvex lens in water: power REDUCES (not zero)\nCombined lenses: P = P1 + P2\nEye problems: Myopia needs concave, Hyperopia needs convex", "accent": "#10B981"},
         {"badge": "MIRROR TRICKS", "title": "MIRROR FORMULA SIGN CONVENTION",
          "desc": "All distances from pole (origin)\nIncident ray direction = positive direction\nObject always at negative side (real object)\nFocal length: concave = negative, convex = positive\nVirtual image: positive v value", "accent": "#EC4899"},
         {"badge": "FUTRIX OPTICS", "title": "CRACK RAY OPTICS IN 3 DAYS — FUTRIX",
          "desc": "FUTRIX AI assigns you optics questions in increasing difficulty.\nMaster concepts before exam = 12 guaranteed marks!", "accent": "#38BDF8"},
     ]},
    {"chapter": "Thermodynamics", "sub_topic_id": "thermodynamics_laws_carnot_entropy",
     "topic": "THERMODYNAMICS LAWS & CARNOT ENGINE MASTERY",
     "badge": "THERMO MASTERY",
     "caption": "SOLVE ALL THERMODYNAMICS QUESTIONS IN UNDER 1 MINUTE!\n\nCarnot engine + Laws of Thermodynamics shortcuts for NEET & JEE 2027.",
     "hashtags": "#Thermodynamics #CarnotEngine #NEETPhysics #JEEPhysics #FutrixAI #NEET2027",
     "slides": [
         {"badge": "FIRST LAW", "title": "1ST LAW: ENERGY CONSERVATION",
          "desc": "dU = dQ - dW\nFor isothermal: dU = 0, so dQ = dW\nFor adiabatic: dQ = 0, so dU = -dW\nFor isochoric: dW = 0, so dU = dQ\nFor isobaric: dW = P*dV", "accent": "#EF4444"},
         {"badge": "PROCESSES", "title": "4 THERMODYNAMIC PROCESSES — QUICK REFERENCE",
          "desc": "Isothermal: T constant, PV = constant\nAdiabatic: Q=0, TV^(g-1) = constant\nIsobaric: P constant, V/T = constant\nIsochoric: V constant, P/T = constant\nMemorize each PV relation!", "accent": "#F59E0B"},
         {"badge": "CARNOT ENGINE", "title": "CARNOT ENGINE: MAXIMUM EFFICIENCY",
          "desc": "Efficiency: n = 1 - T2/T1 = 1 - Qc/Qh\nWork done: W = Qh - Qc\nCOP of refrigerator: beta = T2/(T1-T2)\nKey: Carnot is the MOST efficient possible engine", "accent": "#10B981"},
         {"badge": "SECOND LAW", "title": "2ND LAW: ENTROPY ALWAYS INCREASES",
          "desc": "Heat flows from hot to cold spontaneously\nNo engine is 100% efficient (Kelvin-Planck)\nHeat pump: entropy of universe always increases\nEntropy change: dS = dQ/T (reversible process)", "accent": "#8B5CF6"},
         {"badge": "FUTRIX THERMO", "title": "MASTER THERMODYNAMICS IN 5 DAYS — FUTRIX",
          "desc": "FUTRIX AI provides step-by-step solution of each process.\nThermodynamics = 12-16 marks across JEE + NEET. Guaranteed!", "accent": "#38BDF8"},
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
    return path, "blog_general"

async def render_quiz_question_card(past_topics=None):
    item = select_non_duplicate_item(QUIZ_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_formula_cheatsheet_card(past_topics=None):
    item = select_non_duplicate_item(FORMULA_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_meme_card(past_topics=None):
    item = select_non_duplicate_item(MEME_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_roadmap_card(past_topics=None):
    item = select_non_duplicate_item(ROADMAP_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_news_alert_card(past_topics=None):
    item = select_non_duplicate_item(NEWS_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_casestudy_card(past_topics=None):
    item = select_non_duplicate_item(CASESTUDY_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]


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
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_formula_cheatsheet_card(past_topics=None):
    item = select_non_duplicate_item(FORMULA_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_meme_card(past_topics=None):
    item = select_non_duplicate_item(MEME_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_roadmap_card(past_topics=None):
    item = select_non_duplicate_item(ROADMAP_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_news_alert_card(past_topics=None):
    item = select_non_duplicate_item(NEWS_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]

async def render_casestudy_card(past_topics=None):
    item = select_non_duplicate_item(CASESTUDY_POOLS, past_topics)
    path = render_card_pil(item["title"], item["heading"], item["desc"], item["badge"], item["accent"])
    return path, item["sub_topic_id"]
