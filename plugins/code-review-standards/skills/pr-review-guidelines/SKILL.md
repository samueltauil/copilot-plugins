---
name: "pr-review-guidelines"
description: "General PR review guidelines and conventions"
version: "1.0.0"
---
# PR review guidelines and conventions

Use this skill when reviewing pull requests, drafting review comments, or suggesting incremental improvements.

## Pull Request Review Guidelines

### Scope of recommendations
- **Limit recommendations to code modified in this PR** unless severe security vulnerabilities or critical bugs are detected in adjacent code.
- Do not suggest changes to files outside the PR's diff unless they are directly impacted by the changes.
- If legacy code quality concerns arise, flag them as informational notes but **do not propose full rewrites**.

### Incremental improvements over large refactors
- Prefer **incremental, low-risk improvements** over large-scale refactors.
- Avoid suggesting architectural changes unless the PR explicitly requests them.
- When proposing alternatives, ensure they:
  - Align with existing project patterns and conventions
  - Are low-risk and well-contained
  - Do not introduce unnecessary complexity

### Feedback style
- Be concise and actionable in review comments.
- Prioritize issues by severity: security > bugs > performance > style.
- Provide clear reasoning for each suggestion.
- When flagging potential issues, distinguish between:
  - **Must fix**: Security vulnerabilities, bugs, breaking changes
  - **Should fix**: Performance issues, maintainability concerns
  - **Consider**: Style improvements, minor optimizations

## Code suggestion guidelines

### General principles
- Follow existing code patterns and conventions already established in the repository.
- Prefer readability and maintainability over clever one-liners.
- Suggest type-safe solutions when applicable.
- Respect the project's established architecture and design decisions.

### What to avoid
- Do not suggest breaking changes without explicit warning.
- Avoid introducing new dependencies unless absolutely necessary.
- Do not recommend deprecated APIs or patterns.
- Avoid over-engineering simple solutions.

## PR best practices for contributors

### Keep PRs small and focused
- Smaller PRs lead to more relevant and contained Copilot feedback.
- Large PRs expand Copilot's context window, which may result in broader and less relevant suggestions.
- Aim for PRs that address a single concern or feature.

### Local review before opening a PR
- Run Copilot review locally before opening the PR to:
  - Stabilize feedback and address common issues early
  - Reduce unexpected findings during formal review
  - Improve overall PR quality before human review

### Model selection for reviews
- **Faster models** are suitable for lightweight suggestions, syntax checks, and quick iterations.
- **Reasoning-optimized models** are better for deeper structural analysis, complex logic review, and architectural considerations.
- Choose the appropriate model based on the PR's complexity and review needs.

## Human judgment integration

### Copilot's role
- Copilot provides **comment-only feedback** and will never block a merge.
- Its purpose is to **augment reviewer efficiency**, not override human decisions.
- Treat Copilot suggestions as a starting point for discussion, not a final verdict.

### When to override Copilot
- When business context or domain knowledge contradicts the suggestion.
- When project-specific constraints make a suggestion impractical.
- When the suggestion conflicts with established team conventions.
- When performance or security trade-offs require human judgment.

## Repository-specific review reminders

### Commit messages
- Follow conventional commit format when applicable.
- Keep commit messages clear and descriptive.

### Documentation
- Update relevant documentation when code changes affect public APIs or user-facing behavior.
- Keep README and inline comments up to date.

### Testing
- Suggest tests for new functionality when appropriate.
- Do not suggest removing existing tests unless they are clearly obsolete or incorrect.

## Summary

| Principle | Guideline |
|-----------|-----------|
| Scope | Limit to modified code unless critical issues are found |
| Refactoring | Prefer incremental improvements |
| Alternatives | Only if low-risk and pattern-aligned |
| Legacy code | Flag concerns, don't propose rewrites |
| PR size | Smaller is better for focused feedback |
| Human judgment | Copilot augments, humans decide |
