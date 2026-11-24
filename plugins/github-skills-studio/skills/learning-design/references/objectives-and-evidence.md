# Objectives, evidence, and alignment

Backward design: decide what learners should be able to do, decide what evidence would show it, then design the
activities and the checks. Everything in the exercise should trace to an objective.

## Writing objectives

An objective names an observable behavior, the context, and when useful a quality bar:

> Create a branch protection rule that requires a pull request review before merging to `main`.

Prefer verbs that produce evidence in a repository or an issue:

| Cognitive work (revised Bloom) | Verbs that fit GitHub Skills | Evidence a workflow can observe |
| --- | --- | --- |
| Remember / understand | identify, explain, compare, choose | Answer in an issue comment; choice in a checklist |
| Apply | create, configure, run, commit, open, assign | File, setting, branch, pull request, workflow run |
| Analyze | diagnose, trace, review, debug | Fixed file, review comment, passing workflow |
| Evaluate | justify, select, critique, approve | Review decision with a reason |
| Create | design, compose, author, automate | New workflow, agent file, instructions file |

Avoid "understand", "learn", "know", "be familiar with", and "explore" as the main verb: they are not observable.
A verb alone does not fix difficulty. "Create a workflow" can be trivial or advanced depending on the conditions.

## Alignment matrix

Fill this in the outline. Every row must be complete before building.

| Step | Objective (observable) | Activity that performs it | Evidence (what exists afterwards) | Automated check (what it proves) | What the check does **not** prove | Feedback if it fails |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Create a feature branch named `add-docs` | Create and publish the branch in the web UI | Branch `add-docs` exists | `push` trigger on `add-docs` fires | That the learner knows why branches isolate work | "Branch not found. Name it exactly `add-docs`." |
| 2 | ... | ... | ... | ... | ... | ... |

## Assessment validity checklist

For every check:

1. Name the objective it supports and the exact observation ("`.github/copilot-instructions.md` contains
   `test`, case-insensitive").
2. List legitimate alternative solutions and make sure they pass (synonyms, different file locations the
   instructions allow, different casing).
3. List plausible wrong answers and make sure they fail with useful feedback.
4. Run the check against a correct artifact, an incorrect artifact, and an alternative (the walkthrough test does
   this).
5. Do not claim mastery in the results table or review. Say what was observed: "Your workflow ran and passed",
   not "You have mastered CI".

## When not to grade

Leave a step ungraded (it advances on the event) when:

- No useful feedback could be given (open-ended exploration, prompt experimentation with Copilot).
- A wrong result cannot block later steps.
- The only possible check is a brittle proxy (exact wording of an AI response).

A step without grading is better than a step that strands learners on a false failure **(official guidance)**.

## Evidence beyond the workflow

If the exercise is part of a workshop that needs evidence of learning (for example, for certification
preparation), add a less-supported task at the end of the series, or a short knowledge check in the review, and
evaluate it separately from completion (see the workshop-design skill's evaluation reference).
