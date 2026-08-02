# Inter-Executive Communication Protocol

> **System**: FAIOS (FUTRIX AI Operating System)  
> **Document Type**: Cross-Agent Communication Architecture  
> **Status**: Active Production Standard (v1.0.0)  

---

## 📌 Overview

The **Inter-Executive Communication Protocol** governs how all 15 AI Executives asynchronously and synchronously communicate, delegate tasks, request technical assets, submit content for approval, and resolve operational conflicts.

---

## 🔄 Messaging Topology & JSON Schema

All executive communications use structured JSON messages dispatched across the internal event bus.

### 1. Inter-Executive Message Schema

```json
{
  "$schema": "https://futrix.ai/schemas/inter_executive_msg.v1.json",
  "message_id": "msg_20260730_cmo_ceo_reel_001",
  "timestamp": "2026-07-30T21:25:00Z",
  "sender": "AI-CMO",
  "recipient": "AI-CEO",
  "priority": "HIGH",
  "intent": "APPROVAL_REQUEST",
  "context": {
    "module": "Marketing-Growth",
    "topic": "Social Educational Reel Scheduling",
    "reference_materials": [
      "https://t.me/futrix_founder_ref_reel_04.mp4"
    ]
  },
  "payload": {
    "action_name": "Schedule Batch Social Reels (NEET/JEE)",
    "content_type": "DOCUMENTARY_REEL",
    "avatar_used": "FUTRIX_PERMANENT_AVATAR",
    "video_engine": "GOOGLE_FLOW_OMINI",
    "scheduled_posts": [
      {
        "platform": "Instagram",
        "post_time": "2026-07-31T18:00:00Z",
        "caption": "Why 99% students fail Physics Numerical in NEET! 🧬 #NEET #FUTRIX",
        "media_url": "https://storage.supabase.co/reels/reel_physics_001.mp4"
      }
    ]
  },
  "approval_gate": {
    "founder_telegram_required": true,
    "status": "PENDING"
  }
}
```

---

## 🤝 Key Inter-Executive Interactions

### 1. AI CMO ↔ AI CEO ↔ Founder (Social Reel Pipeline)
1. **Research & Creation**: AI CMO conducts market research on trending educational reel formats in NEET/JEE, drafts video scripts, and generates documentary-style reels using the Founder's locked avatar on Google Flow.
2. **Batch Scheduling Submission**: AI CMO submits the batch of reels and posting schedules to AI CEO via an `APPROVAL_REQUEST` message.
3. **Founder Telegram Gate**: AI CEO forwards the reel batch to the Founder via Telegram Bot.
4. **Automated Scheduling**: Upon receiving Founder `APPROVED` callback, AI CEO signals AI CMO to directly post/schedule the reels on social channels in advance.

### 2. AI CPO ↔ AI CAO ↔ AI CTO (Product & Academic Integration)
- **AI CAO** provides verified question banks.
- **AI CPO** integrates them into the gamified UI.
- **AI CTO** optimizes Supabase database query indices and Edge Function latency.

### 3. AI CFO ↔ All Executives (Zero-Cost Stack Audit)
- **AI CFO** continuously audits rate limits and usage metrics across Gemini API, Supabase, and GitHub Actions to ensure zero cost.
