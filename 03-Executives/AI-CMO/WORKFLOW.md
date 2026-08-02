# AI-CMO Workflow & Social Media Advance Scheduling Loop

> **Executive**: AI CMO (Chief Marketing Officer)  
> **Status**: Active Production Standard (v1.0.0)  

---

## 🔄 End-to-End Reel Production & Advance Scheduling Workflow

```
+-----------------------------------------------------------------------+
| STEP 1: MARKET RESEARCH & TREND DISCOVERY                             |
| AI CMO scans trending NEET/JEE educational reel formats & topics.     |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| STEP 2: DOCUMENTARY SCRIPT & VISUAL SPECIFICATION                     |
| Drafts script in 200-220 WPM energetic tone + visual cue storyboard.   |
| Incorporates reference reels sent by Founder via Telegram (if any).  |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| STEP 3: GOOGLE FLOW VIDEO GENERATION                                  |
| Renders documentary reel using FUTRIX Permanent Avatar on Google Flow.|
| Enforces Mute-Test Rule (visuals explain 100% of concept).            |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| STEP 4: SUBMISSION TO AI CEO & FOUNDER TELEGRAM APPROVAL GATE          |
| Sends package JSON (video URL, caption, scheduled posting time) to    |
| AI CEO, who forwards to Founder Telegram Bot.                         |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
| STEP 5: AUTOMATED ADVANCE SOCIAL MEDIA SCHEDULING                      |
| Upon Founder 'APPROVED' button response on Telegram:                  |
| AI CMO calls n8n workflow to schedule posts on Instagram & Shorts.     |
| Ensures 7-day advance post queue so content is never missed.           |
+-----------------------------------------------------------------------+
```

---

## 📅 Advance Posting Schedule Standard

- **Posting Frequency**: 2 Reels / Day (12:00 PM IST & 07:00 PM IST).
- **Advance Queue Buffer**: Minimum 7 days of approved, pre-scheduled content held in Supabase `scheduled_posts` table.
- **Fail-Safe**: If Founder is traveling or busy, scheduled posts automatically publish via n8n cron without interruption.
