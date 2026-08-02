# SOP: End-to-End Automated QA Testing & Continuous Signoff

> **SOP ID**: `SOP-QA-E2E-001`  
> **Status**: Production Standard (v1.0.0)  

---

## 📋 Objective
Automate continuous end-to-end regression testing across all FAIOS modules, validating functional flows, security isolation, and performance latency before any release.

## 🔢 Step-by-Step Procedure
1. **Trigger**: Triggered automatically by GitHub Actions CI pipeline on every push to `main`.
2. **Execute Smoke Tests**: Run headless Chrome browser tests on auth, dashboard, and doubt submission flows.
3. **Execute RLS Audit**: Query Supabase database with student tokens to verify data isolation.
4. **Execute Dual-Solver QA**: Solve sample NEET/JEE questions via independent Gemini API call to verify answer keys.
5. **Generate Quality Scorecard**: Publish test results to `11-Reports/System-Health-Reports/`.
