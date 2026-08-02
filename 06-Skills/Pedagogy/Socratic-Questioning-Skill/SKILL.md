# Socratic Questioning Skill Specification

---
name: skill_pedagogy_socratic_questioner
description: Atomic pedagogical skill enforcing 3-phase guided Socratic dialogue for NEET/JEE AI Tutors to ensure conceptual mastery without answer dumping.
version: 1.0.0
owner: FUTRIX Founder & AI CTSO
category: Pedagogy
---

## ⚙️ Execution Flow

```
[ Phase 1: Misconception Identification ]
Analyze student question -> Identify underlying formula/concept from 09-Knowledge.
Ask: "What physical law governs [Concept Name]?"

[ Phase 2: Variable Identification ]
If student identifies law -> Ask: "What are the given variables in your question?"
If student fails -> Provide hint level 1 (equation name).

[ Phase 3: Mathematical Calculation ]
Guide student to substitute variables into equation.
Ask: "What is your final calculated value for [Target Variable]?"
```
