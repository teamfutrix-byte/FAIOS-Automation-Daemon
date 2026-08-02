# Standard Operating Procedure: Exam Content Validation

> **SOP ID**: `SOP-ACAD-001`  
> **Target Audience**: AI Content Creators, Quality Auditors & Academic Leads  
> **Status**: Production Standard (v1.0.0)  

---

## 📋 Objective
Ensure zero mathematical errors, zero incorrect answer keys, zero ambiguous questions, and 100% syllabus alignment for all NEET UG/PG and JEE Main/Advanced mock questions published on FUTRIX.

---

## 🔢 Step-by-Step Procedure

### Step 1: Draft Generation
- AI Content Creator generates question, 4 multiple choice options, single correct key, and detailed solution explanation.

### Step 2: Syllabus & Topic Mapping
- Verify question against `09-Knowledge` syllabus matrices. Tag exact topic ID (e.g. `NEET_PHY_MECH_LAWS_OF_MOTION_004`).

### Step 3: Dual-LLM Verification & Solvability Audit
- Pass question and solution through Quality Auditor LLM model. Verify:
  - Option uniqueness (no duplicate answer options).
  - Mathematical correctness of step-by-step working.
  - Absence of ambiguous physical assumptions.

### Step 4: Founder Telegram Approval Gate Dispatch
- Compile batch JSON of verified questions and post to n8n webhook.
- Await Founder Telegram `APPROVED` signal before releasing batch into production Supabase Postgres database.
