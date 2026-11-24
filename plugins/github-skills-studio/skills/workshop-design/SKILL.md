---
name: workshop-design
description: Design a workshop or learning path made of several GitHub Skills exercises, for instructor-led, self-paced, or hybrid delivery. Use when turning a half-day or full-day training into a sequence of exercises, planning prerequisites, spacing and a capstone, preparing an organization or EMU enterprise to run exercises, writing a facilitator guide or agenda, or deciding how to evaluate a workshop.
---

# Workshop design with GitHub Skills

A GitHub Skills exercise teaches one skill in about 30 to 45 minutes, in five steps or fewer. A workshop is a
sequence of exercises plus the human parts around them: setup, facilitation, breaks, help, and evaluation. This
skill designs that whole experience.

## Workflow

1. **Frame the workshop.** Audience (load `learning-design` for the persona), the capability learners should
   have at the end, delivery mode (instructor-led, self-paced, hybrid), duration, and environment (personal
   accounts, a learning organization, or an Enterprise Managed User (EMU) enterprise).
2. **Map the curriculum.** List the capabilities, then split them into exercises that each teach one new skill.
   Check the [GitHub Skills catalog](https://learn.github.com/skills) first and reuse published exercises where
   they fit; author only the gaps. See [references/sequencing.md](references/sequencing.md).
3. **Sequence for retention.** Draw the prerequisite graph, spiral earlier skills into later exercises
   without reprinting their instructions, remember that every exercise is a separate repository copy, and end
   with a capstone that integrates the skills.
4. **Timebox realistically.** Budget setup time, learner pace (often several times expert pace), breaks,
   checkpoints, and an asynchronous continuation route. Test the timing in a dry run.
5. **Prepare the environment.** Accounts, organization settings, Codespaces, Copilot plans, Actions policy and
   allowlists, repository naming in shared organizations, and costs. See
   [references/delivery-and-logistics.md](references/delivery-and-logistics.md).
6. **Plan facilitation.** Roles, help channel, a stuck-learner protocol, and fixes for the common failures.
7. **Run preflight.** Walk through every exercise end to end with the `exercise-walkthrough-test` skill using
   an account configured like a participant's, then complete
   [assets/preflight-checklist.md](assets/preflight-checklist.md).
8. **Plan evaluation.** Reaction, learning (a less-supported task), later behavior, and cautious results. See
   [references/evaluation.md](references/evaluation.md).

## Deliverables

| Artifact | Template | Audience |
| --- | --- | --- |
| Workshop plan (outcomes, sequence, agenda, environment, evaluation) | [assets/workshop-plan.md](assets/workshop-plan.md) | Organizers |
| Facilitator guide (scripts, timings, troubleshooting, resets) | [assets/facilitator-guide.md](assets/facilitator-guide.md) | Facilitators |
| Preflight checklist | [assets/preflight-checklist.md](assets/preflight-checklist.md) | Organizers, admins |
| One outline per new exercise | `exercise-outline` skill | Authors |

## Rules

- One new skill per exercise. If a module needs more than five steps, it is two exercises.
- Never assume state carries over between exercises. Each one starts from its own template copy; provide
  starter files for anything a later exercise needs.
- Put a short retrieval moment at the start of each later exercise ("Create a branch for this work, as you did
  in the first exercise").
- Plan breaks and pacing from tested timings, not from an attention-span rule.
- Give every learner a way to finish asynchronously (the exercises keep working after the session).
- In shared organizations, tell learners to add a suffix to the suggested repository name to avoid
  collisions.
- Use a dedicated learning organization for EMU enterprises, as GitHub Skills recommends.
- Ask permission before collecting any learner data, and never collect repository contents or secrets.

## Output

Return the workshop plan using the template, then list the new exercises to author with one-line objectives,
and the reused catalog exercises with links.
