# Preflight checklist: (replace-me: workshop title)

Complete at least two working days before the session. Use an account configured like a participant's.

## Accounts and access

- [ ] Every participant has a GitHub account (or EMU account) and knows which owner to copy exercises into.
- [ ] Copilot plan and policies cover every Copilot feature the exercises use.
- [ ] Participants can create repositories in the target organization (member repository creation).

## Organization settings (if not using personal accounts)

- [ ] Dedicated learning organization (recommended for EMU).
- [ ] Codespaces enabled for members, with quota or spending limit set.
- [ ] Actions policy allows all actions, or the allowlist includes the
      [GitHub Skills allowlist](https://github.com/skills/skills-for-emu/tree/main/actions-allowlist) plus any
      action used by custom exercises.
- [ ] Default workflow permissions do not block exercises (exercises declare their own permissions).

## Exercises

- [ ] Each custom exercise passes `validate_exercise.py` with no blocking findings.
- [ ] Each exercise passes a walkthrough test end to end (exercise-walkthrough-test skill), including at least one
      failed check and recovery.
- [ ] Template repositories are public (or visible to participants), marked as templates, with step workflows
      disabled.
- [ ] Copy Exercise buttons point at the right owner and template.
- [ ] Tested time per exercise recorded in the workshop plan.

## Logistics

- [ ] Agenda shared; pre-work sent with links.
- [ ] Help channel ready; helpers briefed with the facilitator guide.
- [ ] Accessibility: materials shared in advance; captions for any video; keyboard-only route checked.
- [ ] Backup plan documented (for example, a local setup if Codespaces fails).
- [ ] Survey and evaluation instruments ready.
