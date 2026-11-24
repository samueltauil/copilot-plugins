---
name: exercise-review
description: Review a GitHub Skills exercise or draft without changing it - run the static validator, then audit framework wiring, workflow safety, grading validity, learning design, clarity (paper cognitive walkthrough), accessibility, maintainability and publish readiness, and report severity-ranked findings with proposed fixes. Use when asked to review, audit, QA, or check an exercise before publishing, after a build round, or when adapting an existing exercise for a workshop.
---

# Review a GitHub Skills exercise

Report-only. Do not edit files, push, or change repository settings during a review, even when tools allow it.
Findings and proposed fixes go to the user, who decides what to apply in a separate build round.

For an independent review, run this skill through the `exercise-reviewer` agent (separate context from the
author). A review by the same session that built the exercise is a self-check, not independent review; say which
one it is in the report.

## Process

1. **Identify the promise.** Read the README and `.github/exercise-outline.md` (if present): learner, objective,
   steps, time.
2. **Run the validator** from the exercise root:

   ```bash
   python <this-skill>/scripts/validate_exercise.py <exercise-root> --format markdown --online
   ```

   Add `--template-repo OWNER/NAME` when the git remote is not the published template. Drop `--online` without
   network access. PyYAML is optional. Exit code 1 means blocking findings.
3. **Trace the learner journey** step by step: README → Copy Exercise → issue → step 1 → action → feedback →
   ... → review. For every instruction, ask the four cognitive walkthrough questions (see the rubric).
4. **Inspect each workflow** against its step: does the final action produce the trigger, is it copy-safe, does
   grading prove the objective, is feedback actionable, are permissions minimal?
5. **Apply the rubric** in [references/review-rubric.md](references/review-rubric.md), lens by lens. Use the
   `learning-design` skill's references for the learning lens.
6. **Rank findings** with the severity guide. Merge duplicates; keep validator rule IDs in the evidence.
7. **List what you could not verify** without a live run, and propose a walkthrough focus.
8. **Write the report** with [references/report-template.md](references/report-template.md), then stop and ask
   which fixes to apply.

## What the validator checks

| Group | Examples |
| --- | --- |
| Structure (S) | step numbering, five-step limit, review file, README, LICENSE, workflow file names |
| Workflows (W) | names, enable targets, posting of every step, toolkit pins, Step 0 guard, final workflow, copy-time triggers, grading wiring, find-comment filter, permissions, script injection, template variables |
| Content (C) | step headings, theory and activities, Having trouble per activity, instruction count and depth, list breaks, indented alerts, images (path, existence, alt), relative links, placeholders |
| README (R) | welcome block, Copy Exercise parameters, footer |
| Learning (L) | objectives per step, observable verbs, first-step difficulty, time vs README promise, review retrieval |

It cannot judge clarity, accuracy against the current UI, or whether checks are valid for the objective. That is
your job, and the walkthrough test's.

## Rules

- Evidence for every finding: file and line, quoted text, or validator rule.
- Explain why it matters for learners (and the principle when relevant) and propose a concrete fix.
- Prefer fewer, high-signal findings over long lists of nits.
- Do not recommend changes that conflict with the framework contract.
- If the same finding survives two fix rounds, escalate it to the user instead of re-reporting it silently.
