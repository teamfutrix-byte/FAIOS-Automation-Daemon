# Universal AI Agent Communication Bus Standard

> **Document Type**: Cross-Agent Communication Architecture  
> **Status**: Production Standard (v1.0.0)  

---

## 📌 Protocol Overview

The **Universal AI Communication Bus** defines the standard JSON envelope used by all 15 AI Executives and 26 AI Employees to exchange tasks, submit approval requests, transfer student doubt contexts, and return telemetry metrics.

---

## 📄 JSON Communication Envelope Schema

```json
{
  "$schema": "https://futrix.ai/schemas/universal_agent_msg.v1.json",
  "header": {
    "message_id": "msg_20260730_ceo_cto_001",
    "timestamp": "2026-07-30T22:00:00Z",
    "sender": {
      "agent_id": "AI-CEO",
      "role": "Chief Executive Officer",
      "department": "03-Executives"
    },
    "recipient": {
      "agent_id": "AI-CTO",
      "role": "Chief Technology Officer",
      "department": "03-Executives"
    },
    "priority": "HIGH",
    "intent": "TASK_ASSIGNMENT"
  },
  "task": {
    "title": "Optimize Supabase Vector Index Query Latency",
    "description": "Tune ivfflat index parameters on student_mastery_vectors to reduce p99 search latency below 100ms.",
    "deadline": "2026-07-31T23:59:59Z",
    "required_skills": [
      "06-Skills/Engineering/Supabase-DDL-Builder-Skill"
    ],
    "sop_reference": "07-SOP/Supabase-Schema-Migration-SOP"
  },
  "approval_requirements": {
    "founder_telegram_approval": false,
    "ceo_approval": true
  },
  "status": "PENDING"
}
```
