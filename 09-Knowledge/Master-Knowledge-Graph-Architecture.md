# Master Knowledge Graph Architecture

> **Document Type**: Connected Knowledge Graph Topology  
> **Status**: Production Standard (v1.0.0)  

---

## 📌 Graph Topology & Connection Nodes

FAIOS eliminates isolated data silos by interconnecting all student activities, pedagogical responses, content assets, executive decisions, and revenue drivers into a single living graph.

```
+------------------+       +------------------+       +------------------+
| Student Practice | ----> | Socratic AI Tutor| ----> | Telemetry Log    |
| (NEET / JEE Qs)  |       | (Physics / Math) |       | (Supabase Postgres)
+------------------+       +------------------+       +------------------+
         |                                                     |
         v                                                     v
+------------------+       +------------------+       +------------------+
| Memory Lab Engine| ----> | Spaced Repetition| ----> | Student Mastery  |
| (Flashcards)     |       | (SuperMemo-2 Math|       | Vector (pgvector)|
+------------------+       +------------------+       +------------------+
         |                                                     |
         v                                                     v
+------------------+       +------------------+       +------------------+
| Daily Streaks    | ----> | Retention Engine | ----> | Founder Telegram |
| & XP Mechanics   |       | (D1, D7 Metrics) |       | Approval Gate    |
+------------------+       +------------------+       +------------------+
```

---

## 🔗 Node Definitions & Data Contracts

1. **Student Practice Node**: Captures real-time question attempts, topic ID, response time, and selected answer choice.
2. **Socratic AI Tutor Node**: Invokes `06-Skills/Pedagogy/Socratic-Questioning-Skill` to guide student without dumping raw answers.
3. **Student Mastery Vector Node**: Updates `student_mastery_vectors` table in Supabase via `pgvector` embeddings.
4. **Retention Engine Node**: Aggregates D1/D7/D30 active usage and triggers n8n Telegram approval requests for new feature releases when retention targets are met.
