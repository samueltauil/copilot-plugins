---
name: exercise-walkthrough-test
description: Run an automated end-to-end walkthrough of a GitHub Skills exercise as a learner, using Computer Use to drive and observe the real UI (browser on github.com, Codespaces or VS Code, terminal with Copilot CLI, Copilot app) plus a gh-based harness for ground truth. Validates execution (triggers, grading, feedback, transitions, recovery), UI fidelity (labels, locations, rendered comments) and usability (cognitive walkthrough, heuristics, ease ratings), then writes a severity-rated report. Use before publishing, after changes, before a workshop, or when learners get stuck.
---

# Walkthrough-test an exercise with Computer Use

Play the learner in a disposable copy of the exercise and check three things at every step:

- **Execution:** the action fires the trigger, grading passes correct work and rejects plausible mistakes with
  actionable feedback, recovery works, and Mona posts the next step.
- **UI fidelity:** every label, location, link, image, and screenshot in the instructions matches the real UI,
  and Mona's comments render correctly.
- **Usability:** each instruction passes the cognitive walkthrough, friction is rated, and time is measured.

Computer Use operates the UI the way a learner would. The harness
[`scripts/exercise_harness.py`](scripts/exercise_harness.py) (Python 3.9+, `gh`) reports repository truth: runs,
comments, current step, latency, rendering problems, and codespaces. Paths in this skill are relative to this
skill's folder; run scripts with their full path, for example
`python <skill-folder>/scripts/exercise_harness.py status --repo ...`.

## Modes

| Mode | Who performs learner actions | Covers | Approvals |
| --- | --- | --- | --- |
| `ui` (default) | Computer Use, through the real UI, exactly as written | Execution, UI fidelity, usability | Every state change the Computer Use action policy marks ALWAYS CONFIRM, one approval per action |
| `cli` | The harness, `git`, and `gh`; no Computer Use | Execution and rendered comments only | The user approves the run plan, which lists every state change in the sandbox copy; anything not listed needs its own approval |
| `static` | Nobody: validator plus a paper cognitive walkthrough | Content and wiring only | None |

Rules that apply to every mode:

- Use one UI driver per run. In `ui` mode that is Computer Use for every surface; once you use it for app UI, you
  observe and act only through it. Never launch, focus, or click UI through a shell.
- A refusal never authorizes another route. If the user declines an action, do not perform it with a different tool
  or mode; record the step as not executed.
- If Computer Use is unavailable, run `cli` mode (or a browser-automation tool for github.com-only exercises) and
  mark UI fidelity and usability for desktop surfaces as not verified.

## Requirements

- `ui` mode: Computer Use enabled (Copilot CLI: `/computer show`, then `/computer on` if needed).
- `gh` signed in with `repo` and `workflow` scopes; `codespace` to list or delete test codespaces; `delete_repo` only
  to delete the copy.
- A sandbox owner (personal account or test organization) that the user approves. Never test in production
  organizations or directly on the template.
- A template that contains the exact commit under test. For a new exercise or an unmerged change, publish it to a
  staging template first (`exercise-publish`, Path S), with explicit authorization.
- The exercise passes `../exercise-review/scripts/validate_exercise.py` with no blocking findings, or the user
  accepts testing it anyway.

## Safety rules (non-negotiable)

1. In `ui` mode, the first Computer Use call is `var windows = cua.listWindows();` on its own. Read the
   documentation and action policy it returns; the policy overrides anything here.
2. Before each ALWAYS CONFIRM action (submitting a form such as **Create repository**, **Commit changes**, opening
   or merging a pull request, posting a comment, creating a codespace, deleting anything), ask
   "Do you approve [action] to [consequence]?" and stop. One approval covers one action and is used once. The
   original request is not approval. Never act first and ask afterwards.
3. Hand sign-in, credential changes, and operating-system authentication to the user. Never type credentials.
4. Work only in the disposable learner copy and the windows you bound for the test. Leave the template, other
   repositories, and unrelated windows alone.
5. The harness refuses to create or clean up without `--yes`, and `create` requires an explicit `--visibility`.
   Pass `--yes` only after the user approved that exact action. Never make a public copy of a private or internal
   template.
6. Keep secrets and unrelated personal data out of screenshots and logs.

## Procedure

### 1. Plan

Fill [references/test-plan-template.md](references/test-plan-template.md): template and commit, mode, sandbox
owner, copy name, visibility, persona, surfaces, cleanup, every approval you will need, and the action map
(instruction → type → expected UI element → expected trigger or check → negative test). Show the plan and get
approval for it. In `cli` mode this approval covers the listed state changes; in `ui` mode it does not replace
per-action approvals.

### 2. Static pass

```bash
python ../exercise-review/scripts/validate_exercise.py <checkout-of-commit-under-test> --format markdown \
  --template-repo <final-owner>/<final-name>
```

Pass `--template-repo` with the final repository: on a staging checkout the git remote is the staging repository,
while the README badge intentionally names the final one. Read every step file and run a paper cognitive walkthrough
([references/usability-heuristics.md](references/usability-heuristics.md)). Note risks to verify live.

### 3. Preflight

```bash
python scripts/exercise_harness.py preflight --template <owner>/<template> --owner <sandbox-owner>
```

Confirm the template's default-branch commit (`head_sha`) is the commit under test (`git rev-parse HEAD` of the
reviewed exercise). In `ui` mode, make the first Computer Use call, bind the browser window, and confirm the user
is signed in to github.com there; hand off sign-in if not.

### 4. Copy and start

1. Open the template README. Check the Copy Exercise button's parameters as text (`template_owner`,
   `template_name`, `owner=%40me`, `name=skills-<repo>`, `description`, `visibility`). On a staging template the
   button points at the final repository, so do not follow it; use the staging repository's **Use this template**
   button instead.
2. Create the copy with the approved name and visibility:
   - `ui`: fill the "Create a new repository" form, then ask before clicking **Create repository**.
   - `cli`: `exercise_harness.py create --template <t> --owner <o> --visibility <v> --yes` (listed in the plan).
3. `exercise_harness.py wait-start --repo <copy>`: records copy → issue → step 1 latency and whether "about
   20 seconds" held.
4. Refresh the repository page: the README shows the exercise-started page with a link to the issue. Open the issue
   and read the welcome message and step 1.

### 5. Each step

For step `N`:

1. **Read** the step comment (text-first). Check headings, theory, activities, badges, images (screenshot only if
   needed), and that every Having trouble block opens.
2. **Walk** each instruction: locate the named control where the text says it is, confirm the label matches,
   perform it (`ui`, asking before submissions) or perform the equivalent with `git`/`gh` (`cli`), check the
   confirmation cue, and answer the four walkthrough questions.
3. **Negative tests**, before the correct action. Take a timestamp with `exercise_harness.py now` before each one.
   - A mistake that still matches the trigger (right branch and file, wrong content):
     `wait-step --repo <copy> --step N --since <ts> --expect fail`. Expect `failed-check`; verify the results table
     and tips explain the fix and that Having trouble covers it.
   - A mistake the trigger filters out (wrong branch, wrong path, closing instead of merging):
     `wait-step ... --expect none`. Expect `ignored`: no graded run and no new step. Learners get no reply here,
     so the step's Having trouble block must tell them what to check when Mona stays silent.
4. **Correct action:** new timestamp, perform the final action, then
   `wait-step --repo <copy> --step N --since <ts>`. Expect `advanced` and record `feedback_after_s`.
5. **Verify the transition in the UI:** refresh the issue; the results table (graded steps), the "step finished"
   message, step `N+1`, and the "watching" message appear in order.
6. **Rate** the step: Single Ease Question (1–7) with a reason, walkthrough failures, heuristics violated.

`wait-step` only watches the `Step N` workflow, so unrelated runs (for example a learner CI workflow that is
supposed to fail) do not count. If a step does not advance, use `status`, `runs --failed-logs`, and `timeline` to
find out why, record the finding, and stop unless the user wants you to work around it.

### 6. Finish

After the last step, the review is posted, the "finished" comment appears, the issue is closed, and the README
shows the congratulations page. Then:

```bash
python scripts/exercise_harness.py lint-comments --repo <copy>
python scripts/exercise_harness.py timeline --repo <copy>
```

### 7. Clean up

Run `exercise_harness.py codespaces --repo <copy>` to see codespaces the test created (stopped codespaces still use
storage). Then ask whether to archive the copy (default, keeps evidence) or delete it, and separately whether to
delete its codespaces, and run, for example,
`exercise_harness.py cleanup --repo <copy> --mode archive --delete-codespaces --yes`. Report anything retained.

### 8. Report

Write the report with [references/report-template.md](references/report-template.md): verdict, execution matrix,
UI fidelity, usability, rendering checks, findings with severity and owning skill, time, what was not verified,
evidence, and cleanup. Route fixes: content → `exercise-content`, triggers and grading → `exercise-automation`,
wiring → `exercise-scaffold`.

## Harness reference

| Command | Purpose |
| --- | --- |
| `now` | UTC timestamp to pass as `--since` before an action |
| `preflight [--template] [--owner]` | gh, scopes, template flag and default-branch commit, organization membership |
| `create --template --owner --visibility public\|private\|internal [--name] --yes` | Create the learner copy (exit 3 without `--yes`; refuses public copies of non-public templates) |
| `wait-start --repo` | Wait for the issue and step 1; latency and "20 seconds" check |
| `status --repo [--json]` | Active step workflow, steps posted, review, finished, runs, last comments |
| `comments --repo [--since] [--full] [--json]` | Read Mona's and the learner's comments |
| `wait-step --repo --step N --since <ts> [--expect pass\|fail\|any\|none]` | `advanced`, `failed-check`, `ignored`, `workflow-error`, or `timeout`, for the `Step N` workflow only |
| `lint-comments --repo` | Unrendered `{{ }}`, unrendered alerts, relative images or links, missing images |
| `timeline --repo [--json]` | Chronological runs and comments with durations |
| `runs --repo [--failed-logs]` | Recent runs and the last failed log |
| `codespaces --repo` | Codespaces that belong to the copy |
| `cleanup --repo --mode archive\|delete [--delete-codespaces] --yes` | Archive or delete the copy and optionally its codespaces (exit 3 without `--yes`) |

Details for driving each surface (browser, VS Code or codespaces, terminal, Copilot app) are in
[references/computer-use-playbook.md](references/computer-use-playbook.md).

## Limits

An agent is not a representative learner. It reads faster, may fill gaps, and sees an accessibility tree. Use the
walkthrough to remove defects before people test, report agent ratings as judgments, and recommend testing with
learners who match the persona. Copilot responses vary: judge whether the instructions hold up across reasonable
variations, never whether an AI response matches exact text.
