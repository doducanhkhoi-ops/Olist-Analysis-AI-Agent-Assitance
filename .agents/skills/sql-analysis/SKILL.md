---
name: sql-analysis
description: Plan and write SQL analysis for product, business, cohort, funnel, retention, revenue, and operations questions with explicit joins, grain, QA checks, and reproducibility notes.
version: 0.1.0
---

# SQL Analysis

Use this skill when the user needs a reliable query plan or SQL draft.

## Workflow

1. Identify question, source tables, join keys, grain, filters, and output shape.
2. Write SQL in stages: base population, events/facts, aggregation, QA, final.
3. Add row-count, null, duplicate, and join-multiplication checks.
4. Explain assumptions and expected result columns.

## Output

Return `Query plan`, `SQL`, `QA queries`, `Assumptions`, and `Interpretation
guide`.

