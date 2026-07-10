---
name: brownfield-import
description: Import brownfield Azure resources into Terraform using import blocks
---

Use this skill when onboarding existing Azure resources into Terraform management without recreating them.

# Goal

Faithfully import brownfield Azure resources into Terraform using `import {}` blocks so the plan becomes zero-diff against the live estate.

# Workflow

1. Use the Azure CLI to enumerate every resource in resource group `rg-brownfield-demo` for the currently selected subscription.
2. For each discovered resource:
   - Add an `import {}` block in `imports.tf`
   - Set `to` to the Terraform resource address you will define
   - Set `id` to the full Azure resource ID returned by `az`
3. Add the matching `resource {}` block in the correct file:
   - Resource groups → `imports.tf`
   - Storage accounts → `storage.tf`
   - Virtual networks, subnets, and NSGs → `network.tf`
4. Follow the Azure landing-zone repository conventions and guardrails.
5. Preserve reality during import:
   - Do not “fix” policy violations during this step
   - Use `local.required_tags` when tags already align with the convention
   - Otherwise preserve existing live tags from Azure

# Validation

- Run `terraform fmt -recursive`
- Run `terraform plan`
- Confirm the summary is exactly **0 to add, 0 to change, 0 to destroy**

# Hard rules

- Do **not** run `terraform apply`
- Do **not** delete existing resources
- Use `import {}` blocks, never the `terraform import` CLI
- Keep imports and resource definitions aligned so state matches reality exactly
