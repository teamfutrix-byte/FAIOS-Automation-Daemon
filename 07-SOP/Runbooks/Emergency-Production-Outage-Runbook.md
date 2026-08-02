# Emergency Production Outage Runbook

> **Runbook ID**: `RUNBOOK-OUTAGE-001`  
> **Target Scenarios**: Supabase Outage | Gemini API Rate Limit | n8n Flow Failure | GitHub Actions Build Failure  
> **Status**: Production Executable Runbook (v1.0.0)  

---

## 🚨 Scenario 1: Supabase Free Tier Database Outage / Connection Drop

### 1. Detection
- UptimeRobot monitor emits HTTP 500 alert for `/rest/v1/scheduled_posts`.
- `emp_platform_devops` receives alert notification.

### 2. Impact Analysis
- High. Doubt submissions and social reel queue reads temporarily blocked.

### 3. Immediate Containment Actions
```bash
# Step 1: Check Supabase Status Page API
curl -s https://status.supabase.com/api/v2/status.json

# Step 2: Route Edge Traffic to Cached Cloudflare Cache
n8n execute --workflow-id "n8n-cloudflare-edge-cache-fallback"
```

### 4. Temporary Mitigation
- Enable read-only memory cache on Cloudflare Free Worker, serving cached flashcard Q-Bank items.

### 5. Recovery & Validation
- Once Supabase restores connection, verify Postgres DB queries return HTTP 200 OK.
- Run RLS isolation audit test: `npm run test:rls-audit`.

---

## 🚨 Scenario 2: Gemini API Rate Limit Exceeded (HTTP 429)

### 1. Detection
- Socratic AI Tutor returns HTTP 429 (`ResourceExhausted`) error payload.

### 2. Immediate Containment Actions
- Automatically switch prompt completion payload to fallback model (`Gemini 1.5 Flash` cached route).
- Trigger prompt caching header optimization (`06-Skills/Pedagogy/Socratic-Questioning-Skill`).
