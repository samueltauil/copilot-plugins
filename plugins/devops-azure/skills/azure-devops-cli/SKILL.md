---
name: Azure DevOps CLI operations
description: Use this skill when you need practical `az devops` workflows for pipelines, repos, boards, artifacts, and project automation.
---

# Azure DevOps CLI operations

## Use this skill when
- You need repeatable command-line operations for Azure DevOps organizations and projects.
- A task involves pipelines, repos, pull requests, boards, or artifacts.
- You want automation-friendly guidance instead of clicking through the web UI.

## Initial setup
1. Ensure the Azure CLI and the Azure DevOps extension are installed.
2. Configure defaults with `az devops configure --defaults organization=<org-url> project=<project>`.
3. Authenticate with a PAT or an existing signed-in context and verify access before scripting.
4. Decide whether the commands must be idempotent for CI or one-off for local operations.

## Pipelines
- Use pipeline list and show commands to inventory definitions and check their IDs.
- Queue runs with explicit branch and variable overrides when validating a change.
- Query recent runs, results, and logs before retrying a failing pipeline.
- Update variables, service connections, and agent pool assumptions carefully because they affect downstream jobs.

## Repos and pull requests
- Script repository creation, default branch policies, and PR automation through CLI commands when supported.
- Check PR status, reviewers, completion options, and linked work items before merging.
- Use repo and PR queries to verify branch naming, merge strategy, and policy compliance.
- Prefer machine-readable output formats such as JSON or table depending on whether a script or human is consuming the result.

## Boards and work items
- Create, update, and query work items with explicit field names rather than ambiguous display labels.
- Link parent-child, related, or pull-request relationships when automating flow across teams.
- Filter boards data by area path, iteration, state, or assigned user to keep queries targeted.
- Validate required fields and allowed values before bulk updates.

## Artifacts and package feeds
- Verify feed names, views, and permissions before publishing or downloading packages.
- Use universal packages or the ecosystem-native publishing command as appropriate.
- Record package versioning rules so automation never overwrites immutable releases.
- Confirm retention policies and cleanup expectations for large feeds.

## Scripting practices
- Use `--output json` and JMESPath queries for stable automation.
- Check exit codes and null results instead of assuming every entity exists.
- Rate-limit or batch large mutations to avoid partial success in long scripts.
- Log organization, project, and entity IDs so troubleshooting is straightforward.

## Troubleshooting checklist
- Re-check default organization and project when commands target the wrong tenant.
- Confirm the PAT scopes or user permissions cover the requested action.
- Inspect preview features, unsupported operations, or REST gaps if the CLI command is missing behavior.
- Fall back to `az rest` only when the CLI extension does not expose the required capability.

## Deliverable format
- State the target org, project, and entity types involved.
- Provide the exact CLI commands or script shape to use.
- Note prerequisites, permissions, and failure modes.
- End with validation commands that prove the operation succeeded.
