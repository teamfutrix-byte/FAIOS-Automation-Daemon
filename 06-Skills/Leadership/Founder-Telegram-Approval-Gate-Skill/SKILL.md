# Founder Telegram Approval Gate Skill Specification

---
name: skill_leadership_founder_telegram_gate
description: Atomic leadership skill providing JSON payload formatting, n8n webhook dispatch, and Telegram inline button callback processing for Founder approval.
version: 1.0.0
owner: FUTRIX Founder & AI CEO
category: Leadership
---

## ⚙️ Workflow Logic

```
1. Format JSON proposal payload (proposal_id, category, summary, risk_level, scheduled_time).
2. Trigger n8n Webhook Endpoint (/webhook/founder-approval).
3. n8n sends Telegram inline keyboard [ ✅ APPROVE ] [ ❌ REJECT ].
4. Await Telegram callback payload (`APPROVE:proposal_id`).
5. Return state `APPROVED` or `REJECTED` to calling agent.
```
