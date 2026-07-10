---
name: repo-contribution
description: Follow repository contribution guidelines by reading project docs first, matching local conventions, and validating changes before handoff.
---

# Repository contribution guidelines

Use this skill before contributing code, documentation, or automation changes to a repository.

## Read repository guidance first

Before editing files:

- check `CONTRIBUTING.md`, `README.md`, and project docs
- look for PR templates, issue templates, and CODEOWNERS
- inspect build, test, lint, and formatting configuration already present in the repo
- prefer explicit repository rules over general defaults

## Match existing conventions

Contribute in a way that fits the repository:

- follow the existing directory structure and naming style
- use the same language, framework, and testing patterns already in place
- mirror current documentation tone and formatting
- keep changes consistent with the surrounding code rather than introducing a personal style

## Keep changes focused

A good contribution is easy to review.

- solve the requested problem completely
- avoid unrelated refactors unless they are required for correctness
- separate independent concerns into separate commits or pull requests
- document assumptions when repository guidance is incomplete or ambiguous

## Validate the change the repo's way

- run the smallest relevant tests, linters, or build commands that already exist
- do not add new tooling unless the task requires it
- verify docs, config, and code changes from the perspective of a reviewer or maintainer
- capture any known limitations or follow-up work

## Prepare for review

Before opening or updating a PR:

- summarize what changed and why
- note test evidence and any manual verification
- call out breaking changes, migrations, or operational impact
- mention related issues or dependencies
- make sure the final diff is understandable without hidden context

## Respect collaboration norms

- follow branch protection and review requirements
- avoid forceful or destructive actions unless the workflow explicitly allows them
- surface uncertainty early instead of guessing on repository-specific rules
- leave the repo in a cleaner, well-explained state for the next contributor
