---
name: exercise-publish
description: Publish, transfer, update, maintain, or deprecate a GitHub Skills exercise repository safely - explicit authorization, Actions disabled during the first push, template flag, description and topics, repository settings, all step workflows disabled, Copy Exercise button fixed, a post-publish walkthrough, release notes, toolkit upgrades and deprecation banners. Use when the user wants an exercise live in an account or organization, moved between organizations, updated after release, or retired.
---

# Publish and maintain an exercise

Publishing changes remote state in the user's account. Nothing here runs without explicit authorization that
names the target owner, repository name, and visibility. An approved name in the outline is not authorization.

## Before publishing (gate)

- [ ] Independent review signed off with no blocking findings (`exercise-review`).
- [ ] `validate_exercise.py --online` reports no blocking findings.
- [ ] Walkthrough test passed against a staging template built from the same commit, including a failed check and
      recovery (`exercise-walkthrough-test`, Path S below).
- [ ] Copy Exercise button, LICENSE, and README footer use the final owner, repository name, year, and holder.
- [ ] The user authorized: "Publish to `<owner>/<name>` as `<public|private|internal>`."

## Visibility

Use exactly the visibility the user authorized; never default to public.

| Visibility | Use when | Copy Exercise link |
| --- | --- | --- |
| `public` | Open exercises; learner copies in personal accounts do not use paid Actions minutes | `visibility=public` |
| `private` | Content must stay private (customer or internal material) | `visibility=private` |
| `internal` | Enterprise-wide exercises in an enterprise organization | `visibility=private` (learners choose the owner) |

Never publish or stage a private or internal exercise as public, and never change an existing repository's
visibility without separate, explicit authorization (`gh repo edit --visibility` also requires
`--accept-visibility-change-consequences`).

## Path A: new repository in an account or organization

Run each command, check its result, and stop on failure. `<repo>` is `owner/name`; `<visibility>` is the
authorized one.

```bash
# 1. Create an empty remote repository (no files yet).
gh repo create <repo> --<visibility> --description "<one-line promise from the README>"

# 2. Disable Actions so the first push cannot run anything.
gh api -X PUT repos/<repo>/actions/permissions -F enabled=false

# 3. Mark it as a template and set features and merge settings.
gh repo edit <repo> --template --enable-wiki=false --enable-projects=false --enable-discussions=false \
  --enable-merge-commit=false --enable-rebase-merge=false --enable-squash-merge --delete-branch-on-merge
gh repo edit <repo> --add-topic skills-exercise

# 4. Push exactly the reviewed and tested commit (from the exercise folder). If `origin` already exists,
#    check it with `git remote get-url origin` and point it here with `git remote set-url origin <url>`.
git remote add origin https://github.com/<repo>.git
git push origin <reviewed-sha>:refs/heads/main

# 5. Disable every workflow, then re-enable Actions.
gh workflow list -R <repo> --all
gh workflow disable "Step 0" -R <repo>   # repeat for every "Step N"
gh api -X PUT repos/<repo>/actions/permissions -F enabled=true
```

If step 5 lists no workflows while Actions is disabled, re-enable Actions first and then disable each workflow:
the push already happened while Actions was off, so nothing runs in between.

Then verify:

- `gh api repos/<repo> --jq .is_template` is `true`.
- `gh workflow list -R <repo> --all` shows every step workflow as `disabled_manually`.
- The README's Copy Exercise button opens "Create a new repository" with this template selected.
- A short walkthrough from the published template passes (at least the start and step 1).

If the push fails for permissions, ask the user to push manually and continue from step 5.

## Path S: staging template for walkthrough tests

A walkthrough copies a template's default branch, so an unpublished exercise or an unmerged change needs a
staging template that holds exactly the reviewed commit. With explicit authorization naming owner, name, and
visibility (the final visibility, or private):

```bash
# 1. Create the staging repository and make it a template with Actions off (as in Path A, steps 1 to 3).
gh repo create <staging> --<visibility> --description "Staging: <exercise title>"
gh api -X PUT repos/<staging>/actions/permissions -F enabled=false
gh repo edit <staging> --template

# 2. Push exactly the reviewed commit to the staging default branch through its own remote, so the final
#    publication (origin) is untouched. For an update, <reviewed-sha> is the pull request's head commit.
git remote add staging https://github.com/<staging>.git
git push staging <reviewed-sha>:refs/heads/main

# 3. Disable every step workflow, then re-enable Actions (as in Path A, step 5).
```

Then:

1. Do not edit the commit: the README's Copy Exercise button keeps pointing at the final repository. The walkthrough
   checks the badge's parameters as text and creates the copy with the staging repository's **Use this template**
   button (or the harness `create`).
2. Confirm the staged commit is the reviewed one: `exercise_harness.py preflight --template <staging>` must report
   `head_sha` equal to `<reviewed-sha>`.
3. Run the walkthrough test against the staging template.
4. After it passes, publish the same `<reviewed-sha>` to the final repository with Path A (push it with
   `git push origin <reviewed-sha>:refs/heads/main`), then archive or delete the staging repository with separate
   approval and remove the `staging` remote.

## Path B: transfer between organizations

1. Confirm the user is an admin of the source and can create repositories in the destination.
2. Get explicit authorization naming source and destination.
3. `gh api -X POST repos/<source-owner>/<name>/transfer -f new_owner=<destination-owner>`
4. Update `template_owner` in the Copy Exercise button, commit through a pull request, and verify the workflows
   are still disabled and the template flag is still set.
5. Old URLs redirect, but update links in catalogs and other exercises.

## Path C: update a published exercise

1. Work on a branch; open a pull request in the template repository.
2. Workflows in the template stay disabled; Step 0 is guarded by `is_template`, so merging does not start an
   exercise in the template.
3. Re-run the validator and a walkthrough test against a copy made from the branch (or after merge).
4. Add release notes (what changed, why, any action needed by facilitators).

Learners who already copied the exercise keep their version. Tell facilitators when an update changes
instructions mid-workshop.

## Organization and EMU notes

- Publishing into a learning organization: confirm members can see the template (public, or internal or private
  with access) and that the Actions policy allows every action the exercise uses.
- Private templates: set `visibility=private` in the Copy Exercise link so copies do not expose the content, and
  warn that private copies use Actions minutes.

## Maintenance

See [references/maintenance.md](references/maintenance.md) for the cadence, toolkit upgrades, UI drift, the
feedback loop, and deprecation. The release checklist is in
[references/release-checklist.md](references/release-checklist.md).

## Output

```markdown
## Publish report: <owner>/<name>

- **Authorization:** <quote of the user's approval>
- **Actions taken:** <commands and results>
- **Verification:** template flag, workflows disabled, Copy Exercise target, walkthrough result
- **Release notes:** <summary>
- **Follow-ups:** <catalog links, facilitator notice, remaining risks>
```
