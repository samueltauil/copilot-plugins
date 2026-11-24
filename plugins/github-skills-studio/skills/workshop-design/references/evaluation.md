# Evaluating a workshop

Use Kirkpatrick's four levels to ask different questions. They are not a causal chain, and satisfaction alone
does not show learning.

| Level | Question | Instrument | When |
| --- | --- | --- | --- |
| 1. Reaction | Was it relevant and usable? | Two to five survey items, the Single Ease Question per exercise, optional SUS for the whole workshop | End of each exercise or session |
| 2. Learning | Can they do it with less support? | A short, less-guided task or knowledge check, scored with a rubric | End of the workshop |
| 3. Behavior | Do they use it at work? | Opt-in follow-up after 30 days ("Have you used X? How?") | Later |
| 4. Results | Did something the organization cares about change? | Cautious comparison of relevant metrics, with a comparison group if you make causal claims | Later |

## Reaction items (examples)

- "How relevant was this exercise to your work?" (1 to 5)
- "Overall, how easy or difficult was this task?" (Single Ease Question, 1 to 7)
- "What was the most confusing moment?" (free text; feeds Having trouble blocks)

## Learning evidence

- A capstone exercise graded on outcomes, done with lighter guidance than the guided exercises.
- Recall questions answered before revealing answers (self-check, not graded).
- Do not use exercise completion as proof of learning: it shows that checks passed.

## Completion data (with consent)

- In a learning organization, the walkthrough harness `status` command shows, for a learner copy, the current
  step, posted steps, and whether the exercise finished. Aggregate only with the learners' and organization's
  agreement, and never read repository contents beyond what is needed.
- Track where learners stop (the step whose workflow is still enabled). Repeated stops at the same step point to
  a design problem worth a walkthrough test.

## Closing the loop

1. Collect feedback in one tracking issue per exercise.
2. Turn recurring confusion into Having trouble bullets, clearer instructions, or a split step.
3. Re-run the walkthrough test after changes.
4. Record changes in the exercise's release notes.
