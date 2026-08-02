# Socratic Questioning Tool Specification

> **Skill Name**: `skill_pedagogy_socratic_questioner`  
> **Target Invokers**: `05-AI-Employees/Tutors`  
> **Status**: Production Standard (v1.0.0)  

---

## ⚙️ Function Signature

```typescript
interface SocraticPromptRequest {
  student_query: string;
  subject: "Physics" | "Chemistry" | "Biology" | "Mathematics";
  exam_target: "NEET_UG" | "NEET_PG" | "JEE_MAIN" | "JEE_ADVANCED";
  student_mastery_level: number; // 0.0 - 1.0
  previous_attempts: string[];
}

interface SocraticPromptResponse {
  guiding_question: string;
  underlying_concept_id: string;
  hint_level: 1 | 2 | 3;
}
```

---

## 📜 Execution Logic

1. **Identify Misconception**: Analyze `student_query` against the topic graph in `09-Knowledge`.
2. **Phase 1 (Hint Level 1)**: Ask a fundamental concept question without giving formula numbers.
3. **Phase 2 (Hint Level 2)**: Provide the governing law equation and ask student to identify variables.
4. **Phase 3 (Hint Level 3)**: Show step-by-step substitution and ask student to solve final arithmetic calculation.
