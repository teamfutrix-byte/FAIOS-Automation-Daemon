# FAIOS Contribution Protocol

Welcome to the **FUTRIX AI Operating System (FAIOS)** contribution guide. This document applies to both **Human Engineers** and **Autonomous AI Agents** modifying or extending FAIOS.

---

## 🤖 Rules for AI Agents & Subagents

1. **Inspect Module README First**: Before editing any module, read its dedicated `README.md` to understand scope, ownership, dependencies, and forbidden contents.
2. **Zero Placeholder Policy**: Never output `TODO`, `FIXME`, dummy json, or fake schemas. Every addition must be complete and production-ready.
3. **Changelog Integrity**: Any modification to a module MUST be recorded in that module's `CHANGELOG.md` adhering to Semantic Versioning.
4. **Preserve Naming Standard**: All filenames must use `Kebab-Case.md` or `CamelCase.json`. No spaces or ambiguous titles allowed.
5. **Founder Approval Required**: Any change altering executive prompts (`03-Executives`), core frameworks (`02-Frameworks`), or database schema triggers an n8n Telegram notification to the FUTRIX Founder.

---

## 👨‍💻 Rules for Human Engineers

1. Create feature branches following `feature/module-name` pattern.
2. Run standard verification scripts before submitting Pull Requests to `main`.
3. Ensure all environment secrets remain stored strictly in Bitwarden / Supabase Vault / GitHub Secrets. Never commit plain-text API keys or credentials.
