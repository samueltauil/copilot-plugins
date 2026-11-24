# Review rubric

Seven lenses. Answer each item **yes**, **no** (a finding), **unknown** (needs a live test or learners), or
**n/a**. The validator (`scripts/validate_exercise.py`) answers most of lens 1 and part of lenses 2, 5, and 6;
the rest needs judgment.

## 1. Framework contract and wiring (validator rules S, W0xx, C001, C008, R)

1. Every numbered step file is posted by exactly one workflow, and the final workflow posts `x-review.md`.
2. Workflow names are `Step N`; every `gh workflow enable` target exists; Step N enables Step N+1.
3. Step 0 calls `start-exercise.yml`, is guarded by `is_template`, has a `push` trigger on `main`, enables Step 1.
4. Only the final workflow calls `finish-exercise.yml`.
5. One toolkit tag everywhere, a published release, no `@main`.
6. No placeholders remain (`replace-me`, `<STEP>`, `(replace-me-owner)`).
7. The README has exactly one Copy Exercise button with the right owner, template name, `skills-` copy name,
   `owner=%40me`, and visibility.

## 2. Automation reliability and safety (validator rules W030+)

8. Each trigger is produced by the final action of its step and cannot fire on the template-copy push.
9. Graded steps gate progress (`needs: check_step_work`), every check reports a row, and the job fails on any
   failed check.
10. `find-comment` filters `comment-author: github-actions[bot]`.
11. Least-privilege permissions; the grading job has no `actions: write`.
12. No untrusted context interpolated into scripts; no `pull_request_target`; no branch-pinned actions.
13. Every variable a step file uses is passed in `vars:` by the workflow that posts it (missing ones render
    empty), and any `${{ }}` or literal `{{`, `{%`, `{#` in step Markdown is wrapped in `{% raw %}`.
14. Each check is valid: it observes what the objective needs, accepts legitimate alternatives, and was (or will
    be) tested with a correct, a wrong, and an alternative artifact. A `wait-for-workflow` check also asserts the
    awaited run's `conclusion`.

## 3. Learning design (from the learning-design skill)

15. The README states one observable new skill, prerequisites, access needs, costs, and a realistic time.
16. Every activity performs the behavior in its step objective (alignment).
17. Each theory section introduces only what its activity needs; terms are defined before use.
18. Step 1 is a worked example with a quick, guaranteed win.
19. Support fades across steps without abrupt drops.
20. At least one retrieval or generation moment after step 1.
21. Failure feedback names the problem and one next action (rows plus tips); it describes work, not the person.
22. The review recaps capabilities, asks a recall question with an answer, and includes a transfer prompt.
23. No mastery is claimed from proxy checks.
24. No learning myths (learning styles, retention pyramids, ten-minute attention) in content or justification.

## 4. Clarity and usability (paper cognitive walkthrough)

For each instruction, ask the four walkthrough questions:

- Will the learner try to achieve the right effect (do they know what this instruction is for)?
- Will they notice that the correct control is available (is its location described first)?
- Will they associate the control with the effect (is the label exactly what the UI shows)?
- After acting, will they see progress (is there a confirmation cue, and does Mona respond)?

Plus:

25. Context switches (issue tab, codespace, terminal) are announced.
26. Every activity has its own Having trouble block written as symptom, cause, recovery, including how to
    re-trigger Mona.
27. Lists render as intended (no restarted numbering, no indented GitHub alerts).
28. Terminology and UI labels are consistent across steps.

## 5. Accessibility

29. Informative images have meaningful alt text; badges have meaningful alt text.
30. Link text is descriptive; headings are in order; status never depends on color or emoji alone.
31. Keyboard shortcuts are given for both platforms; no time-limited actions.
32. Video, if any, has captions and a transcript.

## 6. Maintainability

33. No copied Docs text; links point to official sources.
34. No volatile facts (prices, quotas, model lists) unless the exercise is about them and has an owner to update
    them.
35. Screenshots match the current UI (confirm in the walkthrough test).
36. Pins follow the known-good set; upgrades are applied everywhere at once.

## 7. Publication readiness

37. LICENSE matches the README footer year and holder.
38. Repository settings checklist is planned (template flag, disabled step workflows, features, merge settings).
39. A walkthrough test passed end to end, including at least one failed check and recovery.

## Severity guide

| Severity | Use when | Usability severity equivalent (Nielsen) |
| --- | --- | --- |
| **Blocking** | The exercise breaks, skips ahead, strands learners, leaks privileges, or ships placeholders | 4 (catastrophe) |
| **Important** | Learners are likely to get confused, stuck for minutes, or learn the wrong thing; accessibility barriers | 3 (major), some 2 |
| **Nice to improve** | Polish, consistency, stronger learning moves | 2 (minor), 1 (cosmetic) |

Rate usability problems by frequency, impact, and persistence. A problem every learner hits that blocks progress is
Blocking even if it is "just wording".
