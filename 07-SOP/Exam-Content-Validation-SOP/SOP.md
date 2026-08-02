# Standard Operating Procedure: Exam Content Validation (4-Tier QA)

---
sop_id: SOP-ACAD-QA-001
name: Exam Content Validation
version: 1.0.0
owner: emp_qbank_auditor, AI CAO
trigger: Question Bank Generation Event
---

## 📋 Procedure Steps
1. **Tier 1 (Draft Generation)**: Content Creator Agent drafts question, 4 choices, answer key, and working.
2. **Tier 2 (Syllabus Mapping)**: Map topic tag against `09-Knowledge/NEET-UG-Syllabus-Matrix.md`.
3. **Tier 3 (Dual-Solver Audit)**: Independent Gemini Solver resolves problem. Verify solution matches answer key with 0% error.
4. **Tier 4 (Founder Approval Gate)**: Submit verified batch to AI CEO -> Founder Telegram Bot before publishing to Supabase live database.
