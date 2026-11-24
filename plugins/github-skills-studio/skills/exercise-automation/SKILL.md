---
name: exercise-automation
description: Design and fix the GitHub Actions automation of a GitHub Skills exercise - step triggers that match the learner's action and are safe on the template-copy push, grading checks that prove the right thing, feedback tables with actionable tips, workflow chaining with the skills/exercise-toolkit, least-privilege permissions, and injection-safe scripts. Use when writing or debugging step workflows, choosing a trigger, adding grading, or when Mona does not advance, advances too early, or gives unhelpful feedback.
---

# Exercise automation

Each step workflow watches for one learner action, checks the result when feedback is useful, then posts the
next step. This skill makes that loop reliable, fair, and safe. The structural contract (names, chaining, pins,
permissions) is in the scaffold skill's [framework contract](../exercise-scaffold/references/framework-contract.md);
start from its workflow templates in `../exercise-scaffold/assets/workflows/`.

## Choose the trigger

1. Name the final learner action of the step.
2. Look up its event and filters in [references/triggers.md](references/triggers.md).
3. Prove it cannot fire on the template-copy push (no `push` to `main` without `paths` of a new file; otherwise
   add the initial-commit guard).
4. Keep `workflow_dispatch` for facilitators and tests.
5. Add `concurrency: { group: ${{ github.workflow }}, cancel-in-progress: true }` for steps learners may trigger
   twice quickly.

## Decide on grading

Grade when a wrong result would block later steps or when feedback would help the learner fix it. Otherwise leave
the step ungraded; a stranded learner is worse than an unchecked step. For each check, write down what it proves
and what it does not (assessment validity), then pick a recipe from
[references/grading-patterns.md](references/grading-patterns.md):

| Need | Recipe |
| --- | --- |
| File created | `file-exists` |
| File content | `action-keyphrase-checker` (case-insensitive stems), or a regex for several accepted answers |
| Branch or title | `action-keyphrase-checker` with `text:` input |
| File changed | native `git diff` (no third-party action) |
| Valid config | `json.load` or `yq` |
| Code works | run tests |
| Learner's workflow works | `wait-for-workflow` plus a check that its `conclusion` is `success` |
| Pull request details | `actions/github-script` with the event payload |
| Answer in a comment | `issue_comment` trigger plus a keyphrase check |

Grading job invariants:

- Each check: own step, stable `id`, `continue-on-error: true`, a row in `results_table`.
- The job ends with `if: contains(steps.*.outcome, 'failure')` → `exit 1`.
- `post_next_step_content.needs` includes `check_step_work`.
- `peter-evans/find-comment@v4` uses `comment-author: github-actions[bot]`.
- The grading job never holds `actions: write`.

## Write the feedback

Rows describe expectations in learner language; `tips` give next actions and render only on failure; one clear
status per run. Patterns and the comment lifecycle are in
[references/feedback-messages.md](references/feedback-messages.md).

## Keep it safe

Least-privilege permissions, no untrusted context in `run:` scripts, no `pull_request_target`, tag or SHA pins,
no secrets. Details in [references/workflow-security.md](references/workflow-security.md).

## Debugging "Mona did not respond"

| Observation | Likely cause |
| --- | --- |
| No run in the Actions tab | Trigger mismatch (event, branch, paths), or the step workflow is disabled |
| Run skipped | A job `if:` guard did not match (merged guard, comment guard) |
| Run failed in `find_exercise` | Exercise issue title changed, or another issue title contains `Exercise` |
| Run failed in a comment step | Missing `issues: write`, wrong comment id, or a Nunjucks error in the step file |
| Run failed at `gh workflow enable` | Missing `actions: write`, or the target `Step N` name does not exist |
| Learner advanced despite a failure | `post_next_step_content.needs` is missing `check_step_work` |
| Step ran right after copying | Copy-time push matched the trigger |

Use the walkthrough harness (`exercise-walkthrough-test` skill) to observe runs and comments:
`exercise_harness.py status`, `runs --failed-logs`, and `timeline`.

## Validate

Run `python ../exercise-review/scripts/validate_exercise.py <exercise-root>` (path relative to this skill) after
every workflow change. Fix blocking findings before any live test.
