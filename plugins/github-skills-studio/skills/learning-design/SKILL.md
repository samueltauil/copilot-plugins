---
name: learning-design
description: Apply evidence-based learning psychology (cognitive load, worked examples and fading, retrieval practice, feedback, motivation, scaffolding, transfer, accessibility, assessment validity) to GitHub Skills exercises and workshops. Use when defining learners and objectives, deciding how a step should teach, writing feedback, judging whether an exercise will actually help people learn, or when someone asks why a design choice works.
---

# Learning design for GitHub Skills exercises

GitHub Skills exercises teach by doing: a short story, just enough theory, a hands-on activity in a real
repository, and automated feedback from Mona. This skill makes each of those moments deliberate, using
principles with real evidence behind them and avoiding popular myths.

## When to use

- Before outlining: to analyze the learner, choose one objective, and decide the evidence.
- While writing: to decide how much support each step gives and how feedback is phrased.
- During review: to check that the exercise teaches, not just runs.
- When converting a workshop or slide deck into self-paced steps.

## Core moves

Work through these in order. Record the decisions in the outline (`.github/exercise-outline.md`).

1. **Analyze the learner.** Write a short persona: role, what they can already do, likely misconceptions,
   motivation, constraints, access needs. See [references/learner-analysis.md](references/learner-analysis.md).
2. **Choose one new skill.** One observable objective for the exercise and one per step. If you need more than
   five steps, it is a series (load the `workshop-design` skill).
3. **Decide the evidence first.** For each step, what will exist afterwards, what a check can observe, and what
   it cannot prove. Fill the alignment matrix in
   [references/objectives-and-evidence.md](references/objectives-and-evidence.md).
4. **Plan the support curve.** Step 1 is a complete worked example with a quick win. Middle steps are partly
   specified. The last step sets a goal with lighter guidance. Keep hints available throughout.
5. **Place retrieval and generation.** From step 2, ask learners to repeat an earlier action without full
   instructions, write their own messages or prompts where grading allows, and answer one or two recall
   questions in the review.
6. **Design feedback.** Every check maps to a learner-readable expectation and a next action on failure. Use
   the patterns in [references/feedback-and-motivation.md](references/feedback-and-motivation.md).
7. **Design motivation honestly.** Relevance in the README and story, early success, meaningful choice, a
   recap that names capabilities, and a real next step. No fake progress, no mastery claims.
8. **Design for everyone.** Alt text, descriptive links, status not by color alone, plain language, keyboard
   operable hints, stated costs and access requirements.
9. **Plan validation with learners.** Schedule a walkthrough test (`exercise-walkthrough-test` skill) and, before
   release, testers who match the persona.

## Twelve rules to apply everywhere

1. One new skill per exercise; one concept per activity.
2. Theory is awareness level and only what the activity needs; link to GitHub Docs for depth.
3. Instruction, example, and expected result sit together; say what the learner should see after acting.
4. Location first, then the control in **bold**, then the value in `code`; announce context switches.
5. Fade support across steps; never remove help abruptly.
6. Include at least one retrieval moment after step 1 and one in the review.
7. Feedback names the observed problem and one next action; it describes the work, never the person.
8. Grade only when feedback is useful or later steps depend on it, and never let a failed check advance.
9. Each check states what it proves; accept legitimate alternatives.
10. Every activity has its own "Having trouble? 🤷" block: symptom, cause, recovery.
11. Accessible by default: alt text, link text, headings, non-color status, captions.
12. Measure with learners and walkthrough tests; treat time and step limits as heuristics.

The full table of rules by exercise part is in [references/design-rules.md](references/design-rules.md).

## Evidence and honesty

- Cite the principle when you justify a recommendation, using the labels in
  [references/evidence-base.md](references/evidence-base.md) (Strong, Moderate, Framework, Exploratory).
- Do not invent effect sizes or claim that a design guarantees learning.
- If a requester asks for learning styles, retention-percentage pyramids, or a ten-minute attention rule,
  explain kindly why you will not use them. See [references/myths-to-avoid.md](references/myths-to-avoid.md).

## Output

When asked for a learning design, return:

```markdown
## Learning design: <exercise title>

### Learner
<persona summary, prior knowledge, misconceptions, constraints, access needs>

### Objective and evidence
<exercise objective; alignment matrix rows per step>

### Support curve
<step-by-step: worked example → completion → independent; where hints live>

### Retrieval, generation, and reflection points
<where and how>

### Feedback plan
<per check: expectation, failure message, tips>

### Motivation and story
<scenario, the question each step answers, early win, ending>

### Accessibility and inclusion
<specific measures>

### Risks and open questions
<what to validate with testers>
```
