# Feedback messages

How Mona's comments flow during a step, and how to make them useful. Grounded in the feedback principles in the
`learning-design` skill (feed up, feed back, feed forward; describe the work, not the person).

## The comment lifecycle

| Moment | Comment | Created or edited | Template |
| --- | --- | --- | --- |
| Step content posted | `## Step N: ...` | created | your `.github/steps/N-step.md` |
| Right after | "I'll watch your progress..." | created | `step-feedback/watching-for-progress.md` |
| Learner acts, grading starts | "Let's see if I have some feedback..." | **edits** the watching comment | `step-feedback/checking-work.md` |
| Grading ends | `## Step N - Passed ✅` or `## Step N - Fail ❌` table | **edits** the same comment | `step-feedback/step-results-table.md` |
| Passed | "Preparing content for step N+1" | created | `step-feedback/step-finished-prepare-next-step.md` |
| Last step passed | "Let's do a quick review" then the review | created | `step-feedback/lesson-review.md`, `x-review.md` |
| Finished | Congratulations, issue closed, README updated | created | toolkit `finish-exercise.yml` |

The grading job edits one comment in place and never adds new ones, so a retry replaces the old result instead of
stacking failures.

## Results table rows

The template renders each row as "✅ - Pass" or "❌ - Fail" plus your description. Write descriptions as
learner-language expectations, so a failed row reads as what is still missing:

| Weak | Strong |
| --- | --- |
| "Checked file" | "`docs/plan.md` exists on the `add-docs` branch" |
| "Keyphrase check" | "Your plan mentions how you will test the change" |
| "Branch check" | "You pushed a branch named `add-docs`" |

## Tips (feed forward)

`step-results-table.md` renders an optional `tips` list. Show tips only on failure with an expression:

```yaml
tips: ${{ contains(steps.*.outcome, 'failure') && '["Create docs/plan.md on the add-docs branch, then push again.", "Use the branch selector above the file list to check which branch you are on."]' || '[]' }}
```

- Write each tip as one next action.
- Cover the two most likely causes (from walkthrough tests and tester feedback).
- No single quotes inside the tips (they end the expression string).

## Targeted messages with `step-mistake.md`

For a known mistake that deserves its own message (for example, the learner pushed to `main` instead of a
branch), use the toolkit's `step-feedback/step-mistake.md`, which renders `feedback_message`. Prefer folding the
message into the results comment (edit it) rather than adding a new comment:

```yaml
- name: Update comment - common mistake
  if: steps.check-branch.outcome == 'failure'
  uses: GrantBirki/comment@v2.1.1
  with:
    repository: ${{ env.ISSUE_REPOSITORY }}
    issue-number: ${{ env.ISSUE_NUMBER }}
    comment-id: ${{ steps.find-last-comment.outputs.comment-id }}
    edit-mode: replace
    file: exercise-toolkit/markdown-templates/step-feedback/step-mistake.md
    vars: |
      feedback_message: "Your commit went to `main`. Create the `add-docs` branch and commit there, then push again."
```

Use either the results table or the mistake message for a given run, not both, so the learner sees one clear
status.

## Honest status

- Never post "Passed" before checks complete; the toolkit order (checking → results) guarantees this.
- If a step is ungraded, its step content should say Mona advances when the action happens, not that work is
  checked.
- When a workflow fails for infrastructure reasons, learners see no new comment. Every step's Having trouble block
  should say how to check the **Actions** tab and how to retry.

## Custom templates

Only create a local `.github/markdown-templates/` file when no toolkit template fits. Keep Mona's voice, the
octocat image conventions, and Nunjucks variables passed through `vars:`.
