# Triggers: from learner action to workflow event

Pick the event that the step's final learner action produces, then add filters so nothing else (especially the
template-copy push) can fire it. See also the
[exercise-creator transition triggers](https://github.com/skills/exercise-creator/blob/main/docs/reference/transition-triggers.md)
and [events that trigger workflows](https://docs.github.com/actions/reference/workflows-and-actions/events-that-trigger-workflows).

## Action → trigger table

| Learner action | Trigger | Filters and guards |
| --- | --- | --- |
| Create and push a new branch | `push` | `branches: [exact-name]` or `branches-ignore: [main]` |
| Commit a file on a branch (web editor or terminal) | `push` | `branches: [name]` plus `paths: [the-file]` |
| Commit a new file on `main` | `push` | `branches: [main]` plus `paths:` of a file that does **not** exist in the template |
| Open a pull request | `pull_request` | `types: [opened]`, `branches: [main]` |
| Push more commits to an open pull request | `pull_request` | `types: [synchronize]` |
| Merge a pull request | `pull_request` | `types: [closed]` plus job guard `github.event.pull_request.merged == true` |
| Submit a review | `pull_request_review` | `types: [submitted]`; optionally `github.event.review.state == 'approved'` |
| Open an issue | `issues` | `types: [opened]`; filter by label or title (never a title containing `Exercise`) |
| Assign an issue (for example to Copilot) | `issues` | `types: [assigned]` |
| Answer in the exercise issue | `issue_comment` | `types: [created]`; guard `!github.event.issue.pull_request` and `contains(github.event.issue.title, 'Exercise')` |
| Comment on a pull request | `issue_comment` | guard `github.event.issue.pull_request` |
| Run or write a workflow | `workflow_run` (`workflows: [Name]`, `types: [completed]`) or grade with `wait-for-workflow` | The **listening** workflow file must exist on the default branch; the triggering workflow can run on any branch (limit it with `branches:`). Check `github.event.workflow_run.conclusion` and use `github.event.workflow_run.head_sha` to inspect the triggering commit |
| Publish a release | `release` | `types: [published]` |
| Build GitHub Pages | `page_build` | none |
| Create a discussion | `discussion` | `types: [created]` |
| Finish codespace setup or run a script | `repository_dispatch` | `types: [custom-name]` sent with `gh api` from the script |
| Publish a package | `registry_package` | `types: [published]` |
| Anything without a natural event | `issue_comment` | Ask the learner to comment a specific phrase in the exercise issue |

Always keep `workflow_dispatch` too, so facilitators and testers can re-run a step.

## The template-copy push

When a learner copies the exercise, GitHub creates the repository with one commit on `main` (message
`Initial commit`). That push reaches **every** workflow in the copy before Step 0 disables them, because
workflow enabled/disabled state is not copied from the template. A step workflow must never fire on it.

Safe by design:

- `push` with `branches:` that excludes `main`.
- `push` to `main` with `paths:` that only match files the learner creates (never files in the template).
- Any non-push event (`pull_request`, `issues`, `issue_comment`, ...).

If a `push` to `main` trigger cannot avoid existing files, guard the first job:

```yaml
jobs:
  find_exercise:
    if: github.event_name != 'push' || (github.event.created == false && github.event.head_commit.message != 'Initial commit')
```

Use `github.run_number != 1` only when the copy push is guaranteed to trigger the workflow; otherwise it skips
the learner's first real attempt.

## Pitfalls

| Pitfall | Effect | Fix |
| --- | --- | --- |
| `push` to `main` without `paths` | Step runs at copy time and skips ahead | Filter by branch or new-file paths |
| `paths` lists a file already in the template | Same as above | Choose a file the learner creates |
| `pull_request` `closed` without a merged guard | Closing without merging finishes the step | Add `github.event.pull_request.merged == true` |
| `issue_comment` without a pull request guard | Pull request comments advance the exercise | Guard on `github.event.issue.pull_request` |
| Learner-created issue titles contain `Exercise` | `find-exercise-issue` picks the wrong issue | Avoid the word, or set a distinctive `issue-title-prefix` and matching `issue-title-text` |
| Trigger depends on Mona's own action | Events created with `GITHUB_TOKEN` do not start workflows; pull requests Mona opens or updates create runs that wait for approval | Trigger on the learner's action |
| Workflow named differently from `Step N` | `gh workflow enable "Step N"` fails | Keep `name: Step N` |
| A second quick push | Two runs grade at once | `concurrency: { group: ${{ github.workflow }}, cancel-in-progress: true }` |
| Steps built on Copilot coding agent pull requests | Workflows on pull requests from Copilot may need a person to approve the run | Trigger on what the learner does (assigning, reviewing, merging) and say so in the instructions |
| Non-exercise workflow file starts with a digit | Step 0 disables it when the exercise starts | Name it without a leading digit (`ci.yml`) |

## Testing a trigger

1. Validate statically: `validate_exercise.py` flags copy-time and wiring risks.
2. Locally: [nektos/act](https://nektosact.com/) with sample payloads, as described in
   [exercise-creator's workflow testing guide](https://github.com/skills/exercise-creator/blob/main/docs/guide/test-a-workflow.md).
3. Live: the `exercise-walkthrough-test` skill performs the real action in a disposable copy and measures the
   result with the harness `wait-step` command.
