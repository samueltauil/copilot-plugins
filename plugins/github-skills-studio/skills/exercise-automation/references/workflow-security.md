# Workflow security for exercises

Exercises are templates thousands of people copy, and their workflows are read as examples. Model good practice.
Based on GitHub's [security hardening for GitHub Actions](https://docs.github.com/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions).

## Least privilege

- `permissions: {}` at the workflow level, then per-job grants (see the framework contract's permissions matrix).
- Grading jobs: `contents: read`, `issues: write`, and only what a check needs (`pull-requests: read`,
  `actions: read`). Never `actions: write`: a learner-triggered job must not enable or disable workflows.
- Never `permissions: write-all`.

## Script injection

Titles, bodies, comments, branch names, and commit messages are attacker-controllable. Never interpolate them
into `run:` or `actions/github-script` code:

```yaml
# Unsafe
- run: echo "${{ github.event.comment.body }}"

# Safe: pass through the environment
- env:
    BODY: ${{ github.event.comment.body }}
  run: printf '%s\n' "$BODY"
```

Passing them as `with:` inputs to an action (such as `action-keyphrase-checker`) is safe. The validator flags
interpolation of known untrusted contexts in scripts.

## Triggers

- Never use `pull_request_target` for grading; it runs with base-repository privileges and secrets.
- Do not rely on events Mona creates with `GITHUB_TOKEN` to start the next step: they do not start workflows,
  except `workflow_dispatch`, `repository_dispatch`, and pull requests opened or updated by a workflow, whose runs
  wait for approval.
- Guard `issue_comment` triggers to the intended issue type.

## Comments

- Find Mona's comment with `comment-author: github-actions[bot]` before `edit-mode: replace`, so a learner's comment
  is never overwritten.
- Grading jobs edit one comment; they do not create new ones.

## Dependencies

- Pin every action to a release tag or a full commit SHA; never a branch.
- Prefer first-party (`actions/*`) and GitHub Skills (`skills/*`) actions. Third-party actions are code you run
  with your token.
- `tj-actions/changed-files` was compromised in March 2025 (CVE-2025-30066). Prefer native `git diff`, or pin a
  reviewed full commit SHA.
- Public exercises use tag pins so the GitHub Skills EMU allowlist (which lists tags) keeps working. Private or
  internal workshops can pin SHAs and allowlist them.

## Secrets and data

- Exercises should not need secrets beyond `GITHUB_TOKEN`.
- Never ask learners to paste tokens, passwords, or workplace data into issues, comments, or files.
- Never print tokens; do not `set -x` in steps that handle them.

## Running learner code

Grading that runs tests executes code the learner wrote or Copilot generated. Keep that job's token minimal and
do not expose secrets to it.

## Template repository hygiene

- Mark the source repository as a template before enabling `push` triggers in Step 0.
- Keep all step workflows disabled in the source repository.
- Disable Dependabot and Copilot Autofix on the template to avoid noise (exercise-creator repository settings
  checklist).
