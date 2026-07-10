---
name: git-commit
description: Generate standardized conventional commit messages, stage related changes cleanly, and record meaningful history.
---

# Standardized git commits

Use this skill when preparing a commit or helping someone write a commit message.

## Stage changes intentionally

Before writing a commit message:

- review the diff and understand the purpose of the change
- stage only files that belong to the same logical unit of work
- split unrelated edits into separate commits
- avoid mixing refactors, formatting noise, and feature work unless they are inseparable

A strong commit starts with a coherent change set.

## Use conventional commit format

Format commits as:

```text
<type>(<scope>): <short summary>
```

Examples:

```text
feat(auth): add device code login flow
fix(api): handle null status from webhook payload
docs(readme): clarify plugin installation steps
```

## Choose the right type

Use the type that best reflects the intent of the change:

- `feat`: new user-facing functionality
- `fix`: bug fix or regression correction
- `docs`: documentation only
- `refactor`: code restructuring without behavior change
- `test`: added or updated tests
- `chore`: maintenance or housekeeping
- `build`: build system or dependency changes
- `ci`: CI/CD workflow updates
- `perf`: measurable performance improvements
- `style`: formatting-only changes
- `revert`: revert of a previous commit

## Pick a meaningful scope

Scope is optional, but recommended when the repository has multiple components.

- use the primary module, package, feature area, or directory name
- keep it short and recognizable
- avoid overly broad scopes like `misc` or `stuff`
- omit scope only when the change is truly repository-wide and a scope would mislead

## Write the summary line well

The summary should be:

- imperative (`add`, `fix`, `update`, not `added` or `fixes`)
- concise, typically under 72 characters
- specific about the observable change
- free of trailing punctuation

Prefer describing the outcome, not the implementation detail.

## Add body and footers when helpful

Include a body when context is important:

- explain why the change was needed
- summarize the main approach
- call out risk, migration, or rollout considerations

Use footers when relevant:

```text
Closes #123
Refs #456
```

## Handle breaking changes explicitly

For breaking changes:

- add `!` after the type or scope, for example `feat(api)!: remove v1 endpoints`
- include a `BREAKING CHANGE:` footer describing the impact and migration path

Example:

```text
feat(config)!: rename plugin registry setting

BREAKING CHANGE: `marketplaceUrl` is now `marketplaceSource`.
```

## Final quality check

Before committing, verify that:

- the staged diff matches the message
- the message reflects user-visible intent
- issue references are correct
- the change is small enough to review comfortably
