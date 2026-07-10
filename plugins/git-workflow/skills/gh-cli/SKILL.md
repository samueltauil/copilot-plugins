---
name: gh-cli
description: Use GitHub CLI effectively for repository operations, pull requests, issues, and automation-friendly GitHub workflows.
---

# GitHub CLI workflows

Use this skill when working with GitHub from the terminal through `gh`.

## Establish context first

Before taking action:

- confirm authentication with `gh auth status`
- confirm the repository context with `gh repo view` or `gh repo set-default`
- check the current branch before opening or updating pull requests
- prefer repo-local commands over manually pasting long URLs

## Common issue workflows

Typical issue operations include:

```bash
gh issue list
gh issue view 123
gh issue create
gh issue comment 123 --body "..."
gh issue edit 123 --add-label bug
```

When creating or editing issues:

- use a clear title and concrete description
- apply labels, assignees, and milestones when available
- search first to avoid duplicates

## Common pull request workflows

Typical PR operations include:

```bash
gh pr status
gh pr create
gh pr view --web
gh pr checkout 456
gh pr review 456 --approve
gh pr merge 456 --squash
```

When working with PRs:

- make sure the branch is pushed and up to date
- write a PR title and body that summarize why the change matters
- include test evidence, screenshots, or rollout notes when relevant
- review the diff before approving or merging

## Prefer structured output for automation

When another tool or script needs the result:

- use `--json` for machine-readable output
- use `--jq` to filter fields when helpful
- use `gh api` when high-level commands do not expose the needed data

Examples:

```bash
gh pr list --json number,title,headRefName
gh api repos/{owner}/{repo}/labels
```

## Use safe, intentional operations

- verify the target repo, branch, PR, or issue before mutating it
- be careful with close, reopen, edit, delete, and merge operations
- prefer explicit flags over interactive prompts in automated flows
- document follow-up actions when a command changes shared project state

## Recommended workflow patterns

- use `gh issue create` to capture work before coding when the team tracks work in issues
- use `gh pr create --fill` only after verifying the generated title/body
- use `gh pr checks` or status views before merge
- use `gh run list` and `gh run view` to inspect CI when a PR is blocked
