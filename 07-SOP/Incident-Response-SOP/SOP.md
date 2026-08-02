# Standard Operating Procedure: Incident Response & Downtime Mitigation

---
sop_id: SOP-INFRA-INCIDENT-001
name: Incident Response & Downtime Mitigation
version: 1.0.0
owner: emp_infra_monitor, emp_security_analyst, AI CTO
trigger: UptimeRobot Outage Alert / Security Vulnerability Detection
---

## 📋 Incident Triage Steps
1. **Detection**: UptimeRobot detects endpoint failure (>500ms latency or 5xx HTTP error).
2. **Immediate Alert**: n8n triggers high-priority alert to Founder Telegram Bot.
3. **Automated Failover**: Cloudflare Page Rules reroute traffic to backup Edge Worker page.
4. **Root Cause Audit**: `emp_infra_monitor` inspects Supabase database logs and Gemini API rate limits.
5. **Recovery**: Restore endpoint health, log incident report in `11-Reports/System-Health-Reports/`.
