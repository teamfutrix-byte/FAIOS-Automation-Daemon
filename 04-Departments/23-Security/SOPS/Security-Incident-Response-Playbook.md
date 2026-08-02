# Security Incident Response Playbook

> **SOP ID**: `SOP-SEC-INCIDENT-001`  
> **Status**: Production Standard (v1.0.0)  

---

## 📋 7-Phase Incident Response Playbook

```
1. DETECTION: Alarm triggered via UptimeRobot outage alert or automated Bitwarden secret scanner.
2. CONTAINMENT: Revoke compromised API tokens immediately. Freeze GitHub Actions deployments.
3. INVESTIGATION: `emp_security_analyst` audits immutable logs in Supabase system_approvals.
4. MITIGATION: Rotate secrets in Bitwarden vault. Apply emergency patch to RLS policies.
5. RECOVERY: Restore verified database backup. Un-freeze edge routes on Cloudflare.
6. POST-MORTEM: Document incident root cause in 11-Reports/System-Health-Reports/.
7. LESSONS LEARNED: Update 00-Codex/Security-Privacy-Standard.md to prevent recurrence.
```
