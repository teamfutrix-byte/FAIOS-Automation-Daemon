# 08-Automation — Executable Workflows & Autonomous Orchestration Engine

## 📌 Purpose
The `08-Automation` module is the operational engine of FUTRIX. It converts all FAIOS blueprints, Executive directives, Department workflows, Employee skills, and SOPs into runnable n8n flow JSONs, GitHub Actions CI/CD pipelines, Supabase Postgres SQL migrations, and self-healing error recovery protocols.

## 👤 Owner & Scope
- **Owner**: AI CTO & Platform DevOps (`04-Departments/14-AI-Engineering`, `04-Departments/24-Infrastructure`)
- **Scope**: Enterprise-wide orchestration enforcing a **95% AI Automation / 5% Founder Approval** model.

## 🔗 Dependencies
- **Upstream Dependencies**: `00-Codex`, `01-Blueprint`, `02-Frameworks`, `03-Executives`, `04-Departments`, `05-AI-Employees`, `06-Skills`, `07-SOP`.
- **Downstream Dependencies**: Production Infrastructure (Supabase, Cloudflare, GitHub, Telegram).

## 📁 Executable Automation Roster

| Automation Artifact | Type | Primary Target | Value Delivered |
| :--- | :--- | :--- | :--- |
| [Universal-AI-Communication-Bus.md](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/Universal-AI-Communication-Bus.md) | Protocol Spec | Cross-Agent Bus | Universal JSON messaging bus for all 15 Executives & 26 Employees |
| [Self-Healing-Error-Recovery-Engine.md](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/Self-Healing-Error-Recovery-Engine.md) | Recovery Engine | System Errors | Automated 6-step failure detection, research, retry & incident report engine |
| [Founder-Dashboard-Telemetry.md](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/Founder-Dashboard-Telemetry.md) | Telemetry Spec | Founder Dashboard | Multi-source metric tracking (UptimeRobot, DAU, Gemini API token burn) |
| [n8n-Workflows/Founder-Telegram-Approval-Workflow.json](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/n8n-Workflows/Founder-Telegram-Approval-Workflow.json) | Executable n8n JSON | Telegram Bot | Single-click Founder Telegram approval & callback handling |
| [n8n-Workflows/Google-Flow-Reel-Social-Scheduler.json](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/n8n-Workflows/Google-Flow-Reel-Social-Scheduler.json) | Executable n8n JSON | Google Flow / IG Reels | Educational reel rendering (Google Flow) & 7-day advance post scheduling |
| [n8n-Workflows/Doubt-Resolution-SLA-Router.json](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/n8n-Workflows/Doubt-Resolution-SLA-Router.json) | Executable n8n JSON | Supabase Realtime | Real-time doubt queue listener invoking Socratic AI Tutors (<60s SLA) |
| [GitHub-Actions/faios-ci-cd-pipeline.yml](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/GitHub-Actions/faios-ci-cd-pipeline.yml) | Executable YAML | GitHub Actions | CI/CD pipeline for repository linting, SQL DDL checks & Edge Function deploys |
| [Supabase-Functions/ddl-schema-migrations.sql](file:///c:/Users/L470/Desktop/Futrix/FAIOS/08-Automation/Supabase-Functions/ddl-schema-migrations.sql) | Executable SQL | Supabase Postgres | Production Postgres DDL, Row-Level Security, Triggers & Vector Memory Views |
