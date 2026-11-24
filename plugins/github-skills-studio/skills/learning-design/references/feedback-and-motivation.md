# Feedback and motivation patterns

How Mona should speak, and how each part of the exercise keeps learners motivated without overclaiming.

## Feedback levels applied to Mona

| Level (Hattie & Timperley) | Use in exercises | Example |
| --- | --- | --- |
| Task: is the result correct? | Results table rows | "✅ `docs/plan.md` exists on your branch" |
| Process: how to get there | Tips on failure, Having trouble hints | "Commit from the **plan** branch selector, not `main`, then push again." |
| Self-regulation: how to check yourself | Confirmation cues, prediction prompts | "Before you push, open the **Files changed** tab. Do you see one file?" |
| Self (praise of the person) | Avoid as the only content | Not "You're a natural!"; instead "Nice: that commit message says exactly what changed." |

Feed up, feed back, feed forward in one failure message:

> Step 2 needs a workflow that runs on `pull_request` (feed up). Your workflow file exists, but its trigger is
> `push` (feed back). Change `on:` to `pull_request`, commit, and push again (feed forward).

## Message patterns

| Situation | Pattern | Example |
| --- | --- | --- |
| Check failed | What was observed, what is expected, one next action | "The branch `main` was pushed. This step watches `add-docs`. Switch branches and push again." |
| Several checks failed | One row per check, tips for the two most likely causes | Results table plus `tips` |
| Workflow did not run | Tell the learner how to tell, and what to do | Having trouble: "No reply after two minutes? Open the **Actions** tab..." |
| Passed | Name what worked, then move on | Toolkit "step finished" template |
| Exercise finished | Recap capabilities, next step | `x-review.md` |

Avoid: "Wrong", "Oops, you failed", sarcasm, exclamation-mark walls, blame ("you forgot"), and claims of mastery.

## Motivation by exercise part (ARCS and self-determination)

| Part | Attention | Relevance | Confidence | Satisfaction |
| --- | --- | --- | --- | --- |
| README | Concrete outcome in the title | "What you'll build" names a real artifact | Honest prerequisites and time | |
| Step story | One question this step answers | Tie to the scenario and to real work | | |
| Step 1 activity | | | Quick, guaranteed early success | First ✅ within minutes |
| Later activities | Small variation or prediction | Choice where both routes are graded fairly | Hints next to each activity | Visible progress "Step 3 of 4" |
| Review | | Transfer prompt to own work | Recap of capabilities | Honest celebration and next step |

Autonomy: allow learners to choose names, messages, and examples where grading allows it. Competence: early
success, specific feedback, fading support. Relatedness: point to a community or facilitator channel; Mona is
friendly but is not a substitute for a human.

## Story and scenario

- Pick one scenario that matches the persona's work (an internal tool, a school website, an open source library).
- Keep the cast small and consistent; the learner is the protagonist and makes the decisions.
- Each step's story raises one question; the activity answers it.
- Light humor and themed flavor (for example, a mascot) help attention for some audiences; keep instructions
  literal and unambiguous regardless of the theme.

## Mona's voice

- Second person, present tense, active voice: "Create a branch named `add-docs`."
- Warm and brief: one emoji at most per paragraph, never inside instructions that must be copied.
- Professional, polite, inviting **(official)**; spell out "repository".
- Consistent names for UI controls, exactly as the UI shows them.
