# Founder Telegram Approval Gate Specification

> **Module**: `02-Frameworks/Autonomous-Decision-Engine`  
> **Status**: Production Standard (v1.0.0)  
> **Owner**: AI CEO & FUTRIX Founder  

---

## 📌 Executive Summary

The **Founder Telegram Approval Gate** enforces mandatory human-in-the-loop validation for all AI CEO strategic initiatives, financial allocations, code/schema updates, and category expansion attempts.

No AI Executive can proceed past a critical gate without explicit approval transmitted via Telegram inline buttons from the FUTRIX Founder.

---

## 🔄 Workflow Logic & Payload Protocol

```
+-------------------------------------------------------------------+
| 1. AI CEO Generates Strategic Proposal (JSON)                     |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 2. Post to n8n Webhook Endpoint (/webhook/founder-approval)      |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 3. n8n Dispatches Telegram Message with Inline Buttons           |
|    [ ✅ APPROVE ]    [ ❌ REJECT ]    [ 📝 REQUEST REVISION ]    |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 4. Founder Clicks Button on Telegram Mobile / Desktop App          |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 5. n8n Callback Updates Proposal Status in Supabase Table          |
|    `system_approvals` (status: 'APPROVED' | 'REJECTED')           |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| 6. AI CEO Polls/Receives Callback Event & Resumes / Aborts Action |
+-------------------------------------------------------------------+
```

---

## 📋 JSON Proposal Schema

When triggering the gate, the AI CEO must generate the following standard payload:

```json
{
  "proposal_id": "prop_20260730_neet_mock_series_v1",
  "timestamp": "2026-07-30T21:12:00Z",
  "executive": "AI-CEO",
  "category": "CONTENT_RELEASE",
  "title": "Release NEET UG Physics High-Yield Mock Series 01",
  "impact_summary": "Publishes 180 verified Qs for NEET UG 2027 aspirants. Zero SaaS cost.",
  "risk_assessment": "LOW. Content validated by Academic-Engineering 4-tier auditor.",
  "data_metrics": {
    "pmf_score": 8.7,
    "dau_retention_7d": "74%",
    "zero_cost_compliance": true
  },
  "actions_requested": [
    "Deploy 180 questions to Supabase `questions` table",
    "Publish banner on FUTRIX Mobile Web App"
  ]
}
```

---

## 🔒 Security Requirements

1. **Telegram Chat ID Lock**: The n8n Telegram node strictly filters responses to match the Founder's pre-configured Telegram Chat ID stored securely in Bitwarden / Environment Secrets (`FOUNDER_TELEGRAM_CHAT_ID`).
2. **HMAC Signature**: Webhook payloads are signed using SHA-256 HMAC tokens to prevent spoofing.
