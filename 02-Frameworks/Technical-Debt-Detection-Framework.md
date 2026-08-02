# Technical Debt Detection & Refactoring Framework

> **Document Type**: Code & Documentation Refactoring Engine  
> **Status**: Production Standard (v1.0.0)  

---

## 🔍 Continuous Technical Debt Audit Categories

1. **Logic Duplication Scanner**: Detects duplicated prompt logic across AI Tutors or Executives and refactors them into reusable atomic skills in `06-Skills`.
2. **Stale Documentation & Broken Link Audit**: GitHub Actions workflow verifies zero broken markdown relative links across all 13 FAIOS root modules.
3. **Deprecated SOP Scanner**: Flags SOPs un-updated for over 180 days and generates automated refactoring proposals.
4. **Unused Automation Flow Audit**: Monitors n8n execution logs to prune dead webhooks or un-triggered cron workflows.
