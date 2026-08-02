# Supreme Security & Data Privacy Standard

> **Document Type**: Core System Security & Privacy Law  
> **Enforcement**: Mandatory for all AI Executives, Departments, AI Employees & Systems  
> **Status**: Production Standard (v1.0.0)  

---

## 🔒 Section I: Zero-Trust & Least Privilege Mandate

### Clause 1.1 — Zero-Trust Architecture
No system user, AI agent, edge function, or internal script is granted inherent trust. Every API request, database query, and automated workflow must authenticate using cryptographically signed tokens or verified session IDs.

### Clause 1.2 — Secrets Vault Mandate (Bitwarden / Supabase Secrets)
1. **Zero Hardcoded Credentials**: No API key, database password, secret token, or private URL may be committed to git tracking or hardcoded in prompts.
2. **Bitwarden Vault Enforcement**: All production secrets are managed via encrypted Bitwarden vaults or Supabase Vault environment variables (`$env.KEY`).
3. **Automated Secret Scanning**: GitHub Actions workflows continuously scan commits for credential patterns. Any push containing un-encrypted secrets triggers an immediate repository freeze.

---

## 🛡 Section II: Student Data Sovereignty & DPDP Compliance

### Clause 2.1 — Student Data Ownership
Students maintain 100% legal ownership over their personal data, performance logs, and study records. Neither FUTRIX nor the AI CEO holds ownership rights over student personal data.

### Clause 2.2 — Student Data Rights API
Students possess immediate rights to:
1. **View & Export Data**: Download a complete JSON archive of study trajectories via `/api/user/export-data`.
2. **Delete Data**: Trigger permanent, un-recoverable deletion of all personal records via `/api/user/delete-data`.
3. **Consent Transparency**: Zero third-party data sales, zero unauthorized data sharing.
