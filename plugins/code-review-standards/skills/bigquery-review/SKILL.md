---
name: "bigquery-review"
description: "BigQuery SQL and Dataform review standards"
version: "1.0.0"
---
# BigQuery SQL and Dataform review standards

Use this skill when reviewing pull requests that change BigQuery SQL, Dataform `.sqlx` models, or related data-pipeline code.

## Review focus areas

1. **Data quality risks**
   - Missing `NULL` checks
   - Unbounded date ranges
   - Implicit type conversions
2. **BigQuery anti-patterns**
   - `SELECT *`
   - Missing partition filters
   - Cross joins on large tables
3. **Window function correctness**
   - Verify `PARTITION BY` clauses match the intended grouping
   - Verify `ORDER BY` clauses match the intended sequencing and determinism
4. **Breaking changes**
   - Schema changes that could break downstream views, reports, or dashboards
5. **Dataform config quality**
   - Ensure `config {}` blocks use the correct type, schema, and assertions
6. **Date filter consistency**
   - Ensure queries use consistent date boundaries
   - Check shared constants such as `includes/constants.js` when present

## How to apply these standards

- Prioritize correctness and data safety over minor style issues.
- Treat partitioning, filtering, and join shape as first-class review concerns for cost and performance.
- Call out ambiguous window definitions when business logic depends on row order or deduplication.
- Flag schema changes early when they can cascade into downstream failures.
