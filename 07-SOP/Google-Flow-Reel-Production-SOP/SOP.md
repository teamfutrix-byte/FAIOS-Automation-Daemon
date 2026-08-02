# Standard Operating Procedure: Google Flow Educational Reel Production

---
sop_id: SOP-MKT-REEL-001
name: Google Flow Educational Reel Production
version: 1.0.0
owner: emp_script_writer, emp_insta_mgr, AI CMO
trigger: Daily Content Calendar Cron / Trend Discovery Event
---

## 📋 Objective & Scope
Produce high-retention, documentary-style educational video reels on Google Flow Omini using the locked Founder Avatar and automatically schedule them in advance on Instagram Reels & YouTube Shorts upon receiving Founder Telegram Approval.

## ⚙️ Step-by-Step Procedure
1. **Trend Discovery**: `emp_script_writer` scans trending NEET/JEE educational reel formats.
2. **Script Generation**: Draft 30-60 second script adhering to Master Prompt v14.1 (200-220 WPM, visual-first storytelling, permanent avatar identity lock). Incorporates reference reels sent by Founder via Telegram (if any).
3. **Google Flow Render**: `emp_insta_mgr` renders video reel using Google Flow Omini with locked avatar parameters.
4. **Mute-Test Audit**: Audit video to ensure student understands 100% of concept visually without audio.
5. **Telegram Approval Gate Submission**: Submit proposal JSON (video URL, caption, scheduled posting time) to AI CEO -> Founder Telegram Bot.
6. **Advance Post Scheduling**: Upon receiving Founder Telegram `APPROVED` signal, execute n8n workflow to schedule posts 7 days in advance on Instagram Reels & Shorts.
