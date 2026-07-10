---
name: drift-remediation
description: Remediate configuration drift detected between Terraform and Azure
---

Use this skill when a scheduled drift check reports that Azure resources no longer match Terraform state or configuration.

# Goal

Reconcile drift with the minimum Terraform changes while enforcing landing-zone guardrails.

# Workflow

1. Read the linked GitHub issue created by `drift.yml` and inspect the included `terraform plan` diff.
2. Determine whether each out-of-band change is policy-compliant.
   - If it violates landing-zone policy, re-assert the Terraform value in code.
   - If it is benign and policy-compliant, update Terraform to match reality so the environment is no longer drifted.
3. Edit only the necessary `*.tf` files to reconcile the drift.
4. Run:
   - `terraform fmt -recursive`
   - `terraform validate`
5. Run `terraform plan` and confirm the resulting diff matches the intended remediation.
6. Do **not** run `terraform apply`.

# Pull request requirements

- Target branch: `main`
- Branch name: `drift/remediate-<short-description>`
- Include in the PR body:
  - A link to the originating drift issue
  - A bulleted list of the `LZ-*` rules satisfied by the change
  - The `terraform plan` summary showing adds / changes / destroys
  - The exact sentence: `This PR reconciles drift detected by \`drift.yml\`.`

# Decision rules

- Prefer restoring secure, policy-approved Terraform values over normalizing unauthorized portal changes.
- When drift reveals a policy violation such as public network exposure, do not update code to match the insecure live state.
- Keep the change set minimal and focused on drift reconciliation.
