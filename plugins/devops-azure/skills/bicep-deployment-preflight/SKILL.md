---
name: Bicep deployment preflight
description: Use this skill when you need to validate Azure Bicep deployments before execution with build checks, parameter validation, what-if analysis, and policy awareness.
---

# Bicep deployment preflight

## Use this skill when
- You are preparing to deploy Azure infrastructure defined in Bicep.
- You need a safer review step before merging or running a live deployment.
- A deployment has failed before and you want a disciplined preflight checklist.

## Preflight inputs
1. Identify the deployment scope: resource group, subscription, management group, or tenant.
2. Collect the Bicep entry point, modules, parameter files, and target environment naming rules.
3. Confirm required providers, regions, quotas, identities, and policy constraints.

## Syntax and compilation checks
- Run `az bicep build` or equivalent validation to catch syntax, type, and module reference issues.
- Resolve linter warnings that indicate broken defaults, unused params, or unsafe patterns.
- Verify external module references and template specs are reachable and version-pinned where appropriate.
- Ensure generated ARM JSON is not unexpectedly large or duplicated.

## Parameter validation
- Check that every required parameter is provided for the target environment.
- Validate allowed values, naming conventions, SKU compatibility, and location constraints.
- Confirm secrets come from secure sources such as Key Vault references or pipeline secrets.
- Review defaults carefully so non-production values never leak into production deployments.

## What-if and impact review
- Run the correct `az deployment <scope> what-if` command for the target scope.
- Review creates, updates, deletes, and replacements separately; replacements deserve special scrutiny.
- Investigate any delete or replace actions caused by name changes, mode differences, or immutable properties.
- Compare the what-if output against the intended change request, not just against the template.

## Policy, RBAC, and environment readiness
- Check Azure Policy assignments that may block SKUs, regions, public networking, or tagging requirements.
- Verify the deploying identity has permissions for all resource providers and nested scopes.
- Confirm provider registration and regional capacity for the resources being introduced.
- Validate dependencies on existing VNets, subnets, Key Vaults, or identities before deployment time.

## CI/CD recommendations
- Run build, lint, parameter validation, and what-if on every pull request for infra changes.
- Persist what-if output as an artifact for human review and approval workflows.
- Use environment-specific parameter files and explicit scopes instead of hidden defaults.
- Block merge when the preflight output includes unexplained destructive changes.

## Deliverable format
- State the deployment scope, entry file, and parameter set.
- Summarize syntax, policy, and readiness checks.
- Highlight risky what-if findings such as deletes, replacements, or policy conflicts.
- End with the exact remediation or approval recommendation.
