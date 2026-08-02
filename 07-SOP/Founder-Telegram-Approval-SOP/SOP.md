# Standard Operating Procedure: Founder Telegram Approval Intercept

---
sop_id: SOP-GOV-TELEGRAM-001
name: Founder Telegram Approval Intercept
version: 1.0.0
owner: AI CEO & FUTRIX Founder
trigger: Executive Proposal Event (Category Expansion, Reel Post, Schema Change, Capital Spend)
---

## 📋 Procedure Steps
1. **Payload Assembly**: Executive formats standard JSON payload (`proposal_id`, `executive`, `category`, `summary`, `risk_level`, `scheduled_time`).
2. **n8n Webhook Dispatch**: Post payload to `/webhook/founder-approval`.
3. **Telegram Message Delivery**: n8n Telegram node sends message to Founder with inline buttons `[ ✅ APPROVE ]` and `[ ❌ REJECT ]`.
4. **Founder Interaction**: Founder taps button on mobile/desktop app.
5. **Callback Handling**: n8n receives callback payload (`APPROVE:proposal_id`). Updates Supabase `system_approvals` table.
6. **Execution Unblock**: Calling AI Executive receives `APPROVED` token and executes task.
