# Release checklist

Combines the exercise-creator [repository files](https://github.com/skills/exercise-creator/blob/main/docs/guide/checklist/repository-files.md),
[repository settings](https://github.com/skills/exercise-creator/blob/main/docs/guide/checklist/repository-settings.md),
and [publishing](https://github.com/skills/exercise-creator/blob/main/docs/guide/checklist/publishing.md) checklists
with this plugin's quality gates.

## Files

- [ ] `.gitignore` covers OS and build artifacts; `LICENSE` present.
- [ ] README current, prerequisites minimal and complete, Copy Exercise owner and name correct, footer with
      copyright, Code of Conduct, and license.
- [ ] All steps in `.github/steps/`, images stored in the repository and referenced relatively.
- [ ] Tense, tone, and terminology consistent; spell check clean; acronyms explained.
- [ ] Sample code has intuitive comments; setup is automated in the codespace.
- [ ] Workflows give useful feedback for common mistakes; the final workflow posts the review and updates the
      README.

## Quality gates

- [ ] `validate_exercise.py --online`: no blocking findings; important findings resolved or accepted with reasons.
- [ ] Independent review signed off.
- [ ] Walkthrough test passed with at least one failed check and recovery per graded step.
- [ ] Testers matching the persona completed it; their feedback is tracked in an issue.

## Repository settings

- [ ] Repository name and description final; template flag on.
- [ ] Wiki, Projects, and Discussions disabled (unless the exercise uses them).
- [ ] Squash merging only; delete head branches automatically.
- [ ] Branch ruleset on the default branch: linear history, pull request before merging.
- [ ] Dependabot and Copilot Autofix disabled on the template.
- [ ] Collaborators: the responsible owner is an admin; organization team access set.
- [ ] Actions tab: every step workflow disabled.

## During release

- [ ] Not a Friday afternoon (exercise-creator wisdom).
- [ ] Visibility set as authorized.

## After release

- [ ] Close the tracking issue with the release date.
- [ ] Add release notes; announce to facilitators.
- [ ] Add the exercise to your catalog or workshop plan.
- [ ] Thank the testers with specifics.
