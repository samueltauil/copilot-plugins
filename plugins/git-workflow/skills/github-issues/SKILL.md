---
name: github-issues
description: Create, triage, and maintain GitHub issues with clear problem statements, actionable scope, and strong lifecycle hygiene.
---

# GitHub issue management

Use this skill when creating, refining, or organizing work in GitHub issues.

## Start with the right issue type

Decide whether the issue is primarily:

- a bug report
- a feature request
- a task or engineering chore
- a documentation or process improvement

Choose a title that makes the problem obvious without requiring the reader to open the issue.

## Write a useful issue body

A good issue usually contains:

- context: what is happening and why it matters
- current behavior or problem statement
- expected behavior or desired outcome
- reproduction steps for bugs
- acceptance criteria for features or tasks
- links to related issues, PRs, docs, or incidents

If the work is large, break it into smaller issues and connect them with references.

## Triage deliberately

During triage:

- search for duplicates before creating a new issue
- assign labels for type, priority, area, or team ownership
- add assignees or leave unassigned intentionally
- place the issue in a milestone or project when the repo uses them
- identify blockers, dependencies, and follow-up tasks

## Make issues actionable

Prefer issues that a contributor can pick up without extra clarification.

- state clear success criteria
- note constraints, risks, or non-goals
- include sample inputs, screenshots, logs, or stack traces when relevant
- avoid vague requests like "improve this" without measurable direction

## Keep issue lifecycle clean

As work progresses:

- update the issue when scope changes
- link the implementing PR
- comment with decisions that future readers need
- close the issue with a short explanation of the resolution
- reopen only when new evidence shows the original problem still exists

## Common GitHub CLI support

Helpful commands include:

```bash
gh issue list
gh issue create
gh issue edit <number>
gh issue comment <number> --body "..."
gh issue close <number>
```
