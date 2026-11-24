# Maintaining exercises

Exercises teach live products. UIs change, actions get new majors, and learners find gaps. Plan maintenance like
any other product.

## Cadence

| When | Do |
| --- | --- |
| Monthly, or when the product area ships changes (see the [GitHub Changelog](https://github.blog/changelog/)) | Observe-mode walkthrough test of every step |
| When `skills/exercise-toolkit` publishes a release | Read the release notes; upgrade every reference together; validate; walkthrough |
| Before every workshop | Full walkthrough from a participant-like account; preflight checklist |
| When a learner reports an issue | Reproduce with the harness `status` and `timeline` on their copy (with permission) |
| Quarterly | Review stopping points, feedback themes, and links; prune or split content |

## Toolkit and action upgrades

1. `gh release list --repo skills/exercise-toolkit` and read the notes for the new tag.
2. Re-read the `workflow_call` inputs and outputs of `start-exercise.yml`, `find-exercise-issue.yml`, and
   `finish-exercise.yml` at the new tag.
3. Replace the tag in every `uses: skills/exercise-toolkit/...` and every toolkit checkout `ref:`.
4. Check third-party actions (`actions/checkout`, `GrantBirki/comment`, `peter-evans/find-comment`,
   `skills/action-keyphrase-checker`) for new majors and breaking changes; keep EMU allowlist compatibility in
   mind.
5. `validate_exercise.py --online`, then a walkthrough test.

## UI drift

- The walkthrough's UI fidelity table lists labels, locations, and screenshots that no longer match.
- Update text first; replace screenshots only when words cannot carry the change.
- Record changes in release notes so facilitators know.

## Feedback loop

1. Collect learner and facilitator feedback in one tracking issue per exercise.
2. Classify: content clarity, automation bug, environment, scope.
3. Turn recurring confusion into Having trouble bullets, clearer instructions, or a split step.
4. Re-test, release, and close the loop with the reporter.

## Deprecation

1. Review and close open issues and pull requests.
2. Add this banner at the top of the README:

   ```markdown
   ![Deprecation Badge](https://img.shields.io/badge/Skills-Deprecated-333?logo=github&labelColor=454c54&color=bf8700)

   This exercise has been deprecated. Please visit the [New Exercise Name](https://github.com/<owner>/<new-exercise>) exercise for the newest learning content.
   ```

3. Remove it from catalogs and workshop plans; keep the repository readable for existing learners.
