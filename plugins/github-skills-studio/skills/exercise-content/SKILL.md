---
name: exercise-content
description: Write or improve the learner-facing content of a GitHub Skills exercise - step files with story, theory, activities, confirmation cues and Having trouble hints, the review, and README copy - using evidence-based scaffolding (worked examples then fading, retrieval, generation, feedback) and the official GitHub Skills formatting conventions. Use when drafting steps from an outline, rewriting confusing instructions, adjusting tone, adding hints, or making content accessible.
---

# Write exercise content

Learners meet the exercise one issue comment at a time. Each comment must be short, unambiguous, and doable
without leaving them guessing. This skill covers what learners read; triggers and grading live in
`exercise-automation`, wiring in `exercise-scaffold`.

## Before writing

- Read the outline's persona, objectives, support curve, and the step's transition (what the final action must
  produce, and what the check looks for). The instructions must make that exact outcome happen.
- Open the real UI you are describing (or ask for screenshots). Never describe a UI from memory; labels change.

## Writing a step

Follow the anatomy in [references/step-anatomy.md](references/step-anatomy.md):

1. `## Step N: <outcome title>` then a one-to-three sentence story hook that raises this step's question.
2. `### 📖 Theory: <concept>`: two to five sentences, terms defined before use, key words linked inline to
   GitHub Docs, at most one small table, list, or diagram.
3. `### ⌨️ Activity: <verb + object>` (number them when there are several): numbered instructions, location →
   control → value, context switches announced, a confirmation cue after consequential actions.
4. End the last activity with the triggering action and: "Wait a moment for Mona to check your work, provide
   feedback, and share the next lesson."
5. After **each** activity, a `Having trouble? 🤷` block: symptom → cause → recovery, including how to re-trigger
   the check.

## Apply the support curve

- Step 1 is a worked example: exact, complete, with a quick win.
- Later steps fade: refer back instead of repeating, let learners write their own messages and prompts, swap exact
  text for tips. See [references/scaffolding-patterns.md](references/scaffolding-patterns.md).
- Include at least one retrieval moment after step 1, and recall questions plus a transfer prompt in the review.

## Formatting essentials

Details and copy-ready snippets are in [references/writing-style.md](references/writing-style.md).

- `1.` for every instruction, one blank line between them, three-space indentation for anything inside.
- No GitHub alerts inside lists; use the emoji blockquotes (`> 💡 **Tip:** ...`).
- Prompts and commands in badge-led blockquotes with meaningful alt text.
- `{{ full_repo_name }}` and `{{ login }}` for personalization (the posting workflow must pass them in
  `vars:`; missing ones render empty); `{% raw %}` around any `${{ }}` or literal `{{`, `{%`, `{#`.
- Images in `.github/images`, referenced as `../images/<file>` with `alt` and `width`.
- No relative links like `../../actions` in step files; use `https://github.com/{{ full_repo_name }}/actions`.

## Accessibility

Run [references/accessibility.md](references/accessibility.md) on every step: alt text, link text, heading
order, non-color status, keyboard shortcuts for both platforms, no time pressure, disclosed requirements.

## Tone

Friendly, casual, active, and precise. Describe the work, never the learner. Spell out "repository". Keep theme
and humor out of the literal instructions.

## Self-check before handing off

- [ ] Each activity practices one concept and ends in an observable result.
- [ ] Every instruction can be followed literally by the persona, with no unstated assumptions.
- [ ] The final action produces exactly what the step's trigger and checks expect (branch names, file paths,
      keyphrases).
- [ ] Theory covers every concept the activity uses, and nothing more.
- [ ] Hints cover the top mistakes; the walkthrough test will add more.
- [ ] Support fades across steps; retrieval and generation moments are present.
- [ ] The validator reports no content findings above "Nice to improve" without a reason.
