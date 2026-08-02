# Master KPI Dictionary & Telemetry Specification

> **Document Type**: System-Wide Metric Standard  
> **Status**: Production Standard (v1.0.0)  

---

## 📊 Business & Infrastructure Metrics

| Metric Name | Category | Calculation Formula | Source | Target Standard |
| :--- | :--- | :--- | :--- | :--- |
| **Zero-Cost Compliance** | Finance | $\text{Paid SaaS Spend} = \$0.00$ | Supabase / Bitwarden | 100% Zero Paid SaaS |
| **D1 Student Retention** | Product | $\frac{\text{Active Students Day 1}}{\text{New Students Day 0}} \times 100$ | Supabase `student_mastery_vectors` | $\ge 80\%$ |
| **D7 Student Retention** | Product | $\frac{\text{Active Students Day 7}}{\text{New Students Day 0}} \times 100$ | Supabase Telemetry | $\ge 65\%$ |
| **Doubt SLA Resolution** | Student Success | $\text{Timestamp}_{\text{Response}} - \text{Timestamp}_{\text{Submission}}$ | Supabase Doubt Queue | $< 60$ Seconds |
| **Mute-Test Pass Rate** | Marketing | $\frac{\text{Visual Comprehension Audits Passed}}{\text{Total Video Reels Rendered}} \times 100$ | Google Flow QA Auditor | 100% |
| **Advance Schedule Buffer**| Marketing | $\text{Pre-Scheduled Post Queue Buffer (Days)}$ | Supabase `scheduled_posts` | $\ge 7$ Days |
| **PMF Category Score** | Strategy | Weighted Score (Retention, DAU, Doubt Satisfaction) | PMF Evaluator Framework | $\ge 8.5 / 10.0$ |
| **System Uptime** | Infrastructure | $\frac{\text{Total Operational Minutes}}{\text{Total Minutes}} \times 100$ | UptimeRobot Monitor | $\ge 99.9\%$ |
