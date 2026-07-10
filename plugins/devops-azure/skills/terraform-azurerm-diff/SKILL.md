---
name: Terraform AzureRM diff analysis
description: Use this skill when you need to interpret Terraform AzureRM plan changes, detect drift, and explain the operational impact of resource updates.
---

# Terraform AzureRM diff analysis

## Use this skill when
- You need to review a Terraform plan that targets AzureRM resources.
- The plan contains noisy diffs and you must separate cosmetic churn from real infrastructure change.
- A pipeline or pull request needs a clear impact assessment before apply.

## Gather the right inputs
1. Use a fresh plan generated from the intended workspace, backend, and variable set.
2. Prefer `terraform show -json` or a saved plan file when you need machine-readable review.
3. Capture the provider version, module versions, and any recent state operations that may explain drift.

## Classify change types
- Separate creates, in-place updates, deletes, and forced replacements.
- Flag replacements immediately because they can imply downtime, data loss, or IP changes.
- Distinguish tag-only or metadata-only changes from service-impacting configuration changes.
- Note when a child resource change is actually driven by a parent identity, name, or SKU update.

## Azure-specific review points
- Check immutable properties such as resource names, location, SKU families, or subnet bindings.
- Review identity, networking, private endpoint, firewall, and DNS changes for blast radius.
- Watch for managed identity principal changes that require downstream role assignment updates.
- Inspect app settings, connection strings, or secret references for accidental drift or redaction noise.

## Drift detection
- Compare the plan against expected code changes; unexplained changes may indicate manual drift.
- Confirm whether drift comes from portal edits, policy remediation, autoscaling, or provider normalization.
- Investigate recurring false positives and document accepted noise patterns per resource type.
- Refresh state deliberately; do not hide drift by blindly applying a plan you do not understand.

## Risk assessment
- Estimate service interruption, data movement, security posture change, and rollback difficulty.
- Call out any changes that affect public ingress, certificates, storage lifecycle, or encryption settings.
- Identify dependencies on maintenance windows, DNS propagation, or staged cutovers.
- Recommend manual approval for destructive or customer-visible changes.

## Review workflow
- Summarize module path and resource addresses for every meaningful change.
- Group related resources so reviewers can see the intended architectural move.
- Ignore reordered JSON, provider-computed defaults, or timestamp churn unless they have side effects.
- When possible, link suspicious diffs back to the exact HCL line or module input that produced them.

## Deliverable format
- Provide a concise resource-by-resource summary.
- Separate harmless noise from material risk.
- Explain any drift hypotheses and what to verify before apply.
- End with a clear recommendation: safe to apply, needs investigation, or blocked.
