# 6-Tier Data Classification & Encryption Specification

> **Document Type**: Data Security & Storage Standard  
> **Status**: Production Standard (v1.0.0)  

---

## 🔒 Data Tier Classification Matrix

| Tier Level | Class Name | Examples | Encryption at Rest | Access Control |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Public** | Marketing reels, blog posts, public syllabus matrices | None | Read: Public, Write: CMO |
| **Tier 2** | **Internal** | System SOPs, department roadmaps, KPI dictionaries | AES-256 | System-Wide AI Agents |
| **Tier 3** | **Confidential** | Competitor war room, financial runway audits | AES-256 | AI CEO, CFO, Founder |
| **Tier 4** | **Restricted** | Student performance vectors, doubt history | AES-256 (pgvector) | Student Only + RLS |
| **Tier 5** | **Highly Sensitive**| Student PII, telephone hashes, email addresses | AES-256 + Hash | Restricted RLS Policy |
| **Tier 6** | **Secrets** | Bitwarden keys, Gemini API tokens, Supabase Service Key | Encrypted Vault | Bitwarden / Founder |
