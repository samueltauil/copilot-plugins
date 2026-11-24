# Scaffolding patterns

Patterns that put the learning-design principles into step content. Use them deliberately and sparingly; each
step should feel light.

## The support ladder

| Step position | Support | What the instructions look like |
| --- | --- | --- |
| First | Worked example | Exact clicks, exact names, exact prompt, a screenshot where navigation is hard, a confirmation cue |
| Middle | Completion | The goal plus key specifics; refer back to an earlier step for the familiar parts; tips instead of exact text |
| Last | Independent | A goal and constraints; hints in Having trouble; grading on the outcome |

Never drop more than one rung between consecutive steps.

## Retrieval moments

- **Reuse without the recipe:** "Create a branch named `fix-typo`, the same way you did in step 1."
- **Recall before reveal (review):**

  ```markdown
  <details>
  <summary>Which event did Mona watch for in step 2, and why that one?</summary><br/>

  `pull_request`: opening the pull request is the action that shows your change is ready for review.

  </details>
  ```

- **Spot the difference:** "Before you run it, which of these two triggers fits a nightly job?" with the answer
  in a collapsible block.

## Generation tasks

- Let learners write their own commit messages, pull request titles, issue text, and prompt variations.
- Grade only what must be exact (file names, branch names the workflow listens to), and say so explicitly.
- Offer a model answer afterwards: "Here's one way to phrase it: ...".

## Prediction prompts

> Before you click **Run workflow**, predict: will this run on your branch or on `main`? Check the run's branch
> afterwards.

Use at most one per step, before a consequential action, and always resolve it.

## Hint ladder in Having trouble

Order bullets from gentle to explicit:

1. Clue: "Check which branch the selector shows."
2. Targeted instruction: "Switch the selector to `add-docs`, then commit again."
3. Worked example: a short exact sequence or a screenshot.

Write every bullet as symptom, cause, and recovery, and include how to re-trigger Mona.

## Fast path for experienced learners

```markdown
> 💡 **Tip:** Comfortable with the GitHub CLI? Run `gh pr create --fill` instead of steps 2 to 4.
```

Only add a fast path when the grading accepts both routes.

## Transfer prompts

- In the review: "Where in your own repositories would a required review have caught a problem?"
- A "Take it to your work" challenge: one small, concrete thing to try this week.
- Keep reflection private: never ask learners to post work details in a public issue.

## Anti-patterns

| Anti-pattern | Why it hurts | Instead |
| --- | --- | --- |
| A wall of theory before any action | Overloads working memory | Two to five sentences, then do |
| Same exact instructions in every step | No fading, no retrieval | Refer back and fade |
| Hidden essential steps "to make it challenging" | Undesirable difficulty | Challenge the thinking, not the navigation |
| Hints that only restate the instruction | No new information | Symptom, cause, recovery |
| Grading the exact wording of an AI response | Invalid check | Grade the artifact the learner controls |
| Quiz questions graded by exact keyword | Rejects valid answers | Self-check with collapsible answers |
