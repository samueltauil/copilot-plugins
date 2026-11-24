---
name: exercise-outline
description: Design a learner-centered GitHub Skills exercise outline from a topic, idea, demo, workshop module, or existing training material, including learner persona, one observable objective, step-by-step theory and activities, triggers, grading checks with what they prove, feedback, review, naming and file map. Use before building any exercise files, or when converting slides or labs into self-paced steps automated by GitHub Actions.
---

# Create a GitHub Skills exercise outline

The outline is the build contract: the scaffold, content, and automation skills must be able to build the
exercise from it without guessing. Invest here; every minute saves hours of fixes **(exercise-creator guidance)**.

## Inputs to gather

Ask only for what is missing; propose sensible defaults.

- Topic and the one new skill. If the topic is broad, propose a split.
- Learner: role, prior knowledge, constraints, access needs (load `learning-design` for the persona).
- Environment: browser only, Codespaces, local VS Code, Copilot CLI, Copilot app.
- Time box (default: 30 to 45 learner minutes).
- Source material to convert (slides, docs, labs) and any organization standards.
- Owner, copyright holder, and whether it belongs to a series (`workshop-design`).

## Workflow

1. **Narrow** to one primary skill. Out-of-scope ideas go to "Future considerations".
2. **Analyze the learner** and write the persona section.
3. **Backward design:** write the exercise objective, then one observable objective per step and the evidence
   for each (alignment matrix). Use [learning-design objectives guidance](../learning-design/references/objectives-and-evidence.md).
4. **Story:** one scenario; each step raises one question its activity answers.
5. **Identity:** propose the title and repository names (rules below).
6. **Steps:** three to five, each building on the last, using the requirements table below.
7. **Support curve:** step 1 is a worked example with a quick win; fade guidance; place retrieval, generation,
   and prediction moments.
8. **Transitions:** for every step, choose a trigger that the final action produces and that cannot fire on the
   template-copy push; decide graded or ungraded; write what each check proves and the failure feedback. Use
   the [triggers reference](../exercise-automation/references/triggers.md) and
   [grading patterns](../exercise-automation/references/grading-patterns.md).
9. **Review:** recap as capabilities, recall questions, transfer prompt, what's next.
10. **File map, test plan, risks.** Fill in [assets/exercise-outline.md](assets/exercise-outline.md).
11. **Present and iterate** until the user explicitly approves (Gate 1).

## Exercise identity

- **Title:** outcome-focused with a short hook, for example "Ship Safely: Protect Your Main Branch".
- **Repository names:** offer three to five; lowercase letters, digits, and hyphens; start with a letter; under
  about 40 characters; topic first (`branch-protection-ship-safely`).
- Never prefix with `skills-`. The Copy Exercise button adds it, so the learner's copy becomes
  `skills-<repository>`.
- Recommend one name with a one-sentence reason.

## Step requirements

| Element | Requirement |
| --- | --- |
| Question | The one question this step answers (story hook) |
| 📖 Theory | Exactly one; two to five sentences of real, awareness-level content tied to the activity; terms defined before use |
| References | One to three official links, used inline in the theory |
| ⌨️ Activity | One to three per step; one concept each; numbered actions tagged by type (GitHub UI, chat prompt, CLI prompt, terminal) |
| Confirmation cues | What the learner should see after consequential actions |
| Final action | The one action that produces the trigger event |
| Having trouble | Top mistakes per activity as symptom → cause → recovery |
| Trigger | Event plus filters; copy-time safety explained |
| Grading | Checks with what each proves and does not prove, or "ungraded" with a reason |
| Feedback | Results-table rows in learner language and tips for likely failures |
| Artifact | What exists in the repository after success |
| Time | Estimated learner minutes |

## Converting existing material

| Source | Becomes |
| --- | --- |
| Module objective | Exercise objective |
| Slide explanation | Theory (trimmed to awareness) plus Docs links |
| Live demo | Step 1 worked example |
| Lab task | Activity with a triggering action and a check |
| Lab solution | Having trouble hints and recall answers |
| Quiz question | Recall question in the review, or an `issue_comment` answer step |

Drop anything the activities do not need. If the material covers several skills, propose a series and hand it to
`workshop-design`.

## Quality bar (check before asking for approval)

- One new skill; every step objective is observable and traces to the exercise objective.
- Every step has a theory, at least one activity, troubleshooting, a trigger, and a grading decision.
- Every trigger is produced by the final action and is safe on the template-copy push.
- Every check states what it proves; no check requires exact wording of AI output.
- Step 1 can be finished quickly by the persona.
- At least one retrieval moment after step 1 and one in the review.
- References come from official sources: GitHub Docs, GitHub Learn, GitHub Blog and Changelog, VS Code docs.
- No `replace-me` remains except in sections deliberately left for the user to decide.

## Approval gate

Do not create repository files from this skill. When the user approves, confirm the title, repository name, step
count, graded steps, and file map, then hand off to `exercise-scaffold`. The approved outline is saved to
`.github/exercise-outline.md` in the exercise repository.
